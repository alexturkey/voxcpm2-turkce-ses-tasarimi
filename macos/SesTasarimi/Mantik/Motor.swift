import Foundation

/// Yamalı audio.cpp motorunu tek oturumda istek dizisiyle çalıştırır. Port of `ses_tasarim/motor.py`.
/// Kalite sabit: 16 adım, cfg 2.0. Tohum kalite ayarı değildir: tasarımda çeşitlilik, okumada sesin kendi tohumu.
enum Motor {
    static let adim = 16
    static let cfg = 2.0
    static let ornekleme = 48000
    static let metinParcasi = 2048
    // referans kodlayıcı örnek kapasitesi: motor varsayılanı 240000 (16 kHz, 15 sn); tasarım kayıtları 20-35 sn → 36 sn
    static let referansSecenegi = ["--session-option", "voxcpm2.audiovae_encoder_sample_capacity=576000"]
    static let enAzReferansSn = 8.0
    static let audiovaeIsParcacigi = 6
    static let motorIsParcacigi = 4

    struct Istek {
        var kimlik: String
        var metin: String
        var tohum: UInt32
        var referans: URL? = nil
        var referansMetni: String? = nil

        var json: [String: Any] {
            var d: [String: Any] = ["id": kimlik, "text": metin, "seed": Int(tohum),
                                    "num_inference_steps": Motor.adim, "guidance_scale": Motor.cfg,
                                    "text_chunk_size": Motor.metinParcasi,
                                    "max_tokens": 80 + Int(Double(metin.unicodeScalars.count) * 1.2)]
            if let referans, let referansMetni {
                // tasarım kaydı iki girişe birden (audio + voice_ref), yanında okunan metni (reference_text)
                d["audio"] = referans.path
                d["voice_ref"] = referans.path
                d["reference_text"] = referansMetni.trimmingCharacters(in: .whitespacesAndNewlines)
            }
            return d
        }
    }

    static func tasarimIstegi(_ kimlik: String, tarif: String, metin: String, tohum: UInt32) -> Istek {
        // tarif parantez içinde metnin önüne; parantez prompt sınırıdır
        Istek(kimlik: kimlik, metin: "(\(tarif.trimmingCharacters(in: .whitespacesAndNewlines)))\(metin.trimmingCharacters(in: .whitespacesAndNewlines))",
              tohum: tohum)
    }

    static func okumaIstegi(_ kimlik: String, metin: String, tohum: UInt32, referans: URL, referansMetni: String) -> Istek {
        Istek(kimlik: kimlik, metin: metin, tohum: tohum, referans: referans, referansMetni: referansMetni)
    }

    /// 4 GB sığdırma ve hız ayarları; yalnız motor sürecine verilir. / 4 GB fit + speed env, engine process only.
    static func ortam(onbellek: URL, calisma: URL) -> [String: String] {
        var env = ProcessInfo.processInfo.environment
        env.merge([
            "VOXCPM2_KV_CAPACITY": "auto",                       // KV önbelleği gerektiği kadar (yama a)
            "VOXCPM2_AUDIOVAE_CPU": "1",                         // AudioVAE kodlayıcı CPU'da (yama a)
            "VOXCPM2_AUDIOVAE_THREADS": String(audiovaeIsParcacigi),
            "VOXCPM2_AUDIOVAE_GPU_CHUNK": "10",                  // LM boşalt, çözücü GPU'da 10 sn dilimlerle (yama b)
            "VOXCPM2_TOPLU_COZ": "1",                            // önce bütün satırlar, sonra tek seferde çözüm (yama c5)
            "VOXCPM2_PROMPT_CACHE_DIR": onbellek.path,           // referans kodlaması diske (yama c4)
            "VOXCPM2_PROBE_EOS_CONFIRMATIONS": "2",
            "VOXCPM2_PROBE_POSITION_CONSENSUS": "8",
            "VOXCPM2_PROBE_ACOUSTIC_RESCUE": "1",
            "VOXCPM2_PROBE_HOLD_UNTIL": "0",
            "VOXCPM2_PROBE_DISABLE_EOS": "0",
            "VOXCPM2_PROBE_FULL_TRACE": "0",
            "VOXCPM2_PROBE_PCM_DIR": calisma.path,
        ]) { _, yeni in yeni }
        return env
    }

    /// Her istek bloğu `toplu_coz.deferred` ile biter; EOS'suz blok yarım ses demektir. Log parça parça okunur.
    struct EOSIzleyici {
        private(set) var tamam: [Bool]
        private var blok = 0
        private var artik = Data()
        private var konum: UInt64 = 0

        init(sayi: Int) { tamam = Array(repeating: false, count: sayi) }

        mutating func satirIsle(_ satir: Substring) {
            if blok < tamam.count, satir.contains("eos_accepted_at_patch") { tamam[blok] = true }
            if satir.contains("voxcpm2.toplu_coz.deferred") { blok += 1 }
        }

        mutating func oku(_ log: URL) {
            guard let tutamac = try? FileHandle(forReadingFrom: log) else { return }
            defer { try? tutamac.close() }
            try? tutamac.seek(toOffset: konum)
            guard let yeni = try? tutamac.readToEnd(), !yeni.isEmpty else { return }
            konum += UInt64(yeni.count)
            artik.append(yeni)
            guard let sonSatirSonu = artik.lastIndex(of: UInt8(ascii: "\n")) else { return }
            let tam = String(decoding: artik[..<sonSatirSonu], as: UTF8.self)
            artik = Data(artik[artik.index(after: sonSatirSonu)...])
            for satir in tam.split(separator: "\n", omittingEmptySubsequences: false) { satirIsle(satir) }
        }

        mutating func bitir(_ log: URL) {
            oku(log)
            if !artik.isEmpty { satirIsle(Substring(String(decoding: artik, as: UTF8.self))); artik = Data() }
        }
    }

    struct Sonuc {
        var sesler: [String: [Int16]]
        var bozuk: [String]
        var saniye: Double
        var gpuTepeMB: Int
    }

    struct Ilerleme: Sendable {
        var biten: Int
        var toplam: Int
        var gecen: Double
        var gpuMB: Int
    }

    /// İstekleri tek motor oturumunda üretir (model bir kez yüklenir). / One engine session for all requests.
    static func calistir(motor: URL, model: URL, onbellek: URL, istekler: [Istek], calisma: URL,
                         ilerleme: (@Sendable (Ilerleme) -> Void)? = nil) async throws -> Sonuc {
        let fm = FileManager.default
        try fm.createDirectory(at: calisma, withIntermediateDirectories: true)
        try fm.createDirectory(at: onbellek, withIntermediateDirectories: true)
        let dizi = calisma.appendingPathComponent("dizi.json")
        try JSONSerialization.data(withJSONObject: ["requests": istekler.map(\.json)],
                                   options: [.prettyPrinted, .withoutEscapingSlashes]).write(to: dizi)
        let log = calisma.appendingPathComponent("motor.log")
        let stdout = calisma.appendingPathComponent("stdout.txt")
        fm.createFile(atPath: stdout.path, contents: nil)

        let surec = Process()
        surec.executableURL = motor
        surec.arguments = ["--model", model.path, "--task", "tts", "--backend", "metal",
                           "--threads", String(motorIsParcacigi), "--request-sequence", dizi.path]
            + referansSecenegi
            + ["--out-dir", calisma.appendingPathComponent("out").path,
               "--batch-manifest-out", calisma.appendingPathComponent("manifest.json").path,
               "--log", "--log-file", log.path, "--metrics"]
        surec.environment = ortam(onbellek: onbellek, calisma: calisma)
        surec.currentDirectoryURL = calisma
        let cikis = try FileHandle(forWritingTo: stdout)
        surec.standardOutput = cikis
        surec.standardError = cikis
        defer { try? cikis.close() }

        let baslangic = Date()
        var izleyici = EOSIzleyici(sayi: istekler.count)
        var tepe = GPUBellek.kullanilanMB() ?? 0
        try surec.run()
        Motor.calisanSurec.deger = surec
        defer {
            Motor.calisanSurec.deger = nil
            if surec.isRunning { surec.terminate(); surec.waitUntilExit() }
        }
        try await withTaskCancellationHandler {
            while surec.isRunning {
                try await Task.sleep(for: .milliseconds(500))
                tepe = max(tepe, GPUBellek.kullanilanMB() ?? 0)
                izleyici.oku(log)
                ilerleme?(Ilerleme(biten: izleyici.tamam.filter { $0 }.count, toplam: istekler.count,
                                   gecen: Date().timeIntervalSince(baslangic), gpuMB: tepe))
            }
        } onCancel: {
            // iptal ya da hata: motor yetim kalmasın / never orphan the engine
            if surec.isRunning { surec.terminate() }
        }
        surec.waitUntilExit()
        if Task.isCancelled { throw CancellationError() }
        guard surec.terminationStatus == 0 else {
            let kuyruk = (try? String(contentsOf: stdout, encoding: .utf8)).map { String($0.suffix(1500)) } ?? ""
            throw SesHatasi("motor rc=\(surec.terminationStatus); \(stdout.path)\n\(kuyruk)")
        }
        izleyici.bitir(log)
        var sesler: [String: [Int16]] = [:]
        var bozuk: [String] = []
        for (istek, bitti) in zip(istekler, izleyici.tamam) {
            let wav = calisma.appendingPathComponent("out/\(istek.kimlik).wav")
            guard bitti, fm.fileExists(atPath: wav.path) else { bozuk.append(istek.kimlik); continue }
            let ses = try Wav.oku(wav)
            guard ses.oran == ornekleme else { throw SesHatasi("beklenmeyen örnekleme \(ses.oran)") }
            sesler[istek.kimlik] = ses.ornekler
        }
        return Sonuc(sesler: sesler, bozuk: bozuk, saniye: (Date().timeIntervalSince(baslangic) * 10).rounded() / 10,
                     gpuTepeMB: tepe)
    }

    /// Uygulama kapanırken motoru durdurmak için. / So quitting the app also stops the engine.
    final class SurecKutusu: @unchecked Sendable {
        private let kilit = NSLock()
        private var _deger: Process?
        var deger: Process? {
            get { kilit.withLock { _deger } }
            set { kilit.withLock { _deger = newValue } }
        }
    }
    static let calisanSurec = SurecKutusu()

    static func cihazlar(motor: URL) -> String {
        let surec = Process()
        surec.executableURL = motor
        surec.arguments = ["--list-devices"]
        let boru = Pipe()
        surec.standardOutput = boru
        surec.standardError = boru
        guard (try? surec.run()) != nil else { return "" }
        let veri = boru.fileHandleForReading.readDataToEndOfFile()
        surec.waitUntilExit()
        return String(decoding: veri, as: UTF8.self)
    }
}

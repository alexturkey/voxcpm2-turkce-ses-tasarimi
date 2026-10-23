import Foundation

/// Tasarım, okuma ve klonlama. Port of `tasarla.py`, `oku.py`, `klonla.py`.
struct Islemler: Sendable {
    let depo: Depo
    typealias IlerlemeBildir = @Sendable (Motor.Ilerleme) -> Void

    func motorYolu() throws -> URL {
        guard let motor = depo.motor, FileManager.default.isExecutableFile(atPath: motor.path) else {
            throw SesHatasi("motor uygulamanın içinde bulunamadı (audiocpp_cli)")
        }
        return motor
    }

    // MARK: - 1. Tasarım

    static let varsayilanCesit = 3

    struct Cesit: Identifiable, Sendable {
        var id: UInt32 { tohum }
        let tohum: UInt32
        var kart: SesKarti? = nil
        var referansSn: Double = 0
        var hata: String? = nil
        var uyari: String? = nil
    }

    struct TasarimSonucu: Sendable {
        let ses: String
        let cesitler: [Cesit]
        let sureSn: Double
        let gpuTepeMB: Int
    }

    static func tohumlar(_ sayi: Int) -> [UInt32] {
        var secilen = Set<UInt32>()
        while secilen.count < max(1, sayi) { secilen.insert(UInt32.random(in: .min ... .max)) }
        return secilen.sorted()
    }

    static func kisaAd(_ ad: String) -> String {
        let harita: [Character: Character] = ["ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
                                              "Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"]
        let ascii = String(ad.map { harita[$0] ?? $0 }).lowercased()
        let parca = String(ascii.map { $0.isLetter || $0.isNumber ? $0 : " " }).split(separator: " ")
        return parca.isEmpty ? "ses" : parca.joined(separator: "_")
    }

    static func tasarimDenetle(ad: String, tarif: String, metin: String) -> [String] {
        var bulunan: [String] = []
        if ad.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty { bulunan.append("sesin adı boş") }
        if tarif.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty { bulunan.append("tarif boş") }
        if tarif.contains("(") || tarif.contains(")") {
            bulunan.append("tarifte parantez olmaz (motor parantezi tarif sınırı sayar)")
        }
        return bulunan + Okunus.sorunlar(metin, yer: "ses yaratılırken okutulan metin")
    }

    func tasarla(ad: String, tarif: String, metin: String, cesit: Int, tohumlar verilen: [UInt32]? = nil,
                 ilerleme: IlerlemeBildir? = nil) async throws -> TasarimSonucu {
        let bulunan = Self.tasarimDenetle(ad: ad, tarif: tarif, metin: metin)
        guard bulunan.isEmpty else { throw SesHatasi("form eksik:\n  - " + bulunan.joined(separator: "\n  - ")) }
        let kurallar = try depo.kurallar()
        let soylenen = try Okunus.satirlar(Okunus.soylenen(metin, kurallar)).map(\.metin).joined(separator: " ")
        let fm = FileManager.default
        let sesKlasoru = depo.sesler.appendingPathComponent(Self.kisaAd(ad), isDirectory: true)
        try fm.createDirectory(at: sesKlasoru, withIntermediateDirectories: true)
        let mevcut = ((try? fm.contentsOfDirectory(atPath: sesKlasoru.path)) ?? []).filter { $0.hasPrefix("cesit_") }
        let tohumlar = verilen ?? Self.tohumlar(cesit)
        let istekler = tohumlar.map { Motor.tasarimIstegi("t_\($0)", tarif: tarif, metin: soylenen, tohum: $0) }
        let calisma = depo.calisma.appendingPathComponent("tasarim_\(Depo.zamanDamgasi())_\(UUID().uuidString.prefix(4))")
        let sonuc = try await Motor.calistir(motor: try motorYolu(), model: depo.model, onbellek: depo.onbellek,
                                             istekler: istekler, calisma: calisma, ilerleme: ilerleme)
        var cesitler: [Cesit] = []
        var numara = mevcut.count
        for istek in istekler {
            guard let ses = sonuc.sesler[istek.kimlik] else {
                cesitler.append(Cesit(tohum: istek.tohum, hata: "EOS gelmedi (yarım ses); başka tohumla yeniden dene"))
                continue
            }
            numara += 1
            var deneme = sesKlasoru.appendingPathComponent(String(format: "cesit_%02d", numara), isDirectory: true)
            while fm.fileExists(atPath: deneme.path) {
                numara += 1
                deneme = sesKlasoru.appendingPathComponent(String(format: "cesit_%02d", numara), isDirectory: true)
            }
            try fm.createDirectory(at: deneme, withIntermediateDirectories: false)
            // referans.wav motora geri verilir: etiketsiz düz PCM16 (motorun WAV okuyucusu için)
            try Wav.yaz(Wav.Ses(ornekler: ses, oran: Motor.ornekleme), deneme.appendingPathComponent("referans.wav"))
            let saniye = (Double(ses.count) / Double(Motor.ornekleme) * 100).rounded() / 100
            let kart: [String: Any] = [
                "ad": sesKlasoru.lastPathComponent, "gorunen_ad": ad.trimmingCharacters(in: .whitespacesAndNewlines),
                "cesit": numara,
                "ses_yaratici_ingilizce_prompt": tarif.trimmingCharacters(in: .whitespacesAndNewlines),
                "ses_yaratilirken_okutulan_metin": soylenen,
                "tasarim_tohumu": Int(istek.tohum), "okuma_tohumu": Int(istek.tohum),
                "referans": "referans.wav", "referans_sn": saniye, "model": depo.model.lastPathComponent,
                "adim": Motor.adim, "cfg": Motor.cfg, "yapay": true,
                "tarih": Depo.zamanDamgasi(bicim: "yyyy-MM-dd HH:mm"),
            ]
            try JSONYaz.yaz(kart, deneme.appendingPathComponent("ses.json"))
            var cesit = Cesit(tohum: istek.tohum,
                              kart: try SesKarti(klasor: deneme, kimlik: "\(sesKlasoru.lastPathComponent)/\(numara)", hazir: false),
                              referansSn: saniye)
            if saniye < Motor.enAzReferansSn {
                cesit.uyari = "referans \(saniye) sn < \(Motor.enAzReferansSn) sn; tasarım metnini uzat"
            }
            cesitler.append(cesit)
        }
        try? fm.removeItem(at: calisma)  // başarıda geçici motor dosyaları silinir; hatada tanı için kalır
        return TasarimSonucu(ses: sesKlasoru.lastPathComponent, cesitler: cesitler, sureSn: sonuc.saniye,
                             gpuTepeMB: sonuc.gpuTepeMB)
    }

    // MARK: - 2. Okuma

    struct OkumaSonucu: Sendable {
        let wav: URL
        let sesSn: Double
        let sureSn: Double
        let gpuTepeMB: Int
        let tohum: UInt32
        var rtf: Double { sesSn > 0 ? sureSn / sesSn : 0 }
    }

    /// Referanslı okuma: kayıt motorun iki girişine birden (audio + voice_ref), yanında referansın metni ve sesin
    /// kendi tohumu. Cümle cümle okunur, aralara durak konur.
    func oku(ses: SesKarti, metin: String, cikti: URL, onbellek: URL? = nil, etiket: Wav.Etiket = .okuma,
             dosyaAdi: String = "okuma.wav", ilerleme: IlerlemeBildir? = nil) async throws -> OkumaSonucu {
        let bulunan = Okunus.sorunlar(metin)
        guard bulunan.isEmpty else { throw SesHatasi("metin:\n  - " + bulunan.joined(separator: "\n  - ")) }
        let satirlar = try Okunus.satirlar(Okunus.soylenen(metin, try depo.kurallar()))
        let fm = FileManager.default
        let calisma = cikti.appendingPathComponent("_motor", isDirectory: true)
        try fm.createDirectory(at: calisma, withIntermediateDirectories: true)
        var referans = ses.referansURL
        if referans.pathExtension.lowercased() != "wav" {
            let hedef = calisma.appendingPathComponent(referans.deletingPathExtension().lastPathComponent + ".wav")
            _ = try Wav.pcm16eCevir(referans, hedef: hedef)
            referans = hedef
        }
        let istekler = satirlar.enumerated().map { sira, satir in
            Motor.okumaIstegi("s\(sira + 1)", metin: satir.metin, tohum: ses.okumaTohumu, referans: referans,
                              referansMetni: ses.referansMetni)
        }
        let sonuc = try await Motor.calistir(motor: try motorYolu(), model: depo.model, onbellek: onbellek ?? depo.onbellek,
                                             istekler: istekler, calisma: calisma, ilerleme: ilerleme)
        if !sonuc.bozuk.isEmpty {
            let numaralar = sonuc.bozuk.compactMap { Int($0.dropFirst()) }.map(String.init).joined(separator: ", ")
            throw SesHatasi("şu satırlar düzgün bitmedi (EOS yok): \(numaralar); cümleyi kısalt ya da yeniden dene")
        }
        let sesler = istekler.map { sonuc.sesler[$0.kimlik]! }
        let birlesik = Wav.birlestir(sesler, duraklar: satirlar.map(\.durakSn))
        let wav = cikti.appendingPathComponent(dosyaAdi)
        try Wav.yaz(Wav.Ses(ornekler: birlesik, oran: Motor.ornekleme), wav, etiket: etiket)

        var imlec = 0
        var kayitlar: [[String: Any]] = []
        for (sira, (ses, satir)) in zip(sesler, satirlar).enumerated() {
            let t0 = Double(imlec) / Double(Motor.ornekleme)
            imlec += ses.count
            kayitlar.append(["satir": sira + 1, "metin": satir.metin, "t0": (t0 * 1000).rounded() / 1000,
                             "t1": (Double(imlec) / Double(Motor.ornekleme) * 1000).rounded() / 1000])
            imlec += Int(satir.durakSn * Double(Motor.ornekleme))
        }
        let sesSn = (Double(birlesik.count) / Double(Motor.ornekleme) * 100).rounded() / 100
        try JSONYaz.yaz(["ses": ses.ad, "kimlik": ses.kimlik, "tohum": Int(ses.okumaTohumu), "adim": Motor.adim,
                         "cfg": Motor.cfg, "ses_sn": sesSn, "sure_sn": sonuc.saniye, "vram_tepe_mb": sonuc.gpuTepeMB,
                         "wav": wav.lastPathComponent, "satirlar": kayitlar, "yapay": true,
                         "tarih": Depo.zamanDamgasi(bicim: "yyyy-MM-dd HH:mm")],
                        cikti.appendingPathComponent("ozet.json"))
        try? fm.removeItem(at: calisma)
        return OkumaSonucu(wav: wav, sesSn: sesSn, sureSn: sonuc.saniye, gpuTepeMB: sonuc.gpuTepeMB, tohum: ses.okumaTohumu)
    }

    // MARK: - 3. Klonlama (yalnız kendi sesiniz ya da sahibinden açık izin alınmış ses)

    struct KlonSonucu: Sendable {
        let okuma: OkumaSonucu
        let referansSn: Double
        let notlar: [String]
    }

    func klonla(kayit: URL, kayitMetni: String, metin: String, cikti: URL, onay: Bool, tohum: UInt32 = Klon.varsayilanTohum,
                ilerleme: IlerlemeBildir? = nil) async throws -> KlonSonucu {
        // izin kapısı: onaysız hiçbir şey okunmaz, motor açılmaz / consent gate: nothing runs without it
        let bulunan = Klon.denetle(kayitMetni: kayitMetni, metin: metin, onay: onay)
        guard bulunan.isEmpty else { throw SesHatasi(bulunan.joined(separator: "\n")) }
        let fm = FileManager.default
        let gecici = fm.temporaryDirectory.appendingPathComponent("klon_\(UUID().uuidString)", isDirectory: true)
        defer { Klon.sil(gecici) }  // kayıt, metni ve kodlaması kalıcı tutulmaz (hata olsa da) / nothing persists
        let sesKlasoru = gecici.appendingPathComponent("ses", isDirectory: true)
        try fm.createDirectory(at: sesKlasoru, withIntermediateDirectories: true)
        let referans = try Klon.referansHazirla(kayit, hedef: sesKlasoru.appendingPathComponent("referans.wav"))
        let kart: [String: Any] = ["ad": "klon", "referans": "referans.wav", "okuma_tohumu": Int(tohum),
                                   "ses_yaratilirken_okutulan_metin": kayitMetni.split(whereSeparator: \.isWhitespace).joined(separator: " "),
                                   "yapay": true]
        try JSONYaz.yaz(kart, sesKlasoru.appendingPathComponent("ses.json"))
        let ses = try SesKarti(klasor: sesKlasoru, kimlik: "klon", hazir: false)
        // referans kodlama önbelleği kalıcı klasöre değil geçici klasöre / encoding cache goes to the temp folder
        let gecOkuma = gecici.appendingPathComponent("okuma", isDirectory: true)
        let okuma = try await oku(ses: ses, metin: metin, cikti: gecOkuma, onbellek: gecici.appendingPathComponent("onbellek"),
                                  etiket: .klon, dosyaAdi: "klon_synthetic.wav", ilerleme: ilerleme)
        try fm.createDirectory(at: cikti, withIntermediateDirectories: true)
        let wav = cikti.appendingPathComponent("klon_synthetic.wav")
        if fm.fileExists(atPath: wav.path) { try fm.removeItem(at: wav) }
        try fm.moveItem(at: okuma.wav, to: wav)
        // kayıt metni ozet.json'a yazılmaz / the transcript is not written to the summary
        try JSONYaz.yaz(["tur": "klon", "tohum": Int(tohum), "adim": Motor.adim, "cfg": Motor.cfg,
                         "referans_sn": referans.saniye, "notlar": referans.notlar, "ses_sn": okuma.sesSn,
                         "sure_sn": okuma.sureSn, "vram_tepe_mb": okuma.gpuTepeMB, "wav": wav.lastPathComponent,
                         "yapay": true, "not": Klon.yapayNotu, "onay": Klon.onayTR,
                         "tarih": Depo.zamanDamgasi(bicim: "yyyy-MM-dd HH:mm")],
                        cikti.appendingPathComponent("ozet.json"))
        return KlonSonucu(okuma: OkumaSonucu(wav: wav, sesSn: okuma.sesSn, sureSn: okuma.sureSn, gpuTepeMB: okuma.gpuTepeMB,
                                             tohum: tohum),
                          referansSn: referans.saniye, notlar: referans.notlar)
    }
}

/// Klonlama kuralları (ETHICS.md). Onay kapısı kaldırılmaz. / Cloning rules; the consent gate stays.
enum Klon {
    // motor referans kodlayıcı kapasitesi 576000 örnek @16 kHz = 36 sn (Motor.referansSecenegi)
    static let enCokSn = 36.0
    static let enAzSn = 3.0
    static let onerilen = 5.0...30.0
    static let enCokBayt = 25_000_000
    static let varsayilanTohum: UInt32 = 42
    static let onayTR = "Bu ses bana ait ya da sahibinden açık izin aldım; taklit, dolandırıcılık ya da yanıltma için kullanmayacağım."
    static let onayEN = "This voice is mine or I have the owner's explicit permission; I will not use it for impersonation, fraud or deception."
    static let yapayNotu = "AI-generated synthetic speech (VoxCPM2 voice cloning) / Yapay zekâ ile üretilmiş sestir"

    static func denetle(kayitMetni: String, metin: String, onay: Bool) -> [String] {
        var bulunan: [String] = []
        if onay != true { bulunan.append("izin onayı yok (consent missing): \(onayTR) / \(onayEN)") }
        if kayitMetni.trimmingCharacters(in: .whitespacesAndNewlines).unicodeScalars.count < 10 {
            bulunan.append("kaydın birebir metni zorunlu: kayıtta ne söyleniyorsa aynısını yazın (exact transcript of the recording required)")
        }
        return bulunan + Okunus.sorunlar(metin)
    }

    /// Kaydı mono PCM16 WAV'a çevirir; 3 sn altını reddeder, 36 sn üstünü kırpar. / Decode, mono, trim to 36 s.
    static func referansHazirla(_ kayit: URL, hedef: URL) throws -> (saniye: Double, notlar: [String]) {
        let boy = (try? kayit.resourceValues(forKeys: [.fileSizeKey]).fileSize) ?? 0
        if boy == 0 { throw SesHatasi("ses dosyası boş (empty recording)") }
        if boy > enCokBayt {
            throw SesHatasi("ses dosyası çok büyük (\(boy / 1_000_000) MB); 36 sn'lik bir kayıt yeter (file too large, max \(enCokBayt / 1_000_000) MB)")
        }
        let (saniye, ozgun) = try Wav.pcm16eCevir(kayit, hedef: hedef, enCokSaniye: enCokSn)
        var notlar: [String] = []
        if ozgun < enAzSn {
            throw SesHatasi(String(format: "kayıt çok kısa (%.1f sn); en az 3 sn, önerilen 5-30 sn (too short; at least 3 s, 5-30 s advised)", ozgun))
        }
        if ozgun > enCokSn {
            notlar.append(String(format: "kayıt %.1f sn idi, ilk 36 sn kullanıldı; kayıt metni yalnız bu kısmı içermeli / trimmed to the first 36 s, the transcript must match that part", ozgun))
        } else if !onerilen.contains(ozgun) {
            notlar.append(String(format: "kayıt %.1f sn; en iyi sonuç 5-30 sn temiz kayıtla / best with 5-30 s clean speech", ozgun))
        }
        return ((saniye * 100).rounded() / 100, notlar)
    }

    static func sil(_ klasor: URL) {
        for _ in 0..<5 {
            try? FileManager.default.removeItem(at: klasor)
            if !FileManager.default.fileExists(atPath: klasor.path) { return }
            Thread.sleep(forTimeInterval: 0.5)
        }
        NSLog("uyarı: geçici klasör silinemedi, elle silin (temp folder not deleted): %@", klasor.path)
    }
}

import CryptoKit
import Foundation
import Observation

/// Sabitlenmiş VoxCPM2 Q8_0 GGUF modelini indirir: ilerleme, kaldığı yerden sürdürme ve sha256 doğrulaması.
/// Downloads the pinned model with progress, resume (HTTP Range on a .part file) and streaming sha256.
@MainActor @Observable
final class ModelIndirici {
    nonisolated static let adres = URL(string: "https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/661a224e9d9adbd49c01626f85e426f5f425d771/VoxCPM2-GGUF/voxcpm2-q8_0.gguf")!
    nonisolated static let sha256 = "c8e01ab4416011e12a28f24ede298a1aa5ce64b43f8e8aaad53b1e2fe7c96432"
    nonisolated static let boyut: Int64 = 2_955_000_480
    nonisolated static let dosyaAdi = "voxcpm2-q8_0.gguf"
    private static let dogrulamaAnahtari = "modelDogrulandi"   // "yol|boyut|değişim zamanı"

    enum Durum: Equatable {
        case denetleniyor, eksik, indiriliyor, duraklatildi, dogrulaniyor, hazir
        case hata(String)
    }

    private(set) var durum: Durum = .denetleniyor
    private(set) var tamamlanan: Int64 = 0
    private(set) var hizMBsn: Double = 0
    var oran: Double { Double(tamamlanan) / Double(Self.boyut) }

    let depo: Depo
    private var gorev: Gorev?

    init(depo: Depo) { self.depo = depo }

    // MARK: - Denetim

    func denetle() {
        let model = depo.model
        if let iz = Self.iz(model), UserDefaults.standard.string(forKey: Self.dogrulamaAnahtari) == iz {
            durum = .hazir
            return
        }
        if FileManager.default.fileExists(atPath: model.path) {
            dosyaDogrula(model, harici: model != depo.indirilenModel)
            return
        }
        tamamlanan = Self.boy(parca)
        durum = tamamlanan > 0 ? .duraklatildi : .eksik
    }

    private var parca: URL { depo.indirilenModel.appendingPathExtension("part") }

    private static func boy(_ url: URL) -> Int64 {
        ((try? FileManager.default.attributesOfItem(atPath: url.path))?[.size] as? NSNumber)?.int64Value ?? 0
    }

    private static func iz(_ url: URL) -> String? {
        guard let a = try? FileManager.default.attributesOfItem(atPath: url.path),
              let boy = (a[.size] as? NSNumber)?.int64Value, boy == boyut,
              let tarih = a[.modificationDate] as? Date else { return nil }
        return "\(url.path)|\(boy)|\(tarih.timeIntervalSince1970)"
    }

    /// Kullanıcının elindeki dosya (ör. kur.sh ile indirilmiş ~/vox/model/voxcpm2-q8_0.gguf): sha256 doğruysa kullanılır.
    func dosyaDogrula(_ url: URL, harici: Bool) {
        durum = .dogrulaniyor
        tamamlanan = 0
        Task.detached {
            let sonuc = ModelIndirici.ozet(url, ilerleme: { n in Task { @MainActor [weak self] in self?.tamamlanan = n } })
            await MainActor.run { [weak self] in
                guard let self else { return }
                if sonuc == Self.sha256 {
                    if harici { UserDefaults.standard.set(url.path, forKey: Depo.hariciModelAnahtari) }
                    UserDefaults.standard.set(Self.iz(url), forKey: Self.dogrulamaAnahtari)
                    self.durum = .hazir
                } else {
                    self.durum = .hata("sha256 tutmadı (\(url.lastPathComponent)); dosya bozuk ya da farklı bir model")
                }
            }
        }
    }

    nonisolated private static func ozet(_ url: URL, ilerleme: (Int64) -> Void) -> String? {
        guard let tutamac = try? FileHandle(forReadingFrom: url) else { return nil }
        defer { try? tutamac.close() }
        var hasher = SHA256()
        var okunan: Int64 = 0
        while let parca = try? tutamac.read(upToCount: 16 << 20), !parca.isEmpty {
            hasher.update(data: parca)
            okunan += Int64(parca.count)
            ilerleme(okunan)
        }
        return hasher.finalize().map { String(format: "%02x", $0) }.joined()
    }

    // MARK: - İndirme

    func baslat() {
        guard gorev == nil else { return }
        do { try depo.hazirla() } catch { durum = .hata(error.localizedDescription); return }
        UserDefaults.standard.removeObject(forKey: Depo.hariciModelAnahtari)
        let bos = (try? depo.modelKlasoru.resourceValues(forKeys: [.volumeAvailableCapacityForImportantUsageKey]))?
            .volumeAvailableCapacityForImportantUsage ?? Int64.max
        let gereken = Self.boyut - Self.boy(parca) + 200_000_000
        if bos < gereken {
            durum = .hata(String(format: "diskte yer yok: %.1f GB gerekli, %.1f GB boş", Double(gereken) / 1e9, Double(bos) / 1e9))
            return
        }
        durum = .indiriliyor
        let g = Gorev(parca: parca, hedef: depo.indirilenModel)
        gorev = g
        g.ilerleme = { [weak self] n, hiz in
            Task { @MainActor in
                guard let self, self.durum == .indiriliyor || self.durum == .dogrulaniyor else { return }
                self.tamamlanan = n
                self.hizMBsn = hiz
            }
        }
        g.bitti = { [weak self] sonuc in
            Task { @MainActor in
                guard let self else { return }
                self.gorev = nil
                switch sonuc {
                case .success:
                    UserDefaults.standard.set(Self.iz(self.depo.indirilenModel), forKey: Self.dogrulamaAnahtari)
                    self.durum = .hazir
                case .failure(let hata as SesHatasi) where hata.mesaj == Gorev.durduruldu:
                    self.durum = .duraklatildi
                case .failure(let hata):
                    self.tamamlanan = Self.boy(self.parca)
                    self.durum = .hata(hata.localizedDescription)
                }
            }
        }
        g.baslat()
    }

    func duraklat() {
        gorev?.durdur()
    }

    // MARK: - Ağ görevi (arka plan kuyruğunda)

    final class Gorev: NSObject, URLSessionDataDelegate, @unchecked Sendable {
        static let durduruldu = "durduruldu"
        let parca: URL
        let hedef: URL
        var ilerleme: ((Int64, Double) -> Void)?
        var bitti: ((Result<Void, Error>) -> Void)?

        private var oturum: URLSession?
        private var yazici: FileHandle?
        private var hasher = SHA256()
        private var yazilan: Int64 = 0
        private var hizBaslangic = (Date(), Int64(0))
        private var sonBildirim = Date.distantPast
        private var hata: Error?

        init(parca: URL, hedef: URL) {
            self.parca = parca
            self.hedef = hedef
        }

        func baslat() {
            let kuyruk = OperationQueue()
            kuyruk.maxConcurrentOperationCount = 1
            kuyruk.addOperation { [self] in
                // kaldığı yer: var olan .part'ın özetini çıkar, sonra Range ile devam et
                let fm = FileManager.default
                if !fm.fileExists(atPath: parca.path) { fm.createFile(atPath: parca.path, contents: nil) }
                yazilan = 0
                if let okuyucu = try? FileHandle(forReadingFrom: parca) {
                    while let p = try? okuyucu.read(upToCount: 16 << 20), !p.isEmpty {
                        hasher.update(data: p)
                        yazilan += Int64(p.count)
                    }
                    try? okuyucu.close()
                }
                if yazilan > ModelIndirici.boyut { try? fm.removeItem(at: parca); fm.createFile(atPath: parca.path, contents: nil); hasher = SHA256(); yazilan = 0 }
                ilerleme?(yazilan, 0)
                if yazilan == ModelIndirici.boyut { bitir(); return }
                yazici = try? FileHandle(forWritingTo: parca)
                _ = try? yazici?.seekToEnd()
                var istek = URLRequest(url: ModelIndirici.adres)
                if yazilan > 0 { istek.setValue("bytes=\(yazilan)-", forHTTPHeaderField: "Range") }
                hizBaslangic = (Date(), yazilan)
                let ayar = URLSessionConfiguration.default
                ayar.timeoutIntervalForRequest = 60
                oturum = URLSession(configuration: ayar, delegate: self, delegateQueue: kuyruk)
                oturum?.dataTask(with: istek).resume()
            }
        }

        func durdur() {
            hata = SesHatasi(Self.durduruldu)
            oturum?.invalidateAndCancel()
        }

        func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive response: URLResponse,
                        completionHandler: @escaping (URLSession.ResponseDisposition) -> Void) {
            let kod = (response as? HTTPURLResponse)?.statusCode ?? 0
            if kod == 200 && yazilan > 0 {
                // sunucu Range'i yok saydı: baştan
                try? yazici?.truncate(atOffset: 0)
                hasher = SHA256()
                yazilan = 0
            } else if kod != 200 && kod != 206 {
                hata = SesHatasi("indirme hatası: HTTP \(kod)")
                completionHandler(.cancel)
                return
            }
            completionHandler(.allow)
        }

        func urlSession(_ session: URLSession, dataTask: URLSessionDataTask, didReceive data: Data) {
            do { try yazici?.write(contentsOf: data) } catch {
                hata = error
                dataTask.cancel()
                return
            }
            hasher.update(data: data)
            yazilan += Int64(data.count)
            let simdi = Date()
            if simdi.timeIntervalSince(sonBildirim) > 0.25 {
                sonBildirim = simdi
                let gecen = simdi.timeIntervalSince(hizBaslangic.0)
                ilerleme?(yazilan, gecen > 0 ? Double(yazilan - hizBaslangic.1) / gecen / 1e6 : 0)
            }
        }

        func urlSession(_ session: URLSession, task: URLSessionTask, didCompleteWithError error: Error?) {
            try? yazici?.close()
            yazici = nil
            session.finishTasksAndInvalidate()
            if let hata { bitti?(.failure(hata)); return }
            if let error {
                bitti?(.failure(SesHatasi("indirme kesildi, Sürdür ile kaldığı yerden devam eder: \(error.localizedDescription)")))
                return
            }
            bitir()
        }

        private func bitir() {
            ilerleme?(yazilan, 0)
            let ozet = hasher.finalize().map { String(format: "%02x", $0) }.joined()
            guard yazilan == ModelIndirici.boyut, ozet == ModelIndirici.sha256 else {
                try? FileManager.default.removeItem(at: parca)
                bitti?(.failure(SesHatasi("sha256 tutmadı (\(yazilan) bayt); bozuk parça silindi, yeniden indirin")))
                return
            }
            do {
                if FileManager.default.fileExists(atPath: hedef.path) { try FileManager.default.removeItem(at: hedef) }
                try FileManager.default.moveItem(at: parca, to: hedef)
                bitti?(.success(()))
            } catch {
                bitti?(.failure(error))
            }
        }
    }
}

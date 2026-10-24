import Foundation

/// Klasörler ve dosya yolları. Kodda sabit kullanıcı yolu yoktur: her şey Application Support altında.
/// Folders: everything lives under ~/Library/Application Support/SesTasarimi.
struct Depo: Sendable {
    let kok: URL
    var sabitModel: URL? = nil   // öz sınama için / for the self-test

    static let varsayilan: Depo = {
        let destek = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0]
        return Depo(kok: destek.appendingPathComponent("SesTasarimi", isDirectory: true))
    }()

    var modelKlasoru: URL { kok.appendingPathComponent("model", isDirectory: true) }
    var indirilenModel: URL { modelKlasoru.appendingPathComponent(ModelIndirici.dosyaAdi) }
    /// İndirilen model ya da kullanıcının seçtiği (sha256'sı doğrulanmış) mevcut dosya, ör. ~/vox/model.
    var model: URL {
        if let sabitModel { return sabitModel }
        if let yol = UserDefaults.standard.string(forKey: Depo.hariciModelAnahtari),
           FileManager.default.fileExists(atPath: yol) { return URL(fileURLWithPath: yol) }
        return indirilenModel
    }
    static let hariciModelAnahtari = "hariciModelYolu"
    var sesler: URL { kok.appendingPathComponent("sesler", isDirectory: true) }       // tasarlanan sesler
    var okumalar: URL { kok.appendingPathComponent("okumalar", isDirectory: true) }   // okuma ve klon çıktıları
    var onbellek: URL { kok.appendingPathComponent("onbellek", isDirectory: true) }   // referans kodlama önbelleği
    var calisma: URL { kok.appendingPathComponent("_calisma", isDirectory: true) }
    var sozluk: URL { kok.appendingPathComponent("okunus_sozlugu.tsv") }

    /// Uygulamaya gömülü motor (Contents/MacOS/audiocpp_cli). / Engine embedded in the app bundle.
    var motor: URL? {
        if let yol = ProcessInfo.processInfo.environment["SES_TASARIMI_MOTOR"] { return URL(fileURLWithPath: yol) }
        return Bundle.main.url(forAuxiliaryExecutable: "audiocpp_cli")
    }

    var hazirSesler: URL { Bundle.main.resourceURL!.appendingPathComponent("hazir_sesler", isDirectory: true) }

    func hazirla() throws {
        let fm = FileManager.default
        for klasor in [modelKlasoru, sesler, okumalar, onbellek, calisma] {
            try fm.createDirectory(at: klasor, withIntermediateDirectories: true)
        }
        // kullanıcının düzenleyebileceği okunuş sözlüğü: ilk açılışta paketteki kopyalanır
        if !fm.fileExists(atPath: sozluk.path), let paket = Bundle.main.url(forResource: "okunus_sozlugu", withExtension: "tsv") {
            try fm.copyItem(at: paket, to: sozluk)
        }
    }

    func kurallar() throws -> [Okunus.Kural] {
        guard let icerik = try? String(contentsOf: sozluk, encoding: .utf8) else { return [] }
        return try Okunus.kurallariOku(icerik)
    }

    static func zamanDamgasi(_ tarih: Date = Date(), bicim: String = "yyyyMMdd_HHmmss") -> String {
        let f = DateFormatter()
        f.locale = Locale(identifier: "en_US_POSIX")
        f.dateFormat = bicim
        return f.string(from: tarih)
    }
}

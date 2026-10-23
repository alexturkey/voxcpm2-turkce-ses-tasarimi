import Foundation

/// Bir sesin kartı (`ses.json`, Python sürümüyle aynı anahtarlar) ve klasörü.
/// A voice card (`ses.json`, same keys as the Python version) and its folder.
struct SesKarti: Identifiable, Hashable, Sendable {
    let kimlik: String          // "hazir/<ad>" ya da "<ad>/<çeşit>"
    let klasor: URL
    let hazir: Bool
    let ad: String
    let gorunenAd: String
    let tanitim: String
    let okumaTohumu: UInt32
    let referans: String
    let referansMetni: String
    let referansSn: Double?
    let ornekOkuma: String?
    let cesit: Int?

    var id: String { kimlik }
    var referansURL: URL { klasor.appendingPathComponent(referans) }
    var dinlemeURL: URL { klasor.appendingPathComponent(ornekOkuma ?? referans) }

    init(klasor: URL, kimlik: String, hazir: Bool) throws {
        let veri = try Data(contentsOf: klasor.appendingPathComponent("ses.json"))
        guard let d = try JSONSerialization.jsonObject(with: veri) as? [String: Any] else {
            throw SesHatasi("ses.json okunamadı: \(klasor.path)")
        }
        self.kimlik = kimlik
        self.klasor = klasor
        self.hazir = hazir
        ad = d["ad"] as? String ?? klasor.lastPathComponent
        gorunenAd = d["gorunen_ad"] as? String ?? ad
        tanitim = d["tanitim_tr"] as? String ?? d["ses_yaratici_ingilizce_prompt"] as? String ?? ""
        guard let tohum = (d["okuma_tohumu"] as? NSNumber)?.uint32Value else { throw SesHatasi("okuma_tohumu yok: \(klasor.path)") }
        okumaTohumu = tohum
        referans = d["referans"] as? String ?? "referans.wav"
        referansMetni = d["ses_yaratilirken_okutulan_metin"] as? String ?? ""
        referansSn = (d["referans_sn"] as? NSNumber)?.doubleValue
        ornekOkuma = d["ornek_okuma"] as? String
        cesit = (d["cesit"] as? NSNumber)?.intValue
    }
}

enum SesKatalogu {
    /// Hazır sesler (paketten) ve tasarlanan sesler (Application Support). / Bundled + designed voices.
    static func listele(_ depo: Depo) -> (hazir: [SesKarti], tasarlanan: [SesKarti]) {
        let fm = FileManager.default
        func klasorler(_ url: URL) -> [URL] {
            ((try? fm.contentsOfDirectory(at: url, includingPropertiesForKeys: [.isDirectoryKey])) ?? [])
                .filter { (try? $0.resourceValues(forKeys: [.isDirectoryKey]).isDirectory) == true }
                .sorted { $0.lastPathComponent < $1.lastPathComponent }
        }
        let hazir = klasorler(depo.hazirSesler).compactMap {
            try? SesKarti(klasor: $0, kimlik: "hazir/\($0.lastPathComponent)", hazir: true)
        }
        var tasarlanan: [SesKarti] = []
        for ses in klasorler(depo.sesler) where !ses.lastPathComponent.hasPrefix("_") {
            for cesit in klasorler(ses) where cesit.lastPathComponent.hasPrefix("cesit_") {
                guard let numara = Int(cesit.lastPathComponent.dropFirst(6)),
                      let kart = try? SesKarti(klasor: cesit, kimlik: "\(ses.lastPathComponent)/\(numara)", hazir: false)
                else { continue }
                tasarlanan.append(kart)
            }
        }
        return (hazir, tasarlanan)
    }
}

/// Metin dosyası olarak JSON yazımı (Python'daki `json.dumps(..., ensure_ascii=False, indent=2)` karşılığı).
enum JSONYaz {
    static func yaz(_ nesne: [String: Any], _ url: URL) throws {
        var veri = try JSONSerialization.data(withJSONObject: nesne, options: [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes])
        veri.append(UInt8(ascii: "\n"))
        try veri.write(to: url, options: .atomic)
    }
}

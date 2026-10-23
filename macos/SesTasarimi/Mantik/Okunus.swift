import Foundation

/// Türkçe okunuş hazırlığı: tırnak temizliği, okunuş sözlüğü, satır ve durak ayrıştırma, metin denetimi.
/// Port of `ses_tasarim/okunus.py`. Kural: rakam ve tırnak motora gitmez (rakamı yazıyla yaz: "iki bin yirmi altı").
enum Okunus {
    static let maxSatirKarakter = 2000      // motor metin bütçesi 2048 kod noktası / engine text budget
    static let satirArasiSn = 0.35          // satırlar arası varsayılan sessizlik / default gap between lines
    static let duraklar: [(ad: String, sn: Double)] = [("bagli", 0.25), ("normal", 0.5), ("paragraf", 1.0), ("agir", 1.5)]

    static let tirnaklar: Set<Character> = ["\"", "“", "”", "„", "«", "»", "‘", "’", "‚", "‹", "›", "`", "´", "'"]

    struct Kural: Equatable {
        let yazilis: String
        let okunus: String
    }

    struct Satir: Equatable {
        let metin: String
        let durakSn: Double
    }

    // MARK: - Küçük harf ve kelime sınırı

    static func turkceKucuk(_ metin: String) -> String {
        String(metin.map(turkceKucukKarakter))
    }

    /// Tek karakter tek karaktere: sözlük eşleşmesi özgün metindeki yerleri korur.
    static func turkceKucukKarakter(_ c: Character) -> Character {
        switch c {
        case "I": return "ı"
        case "İ": return "i"
        default:
            let kucuk = c.lowercased()
            return kucuk.count == 1 ? Character(kucuk) : c
        }
    }

    /// Python `\w` + Türkçe harfler: harf, rakam ya da alt çizgi.
    static func kelimeKarakteri(_ c: Character) -> Bool {
        c.isLetter || c.isNumber || c == "_"
    }

    // MARK: - Sözlük

    /// `yazılış<TAB>okunuş` satırları; `#` yorum. Uzun ifade önce denenir.
    static func kurallariOku(_ icerik: String, dosyaAdi: String = "okunus_sozlugu.tsv") throws -> [Kural] {
        var kurallar: [(Int, Kural)] = []
        var gorulen: [String: Int] = [:]
        for (sira, ham) in icerik.components(separatedBy: .newlines).enumerated() {
            let numara = sira + 1
            let satir = ham.trimmingCharacters(in: .whitespaces)
            if satir.isEmpty || satir.hasPrefix("#") { continue }
            guard let sekme = satir.firstIndex(of: "\t") else {
                throw SesHatasi("\(dosyaAdi):\(numara): beklenen biçim 'yazılış<TAB>okunuş'")
            }
            let yazilis = satir[..<sekme].trimmingCharacters(in: .whitespaces)
            let okunus = satir[satir.index(after: sekme)...].trimmingCharacters(in: .whitespaces)
            let anahtar = turkceKucuk(yazilis)
            if let onceki = gorulen[anahtar] {
                throw SesHatasi("\(dosyaAdi):\(numara): '\(yazilis)' zaten \(onceki). satırda")
            }
            gorulen[anahtar] = numara
            kurallar.append((kurallar.count, Kural(yazilis: yazilis, okunus: okunus)))
        }
        return kurallar.sorted { a, b in
            let (la, lb) = (a.1.yazilis.unicodeScalars.count, b.1.yazilis.unicodeScalars.count)
            return la != lb ? la > lb : a.0 < b.0
        }.map(\.1)
    }

    /// Tam kelime, büyük-küçük harf duyarsız değiştirme (soldan sağa, ilk uyan kural).
    static func sozlukUygula(_ metin: String, _ kurallar: [Kural]) -> String {
        guard !kurallar.isEmpty else { return metin }
        let ozgun = Array(metin)
        let kucuk = ozgun.map(turkceKucukKarakter)
        let anahtarlar = kurallar.map { (Array(turkceKucuk($0.yazilis)), $0.okunus) }
        var parcalar = ""
        var i = 0, imlec = 0
        while i < kucuk.count {
            if i == 0 || !kelimeKarakteri(kucuk[i - 1]) {
                let uyan = anahtarlar.first { anahtar, _ in
                    let son = i + anahtar.count
                    return !anahtar.isEmpty && son <= kucuk.count && Array(kucuk[i..<son]) == anahtar
                        && (son == kucuk.count || !kelimeKarakteri(kucuk[son]))
                }
                if let (anahtar, okunus) = uyan {
                    parcalar += String(ozgun[imlec..<i]) + okunus
                    i += anahtar.count
                    imlec = i
                    continue
                }
            }
            i += 1
        }
        return parcalar + String(ozgun[imlec...])
    }

    // MARK: - Temizlik ve denetim

    static func tirnaklariAt(_ metin: String) -> String {
        let temiz = String(metin.filter { !tirnaklar.contains($0) })
        // Satır sonu (boş satır dahil) cümle sınırı olarak kalır; Python okunus.strip_quotes ile birebir.
        // Line breaks (blank lines too) stay as sentence boundaries; mirrors Python okunus.strip_quotes.
        return temiz.replacingOccurrences(of: "[^\\S\\n]*\\n[^\\S\\n]*", with: "\n", options: .regularExpression)
            .replacingOccurrences(of: "[^\\S\\n]{2,}", with: " ", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines)
    }

    /// Motora gidecek hali. / Final form sent to the engine.
    static func soylenen(_ metin: String, _ kurallar: [Kural]) -> String {
        tirnaklariAt(sozlukUygula(metin, kurallar))
    }

    static func sorunlar(_ metin: String, yer: String = "metin") -> [String] {
        var bulunan: [String] = []
        let isaretler = Set(metin.filter { tirnaklar.contains($0) || $0.isNumber && $0.unicodeScalars.allSatisfy { $0.properties.numericType == .decimal } })
        if !isaretler.isEmpty {
            let liste = isaretler.map(String.init).sorted().joined(separator: " ")
            bulunan.append("\(yer): okunamayan işaret [\(liste)]; tırnak ve kesme işaretini kaldır, rakamı yazıyla yaz")
        }
        do {
            for (sira, satir) in try satirlar(metin).enumerated() where satir.metin.unicodeScalars.count > maxSatirKarakter {
                bulunan.append("\(yer): \(sira + 1). satır \(satir.metin.unicodeScalars.count) karakter > \(maxSatirKarakter); satırı böl")
            }
        } catch {
            bulunan.append("\(yer): \(error.localizedDescription)")
        }
        if metin.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            bulunan.append("\(yer): boş")
        }
        return bulunan
    }

    // MARK: - Satır ve durak

    /// `metin || paragraf` → (metin, saniye). / Trailing pause marker.
    static func durakAyir(_ satir: String) throws -> Satir {
        guard let ayrac = satir.range(of: "||", options: .backwards) else {
            return Satir(metin: satir.trimmingCharacters(in: .whitespaces), durakSn: satirArasiSn)
        }
        let ad = satir[ayrac.upperBound...].trimmingCharacters(in: .whitespaces)
        guard let durak = duraklar.first(where: { $0.ad == ad }) else {
            throw SesHatasi("bilinmeyen durak '\(ad)'; seçenekler: \(duraklar.map(\.ad).joined(separator: ", "))")
        }
        return Satir(metin: satir[..<ayrac.lowerBound].trimmingCharacters(in: .whitespaces), durakSn: durak.sn)
    }

    /// Her satır bir cümle; sonundaki durak süresiyle. / One sentence per line with its pause.
    static func satirlar(_ metin: String) throws -> [Satir] {
        try metin.split(whereSeparator: \.isNewline).map(String.init)
            .filter { !$0.trimmingCharacters(in: .whitespaces).isEmpty }
            .map(durakAyir)
    }
}

struct SesHatasi: LocalizedError, Equatable {
    let mesaj: String
    init(_ mesaj: String) { self.mesaj = mesaj }
    var errorDescription: String? { mesaj }
}

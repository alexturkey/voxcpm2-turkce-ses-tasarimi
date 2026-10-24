import CryptoKit
import Foundation

/// Komut satırı öz sınaması: 2 çeşitli tasarım, tasarlanan sesle okuma, hazır sesle aynı tohumla iki okuma
/// (bayt bayt aynı olmalı). Uygulamanın kendi motoru ve modeliyle, ayrı bir klasörde çalışır.
/// Self-test: design 2 variants, read with one, read twice with a bundled voice and compare sha256.
enum OzSinama {
    final class Kutu: @unchecked Sendable { var deger: Int32 = 0 }

    static let tarif = "A mature 70-year-old Turkish man with a deep, full, resonant chest voice and a slightly husky warmth. He speaks as a seasoned news anchor: calm, authoritative and trustworthy, at a measured, unhurried pace. Clear Turkish diction, natural pauses between phrases, slightly longer pauses at sentence endings. Clean and smooth, no rasp, no breathiness, no hiss, recorded cleanly in a studio with no background noise."
    static let tasarimMetni = "İyi akşamlar, ana haber bültenine hoş geldiniz. Bugün gündemde ekonomi, sağlık ve spor haberleri var. Önce hava durumuna bakalım, çünkü hafta sonu planı yapanları sevindirecek gelişmeler var."
    static let okumaMetni = """
        Bu ses yalnız bir metin tarifinden tasarlandı, bir kayıttan klonlanmadı.
        Yapay zekâ ile üretilmiş bir sestir. || paragraf
        Şimdi istediğiniz metni okuyabilir.
        """

    static func calistir(_ klasor: URL) -> Int32 {
        let varsayilan = Depo.varsayilan
        let model = ProcessInfo.processInfo.environment["SES_TASARIMI_MODEL"].map { URL(fileURLWithPath: $0) } ?? varsayilan.model
        let depo = Depo(kok: klasor, sabitModel: model)
        let islemler = Islemler(depo: depo)
        @Sendable func yaz(_ s: String) { print(s); fflush(stdout) }
        @Sendable func ozet(_ url: URL) -> String {
            SHA256.hash(data: (try? Data(contentsOf: url)) ?? Data()).map { String(format: "%02x", $0) }.joined()
        }
        let bildir: Islemler.IlerlemeBildir = { i in yaz("  \(i.biten)/\(i.toplam), \(Int(i.gecen)) sn, GPU \(i.gpuMB) MB") }
        let kod = Kutu()
        let bitti = DispatchSemaphore(value: 0)
        Task.detached {
            do {
                try depo.hazirla()
                yaz("model: \(depo.model.path)")
                yaz("== tasarım: 2 çeşit (tohum 7, 42)")
                let t = try await islemler.tasarla(ad: "oz_sinama", tarif: tarif, metin: tasarimMetni, cesit: 2,
                                                   tohumlar: [7, 42], ilerleme: bildir)
                for c in t.cesitler {
                    yaz("  tohum \(c.tohum): \(c.hata ?? "\(c.referansSn) sn, sha256 \(c.kart.map { ozet($0.referansURL) } ?? "")")")
                }
                yaz("  süre \(t.sureSn) sn, GPU tepe \(t.gpuTepeMB) MB")
                guard let tasarlanan = t.cesitler.compactMap(\.kart).first else { throw SesHatasi("çeşit yok") }

                yaz("== okuma: tasarlanan ses \(tasarlanan.kimlik)")
                let o1 = try await islemler.oku(ses: tasarlanan, metin: okumaMetni, cikti: klasor.appendingPathComponent("okuma_tasarlanan"),
                                                ilerleme: bildir)
                yaz("  \(o1.sesSn) sn ses, \(o1.sureSn) sn, RTF \(String(format: "%.2f", o1.rtf)), GPU tepe \(o1.gpuTepeMB) MB")

                let hazir = SesKatalogu.listele(depo).hazir
                guard let belgesel = hazir.first(where: { $0.ad == "belgesel_hanim" }) else { throw SesHatasi("hazır ses yok") }
                var ozetler: [String] = []
                for tur in 1...2 {
                    yaz("== okuma \(tur)/2: hazır ses belgesel_hanim, tohum \(belgesel.okumaTohumu)")
                    let o = try await islemler.oku(ses: belgesel, metin: okumaMetni, cikti: klasor.appendingPathComponent("okuma_hazir_\(tur)"),
                                                   ilerleme: bildir)
                    ozetler.append(ozet(o.wav))
                    yaz("  \(o.sesSn) sn ses, \(o.sureSn) sn, RTF \(String(format: "%.2f", o.rtf)), sha256 \(ozetler.last!)")
                }
                let ayni = ozetler[0] == ozetler[1]
                yaz(ayni ? "AYNI_TOHUM_AYNI_WAV: evet" : "AYNI_TOHUM_AYNI_WAV: HAYIR")
                yaz(ayni ? "OZ_SINAMA_OK" : "OZ_SINAMA_HATA")
                kod.deger = ayni ? 0 : 1
            } catch {
                yaz("hata: \(error.localizedDescription)")
                kod.deger = 1
            }
            bitti.signal()
        }
        bitti.wait()
        return kod.deger
    }
}

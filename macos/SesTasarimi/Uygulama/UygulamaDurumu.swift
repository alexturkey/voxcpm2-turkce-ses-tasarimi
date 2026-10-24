import AppKit
import AVFoundation
import Observation
import UniformTypeIdentifiers

/// Bölüm durumu: boşta / çalışıyor (ilerleme) / bitti / hata. / Per-section job state.
enum IsDurumu: Equatable {
    case bosta
    case calisiyor(String, Double?)
    case bitti(String)
    case hata(String)

    var mesaj: String {
        switch self {
        case .bosta: ""
        case .calisiyor(let m, _), .bitti(let m), .hata(let m): m
        }
    }
}

enum Bolum: Hashable { case tasarla, oku, klonla }

/// Uygulamanın tek durumu. Aynı anda tek motor işi (GPU) çalışır; diğer düğmeler beklerken kapalıdır.
/// App state. One engine job at a time.
@MainActor @Observable
final class UygulamaDurumu {
    let depo = Depo.varsayilan
    let indirici: ModelIndirici
    let oynatici = Oynatici()
    var islemler: Islemler { Islemler(depo: depo) }

    var hazirSesler: [SesKarti] = []
    var tasarlananSesler: [SesKarti] = []
    var durum: [Bolum: IsDurumu] = [:]
    private(set) var calisan: Bolum?
    private var gorev: Task<Void, Never>?
    var kurulumHatasi: String?

    // 1. Tasarım formu
    var tasarimAdi = ""
    var tasarimTarifi = ""
    var tasarimMetni = ""
    var cesitSayisi = Islemler.varsayilanCesit
    var sonTasarim: Islemler.TasarimSonucu?

    // 2. Okuma formu
    var seciliSes: String = "hazir/belgesel_hanim"
    var okumaMetni = ""
    var sonOkuma: Islemler.OkumaSonucu?

    // 3. Klonlama formu
    var klonKaydi: URL?
    var klonKaydiBilgisi = ""
    var klonKayitMetni = ""
    var klonMetni = ""
    var klonTohumu = Int(Klon.varsayilanTohum)
    var klonOnayi = false
    var sonKlon: Islemler.KlonSonucu?

    init() {
        indirici = ModelIndirici(depo: depo)
        do { try depo.hazirla() } catch { kurulumHatasi = error.localizedDescription }
        indirici.denetle()
        sesleriYenile()
    }

    var mesgul: Bool { calisan != nil }

    func sesleriYenile() {
        let liste = SesKatalogu.listele(depo)
        hazirSesler = liste.hazir
        tasarlananSesler = liste.tasarlanan
    }

    func ses(_ kimlik: String) -> SesKarti? {
        (tasarlananSesler + hazirSesler).first { $0.kimlik == kimlik }
    }

    // MARK: - İş yürütme

    private func calistir<T: Sendable>(_ bolum: Bolum,
                                       _ is_: @escaping @Sendable (Islemler, @escaping Islemler.IlerlemeBildir) async throws -> T,
                                       bitti: @escaping (T) -> String) {
        guard calisan == nil else { return }
        calisan = bolum
        durum[bolum] = .calisiyor("motor başlatılıyor, model yükleniyor (~10-20 sn)", nil)
        let islemler = islemler
        gorev = Task {
            let bildir: Islemler.IlerlemeBildir = { [weak self] i in
                Task { @MainActor in
                    guard let self, case .calisiyor = self.durum[bolum] else { return }
                    let metin = "\(i.biten)/\(i.toplam) hazır, \(Int(i.gecen)) sn · GPU belleği \(i.gpuMB) MB"
                    self.durum[bolum] = .calisiyor(metin, i.toplam > 0 ? Double(i.biten) / Double(i.toplam) : nil)
                }
            }
            do {
                let sonuc = try await Task.detached { try await is_(islemler, bildir) }.value
                durum[bolum] = .bitti(bitti(sonuc))
            } catch is CancellationError {
                durum[bolum] = .hata("durduruldu")
            } catch {
                durum[bolum] = .hata(error.localizedDescription)
            }
            calisan = nil
            gorev = nil
            sesleriYenile()
        }
    }

    func durdur() {
        gorev?.cancel()
        Motor.calisanSurec.deger?.terminate()
    }

    func tasarla() {
        let (ad, tarif, metin, sayi) = (tasarimAdi, tasarimTarifi, tasarimMetni, max(1, min(10, cesitSayisi)))
        let sorunlar = Islemler.tasarimDenetle(ad: ad, tarif: tarif, metin: metin)
        guard sorunlar.isEmpty else { durum[.tasarla] = .hata(sorunlar.joined(separator: "\n")); return }
        sonTasarim = nil
        calistir(.tasarla, { try await $0.tasarla(ad: ad, tarif: tarif, metin: metin, cesit: sayi, ilerleme: $1) }) { [weak self] s in
            self?.sonTasarim = s
            if let ilk = s.cesitler.first(where: { $0.kart != nil })?.kart { self?.seciliSes = ilk.kimlik }
            return "bitti: \(s.cesitler.count) çeşit, \(Self.sn(s.sureSn)) sn, GPU belleği tepe \(s.gpuTepeMB) MB"
        }
    }

    func oku() {
        guard let ses = ses(seciliSes) else { durum[.oku] = .hata("ses bulunamadı: \(seciliSes)"); return }
        let metin = okumaMetni
        let sorunlar = Okunus.sorunlar(metin)
        guard sorunlar.isEmpty else { durum[.oku] = .hata(sorunlar.joined(separator: "\n")); return }
        sonOkuma = nil
        let cikti = depo.okumalar.appendingPathComponent("\(Depo.zamanDamgasi())_\(UUID().uuidString.prefix(6))")
        calistir(.oku, { try await $0.oku(ses: ses, metin: metin, cikti: cikti, ilerleme: $1) }) { [weak self] s in
            self?.sonOkuma = s
            return "bitti"
        }
    }

    var klonHazir: Bool {
        klonOnayi && klonKaydi != nil && !klonKayitMetni.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
            && !klonMetni.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
    }

    func klonla() {
        guard klonOnayi, let kayit = klonKaydi else { return }  // onay kutusu işaretlenmeden çalışmaz
        let (kayitMetni, metin, onay) = (klonKayitMetni, klonMetni, klonOnayi)
        let tohum = UInt32(clamping: max(0, klonTohumu))
        let sorunlar = Klon.denetle(kayitMetni: kayitMetni, metin: metin, onay: onay)
        guard sorunlar.isEmpty else { durum[.klonla] = .hata(sorunlar.joined(separator: "\n")); return }
        sonKlon = nil
        let cikti = depo.okumalar.appendingPathComponent("\(Depo.zamanDamgasi())_klon_\(UUID().uuidString.prefix(6))")
        calistir(.klonla, {
            try await $0.klonla(kayit: kayit, kayitMetni: kayitMetni, metin: metin, cikti: cikti, onay: onay, tohum: tohum,
                                ilerleme: $1)
        }) { [weak self] s in
            self?.sonKlon = s
            return "bitti: yapay ses hazır (synthetic)"
        }
    }

    func klonKaydiSec() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.audio]
        panel.allowsMultipleSelection = false
        panel.message = "Kendi sesiniz ya da sahibinden açık izin alınmış bir kayıt (5-30 sn)"
        guard panel.runModal() == .OK, let url = panel.url else { return }
        klonKaydi = url
        if let dosya = try? AVAudioFile(forReading: url) {
            let sn = Double(dosya.length) / dosya.processingFormat.sampleRate
            var bilgi = String(format: "%.1f sn", sn)
            if sn > Klon.enCokSn { bilgi += " · 36 sn üstü kırpılacak, kayıt metni ilk 36 sn ile eşleşmeli" }
            else if sn < Klon.enAzSn { bilgi += " · çok kısa, en az 3 sn gerekli" }
            else if !Klon.onerilen.contains(sn) { bilgi += " · 5-30 sn önerilir" }
            klonKaydiBilgisi = bilgi
        } else {
            klonKaydiBilgisi = "bu dosya çözülemedi; wav, mp3, flac, m4a ya da aiff deneyin"
        }
    }

    func kaydet(_ wav: URL, onerilenAd: String) {
        let panel = NSSavePanel()
        panel.allowedContentTypes = [.wav]
        panel.nameFieldStringValue = onerilenAd
        panel.message = "Yapay zekâ ile üretilmiş sestir; paylaşırken belirtin."
        guard panel.runModal() == .OK, let hedef = panel.url else { return }
        do {
            if FileManager.default.fileExists(atPath: hedef.path) { try FileManager.default.removeItem(at: hedef) }
            try FileManager.default.copyItem(at: wav, to: hedef)
        } catch {
            NSAlert(error: error).runModal()
        }
    }

    func sozluguAc() {
        NSWorkspace.shared.open([depo.sozluk], withApplicationAt: URL(fileURLWithPath: "/System/Applications/TextEdit.app"),
                                configuration: NSWorkspace.OpenConfiguration())
    }

    func klasoruGoster() {
        NSWorkspace.shared.activateFileViewerSelecting([depo.kok])
    }

    static func sn(_ x: Double) -> String { String(format: "%.1f", x) }
}

/// Tek oynatıcı: aynı anda bir ses çalar. / One player; one sound at a time.
@MainActor @Observable
final class Oynatici: NSObject, AVAudioPlayerDelegate {
    private(set) var calan: URL?
    private(set) var konum: Double = 0
    private(set) var sure: Double = 0
    private var oyuncu: AVAudioPlayer?
    private var zamanlayici: Timer?

    func degistir(_ url: URL) {
        if calan == url, let oyuncu {
            if oyuncu.isPlaying { oyuncu.pause(); zamanlayici?.invalidate() } else { oyuncu.play(); izle() }
            calan = url
            return
        }
        durdur()
        guard let yeni = try? AVAudioPlayer(contentsOf: url) else { return }
        yeni.delegate = self
        oyuncu = yeni
        calan = url
        sure = yeni.duration
        yeni.play()
        izle()
    }

    func caliyor(_ url: URL) -> Bool { calan == url && oyuncu?.isPlaying == true }

    func ilerleme(_ url: URL) -> Double { calan == url && sure > 0 ? konum / sure : 0 }

    func durdur() {
        zamanlayici?.invalidate()
        oyuncu?.stop()
        oyuncu = nil
        calan = nil
        konum = 0
    }

    private func izle() {
        zamanlayici?.invalidate()
        zamanlayici = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] _ in
            Task { @MainActor in self?.konum = self?.oyuncu?.currentTime ?? 0 }
        }
    }

    nonisolated func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        Task { @MainActor in self.durdur() }
    }
}

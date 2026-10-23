import SwiftUI

struct AnaGorunum: View {
    @Environment(UygulamaDurumu.self) private var uygulama

    var body: some View {
        if uygulama.indirici.durum == .hazir {
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    YapayUyarisi()
                    TasarlaBolumu()
                    OkuBolumu()
                    KlonlaBolumu()
                    HazirSeslerBolumu()
                }
                .padding(20)
                .frame(maxWidth: 900)
                .frame(maxWidth: .infinity)
            }
        } else {
            ModelKurulumu()
        }
    }
}

// MARK: - Ortak parçalar

struct YapayUyarisi: View {
    var body: some View {
        Uyari {
            Text("Üretilen her ses yapay zekâ ürünüdür; paylaşırken belirtin. Ses tasarımı (1-2) kayıt istemez; ses klonlama (3) yalnız kendi sesiniz ya da sahibinden açık izin alınmış sesle.")
            Text("Every generated voice is synthetic; label it as AI-generated when sharing. Voice design (1-2) needs no recording; voice cloning (3) only with your own voice or the owner's explicit permission.")
                .font(.caption).foregroundStyle(.secondary)
        }
    }
}

struct Uyari<Icerik: View>: View {
    @ViewBuilder var icerik: Icerik
    var body: some View {
        HStack(spacing: 0) {
            Rectangle().fill(Color.accentColor).frame(width: 3)
            VStack(alignment: .leading, spacing: 4) { icerik }
                .padding(.horizontal, 10).padding(.vertical, 6)
            Spacer(minLength: 0)
        }
        .fixedSize(horizontal: false, vertical: true)
    }
}

struct BolumKutusu<Icerik: View>: View {
    let baslik: String
    let altBaslik: String
    @ViewBuilder var icerik: Icerik
    var body: some View {
        GroupBox {
            VStack(alignment: .leading, spacing: 10) { icerik }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(8)
        } label: {
            HStack(alignment: .firstTextBaseline) {
                Text(baslik).font(.title3.bold())
                Text(altBaslik).foregroundStyle(.secondary)
            }
        }
    }
}

struct Etiketli<Icerik: View>: View {
    let etiket: String
    @ViewBuilder var icerik: Icerik
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(etiket).font(.callout).foregroundStyle(.secondary)
            icerik
        }
    }
}

struct MetinKutusu: View {
    @Binding var metin: String
    var yukseklik: CGFloat = 90
    var body: some View {
        TextEditor(text: $metin)
            .font(.body)
            .frame(minHeight: yukseklik)
            .scrollContentBackground(.hidden)
            .padding(4)
            .background(RoundedRectangle(cornerRadius: 6).fill(Color(nsColor: .textBackgroundColor)))
            .overlay(RoundedRectangle(cornerRadius: 6).stroke(Color.secondary.opacity(0.3)))
    }
}

struct DurumSatiri: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    let bolum: Bolum
    var body: some View {
        let durum = uygulama.durum[bolum] ?? .bosta
        switch durum {
        case .bosta: EmptyView()
        case .calisiyor(let mesaj, let oran):
            HStack {
                if let oran { ProgressView(value: oran).frame(width: 160) } else { ProgressView().controlSize(.small) }
                Text(mesaj).foregroundStyle(.secondary).monospacedDigit()
                Spacer()
                Button("Durdur", role: .cancel) { uygulama.durdur() }
            }
        case .bitti(let mesaj):
            Label(mesaj, systemImage: "checkmark.circle").foregroundStyle(.green)
        case .hata(let mesaj):
            Label { Text(mesaj).textSelection(.enabled) } icon: { Image(systemName: "exclamationmark.triangle") }
                .foregroundStyle(.red)
        }
    }
}

/// Bir ses dosyası için çal/duraklat + ilerleme çubuğu. / Play button with progress for one file.
struct SesSatiri: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    let url: URL
    var body: some View {
        let oynatici = uygulama.oynatici
        HStack {
            Button {
                oynatici.degistir(url)
            } label: {
                Image(systemName: oynatici.caliyor(url) ? "pause.fill" : "play.fill").frame(width: 16)
            }
            .help(oynatici.caliyor(url) ? "Duraklat" : "Dinle")
            ProgressView(value: oynatici.ilerleme(url)).frame(minWidth: 120)
        }
    }
}

struct Istatistik: View {
    let sonuc: Islemler.OkumaSonucu
    var body: some View {
        Text("\(UygulamaDurumu.sn(sonuc.sesSn)) sn ses, \(UygulamaDurumu.sn(sonuc.sureSn)) sn üretim (RTF \(String(format: "%.2f", sonuc.rtf))), GPU belleği tepe \(sonuc.gpuTepeMB) MB, tohum \(sonuc.tohum)")
            .font(.caption).foregroundStyle(.secondary).monospacedDigit().textSelection(.enabled)
    }
}

// MARK: - 1. Ses tasarla

struct TasarlaBolumu: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    var body: some View {
        @Bindable var u = uygulama
        BolumKutusu(baslik: "1. Ses tasarla", altBaslik: "(voice design)") {
            HStack(alignment: .top, spacing: 12) {
                Etiketli(etiket: "Sesin adı (voice name)") {
                    TextField("deniz_feneri", text: $u.tasarimAdi).textFieldStyle(.roundedBorder)
                }
                Etiketli(etiket: "Çeşit sayısı (her biri ayrı tohum)") {
                    Stepper(value: $u.cesitSayisi, in: 1...10) { Text("\(u.cesitSayisi)").monospacedDigit() }
                }
                .frame(width: 220)
            }
            Etiketli(etiket: "İngilizce ses tarifi, parantezsiz (voice description in English)") {
                MetinKutusu(metin: $u.tasarimTarifi, yukseklik: 70)
            }
            Etiketli(etiket: "Ses yaratılırken okutulan Türkçe metin, 25-35 sn, rakam ve tırnak yok (text read while creating the voice)") {
                MetinKutusu(metin: $u.tasarimMetni)
            }
            HStack {
                Button("Tasarla") { uygulama.tasarla() }
                    .buttonStyle(.borderedProminent)
                    .disabled(uygulama.mesgul)
                Text("Kalite sabit: 16 adım, cfg 2.0").font(.caption).foregroundStyle(.secondary)
            }
            DurumSatiri(bolum: .tasarla)
            if let sonuc = uygulama.sonTasarim {
                ForEach(sonuc.cesitler) { cesit in
                    if let kart = cesit.kart {
                        HStack {
                            Button {
                                uygulama.seciliSes = kart.kimlik
                            } label: {
                                Image(systemName: uygulama.seciliSes == kart.kimlik ? "largecircle.fill.circle" : "circle")
                            }
                            .buttonStyle(.plain)
                            .help("Bu çeşitle oku (2. bölüm)")
                            VStack(alignment: .leading) {
                                Text("çeşit \(kart.cesit ?? 0)")
                                Text("tohum \(String(cesit.tohum)), \(UygulamaDurumu.sn(cesit.referansSn)) sn")
                                    .font(.caption).foregroundStyle(.secondary)
                                if let uyari = cesit.uyari { Text(uyari).font(.caption).foregroundStyle(.orange) }
                            }
                            .frame(width: 220, alignment: .leading)
                            SesSatiri(url: kart.referansURL)
                        }
                        Divider()
                    } else {
                        Text("tohum \(String(cesit.tohum)): \(cesit.hata ?? "")").foregroundStyle(.red)
                    }
                }
            }
        }
    }
}

// MARK: - 2. Bu sesle oku

struct OkuBolumu: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    var body: some View {
        @Bindable var u = uygulama
        BolumKutusu(baslik: "2. Bu sesle oku", altBaslik: "(read with the selected voice)") {
            Etiketli(etiket: "Ses (voice)") {
                Picker("", selection: $u.seciliSes) {
                    if !uygulama.tasarlananSesler.isEmpty {
                        Section("Tasarlanan sesler") {
                            ForEach(uygulama.tasarlananSesler) { s in
                                Text("\(s.kimlik) (tohum \(String(s.okumaTohumu)))").tag(s.kimlik)
                            }
                        }
                    }
                    Section("Hazır sesler") {
                        ForEach(uygulama.hazirSesler) { s in
                            Text("\(s.gorunenAd) — \(String(s.tanitim.prefix(60)))").tag(s.kimlik)
                        }
                    }
                }
                .labelsHidden()
            }
            Etiketli(etiket: "Okunacak metin: her satır bir cümle; satır sonuna \"|| paragraf\" uzun durak (bagli, normal, paragraf, agir)") {
                MetinKutusu(metin: $u.okumaMetni, yukseklik: 120)
            }
            HStack {
                Button("Bu sesle oku") { uygulama.oku() }
                    .buttonStyle(.borderedProminent)
                    .disabled(uygulama.mesgul)
                Button("Okunuş sözlüğü…") { uygulama.sozluguAc() }
                    .help("Yanlış okunan kelimeyi ekleyin: yazılış<TAB>okunuş")
            }
            DurumSatiri(bolum: .oku)
            if let sonuc = uygulama.sonOkuma {
                HStack {
                    SesSatiri(url: sonuc.wav)
                    Button("Kaydet…") { uygulama.kaydet(sonuc.wav, onerilenAd: "okuma_synthetic.wav") }
                }
                Istatistik(sonuc: sonuc)
            }
        }
    }
}

// MARK: - 3. Ses klonlama

struct KlonlaBolumu: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    var body: some View {
        @Bindable var u = uygulama
        BolumKutusu(baslik: "3. Ses klonlama: kendi sesin ya da izinli ses", altBaslik: "(voice cloning: own or consented voice)") {
            Uyari {
                Text("Yalnız kendi sesiniz ya da sahibinden açık izin aldığınız ses. Kayıt yalnız bu bilgisayarda işlenir, saklanmaz, ağa gönderilmez; iş bitince (hata olsa da) geçici dosyalar silinir, yalnız yapay çıktı kalır.")
                Text("Only your own voice or a voice whose owner gave explicit permission. The recording is processed on this computer only, never stored or sent over the network; temp files are deleted when the job ends (also on failure), only the synthetic output is kept.")
                    .font(.caption).foregroundStyle(.secondary)
            }
            Etiketli(etiket: "Ses kaydı: wav / mp3 / flac / m4a / aiff, 5-30 sn temiz konuşma önerilir, 3 sn altı reddedilir, 36 sn üstü kırpılır") {
                HStack {
                    Button("Kayıt seç…") { uygulama.klonKaydiSec() }
                    Text(uygulama.klonKaydi?.lastPathComponent ?? "seçilmedi").foregroundStyle(.secondary)
                    Text(uygulama.klonKaydiBilgisi).font(.caption).foregroundStyle(.secondary)
                }
            }
            Etiketli(etiket: "Kaydın birebir metni, zorunlu: kayıtta ne söyleniyorsa aynısı (exact transcript)") {
                MetinKutusu(metin: $u.klonKayitMetni, yukseklik: 60)
            }
            Etiketli(etiket: "Okunacak metin: her satır bir cümle") {
                MetinKutusu(metin: $u.klonMetni, yukseklik: 60)
            }
            HStack(spacing: 16) {
                Etiketli(etiket: "Tohum (aynı tohum = aynı sonuç)") {
                    TextField("42", value: $u.klonTohumu, format: .number.grouping(.never))
                        .textFieldStyle(.roundedBorder).frame(width: 140)
                }
                Etiketli(etiket: "Kalite (sabit / fixed)") { Text("16 adım, cfg 2.0") }
            }
            Toggle(isOn: $u.klonOnayi) {
                VStack(alignment: .leading) {
                    Text(Klon.onayTR)
                    Text(Klon.onayEN).font(.caption).foregroundStyle(.secondary)
                }
            }
            .toggleStyle(.checkbox)
            Button("Klonla ve oku (clone and read)") { uygulama.klonla() }
                .buttonStyle(.borderedProminent)
                .disabled(!uygulama.klonHazir || uygulama.mesgul)
            DurumSatiri(bolum: .klonla)
            if let sonuc = uygulama.sonKlon {
                HStack {
                    SesSatiri(url: sonuc.okuma.wav)
                    Button("Kaydet…") { uygulama.kaydet(sonuc.okuma.wav, onerilenAd: "klon_synthetic.wav") }
                }
                Uyari {
                    Text("Yapay üretilmiş sestir. Paylaşırken belirtin.").bold()
                    Text("AI-generated synthetic speech; label it when sharing.").font(.caption)
                }
                Istatistik(sonuc: sonuc.okuma)
                Text("referans \(UygulamaDurumu.sn(sonuc.referansSn)) sn").font(.caption).foregroundStyle(.secondary)
                ForEach(sonuc.notlar, id: \.self) { Text($0).font(.caption).foregroundStyle(.secondary) }
            }
        }
    }
}

// MARK: - Hazır sesler

struct HazirSeslerBolumu: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    var body: some View {
        BolumKutusu(baslik: "Hazır sesler", altBaslik: "(bundled voices, synthetic)") {
            ForEach(uygulama.hazirSesler) { s in
                HStack(alignment: .center) {
                    VStack(alignment: .leading, spacing: 2) {
                        HStack {
                            Text(s.gorunenAd).bold()
                            Text("tohum \(String(s.okumaTohumu))").font(.caption).foregroundStyle(.secondary)
                        }
                        Text(s.tanitim).font(.caption).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
                    }
                    Spacer()
                    SesSatiri(url: s.dinlemeURL).frame(width: 220)
                    Button("Seç") { uygulama.seciliSes = s.kimlik }
                        .help("2. bölümde bu sesle oku")
                }
                Divider()
            }
        }
    }
}

// MARK: - Model kurulumu

struct ModelKurulumu: View {
    @Environment(UygulamaDurumu.self) private var uygulama
    var body: some View {
        let indirici = uygulama.indirici
        VStack(alignment: .leading, spacing: 14) {
            Text("VoxCPM2 modeli").font(.title2.bold())
            Text("Uygulama ilk açılışta modeli bir kez indirir (2,96 GB, Hugging Face, sabit sürüm, sha256 doğrulanır). Sonra internet gerekmez; bütün üretim bu Mac'te yapılır.")
                .fixedSize(horizontal: false, vertical: true)
            Text("The app downloads the model once (2.96 GB, pinned revision, sha256-verified). After that everything runs offline on this Mac.")
                .font(.caption).foregroundStyle(.secondary)
            if let hata = uygulama.kurulumHatasi { Text(hata).foregroundStyle(.red) }

            switch indirici.durum {
            case .denetleniyor:
                ProgressView("Denetleniyor…")
            case .dogrulaniyor:
                ProgressView(value: indirici.oran) { Text("sha256 doğrulanıyor…") }
            case .indiriliyor:
                ProgressView(value: indirici.oran) {
                    Text(ilerlemeMetni(indirici) + String(format: " · %.1f MB/sn", indirici.hizMBsn)).monospacedDigit()
                }
                Button("Duraklat") { indirici.duraklat() }
            case .eksik, .duraklatildi, .hata:
                if case .hata(let mesaj) = indirici.durum { Text(mesaj).foregroundStyle(.red).textSelection(.enabled) }
                if indirici.tamamlanan > 0 {
                    ProgressView(value: indirici.oran) { Text(ilerlemeMetni(indirici)).monospacedDigit() }
                }
                HStack {
                    Button(indirici.tamamlanan > 0 ? "Sürdür" : "Modeli indir") { indirici.baslat() }
                        .buttonStyle(.borderedProminent)
                    Button("Elimdeki dosyayı kullan…") { mevcutDosyaSec(indirici) }
                        .help("Daha önce indirilmiş voxcpm2-q8_0.gguf (ör. kur.sh ile ~/vox/model)")
                }
            case .hazir:
                EmptyView()
            }
        }
        .padding(32)
        .frame(maxWidth: 640)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func ilerlemeMetni(_ i: ModelIndirici) -> String {
        String(format: "%.2f / %.2f GB", Double(i.tamamlanan) / 1e9, Double(ModelIndirici.boyut) / 1e9)
    }

    private func mevcutDosyaSec(_ indirici: ModelIndirici) {
        let panel = NSOpenPanel()
        panel.allowsMultipleSelection = false
        panel.message = "voxcpm2-q8_0.gguf dosyasını seçin (sha256 doğrulanır)"
        guard panel.runModal() == .OK, let url = panel.url else { return }
        indirici.dosyaDogrula(url, harici: true)
    }
}

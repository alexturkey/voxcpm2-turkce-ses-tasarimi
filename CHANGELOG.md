# Sürüm notları / Release notes

## Yayımlanmamış / Unreleased

**TR**
- Taşma düzeltmeleri (kart zemindir, her şey onun içinde kalır; 30 dil × 768/390 genişlik × 12 durum taraması:
  normal, ad kutusu, ⋯ menüsü ve içinde yeniden adlandırma, ses listesi, alt menü, taslaklar, satır menüsü, hata yazısı,
  *Duymak istediğin metin* penceresi ve içindeki taslak menüsü; 720 ölçüm, 0 taşma): çeşit kartında *Okuma listeme ekle*
  ad kutusu açılınca *Vazgeç* artık kartın 22 px dışına çıkmaz; uzun dillerde (Yunanca, Svahili) *Okuma listeme ekle*
  düğmesi çerçeveye sığmazsa kendi içinde iki satıra iner; ⋯ menüsünde *Yeniden adlandır* kutusu açılınca menü
  genişlese de görünür alanda kalır (Almanca, Rusça, Felemenkçe, Yunanca'da sağdan dışarı çıkıyordu). *Ses tasarla*
  formu 767×794'te 30 dilin hepsinde kaydırmasız: boş metin kutusunda uzun ipucu artık kaydırma çubuğu çizmez,
  Myanmar dilinde satır yüksekliği sabitlendi (form 42 px uzuyordu). Test: `tests/test_arayuz_tasma.py`.
- *Örnek tarif* seçicisinde aynı adlar tekrar gibi görünmez: 18 rol 8 dilde aynı adla geliyordu (Türkçe arayüzde
  *Belgesel anlatıcısı, erkek* 8 kez). Arayüz dili dışındaki seçenek artık dilini taşır (*Belgesel anlatıcısı, erkek ·
  Deutsch*); kapalı seçicide de seçilen örneğin dili görünür. Test: `tests/test_arayuz_ornek_secici.py`.
- *Duymak istediğin metin* kutusunun ipucu 30 dilde aynı anlamda: tıklayınca satır satır yazılır, beklemeler ayarlanır,
  boşsa örnek cümle okunur (28 dil eski *her satır bir cümle* metnindeydi; her dilde okuma ipucuyla aynı kökte yazıldı).
- Komut satırı: çıktı dosyaya ya da boruya yönlendirilince Windows'ta `UnicodeEncodeError` (cp1254) artık yok
  (`tasarla` son satırındaki →, `ornekler --dil zh --tam`); beş CLI çıktısı UTF-8. Test: `tests/test_cli_kodlama.py`.
- *Duymak istediğin metin* kutusuna tıklayınca *Bu sesle oku*'nun defteri (satır numarası, satır menüsü, bekleme bantları)
  bir pencerede açılır; *Tamam* metni ve beklemeleri kutuya yazar, *Vazgeç*/Esc dokunmaz, okuma sekmesindeki metin ve
  bantlar aynen kalır. **Taslaklar:** defterin iki yerinde (okuma sekmesi ve bu pencere) *📄 Taslaklar* düğmesi;
  hazırladığın metni beklemeleriyle kaydedersin, tek tıkla yüklersin (Ctrl+Z geri alır), ⋯ ile üzerine kaydet,
  yeniden adlandır, sil. Kayıt `sesler/taslaklar.json` (git dışı). Ses tasarla formu 767×794 pencerede kaydırmasız sığar.
  Test: `tests/test_taslaklar.py`.
- İki ses tek kartta: tasarımın ham kaydı bir kez çıkar, aynısı bir daha gelmez; sürekli duyacağın ses, o kaydın referans
  olarak verildiği, çeşidin kendi tohumuyla yapılan okumadır. *Ses tasarla* formunda yeni çerçeve *↻ Duymak istediğin metin*
  (satır = cümle, boş satır = paragraf beklemesi; boşsa örnek cümle okunur): *Tasarla*'ya bir kez basınca her çeşit önce
  tasarlanır, sonra bu metni kalıcı sesiyle okur (bütün okumalar tek motor oturumunda, tasarımdan sonra model bir kez daha
  yüklenir; ilerleme iki aşamayı tek çubukta sayar). Çeşit kartı büyüdü: üstte gri *Ham tasarım sesi*, altında turuncu çerçevede *↻ Sürekli duyacağın ses bu*
  (tohum yazılı) oynatıcısı ve *Bu sesle oku* / *Okuma listeme ekle* düğmeleri. Ses menüsündeki ▶ de artık kalıcı sesi
  çalar. Çeşit klasörüne `dinleme.wav`, kartına `dinleme`, `dinleme_metni`, `dinleme_sn` yazılır; okuma yarım kalırsa
  ya da okuma motoru durursa tasarım bozulmaz, kartta not çıkar; yazdığın metin kartta saklanır, üretim
  yeniden açılınca kutuya döner. Komut satırında `--dinleme`. Eski kartlar eskisi gibi görünür. 30 dilde.
  Test: `tests/test_tasarim_dinleme.py`.
- Okunan satır: sonuç çalarken o an okunan cümlenin numarası ve satırı defterde parlar, satır görünür alana kayar (boş satırlar
  atlanır; metin sonradan değiştiyse aynı cümle aranır). Satır menüsünde en üstte *▶ Buradan dinle* (sonuçta o satır varsa,
  30 dilde). Sunucu ses dosyasında tek aralık (`Range`) isteğini karşılar: oynatıcıda ileri/geri atlama artık çalışır;
  dil dosyaları `Cache-Control: no-cache` ile gelir (güncellemeden sonra eski yazı kalmaz).
- Ctrl+Enter (Mac'te ⌘+Enter): *Ses tasarla* sekmesinde *Tasarla*'yı, okuma sekmesinde *Bu sesle oku*'yu başlatır
  (düğme pasifken ya da menü açıkken hiçbir şey yapmaz; defterin Enter ve Alt kısayolları aynı kalır; odak yerinde kalır).
- Okuma metni ve bekleme bantları sayfa yenilenince kaybolmaz: tarayıcının yerel belleğinde durur (yazarken 400 ms
  seyreltilerek, sayfadan çıkarken hemen; açılış bitmeden hiçbir şey yazılmaz). Seçili ses zaten hatırlanıyordu.
- İnen okumanın adı artık hep `okuma.wav` değil: ses adı + okuma zamanı (ör. `Zeynep_Belgesel_Anlatıcı_2026-11-02_0152.wav`).
  Harfler (Türkçe, Arapça…) kalır; dosya adında yasak işaretler ve boşluk `_` olur. Test: `tests/test_arayuz_okuma.py`.
- Başlıkta küçük, soluk sürüm yazısı: `v0.2.0 · <kısa commit>` (izlenen dosyada kaydedilmemiş değişiklik varsa
  `+` eki; git yoksa yalnız sürüm). Videoda ve ekran görüntüsünde hangi sürümün kullanıldığı görünür. Tek kaynak
  `ses_tasarim/__init__.py` (`__version__` 0.2.0); git sunucu açılışında bir kez, penceresiz sorulur.
- İlerleme çubuğu *Bu sesle oku*'da da var (Tasarla ile aynı parça, düğmenin yanında). Çubuk baştan bir süre tahminiyle
  akar (*geçen / ~toplam*), gerçek ilerlemenin altına inmez, geri gitmez, bitmeden %97'yi geçmez. Tahmin bu makinenin
  ölçümlerinden öğrenilir: süre = açılış + karakter × sn/karakter (tasarla ve okuma ayrı, okumada sesin kendi katsayısı),
  her bitişte üstel ortalamayla güncellenir, aykırı ölçüm atlanır. Kayıt `onbellek/sure_olcumu.json` (repoya girmez).
  Test: `tests/test_sure_tahmini.py`.
- Sade ses akışı: *Sesin adı* etiketi *Üretim adı* oldu (30 dilde, her dilin kendi doğal karşılığıyla); çeşit kartında
  *Okuma listeme ekle* iki düğmenin yerinde ad kutusu açar (✓ önce adı sonra listeyi yazar, *Vazgeç* hiçbir şey yazmaz,
  kart yerinden ve boyundan oynamaz). *Hazır sesler* sekmesi kalktı: hazır sesler okuma sekmesindeki ses menüsünde
  bayraklı durur, tanıtımı satırın ipucunda. Ses menüsü yalnız *Okuma listem* + *Hazır sesler*; tasarlanan çeşit listeye
  eklenince görünür. Her satırda ▶ dinle (tek ortak çalar; ikinci basış durdurur, menü kapanınca susar, Boşluk tuşu da
  çalar), kalp ve ⋯ hep görünür. Adı değiştirilmiş çeşit menüde iki satır: üstte kendi adı, altta gri köken
  (*üretim adı · çeşit N*); ⋯ alt menüde *Üretimine git* (Ses tasarla o üretimle açılır, kart vurgulanır). Ses listesindeki
  ⋯ alt menü olarak açılır, liste açık kalır; menüler kullanıcının gerçekten gördüğü alanda açılır.
- Okuma listesi: *Ses tasarla* çeşit kartında ve *Hazır sesler* kartında *Bu sesle oku*'nun yanında *Okuma listeme ekle*
  düğmesi. Basınca ses (kendi referansı ve tohumuyla) listeye girer, düğme dolu kalple *Listede* olur ve kısa bir
  *Okuma listesine eklendi* satırı çıkar; tekrar basınca çıkar. Liste tektir (iki sekmeden eklenen aynı yerde) ve
  kullanıcının ses klasöründe `sesler/okuma_listesi.json` dosyasında durur (repoya girmez); uygulama yeniden açılınca da
  kalır. `GET /api/sesler` cevabında `okuma_listesi`, değiştirmek için `POST /api/okuma_listesi {kimlik, ekle}`
  (eklemede yalnız var olan ses kimliği; aynı Host/JSON/boyut kuralları).
- *Bu sesle oku* sekmesinde uzun düz ses listesi kalktı: tek satırlık ses düğmesi (bayrak + ad). Basınca satır ve bekleme
  menüsüyle aynı menü hemen altında açılır: başlıkta seçili ses, en üstte *Okuma listem* (kalpli sesler), çizgi, bayraklı
  hazır sesler (önce arayüz dili), çizgi, tasarlanan sesler (*ad · çeşit N*). Seçili ses vurgulu; satırdaki kalp (üstüne
  gelince görünür) listeye ekler/çıkarır; ↑/↓ ve Enter ile seçilir, Esc ya da dışarı tıklama kapatır. Son seçilen ses
  hatırlanır.
- *Hazır sesler* sekmesi: üstte yalnız hazır sesi olan dillerin bayrakları ve ses sayıları (*Tümü 14*, 🇹🇷 7, diğerleri 1);
  bayrağa basınca o dilin sesleri görünür, seçim hatırlanır. Her kartta *Bu sesle oku* (okuma sekmesini o ses seçili açar)
  ve *Okuma listeme ekle*. Yeni yazılar 30 dilde; sağdan sola dillerde Latin ad ve tanıtım doğru yönde.
  Testler: `tests/test_okuma_listesi.py`, `tests/test_arayuz_ses_menusu.py`.
- Hazır seslerin görünen adları anlamlı ve Türkçe harfli: *Zeynep Belgesel Anlatıcı*, *Enerjik Spiker*, *Usta Haber
  Spikeri*, *Masal Cadısı*, *Tok Sesli Anlatıcı*, *Yaşlı Bilge*, *Gizemli Bilge*; yabancı dildekiler *Fransızca Belgesel
  Anlatıcı* kalıbında. Yalnız `gorunen_ad` değişti; klasör adı ve kimlik (`hazir/belgesel_hanim` vb.) aynı, komut satırı ve
  okuma listesi etkilenmez.
- Ses yönetimi: *Bu sesle oku* ses menüsünde her satırın ⋯ düğmesi (üstüne gelince görünür), *Ses tasarla* çeşit kartı ve
  *Hazır sesler* kartındaki ⋯ aynı menüyü açar: *Bu sesle oku*, okuma listesine ekle/çıkar, *Yeniden adlandır* (menüde
  kutu, Enter ya da ✓; boş bırakınca asıl ad döner; *Asıl ada dön*), tasarlanan seste *Sil*, hazır seste *Gizle*. Silme
  ve gizleme önce onay sorar. Silinen ses `sesler/_cop/` altına taşınır, gizlenen hazır ses repodaki dosyaya yazılmaz;
  takma adlar ve gizlenenler `sesler/yerel_katman.json` dosyasında durur (repoya girmez). Ses menüsünün altındaki
  *Gizlenen ve silinen sesler (N)* bölümünden *Geri getir*. `GET /api/sesler` cevabında `gizli` ve `cop`;
  `POST /api/ses_yonet {kimlik, islem, ad?, cop?}` (`islem`: ad, gizle, goster, sil, geri; aynı Host/JSON/boyut
  kuralları). 30 dilde. Test: `tests/test_ses_yonetimi.py`.
- Ses tasarla: okutulan metin kutusu artık *Örnek cümle (sesi tanımak için, 1-2 cümle)*; kutu 3 satır, altında dile göre
  canlı süre çubuğu (~N sn / en fazla 20 sn, aşınca kırmızı). Tahmini 22 sn'yi (%10 pay) aşan metinle Tasarla başlamaz,
  sunucu da `tasarim_uzun` hatasıyla reddeder; *Okuma sekmesine taşı* düğmesi tam metni cümle cümle okuma kutusuna koyar,
  tasarımda ilk 1-2 cümle kalır. Hız: hazır seslerin kaydından ölçülen karakter/saniye (tr, en, de, fr, es, ru, ja, zh),
  ölçülmeyen dillerde varsayılan. 30 dilde metin; `POST /api/sure`. Test: `tests/test_tasarim_suresi.py`.
- Okuma kutusunda satır menüsü: satır numarasına tıklayınca (ya da Alt+Enter) yukarı/aşağı taşı, sıraya taşı, çoğalt,
  sil. Klavye: Alt+↑/↓ taşır, Alt+Shift+↓ çoğaltır; numaradan sürükleyip bırakmak da olur. Ctrl+Z metni ve durakları
  birlikte geri alır. Sağdan sola dillerde (Arapça, İbranice) de çalışır; ekran okuyucu rolleri ve hareket azaltma
  ayarı gözetilir.
- Cümleler arası durak bandı: iki satır arasındaki ince banda tıklayınca durak süresi seçilir (bağlı 0,25 · normal 0,5 ·
  paragraf 1 · ağır 1,5 sn). Dişli çarkla kendi süren (0-5 sn); en çok 6 özel süre tarayıcıda saklanır, kalple favori en
  üstte; özel süre silinmeden önce sorulur, metinde kullanıldığı yerler varsayılana döner. Bant cümleyle birlikte taşınır
  ve çoğalır. Elle yazılan `|| x` işareti banda taşınır; geçersiz işarette (0-5 sn dışı, yarım, bilinmeyen ad) satır
  kırmızı olur ve okuma gönderilmez.
- Arayüzde boş satır artık anlam taşımaz: paragraf = 1 sn ve üstü bant. Enter'a iki kez basmak, yapıştırma ve sayfa
  açılışı boş satırı 1 sn'lik paragraf bandına çevirir. Komut satırında boş satır eskisi gibi paragraf durağıdır.
- Okuma metninde özel durak süresi: satır sonunda `|| 0,8` ya da `|| 1.2s` (0-5 sn); işaretteki rakam "okunamayan
  işaret" sayılmaz. Test: `tests/test_bos_satir.py`.
- Arayüz metinleri 30 dilde yerli kullanıma göre yeniden gözden geçirildi (160 düzeltme: hitap ve terim tutarlılığı,
  Arapça ve İbranicede sayı uyumu). Test: `tests/test_arayuz_dilleri.py`, `tests/test_arayuz_satir.py` (davranış
  testleri node ister, yoksa atlanır).
- Ses tasarla: *Tasarla* yanında kronometre ve ilerleme çubuğu; çeşit sayısı en fazla 50; metin kutularında yazım
  denetimi (kırmızı dalgalı çizgi) kapalı; form değişince eski hata yazısı silinir.
- Linux kurulum betiğinde indirme işlevi adlandırılmış değişkenlerle yazıldı (davranış aynı).
- Deneysel Ubuntu/Linux (NVIDIA CUDA) kurulumu: `scripts/kur-linux.sh` yamalı motoru kaynaktan derler (sabit URL ve
  sha256, sudo çalıştırmaz), isteğe bağlı `Dockerfile.linux`; belge `docs/linux.md`. Linux'ta ayar kontrolü Windows'a özgü
  `cudart64_12.dll` dosyasını istiyordu, düzeltildi (Windows'ta kontrol aynen sürer). Katkı: @mslmyilmaz5 (Müslim Yılmaz), #15. Aynı Docker yolu GTX 1050 Ti 4 GB'de de denendi (Windows 10, Docker Desktop/WSL2, `CUDA_ARCHITECTURES=61`): komut satırı okuma ve tasarım çalışır, tepe VRAM 2849 MiB, aynı girdiyle iki okuma bit bit aynı; arayüz Windows tarayıcısından açılmaz, Windows'ta arayüz için `scripts\kur.ps1` kullanın. Ölçüm ve komutlar `docs/linux.md`.
- Arayüz yerleşimi sadeleşti: dört sekme (Ses tasarla, Bu sesle oku, Ses klonlama, Hazır sesler), geniş ekranda sayfa
  kaymaz, kaydırma yalnız listelerde. Ses tasarla iki sütun: solda ad, çeşit, örnek tarif, tarif ve metin; sağda
  *Üretimler*: her Tasarla basışı bir üretimdir, seçince form o üretimin bilgileriyle dolar ve çeşitleri dinlenir;
  her çeşitte *Bu sesle oku* düğmesi okuma sekmesine o sesle geçer. Dil seçimi tek düğmede açılır menü. Örnek tarifler
  önce arayüz dilinde sıralanır. Okunacak metin kutusu çizgili ve satır numaralı (uzun cümle sarılsa da tek numara).
- Okumada boş satır paragraf durağı sayılır (1 sn); satır sonundaki açık `||` işareti önce gelir. Test: `tests/test_bos_satir.py`.
- Arayüz 30 dilde (VoxCPM2'nin desteklediği dillerin tamamı): üstte bayrak seçici, gece/gündüz düğmesi; seçim tarayıcıda
  saklanır, Arapça ve İbranice sağdan sola. Sunucu hata ve durumları kodla gönderir, arayüz seçili dilde yazar. Çeviriler
  `ses_tasarim/arayuz_dilleri/<kod>.json`, her dil o ülkenin yazılım alışkanlığına göre gözden geçirildi; bayraklar
  flag-icons (MIT). Ses adı Tayca, Hintçe, Birmanca gibi yazılarda bozulmadan klasör adı olur. Test: `tests/test_arayuz_dilleri.py`.
- Örnek ses tarifleri: 8 dilde 18 rol, toplam 144 örnek (belgesel, haber, reklam, sesli kitap, masal, podcast, öğretmen,
  fragman, meditasyon, spor; kadın ve erkek). Tarif İngilizce, içinde milliyet ve yerli aksan; ses yaratılırken okutulan
  metin rolün türüne göre o dilde hazır. `python -m ses_tasarim.ornekler`, `tasarla --ornek <id>`, arayüzde *Örnek
  tarif* kutusu (144 tarif dil başlıklarıyla gruplu), `GET /api/ornekler`, belge `docs/ornek_tarifler.md`, testler `tests/test_ornekler.py`.
  Henüz ölçülmedi: her örnek tek tek tasarlanıp dinlenmedi.
- README ve AGENTS: video dublajı için DubWorld yönlendirmesi (tasarlanan ses orada `ses.voxcpm2_ses` ile kullanılır).
- Ara dosyalar artık birikmiyor: motorun çalışma dosyaları (`motor.log` satır başına yaklaşık 3 MB, PCM dökümleri)
  `_motor_is` klasöründe tutulur ve iş başarıyla bitince silinir; `tasarla` `_calisma/tasarim_*`, `oku` `<çıktı>/_motor`
  bırakmaz. Motor hata verir ya da bir satır yarım kalırsa dosyalar inceleme için kalır; `SES_TASARIM_ARA_DOSYA_TUT=1`
  her zaman saklar. macOS uygulaması zaten böyle çalışıyordu. Test: `tests/test_ara_dosya.py`.
- Çok dilli okuma ve tasarım: `--dil` (tr, en, fr, de, es, ru, zh, ja denendi). Tr dışındaki dillerde Türkçe okunuş
  sözlüğü uygulanmaz, kesme işareti kalır; dil metinden otomatik tanınır (`okunus.detect`); kararsız kalınca tasarımda örnek tarifin dili, okumada sesin kartındaki dil (`dil`) kullanılır; tasarlanan sesin dili kartına yazılır; arayüzde dil kutusu yok; sunucu eski istemcinin `dil` alanını yok sayar; `--dil` isteğe bağlı.
- Yedi yerli anlatıcı hazır ses olarak eklendi: `hazir_sesler/anlatici_{en,fr,de,es,ru,zh,ja}` (istem, tasarım metni,
  tohum, referans, Kapadokya metninden kısa örnek okuma).
- `oku`: cümle cümle hız kapısı (`supheli_satirlar`): harf/sn değeri ortancadan çok sapan satırlar yazdırılır.
- Claude Code becerisi `.claude/skills/ses-tasarimi/SKILL.md`: tarif → çeşitler → referanslı dinletme → seçim → cümle
  cümle okuma. Belge `docs/cok_dilli.md`, çevrimdışı testler `tests/`.
- macOS (Apple Silicon, Metal) desteği: `scripts/kur.sh` (aynı sabit model ve kaynak, sha256 kontrolü, yama, ~1 dk Metal
  derlemesi, `.venv`, `ayarlar.json` `"backend": "metal"`, GPU kontrolü) ve çift tıkla başlatan `baslat.command`. Yamada
  değişiklik gerekmedi. `motor.py` macOS'ta GPU belleğini `ioreg` ile ölçer (arayüzdeki "VRAM tepe"). MacBook Air M4
  16 GB ölçümleri (1 sn ses ≈ 2 sn, aynı tohum bayt bayt aynı, ~5,3 GB RAM, 12 dk'da ısınmadan kaynaklı yavaşlama yok):
  `docs/mac.md`.
- `oku`: komut satırında göreli `--cikti` yolu (ör. `cikti/deneme`) referans yolunu ikiliyor, motor "could not open WAV
  input" ile düşüyordu; yol artık mutlak yapılıyor (her platformda; arayüz etkilenmiyordu).
- `macos/`: native SwiftUI Mac uygulaması (Apple Silicon, macOS 14+). Web arayüzündeki üç bölüm; yamalı motor uygulamanın
  içinde, model ilk açılışta indirilir (sha256, duraklat/sürdür). Klonlama izin kapısı korunur. `hazir_sesler/` ve
  `ayarlar/okunus_sozlugu.tsv` repodan kullanılır, `ses.json` kartları iki sürüm arasında taşınabilir. Ayrıntılar:
  `macos/README.md`.
- `baslat.bat`: arayüzü çift tıkla başlatır, hazır olunca tarayıcıda açar; kurulum yoksa kurulum komutunu gösterir.
- README TR/EN: Vulkan kurulum komutundaki bozuk `C:\vox` düzeltildi (AGENTS.md de); Git'siz kurulum (Download ZIP),
  "hangi kartım var" kontrolü, sık kurulum sorunları tablosu, "Katkıda bulunanlar" bölümü.
- Issue formları: hata bildirimi ve özellik önerisi; Discussions (Q&A, Ideas, Show and tell) ve güvenlik yönlendirmesi.
- Davranış kuralları: `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1, Türkçe özet; bildirim GitHub özel bildirim yolu).
- `SECURITY.md`: sabit yanıt süresi kaldırıldı; bildirimlere en kısa sürede bakılır.
- README TR/EN: en üstte "Hızlı başlangıç (3 adım)": kod zip'i ve CUDA / Vulkan motor paketlerinin doğrudan bağlantıları.
- Ses klonlama politikası (README, ETHICS, AGENTS, marka sesi rehberi): klonlama yalnız kendi sesiniz ya da sahibinin
  açık izniyle; arayüz izin onayı ister; yasak kullanımlar, sorumluluk ve kötüye kullanım bildirimi.
- Arayüze "3. Ses klonlama" bölümü (`ses_tasarim/klonla.py`, CLI `python -m ses_tasarim.klonla`): kendi sesiniz ya da
  izinli ses (wav/mp3/flac/ogg, 5-30 sn önerilir, 36 sn üstü kırpılır) + kaydın birebir metni + okunacak metin + tohum;
  izin onay kutusu işaretlenmeden düğme kapalı, sunucu da onaysız isteği reddeder. Kayıt ve referans kodlaması yalnız
  geçici klasörde işlenir, iş bitince silinir; çıktı `klon_synthetic.wav` (WAV INFO "synthetic" etiketi) ve
  "Yapay üretilmiş sestir" notu. Kalite sabit: 16 adım, cfg 2.0.
- Klonlama metin ve teknik düzeltmeleri: "gerçek kişi değil" gibi eski cümleler (hazır ses notları, arayüz örnek
  metni, README, issue/PR şablonları, CONTRIBUTING, THIRD_PARTY) yeni çizgiye göre yeniden yazıldı; motor hata ya
  da Ctrl+C'de kapatılır, geçici klasör hata yolunda da silinir (kilitliyse yeniden denenir); komut satırı
  `--onay` yoksa kaydı okumadan reddeder, hata mesajları ve `--help` TR/EN; arayüz 3 sn altı ve 30-36 sn uyarısı.
- CPU arka ucunda (`ayarlar.json` içinde `"backend": "cpu"`) çok cümleli okumada cümle sonu (EOS) tespiti
  düzeltildi, uzun metin kesilmeden okunur; blok kaymasına karşı `decoder_seen` koruması. Katkı: @grogureis, #14.

**EN**
- Overflow fixes (the card is the ground, everything stays inside it; scanned 30 languages × 768/390 width × 12 states:
  normal, name box, ⋯ menu and its rename box, voice list, submenu, drafts, line menu, error text, the *Text you want to
  hear* dialog and its drafts menu; 720 checks, 0 overflows): with the *Add to my reading list* name box open, *Cancel*
  no longer sticks 22 px out of the variant card; in long languages (Greek, Swahili) the *Add to my reading list* button
  wraps inside its frame instead of overflowing; opening the *Rename* box in the ⋯ menu keeps the widened menu inside the
  visible area (it ran off the right edge in German, Russian, Dutch, Greek). The *Design a voice* form fits 767×794
  without scrolling in all 30 languages: a long placeholder in an empty text box no longer draws a scrollbar, and
  Burmese gets a fixed line height (the form was 42 px too tall). Test: `tests/test_arayuz_tasma.py`.
- The *Example prompt* picker no longer looks duplicated: the 18 roles share names across 8 languages (in the Turkish UI
  *Documentary narrator, male* showed 8 times). Options outside the UI language now carry their language
  (*Documentary narrator, male · Deutsch*), also visible in the closed picker. Test: `tests/test_arayuz_ornek_secici.py`.
- The *Text you want to hear* placeholder means the same in all 30 languages: click to write line by line and set the
  pauses; left empty, the sample sentence is read (28 languages still had the old *one sentence per line* text).
- Command line: redirecting output to a file or pipe no longer raises `UnicodeEncodeError` (cp1254) on Windows (the →
  in the last `tasarla` line, `ornekler --dil zh --tam`); all five CLIs write UTF-8. Test: `tests/test_cli_kodlama.py`.
- Clicking the *Text you want to hear* box opens the *Read with this voice* notebook (line numbers, line menu, pause
  bands) in a dialog; *OK* writes the text and pauses back, *Cancel*/Esc changes nothing, and the reading tab keeps its
  own text and bands. **Drafts:** a *📄 Drafts* button in both notebook places; save a prepared text with its pauses,
  load it with one click (Ctrl+Z undoes), and use ⋯ to overwrite, rename or delete. Stored in `sesler/taslaklar.json`
  (outside git). The design form fits a 767×794 window without scrolling. Test: `tests/test_taslaklar.py`.
- Two voices on one card: the raw design recording comes out once and never the same again; the voice you keep hearing
  is a reading with that recording as reference and the variant's own seed. The *Design a voice* form has a new frame
  *↻ Text you want to hear* (line = sentence, blank line = paragraph pause; empty reads the sample sentence): one press of
  *Design* designs every variant and then reads this text with its lasting voice (all readings in one engine session,
  the model loads once more after the design; the progress bar counts both phases). The variant card grows: a grey *Raw design voice* on top, below it an
  orange frame *↻ This is the voice you'll keep hearing* (with the seed), its player and the *Read with this voice* /
  *Add to my reading list* buttons. The ▶ in the voice menu now plays the lasting voice too. The variant folder gets
  `dinleme.wav`, the card `dinleme`, `dinleme_metni`, `dinleme_sn`; a failed or crashed reading never fails the design,
  the card shows a note; the text as typed is kept and comes back when the production is reopened. CLI: `--dinleme`. Older cards look as before. 30 languages. Test: `tests/test_tasarim_dinleme.py`.
- The line being read: while the result plays, its number and line glow in the notebook and scroll into view (blank lines
  are skipped; if the text was edited the same sentence is looked up). The line menu starts with *▶ Listen from here* when
  the result has that line (30 languages). The server answers single byte `Range` requests for files, so seeking in the
  player works now; language files are sent with `Cache-Control: no-cache` (no stale strings after an update).
- Ctrl+Enter (⌘+Enter on Mac) starts *Design* on the design tab and *Read with this voice* on the reading tab (nothing
  happens while the button is disabled or a menu is open; the notebook's Enter and Alt shortcuts are unchanged; focus stays put).
- The reading text and its pause bands survive a page reload: kept in the browser's local storage (debounced 400 ms
  while typing, at once when the page is left; nothing is written before loading finishes). The chosen voice was already remembered.
- The downloaded reading is no longer always `okuma.wav`: voice name + reading time (e.g.
  `Zeynep_Belgesel_Anlatıcı_2026-11-02_0152.wav`). Letters stay; characters forbidden in file names and spaces become `_`.
- A small, faint version in the header: `v0.2.0 · <short commit>` (`+` when tracked files have uncommitted changes;
  version only without git), so videos and screenshots show which version was used. Single source
  `ses_tasarim/__init__.py` (`__version__` 0.2.0); git is asked once at server start, without a window.
- A progress bar in *Read with this voice* too (same part as Design, next to the button). It starts from a duration
  estimate (*elapsed / ~total*), never drops below real progress, never goes back, stays under 97 % until done. The estimate
  is learned on this machine: duration = start-up + characters × s/char (design and reading apart, a per-voice factor for
  reading), updated with an exponential average after every job, outliers skipped. Stored in `onbellek/sure_olcumu.json`
  (not in the repo). Test: `tests/test_sure_tahmini.py`.
- Simpler voice flow: the *Voice name* label is now *Generation name* (30 languages, each in its own natural wording); on a
  variant card *Add to my reading list* opens a name box in place of the two buttons (✓ saves the name, then the list;
  *Cancel* writes nothing; the card keeps its place and size). The *Bundled voices* tab is gone: bundled voices live in the
  reading tab's voice menu with flags, their description in the row tooltip. The voice menu shows only *My reading list*
  and *Bundled voices*; a designed variant appears once it is added to the list. Each row has ▶ listen (one shared player;
  a second press stops, closing the menu stops it, Space plays too), the heart and ⋯, always visible. A renamed variant
  takes two lines: its own name above a grey origin (*generation name · variant N*); the ⋯ submenu has *Go to generation*
  (opens Design a voice on that generation and highlights the card). The ⋯ in the voice list opens as a submenu and the
  list stays open; menus open inside the area the user can actually see.
- Reading list: an *Add to my reading list* button next to *Read with this voice* on each variant card (*Design a voice*)
  and on each bundled-voice card. The voice (with its own reference and seed) joins the list, the button turns into a
  filled heart *In my list* and a short *Added to the reading list* line appears; press again to remove. There is one list
  for both tabs, stored in the user's voice folder as `sesler/okuma_listesi.json` (never in the repository), so it
  survives restarts. `GET /api/sesler` returns `okuma_listesi`; `POST /api/okuma_listesi {kimlik, ekle}` changes it
  (adding accepts existing voice ids only; same Host/JSON/size rules).
- *Read with this voice*: the long plain voice list is gone. A one-line voice button (flag + name) opens the same popup
  menu as the line and pause menus, right below it: the selected voice in the header, *My reading list* (hearted voices)
  on top, a divider, bundled voices with flags (interface language first), a divider, designed voices (*name · variant N*).
  The selected voice is highlighted; the heart on each row (visible on hover) adds or removes it; ↑/↓ and Enter choose,
  Esc or a click outside closes. The last chosen voice is remembered.
- *Bundled voices* tab: a row of flags with voice counts, only for languages that have bundled voices (*All 14*, 🇹🇷 7,
  the others 1); a flag filters the cards and the choice is remembered. Each card has *Read with this voice* (opens the
  reading tab with that voice selected) and *Add to my reading list*. New strings in all 30 languages; Latin names and
  descriptions keep their direction in right-to-left languages. Tests: `tests/test_okuma_listesi.py`,
  `tests/test_arayuz_ses_menusu.py`.
- Bundled voices have meaningful Turkish display names: *Zeynep Belgesel Anlatıcı*, *Enerjik Spiker*, *Usta Haber
  Spikeri*, *Masal Cadısı*, *Tok Sesli Anlatıcı*, *Yaşlı Bilge*, *Gizemli Bilge*; the other languages follow *Fransızca
  Belgesel Anlatıcı* (French documentary narrator). Only `gorunen_ad` changed; folder names and ids (`hazir/belgesel_hanim`
  etc.) are the same, so the command line and the reading list are unaffected.
- Voice management: a ⋯ button on each row of the voice menu in *Read with this voice* (visible on hover), on each
  variant card in *Design a voice* and on each bundled-voice card opens the same menu: *Read with this voice*, add to or
  remove from the reading list, *Rename* (a box in the menu, Enter or ✓; leaving it empty restores the original name;
  *Back to original name*), *Delete* for designed voices, *Hide* for bundled ones. Deleting and hiding ask first. A
  deleted voice moves to `sesler/_cop/`; hiding a bundled voice never writes its repository files. Custom names and
  hidden voices live in `sesler/yerel_katman.json` (never in the repository). *Hidden and deleted voices (N)* at the
  bottom of the voice menu has *Restore*. `GET /api/sesler` returns `gizli` and `cop`;
  `POST /api/ses_yonet {kimlik, islem, ad?, cop?}` (`islem`: ad, gizle, goster, sil, geri; same Host/JSON/size rules).
  All 30 languages. Test: `tests/test_ses_yonetimi.py`.
- Design a voice: the design text box is now *Sample sentence (to get to know the voice, 1-2 sentences)*; 3 lines high,
  with a live per-language length bar below it (~N s / max 20 s, red when over). With an estimate above 22 s (10 %
  margin) Design does not start and the server rejects it with `tasarim_uzun`; *Move to reading tab* puts the full text
  into the reading box one sentence per line and keeps the first 1-2 sentences in the design box. Rates are characters
  per second measured on the bundled voices (tr, en, de, fr, es, ru, ja, zh), a default elsewhere. Strings in all 30
  languages; `POST /api/sure`. Test: `tests/test_tasarim_suresi.py`.
- Line menu in the reading box: click a line number (or Alt+Enter) to move up/down, move to a position, duplicate or
  delete. Keyboard: Alt+↑/↓ moves, Alt+Shift+↓ duplicates; dragging by the number works too. Ctrl+Z undoes text and
  pauses together. Works in right-to-left languages (Arabic, Hebrew); screen reader roles and reduced motion are respected.
- Pause band between sentences: click the thin band between two lines to pick the pause (bagli 0.25 · normal 0.5 ·
  paragraf 1 · agir 1.5 s). The gear adds your own length (0-5 s); up to 6 custom lengths are kept in the browser, the
  heart pins favourites to the top; deleting a custom length asks first and its uses in the text revert to the default.
  The band moves and duplicates with its sentence. A typed `|| x` marker is moved into the band; an invalid marker
  (outside 0-5 s, incomplete, unknown name) turns the line red and the reading is not sent.
- In the UI a blank line no longer carries meaning: a paragraph is a band of 1 s or more. Pressing Enter twice, pasting
  and opening the page turn blank lines into a 1 s paragraph band. On the command line a blank line is still a paragraph pause.
- Custom pause length in reading text: `|| 0,8` or `|| 1.2s` at the end of a line (0-5 s); the digits in the marker do
  not count as an unreadable mark. Test: `tests/test_bos_satir.py`.
- UI strings in all 30 languages reviewed again for native usage (160 fixes: consistent forms of address and terms,
  number agreement in Arabic and Hebrew). Tests: `tests/test_arayuz_dilleri.py`, `tests/test_arayuz_satir.py`
  (behaviour tests need node and are skipped without it).
- Design a voice: a stopwatch and progress bar next to *Design*; up to 50 variants; spell check (red wavy underline)
  off in text boxes; an old error message clears when the form changes.
- Linux installer: the download function uses named variables (same behaviour).
- Experimental Ubuntu/Linux (NVIDIA CUDA) install: `scripts/kur-linux.sh` builds the patched engine from source (pinned URLs
  and sha256, never runs sudo), optional `Dockerfile.linux`; guide `docs/linux.md`. On Linux the settings check wrongly
  required the Windows-only `cudart64_12.dll`; fixed (the Windows check is unchanged). Contributed by @mslmyilmaz5
  (Müslim Yılmaz), #15. The same Docker path was also tried on a GTX 1050 Ti 4 GB (Windows 10, Docker Desktop/WSL2, `CUDA_ARCHITECTURES=61`): CLI reading and design work, peak VRAM 2849 MiB, two readings of the same input are bit-identical; the web UI does not open from a Windows browser, so use `scripts\kur.ps1` for the UI on Windows. Measurements and commands in `docs/linux.md`.
- Simpler UI layout: four tabs (Design a voice, Read with this voice, Voice cloning, Bundled voices); on wide screens
  the page does not scroll, only the lists do. Design is two columns: name, variants, example, description and text on
  the left; *Generations* on the right: each Design click is one generation, selecting it refills the form and lists
  its variants; every variant has a *Read with this voice* button that opens the reading tab with that voice. Language
  picker is a single dropdown button. Example descriptions list the UI language first. The reading text box is ruled
  and line-numbered (a wrapped long sentence keeps one number).
- Reading: a blank line now means a paragraph pause (1 s); an explicit `||` marker at the end of a line wins. Test:
  `tests/test_bos_satir.py`.
- Interface in 30 languages (every language VoxCPM2 supports): flag picker and light/dark toggle at the top; the choice is
  remembered in the browser, Arabic and Hebrew are right-to-left. The server sends coded errors and states, the page
  writes them in the selected language. Translations in `ses_tasarim/arayuz_dilleri/<code>.json`, each reviewed for
  local software conventions; flags from flag-icons (MIT). Voice names in Thai, Hindi, Burmese etc. stay intact as
  folder names. Test: `tests/test_arayuz_dilleri.py`.
- Example voice prompts: 18 roles in 8 languages, 144 in total (documentary, news, commercial, audiobook, fairy tale,
  podcast, teacher, trailer, meditation, sports; female and male). The prompt is English with nationality and native
  accent; the design text comes in that language, matched to the role. `python -m ses_tasarim.ornekler`,
  `tasarla --ornek <id>`, an *Example prompt* picker in the web UI (filtered by language), `GET /api/ornekler`,
  `docs/ornek_tarifler.md`, tests in `tests/test_ornekler.py`. Not measured yet: not every example was designed and heard.
- README and AGENTS: pointer to DubWorld for video dubbing (a voice designed here is used there via `ses.voxcpm2_ses`).
- Scratch files no longer pile up: engine work files (`motor.log`, about 3 MB per line, PCM dumps) live in `_motor_is`
  and are deleted after a successful run; `tasarla` leaves no `_calisma/tasarim_*`, `oku` no `<output>/_motor`. On an
  engine error or an unfinished line they are kept for inspection; `SES_TASARIM_ARA_DOSYA_TUT=1` always keeps them.
  The macOS app already worked this way. Test: `tests/test_ara_dosya.py`.
- Multilingual reading and design: `--dil` (tested: tr, en, fr, de, es, ru, zh, ja). Outside Turkish the Turkish
  dictionary is skipped and apostrophes are kept; the language is detected from the text (`okunus.detect`); when unsure,
  design falls back to the example's language and reading to the voice card's (`dil`); no language box in the web UI.
- Seven native narrators bundled: `hazir_sesler/anlatici_{en,fr,de,es,ru,zh,ja}` (prompt, design text, seed,
  reference, short sample from our Cappadocia script).
- `oku`: sentence speed gate (`supheli_satirlar`): lines whose characters per second is far from the median are printed.
- Claude Code skill `.claude/skills/ses-tasarimi/SKILL.md`: describe → variants → reference-based audition → pick →
  sentence-by-sentence reading. Docs `docs/cok_dilli.md`, offline tests `tests/`.
- macOS (Apple Silicon, Metal) support: `scripts/kur.sh` (same pinned model and source, sha256 checks, patch, ~1 min Metal
  build, `.venv`, `ayarlar.json` with `"backend": "metal"`, GPU check) and a double-click `baslat.command`. The patch needed
  no change. `motor.py` measures GPU memory with `ioreg` on macOS (the UI's "VRAM tepe"). MacBook Air M4 16 GB
  measurements (~2 s per 1 s of audio, same seed byte-identical, ~5.3 GB RAM, no thermal slowdown over 12 min): `docs/mac.md`.
- `oku`: a relative `--cikti` path on the command line (e.g. `cikti/deneme`) doubled the reference path and the engine
  failed with "could not open WAV input"; the path is now made absolute (all platforms; the web UI was not affected).
- `macos/`: native SwiftUI Mac app (Apple Silicon, macOS 14+) with the web UI's three sections; the patched engine is
  inside the app, the model is downloaded on first launch (sha256, pause/resume). The cloning consent gate is kept.
  Uses the repo's `hazir_sesler/` and `ayarlar/okunus_sozlugu.tsv`; `ses.json` cards move between both versions.
  Details: `macos/README.md`.
- `baslat.bat`: double-click to start the web UI; it opens the browser when ready and shows the install command if
  nothing is installed yet.
- README TR/EN: fixed the broken `C:\vox` in the Vulkan install command (AGENTS.md too); install without Git (Download
  ZIP), a "which GPU do I have" check, a common install problems table, a "Contributors" section.
- Issue forms: bug report and feature request; links to Discussions (Q&A, Ideas, Show and tell) and the security policy.
- Code of Conduct: `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1, Turkish summary; reports via GitHub private reporting).
- `SECURITY.md`: removed the fixed reply time; reports are looked at as soon as we can.
- README TR/EN: a 3-step "Quick start" at the top with direct links to the code zip and the CUDA / Vulkan engine packages.
- Voice cloning policy (README, ETHICS, AGENTS, brand voice guide): cloning only with your own voice or the owner's
  explicit permission; the UI asks you to confirm it; prohibited uses, responsibility and misuse reporting.
- New "3. Voice cloning" section in the UI (`ses_tasarim/klonla.py`, CLI `python -m ses_tasarim.klonla`): your own or a
  consented voice (wav/mp3/flac/ogg, 5-30 s advised, trimmed at 36 s) + its exact transcript + text to read + seed; the
  button stays disabled until the consent box is ticked and the server rejects requests without consent. The recording
  and its reference encoding live only in a temp folder that is deleted when the job ends; output is
  `klon_synthetic.wav` (WAV INFO "synthetic" tag) with an "AI-generated" note. Fixed quality: 16 steps, cfg 2.0.
- Cloning wording and hardening: old "not a real person" lines (bundled voice notes, UI sample text, README,
  issue/PR templates, CONTRIBUTING, THIRD_PARTY) rewritten for the new policy; the engine is killed on error or
  Ctrl+C and the temp folder is deleted on the failure path too (retried if locked); the CLI refuses without
  `--onay` before reading the recording, errors and `--help` are TR/EN; UI warns under 3 s and for 30-36 s.
- CPU backend (`"backend": "cpu"` in `ayarlar.json`): end-of-sentence (EOS) detection fixed for multi-sentence
  reading, long text is no longer cut; `decoder_seen` guard against block drift. Contributed by @grogureis, #14.

## v0.1.1 — 2026-10-23

**TR**
- Derlemesiz kurulum: `scripts\kur.ps1 -Kok C:\vox` artık Visual Studio istemez; modeli, CUDA 12.8 çalışma DLL'lerini,
  Releases'taki hazır motoru, `.venv`'i ve `ayarlar.json`'ı kurar, sonda ekran kartını kontrol eder (`KONTROL_OK`).
  Derleme ikinci yol: `-Derle` (`-Mimari native` varsayılan).
- Hazır motor artık çok mimarili: GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx (sm_89), RTX 50xx
  (sm_120a) için yerel kod + compute_89 PTX. v0.1.0 yalnız sm_61 yerel kod + compute_61 PTX taşıyordu (RTX kartlarda
  sürücü JIT'iyle çalışıyordu, ilk açılış yavaştı). Zip boyutu: 123 MB (v0.1.0: 20 MB); derleme süresi 8 işte
  55 dk (tek mimari: 12 dk).
- Sürüm zip'indeki `audiocpp_cli.exe` çift tıklanmaz; README.txt ilk satırı bunu söyler. İlk kullanıcı hatası
  ("cudart64_12.dll bulunamadı") belgede ve sorun giderme tablosunda.
- README TR/EN: hızlı kurulum en üstte, desteklenen kartlar, arayüz adresinin elle açıldığı, sık sorulanlar.
  AGENTS.md: iki yol (A hazır, B derleme), adım tablosu, yeni sürüm çıkarma bölümü.
- `.github/ISSUE_TEMPLATE`: kurulum sorunu formu (kart, Windows, sürücü, komut, hata çıktısı) ve Discussions bağlantısı.
- kur.ps1 düzeltmeleri: `-Adim` virgül ayrımı, Windows `tar.exe`, `git apply` çıktısı, UTF-8 log; derle.ps1 vswhere
  uyarısı giderildi; arayüz dolu portta sessizce ikinci sunucu açmıyor, iş hatalarında iz veriyor.
- Model indirme adresi Hugging Face commit'ine sabitlendi (`661a224e…`): `main` üzerindeki dosya 2026-10-19'da
  değişti (2 955 007 488 bayt, sha256 `8df1faf2…`, v0.9.2 spec); sabitlenmeden v0.1.0 kurulumu `sha256 tutmadı` veriyordu.
- Deneysel Vulkan motoru (AMD/Intel/NVIDIA, CUDA gerekmez): ayrı zip `…-win64-vulkan.zip`, kurulum `kur.ps1 -Vulkan`.
  Yalnız NVIDIA GTX 1050 Ti üzerinde Vulkan arka ucuyla denendi; AMD/Intel'de denenmedi, sonuç bekliyoruz.
  Ölçüm (GTX 1050 Ti, Vulkan, aynı 16 adım / cfg 2.0): tasarım çeşidi 108 sn (ilk çalıştırma 216 sn, gölgelendirici
  derlemesi dahil; CUDA 55 sn), okuma 1 sn ses için 6-13 sn hesap (CUDA ≈ 2 sn), VRAM tepe 2,8 GB; aynı tohum iki kez
  bit-bit aynı wav verdi. Uyarı: bu ölçüm sırasında disk başka bir işle doluydu (CUDA 55 sn boş diskte ölçüldü);
  temiz karşılaştırma bekliyor. Motor varsayılan olarak `Vulkan:0` cihazını seçer; birden çok Vulkan cihazı varsa (ör. dahili
  Intel + NVIDIA) `kur.ps1 -Vulkan` `[GPU]` satırını bulup `ayarlar.json` içine `cihaz` dizinini yazar (`--device`).
  Dahili Intel HD 630 üzerinde tasarım `maxComputeWorkGroupCount` hatasıyla durdu. Zip 18,6 MB. Derleme:
  `derle.ps1 -Vulkan` (Vulkan SDK ya da `-VulkanSdk <klasör>`: glslc, başlıklar, vulkan-1.lib).

**EN**
- No-compiler install: `scripts\kur.ps1 -Kok C:\vox` no longer needs Visual Studio; it fetches the model, the CUDA 12.8
  runtime DLLs, the prebuilt engine from Releases, creates `.venv`, writes `ayarlar.json` and checks the GPU
  (`KONTROL_OK`). Building from source is the second path: `-Derle` (`-Mimari native` by default).
- The prebuilt engine is now multi-architecture: native code for GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86),
  RTX 40xx (sm_89), RTX 50xx (sm_120a) plus compute_89 PTX. v0.1.0 carried only sm_61 code + compute_61 PTX (RTX cards
  ran it through the driver JIT, slow first start). Zip size 123 MB (v0.1.0: 20 MB); build time 55 min
  on 8 jobs (single architecture: 12 min).
- The `audiocpp_cli.exe` in the zip is not meant to be double-clicked; README.txt says so in its first line. The first
  user report ("cudart64_12.dll not found") is covered in the docs and the troubleshooting table.
- README TR/EN: quick install first, supported GPUs, how to open the UI, FAQ. AGENTS.md: two paths (A prebuilt,
  B build), step table, release how-to.
- `.github/ISSUE_TEMPLATE`: install-problem form (GPU, Windows, driver, command, error output) and a Discussions link.
- kur.ps1 fixes: comma-separated `-Adim`, Windows `tar.exe`, `git apply` output, UTF-8 log; derle.ps1 vswhere warning
  gone; the UI refuses a busy port instead of silently sharing it and returns a traceback on job errors.
- Model download pinned to a Hugging Face commit (`661a224e…`): the file on `main` was replaced on 2026-10-19
  (2 955 007 488 bytes, sha256 `8df1faf2…`, v0.9.2 spec); without the pin the v0.1.0 installer failed with `sha256 tutmadı`.
- Experimental Vulkan engine (AMD/Intel/NVIDIA, no CUDA): separate zip `…-win64-vulkan.zip`, install with
  `kur.ps1 -Vulkan`. Verified only on an NVIDIA GTX 1050 Ti through the Vulkan backend; untested on AMD/Intel, reports
  welcome. Measured (GTX 1050 Ti, Vulkan, same 16 steps / cfg 2.0): one design variant 108 s (first run 216 s including
  shader compilation; CUDA 55 s), reading 6-13 s of compute per 1 s of speech (CUDA ≈ 2 s), peak VRAM 2.8 GB; the same
  seed produced bit-identical wavs twice. Caveat: the disk was busy with another job during this measurement (the CUDA
  55 s was measured on an idle disk); a clean comparison is pending. The engine defaults to device `Vulkan:0`; with several Vulkan devices (e.g.
  integrated Intel + NVIDIA) `kur.ps1 -Vulkan` picks the `[GPU]` line and writes its index as `cihaz` into `ayarlar.json`
  (`--device`). On the integrated Intel HD 630 a design stopped with a `maxComputeWorkGroupCount` assert. Zip 18.6 MB.
  Build: `derle.ps1 -Vulkan` (Vulkan SDK or `-VulkanSdk <folder>`: glslc, headers, vulkan-1.lib).

## v0.1.0 — 2026-10-22

İlk sürüm / first release: VoxCPM2 Turkish voice design on a 4 GB GPU, patched audio.cpp v0.7.2 engine, 7 bundled
synthetic voices, local web UI, one-command installer (build from source), prebuilt sm_61 engine zip.

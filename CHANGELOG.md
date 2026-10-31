# Sürüm notları / Release notes

## Yayımlanmamış / Unreleased

**TR**
- Ses tasarla: okutulan metin kutusu artık *Örnek cümle (sesi tanımak için, 1-2 cümle)*; kutu 3 satır, altında dile göre
  canlı süre çubuğu (~N sn / en fazla 20 sn, aşınca kırmızı). Tahmini 22 sn'yi (%10 pay) aşan metinle Tasarla başlamaz,
  sunucu da `tasarim_uzun` hatasıyla reddeder; *Okuma sekmesine taşı* düğmesi tam metni cümle cümle okuma kutusuna koyar,
  tasarımda ilk 1-2 cümle kalır. Hız: hazır seslerin kaydından ölçülen karakter/saniye (tr, en, de, fr, es, ru, ja, zh),
  ölçülmeyen dillerde varsayılan. 30 dilde metin; `POST /api/sure`. Test: `tests/test_tasarim_suresi.py`.
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

**EN**
- Design a voice: the design text box is now *Sample sentence (to get to know the voice, 1-2 sentences)*; 3 lines high,
  with a live per-language length bar below it (~N s / max 20 s, red when over). With an estimate above 22 s (10 %
  margin) Design does not start and the server rejects it with `tasarim_uzun`; *Move to reading tab* puts the full text
  into the reading box one sentence per line and keeps the first 1-2 sentences in the design box. Rates are characters
  per second measured on the bundled voices (tr, en, de, fr, es, ru, ja, zh), a default elsewhere. Strings in all 30
  languages; `POST /api/sure`. Test: `tests/test_tasarim_suresi.py`.
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

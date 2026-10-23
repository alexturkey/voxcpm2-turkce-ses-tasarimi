# voxcpm2-turkce-ses-tasarimi

**4 GB ekran kartında VoxCPM2 ile Türkçe ses tasarımı.** Sesi İngilizce tarif edin, model yaratsın, beğendiğiniz çeşidi
seçin, sonra o sesle istediğiniz Türkçe metni okutun. Tek komutluk kurulum, GTX 1050 Ti'ye (4 GB) sığdırılmış yamalı
[audio.cpp](https://github.com/0xShug0/audio.cpp) motoru, küçük bir yerel web arayüzü ve yedi hazır yapay ses içerir.

[English README](README.md) · [4 GB'a nasıl sığdı](docs/4gb.md) · [Yapay zekâ ajanı için kurulum](AGENTS.md) · [Sorumlu kullanım](ETHICS.md)

> Buradaki her ses yapaydır: bir metin tarifinden tasarlanmıştır, hiçbir gerçek kişiden kaydedilmemiş ya da
> klonlanmamıştır. Ürettiğiniz sesi yapay zekâ ürünü olarak etiketleyin. Dışarıdan ses yükleme ve gerçek kişi klonlama yoktur.

## Hızlı başlangıç (Windows, 3 adım)

1. **İndir:** kodu indirin: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Kartınıza uygun hazır motor paketini 3. adımdaki kurulum kendisi indirir:
   NVIDIA → [CUDA paketi](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan paketi, deneysel](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (paketi elle indirdiyseniz aşağıdaki komutun sonuna `-HazirZip <zip'in yolu>` ekleyin).
2. **Aç:** zip'i açın, `voxcpm2-turkce-ses-tasarimi-main` klasörüne girin, Gezgin'in adres çubuğuna `powershell` yazıp
   Enter'a basın.
3. **Çalıştır:** kurulumu başlatın (64-bit Python 3.10–3.13 gerekir; CUDA için NVIDIA sürücüsü ≥ 570), sonra
   **`baslat.bat`**'a çift tıklayın:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: sonuna `-Vulkan` ekleyin. Arayüz http://127.0.0.1:8765/ adresinde açılır.

Motor zip'i tek başına çalışan bir uygulama değildir (içindeki exe, kurulumun yerleştirdiği modele ve DLL'lere ihtiyaç
duyar). Ayrıntı, kart listesi ve sık sorunlar: aşağıdaki "Hızlı kurulum".

## Nasıl çalışır

1. **Ses tasarımı.** İngilizce *ses tarifi* + ses yaratılırken okutulan Türkçe *metin* + çeşit sayısı. Her çeşidin kendi
   tohumu vardır; motora `(tarif)metin` gider, her tohum için 20-35 sn'lik bir tasarım kaydı döner.
2. **Referanslı okuma.** Tasarım kaydı motorun **iki** girişine birden verilir (`audio` ve `voice_ref`), yanında o
   kaydın metni (`reference_text`), okunacak yeni metin ve aynı tohum. Sesi tarif değil kayıt taşır; metinden metne
   kaymaz. Metin cümle cümle okunur.
3. Kalite sabittir: 16 adım, CFG 2.0. Tohum kalite ayarı değildir.

Motor: audio.cpp v0.7.2 + bizim yama (`patches/`); model: VoxCPM2 Q8_0 GGUF. VRAM tepe ≈ 2,8 GB; GTX 1050 Ti'de 1 sn ses
için ≈ 2 sn. Ayrıntı ve ölçümler: [docs/4gb.md](docs/4gb.md).

## Hazır sesler (`hazir_sesler/`)

Yedisi de `ses.json` içindeki tariflerden tasarlandı; hiçbiri gerçek bir kişi değil.

| Ses | Kısa tarif | Dinle |
|---|---|---|
| `belgesel_hanim` | Ellili yaşlarda, derin sıcak alto; sakin belgesel anlatıcısı | [örnek](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referans](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Tok, güçlü, gizemli erkek anlatıcı | [örnek](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referans](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Yetmişlerinde deneyimli haber spikeri, sakin ve otoriter | [örnek](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referans](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Otuzlarında karizmatik akşam haberleri sunucusu, kadifemsi ve vurgulu | [örnek](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referans](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Masal cadısı: pes, hafif genizli, sinsi tatlı | [örnek](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referans](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Çok derin, tok, buyurgan erkek anlatıcı | [örnek](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referans](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Yaşlı bilge, derin ve gür, hafif gizemli | [örnek](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referans](hazir_sesler/yasli_bilge/referans.flac) |

Her klasörde: `referans.flac` (kayıpsız tasarım kaydı), `ses.json` (tarif, metin, tasarım tohumu, okuma tohumu,
tanıtım), `ornek_okuma.mp3` (+ metni). Doğrudan kullanın: `--ses hazir/<ad>`.

## Hızlı kurulum, derleyici gerekmez (Windows 10/11, NVIDIA ekran kartı ≥ 4 GB)

Ön koşullar: NVIDIA sürücüsü ≥ 570 ve 64-bit Python 3.10–3.13 (`winget install Python.Python.3.12`). Başka bir şey
yok: Visual Studio da CUDA kurulumu da gerekmez. Hangi kartınız olduğundan emin değil misiniz? PowerShell'de
`nvidia-smi` yazın: kartın adını, sürücü sürümünü ve belleğini gösterir. NVIDIA kartınız yoksa aşağıdaki "AMD / Intel"
bölümüne bakın.

[Git](https://git-scm.com/download/win) ile:

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Git olmadan: bu sayfada **Code → Download ZIP**'e tıklayın, zip'i açın, çıkan `voxcpm2-turkce-ses-tasarimi-main`
klasörüne girin, Gezgin'in adres çubuğuna `powershell` yazıp Enter'a basın ve yukarıdaki son satırı çalıştırın. Git
yalnız kaynaktan derleme yolunda gerekir.

`-ExecutionPolicy Bypass` yalnız bu süreç için geçerlidir, sistem ayarı değiştirmez; her kurulum betiğinde olduğu gibi
`scripts\kur.ps1`'i çalıştırmadan önce okuyun. Tek komut, ~10 dk, ~3,7 GB indirme, hepsi sha256 doğrulamalı: model (2,95 GB), CUDA 12.8 çalışma DLL'leri taşınabilir zip
olarak (sistem kurulumu yok, PATH değişmez), Releases sayfasındaki **hazır derlenmiş motor**, iki Python paketiyle `.venv`,
`ayarlar.json` ve sonda ekran kartı kontrolü (`KONTROL_OK`). Bir hata olursa aynı komutu yeniden çalıştırın; doğrulanmış
dosyalar atlanır. Sonra web arayüzünü başlatın: repo klasöründeki **`baslat.bat`** dosyasına çift tıklayın. Arayüzü
başlatır, hazır olunca tarayıcıda **http://127.0.0.1:8765/** adresini açar; kapatmak için siyah pencereyi kapatın (ya da
orada Ctrl+C). Aynısı PowerShell'den:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
sonra tarayıcıda **http://127.0.0.1:8765/** adresini siz açın (bu yolla arayüz tarayıcıyı kendisi açmaz; yalnız bu
bilgisayardan erişilir).

> **Sürüm zip'indeki `audiocpp_cli.exe` çift tıklanmaz.** Komut satırı motorudur; yanında CUDA DLL'leri ve model ister,
> hepsini `kur.ps1` yerine koyar ve Python paketi sürer. Çift tıklayınca yalnız "cudart64_12.dll bulunamadı" görürsünüz.

**Desteklenen kartlar (sürüm v0.1.1):** GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx (sm_89) ve
RTX 50xx (sm_120a) için yerel kod; Pascal ve sonrası başka CUDA kartlar gömülü PTX ile sürücü üzerinden çalışır (ilk açılış
yavaş). Maxwell (GTX 9xx) ve eskisi CUDA 12.8'de desteklenmez. Yalnız GTX 1050 Ti 4 GB'de denendi; başka kart deneyimlerinizi
[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)'a yazın.

**AMD / Intel (deneysel):** ayrı bir Vulkan motor zip'i (`…-win64-vulkan.zip`, CUDA gerekmez)
`scripts\kur.ps1 -Kok C:\vox -Vulkan` ile kurulur. Yalnız bizim NVIDIA kartta Vulkan arka ucuyla denendi (orada CUDA'dan
yavaş çalıştı ama aynı tohum aynı sesi verdi; o ölçüm sırasında disk başka bir işle doluydu, temiz hız karşılaştırması
bekliyor); AMD ya da Intel donanımında **denenmedi**: denerseniz sonucu Discussions'a
yazın. Birden çok Vulkan cihazı varsa (dahili + harici) kurulum harici kartın dizinini `ayarlar.json` içine `cihaz`
olarak yazar.

### Seçenek: motoru kaynaktan derlemek

Visual Studio 2022 Build Tools "Desktop development with C++" (C++ CMake tools dahil, ~7 GB) gerekir. Sonra:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Bu yol nvcc'yi de indirir, audio.cpp v0.7.2 kaynağını alır, `patches/0001-voxcpm2-4gb-ve-hiz.patch` yamasını uygular ve
kartınız için derler (`-Mimari native`, varsayılan; ya da ör. `-Mimari 61`), ~15-25 dk. Kökü kısa tutun (`C:\vox`): nvcc
uzun yolda düşer. Adım adım, kontrollü anlatım: [AGENTS.md](AGENTS.md).

### Sık kurulum sorunları

| Gördüğünüz | Anlamı, ne yapmalı |
|---|---|
| exe'ye çift tıklayınca `cudart64_12.dll bulunamadı` | Motor elle açılmak için değil. Yukarıdaki `kur.ps1` komutunu çalıştırın, sonra web arayüzünü başlatın. |
| `64-bit Python 3.10+ bulunamadı` | Python kurun (`winget install Python.Python.3.12`), PowerShell'i kapatıp yenisini açın, aynı komutu yeniden çalıştırın. |
| `motor ekran kartını görmedi` | NVIDIA sürücüsünü 570 ya da üstüne güncelleyin; `nvidia-smi` çalışıyor mu bakın. |
| `indirme başarısız` / `sha256 tutmadı` | Çoğunlukla yarıda kalan indirme. Aynı komutu yeniden çalıştırın; doğrulanmış dosyalar atlanır. |
| Derleme yolunda `nvcc` düşüyor | Kurulum kökünü kısa tutun (`-Kok C:\vox`). |
| Sayfa açılmıyor | Arayüzü `baslat.bat` ile başlatın ya da http://127.0.0.1:8765/ adresini siz açın. Port doluysa `ayarlar.json` içindeki `"port"` değerini değiştirin. |

Sorun mu var? [Discussions (Soru-Cevap)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) ya da
[kurulum sorunu kaydı](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml):
ekran kartı, Windows sürümü, komut ve son satırlarıyla.

## Kullanım

Komut satırı:
```powershell
# sesleri listele
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# hazır sesle oku (satır = cümle; "|| paragraf" uzun durak)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# yeni ses tasarla: 3 çeşit, 3 tohum
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# 2. çeşidiyle oku
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
```
Metin kuralları: rakamı yazıyla yazın, tırnak kullanmayın (araç rakam ve tırnağı reddeder), satır başına bir cümle,
satır ≤ 2000 karakter. Yabancı kelimelerin okunuşu: `ayarlar/okunus_sozlugu.tsv`.

Web arayüzü (yalnız 127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → tarayıcıda http://127.0.0.1:8765/
adresini kendiniz açın (başka port: `--port 8800`). Üç kutu (tarif, yaratılırken okunan metin, okunacak metin) + çeşit
sayısı. *Tasarla* → çeşitleri dinle → birini seç → *Bu sesle oku* → indir. Ya da hazır sesi seçip oku. Sunucuyu Ctrl+C
ile kapatın.

## Sık sorulanlar

**Model mi, motor mu? Hangisi ne?** VoxCPM2 (OpenBMB) *model*dir: metni konuşmaya çeviren 2 milyar parametreli ağ.
audio.cpp *motor*dur: modeli ekran kartında çalıştıran C++/CUDA programı (`audiocpp_cli.exe`). Bizim yama modeli değil
motoru değiştirir: VoxCPM2'yi 4 GB'a sığdırır ve aynı tohumun her seferinde aynı sesi vermesini sağlar. Bu depodaki
Python paketi yalnız metni hazırlar, motoru çağırır ve dosyaları toplar.

**Hangi kartlar?** Yukarıdaki "Desteklenen kartlar": GTX 10xx ve üstü NVIDIA, en az 4 GB VRAM, sürücü ≥ 570. Sürümde
sm_61/75/86/89/120a için yerel kod var; Pascal ve sonrası diğer kartlar gömülü PTX ile çalışır (ilk açılış yavaş).
AMD/Intel: deneysel Vulkan zip'i, `kur.ps1 -Vulkan`, AMD/Intel'de denenmedi (yukarıdaki "AMD / Intel"). Yalnız CPU (`ayarlar.json` içinde `"backend": "cpu"`) çalışır ama
GTX 1050 Ti'den ~6 kat yavaştır (motor ölçümü: 48 sn ses için 535 sn / 94 sn); desteklenen yol değildir.

**Ne kadar hızlı?** GTX 1050 Ti 4 GB (i7-7700HQ) üzerinde ölçüldü: bir tasarım çeşidi (≈ 25 sn kayıt) 55 sn; okuma,
ses başına 1 sn için ≈ 2 sn hesap (gerçek zaman çarpanı 1,9-2,8); ses başına bir kerelik ~50 sn referans kodlaması
(diske önbelleklenir) ve parti başına 10-20 sn model yükleme eklenir; VRAM tepe 2,6-2,9 GB. Yeni kartlar daha hızlı;
sayılar ve yöntem: [docs/4gb.md](docs/4gb.md).

**Gerçek kişiyi klonlar mı?** Hayır. Ses yükleme ve kayıt yolu yoktur: her ses İngilizce bir metin tarifinden başlar,
okumada kullanılan "referans" modelin kendi yapay tasarım kaydıdır. Bkz. [ETHICS.md](ETHICS.md). Yayınladığınızı yapay
zekâ ürünü olarak etiketleyin.

**İyi bir ses tarifi nasıl yazılır?** İngilizce, 1-3 cümle: yaş ve cinsiyet, tını (derin/parlak, sıcak, genizden,
kısık), ton ve rol (sakin belgesel anlatıcısı, enerjik sunucu), tempo (yavaş, ölçülü) ve "clean studio recording, no
background noise". Tarif olsun, senaryo olmasın; parantez kullanmayın. 3-5 çeşit isteyip dinleyin: tohum sesi çok
değiştirir. Yaratılırken okunan metin için istediğiniz havada 3-5 doğal Türkçe cümle (≈ 20-30 sn konuşma). Okumada
satır başına bir cümle; uzun cümleyi bölün, rakamı yazıyla yazın.

## Katkı

Nereden başlayacağını bilmiyorsan bu dört küçük iş iyi bir ilk adım:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Kendi kartında dene; kartı, sürücüyü ve süreleri yaz
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: deneysel Vulkan sürümünü dene
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Test setine bir cümle ekle
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Tasarladığın bir sesi tarifi ve tohumuyla paylaş

Ortak test seti: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); marka sesi rehberi:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); kod gönderme: [CONTRIBUTING.md](CONTRIBUTING.md).
Kurulum sorunu: [sorun formu](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); soru ve sonuçlar: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Katılan herkes [Davranış Kuralları](CODE_OF_CONDUCT.md)'na uyar: nazik olun, geri bildirimi işe yöneltin.

## Katkıda bulunanlar

- [@alexturkey](https://github.com/alexturkey): bakıcı; kod, hazır sesler, belgeler

Adınız da burada yer alabilir: kendi kartınızdaki test sonucu, test setine bir cümle, tasarladığınız bir ses, açık bir
hata bildirimi ya da bir PR, hepsi katkıdır. Deneyip geri yazan herkese teşekkürler.

## Lisans ve teşekkür

Kod ve hazır sesler: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. VoxCPM2 (OpenBMB, Apache-2.0), audio.cpp (ShugoAI LLC,
Apache-2.0) ve audio.cpp GGUF dönüşümü üzerine kuruludur. Tam liste: [THIRD_PARTY.md](THIRD_PARTY.md).
OpenBMB, ModelBest ya da audio.cpp projesiyle bağlantısı yoktur.

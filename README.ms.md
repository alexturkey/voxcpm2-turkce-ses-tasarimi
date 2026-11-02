[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · **Bahasa Melayu** · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Reka bentuk suara bahasa Turki dengan VoxCPM2 pada GPU 4 GB.** Huraikan suara dalam bahasa Inggeris, biarkan model
menciptanya, pilih varian yang anda suka, kemudian baca apa-apa teks bahasa Turki dengan suara itu. Disertakan pemasang
satu arahan, enjin [audio.cpp](https://github.com/0xShug0/audio.cpp) yang telah ditampal supaya muat dalam GTX 1050 Ti
(4 GB), antara muka web setempat yang kecil dan empat belas suara sintetik sedia ada: tujuh suara Turki dan tujuh
pencerita penutur asli bahasa Inggeris, Perancis, Jerman, Sepanyol, Rusia, Cina dan Jepun.

- Aplikasi ini boleh membaca dalam 30 bahasa; antara mukanya juga tersedia dalam 30 bahasa.
- 14 suara sedia ada: 7 suara Turki, serta satu suara setiap satu untuk bahasa Inggeris, Perancis, Jerman, Sepanyol, Rusia, Cina dan Jepun.
- Antara muka web (v0.2.0): setiap kad varian mempunyai dua suara, iaitu suara reka bentuk mentah dan suara yang akan
  anda dengar sentiasa; senarai bacaan dengan menu suara; namakan semula, sembunyikan atau padam suara; draf untuk teks
  yang anda baca. Lihat "Antara muka web" di bawah "Penggunaan".

[Cara ia muat dalam 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Panduan pemasangan untuk ejen AI](AGENTS.md) · [Penggunaan yang bertanggungjawab](ETHICS.md)

> Suara terbina dalam ialah suara sintetik, direka bentuk daripada huraian teks. Bahagian pengklonan suara hanya untuk
> suara anda sendiri atau suara yang digunakan dengan kebenaran jelas daripada pemiliknya; antara muka akan meminta anda
> mengesahkan kebenaran itu. Penyamaran, penipuan dan perbuatan mengelirukan adalah dilarang. Labelkan hasil yang anda
> jana sebagai dijana AI. Lihat [ETHICS.md](ETHICS.md).

## 30 bahasa

Kami menghasilkan satu video dokumentari tentang Cappadocia dalam 8 bahasa: Turki, Inggeris, Perancis, Jerman,
Sepanyol, Rusia, Cina dan Jepun. Setiap bahasa mempunyai **pencerita penutur asli** tersendiri, direka bentuk dengan
VoxCPM2 daripada huraian dalam bahasa Inggeris. Kesemuanya dijana sepenuhnya secara setempat pada GTX 1050 Ti 4 GB,
dengan kualiti tetap yang sama (16 langkah, cfg 2.0). Ketujuh-tujuh pencerita disertakan di sini, bersama prompt, teks
reka bentuk, seed dan rakaman rujukan masing-masing.

| Kod | Bahasa | Suara | Dengar | Video |
|---|---|---|---|---|
| `tr` | Turki | `hazir/belgesel_hanim` (dan 6 lagi) | [sampel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Inggeris | `hazir/anlatici_en` | [sampel](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Perancis | `hazir/anlatici_fr` | [sampel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Jerman | `hazir/anlatici_de` | [sampel](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Sepanyol | `hazir/anlatici_es` | [sampel](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Rusia | `hazir/anlatici_ru` | [sampel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Cina (Mandarin) | `hazir/anlatici_zh` | [sampel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Jepun | `hazir/anlatici_ja` | [sampel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Mengapa ayat demi ayat.** VoxCPM2 tidak stabil untuk satu penjanaan yang panjang (lebih kurang melebihi 30 saat):
rentaknya semakin laju dan suaranya boleh tersasar. Di sini suara dibawa oleh rakaman rujukan dan seed yang tetap, dan
teks panjang dibaca satu ayat bagi setiap baris, jadi warna suara dan gayanya kekal sama dari ayat pertama hingga ayat
terakhir. Bagi bahasa selain bahasa Turki, kamus sebutan bahasa Turki tidak digunakan. Kesemua 30 bahasa yang disokong
VoxCPM2 telah diuji dan berfungsi; gunakan `--dil <code>` bagi bahasa yang belum mempunyai suara terbina dalam. Arahan
mengikut bahasa dan pengajaran yang kami peroleh: [docs/cok_dilli.md](docs/cok_dilli.md). Kemahiran (skill) Claude Code
untuk keseluruhan aliran reka bentuk: [.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 contoh prompt sebagai titik permulaan.** 18 peranan (pencerita dokumentari, pembaca berita, suara iklan, buku
audio, nenek pencerita, hos podcast, guru, treler filem, pemandu meditasi, pengulas sukan dan banyak lagi, lelaki dan
perempuan) dalam setiap satu daripada 8 bahasa. Prompt ditulis dalam bahasa Inggeris dengan kewarganegaraan dan loghat
asli penutur; disertakan bersamanya teks yang dibaca semasa suara dicipta, dalam bahasa itu dan sepadan dengan
peranannya. Pilih satu, dengar varian-variannya, simpan yang anda suka:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, atau pilih *Contoh huraian* dalam antara muka
web. Senarai penuh: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Alih suara video anda dengan suara anda sendiri.** [DubWorld](https://github.com/alexturkey/dubworld) ialah program
alih suara video setempat kami; ia memasang repositori ini sebagai enjin suara VoxCPM2-nya. Suara yang anda reka bentuk
di sini digunakan di sana dengan `ses.voxcpm2_ses = "<name>/<variant>"`.

## Mula pantas (Windows, 3 langkah)

1. **Muat turun** kodnya: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Pakej enjin sedia guna untuk kad grafik anda akan diambil oleh pemasang pada langkah 3:
   NVIDIA → [pakej CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [pakej Vulkan, eksperimen](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (sudah memuat turun salah satu? tambah `-HazirZip <path to the zip>` pada arahan di bawah).
2. **Ekstrak** fail zip, buka folder `voxcpm2-turkce-ses-tasarimi-main`, taip `powershell` dalam bar alamat Explorer
   dan tekan Enter.
3. **Jalankan** pemasang (memerlukan Python 3.10-3.13 64-bit; pemacu NVIDIA ≥ 570 untuk CUDA), kemudian klik dua kali **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: tambah `-Vulkan` di hujungnya. Antara muka dibuka di http://127.0.0.1:8765/.

Zip enjin bukan aplikasi kendiri (fail exe-nya memerlukan model dan DLL yang disediakan oleh pemasang). Butiran,
senarai GPU dan masalah biasa: lihat "Pemasangan pantas" di bawah.

## Ubuntu / Linux (NVIDIA CUDA, eksperimen)

Bina enjin yang telah ditampal dengan `bash scripts/kur-linux.sh`, atau gunakan `Dockerfile.linux` untuk membina dan
menjalankannya dalam persekitaran Ubuntu 24.04 / CUDA 12.8.1. Memerlukan GPU NVIDIA dan pemacu yang serasi; pemasang
natif juga memerlukan CUDA toolkit dan Python 3.10-3.13. Antara muka kekal pada loopback sahaja, termasuk pada pelayan
jauh (pemajuan SSH). Prasyarat, arahan, pemilihan seni bina dan skop pengesahan: [docs/linux.md](docs/linux.md).

## Mula pantas (macOS, Apple Silicon)

Memerlukan Xcode Command Line Tools (`xcode-select --install`) dan [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Pemasang memuat turun model, membina enjin yang telah ditampal dengan Metal (~1 minit) dan menyediakan segala-galanya
di bawah `~/vox`. Kemudian klik dua kali **`baslat.command`**. Pada MacBook Air M4 16 GB: ~2 saat pengiraan bagi
setiap 1 saat pertuturan, seed yang sama memberikan audio yang serupa hingga ke setiap bait, RAM puncak ~5.3 GB, tiada
perlahan akibat haba sepanjang 12 minit bacaan berterusan. Butiran dan ukuran: [docs/mac.md](docs/mac.md).

**Aplikasi Mac natif (tanpa Python, Homebrew atau Terminal):** [macos/README.md](macos/README.md). Ia membawa enjin
bertampal yang sama dan memuat turun model semasa dibuka kali pertama; buat masa ini ia dibina daripada kod sumber
dengan Xcode.

## Untuk pengguna Mac (Apple Silicon)

Terdapat juga adaptasi bebas buatan komuniti untuk Mac Apple Silicon yang menjalankan VoxCPM2 dengan rangka kerja MLX
milik Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Ia dibangunkan dan diselenggara oleh Emre Koç ([@emre-koc](https://github.com/emre-koc)) dalam repositorinya sendiri,
bukan di sini; langkah pemasangan dan soalan sokongan hendaklah diajukan di sana. Terima kasih, Emre, kerana membawa
projek ini ke Mac!

## Cara ia berfungsi

1. **Reka bentuk suara.** Satu *huraian suara* dalam bahasa Inggeris + satu *teks yang dibaca semasa suara dicipta*
   (dalam bahasa suara itu) + bilangan varian. Setiap varian mendapat seed tersendiri; enjin menerima
   `(description)text` dan memulangkan satu rakaman reka bentuk bagi setiap seed. Teks itu ialah sampel pendek untuk
   mengenali suara: 1-2 ayat, paling lama ~20 saat (antara muka memaparkan anggarannya dan tidak akan bermula jika
   melebihi 22 saat); teks panjang ialah urusan langkah 2.
2. **Bacaan berasaskan rujukan.** Rakaman reka bentuk dihantar kepada **kedua-dua** input enjin (`audio` dan
   `voice_ref`), bersama transkripnya (`reference_text`) dan teks baharu yang hendak dibaca, dengan seed yang sama.
   Suara dibawa oleh rakaman, bukan oleh huraian, jadi ia tidak tersasar dari satu teks ke teks yang lain. Teks dibaca
   ayat demi ayat.
3. Kualiti adalah tetap: 16 langkah resapan (diffusion), CFG 2.0. Seed bukan tombol kualiti.

Rakaman reka bentuk mentah ialah sampel suara sekali sahaja; tiada bacaan selepasnya yang berbunyi betul-betul sama
dengannya. Apa yang anda dengar dalam setiap bacaan selepas itu ialah langkah 2: rakaman reka bentuk sebagai rujukan
ditambah seed varian itu sendiri. Itulah sebabnya antara muka web menjalankan langkah 2 sejurus selepas reka bentuk
dan memaparkan kedua-duanya pada kad varian.

Enjinnya ialah audio.cpp v0.7.2 dengan tampalan kami (`patches/`), modelnya ialah VoxCPM2 Q8_0 GGUF. VRAM puncak ≈
2.8 GB; kira-kira 2 saat pengiraan bagi setiap 1 saat pertuturan pada GTX 1050 Ti. Butiran dan ukuran:
[docs/4gb.md](docs/4gb.md).

## Suara terbina dalam (`hazir_sesler/`)

Kesemua empat belas suara direka bentuk daripada prompt yang disimpan dalam `ses.json` masing-masing; tiada satu pun
yang diklon daripada rakaman (pengklonan ialah tab *Pengklonan suara* yang berasingan dan memerlukan kebenaran).

| Suara | Huraian ringkas | Dengar |
|---|---|---|
| `belgesel_hanim` | Wanita matang berusia lima puluhan, alto yang dalam dan hangat; pencerita dokumentari yang tenang | [sampel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [rujukan](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Pencerita lelaki yang dalam, bertenaga dan misteri | [sampel](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [rujukan](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Pembaca berita berpengalaman berusia sekitar tujuh puluh, tenang dan berwibawa | [sampel](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [rujukan](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Pembaca berita malam berkarisma berusia tiga puluhan, lembut seperti baldu dan ekspresif | [sampel](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [rujukan](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Ahli sihir cerita dongeng: rendah, sedikit sengau, manis tetapi licik | [sampel](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [rujukan](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Pencerita lelaki yang luar biasa dalam, padat dan berwibawa | [sampel](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [rujukan](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Lelaki tua yang bijaksana, dalam dan bergema, sedikit misteri | [sampel](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [rujukan](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Pencerita dokumentari lelaki penutur asli bahasa Inggeris berusia lima puluhan (General American); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Pencerita dokumentari lelaki penutur asli bahasa Perancis berusia lima puluhan (Paris); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Pencerita dokumentari lelaki penutur asli bahasa Jerman berusia lima puluhan (Hochdeutsch); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Pencerita dokumentari lelaki penutur asli bahasa Sepanyol berusia lima puluhan (Castilia (Madrid)); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Pencerita dokumentari lelaki penutur asli bahasa Rusia berusia lima puluhan (Moscow); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Pencerita dokumentari lelaki penutur asli bahasa Cina (Mandarin) berusia lima puluhan (Putonghua Beijing); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Pencerita dokumentari lelaki penutur asli bahasa Jepun berusia lima puluhan (standard Tokyo); dalam, tenang, hangat | [sampel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [rujukan](hazir_sesler/anlatici_ja/referans.flac) |

Setiap folder mengandungi: `referans.flac` (rakaman reka bentuk tanpa kehilangan kualiti), `ses.json` (prompt,
transkrip, seed reka bentuk, seed bacaan, huraian; `dil` = bahasa bagi para pencerita), `ornek_okuma.mp3` (+ teksnya).
Gunakan secara terus: `--ses hazir/<name>`. Rakaman rujukan para pencerita adalah pendek (5.6-10 saat); sampel mereka
ialah tiga ayat pertama skrip Cappadocia, dipotong daripada bacaan produksi penuh.

## Pemasangan pantas, tanpa pengkompil (Windows 10/11, GPU NVIDIA ≥ 4 GB)

Prasyarat: pemacu NVIDIA ≥ 570 dan Python 3.10-3.13 64-bit (`winget install Python.Python.3.12`). Tiada yang lain:
tiada Visual Studio, tiada pemasang CUDA. Tidak pasti kad grafik yang anda ada? Jalankan `nvidia-smi` dalam
PowerShell: ia memaparkan nama GPU, versi pemacu dan memori. Tiada kad NVIDIA? Lihat "AMD / Intel" di bawah.

Dengan [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Tanpa Git: pada halaman ini klik **Code → Download ZIP**, ekstrak, buka folder `voxcpm2-turkce-ses-tasarimi-main`
yang telah diekstrak, taip `powershell` dalam bar alamat Explorer dan tekan Enter, kemudian jalankan baris terakhir di
atas. Git hanya diperlukan untuk laluan membina daripada kod sumber.

`-ExecutionPolicy Bypass` hanya terpakai untuk proses ini sahaja dan tidak mengubah sebarang tetapan sistem; baca
`scripts\kur.ps1` sebelum menjalankannya, sama seperti mana-mana skrip pemasang. Satu arahan, ~10 minit, muat turun
~3.7 GB, semuanya disahkan dengan sha256: model (2.95 GB), DLL masa jalan CUDA 12.8 sebagai zip mudah alih (tiada
pemasangan sistem, PATH tidak disentuh), **enjin siap bina** daripada halaman Releases, sebuah `.venv` dengan dua pakej
Python, `ayarlar.json`, dan semakan GPU terakhir (`KONTROL_OK`). Jalankan semula selepas sebarang kegagalan; fail yang
telah disahkan akan dilangkau. Kemudian mulakan antara muka web: klik dua kali **`baslat.bat`** dalam folder
repositori. Ia memulakan antara muka dan membuka **http://127.0.0.1:8765/** dalam pelayar apabila sudah sedia; tutup
tetingkap hitam (atau tekan Ctrl+C di situ) untuk menghentikannya. Perkara yang sama daripada PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
kemudian buka sendiri **http://127.0.0.1:8765/** (jika dimulakan dengan cara ini, antara muka tidak membuka pelayar;
ia hanya mendengar pada localhost).

> **`audiocpp_cli.exe` dalam zip keluaran bukan untuk diklik dua kali.** Ia ialah enjin baris arahan yang memerlukan
> DLL CUDA dan model di sebelahnya; `kur.ps1` meletakkan semuanya di tempat yang betul dan pakej Python yang
> mengendalikannya. Mengklik dua kali hanya memaparkan "cudart64_12.dll not found".

**GPU yang disokong (keluaran v0.1.1):** kod natif untuk GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX
40xx (sm_89) dan RTX 50xx (sm_120a); mana-mana GPU CUDA lain dari Pascal ke atas menjalankan PTX terbenam melalui
pemacu (permulaan pertama lebih perlahan). Maxwell (GTX 9xx) dan yang lebih lama tidak disokong oleh CUDA 12.8. Diuji oleh kami pada GTX 1050 Ti 4 GB (juga melalui Docker Desktop/WSL2 pada Windows, CLI sahaja); diukur oleh @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (butiran dalam [docs/linux.md](docs/linux.md)). Laporan daripada kad lain amat dialu-alukan di [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (eksperimen):** zip enjin Vulkan yang berasingan (`...-win64-vulkan.zip`, tanpa CUDA) dipasang dengan
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Ia hanya disahkan pada kad NVIDIA kami melalui backend Vulkan (di situ ia
berjalan lebih perlahan daripada CUDA tetapi memberikan audio yang sama untuk seed yang sama; ukuran itu diambil
semasa cakera sibuk dengan kerja lain, jadi perbandingan kelajuan yang bersih masih belum dibuat) dan kami **belum**
mengujinya sendiri pada perkakasan AMD atau Intel: jika anda mencubanya, sila kongsikan hasilnya di Discussions.
Apabila terdapat lebih daripada satu peranti Vulkan (bersepadu + diskret), pemasang menulis indeks GPU diskret sebagai
`cihaz` ke dalam `ayarlar.json`.

*Nota: Sokongan Vulkan masih di peringkat eksperimen. Ia telah berjaya dibina dan diuji pada GTX 1050 Ti. Seorang
pengguna luar (mitra_tr) juga melaporkan berjaya menjalankannya pada AMD 6900 XT. Ujian yang lebih meluas pada kad
AMD/Intel masih diperlukan.*

### Alternatif: bina enjin daripada kod sumber

Memerlukan Visual Studio 2022 Build Tools dengan "Desktop development with C++" (termasuk C++ CMake tools), ~7 GB. Kemudian:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Ini turut memuat turun nvcc, mengambil kod sumber audio.cpp v0.7.2, menggunakan `patches/0001-voxcpm2-4gb-ve-hiz.patch`
dan membina untuk GPU anda (`-Mimari native`, lalai; atau contohnya `-Mimari 61`), ~15-25 minit. Pastikan folder akar
pendek (`C:\vox`): nvcc gagal pada laluan yang panjang. Langkah demi langkah dengan semakan: [AGENTS.md](AGENTS.md).

### Masalah pemasangan biasa

| Anda nampak | Maksudnya, apa yang perlu dilakukan |
|---|---|
| `cudart64_12.dll not found` selepas klik dua kali pada exe | Enjin tidak bertujuan untuk dimulakan secara manual. Jalankan arahan `kur.ps1` di atas, kemudian mulakan antara muka web. |
| `64-bit Python 3.10+ bulunamadı` (Python tidak dijumpai) | Pasang Python (`winget install Python.Python.3.12`), tutup PowerShell, buka yang baharu dan jalankan arahan yang sama sekali lagi. |
| `motor ekran kartını görmedi` (enjin tidak mengesan GPU) | Kemas kini pemacu NVIDIA ke 570 atau lebih baharu; semak bahawa `nvidia-smi` boleh dijalankan. |
| `indirme başarısız` / `sha256 tutmadı` (muat turun gagal / checksum tidak sepadan) | Biasanya muat turun yang terganggu. Jalankan arahan yang sama sekali lagi; fail yang telah disahkan akan dilangkau. |
| Laluan bina: `nvcc` gagal | Pastikan akar pemasangan pendek (`-Kok C:\vox`). |
| Halaman tidak terbuka | Mulakan antara muka dengan `baslat.bat`, atau buka sendiri http://127.0.0.1:8765/. Port sedang digunakan? Tukar `"port"` dalam `ayarlar.json`. |

Ada masalah? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) atau buka
[isu pemasangan](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
dengan menyatakan GPU, versi Windows, arahan yang dijalankan dan baris-baris terakhir outputnya.

## Penggunaan

Baris arahan:
```powershell
# list voices
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# read with a bundled voice (one sentence per line; blank line or "|| paragraf" = longer pause, "|| 0,8" = 0.8 s)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# design a new voice: 3 variants, 3 seeds
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# read with variant 2 of it
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
# design, then read a text with each variant's lasting voice (dinleme.wav in each variant folder)
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt --dinleme @metin.txt
```
Peraturan teks: tulis nombor dalam perkataan, jangan gunakan tanda petik (alat ini menolak digit dan tanda petik), satu
ayat bagi setiap baris, ≤ 2000 aksara bagi setiap baris. Jeda selepas baris: `|| bagli` 0.25 saat, `|| normal` 0.5
saat, `|| paragraf` 1 saat, `|| agir` 1.5 saat atau panjang pilihan anda sendiri `|| 0,8` (0-5 saat; digit dalam
penanda ini dibenarkan). `ayarlar/okunus_sozlugu.tsv` membetulkan sebutan perkataan asing dalam teks bahasa Turki.
Bahasa dikesan daripada teks (huruf Turki, sistem tulisan, perkataan lazim; `dil` pada kad suara jika tidak pasti;
`--dil <code>` adalah pilihan). Bagi teks bukan bahasa Turki, apostrofi dibenarkan, kamus bahasa Turki dilangkau,
digit tetap ditolak. Jika sesuatu bacaan mencetak `speed gate: satır [...]`, dengar semula baris-baris tersebut.

### Antara muka web

Setempat sahaja (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → buka sendiri http://127.0.0.1:8765/
(port lain: `--port 8800`), atau klik dua kali `baslat.bat`. Hentikan pelayan dengan Ctrl+C. Tiga tab: *Reka bentuk
suara*, *Baca dengan suara ini*, *Pengklonan suara*. Aliran biasa: *Reka bentuk* → dengar varian-variannya → *Tambah ke
senarai bacaan saya* → *Baca dengan suara ini* → muat turun. Atau pilih suara terbina dalam daripada menu suara dan baca.

- **Versi pada pengepala.** Teks kecil dan pudar `v0.2.0 · <short commit>` (dengan `+` apabila fail yang dijejak
  mempunyai perubahan yang belum di-commit; versi sahaja tanpa git), supaya tangkapan skrin dan video menunjukkan versi
  yang digunakan.
- **Dua suara pada setiap kad varian.** Di atas, berwarna kelabu, ialah *Suara reka bentuk mentah*: ia dijana sekali
  dan tidak akan keluar sama lagi. Di bawahnya, dalam bingkai jingga, ialah *↻ Inilah suara yang akan anda dengar
  sentiasa*: rakaman reka bentuk yang dibaca semula sebagai rujukan dengan seed varian itu sendiri (dipaparkan pada
  kad). Beginilah bunyi suara itu dalam setiap bacaan selepas ini. Di bawahnya terdapat *Baca dengan suara ini* dan
  *Tambah ke senarai bacaan saya*. Satu tekanan *Reka bentuk* melakukan kedua-duanya: ia mereka bentuk setiap varian,
  kemudian membaca teks anda dengan setiap suara kekalnya; satu bar kemajuan mengira kedua-dua fasa. Folder varian
  mendapat `dinleme.wav`. Jika bacaan itu berhenti awal, reka bentuk tetap disimpan dan kad memaparkan nota.
- **Tetingkap "Teks yang anda mahu dengar".** Dalam *Reka bentuk suara*, kotak *↻ Teks yang anda mahu dengar* memuatkan
  apa yang dibaca oleh setiap suara kekal (jika dibiarkan kosong, ayat sampel yang dibaca). Klik padanya untuk membuka
  buku nota bacaan dalam tetingkap: nombor baris, menu baris, jalur jeda. *OK* menulis teks dan jedanya kembali ke
  kotak; *Batal* atau Esc tidak mengubah apa-apa. Tab bacaan menyimpan teksnya sendiri.
- **Buku nota bacaan.** Satu ayat bagi setiap baris. Klik nombor baris untuk membuka menu baris (alih ke atas atau ke
  bawah, alih ke kedudukan tertentu, pendua, padam; Alt+↑/↓, Alt+Shift+↓, atau seret melalui nombornya; Ctrl+Z membuat
  asal teks dan jeda serentak). Klik jalur nipis di antara dua baris untuk memilih jeda (bagli 0.25 · normal 0.5 ·
  paragraf 1 · agir 1.5 saat, atau panjang pilihan anda sendiri 0-5 saat dengan ikon gear); tekan Enter dua kali untuk
  perenggan (1 saat), dan baris kosong menjadi jalur jeda. Semasa hasil dimainkan, baris yang sedang dibaca menyala dan
  ditatal ke dalam paparan; *▶ Dengar dari sini* dalam menu baris memainkan dari baris itu. Teks dan jedanya kekal
  selepas halaman dimuat semula (storan pelayar).
- **Draf.** Butang *📄 Draf* terdapat dalam kedua-dua buku nota (tab bacaan dan tetingkap). Simpan teks semasa bersama
  jedanya sebagai draf, muatkan satu dengan sekali klik (Ctrl+Z membuat asal), dan gunakan ⋯ untuk menulis ganti,
  menamakan semula atau memadamnya. Draf disimpan dalam `sesler/taslaklar.json`, tidak sekali-kali dalam repositori.
- **Senarai bacaan dan menu suara.** Pada kad varian, *Tambah ke senarai bacaan saya* membuka kotak nama: beri varian
  itu nama sendiri dan ✓ menambahkannya. *Nama penjanaan* kekal pada setiap varian daripada larian itu. Dalam *Baca
  dengan suara ini*, butang suara (bendera + nama) membuka menu suara: *Senarai bacaan saya* di atas, kemudian suara
  terbina dalam dengan bendera (bahasa antara muka didahulukan). Setiap baris mempunyai ▶ dengar (suara kekal jika
  ada), ikon hati (tambah atau buang) dan ⋯; ↑/↓ dan Enter untuk memilih, Esc untuk menutup, suara terakhir diingati.
  Senarai ini disimpan dalam `sesler/okuma_listesi.json`, di luar repositori, dan kekal selepas dimulakan semula.
- **Mengurus suara.** Menu ⋯ (baris menu suara atau kad varian) mengandungi *Baca dengan suara ini*, tambah ke atau
  buang daripada senarai, *Namakan semula* (nama kosong memulihkan nama asal; *Kembali ke nama asal*), *Padam* untuk
  suara yang direka bentuk dan *Sembunyikan* untuk suara terbina dalam; kedua-duanya meminta pengesahan dahulu. Suara
  yang dipadam dipindahkan ke `sesler/_cop/`; menyembunyikan tidak sekali-kali menyentuh fail repositori. *Suara
  tersembunyi dan dipadam (N)* di bahagian bawah menu suara mempunyai *Pulihkan*. Nama tersuai dan suara tersembunyi
  disimpan dalam `sesler/yerel_katman.json`. Suara yang telah dinamakan semula memaparkan asal-usulnya dalam warna
  kelabu (*nama penjanaan · varian N*); ⋯ → *Pergi ke penjanaan* membuka reka bentuknya.
- **Pintasan dan fail.** Ctrl+Enter (⌘+Enter pada Mac) memulakan *Reka bentuk* atau *Baca dengan suara ini* pada tab
  yang terbuka. Bar kemajuan memaparkan *berlalu / ~jumlah*, dengan anggaran yang dipelajari daripada kerja terdahulu
  pada mesin anda. Fail muat turun dinamakan mengikut suara dan masa (`Voice_Name_2026-11-02_0152.wav`).

**Pengklonan suara (suara anda sendiri atau suara dengan kebenaran).** Dalam tab *Pengklonan suara* pada antara muka, berikan rakaman anda (wav/mp3/flac/ogg, disyorkan 5-30 saat pertuturan yang bersih; di bawah 3 saat ditolak, melebihi 36 saat dipotong), transkrip tepatnya dan teks yang hendak dibaca. Butang kekal tidak aktif sehingga anda menandakan "Suara ini milik saya atau saya mendapat kebenaran jelas daripada pemiliknya". Rakaman hanya dihantar ke pelayan setempat (127.0.0.1), diproses dalam folder sementara bersama pengekodan rujukannya, dan folder itu dipadam apabila kerja tamat, termasuk apabila ia gagal; tiada apa-apa yang dihantar melalui rangkaian. Hanya output sintetik yang disimpan (antara muka: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Outputnya ialah `klon_synthetic.wav` dengan tag "synthetic"; labelkannya sebagai dijana AI apabila berkongsi. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Soalan lazim

**Model atau enjin? Apa bezanya?** VoxCPM2 (OpenBMB) ialah *model*: rangkaian 2 bilion parameter yang menukar teks
kepada pertuturan. audio.cpp ialah *enjin*: program C++/CUDA yang menjalankan model pada GPU anda
(`audiocpp_cli.exe`). Tampalan kami mengubah enjin, bukan model: ia membolehkan VoxCPM2 muat dalam 4 GB dan memastikan
seed yang sama sentiasa memberikan audio yang sama. Pakej Python dalam repositori ini hanya menyediakan teks, memanggil
enjin dan mengumpul fail-failnya.

**GPU yang mana?** Lihat "GPU yang disokong" di atas: NVIDIA dari GTX 10xx ke atas, VRAM 4 GB atau lebih, pemacu ≥
570. Kod natif tersedia dalam keluaran untuk sm_61/75/86/89/120a; kad lain dari Pascal atau lebih baharu menggunakan
PTX terbenam (permulaan pertama lebih perlahan). AMD/Intel: zip Vulkan eksperimen, `kur.ps1 -Vulkan`; seorang pengguna
luar melaporkan berjaya menjalankannya pada AMD 6900 XT, tetapi ujian AMD/Intel yang lebih meluas masih diperlukan
(lihat "AMD / Intel" di atas). CPU sahaja (`"backend": "cpu"` dalam `ayarlar.json`) boleh berjalan tetapi ~6× lebih
perlahan daripada GTX 1050 Ti (ukuran enjin, 535 saat berbanding 94 saat untuk 48 saat pertuturan); bukan laluan yang
disokong.

**Sepantas mana?** Diukur pada GTX 1050 Ti 4 GB (i7-7700HQ): satu varian reka bentuk (rakaman ≈ 25 saat) 55 saat;
bacaan ≈ 2 saat pengiraan bagi setiap 1 saat pertuturan (faktor masa nyata 1.9-2.8) selepas pengekodan rujukan sekali
sahaja ~50 saat bagi setiap suara (dicache pada cakera) dan 10-20 saat memuatkan model bagi setiap kelompok; VRAM puncak
2.6-2.9 GB. Kad yang lebih baharu lebih pantas; angka dan kaedah: [docs/4gb.md](docs/4gb.md).

**Bolehkah ia mengklon suara?** Model VoxCPM2 yang menjadi asasnya boleh meniru suara daripada rakaman rujukan, dan
bahagian pengklonan menggunakan keupayaan itu. Gunakan hanya dengan suara anda sendiri atau dengan kebenaran jelas
daripada pemilik suara tersebut; antara muka akan meminta anda mengesahkan kebenaran itu. Reka bentuk suara tidak
memerlukan rakaman: ia bermula daripada huraian teks dalam bahasa Inggeris atau Cina, dan "rujukan" yang digunakan
untuk membaca suara yang direka bentuk ialah rakaman reka bentuk sintetik model itu sendiri. Penyamaran, penipuan dan
perbuatan mengelirukan adalah dilarang. Lihat [ETHICS.md](ETHICS.md). Labelkan apa yang anda terbitkan sebagai dijana AI.

**Bagaimana menulis huraian suara yang baik?** Dalam bahasa Inggeris, 1-3 ayat: umur dan jantina, warna suara
(dalam/cerah, hangat, sengau, serak), nada dan peranan (pencerita dokumentari yang tenang, penyampai yang bertenaga),
tempo (perlahan, teratur), dan "clean studio recording, no background noise". Pastikan ia kekal sebagai huraian, bukan
skrip; jangan gunakan tanda kurung. Minta 3-5 varian dan dengar: seed banyak mengubah suara. Untuk teks penciptaan,
gunakan 1-2 ayat semula jadi dalam bahasa suara itu, dengan suasana yang anda mahukan (paling lama ~20 saat
pertuturan). Semasa membaca, satu ayat bagi setiap baris; pecahkan ayat yang panjang, tulis nombor dalam perkataan.

## Menyumbang

Tidak pasti hendak bermula dari mana? Empat isu kecil ini ialah langkah pertama yang baik:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Cuba pada GPU anda dan laporkan kad, pemacu dan masa yang diambil
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: cuba binaan Vulkan eksperimen
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Tambah satu ayat ke dalam set ujian
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Kongsi suara yang anda reka bentuk, bersama huraian dan seed-nya

Set ujian bersama: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); panduan suara jenama:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); cara menghantar kod: [CONTRIBUTING.md](CONTRIBUTING.md).
Masalah pemasangan: [borang isu](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); soalan dan hasil: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Semua yang mengambil bahagian mematuhi [Tatakelakuan](CODE_OF_CONDUCT.md): bersikap baik, dan pastikan maklum balas
berkisar tentang kerja itu.

## Penyumbang

- [@alexturkey](https://github.com/alexturkey): penyelenggara; kod, suara terbina dalam, dokumentasi
- [@cayir21](https://github.com/cayir21): sokongan Metal untuk macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): pembetulan akhir ayat (EOS) untuk bacaan berbilang ayat pada backend CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)

Nama anda juga layak berada di sini: keputusan ujian daripada GPU anda, satu ayat untuk set ujian, suara yang anda reka
bentuk, laporan pepijat yang jelas atau pull request, semuanya dikira sebagai sumbangan. Terima kasih kepada semua yang
mencubanya dan memberi maklum balas.

## Lesen dan penghargaan

Kod dan suara terbina dalam: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Dibina di atas VoxCPM2 (OpenBMB,
Apache-2.0), audio.cpp (ShugoAI LLC, Apache-2.0) dan penukaran GGUF audio.cpp. Senarai penuh:
[THIRD_PARTY.md](THIRD_PARTY.md). Tidak bergabung dengan OpenBMB, ModelBest atau projek audio.cpp.

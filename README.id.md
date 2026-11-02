[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · **Bahasa Indonesia** · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Desain suara berbahasa Turki dengan VoxCPM2 di GPU 4 GB.** Deskripsikan sebuah suara dalam bahasa Inggris, biarkan
model membuatnya, pilih varian yang kamu suka, lalu bacakan teks berbahasa Turki apa pun dengan suara itu. Sudah
termasuk installer satu perintah, engine [audio.cpp](https://github.com/0xShug0/audio.cpp) yang sudah di-patch agar
muat di GTX 1050 Ti (4 GB), antarmuka web lokal yang ringkas, dan empat belas suara sintetis siap pakai: tujuh suara
Turki dan tujuh narator penutur asli bahasa Inggris, Prancis, Jerman, Spanyol, Rusia, Mandarin, dan Jepang.

- Aplikasi ini bisa membacakan 30 bahasa; antarmukanya juga tersedia dalam 30 bahasa.
- 14 suara siap pakai: 7 suara Turki, ditambah masing-masing satu untuk bahasa Inggris, Prancis, Jerman, Spanyol, Rusia, Mandarin, dan Jepang.
- Antarmuka web (v0.2.0): setiap kartu varian punya dua suara, yaitu suara desain mentah dan suara yang akan selalu
  kamu dengar; daftar baca dengan menu suara; ganti nama, sembunyikan, atau hapus suara; draf untuk teks yang kamu
  bacakan. Lihat "Antarmuka web" di bagian "Penggunaan".

[Cara muat di 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Panduan instalasi untuk agen AI](AGENTS.md) · [Penggunaan yang bertanggung jawab](ETHICS.md)

> Suara bawaan bersifat sintetis, didesain dari deskripsi teks. Bagian kloning suara hanya untuk suaramu sendiri atau
> suara yang digunakan dengan izin jelas dari pemiliknya; antarmuka akan memintamu mengonfirmasi izin tersebut.
> Peniruan identitas, penipuan, dan penyesatan dilarang. Beri label bahwa hasil yang kamu buat dihasilkan oleh AI.
> Lihat [ETHICS.md](ETHICS.md).

## 30 bahasa

Kami membuat satu video dokumenter tentang Cappadocia dalam 8 bahasa: Turki, Inggris, Prancis, Jerman, Spanyol, Rusia,
Mandarin, dan Jepang. Setiap bahasa punya **narator penutur asli** sendiri, didesain dengan VoxCPM2 dari deskripsi
berbahasa Inggris. Semuanya dihasilkan sepenuhnya secara lokal di GTX 1050 Ti 4 GB, dengan kualitas tetap yang sama
(16 langkah, cfg 2.0). Ketujuh narator itu disertakan di sini, lengkap dengan prompt, teks desain, seed, dan rekaman
referensinya.

| Kode | Bahasa | Suara | Dengarkan | Video |
|---|---|---|---|---|
| `tr` | Turki | `hazir/belgesel_hanim` (dan 6 lainnya) | [contoh](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Inggris | `hazir/anlatici_en` | [contoh](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Prancis | `hazir/anlatici_fr` | [contoh](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Jerman | `hazir/anlatici_de` | [contoh](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Spanyol | `hazir/anlatici_es` | [contoh](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Rusia | `hazir/anlatici_ru` | [contoh](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Tionghoa (Mandarin) | `hazir/anlatici_zh` | [contoh](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Jepang | `hazir/anlatici_ja` | [contoh](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Kenapa kalimat demi kalimat.** VoxCPM2 tidak stabil untuk satu kali pembuatan yang panjang (kira-kira di atas 30
detik): ritmenya makin cepat dan suaranya bisa bergeser. Di sini suara dijaga oleh rekaman referensi dan seed yang
tetap, dan teks panjang dibacakan satu kalimat per baris, sehingga warna suara dan gayanya tetap sama dari kalimat
pertama hingga terakhir. Untuk bahasa selain Turki, kamus pelafalan bahasa Turki tidak dipakai. Ke-30 bahasa yang
didukung VoxCPM2 sudah diuji dan berfungsi; gunakan `--dil <code>` untuk bahasa yang belum punya suara bawaan. Perintah
per bahasa dan pelajaran yang kami dapat: [docs/cok_dilli.md](docs/cok_dilli.md). Skill Claude Code untuk seluruh alur
desain: [.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 contoh prompt untuk memulai.** 18 peran (narator dokumenter, pembaca berita, suara iklan, buku audio, nenek
pendongeng, host podcast, guru, trailer film, pemandu meditasi, komentator olahraga, dan lainnya, laki-laki dan
perempuan) di masing-masing dari 8 bahasa. Prompt-nya berbahasa Inggris, menyebutkan kebangsaan dan aksen asli
pembicara; disertai teks yang dibacakan saat suara dibuat, dalam bahasa tersebut dan sesuai dengan perannya. Pilih
satu, dengarkan variannya, simpan yang kamu suka: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`,
atau pilih *Contoh deskripsi* di antarmuka web. Daftar lengkap: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Sulih suara videomu dengan suaramu sendiri.** [DubWorld](https://github.com/alexturkey/dubworld) adalah program
sulih suara video lokal kami; program ini memasang repositori ini sebagai engine suara VoxCPM2-nya. Suara yang kamu
desain di sini dipakai di sana dengan `ses.voxcpm2_ses = "<name>/<variant>"`.

## Mulai cepat (Windows, 3 langkah)

1. **Unduh** kodenya: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Paket engine siap pakai untuk kartu grafismu akan diambil oleh installer di langkah 3:
   NVIDIA → [paket CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [paket Vulkan, eksperimental](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (sudah mengunduh salah satunya? tambahkan `-HazirZip <path to the zip>` ke perintah di bawah).
2. **Ekstrak** berkas zip, buka folder `voxcpm2-turkce-ses-tasarimi-main`, ketik `powershell` di bilah alamat
   Explorer, lalu tekan Enter.
3. **Jalankan** installer (butuh Python 3.10-3.13 64-bit; driver NVIDIA ≥ 570 untuk CUDA), lalu klik dua kali **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: tambahkan `-Vulkan` di akhir. Antarmuka terbuka di http://127.0.0.1:8765/.

Zip engine bukan aplikasi mandiri (exe-nya membutuhkan model dan DLL yang disiapkan oleh installer). Detail, daftar
GPU, dan masalah umum: lihat "Instalasi cepat" di bawah.

## Ubuntu / Linux (NVIDIA CUDA, eksperimental)

Build engine yang sudah di-patch dengan `bash scripts/kur-linux.sh`, atau gunakan `Dockerfile.linux` untuk build dan
menjalankannya di lingkungan Ubuntu 24.04 / CUDA 12.8.1. Membutuhkan GPU NVIDIA dan driver yang kompatibel; installer
native juga membutuhkan CUDA toolkit dan Python 3.10-3.13. Antarmuka tetap hanya di loopback, termasuk di server jarak
jauh (penerusan SSH). Prasyarat, perintah, pemilihan arsitektur, dan cakupan validasi: [docs/linux.md](docs/linux.md).

## Mulai cepat (macOS, Apple Silicon)

Membutuhkan Xcode Command Line Tools (`xcode-select --install`) dan [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Installer mengunduh model, mem-build engine yang sudah di-patch dengan Metal (~1 menit), dan menyiapkan semuanya di
`~/vox`. Lalu klik dua kali **`baslat.command`**. Di MacBook Air M4 16 GB: ~2 detik komputasi per 1 detik ucapan, seed
yang sama menghasilkan audio yang identik hingga ke bita, RAM puncak ~5,3 GB, tanpa perlambatan termal selama 12 menit
pembacaan terus-menerus. Detail dan hasil pengukuran: [docs/mac.md](docs/mac.md).

**Aplikasi Mac native (tanpa Python, Homebrew, atau Terminal):** [macos/README.md](macos/README.md). Aplikasi ini
membawa engine yang sama yang sudah di-patch dan mengunduh model saat pertama kali dibuka; untuk saat ini aplikasinya
di-build dari kode sumber dengan Xcode.

## Untuk pengguna Mac (Apple Silicon)

Ada juga adaptasi independen buatan komunitas untuk Mac Apple Silicon yang menjalankan VoxCPM2 dengan framework MLX
milik Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Proyek ini dikembangkan dan dikelola oleh Emre Koç ([@emre-koc](https://github.com/emre-koc)) di repositorinya sendiri,
bukan di sini; langkah instalasi dan pertanyaan dukungan silakan diajukan di sana. Terima kasih, Emre, sudah membawa
proyek ini ke Mac!

## Cara kerja

1. **Desain suara.** Sebuah *deskripsi suara* berbahasa Inggris + sebuah *teks yang dibacakan saat suara dibuat*
   (dalam bahasa suara tersebut) + jumlah varian. Setiap varian mendapat seed sendiri; engine menerima
   `(description)text` dan mengembalikan satu rekaman desain per seed. Teksnya adalah contoh pendek untuk mengenali
   suara: 1-2 kalimat, maksimal ~20 detik (antarmuka menampilkan perkiraannya dan tidak akan mulai jika di atas 22
   detik); teks panjang adalah urusan langkah 2.
2. **Pembacaan berbasis referensi.** Rekaman desain diberikan ke **kedua** input engine (`audio` dan `voice_ref`),
   bersama transkripnya (`reference_text`) dan teks baru yang akan dibacakan, dengan seed yang sama. Suara dibawa oleh
   rekaman, bukan oleh deskripsi, sehingga tidak bergeser dari satu teks ke teks lain. Teks dibacakan kalimat demi kalimat.
3. Kualitas bersifat tetap: 16 langkah difusi, CFG 2.0. Seed bukan pengatur kualitas.

Rekaman desain mentah adalah contoh suara yang hanya muncul sekali; tidak ada pembacaan berikutnya yang terdengar
persis sama dengannya. Yang kamu dengar di setiap pembacaan berikutnya adalah langkah 2: rekaman desain sebagai
referensi ditambah seed milik varian itu sendiri. Karena itulah antarmuka web menjalankan langkah 2 tepat setelah
desain dan menampilkan keduanya di kartu varian.

Engine-nya adalah audio.cpp v0.7.2 dengan patch kami (`patches/`), modelnya VoxCPM2 Q8_0 GGUF. VRAM puncak ≈ 2,8 GB;
sekitar 2 detik komputasi per 1 detik ucapan di GTX 1050 Ti. Detail dan hasil pengukuran: [docs/4gb.md](docs/4gb.md).

## Suara bawaan (`hazir_sesler/`)

Keempat belas suara didesain dari prompt yang tersimpan di `ses.json` masing-masing; tidak ada yang dikloning dari
rekaman (kloning adalah tab *Kloning suara* tersendiri yang memerlukan persetujuan).

| Suara | Deskripsi singkat | Dengarkan |
|---|---|---|
| `belgesel_hanim` | Wanita dewasa berusia lima puluhan, alto yang dalam dan hangat; narator dokumenter yang tenang | [contoh](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referensi](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Narator pria yang dalam, kuat, dan misterius | [contoh](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referensi](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Pembaca berita senior berusia sekitar tujuh puluh, tenang dan berwibawa | [contoh](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referensi](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Pembaca berita malam berusia tiga puluhan yang karismatik, suaranya lembut seperti beledu dan ekspresif | [contoh](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referensi](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Penyihir dongeng: rendah, sedikit sengau, manis tapi licik | [contoh](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referensi](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Narator pria yang luar biasa dalam, padat, dan berwibawa | [contoh](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referensi](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Pria tua yang bijak, dalam dan menggelegar, sedikit misterius | [contoh](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referensi](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Narator dokumenter pria penutur asli bahasa Inggris berusia lima puluhan (General American); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Narator dokumenter pria penutur asli bahasa Prancis berusia lima puluhan (Paris); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Narator dokumenter pria penutur asli bahasa Jerman berusia lima puluhan (Hochdeutsch); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Narator dokumenter pria penutur asli bahasa Spanyol berusia lima puluhan (Kastilia (Madrid)); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Narator dokumenter pria penutur asli bahasa Rusia berusia lima puluhan (Moskow); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Narator dokumenter pria penutur asli bahasa Tionghoa (Mandarin) berusia lima puluhan (Putonghua Beijing); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Narator dokumenter pria penutur asli bahasa Jepang berusia lima puluhan (standar Tokyo); dalam, tenang, hangat | [contoh](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referensi](hazir_sesler/anlatici_ja/referans.flac) |

Setiap folder berisi: `referans.flac` (rekaman desain lossless), `ses.json` (prompt, transkrip, seed desain, seed
pembacaan, deskripsi; `dil` = bahasa untuk para narator), `ornek_okuma.mp3` (+ teksnya). Gunakan langsung:
`--ses hazir/<name>`. Rekaman referensi para narator pendek (5,6-10 detik); contoh pembacaannya adalah tiga kalimat
pertama naskah Cappadocia, dipotong dari pembacaan produksi lengkap.

## Instalasi cepat, tanpa compiler (Windows 10/11, GPU NVIDIA ≥ 4 GB)

Prasyarat: driver NVIDIA ≥ 570 dan Python 3.10-3.13 64-bit (`winget install Python.Python.3.12`). Tidak perlu yang
lain: tanpa Visual Studio, tanpa installer CUDA. Tidak yakin kartu grafis apa yang kamu punya? Jalankan `nvidia-smi` di
PowerShell: perintah ini menampilkan nama GPU, versi driver, dan memorinya. Tidak punya kartu NVIDIA? Lihat "AMD /
Intel" di bawah.

Dengan [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Tanpa Git: di halaman ini klik **Code → Download ZIP**, ekstrak, buka folder `voxcpm2-turkce-ses-tasarimi-main` hasil
ekstraksi, ketik `powershell` di bilah alamat Explorer lalu tekan Enter, kemudian jalankan baris terakhir di atas. Git
hanya diperlukan untuk jalur build dari kode sumber.

`-ExecutionPolicy Bypass` hanya berlaku untuk proses ini saja dan tidak mengubah pengaturan sistem apa pun; baca
`scripts\kur.ps1` sebelum menjalankannya, seperti pada skrip installer mana pun. Satu perintah, ~10 menit, unduhan
~3,7 GB, semuanya diverifikasi dengan sha256: model (2,95 GB), DLL runtime CUDA 12.8 sebagai zip portabel (tanpa
instalasi sistem, PATH tidak diubah), **engine siap pakai** dari halaman Releases, sebuah `.venv` dengan dua paket
Python, `ayarlar.json`, dan pemeriksaan GPU terakhir (`KONTROL_OK`). Jika gagal, jalankan ulang saja; berkas yang
sudah terverifikasi akan dilewati. Lalu jalankan antarmuka web: klik dua kali **`baslat.bat`** di folder repositori.
Ini akan menjalankan antarmuka dan membuka **http://127.0.0.1:8765/** di peramban saat sudah siap; tutup jendela hitam
(atau tekan Ctrl+C di sana) untuk menghentikannya. Hal yang sama dari PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
lalu buka sendiri **http://127.0.0.1:8765/** (jika dijalankan dengan cara ini, antarmuka tidak membuka peramban; ia
hanya mendengarkan di localhost).

> **`audiocpp_cli.exe` di dalam zip rilis tidak dimaksudkan untuk diklik dua kali.** Ini adalah engine baris perintah
> yang membutuhkan DLL CUDA dan model di sebelahnya; `kur.ps1` menempatkan semuanya dan paket Python yang
> menjalankannya. Mengklik dua kali hanya akan menampilkan "cudart64_12.dll not found".

**GPU yang didukung (rilis v0.1.1):** kode native untuk GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89), dan RTX 50xx (sm_120a); GPU CUDA lain mulai dari Pascal menjalankan PTX tertanam melalui driver (start pertama
lebih lambat). Maxwell (GTX 9xx) dan yang lebih lama tidak didukung oleh CUDA 12.8. Kami mengujinya di GTX 1050 Ti 4 GB (juga lewat Docker Desktop/WSL2 di Windows, hanya CLI); diukur oleh @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (detail di [docs/linux.md](docs/linux.md)). Laporan dari kartu grafis lain sangat kami harapkan di [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (eksperimental):** zip engine Vulkan terpisah (`...-win64-vulkan.zip`, tanpa CUDA) dipasang dengan
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Ini baru diverifikasi di kartu NVIDIA kami melalui backend Vulkan (di sana ia
berjalan lebih lambat daripada CUDA tetapi menghasilkan audio yang sama untuk seed yang sama; pengukuran itu dilakukan
saat disk sedang sibuk dengan pekerjaan lain, jadi perbandingan kecepatan yang bersih masih tertunda) dan kami **belum**
mengujinya sendiri di perangkat keras AMD atau Intel: jika kamu mencobanya, silakan unggah hasilnya di Discussions.
Jika ada lebih dari satu perangkat Vulkan (terintegrasi + diskret), installer menulis indeks GPU diskret sebagai `cihaz`
ke dalam `ayarlar.json`.

*Catatan: Dukungan Vulkan saat ini masih eksperimental. Dukungan ini sudah berhasil di-build dan diuji di GTX 1050 Ti.
Seorang pengguna eksternal (mitra_tr) juga melaporkan berhasil menjalankannya di AMD 6900 XT. Pengujian yang lebih luas
di kartu AMD/Intel masih diperlukan.*

**Uji komunitas (AMD):** @mitraTR menjalankan v0.1.1 dengan Vulkan di AMD Radeon RX 6900 XT pada Windows 11: instalasi, desain suara, pembacaan, antarmuka web, dan pengujian semuanya berhasil; pembacaan butuh sekitar 0,8-0,9 dtk komputasi per 1 dtk ucapan ([laporan di #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Pasang di folder pendek yang jalurnya hanya berisi karakter ASCII (mis. `C:\vox`): di Windows mesin tidak bisa membuka jalur yang berisi karakter non-ASCII. Semua laporan sejauh ini: [perangkat keras yang sudah diuji](docs/donanim_testleri.md).

### Alternatif: build engine dari kode sumber

Membutuhkan Visual Studio 2022 Build Tools dengan "Desktop development with C++" (termasuk C++ CMake tools), ~7 GB. Lalu:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Perintah ini juga mengunduh nvcc, mengambil kode sumber audio.cpp v0.7.2, menerapkan
`patches/0001-voxcpm2-4gb-ve-hiz.patch`, dan mem-build untuk GPU-mu (`-Mimari native`, bawaan; atau misalnya
`-Mimari 61`), ~15-25 menit. Gunakan folder root yang pendek (`C:\vox`): nvcc gagal pada path yang panjang. Langkah
demi langkah dengan pemeriksaan: [AGENTS.md](AGENTS.md).

### Masalah instalasi yang umum

| Yang kamu lihat | Artinya, apa yang harus dilakukan |
|---|---|
| `cudart64_12.dll not found` setelah mengklik dua kali exe | Engine tidak dimaksudkan untuk dijalankan secara manual. Jalankan perintah `kur.ps1` di atas, lalu jalankan antarmuka web. |
| `64-bit Python 3.10+ bulunamadı` (Python tidak ditemukan) | Instal Python (`winget install Python.Python.3.12`), tutup PowerShell, buka yang baru, lalu jalankan perintah yang sama lagi. |
| `motor ekran kartını görmedi` (engine tidak mendeteksi GPU) | Perbarui driver NVIDIA ke 570 atau yang lebih baru; pastikan `nvidia-smi` bisa berjalan. |
| `indirme başarısız` / `sha256 tutmadı` (unduhan gagal / checksum tidak cocok) | Biasanya karena unduhan terputus. Jalankan perintah yang sama lagi; berkas yang sudah terverifikasi akan dilewati. |
| Jalur build: `nvcc` gagal | Gunakan root instalasi yang pendek (`-Kok C:\vox`). |
| Halaman tidak terbuka | Jalankan antarmuka dengan `baslat.bat`, atau buka sendiri http://127.0.0.1:8765/. Port sedang dipakai? Ubah `"port"` di `ayarlar.json`. |

Ada masalah? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) atau buat
[issue instalasi](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
dengan menyertakan GPU, versi Windows, perintah yang dijalankan, dan baris-baris terakhir keluarannya.

## Penggunaan

Baris perintah:
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
Aturan teks: tulis angka dengan huruf, jangan pakai tanda kutip (alat ini menolak digit dan tanda kutip), satu kalimat
per baris, ≤ 2000 karakter per baris. Jeda setelah baris: `|| bagli` 0,25 dtk, `|| normal` 0,5 dtk, `|| paragraf` 1
dtk, `|| agir` 1,5 dtk, atau panjang pilihanmu sendiri `|| 0,8` (0-5 dtk; digit pada penanda ini diperbolehkan).
`ayarlar/okunus_sozlugu.tsv` memperbaiki pelafalan kata asing dalam teks berbahasa Turki. Bahasa dideteksi dari teks
(huruf Turki, aksara, kata-kata umum; `dil` dari kartu suara jika ragu; `--dil <code>` bersifat opsional). Untuk teks
non-Turki, apostrof diperbolehkan, kamus Turki dilewati, digit tetap ditolak. Jika sebuah pembacaan mencetak
`speed gate: satır [...]`, dengarkan baris-baris tersebut.

### Antarmuka web

Hanya lokal (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → buka sendiri http://127.0.0.1:8765/
(port lain: `--port 8800`), atau klik dua kali `baslat.bat`. Hentikan server dengan Ctrl+C. Tiga tab: *Desain suara*,
*Bacakan dengan suara ini*, *Kloning suara*. Alur yang biasa: *Desain* → dengarkan variannya → *Tambahkan ke daftar
baca saya* → *Bacakan dengan suara ini* → unduh. Atau pilih suara bawaan dari menu suara lalu bacakan.

- **Versi di bagian header.** Teks kecil dan samar `v0.2.0 · <short commit>` (dengan `+` jika berkas yang dilacak punya
  perubahan yang belum di-commit; hanya versi jika tanpa git), agar tangkapan layar dan video menunjukkan versi yang dipakai.
- **Dua suara di setiap kartu varian.** Di atas, berwarna abu-abu, ada *Suara desain mentah*: dibuat sekali dan tidak
  akan keluar persis sama lagi. Di bawahnya, dalam bingkai oranye, ada *↻ Inilah suara yang akan selalu kamu dengar*:
  rekaman desain yang dibacakan kembali sebagai referensi dengan seed milik varian itu sendiri (ditampilkan di kartu).
  Seperti inilah suara itu terdengar di setiap pembacaan berikutnya. Di bawahnya ada *Bacakan dengan suara ini* dan
  *Tambahkan ke daftar baca saya*. Sekali tekan *Desain* melakukan keduanya: mendesain setiap varian, lalu membacakan
  teksmu dengan setiap suara tetapnya; satu bilah progres menghitung kedua fase. Folder varian mendapat `dinleme.wav`.
  Jika pembacaan itu berhenti lebih awal, desainnya tetap disimpan dan kartu menampilkan catatan.
- **Jendela "Teks yang ingin kamu dengar".** Di *Desain suara*, kotak *↻ Teks yang ingin kamu dengar* berisi apa yang
  dibacakan setiap suara tetap (jika dibiarkan kosong, kalimat contoh yang dibacakan). Mengekliknya membuka buku catatan
  baca di sebuah jendela: nomor baris, menu baris, pita jeda. *OK* menulis teks beserta jedanya kembali ke kotak;
  *Batal* atau Esc tidak mengubah apa pun. Tab baca menyimpan teksnya sendiri.
- **Buku catatan baca.** Satu kalimat per baris. Klik nomor baris untuk membuka menu baris (pindah ke atas atau bawah,
  pindah ke posisi tertentu, duplikat, hapus; Alt+↑/↓, Alt+Shift+↓, atau seret lewat nomornya; Ctrl+Z membatalkan teks
  dan jeda sekaligus). Klik pita tipis di antara dua baris untuk memilih jeda (bagli 0,25 · normal 0,5 · paragraf 1 ·
  agir 1,5 dtk, atau panjang pilihanmu sendiri 0-5 dtk lewat ikon roda gigi); tekan Enter dua kali untuk paragraf (1
  dtk), dan baris kosong menjadi pita jeda. Saat hasil diputar, baris yang sedang dibacakan menyala dan digulir ke dalam
  tampilan; *▶ Dengarkan dari sini* di menu baris memutar dari baris tersebut. Teks dan jedanya tetap ada setelah
  halaman dimuat ulang (penyimpanan peramban).
- **Draf.** Tombol *📄 Draf* ada di kedua buku catatan (tab baca dan jendela). Simpan teks saat ini beserta jedanya
  sebagai draf, muat salah satunya dengan sekali klik (Ctrl+Z membatalkan), dan gunakan ⋯ untuk menimpa, mengganti
  nama, atau menghapusnya. Draf disimpan di `sesler/taslaklar.json`, tidak pernah di dalam repositori.
- **Daftar baca dan menu suara.** Di kartu varian, *Tambahkan ke daftar baca saya* membuka kotak nama: beri varian itu
  nama sendiri dan ✓ akan menambahkannya. *Nama pembuatan* tetap ada di setiap varian dari proses itu. Di *Bacakan
  dengan suara ini*, tombol suara (bendera + nama) membuka menu suara: *Daftar baca saya* di atas, lalu suara bawaan
  dengan bendera (bahasa antarmuka lebih dulu). Setiap baris punya ▶ dengarkan (suara tetap jika ada), ikon hati
  (tambah atau hapus), dan ⋯; ↑/↓ dan Enter untuk memilih, Esc untuk menutup, suara terakhir diingat. Daftar ini
  tersimpan di `sesler/okuma_listesi.json`, di luar repositori, dan tetap ada setelah dimulai ulang.
- **Mengelola suara.** Menu ⋯ (baris di menu suara atau kartu varian) berisi *Bacakan dengan suara ini*, tambah ke
  atau hapus dari daftar, *Ganti nama* (nama kosong mengembalikan nama aslinya; *Kembali ke nama asli*), *Hapus* untuk
  suara hasil desain, dan *Sembunyikan* untuk suara bawaan; keduanya meminta konfirmasi lebih dulu. Suara yang dihapus
  dipindahkan ke `sesler/_cop/`; menyembunyikan tidak pernah menyentuh berkas repositori. *Suara tersembunyi dan
  terhapus (N)* di bagian bawah menu suara punya *Pulihkan*. Nama kustom dan suara tersembunyi disimpan di
  `sesler/yerel_katman.json`. Suara yang sudah diganti namanya menampilkan asalnya dalam warna abu-abu (*nama pembuatan
  · varian N*); ⋯ → *Buka pembuatan* membuka desainnya.
- **Pintasan dan berkas.** Ctrl+Enter (⌘+Enter di Mac) memulai *Desain* atau *Bacakan dengan suara ini* di tab yang
  sedang terbuka. Bilah progres menampilkan *berjalan / ~total*, dengan perkiraan yang dipelajari dari pekerjaan
  sebelumnya di komputermu. Hasil unduhan dinamai sesuai suara dan waktu (`Voice_Name_2026-11-02_0152.wav`).

**Kloning suara (suaramu sendiri atau suara dengan izin).** Di tab *Kloning suara* pada antarmuka, berikan rekamanmu (wav/mp3/flac/ogg, disarankan 5-30 dtk ucapan yang bersih; di bawah 3 dtk ditolak, di atas 36 dtk dipotong), transkrip persisnya, dan teks yang akan dibacakan. Tombolnya tetap nonaktif sampai kamu mencentang "Suara ini milik saya atau saya punya izin jelas dari pemiliknya". Rekaman hanya dikirim ke server lokal (127.0.0.1), diproses di folder sementara bersama encoding referensinya, dan folder itu dihapus saat pekerjaan selesai, termasuk saat gagal; tidak ada yang dikirim lewat jaringan. Hanya keluaran sintetis yang disimpan (antarmuka: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Keluarannya adalah `klon_synthetic.wav` dengan tag "synthetic"; beri label sebagai buatan AI saat membagikannya. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Tanya jawab

**Model atau engine? Apa bedanya?** VoxCPM2 (OpenBMB) adalah *model*-nya: jaringan dengan 2 miliar parameter yang
mengubah teks menjadi ucapan. audio.cpp adalah *engine*-nya: program C++/CUDA yang menjalankan model di GPU-mu
(`audiocpp_cli.exe`). Patch kami mengubah engine, bukan model: patch ini membuat VoxCPM2 muat di 4 GB dan membuat seed
yang sama selalu menghasilkan audio yang sama. Paket Python di repositori ini hanya menyiapkan teks, memanggil engine,
dan mengumpulkan berkas-berkasnya.

**GPU apa saja?** Lihat "GPU yang didukung" di atas: NVIDIA mulai dari GTX 10xx, VRAM 4 GB atau lebih, driver ≥ 570.
Kode native ada di rilis untuk sm_61/75/86/89/120a; kartu lain dari Pascal atau yang lebih baru memakai PTX tertanam
(start pertama lebih lambat). AMD/Intel: zip Vulkan eksperimental, `kur.ps1 -Vulkan`; seorang pengguna eksternal
melaporkan berhasil menjalankannya di AMD 6900 XT, tetapi pengujian AMD/Intel yang lebih luas masih diperlukan (lihat
"AMD / Intel" di atas). Hanya CPU (`"backend": "cpu"` di `ayarlar.json`) bisa berjalan tetapi ~6× lebih lambat daripada
GTX 1050 Ti (pengukuran engine, 535 dtk vs 94 dtk untuk 48 dtk ucapan); bukan jalur yang didukung.

**Seberapa cepat?** Diukur di GTX 1050 Ti 4 GB (i7-7700HQ): satu varian desain (rekaman ≈ 25 dtk) 55 dtk; pembacaan ≈
2 detik komputasi per 1 detik ucapan (real-time factor 1,9-2,8) setelah encoding referensi satu kali ~50 dtk per suara
(di-cache di disk) dan 10-20 dtk memuat model per batch; VRAM puncak 2,6-2,9 GB. Kartu yang lebih baru lebih cepat;
angka dan metodenya: [docs/4gb.md](docs/4gb.md).

**Bisakah mengkloning suara?** Model VoxCPM2 yang mendasarinya bisa meniru suara dari rekaman referensi, dan bagian
kloning memakai kemampuan itu. Gunakan hanya dengan suaramu sendiri atau dengan izin jelas dari pemilik suara tersebut;
antarmuka akan memintamu mengonfirmasi izin itu. Desain suara tidak memerlukan rekaman: ia dimulai dari deskripsi teks
dalam bahasa Inggris atau Mandarin, dan "referensi" yang dipakai untuk membacakan suara hasil desain adalah rekaman
desain sintetis buatan model itu sendiri. Peniruan identitas, penipuan, dan penyesatan dilarang. Lihat
[ETHICS.md](ETHICS.md). Beri label bahwa yang kamu publikasikan dihasilkan oleh AI.

**Bagaimana menulis deskripsi suara yang baik?** Dalam bahasa Inggris, 1-3 kalimat: usia dan jenis kelamin, warna
suara (dalam/cerah, hangat, sengau, serak), nada dan peran (narator dokumenter yang tenang, presenter yang energik),
tempo (lambat, terukur), dan "clean studio recording, no background noise". Pastikan tetap berupa deskripsi, bukan
naskah; jangan pakai tanda kurung. Minta 3-5 varian lalu dengarkan: seed sangat mengubah suara. Untuk teks pembuatan,
gunakan 1-2 kalimat alami dalam bahasa suara tersebut, dengan suasana yang kamu inginkan (maksimal ~20 dtk ucapan).
Saat membacakan, satu kalimat per baris; pecah kalimat panjang, tulis angka dengan huruf.

## Berkontribusi

Bingung mulai dari mana? Empat issue kecil ini adalah langkah awal yang bagus:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Coba di GPU-mu dan laporkan kartu grafis, driver, dan waktunya
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: coba build Vulkan eksperimental
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Tambahkan satu kalimat ke set uji
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Bagikan suara yang kamu desain, beserta deskripsi dan seed-nya

**Uji kartu grafismu, tulis laporan:** tidak perlu bisa koding, cukup isi [formulir laporan uji perangkat keras](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); belum ada laporan dari kartu grafis Intel.

Set uji bersama: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); panduan suara merek:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); cara mengirim kode: [CONTRIBUTING.md](CONTRIBUTING.md).
Masalah instalasi: [formulir issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); pertanyaan dan hasil: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Semua yang ikut serta mengikuti [Kode Etik](CODE_OF_CONDUCT.md): bersikap baik, dan jaga agar masukan tetap tentang pekerjaannya.

## Kontributor

- [@alexturkey](https://github.com/alexturkey): maintainer; kode, suara bawaan, dokumentasi
- [@cayir21](https://github.com/cayir21): dukungan Metal untuk macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): perbaikan akhir kalimat (EOS) untuk pembacaan multi-kalimat di backend CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): instalasi CUDA eksperimental untuk Ubuntu/Linux dan dukungan Docker, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Namamu juga layak ada di sini: hasil uji dari GPU-mu, satu kalimat untuk set uji, suara yang kamu desain, laporan bug
yang jelas, atau pull request, semuanya terhitung sebagai kontribusi. Terima kasih kepada semua yang mencoba dan
memberi kabar.

## Lisensi dan kredit

Kode dan suara bawaan: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Dibangun di atas VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0), dan konversi GGUF audio.cpp. Daftar lengkap: [THIRD_PARTY.md](THIRD_PARTY.md).
Tidak berafiliasi dengan OpenBMB, ModelBest, atau proyek audio.cpp.

# Vulkan engine (AMD, Intel, NVIDIA) / Vulkan motoru

Experimental. The Vulkan engine needs no CUDA: any GPU with a Vulkan 1.2+ driver (`vulkan-1.dll`) can run it.
Word timings work on Vulkan since engine v0.3.1. Short user notes are in the README; this page has the details.
/ Deneysel. Vulkan motoru CUDA istemez: Vulkan 1.2+ sürücüsü (`vulkan-1.dll`) olan her ekran kartında çalışır. Kelime
zamanları motor v0.3.1'den beri Vulkan'da da çıkar. Kısa kullanıcı notları README'de; ayrıntı bu sayfada.

## Two packages / İki paket

| Package / Paket | CPU / İşlemci | Speed / Hız |
|---|---|---|
| `…-win64-vulkan.zip` | AVX2 + FMA + F16C + BMI2 (most Intel Core from 2013 / Haswell, AMD from 2015 / Excavator; many Pentium/Celeron lack AVX2) | fast / hızlı |
| `…-win64-vulkan-uyumlu.zip` | any 64-bit x86 CPU (SSE2) / her 64 bit x86 işlemci | a voice's first reading ~2.2x as long / sesin ilk okuması ~2,2 kat uzun |

Measured on a GTX 1050 Ti (Vulkan, same text and seed): first reading of a voice 109.5 s (AVX2) vs 243.9 s
(compatible); later readings with the cached reference 57.8 s vs 57.8 s. The difference is the reference encoding,
which runs on the CPU. The GPU part is the same, and so is the audio for the same seed on the same card.
/ GTX 1050 Ti'de ölçüm (Vulkan, aynı metin ve tohum): sesin ilk okuması 109,5 sn (AVX2), 243,9 sn (uyumlu); referans
önbellekteyken sonraki okumalar 57,8 / 57,8 sn. Fark işlemcide çalışan referans kodlamasından gelir; ekran kartı kısmı
ve aynı kartta aynı tohumla çıkan ses aynıdır.

## Automatic choice / Kendiliğinden seçim

`scripts\kur.ps1 -Kok C:\vox -Vulkan` picks the package (`-Islemci oto`, the default):
1. The Python step runs first. `python -m ses_tasarim.islemci` reads numpy's CPU detection: if AVX, AVX2, FMA3 or F16C
   is missing (or BMI, BMI2, LZCNT when numpy lists them), or detection fails, the compatible package is chosen.
2. If the AVX2 package was chosen, its exe runs `--list-devices` once from a temp folder, before it is installed.
   Any result other than "ok" (for example illegal instruction, `0xC000001D`) installs the compatible package instead.
   No Windows error dialog opens.

`-Islemci avx2` or `-Islemci uyumlu` chooses by hand, without the test run. With `-HazirZip <zip>` the package is
recognised from the zip's sha256.
/ `kur.ps1 -Vulkan` paketi kendisi seçer (`-Islemci oto`): önce Python adımı çalışır, `ses_tasarim.islemci` numpy'nin
işlemci tespitini okur (bir aile eksikse ya da okunamazsa uyumlu). AVX2 seçildiyse exe yerleşmeden önce geçici klasörde
bir kez çalıştırılır, "ok" dışındaki her sonuçta uyumlu paket kurulur. `-Islemci avx2|uyumlu` elle seçer; `-HazirZip`
ile paket zip'in sha256'sından anlaşılır.

## Decoder chunk / Çözücü dilimi

Cards with a low compute limit (`maxComputeWorkGroupCount` below 2^20, for example Intel HD 630 with 65536) decode audio
in 5 s chunks instead of 10 s; `ses_tasarim/vulkan_sinir.py` reads the limit. The chunk length does not change the
audio (measured: 10 s and 5 s chunks give byte-identical output). Before this, long designs and long single-line readings
aborted on such cards with `GGML_ASSERT ... maxComputeWorkGroupCount`.
/ İş kümesi sınırı düşük kartlarda (2^20 altı, ör. Intel HD 630: 65536) ses 10 yerine 5 sn'lik dilimlerle çözülür; dilim
boyu sesi değiştirmez (ölçüldü: bayt bayt aynı).

## Build it yourself / Kendin derle

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\derle.ps1 -Kaynak C:\vox\motor\src -Build C:\vox\motor\build `
    -Vulkan -VulkanSdk <LunarG SDK> -Islemci native
```
`-Islemci native` builds for this PC's CPU (fastest here, may not run elsewhere); `avx2` and `tasinabilir` match the
two release packages. The source must be audio.cpp v0.7.2 with patches 0001 and 0002 (`kur.ps1 -Adim kaynak` applies
all three; 0003 only touches CUDA code). Needs `glslc.exe`, the Vulkan headers (incl. `spirv/unified1/spirv.hpp`) and `vulkan-1.lib`.
/ `-Islemci native` bu bilgisayarın işlemcisine göre derler (burada en hızlı, başka makinede çalışmayabilir); `avx2` ve
`tasinabilir` iki yayın paketinin ayarı. Kaynak: audio.cpp v0.7.2 + yama 0001 ve 0002.

## Checking the compatible build on a modern CPU / Uyumlu paketi yeni işlemcide denemek

Intel SDE (Software Development Emulator) emulates older CPUs: `sde.exe -snb -- audiocpp_cli.exe --list-devices` runs the
exe as on Sandy Bridge (AVX, no AVX2), `-mrm` as on Merom (no AVX). The compatible exe passed real readings under both;
the AVX2 exe stops under `-snb` at its first BMI2 instruction (`shlx`), which is the expected result. Emulation is slow;
use short texts.
/ Intel SDE eski işlemcileri taklit eder: `-snb` Sandy Bridge (AVX var, AVX2 yok), `-mrm` Merom (AVX yok). Uyumlu exe
ikisinde de gerçek okumayı geçti; AVX2 exe `-snb` altında ilk BMI2 komutunda (`shlx`) durur, beklenen budur.

## Common errors / Sık hatalar

| Message / Mesaj | Cause and fix / Neden ve çözüm |
|---|---|
| `motor Vulkan cihazı görmedi` (kontrol step) | no Vulkan driver: install the current AMD/Intel/NVIDIA driver; `vulkan-1.dll` must exist / Vulkan sürücüsü yok: güncel sürücü |
| exit code `0xC000001D` / `-1073741795` | CPU lacks an instruction of the AVX2 package: use `vulkan-uyumlu` (`kur.ps1 -Vulkan` does this itself) / işlemci AVX2 paketini çalıştıramıyor |
| `GGML_ASSERT ... maxComputeWorkGroupCount` | older repo version on a low-limit card: update (`git pull`); the 5 s chunk fixes it / eski sürüm, güncelleyin |
| design aborts on a laptop with two GPUs | device 0 is the integrated GPU: the installer writes the discrete GPU as `"cihaz"` in `ayarlar.json`; check it there / dahili kart seçilmiş, `ayarlar.json` `cihaz` |
| very slow first start | shaders compile on the first run (a few minutes); later starts are faster / ilk açılışta gölgelendirici derlemesi |
| engine cannot open a path | path has non-ASCII letters: install to a short ASCII folder such as `C:\vox` / yol ASCII değil |

## Integrated graphics: RAM / Dahili (gömülü) kart: RAM

An integrated GPU (for example Intel HD/UHD Graphics) has no memory of its own: the model and the engine's buffers live
in system RAM. On a dedicated card the same data sits in the card's memory.

**With integrated graphics the engine uses up to about 8 GB of RAM** (measured: 8.0 GB while reading, 6.5 GB while
designing a voice). On a computer with 8 GB of RAM in total this may not be enough together with Windows and other
programs (not tested on such a machine). Generation is also much slower: the same two-line reading took 446 s on the
integrated Intel HD Graphics 630 and 110 s on a GTX 1050 Ti (both Vulkan, first reading of the voice).

**Dahili kartla üretimde motor en çok yaklaşık 8 GB RAM kullanır** (ölçüm: okumada 8,0 GB, ses tasarımında 6,5 GB).
Toplam 8 GB RAM'li bilgisayarda Windows ve diğer programlarla birlikte yetmeyebilir (böyle bir makinede denenmedi).
Üretim de çok daha yavaştır: aynı iki satırlık okuma dahili Intel HD Graphics 630'da 446 sn, GTX 1050 Ti'de 110 sn
sürdü (ikisi de Vulkan, sesin ilk okuması).

Measurement / Ölçüm: Intel HD Graphics 630, 16 GB RAM, Windows 10, Vulkan AVX2 build, first reading of the voice
(reference not cached yet). "Engine peak RAM" is the engine process's peak working set as reported by Windows;
"lowest free RAM" is free memory of the whole system (Windows and background programs included), sampled every 5 s.
/ "Motor tepe RAM" Windows'un bildirdiği motor sürecinin en yüksek çalışma kümesi; "en az boş RAM" bütün sistemin boş
belleği (Windows ve arka plan programları dahil), 5 sn'de bir örnek.

| Job / İş | Engine peak RAM / Motor tepe RAM | Lowest free RAM / En az boş RAM | Time / Süre | Audio / Ses |
|---|---|---|---|---|
| Reading, 2 lines / Okuma, 2 satır | 8,001 MB | 2,561 MB (10,540 MB before start / başlamadan önce) | 446 s | 9.2 s |
| Voice design, 30 s text / Ses tasarımı, 30 sn metin | 6,506 MB | 3,907 MB | 902 s | 26.9 s |

Windows also counted more committed memory for the engine than it kept in RAM (peak private bytes 16,050 MB in the
reading above). Committed memory must fit within RAM plus the page file (the Windows commit limit), so leave the page
file on (the Windows default); with it turned off the engine may run out of memory (not tested).
/ Windows motor için RAM'de tuttuğundan fazla ayrılmış bellek saydı (yukarıdaki okumada en çok 16.050 MB). Ayrılmış
bellek RAM ile sayfa dosyasının toplamına sığmalıdır (Windows'un ayırma sınırı); sayfa dosyasını açık bırakın (Windows
varsayılanı), kapalıyken bellek yetmeyebilir (denenmedi).

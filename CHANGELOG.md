# Sürüm notları / Release notes

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

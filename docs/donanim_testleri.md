# Test edilmiş donanım / Tested hardware

**TR:** Bu listedeki her satır gerçek bir makinede çalıştırılmış bir denemedir. Hız, 1 saniyelik konuşma için geçen hesap
süresidir (küçük = hızlı); ölçenin kendi ölçümüdür, karşılaştırmalı bir hız testi değildir. Kalite her satırda aynı:
16 adım, cfg 2.0. Kendi kartında denedin mi? [Donanım test raporu formunu](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml)
doldur, satırın adınla buraya eklensin. **Intel ekran kartında henüz hiç deneme yok**; Intel Arc ya da dahili Intel
grafikle Vulkan sürümünü deneyen ilk rapor çok değerli olur ([#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6)).

**EN:** Every row is a run on a real machine. Speed is the compute time per 1 second of speech (lower = faster), as
measured by the reporter; it is not a side-by-side benchmark. Quality is the same in every row: 16 steps, cfg 2.0.
Tried it on your GPU? Fill in the [hardware test report form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml)
and your row is added here with your name. **There is no Intel GPU report yet**; a first run of the Vulkan build on
Intel Arc or Intel integrated graphics would help a lot ([#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6)).

| Kart / GPU | İşletim sistemi / OS | Backend | Sürüm / Version | Hız / Speed (1 sn ses / 1 s speech) | Ne çalıştı / What worked | Raporlayan / Reported by | Kaynak / Source |
|---|---|---|---|---|---|---|---|
| NVIDIA GTX 1050 Ti 4 GB | Windows 10 | CUDA 12.8 | v0.1.0+ | ~2 sn / s (1.9-2.8) | kurulum, tasarım, okuma, arayüz / install, design, reading, UI | @alexturkey | [docs/4gb.md](4gb.md) |
| NVIDIA RTX 3060 Ti 8 GB | Ubuntu 26.04 (Docker, Ubuntu 24.04) | CUDA 12.8.1, kaynaktan / from source | main, 2026-10-31 | kısa duman testi, hız ölçümü değil / short smoke test, not a speed benchmark | derleme, testler, tasarım, okuma / build, tests, design, reading | @mslmyilmaz5 | [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15), [docs/linux.md](linux.md) |
| Apple M4 (MacBook Air, 16 GB) | macOS 27.0.1 | Metal | main, 2026-10-23 | ~2.0 sn / s | derleme, tasarım, okuma / build, design, reading | @cayir21 | [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10), [docs/mac.md](mac.md) |
| AMD Radeon RX 6900 XT 16 GB | Windows 11 Home | Vulkan (deneysel / experimental) | v0.1.1 | ~0.8-0.9 sn / s | kurulum, tasarım, okuma, arayüz, testler / install, design, reading, UI, tests | @mitraTR | [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655) |
| Intel (Arc / dahili / integrated) | - | Vulkan | - | henüz rapor yok / no report yet | - | sen? / you? | [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) |

## Bilinen notlar / Known notes

- **Yol / Path (Windows):** motor yalnız ASCII karakterli yolları açabiliyor; Türkçe harfli klasörde `No mapping for the
  Unicode character exists in the target multi-byte code page` ya da `Failed to open log file` verir. Kurulumu ve repoyu
  kısa, ASCII bir klasöre koy (ör. `C:\vox`); `kur.ps1` artık ASCII olmayan `-Kok` yolunda baştan uyarıp durur (#6, @mitraTR).
  The engine opens ASCII-only paths on Windows; keep the install and the repo in a short ASCII folder such as `C:\vox`.
  `kur.ps1` now stops early on a non-ASCII `-Kok` path.
- **VRAM ölçümü / VRAM reading:** tepe VRAM yalnız NVIDIA (`nvidia-smi`) ve macOS'ta ölçülür. AMD/Intel'de özet artık
  0 MB yazmaz, VRAM kısmını göstermez; ölçülemeyen değer `ozet.json`'da `null` olur (#6, @mitraTR).
  Peak VRAM is measured only on NVIDIA and macOS; on AMD/Intel the summary leaves the VRAM part out instead of showing
  0 MB, and `ozet.json` stores `null`.
- **Birden çok Vulkan aygıtı / Several Vulkan devices:** dahili + harici kart varsa `kur.ps1 -Vulkan` harici kartın
  numarasını `ayarlar.json` içine `cihaz` olarak yazar (AMD + Intel UHD 770 makinesinde doğrulandı, #6).
  With integrated + discrete GPUs the installer writes the discrete card's index as `cihaz` (confirmed on an AMD +
  Intel UHD 770 machine, #6).

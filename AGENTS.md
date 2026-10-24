# AGENTS.md — step-by-step install for an AI coding agent (Claude Code, Codex, Cursor...)

This file is for an agent setting up the project on a **Windows 10/11 PC with an NVIDIA GPU (≥ 4 GB VRAM)**. Follow the
steps in order. **On a Mac (Apple Silicon) skip to "6b. macOS".** Every step has a command, the expected output and a check. Do not skip a check. Turkish is fine for the
user-facing texts; commands are language-neutral. `CLAUDE.md` points here.

Hard rules for agents working in this repo:
- Quality settings are fixed: 16 steps, cfg 2.0 (`ses_tasarim/motor.py: FIXED`). Never lower them "for speed".
- One GPU job at a time. Do not run two engine processes concurrently (`GGML_ASSERT mem_buffer`).
- Voice cloning is only for the user's own voice or a voice used with its owner's explicit permission. Keep the
  permission confirmation and the AI-generated notice in the UI; do not remove or bypass them. See `ETHICS.md`.
- Keep install paths short (`C:\vox`). Long paths break nvcc at the 260-character limit.
- `patches/*.patch` are LF. Never convert them to CRLF (`.gitattributes` protects them).
- Do not commit `ayarlar.json`, `sesler/`, `onbellek/`, models or build output (see `.gitignore`).

Two install paths. **Path A (default): prebuilt engine from the Releases page, no compiler.** Path B: build the engine
from source (needs Visual Studio Build Tools). Use A unless the user asks for B or the GPU is not covered by the release
(see "Supported GPUs" below).

## 0. Prerequisites (check, install what is missing)

| Need | Path | Check command | Expected | If missing |
|---|---|---|---|---|
| NVIDIA driver ≥ 570 (CUDA 12.8 runtime) | A, B | `nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader` | e.g. `NVIDIA GeForce GTX 1050 Ti, 581.29, 4096 MiB` | update the driver (admin) |
| Git | A, B | `git --version` | `git version 2.x` | `winget install Git.Git` |
| Python 3.10–3.13, 64-bit | A, B | `py -3 -c "import sys,struct;print(sys.version,struct.calcsize('P')*8)"` | `3.1x ... 64` | `winget install Python.Python.3.12`, then open a new shell. The Microsoft Store "python" alias is not a Python; `kur.ps1` skips it |
| curl, tar (built into Windows 10 1803+) | A, B | `curl.exe --version`, `tar.exe --version` | version lines | update Windows |
| Disk | A | `fsutil volume diskfree C:` | ≥ 8 GB free | model 2.95 GB + CUDA DLL zips 0.7 GB + extracted 0.9 GB + engine 0.1 GB |
| Visual Studio 2022 Build Tools with **Desktop development with C++** (MSVC v143, Windows SDK, **C++ CMake tools for Windows**) | B only | `"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath` | a path like `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools` | `winget install Microsoft.VisualStudio.2022.BuildTools --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"` (needs admin, ~7 GB) |
| Disk | B | `fsutil volume diskfree C:` | ≥ 12 GB free | + nvcc/cccl 0.2 GB + source 0.1 GB + build 0.4 GB |
| RAM | A, B | ≥ 8 GB total, ≥ 4.5 GB free when generating | – | – |

Known-good toolchain: VS 2022 17.14 (MSVC 14.44), CUDA 12.8.2 redist, Windows 10 22H2, driver 581.29. CUDA 13 does
**not** support Pascal (GTX 10xx); CUDA 11.8 does not build with MSVC 14.44. This is why the installer pins CUDA 12.8.

**Supported GPUs.** Release v0.1.1 `audiocpp_cli.exe` carries native code for sm_61 (GTX 10xx), sm_75 (RTX 20xx),
sm_86 (RTX 30xx), sm_89 (RTX 40xx), sm_120a (RTX 50xx) plus compute_89 PTX; other CUDA GPUs from Pascal on run the PTX
through the driver JIT (works, slower first start). Maxwell (GTX 9xx) and older: not supported by CUDA 12.8. Verified
only on a GTX 1050 Ti 4 GB. Check what a given exe contains with `cuobjdump --list-elf audiocpp_cli.exe` (CUDA
`cuda_cuobjdump` redist package).

**Vulkan (experimental, AMD/Intel/NVIDIA).** Separate release zip `…-win64-vulkan.zip`; `kur.ps1 -Kok C:\vox -Vulkan`
runs `model,hazir,python,ayar,kontrol` (no `cuda` step), writes `"backend": "vulkan"`, `"cuda_bin": ""`; `kontrol`
needs a `Vulkan:N` line from `--list-devices` and, when several devices are listed, writes the index of the `[GPU]` line as
`"cihaz"` (passed to the engine as `--device N`; default device 0 may be an integrated GPU, where a design aborts with
`maxComputeWorkGroupCount`). Verified only on a GTX 1050 Ti via Vulkan: design variant 108 s (CUDA 55 s), reading
6-13 s per 1 s of speech (CUDA ≈ 2 s), same seed → bit-identical wav. Vulkan numbers were taken while the disk was busy
with another job (CUDA numbers on an idle disk): clean comparison pending. Build: `kur.ps1 -Derle -Vulkan` /
`derle.ps1 -Vulkan [-VulkanSdk <dir>]` (needs `glslc.exe`, Vulkan headers incl. `spirv/unified1/spirv.hpp`,
`vulkan-1.lib`; `VULKAN_SDK` env var is the default). Runtime: a driver with Vulkan 1.3 (`vulkan-1.dll`).

## 1. Get the code

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
```
(`kur.ps1` creates `.venv` and installs `requirements.txt` itself in its `python` step.)

## 2. Path A: run the installer with the prebuilt engine (default)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```
Takes ~10 min (downloads ~3.7 GB). Run it in the background and poll the log if your tool has a timeout. Expected
marker lines, in order: `MODEL_OK`, `CUDA_OK`, `HAZIR_OK`, `PYTHON_OK`, `AYAR_OK`, `KONTROL_OK`, `KURULUM_OK`. The
script is idempotent: re-run it after a failure; verified downloads are skipped. The last step runs the engine's
`--list-devices` and fails loudly if no `CUDA:0` device is seen.

Steps can be run one at a time with `-Adim model,cuda,hazir,python,ayar,kontrol` (any subset, comma-separated). What each
step does and how to check it by hand:

| Step | Does | Check |
|---|---|---|
| `model` | downloads `voxcpm2-q8_0.gguf` from `https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/661a224e9d9adbd49c01626f85e426f5f425d771/VoxCPM2-GGUF/voxcpm2-q8_0.gguf` (pinned commit; the file on `main` was replaced on 2026-10-19 with a different build, 2 955 007 488 bytes, sha256 `8df1faf2…`, not verified with this engine) to `C:\vox\model\` | `(Get-FileHash C:\vox\model\voxcpm2-q8_0.gguf).Hash` = `C8E01AB4416011E12A28F24EDE298A1AA5CE64B43F8E8AAAD53B1E2FE7C96432`, size 2 955 000 480 bytes |
| `cuda` | downloads the CUDA 12.8.2 redist zips (cudart, cublas, cufft; with `-Derle` also nvcc, cccl; sha256 pinned in the script), merges them into `C:\vox\cuda\{bin,include,lib}`; no system install, PATH untouched | `cudart64_12.dll`, `cublas64_12.dll`, `cublasLt64_12.dll`, `cufft64_11.dll` exist in `C:\vox\cuda\bin` |
| `hazir` | downloads the release zip pinned in the script (`$REL_SURUM`, `$REL_ZIP_SHA`, `$REL_EXE_SHA`) from `https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/<version>/<zip>`, verifies both sha256, unpacks `audiocpp_cli.exe` (+ LICENSE, THIRD_PARTY.md, README.txt) into `C:\vox\motor\build\bin\` | `(Get-FileHash C:\vox\motor\build\bin\audiocpp_cli.exe).Hash` equals `$REL_EXE_SHA` in `scripts\kur.ps1` |
| `python` | finds a 64-bit Python 3.10+ (`py -3`, `python`, `python3`), creates `.venv` in the repo, `pip install -r requirements.txt` | `.venv\Scripts\python.exe -c "import numpy, soundfile; print('ok')"` → `ok` |
| `ayar` | writes `ayarlar.json` in the repo root with the paths above | `type ayarlar.json` shows `motor`, `model`, `cuda_bin` |
| `kontrol` | checks exe + DLLs, runs `audiocpp_cli.exe --list-devices` with `C:\vox\cuda\bin` on PATH | prints a `CUDA:0 "<GPU name>"` line, then `KONTROL_OK` |

Offline or testing a zip you already have: `-HazirZip <path>.zip` (the sha256 must still match the pinned one).

## 2b. Path B: build the engine from source

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Takes ~30-45 min (downloads ~4 GB, build ~15-25 min on 6 cores). Markers, in order: `MODEL_OK`, `CUDA_OK`, `KAYNAK_OK`,
`BUILD_OK`, `DERLE_OK`, `PYTHON_OK`, `AYAR_OK`, `KONTROL_OK`, `KURULUM_OK`. Extra steps:

| Step | Does | Check |
|---|---|---|
| `kaynak` | downloads audio.cpp v0.7.2 tarball (sha256 `cab8db31…6cbf`), extracts to `C:\vox\motor\src` with Windows' own `tar.exe`, applies `patches/0001-voxcpm2-4gb-ve-hiz.patch` with `git apply` | inside `C:\vox\motor\src`: `git apply --reverse --check <repo>\patches\0001-voxcpm2-4gb-ve-hiz.patch` exits 0 (patch is applied) |
| `derle` | `scripts\derle.ps1` → CMake + Ninja + nvcc (all from Build Tools / the CUDA zips), target `audiocpp_cli`, `-DCMAKE_CUDA_ARCHITECTURES=<Mimari>` | `C:\vox\motor\build\bin\audiocpp_cli.exe` exists (~34 MB for one architecture); log ends with `BUILD_OK` |

GPU architecture for the build: `-Mimari native` (default) compiles for the GPU in this PC. Explicit values: GTX 10xx → `61`,
RTX 20xx → `75`, RTX 30xx → `86`, RTX 40xx → `89`, RTX 50xx → `120`; a list like `"61-real;75-real;86-real;89;120"` builds
a multi-GPU exe (what the release uses; ~5× longer CUDA compile). Fewer cores / quieter PC: `-Paralel 2`.

## 3. Verify the engine sees the GPU

```powershell
$env:PATH = "C:\vox\cuda\bin;" + $env:PATH
C:\vox\motor\build\bin\audiocpp_cli.exe --list-devices
```
Expected: a line containing `CUDA:0` and your GPU name. If only `CPU` is listed, the CUDA DLLs are not on PATH or the
driver is too old.

## 4. Smoke test (uses the GPU, ~1-2 min)

```powershell
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
```
Expected: `Hazır sesler` followed by 14 voices: `hazir/anlatici_de` … `hazir/anlatici_zh` (language column `de` … `zh`)
and the 7 Turkish voices `hazir/belgesel_hanim` … `hazir/yasli_bilge` (`tr`).

```powershell
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin "Merhaba, bu bir deneme okumasıdır." --cikti cikti\ilk
```
Expected last line: `bitti: ~3 sn ses, ~60-90 sn, VRAM tepe < 3300 MB → ...\cikti\ilk\okuma.wav` (the first run encodes
the reference, ~50 s; later runs with the same voice take ~2 s per second of audio). `cikti\ilk\ozet.json` lists the
sentences with start/end times. Play `okuma.wav` (48 kHz mono) to confirm.

Design test (~1 min):
```powershell
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deneme --cesit 1 --tohum 42 --tarif "A calm Turkish woman in her forties with a warm, low voice, speaking slowly and clearly. Clean studio recording, no background noise." --metin "Merhaba, ben sakin sesli bir anlatıcıyım. Uzun yolculukları, eski şehirleri ve küçük insan hikâyelerini anlatmayı severim. Sesim yavaş ve sıcaktır; dinleyeni acele ettirmez, her cümleye nefes aldırır. Belgesellerde ve sesli kitaplarda yanınızdayım."
```
Expected: `çeşit 1: tohum 42, ~20-30 sn → ...\sesler\deneme\cesit_01` and `süre ~55 sn, VRAM tepe ~2800 MB`.

Other languages (tr, en, fr, de, es, ru, zh, ja tested): the language comes from the voice card (`dil`), `--dil` overrides.
```powershell
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
```
Expected: `bitti: ~11 sn ses, ...`. Offline unit tests (no GPU): `.venv\Scripts\python.exe -m unittest discover -s tests`
→ `OK`. To design and audition a voice with the user, follow `.claude/skills/ses-tasarimi/SKILL.md`.

## 5. Web UI

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
Expected: `Arayüz hazır: http://127.0.0.1:8765/`. It binds 127.0.0.1 only and does **not** open a browser: tell the
user to open that address (or open it for them). Another port: `--port 8800`. If the port is busy the server exits with
`Address already in use` instead of silently sharing it. API check: `curl.exe http://127.0.0.1:8765/api/sesler` → JSON
with `"hazir"` (7 items). Jobs run one at a time (`/api/is/<id>` → `durum` sirada/calisiyor/bitti/hata; on `hata` the
`iz` field holds the traceback). Stop with Ctrl+C.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Double-clicking `audiocpp_cli.exe` says `cudart64_12.dll` (or `cublas64_12.dll`) `was not found` | the exe is a command-line engine; the CUDA DLLs live in `C:\vox\cuda\bin` and are put on PATH by the Python package, not by Windows | never double-click it; run `kur.ps1` (puts exe, DLLs, model, settings in place), then `python -m ses_tasarim.arayuz` or `ses_tasarim.oku` |
| `bu kur.ps1 sürümünde hazır motor sha256'sı yok` | old checkout | `git pull` |
| `yerel zip sha256 tutmadı` / `exe sha256 tutmadı` | zip is not the pinned release build | download the pinned `$REL_SURUM` zip from Releases, or build (Path B) |
| `64-bit Python 3.10+ bulunamadı` | no real Python; the Store alias answers `python` | `winget install Python.Python.3.12`, new shell, re-run `-Adim python,ayar,kontrol` |
| `motor ekran kartını görmedi` (KONTROL) | driver < 570, GPU not CUDA, or a Maxwell/older card | update driver; check `nvidia-smi`; see "Supported GPUs" |
| `sha256 tutmadı` | partial or changed download | re-run `kur.ps1`; the `.part` file is deleted automatically |
| `yama uygulanamıyor` | source is not pristine v0.7.2, or patch converted to CRLF | delete `C:\vox\motor\src`, re-run `-Adim kaynak`; check `git config core.autocrlf` (patch must stay LF) |
| `yama sessizce atlandı` | `C:\vox` is inside another git repository | move `-Kok` outside any repo, or `git apply --directory=...` |
| nvcc `Could not open output file ...obj.d` or `C1083` | path too long | shorter `-Kok` (e.g. `C:\v`) |
| `cmake configure failed` with CUDA not found | `C:\vox\cuda\bin\nvcc.exe` missing or VS lacks CMake/Ninja | re-run `-Adim cuda`; add "C++ CMake tools for Windows" to Build Tools |
| `C2137` during build | NUL byte inside a patch | never edit the patch in an editor that inserts NUL; re-clone |
| `--list-devices` shows only CPU | CUDA DLLs not on PATH, driver < 570, or GPU arch mismatch | `cuda_bin` in `ayarlar.json`; update driver; Path B with the right `-Mimari` |
| First generation on an RTX card takes minutes before any output | the driver is JIT-compiling the PTX (exe has no native code for that GPU) | normal once; cached by the driver. For full speed build Path B with `-Mimari native` |
| `motor rc=...` and `GGML_ASSERT mem_buffer` | two GPU jobs at once or < 4.5 GB free RAM | run one job; close other GPU apps |
| `CapacityError` | a single line exceeds the KV budget | shorten the line (one sentence per line) |
| EOS missing (`şu satırlar düzgün bitmedi`) | sentence too long or odd punctuation | split the sentence; remove digits and quotes (write numbers in words) |
| `okunamayan işaret` | digits or quotes in text | write numbers in words (`iki bin yirmi altı`), remove quotes |
| Build is slow / PC freezes | all cores used | `-Paralel 4` (kur.ps1 / derle.ps1) or `derle.ps1 -DusukOncelik` |

## 6b. macOS (Apple Silicon, Metal)

No prebuilt engine: the installer builds it from source with Metal (~1 min). Details and measurements: `docs/mac.md`.

| Need | Check | If missing |
|---|---|---|
| Apple Silicon | `uname -m` → `arm64` | Intel Macs are untested |
| Xcode Command Line Tools + Metal compiler | `xcrun --sdk macosx --find metal` → a path | `xcode-select --install` (full Xcode also works) |
| cmake, Python 3.10-3.13 | `cmake --version`, `python3.12 --version` | `brew install cmake python@3.12` |

```bash
bash scripts/kur.sh            # root ~/vox; --kok <dir>; --adim model,kaynak,derle,python,ayar,kontrol
```
Expect `MODEL_OK`, `KAYNAK_OK`, `DERLE_OK`, `PYTHON_OK`, `AYAR_OK`, `KONTROL_OK` (with a `MTL:0 "Apple M…" [GPU]` line) and
finally `KURULUM_OK`. `ayarlar.json` gets `"backend": "metal"`, `"cuda_bin": ""`. Smoke test (step 4) works the same with
`.venv/bin/python`; the UI starts with `./baslat.command`. Determinism check: run the same reading twice, the two
`okuma.wav` files must have the same `shasum`.

## 7. Layout

```
ses_tasarim/      Python package: ayarlar (settings), okunus (text prep), motor (engine), tasarla (step 1), oku (step 2), arayuz (web UI)
hazir_sesler/     14 bundled synthetic voices (7 Turkish + anlatici_<en|fr|de|es|ru|zh|ja>): referans.flac + ses.json (+ ornek_okuma.mp3)
.claude/skills/ses-tasarimi/  Claude Code skill: design, reference-based audition, sentence-by-sentence reading (EN + TR)
docs/cok_dilli.md multilingual use, per-language commands, lessons
tests/            offline unit tests (python -m unittest discover -s tests)
patches/          0001-voxcpm2-4gb-ve-hiz.patch — audio.cpp v0.7.2 changes (LF, apply with git apply)
scripts/          kur.ps1 (installer: prebuilt or -Derle), derle.ps1 (build), release_zip.ps1 (packs a release zip)
ayarlar/          okunus_sozlugu.tsv pronunciation dictionary
docs/4gb.md       how it fits in 4 GB, measurements
docs/marka_sesi_rehberi.md   brand voice guide (prompt pattern, seeds, ethics)
docs/test_seti/cumleler.txt  shared Turkish test set (CC0; digit sentences need spelling out for this reader)
CONTRIBUTING.md   how to contribute (starter issues #5-#8, PR rules); SECURITY.md private reporting
.github/          ISSUE_TEMPLATE (install problem form, Discussions link), pull_request_template.md, dependabot.yml
ayarlar.example.json, requirements.txt, LICENSE (Apache-2.0), THIRD_PARTY.md, ETHICS.md
```

Questions: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions). Install failures:
[issue form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml).

## 8. Making a new release (maintainer)

1. Build the multi-GPU exe at a neutral, short path (the exe embeds source paths through `__FILE__`):
   `derle.ps1 -Kaynak E:\b\src -Build E:\b\bm -Cuda E:\b\cuda -Mimari "61-real;75-real;86-real;89;120"`.
2. Byte-scan the exe for personal paths (UTF-8 and UTF-16) → must be 0. `cuobjdump --list-elf` → sm_61/75/86/89/120a.
3. `scripts\release_zip.ps1 -Exe <exe> -Surum vX.Y.Z` → `dist\...zip`; copy `ZIP_SHA256` / `EXE_SHA256` into
   `kur.ps1` (`$REL_SURUM`, `$REL_ZIP`, `$REL_ZIP_SHA`, `$REL_EXE_SHA`), commit, tag, upload the zip to the GitHub Release.
4. Test on a clean root: `kur.ps1 -Kok <short> -HazirZip dist\...zip`, then after publishing without `-HazirZip`.

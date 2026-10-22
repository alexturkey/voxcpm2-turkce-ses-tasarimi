# AGENTS.md — step-by-step install for an AI coding agent (Claude Code, Codex, Cursor...)

This file is for an agent setting up the project on a **Windows 10/11 PC with an NVIDIA GPU (≥ 4 GB VRAM)**. Follow the
steps in order. Every step has a command, the expected output and a check. Do not skip a check. Turkish is fine for the
user-facing texts; commands are language-neutral. `CLAUDE.md` points here.

Hard rules for agents working in this repo:
- Quality settings are fixed: 16 steps, cfg 2.0 (`ses_tasarim/motor.py: FIXED`). Never lower them "for speed".
- One GPU job at a time. Do not run two engine processes concurrently (`GGML_ASSERT mem_buffer`).
- No audio upload / real-voice cloning feature. See `ETHICS.md`. Do not add one.
- Keep install paths short (`C:\vox`). Long paths break nvcc at the 260-character limit.
- `patches/*.patch` are LF. Never convert them to CRLF (`.gitattributes` protects them).
- Do not commit `ayarlar.json`, `sesler/`, `onbellek/`, models or build output (see `.gitignore`).

## 0. Prerequisites (check, install what is missing)

| Need | Check command | Expected | If missing |
|---|---|---|---|
| NVIDIA driver ≥ 570 (CUDA 12.8 runtime) | `nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader` | e.g. `NVIDIA GeForce GTX 1050 Ti, 581.29, 4096 MiB` | update the driver (admin) |
| Git | `git --version` | `git version 2.x` | `winget install Git.Git` |
| Python 3.10–3.13 (64-bit) | `python --version` | `Python 3.1x` | `winget install Python.Python.3.12` |
| curl, tar (built into Windows 10 1803+) | `curl.exe --version`, `tar.exe --version` | version lines | update Windows |
| Visual Studio 2022 Build Tools with **Desktop development with C++** (MSVC v143, Windows SDK, **C++ CMake tools for Windows**) | `"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath` | a path like `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools` | `winget install Microsoft.VisualStudio.2022.BuildTools --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"` (needs admin, ~7 GB) |
| Disk | `fsutil volume diskfree C:` | ≥ 12 GB free | model 2.95 GB + CUDA 1.4 GB (zips 0.9 GB) + build 0.4 GB + source 0.1 GB |
| RAM | ≥ 8 GB total, ≥ 4.5 GB free when generating | – | – |

Known-good toolchain: VS 2022 17.14 (MSVC 14.44), CUDA 12.8.2 redist, Windows 10 22H2, driver 581.29. CUDA 13 does
**not** support Pascal (GTX 10xx); CUDA 11.8 does not build with MSVC 14.44. This is why the installer pins CUDA 12.8.

## 1. Get the code

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```
Check: `.venv\Scripts\python.exe -c "import numpy, soundfile; print('ok')"` → `ok`.

## 2. Run the installer (downloads, verifies sha256, patches, builds, writes `ayarlar.json`)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```
Takes ~30-45 min (downloads ~4 GB, build ~15-25 min). Run it in the background and poll the log if your tool has a
timeout. Expected marker lines, in order: `MODEL_OK`, `CUDA_OK`, `KAYNAK_OK`, `BUILD_OK`, `DERLE_OK`, `AYAR_OK`, `KURULUM_OK`.
The script is idempotent: re-run it after a failure; verified downloads are skipped.

Steps can be run one at a time with `-Adim model` / `cuda` / `kaynak` / `derle` / `ayar`. What each step does and how to
check it by hand:

| Step | Does | Check |
|---|---|---|
| `model` | downloads `voxcpm2-q8_0.gguf` from `https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/main/VoxCPM2-GGUF/voxcpm2-q8_0.gguf` to `C:\vox\model\` | `(Get-FileHash C:\vox\model\voxcpm2-q8_0.gguf).Hash` = `C8E01AB4416011E12A28F24EDE298A1AA5CE64B43F8E8AAAD53B1E2FE7C96432`, size 2 955 000 480 bytes |
| `cuda` | downloads 5 CUDA 12.8.2 redist zips (cudart, cublas, cufft, nvcc, cccl; sha256 pinned in the script), merges them into `C:\vox\cuda\{bin,include,lib,nvvm}`; no system install, PATH untouched | `C:\vox\cuda\bin\nvcc.exe --version` → `Cuda compilation tools, release 12.8`; `cudart64_12.dll`, `cublas64_12.dll`, `cublasLt64_12.dll`, `cufft64_11.dll` exist in `C:\vox\cuda\bin` |
| `kaynak` | downloads audio.cpp v0.7.2 tarball (sha256 `cab8db31…6cbf`), extracts to `C:\vox\motor\src`, applies `patches/0001-voxcpm2-4gb-ve-hiz.patch` | inside `C:\vox\motor\src`: `git apply --reverse --check <repo>\patches\0001-voxcpm2-4gb-ve-hiz.patch` exits 0 (patch is applied) |
| `derle` | `scripts\derle.ps1` → CMake + Ninja + nvcc, target `audiocpp_cli`, `-DCMAKE_CUDA_ARCHITECTURES=61` | `C:\vox\motor\build\bin\audiocpp_cli.exe` exists (~34 MB); log ends with `BUILD_OK` |
| `ayar` | writes `ayarlar.json` in the repo root with the paths above | `type ayarlar.json` shows `motor`, `model`, `cuda_bin` |

GPU architecture: GTX 10xx → `-Mimari 61` (default). RTX 20xx → 75, RTX 30xx → 86, RTX 40xx → 89. Pass it to `kur.ps1`.

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
Expected: `Hazır sesler` followed by 7 voices (`hazir/belgesel_hanim` … `hazir/yasli_bilge`).

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

## 5. Web UI

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
Expected: `Arayüz hazır: http://127.0.0.1:8765/`. It binds 127.0.0.1 only and does not open a browser. API check:
`curl.exe http://127.0.0.1:8765/api/sesler` → JSON with `"hazir"` (7 items). Stop with Ctrl+C.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `sha256 tutmadı` | partial or changed download | re-run `kur.ps1`; the `.part` file is deleted automatically |
| `yama uygulanamıyor` | source is not pristine v0.7.2, or patch converted to CRLF | delete `C:\vox\motor\src`, re-run `-Adim kaynak`; check `git config core.autocrlf` (patch must stay LF) |
| `yama sessizce atlandı` | `C:\vox` is inside another git repository | move `-Kok` outside any repo, or `git apply --directory=...` |
| nvcc `Could not open output file ...obj.d` or `C1083` | path too long | shorter `-Kok` (e.g. `C:\v`) |
| `cmake configure failed` with CUDA not found | `C:\vox\cuda\bin\nvcc.exe` missing or VS lacks CMake/Ninja | re-run `-Adim cuda`; add "C++ CMake tools for Windows" to Build Tools |
| `C2137` during build | NUL byte inside a patch | never edit the patch in an editor that inserts NUL; re-clone |
| `--list-devices` shows only CPU | CUDA DLLs not on PATH, driver < 570, or GPU arch mismatch | `cuda_bin` in `ayarlar.json`; update driver; rebuild with the right `-Mimari` |
| `motor rc=...` and `GGML_ASSERT mem_buffer` | two GPU jobs at once or < 4.5 GB free RAM | run one job; close other GPU apps |
| `CapacityError` | a single line exceeds the KV budget | shorten the line (one sentence per line) |
| EOS missing (`şu satırlar düzgün bitmedi`) | sentence too long or odd punctuation | split the sentence; remove digits and quotes (write numbers in words) |
| `okunamayan işaret` | digits or quotes in text | write numbers in words (`iki bin yirmi altı`), remove quotes |
| Build is slow / PC freezes | all cores used | `-Paralel 4` (kur.ps1 / derle.ps1) or `derle.ps1 -DusukOncelik` |

## 7. Layout

```
ses_tasarim/      Python package: ayarlar (settings), okunus (text prep), motor (engine), tasarla (step 1), oku (step 2), arayuz (web UI)
hazir_sesler/     7 bundled synthetic voices: referans.flac + ses.json (+ ornek_okuma.mp3)
patches/          0001-voxcpm2-4gb-ve-hiz.patch — audio.cpp v0.7.2 changes (LF, apply with git apply)
scripts/          kur.ps1 (installer), derle.ps1 (build)
ayarlar/          okunus_sozlugu.tsv pronunciation dictionary
docs/4gb.md       how it fits in 4 GB, measurements
ayarlar.example.json, requirements.txt, LICENSE (Apache-2.0), THIRD_PARTY.md, ETHICS.md
```

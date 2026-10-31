# Ubuntu / Linux (NVIDIA CUDA)

**TR:** Bu yol yamalı audio.cpp motorunu Linux için kaynaktan derler. Windows `.exe`/DLL paketlerini kullanmaz.
Kalite aynı: 16 adım, cfg 2.0. Kurulum betiği sudo çalıştırmaz; eksik sistem paketlerini yönetici kurmalıdır.
Arayüz yalnız `127.0.0.1` adresindedir. Uzak sunucuda SSH tüneli kullanın; Host kontrolünü kapatmayın.

**EN:** Build the patched audio.cpp engine from source for Linux; Windows binaries are not used.
Quality stays at 16 steps, cfg 2.0. The installer never invokes sudo. The administrator installs missing system
packages first. The UI remains loopback-only, with its existing Host checks; use SSH forwarding for a remote server.

## Native installation

Requirements: x86-64 Linux, NVIDIA GPU with at least 4 GB VRAM, a driver compatible with the installed CUDA toolkit,
CUDA toolkit including `nvcc` (CUDA 12.8 is the reference version), CMake 3.24+, a toolkit-supported C++ compiler,
Git, curl, sha256sum, tar, and 64-bit Python 3.10–3.13 with venv. A working NVIDIA driver alone does not include nvcc.
Keep at least 12 GB free for the model, source and build files; the CUDA toolkit needs additional space.

On Ubuntu 24.04, install the non-CUDA dependencies:

```bash
sudo apt-get update
sudo apt-get install build-essential cmake git curl ca-certificates python3 python3-venv libsndfile1
```

Install the CUDA toolkit using NVIDIA's instructions for your distribution. Verify `nvcc --version` and
`nvidia-smi`; place nvcc on PATH and make the toolkit's shared libraries visible to the system loader.
Use a Python 3.10–3.13 environment or the Docker path below on distributions shipping a newer Python.

```bash
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur-linux.sh
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -m ses_tasarim.oku --liste
.venv/bin/python -m ses_tasarim.oku --ses hazir/belgesel_hanim \
  --metin "Merhaba, bu bir deneme okumasıdır." --cikti cikti/ilk
.venv/bin/python -m ses_tasarim.arayuz
```

Open `http://127.0.0.1:8765/`. The first reading encodes the reference; later readings reuse its disk cache.
Do not start another CLI engine while a UI job is running. Inspect `cikti/ilk/okuma.wav` and `ozet.json` after the test.

Options: `--kok ~/vox` (engine/model root), `--paralel 4`, `--mimari native` (default, local GPU),
`--mimari 86` (RTX 30xx), `--mimari 61` (GTX 10xx), `--adim model,kaynak,derle,python,ayar,kontrol` (any subset).
The source and model use the same pinned URLs and SHA256 hashes as the existing installers. Re-running verifies
downloads, checks that the patch is applied, and preserves user settings with a timestamped backup before updating paths.
Success markers: `MODEL_OK`, `KAYNAK_OK`, `DERLE_OK`, `PYTHON_OK`, `AYAR_OK`, `KONTROL_OK`, `KURULUM_OK`.

## Docker (Linux host)

Requires Docker, a compatible NVIDIA driver and NVIDIA Container Toolkit already configured on the host.
The image uses Ubuntu 24.04, Python 3.12 and CUDA 12.8.1, including the build tools. No host Python or host nvcc is needed.
Building downloads the pinned audio.cpp source and Python dependencies; first startup downloads the pinned 2.95 GB model.

```bash
# Default architecture 86 targets RTX 30xx. Override for your GPU (e.g. 61 for GTX 10xx, 89 for RTX 40xx).
docker build -f Dockerfile.linux --build-arg CUDA_ARCHITECTURES=86 -t voxcpm2-linux .
docker run --rm --gpus all --network host \
  -v voxcpm2-data:/data voxcpm2-linux
```

Do not use `-p 8765:8765`: the application intentionally listens on loopback inside the network namespace.
Linux host networking preserves that loopback binding. Model files, voices and caches persist in `voxcpm2-data`.
The engine exits after each batch; it does not keep a model process loaded between jobs.

### Windows 10/11 with Docker Desktop (WSL2 backend)

The GPU is passed through to the container (`--gpus all`), so the CLI works the same as on Linux. Build for your card
(example: GTX 10xx = `61`) and run reading or design as one-off commands; the command below runs the image's own model step
(the pinned model is downloaded into the mounted folder, here `C:\vox\data`; in our test the model was already there, so
the download itself was not exercised):

```powershell
docker build -f Dockerfile.linux --build-arg CUDA_ARCHITECTURES=61 -t voxcpm2-linux .
docker run --rm --gpus all -v C:\vox\data:/data voxcpm2-linux bash -c "bash scripts/kur-linux.sh --kok /data --adim model && python -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin 'Merhaba, bu bir deneme okumasıdır.' --cikti /data/cikti/ilk"
```

The result is `C:\vox\data\cikti\ilk\okuma.wav`. Design works the same way with `python -m ses_tasarim.tasarla ...`.
**The web UI does not open from Windows this way.** It listens on `127.0.0.1` inside the container, and neither
`--network host` nor `-p 127.0.0.1:8765:8765` made `http://127.0.0.1:8765/` reachable from the Windows side (both
returned no response in our test; we did not try Docker Desktop's separate host-networking setting). On Windows use the
native installer for the UI (`scripts\kur.ps1`, see the README quick start).

For a remote server, run this **on your client computer** and leave it open:

```bash
ssh -N -L 8765:127.0.0.1:8765 user@server
```

Then open `http://127.0.0.1:8765/` on the client. No reverse proxy, authentication changes, or public port is needed.

## Validation scope

### Tested configuration (2026-10-31, Europe/Istanbul)

Host: Ubuntu 26.04.1 x86-64, Intel i5-12400F, 30 GiB RAM, NVIDIA RTX 3060 Ti 8 GiB,
driver 595.99.02, Docker 29.9.2. Container: Ubuntu 24.04, CUDA 12.8.1 (nvcc 12.8.93),
GCC 13.3, Python 3.12, numpy 2.2.6, soundfile 0.14.0. Architecture: `86`.

`docker build -f Dockerfile.linux --build-arg CUDA_ARCHITECTURES=86 -t voxcpm2-linux .`
completed successfully; `docker run --rm --network none voxcpm2-linux python -m unittest discover -s tests`
passed all 42 tests. GPU inference also ran without network access using the previously verified model.

| Test | Audio duration | Engine sequence time | Peak GPU memory (total) |
|---|---:|---:|---:|
| `hazir/belgesel_hanim`, first reference encoding | 2.56 s | 24.0 s | 3057 MiB |
| Same text/voice/seed, cached reference | 2.56 s | 6.0 s | 3057 MiB |
| New voice design, seed 42 (AGENTS.md design test) | 16.64 s | 12.4 s | 2965 MiB |
| Reading with that newly designed voice | 3.04 s | 21.0 s | 2943 MiB |

Reading text: `Merhaba, bu bir deneme okumasıdır.` Quality: 16 steps, CFG 2.0 throughout.
Both bundled-voice readings produced the same WAV SHA256:
`9919e687e447a07cd508774deee12b30530602dfbac2be650270f88823fc15df`.
GPU memory returned to its 77 MiB baseline after each bundled-voice reading and at the end of the sequence.
The reading outputs were non-silent, finite, mono 48 kHz WAVs; these checks do not assess pronunciation or subjective quality.
Times include engine/model startup and reference encoding when needed; they are short smoke tests, not throughput benchmarks.
No other model was loaded on the GPU during these measurements.

### Tested configuration 2 (2026-10-31, Europe/Istanbul): 4 GB card

Host: Windows 10 (Docker Desktop, WSL2 backend), Intel i7-7700HQ, NVIDIA GTX 1050 Ti 4 GiB (compute capability 6.1),
driver 581.29, Docker 29.1.2. Container: Ubuntu 24.04, CUDA 12.8.1. Architecture: `61`:
`docker build -f Dockerfile.linux --build-arg CUDA_ARCHITECTURES=61 -t voxcpm2-linux .` completed (about 20 minutes).
The engine listed `CUDA:0 "NVIDIA GeForce GTX 1050 Ti"`. The model was supplied from a folder that already held the
verified file (same SHA256, the installer skipped the download). Quality: 16 steps, CFG 2.0 throughout.

| Test | Audio duration | Engine sequence time | Peak GPU memory (total) |
|---|---:|---:|---:|
| `hazir/belgesel_hanim`, first reference encoding | 2.56 s | 101.0 s (77.0 s on a second cold run) | 2849 MiB |
| Same text/voice/seed, cached reference | 2.56 s | 44.1 s | 2849 MiB |
| New voice design, seed 42, 1 variant | 4.48 s | 36.4 s | 2673 MiB |
| Reading with that newly designed voice | 2.56 s | 72.5 s | 2619 MiB |

Reading text: `Merhaba, bu bir deneme okumasıdır.` The cold and cached bundled-voice readings produced the same WAV SHA256
(also a third run on a fresh data folder): `485143b3cee8a745fe8ea7b64f9e4bf65c2cd1dc8fb662cf5594f819318ddf85`.
GPU memory was 0 MiB before the runs and after the last one; an independent `nvidia-smi` sampler
(0.4 s interval) saw the same 2849 MiB peak as the engine. The outputs were finite, mono, 48 kHz WAVs and not silent.
Speed on this machine: the same reading with the native Windows engine took 79.3 s cold and 18.5 s with the reference cached
(same 2849 MiB peak), so WSL2 Docker was about 2.4x slower for the cached reading and about 1.0-1.3x for the cold one
(single runs each, not benchmarks). The Windows and Docker WAVs differ (different build/OS); bit-identical output across
operating systems is not claimed.

Note on older cards: CUDA 12.8.1 still builds `sm_61` (Pascal). A newer toolkit may drop old architectures, so keep the
image pinned to 12.8.1 for GTX 10xx and check NVIDIA's release notes before changing it.

Linux support is initially experimental. A successful test on one GPU/distribution is not a guarantee for all
Ubuntu versions or CUDA architectures. Include the host OS, container OS (if used), driver, toolkit, GPU, commands,
timings, peak VRAM and whether memory returns after the engine exits when reporting results.
Keep generated audio, model files and build outputs out of pull requests.

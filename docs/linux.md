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
`--mimari 86` (RTX 30xx), `--adim model,kaynak,derle,python,ayar,kontrol` (any subset).
The source and model use the same pinned URLs and SHA256 hashes as the existing installers. Re-running verifies
downloads, checks that the patch is applied, and preserves user settings with a timestamped backup before updating paths.
Success markers: `MODEL_OK`, `KAYNAK_OK`, `DERLE_OK`, `PYTHON_OK`, `AYAR_OK`, `KONTROL_OK`, `KURULUM_OK`.

## Docker (Linux host)

Requires Docker, a compatible NVIDIA driver and NVIDIA Container Toolkit already configured on the host.
The image uses Ubuntu 24.04, Python 3.12 and CUDA 12.8.1, including the build tools. No host Python or host nvcc is needed.
Building downloads the pinned audio.cpp source and Python dependencies; first startup downloads the pinned 2.95 GB model.

```bash
# Default architecture 86 targets RTX 30xx. Override for your GPU (e.g. 89 for RTX 40xx).
docker build -f Dockerfile.linux --build-arg CUDA_ARCHITECTURES=86 -t voxcpm2-linux .
docker run --rm --gpus all --network host \
  -v voxcpm2-data:/data voxcpm2-linux
```

Do not use `-p 8765:8765`: the application intentionally listens on loopback inside the network namespace.
Linux host networking preserves that loopback binding. Model files, voices and caches persist in `voxcpm2-data`.
The engine exits after each batch; it does not keep a model process loaded between jobs.

For a remote server, run this **on your client computer** and leave it open:

```bash
ssh -N -L 8765:127.0.0.1:8765 user@server
```

Then open `http://127.0.0.1:8765/` on the client. No reverse proxy, authentication changes, or public port is needed.

## Validation scope

Linux support is initially experimental. A successful test on one GPU/distribution is not a guarantee for all
Ubuntu versions or CUDA architectures. Include the host OS, container OS (if used), driver, toolkit, GPU, commands,
timings, peak VRAM and whether memory returns after the engine exits when reporting results.
Keep generated audio, model files and build outputs out of pull requests.

# voxcpm2-turkce-ses-tasarimi

**Turkish voice design with VoxCPM2 on a 4 GB GPU.** Describe a voice in English, let the model create it, pick the
variant you like, then read any Turkish text with that voice. Includes a one-command installer, a patched
[audio.cpp](https://github.com/0xShug0/audio.cpp) engine that fits a GTX 1050 Ti (4 GB), a tiny local web UI and seven
ready-made synthetic voices.

[Türkçe README](README.tr.md) · [How it fits in 4 GB](docs/4gb.md) · [Install guide for AI agents](AGENTS.md) · [Responsible use](ETHICS.md)

> Every voice here is synthetic: designed from a text description, never recorded from or cloned off a real person.
> Label what you generate as AI-generated. No audio upload, no voice cloning of real people.

## How it works

1. **Voice design.** An English *voice description* + a Turkish *text read while the voice is created* + a number of
   variants. Each variant gets its own seed; the engine receives `(description)text` and returns a 20-35 s design
   recording per seed.
2. **Reference-based reading.** The design recording is passed to **both** engine inputs (`audio` and `voice_ref`),
   together with its transcript (`reference_text`) and the new text to read, with the same seed. The voice is carried by
   the recording, not by the description, so it does not drift from text to text. Text is read sentence by sentence.
3. Quality is fixed: 16 diffusion steps, CFG 2.0. The seed is not a quality knob.

The engine is audio.cpp v0.7.2 with our patch (`patches/`), the model is VoxCPM2 Q8_0 GGUF. Peak VRAM ≈ 2.8 GB;
about 2 s of compute per 1 s of speech on a GTX 1050 Ti. Details and measurements: [docs/4gb.md](docs/4gb.md).

## Bundled voices (`hazir_sesler/`)

All seven were designed from the prompts stored in their `ses.json`; none is a real person.

| Voice | Short description | Listen |
|---|---|---|
| `belgesel_hanim` | Mature woman in her fifties, deep warm alto; calm documentary narrator | [sample](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [reference](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Deep, powerful, mysterious male narrator | [sample](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Seasoned news anchor around seventy, calm and authoritative | [sample](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [reference](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Charismatic evening-news anchor in her thirties, velvety and expressive | [sample](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [reference](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Fairy-tale witch: low, slightly nasal, slyly sweet | [sample](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [reference](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Exceptionally deep, dense, commanding male narrator | [sample](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [reference](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Old wise man, deep and booming, slightly mysterious | [sample](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/yasli_bilge/referans.flac) |

Each folder: `referans.flac` (lossless design recording), `ses.json` (prompt, transcript, design seed, reading seed,
description), `ornek_okuma.mp3` (+ its text). Use them directly: `--ses hazir/<name>`.

## Install (Windows 10/11, NVIDIA GPU ≥ 4 GB)

Prerequisites: NVIDIA driver ≥ 570, Git, Python 3.10+, Visual Studio 2022 Build Tools with "Desktop development with C++"
(incl. C++ CMake tools). Exact checks and fixes: [AGENTS.md](AGENTS.md).

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
python -m venv .venv && .venv\Scripts\python.exe -m pip install -r requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

`kur.ps1` downloads the model (2.95 GB, sha256-verified), the CUDA 12.8 runtime + compiler as portable zips (no system
install, PATH untouched), the audio.cpp v0.7.2 source, applies the patch, builds `audiocpp_cli.exe` (~15-25 min) and
writes `ayarlar.json`. Keep the root short (`C:\vox`): nvcc fails on long paths. Other GPUs: `-Mimari 75/86/89`.

Prebuilt engine: see the Releases page for a zip with `audiocpp_cli.exe` (GTX 10xx / sm_61, CUDA 12.8). You still need
the CUDA DLLs (`kur.ps1 -Adim cuda`) and the model (`-Adim model`).

## Use

Command line:
```powershell
# list voices
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# read with a bundled voice (one sentence per line; "|| paragraf" = longer pause)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# design a new voice: 3 variants, 3 seeds
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# read with variant 2 of it
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
```
Text rules: write numbers in words, no quotation marks (the tool refuses digits and quotes), one sentence per line,
≤ 2000 characters per line. `ayarlar/okunus_sozlugu.tsv` fixes pronunciations of foreign words.

Web UI (local only, 127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → open the printed address.
Three boxes (description, creation text, text to read) + variant count. *Design* → listen to the variants → pick one →
*Read with this voice* → download. Or pick a bundled voice and read.

## License and credits

Code and bundled voices: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Built on VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) and the audio.cpp GGUF conversion. Full list: [THIRD_PARTY.md](THIRD_PARTY.md).
Not affiliated with OpenBMB, ModelBest or the audio.cpp project.

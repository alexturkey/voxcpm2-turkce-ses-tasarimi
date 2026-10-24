# voxcpm2-turkce-ses-tasarimi

**Turkish voice design with VoxCPM2 on a 4 GB GPU.** Describe a voice in English, let the model create it, pick the
variant you like, then read any Turkish text with that voice. Includes a one-command installer, a patched
[audio.cpp](https://github.com/0xShug0/audio.cpp) engine that fits a GTX 1050 Ti (4 GB), a tiny local web UI and fourteen
ready-made synthetic voices: seven Turkish and seven native narrators in English, French, German, Spanish,
Russian, Chinese and Japanese (8 languages in total).

[Türkçe README](README.tr.md) · [How it fits in 4 GB](docs/4gb.md) · [macOS](docs/mac.md) · [Install guide for AI agents](AGENTS.md) · [Responsible use](ETHICS.md)

> The bundled voices are synthetic, designed from a text description. The voice cloning section is only for your own
> voice or a voice used with its owner's explicit permission; the UI asks you to confirm that permission. Impersonation,
> fraud and deception are prohibited. Label what you generate as AI-generated. See [ETHICS.md](ETHICS.md).

## Multilingual: 8 languages, native narrators, sentence-by-sentence consistency

We made one Cappadocia documentary video in 8 languages: Turkish, English, French, German, Spanish, Russian, Chinese
and Japanese. Each language has its own **native narrator**, designed with VoxCPM2 from an English description. All of
it was generated fully locally on a 4 GB GTX 1050 Ti, with the same fixed quality (16 steps, cfg 2.0). The seven
narrators are bundled here, with their prompt, design text, seed and reference recording.

| Code | Language | Voice | Listen | Video |
|---|---|---|---|---|
| `tr` | Turkish | `hazir/belgesel_hanim` (and 6 more) | [sample](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | English | `hazir/anlatici_en` | [sample](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | French | `hazir/anlatici_fr` | [sample](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | German | `hazir/anlatici_de` | [sample](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Spanish | `hazir/anlatici_es` | [sample](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Russian | `hazir/anlatici_ru` | [sample](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Chinese (Mandarin) | `hazir/anlatici_zh` | [sample](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Japanese | `hazir/anlatici_ja` | [sample](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language comes from the voice card; --dil overrides it
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Why sentence by sentence.** VoxCPM2 is not stable for a single long generation (roughly above 30 seconds): the rhythm
speeds up and the voice can drift. Here the voice is carried by a fixed reference recording and seed, and long text is
read one sentence per line, so timbre and style stay the same from the first sentence to the last. For languages other
than Turkish the Turkish pronunciation dictionary is not applied. Other languages VoxCPM2 supports should work with
`--dil <code>`; we have not tested them. Per-language commands and the lessons we learned:
[docs/cok_dilli.md](docs/cok_dilli.md). Claude Code skill for the whole design flow:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

## Quick start (Windows, 3 steps)

1. **Download** the code: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   The ready-made engine package for your card is fetched by the installer in step 3:
   NVIDIA → [CUDA package](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan package, experimental](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (already downloaded one? add `-HazirZip <path to the zip>` to the command below).
2. **Extract** the zip, open the `voxcpm2-turkce-ses-tasarimi-main` folder, type `powershell` in the Explorer address
   bar and press Enter.
3. **Run** the installer (needs 64-bit Python 3.10–3.13; NVIDIA driver ≥ 570 for CUDA), then double-click **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: add `-Vulkan` at the end. The UI opens at http://127.0.0.1:8765/.

The engine zip is not a standalone app (its exe needs the model and DLLs that the installer sets up). Details, GPU
list and common problems: "Quick install" below.

## Quick start (macOS, Apple Silicon)

Needs Xcode Command Line Tools (`xcode-select --install`) and [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
The installer downloads the model, builds the patched engine with Metal (~1 min) and sets everything up under `~/vox`.
Then double-click **`baslat.command`**. On a MacBook Air M4 16 GB: ~2 s of compute per 1 s of speech, same seed gives
byte-identical audio, peak ~5.3 GB RAM, no thermal slowdown over 12 min of continuous reading. Details and
measurements: [docs/mac.md](docs/mac.md).

**Native Mac app (no Python, Homebrew or Terminal):** [macos/README.md](macos/README.md). It bundles the same
patched engine and downloads the model on first launch; for now it is built from source with Xcode.

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

All fourteen were designed from the prompts stored in their `ses.json`; none was cloned from a recording (cloning is the
separate, consent-gated section 3).

| Voice | Short description | Listen |
|---|---|---|
| `belgesel_hanim` | Mature woman in her fifties, deep warm alto; calm documentary narrator | [sample](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [reference](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Deep, powerful, mysterious male narrator | [sample](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Seasoned news anchor around seventy, calm and authoritative | [sample](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [reference](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Charismatic evening-news anchor in her thirties, velvety and expressive | [sample](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [reference](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Fairy-tale witch: low, slightly nasal, slyly sweet | [sample](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [reference](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Exceptionally deep, dense, commanding male narrator | [sample](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [reference](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Old wise man, deep and booming, slightly mysterious | [sample](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Native English male documentary narrator in his fifties (General American); deep, calm, warm | [sample](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Native French male documentary narrator in his fifties (Parisian); deep, calm, warm | [sample](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Native German male documentary narrator in his fifties (Hochdeutsch); deep, calm, warm | [sample](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Native Spanish male documentary narrator in his fifties (Castilian (Madrid)); deep, calm, warm | [sample](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Native Russian male documentary narrator in his fifties (Moscow); deep, calm, warm | [sample](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Native Chinese (Mandarin) male documentary narrator in his fifties (Beijing Putonghua); deep, calm, warm | [sample](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Native Japanese male documentary narrator in his fifties (Tokyo standard); deep, calm, warm | [sample](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ja/referans.flac) |

Each folder: `referans.flac` (lossless design recording), `ses.json` (prompt, transcript, design seed, reading seed,
description; `dil` = language for the narrators), `ornek_okuma.mp3` (+ its text). Use them directly: `--ses hazir/<name>`.
The narrators' reference recordings are short (5.6-10 s); their samples are the first three sentences of the
Cappadocia script, cut from the full production reading.

## Quick install, no compiler needed (Windows 10/11, NVIDIA GPU ≥ 4 GB)

Prerequisites: NVIDIA driver ≥ 570 and 64-bit Python 3.10–3.13 (`winget install Python.Python.3.12`). Nothing else:
no Visual Studio, no CUDA installer. Not sure which card you have? Run `nvidia-smi` in PowerShell: it prints the GPU
name, driver version and memory. No NVIDIA card? See "AMD / Intel" below.

With [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Without Git: on this page click **Code → Download ZIP**, extract it, open the extracted
`voxcpm2-turkce-ses-tasarimi-main` folder, type `powershell` in the Explorer address bar and press Enter, then run the
last line above. Git is only needed for the build-from-source path.

`-ExecutionPolicy Bypass` applies to this one process only and changes no system setting; read `scripts\kur.ps1`
before running it, as with any installer script. One command, ~10 min, ~3.7 GB download, everything sha256-verified: the model (2.95 GB), the CUDA 12.8 runtime DLLs as
portable zips (no system install, PATH untouched), the **prebuilt engine** from the Releases page, a `.venv` with the two
Python packages, `ayarlar.json`, and a final GPU check (`KONTROL_OK`). Re-run it after any failure; verified files are
skipped. Then start the web UI: double-click **`baslat.bat`** in the repo folder. It starts the UI and opens
**http://127.0.0.1:8765/** in your browser when it is ready; close the black window (or press Ctrl+C there) to stop it.
The same from PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
then open **http://127.0.0.1:8765/** yourself (started this way the UI does not open the browser; it listens on
localhost only).

> **The `audiocpp_cli.exe` in the release zip is not meant to be double-clicked.** It is a command-line engine that
> needs the CUDA DLLs and the model next to it; `kur.ps1` puts everything in place and the Python package drives it.
> Double-clicking it only shows "cudart64_12.dll not found".

**Supported GPUs (release v0.1.1):** native code for GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) and RTX 50xx (sm_120a); any other CUDA GPU from Pascal on runs the embedded PTX via the driver (slower first
start). Maxwell (GTX 9xx) and older are not supported by CUDA 12.8. Tested on a GTX 1050 Ti 4 GB only; reports from
other cards are welcome in [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (experimental):** a separate Vulkan engine zip (`…-win64-vulkan.zip`, no CUDA) installs with
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. It is verified only on our NVIDIA card through the Vulkan backend (there it ran
slower than CUDA but gave the same audio for the same seed; that measurement was taken while the disk was busy with
another job, so a clean speed comparison is still pending) and has **not** been tried on AMD or Intel hardware: if you try it,
please post the result in Discussions. With more than one Vulkan device (integrated + discrete) the installer writes
the discrete GPU's index as `cihaz` into `ayarlar.json`.

### Alternative: build the engine from source

Needs Visual Studio 2022 Build Tools with "Desktop development with C++" (incl. C++ CMake tools), ~7 GB. Then:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
This also downloads nvcc, fetches the audio.cpp v0.7.2 source, applies `patches/0001-voxcpm2-4gb-ve-hiz.patch` and
builds for your GPU (`-Mimari native`, default; or e.g. `-Mimari 61`), ~15-25 min. Keep the root short (`C:\vox`):
nvcc fails on long paths. Step-by-step with checks: [AGENTS.md](AGENTS.md).

### Common install problems

| You see | What it means, what to do |
|---|---|
| `cudart64_12.dll not found` after double-clicking the exe | The engine is not meant to be started by hand. Run the `kur.ps1` command above, then start the web UI. |
| `64-bit Python 3.10+ bulunamadı` (Python not found) | Install Python (`winget install Python.Python.3.12`), close PowerShell, open a new one and run the same command again. |
| `motor ekran kartını görmedi` (the engine did not see the GPU) | Update the NVIDIA driver to 570 or newer; check that `nvidia-smi` runs. |
| `indirme başarısız` / `sha256 tutmadı` (download failed / checksum mismatch) | Usually an interrupted download. Run the same command again; verified files are skipped. |
| Build path: `nvcc` fails | Keep the install root short (`-Kok C:\vox`). |
| The page does not open | Start the UI with `baslat.bat`, or open http://127.0.0.1:8765/ yourself. Port busy? Change `"port"` in `ayarlar.json`. |

Problems? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) or an
[install issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
with your GPU, Windows version, the command and its last lines.

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
≤ 2000 characters per line. `ayarlar/okunus_sozlugu.tsv` fixes pronunciations of foreign words in Turkish text.
Other languages: `--dil <code>` (or the voice card's `dil`); apostrophes are allowed there, the Turkish dictionary is
skipped, digits are still refused. If a reading prints `speed gate: satır [...]`, listen to those lines.

Web UI (local only, 127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → open http://127.0.0.1:8765/
yourself (another port: `--port 8800`). Three boxes (description, creation text, text to read) + variant count.
*Design* → listen to the variants → pick one → *Read with this voice* → download. Or pick a bundled voice and read.
Stop the server with Ctrl+C.

**Voice cloning (your own or a consented voice).** In section 3 of the UI, provide your recording (wav/mp3/flac/ogg, 5-30 s of clean speech advised; under 3 s is rejected, over 36 s is trimmed), its exact transcript and the text to read. The button stays disabled until you tick "This voice is mine or I have the owner's explicit permission". The recording goes only to the local server (127.0.0.1), is processed in a temp folder together with its reference encoding, and that folder is deleted when the job ends, also when it fails; nothing is sent over the network. Only the synthetic output is kept (UI: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Output is `klon_synthetic.wav` with a "synthetic" tag; label it as AI-generated when sharing. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## FAQ

**Model or engine? What is what?** VoxCPM2 (OpenBMB) is the *model*: the 2-billion-parameter network that turns text
into speech. audio.cpp is the *engine*: the C++/CUDA program that runs the model on your GPU (`audiocpp_cli.exe`). Our
patch changes the engine, not the model: it makes VoxCPM2 fit in 4 GB and makes the same seed give the same audio
every time. The Python package in this repo only prepares text, calls the engine and collects the files.

**Which GPUs?** See "Supported GPUs" above: NVIDIA from GTX 10xx up, 4 GB VRAM or more, driver ≥ 570. Native code is
in the release for sm_61/75/86/89/120a; other Pascal-or-newer cards use the embedded PTX (slower first start). AMD/Intel:
experimental Vulkan zip, `kur.ps1 -Vulkan`, untested on AMD/Intel (see "AMD / Intel" above). CPU-only (`"backend": "cpu"` in `ayarlar.json`) runs but is
~6× slower than a GTX 1050 Ti (engine measurement, 535 s vs 94 s for 48 s of speech); not a supported path.

**How fast?** Measured on a GTX 1050 Ti 4 GB (i7-7700HQ): one design variant (≈ 25 s recording) 55 s; reading ≈ 2 s of
compute per 1 s of speech (real-time factor 1.9-2.8) after a one-time ~50 s reference encoding per voice (cached on
disk) and 10-20 s model load per batch; peak VRAM 2.6-2.9 GB. Newer cards are faster; numbers and method:
[docs/4gb.md](docs/4gb.md).

**Can it clone a voice?** The underlying VoxCPM2 model can imitate a voice from a reference recording, and the cloning
section uses that. Use it only with your own voice or with the explicit permission of the person whose voice it is; the
UI asks you to confirm that permission. Voice design needs no recording: it starts from an English text description, and
the "reference" used for reading a designed voice is the model's own synthetic design recording. Impersonation, fraud
and deception are prohibited. See [ETHICS.md](ETHICS.md). Label what you publish as AI-generated.

**How do I write a good voice description?** In English, 1-3 sentences: age and gender, timbre (deep/bright, warm,
nasal, raspy), tone and role (calm documentary narrator, energetic presenter), tempo (slow, measured), and
"clean studio recording, no background noise". Keep it a description, not a script; no parentheses. Ask for 3-5
variants and listen: the seed changes the voice a lot. For the creation text use 3-5 natural Turkish sentences in the
mood you want (≈ 20-30 s of speech). When reading, one sentence per line; split long sentences, write numbers in words.

## Contributing

Not sure where to start? These four small issues are a good first step:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Try it on your GPU and report the card, driver and timings
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: try the experimental Vulkan build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Add a sentence to the test set
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Share a voice you designed, with its description and seed

Shared test set: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); brand voice guide:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); how to send code: [CONTRIBUTING.md](CONTRIBUTING.md).
Install problems: [issue form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); questions and results: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Everyone taking part follows the [Code of Conduct](CODE_OF_CONDUCT.md): be kind, keep feedback about the work.

## Contributors

- [@alexturkey](https://github.com/alexturkey): maintainer; code, bundled voices, docs
- [@cayir21](https://github.com/cayir21): macOS (Apple Silicon) Metal support, [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)

Your name belongs here too: a test result from your GPU, a sentence for the test set, a voice you designed, a clear bug
report or a pull request all count as contributions. Thank you to everyone who tries it and writes back.

## License and credits

Code and bundled voices: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Built on VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) and the audio.cpp GGUF conversion. Full list: [THIRD_PARTY.md](THIRD_PARTY.md).
Not affiliated with OpenBMB, ModelBest or the audio.cpp project.

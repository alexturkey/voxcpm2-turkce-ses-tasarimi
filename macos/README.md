# Ses Tasarımı: macOS app / Mac uygulaması

Native SwiftUI app with the same three sections as the web UI (`ses_tasarim/arayuz.py`): design a voice, read with it
(or with a bundled voice), clone your own or a consented voice. Apple Silicon, macOS 14+. The user needs no Python,
Homebrew or Terminal: the patched engine is inside the app and the model is downloaded on first launch (2.96 GB, pinned
revision, sha256-verified, pause/resume). For the Python route on a Mac see [`../docs/mac.md`](../docs/mac.md).

Türkçe: web arayüzüyle aynı üç bölümlü Mac uygulaması. Kullanıcı Python, Homebrew ya da Terminal kurmaz; yamalı motor
uygulamanın içindedir, model ilk açılışta bir kez indirilir (sha256 doğrulanır, duraklatılıp sürdürülebilir).

## What maps to what

| App | Python | Notes |
|---|---|---|
| `Mantik/Okunus.swift` | `okunus.py` | digits and quotes refused, one sentence per line, `\|\| bagli/normal/paragraf/agir`, `../ayarlar/okunus_sozlugu.tsv` (copied to the data folder on first launch so the user can edit it: "Okunuş sözlüğü…") |
| `Mantik/Motor.swift` | `motor.py` | `run_sequence`: request-sequence JSON, `engine_env` variables, `REFERENCE_OPTION`, EOS per block via `toplu_coz.deferred` / `eos_accepted_at_patch`, fixed 16 steps / CFG 2.0, one job at a time |
| `Mantik/Islemler.swift` | `tasarla.py`, `oku.py`, `klonla.py` | same `ses.json` card keys, so voices move between the two versions |
| `Mantik/GPUBellek.swift` | `motor.py: _gpu_used_mb` | IOKit `IOAccelerator` → "In use system memory", the value `ioreg` prints |
| `Mantik/ModelIndirici.swift` | `scripts/kur.sh` model step | HTTP Range resume on a `.part` file, streaming sha256 |

Cloning keeps the consent gate of the web UI (`../ETHICS.md`): the checkbox is required and checked again in
`Klon.denetle` before anything is read; the recording, its transcript and its encoding cache live in a temp folder that is
deleted when the job ends, also on failure; only the synthetic output is kept. Do not remove the gate in forks.

Deliberate differences: audio stays 16-bit PCM end to end (Python round-trips through float32), so WAVs are not
bit-identical to the Python output; exported readings are RIFF-INFO-tagged as synthetic as well (Python tags only clones);
clone input is decoded by Core Audio (wav, mp3, flac, m4a, aiff; no Ogg Vorbis). Data lives in
`~/Library/Application Support/SesTasarimi/`.

## Build (developers) / Derleme

Prerequisites: Xcode 16+, `cmake` (`brew install cmake`), `xcodegen` only if `project.yml` changes.

```bash
bash macos/scripts/motoru_derle.sh      # audio.cpp v0.7.2 + ../patches → macos/Vendor/motor/audiocpp_cli (~1 min on M4)
cd macos
xcodebuild -project SesTasarimi.xcodeproj -scheme SesTasarimi -configuration Release -derivedDataPath .build/dd build
xcodebuild -project SesTasarimi.xcodeproj -scheme SesTasarimi -derivedDataPath .build/dd test
```

The engine is built for distribution: arm64, macOS 14 minimum, `--native-cpu OFF` (no instructions specific to the
building Mac), Metal shaders embedded, voxcpm2 only. Xcode copies it to `Contents/MacOS/` and signs it with hardened
runtime. If `kur.sh` already downloaded the audio.cpp source to `~/vox/motor/`, the script reuses it.

Signing: the project has no development team, so it builds with a local (ad-hoc) signature that runs on the Mac that
built it. To sign with your own team, pick it under Signing & Capabilities in Xcode, or pass it on the command line:
`xcodebuild ... DEVELOPMENT_TEAM=<your team ID> CODE_SIGN_IDENTITY="Apple Development" build`. Handing the app to other
people needs a "Developer ID Application" certificate and notarization.

İmza: projede takım yok, derleyen Mac'te çalışan yerel imzayla derlenir. Kendi takımınızla imzalamak için Xcode'da
Signing & Capabilities altından seçin ya da komut satırında `DEVELOPMENT_TEAM=<takım kimliğiniz>` verin. Uygulamayı
başkalarına dağıtmak için "Developer ID Application" sertifikası ve notarizasyon gerekir.

Already have the model from `kur.sh`? Choose "Elimdeki dosyayı kullan…" on the first screen and pick
`~/vox/model/voxcpm2-q8_0.gguf`; it is sha256-checked and used in place (no second 2.95 GB copy).

### Self-test / Öz sınama

```bash
SES_TASARIMI_MODEL=~/vox/model/voxcpm2-q8_0.gguf \
  .build/dd/Build/Products/Release/SesTasarimi.app/Contents/MacOS/SesTasarimi --oz-sinama /tmp/oz_sinama
```

Designs 2 variants (seeds 7 and 42), reads with one, then reads twice with `belgesel_hanim` and checks that both WAVs are
byte-identical (`OZ_SINAMA_OK`). MacBook Air M4 16 GB: 239 s in total; design 71.5 s, GPU memory peak 4.1 GB.

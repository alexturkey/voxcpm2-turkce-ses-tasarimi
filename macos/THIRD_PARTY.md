# Third-party components in the macOS app / Mac uygulamasındaki üçüncü taraf bileşenler

The app (`macos/`) is part of this repository and shares its Apache-2.0 license (`../LICENSE`, `../NOTICE`). Unlike the
Python version, the built `.app` **bundles a binary of the engine**, so its components are listed here. The app copies
this file, `LICENSE`, `NOTICE` and `ETHICS.md` into `Contents/Resources/`.

| Component | What the app uses | In the `.app`? | License | Source |
|---|---|---|---|---|
| **audio.cpp** v0.7.2 (ShugoAI LLC) | inference engine `audiocpp_cli`, built with Metal by `scripts/motoru_derle.sh` and modified by `../patches/0001-voxcpm2-4gb-ve-hiz.patch` | yes, `Contents/MacOS/audiocpp_cli` | Apache-2.0 | https://github.com/0xShug0/audio.cpp |
| ggml (bundled in audio.cpp) | tensor runtime, Metal backend | yes, linked into `audiocpp_cli` | MIT | https://github.com/ggml-org/ggml |
| cJSON, libyaml (bundled in audio.cpp) | engine dependencies | yes, linked into `audiocpp_cli` | MIT | see `external/` in audio.cpp |
| SentencePiece (bundled in audio.cpp) | engine dependency | yes, linked into `audiocpp_cli` | Apache-2.0 | https://github.com/google/sentencepiece |
| **VoxCPM2** (OpenBMB / ModelBest) | TTS model | no: downloaded on first launch | Apache-2.0 (code and weights) | https://github.com/OpenBMB/VoxCPM · https://huggingface.co/openbmb/VoxCPM2 |
| **VoxCPM2 GGUF conversion** (audio.cpp project) | `voxcpm2-q8_0.gguf`, pinned revision `661a224e…`, sha256 `c8e01ab4…` | no: downloaded on first launch | governed by the original model license (Apache-2.0) | https://huggingface.co/audio-cpp/audio.cpp-gguf (`VoxCPM2-GGUF/`) |
| Bundled voices `../hazir_sesler/` | 7 synthetic voices designed from text descriptions | yes, `Contents/Resources/hazir_sesler/` | Apache-2.0 (this repository) | this repository |

The modifications to audio.cpp are described in `../THIRD_PARTY.md` (Apache-2.0 §4) and `../docs/4gb.md`; the patch applies
unchanged on macOS (the CUDA-only line is not compiled). The VoxCPM2 model card forbids impersonation, fraud and
disinformation and asks that AI-generated content be labeled: see `../ETHICS.md`. The engine embeds no audio watermark;
WAV files the app exports carry RIFF INFO tags marking them as AI-generated.

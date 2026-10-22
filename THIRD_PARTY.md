# Third-party components / Üçüncü taraf bileşenler

This project's own code is licensed under Apache-2.0 (see `LICENSE`). It builds on the following; each keeps its own
license. Nothing below is bundled in this repository except the patch in `patches/` (a derivative of audio.cpp source).

| Component | What we use | License | Source |
|---|---|---|---|
| **VoxCPM2** (OpenBMB / ModelBest) | TTS model, weights `voxcpm2-q8_0.gguf` (downloaded by `kur.ps1`, not in the repo) | Apache-2.0 (code and weights) | https://github.com/OpenBMB/VoxCPM · https://huggingface.co/openbmb/VoxCPM2 |
| **VoxCPM2 GGUF conversion** (audio.cpp project) | Q8_0 GGUF package | Governed by the original model license (Apache-2.0) | https://huggingface.co/audio-cpp/audio.cpp-gguf (`VoxCPM2-GGUF/`) |
| **audio.cpp** v0.7.2 (ShugoAI LLC) | C++/CUDA inference engine; our `patches/0001-*.patch` modifies it | Apache-2.0 | https://github.com/0xShug0/audio.cpp |
| ggml (bundled in audio.cpp) | tensor runtime, CUDA backend (one line changed by our patch) | MIT | https://github.com/ggml-org/ggml |
| cJSON, cpp-httplib, libyaml (bundled in audio.cpp) | engine dependencies | MIT | see `external/` in audio.cpp |
| SentencePiece (bundled in audio.cpp) | engine dependency | Apache-2.0 | https://github.com/google/sentencepiece |
| **NVIDIA CUDA 12.8 redistributables** | `cudart`, `cublas`, `cublasLt`, `cufft` runtime DLLs and `nvcc` for building (downloaded by `kur.ps1`, not in the repo) | NVIDIA CUDA Toolkit EULA | https://developer.download.nvidia.com/compute/cuda/redist/ |
| NumPy, python-soundfile (libsndfile) | WAV/FLAC read and write in the Python code | BSD-3 / BSD-3 (libsndfile LGPL-2.1+) | PyPI |

## Modifications to audio.cpp (Apache-2.0 §4)

`patches/0001-voxcpm2-4gb-ve-hiz.patch` changes these audio.cpp v0.7.2 files (see `docs/4gb.md` for what and why):
`app/workflow/execution.cpp`, `external/ggml/src/ggml-cuda/ggml-cuda.cu`, `include/engine/framework/runtime/deferred_decode.h` (new),
`include/engine/models/voxcpm2/{audiovae,generator,minicpm,session}.h`, `src/models/voxcpm2/{audiovae,generator,minicpm,session}.cpp`.
The modified files carry the original copyright; the modifications are Apache-2.0 as well.

## Bundled voices

The seven voices in `hazir_sesler/` were generated with VoxCPM2 from text descriptions (prompts are in each `ses.json`).
They are synthetic; no real person's voice was used. They are released under this repository's Apache-2.0 license.

## Model card notice (VoxCPM2)

The VoxCPM2 model card states: it is strictly forbidden to use VoxCPM for impersonation, fraud or disinformation, and
AI-generated content should be clearly labeled. This project follows that: see `ETHICS.md`.

# VoxCPM2 on a 4 GB GPU (GTX 1050 Ti) / 4 GB ekran kartına sığdırma

VoxCPM2 is a 2B-parameter TTS model. Unpatched audio.cpp runs it on CUDA but does not fit a 4 GB card: the LM's KV
cache plus the AudioVAE decoder fill the memory. Everything below is enabled by environment variables that the Python
code sets for the engine process only (`ses_tasarim/motor.py: engine_env`). Without those variables the patched engine
behaves exactly like upstream.

## What the patch does (patches/0001-voxcpm2-4gb-ve-hiz.patch)

| # | Change | Env | Effect |
|---|---|---|---|
| 1 | Model in **Q8_0 GGUF** (2.95 GB file) instead of bf16 (4.77 GB) | – | weights fit; quality difference inaudible in our listening tests |
| 2 | **KV cache sized to the request** instead of `max_length` 8192 steps (rounded up to 256) | `VOXCPM2_KV_CAPACITY=auto` | the single largest VRAM saving; output byte-identical to the unpatched engine |
| 3 | **AudioVAE encoder on the CPU** (reference encoding) | `VOXCPM2_AUDIOVAE_CPU=1`, `VOXCPM2_AUDIOVAE_THREADS=6` | the encoder never touches VRAM |
| 4 | **Sequential execution**: after the last text chunk the LM (base, residual, shadow, KV) is freed, then the decoder is built on the GPU | `VOXCPM2_AUDIOVAE_GPU_CHUNK=10` | LM and decoder never coexist in VRAM |
| 5 | **Chunked decoding**: the latent sequence is decoded in 10-second slices with a causal left context | same | decoder peak memory bounded regardless of length |
| 6 | **Zeroed CUDA buffers** (`cudaMemset` on every new allocation, graph buffers reset) | – | without it, stale data in re-used VRAM leaked into the audio and the same seed gave different audio between runs |
| 7 | **Reference-embedding cache kept across generator rebuilds** (session-owned) and **on disk** per reference | `VOXCPM2_PROMPT_CACHE_DIR` | encoding a 25 s reference costs ~50 s once, then ~0.1 s |
| 8 | **Deferred decoding**: all lines of a request sequence are generated first, then decoded once | `VOXCPM2_TOPLU_COZ=1` | saves ~2 s of decoder reload per line |
| 9 | One engine session for many requests (`--request-sequence`), model loaded once | – | ~10-20 s load paid once per batch |
| 10 | Shadow-LM EOS confirmation and acoustic rescue (inherited baseline of the voxcpm2 generator in this patch) | `VOXCPM2_PROBE_*` | fewer half-finished sentences; a sentence without `eos_accepted_at_patch` in the log is treated as failed |

Rules that follow from this: read **sentence by sentence** (one line per sentence; a single long chunk pushed peak VRAM
to 3.67 GB and ran out), keep one GPU job at a time, keep text under ~2000 characters per line.

## Measurements (same machine: GTX 1050 Ti 4 GB, i7-7700HQ, 16 GB RAM, Windows 10, CUDA 12.8)

| What | Result |
|---|---|
| 48.5 s of speech, unpatched CUDA / CPU only / patched | 293 s / 535 s / **94 s**, peak VRAM 2999 MB |
| Reading 10 sentences (~52 s audio) before vs after the cache + deferred-decode patches | 179 s → **111 s** (cache warm), 161 s (cache cold) |
| Typical reading | ~2 s of wall time per 1 s of audio (real-time factor 1.9-2.8), peak VRAM 2.6-2.9 GB |
| Voice design, one variant (25 s reference), this repo's code | 55 s, peak VRAM 2835 MB |
| Build from source (VS 2022 Build Tools, Ninja, 6 jobs) | ~15-25 min, ~400 MB build dir, exe ~34 MB |

Quality settings are fixed at 16 diffusion steps and CFG 2.0 and are not used as a speed knob. The seed is not a quality
setting either: for design it provides variety (one seed per variant), for reading it is the chosen voice's own seed
(consistency).

## Türkçe özet

Yamasız motor 4 GB'a sığmaz. Yama: Q8_0 model, KV önbelleği gerektiği kadar, AudioVAE kodlayıcı CPU'da, üretim bitince LM
boşaltılıp çözücü GPU'ya alınır, çözüm 10 sn'lik dilimlerle yapılır, CUDA tamponları sıfırlanır (aynı tohum aynı ses),
referans kodlaması diske önbelleklenir, bütün satırlar üretilip bir kez çözülür, model bir kez yüklenir. Ölçüm: 48,5 sn
ses yamasız 293 sn / CPU 535 sn / yamalı 94 sn, VRAM tepe 3,0 GB; okuma 1 sn ses ≈ 2 sn; tasarım 1 çeşit 55 sn, 2,8 GB.
Kalite ayarları (16 adım, cfg 2.0) sabittir; cümle cümle okunur; aynı anda tek GPU işi.

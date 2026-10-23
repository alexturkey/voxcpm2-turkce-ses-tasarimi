# macOS (Apple Silicon, Metal) / Mac'te çalıştırma

The same patched engine (audio.cpp v0.7.2 + `patches/0001-voxcpm2-4gb-ve-hiz.patch`) builds and runs on Apple Silicon
through ggml's Metal backend. No code in the patch had to change: the patch applies cleanly, and the only CUDA-specific
line (`cudaMemset` in `ggml-cuda.cu`) is simply not compiled on a Mac. The Python code, the voices, the settings and the
quality (16 steps, CFG 2.0) are identical to Windows.

## Install

Prerequisites: Xcode Command Line Tools (`xcode-select --install`) and [Homebrew](https://brew.sh). Then:

```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```

`scripts/kur.sh` mirrors `kur.ps1 -Derle`: it downloads the same pinned model and audio.cpp source (sha256 checked),
applies the patch, builds `audiocpp_cli` with Metal (voxcpm2 only, ~1 min), creates `.venv`, writes
`ayarlar.json` with `"backend": "metal"` and checks that the engine sees the GPU (`MTL:0`). Default root `~/vox`
(`--kok <dir>` to change). Steps can be re-run one by one: `--adim model,kaynak,derle,python,ayar,kontrol`. Disk:
2.8 GB model + ~300 MB source and build.

Start: double-click **`baslat.command`** in Finder (or `./baslat.command`). It opens the browser at
http://127.0.0.1:8765/ when ready; Ctrl+C in its Terminal window stops it. If macOS blocks the first double-click
("cannot be opened"), right-click → Open once. Command line: same as on Windows, with `.venv/bin/python` instead of
`.venv\Scripts\python.exe`.

## Measurements: MacBook Air M4, 16 GB, fanless

macOS 27.0.1, on AC power, 10-core CPU (4P + 6E), 10-core GPU. Same model file (`voxcpm2-q8_0.gguf`, sha256
`c8e01ab4…`) and the same engine settings as on Windows (`ses_tasarim/motor.py: engine_env`, unchanged).

| What | Result |
|---|---|
| Build (`kur.sh`, derle step, voxcpm2 only) | **40 s** (Windows CUDA build: 15-25 min) |
| Reading `belgesel_hanim` sample text (6 sentences, 31.8 s audio), cold cache | 85 s (incl. one-time reference encoding) |
| Same, warm cache | **64 s**, ~2.0 s of wall time per 1 s of audio (GTX 1050 Ti: 1.9-2.8) |
| Same seed, same text, cold vs warm run | **byte-identical WAV** (same sha1): Metal needs no extra fix for determinism |
| Voice design, 2 variants (12-15 s each) | 51 s total |
| Long reading: 54 sentences, 346.9 s (5.8 min) audio | 738.7 s (12.3 min), RTF 2.13, all 54 sentences finished (EOS) |
| Thermal throttling during that 12 min run | **none**: first 27 sentences 334 s, the same 27 sentences again 322 s; `pmset -g therm` CPU speed limit stayed 100, no thermal warning |

### Memory and load

Sampled every second (`ps`, `ioreg` IOAccelerator, `memory_pressure`, `pmset -g therm`; none of them need sudo).

| Metric | Reading / design | Note |
|---|---|---|
| Engine process RAM (RSS) peak | 5.2-5.3 GB | model + LM + decoder; unified memory, so this is also what the GPU uses |
| GPU memory in use, peak (system-wide) | 4.0-4.2 GB | about 0.8 GB of that is macOS/other apps at idle |
| System free memory, lowest | 30-31 % of 16 GB | other apps open during the test; no swapping pressure |
| GPU utilisation | 80-97 % average, 100 % peak | the work is GPU-bound |
| Engine CPU | 15-24 % average | short peaks (up to ~6 cores) during reference encoding and final decode |

What this means in practice:
- **16 GB:** comfortable. You can keep a browser and other light apps open.
- **8 GB:** not tested. The engine needs ~5.3 GB, so it should run with few other apps open; expect swapping, a slower run,
  and close heavy apps first. Reports welcome in Discussions.
- **Fanless Air:** no slowdown seen over 12 minutes of continuous load. The chassis gets warm. Much longer jobs (an
  hour of audio) were not tested.
- One job at a time, as on Windows (the UI already queues jobs).
- The UI's "VRAM tepe" value on a Mac is the system-wide GPU memory in use (from `ioreg`), the counterpart of
  `nvidia-smi` on Windows.
- M1/M2/M3 and Intel Macs were not tested.

## Türkçe özet

Aynı yamalı motor, ggml'in Metal arka ucuyla Apple Silicon'da derleniyor ve çalışıyor. Yamada değişiklik gerekmedi.
Kurulum: `brew install cmake python@3.12`, sonra `bash scripts/kur.sh` (model, kaynak, yama, ~1 dk Metal derlemesi,
Python, ayarlar, GPU kontrolü). Başlatmak için Finder'da `baslat.command` dosyasına çift tıklayın.

MacBook Air M4 16 GB (fansız) ölçümleri:
- Okuma hızı: 1 sn ses ≈ 2 sn, GTX 1050 Ti ile aynı.
- Aynı tohum, ilk ve ikinci çalıştırmada **bayt bayt aynı** ses verdi.
- Tasarım: 2 çeşit 51 sn.
- Uzun okuma: 5,8 dk ses 12,3 dk'da üretildi, yarım cümle yok. **Isınmadan kaynaklı yavaşlama görülmedi**: aynı 27 cümle
  ilk turda 334 sn, ikinci turda 322 sn sürdü.
- Bellek: motor en fazla ~5,3 GB RAM kullandı (birleşik bellek), GPU belleği en fazla ~4,1 GB oldu, sistemde en az %30
  boş bellek kaldı.
- Yük: GPU %80-97 dolu, CPU ortalama %15-24.

8 GB Mac'te ve M1-M3'te denenmedi; denerseniz sonucu Discussions'a yazın.

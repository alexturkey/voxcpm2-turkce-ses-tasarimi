#!/usr/bin/env bash
# Ubuntu/Linux CUDA: doğrulanmış model + yamalı motor + Python ortamı. Sudo çalıştırmaz.
# Verified model + patched engine + Python environment. Never invokes sudo.
set -euo pipefail

usage() {
    cat <<'HELP'
Usage: bash scripts/kur-linux.sh [--kok DIR] [--adim model,kaynak,derle,python,ayar,kontrol]
                               [--mimari native|86|...] [--paralel N]
Requires Linux, NVIDIA driver, CUDA toolkit (nvcc), CMake, C++ compiler, Git, curl,
sha256sum, tar and Python 3.10-3.13 with venv. See docs/linux.md.
HELP
}
KOK="$HOME/vox"
ADIM="model,kaynak,derle,python,ayar,kontrol"
MIMARI="native"
PARALEL=4
while [[ $# -gt 0 ]]; do
    case "$1" in
        --kok|--adim|--mimari|--paralel)
            [[ $# -ge 2 && -n "$2" && "$2" != --* ]] || { usage >&2; exit 2; }
            case "$1" in
                --kok) KOK="$2" ;; --adim) ADIM="$2" ;;
                --mimari) MIMARI="$2" ;; --paralel) PARALEL="$2" ;;
            esac
            shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
    esac
done
[[ "$(uname -s)" == Linux ]] || { echo "Linux only; macOS: scripts/kur.sh; Windows: scripts/kur.ps1" >&2; exit 1; }
[[ "$PARALEL" =~ ^[1-9][0-9]*$ ]] || { echo "--paralel must be a positive integer" >&2; exit 2; }
[[ -n "$ADIM" && "$ADIM" != ,* && "$ADIM" != *, && "$ADIM" != *,,* ]] || { echo "Empty step" >&2; exit 2; }
IFS=, read -r -a steps <<< "$ADIM"
for step in "${steps[@]}"; do
    case "$step" in model|kaynak|derle|python|ayar|kontrol) ;; *) echo "Unknown step: $step" >&2; exit 2 ;; esac
done
adim() { [[ ",$ADIM," == *",$1,"* ]]; }
need() { command -v "$1" >/dev/null || { echo "Missing: $1 (see docs/linux.md)" >&2; exit 1; }; }
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
# Fail before large downloads if selected build/Python steps cannot run.
if adim derle; then need cmake; need nvcc; need c++; fi
if adim python; then
    PY=""
    for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
        if command -v "$candidate" >/dev/null && "$candidate" -c \
            'import sys,struct; sys.exit(0 if (3,10) <= sys.version_info[:2] <= (3,13) and struct.calcsize("P")==8 else 1)' 2>/dev/null; then
            PY="$(command -v "$candidate")"; break
        fi
    done
    [[ -n "$PY" ]] || { echo "64-bit Python 3.10-3.13 required; see docs/linux.md" >&2; exit 1; }
fi
mkdir -p "$KOK"
KOK="$(cd "$KOK" && pwd)"
SRC="$KOK/motor/src"
BUILD="$KOK/motor/build"
MOTOR="$BUILD/bin/audiocpp_cli"
MODEL="$KOK/model/voxcpm2-q8_0.gguf"
PATCH="$REPO/patches/0001-voxcpm2-4gb-ve-hiz.patch"
MODEL_URL="https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/661a224e9d9adbd49c01626f85e426f5f425d771/VoxCPM2-GGUF/voxcpm2-q8_0.gguf"
MODEL_SHA="c8e01ab4416011e12a28f24ede298a1aa5ce64b43f8e8aaad53b1e2fe7c96432"
SRC_URL="https://github.com/0xShug0/audio.cpp/archive/refs/tags/v0.7.2.tar.gz"
SRC_SHA="cab8db31cec26ef8f1e39eabea1df5f02a87e8de87a5ae334b1e66217339c6bf"
sha_ok() { [[ -f "$1" ]] && [[ "$(sha256sum "$1" | cut -d' ' -f1)" == "$2" ]]; }
indir() {
    local url="$1" out="$2" sha="$3"
    need curl; need sha256sum
    if sha_ok "$out" "$sha"; then echo "Verified, skipping: $out"; return; fi
    mkdir -p "$(dirname "$out")"
    curl -fL --retry 3 -C - -o "$out.part" "$url" || curl -fL --retry 3 -o "$out.part" "$url"
    if ! sha_ok "$out.part" "$sha"; then
        rm -f "$out.part"
        echo "SHA256 mismatch: $out" >&2; exit 1
    fi
    mv "$out.part" "$out"
}
if adim model; then
    indir "$MODEL_URL" "$MODEL" "$MODEL_SHA"
    echo MODEL_OK
fi
if adim kaynak; then
    need git; need tar
    indir "$SRC_URL" "$KOK/motor/v0.7.2.tar.gz" "$SRC_SHA"
    if [[ ! -f "$SRC/CMakeLists.txt" ]]; then
        mkdir -p "$SRC"
        tar -xzf "$KOK/motor/v0.7.2.tar.gz" -C "$SRC" --strip-components 1
    fi
    # Keep the source outside another git checkout (git apply can silently skip outside paths).
    if [[ ! -d "$SRC/.git" ]]; then git -C "$SRC" init -q; fi
    if ! git -C "$SRC" apply --reverse --check "$PATCH" 2>/dev/null; then
        git -C "$SRC" apply --check "$PATCH"
        git -C "$SRC" apply "$PATCH"
    fi
    git -C "$SRC" apply --reverse --check "$PATCH"
    echo KAYNAK_OK
fi
if adim derle; then
    cmake -S "$SRC" -B "$BUILD" -DCMAKE_BUILD_TYPE=Release \
        -DAUDIOCPP_MODEL_SET=custom -DAUDIOCPP_MODELS=voxcpm2 -DAUDIOCPP_DEPLOYMENT_BUILD=ON \
        -DAUDIOCPP_BUILD_NATIVE_MODEL_MANAGER=OFF -DAUDIOCPP_EMBED_DEMO_VOICES=OFF \
        -DENGINE_ENABLE_CUDA=ON -DENGINE_ENABLE_CUDA_GRAPHS=ON \
        -DCMAKE_CUDA_COMPILER="$(command -v nvcc)" -DCMAKE_CUDA_ARCHITECTURES="$MIMARI" \
        -DENGINE_ENABLE_HIP=OFF -DENGINE_ENABLE_METAL=OFF -DENGINE_ENABLE_VULKAN=OFF \
        -DENGINE_ENABLE_OPENMP=ON -DGGML_OPENMP=ON \
        -DENGINE_BUILD_TESTS=OFF -DENGINE_BUILD_EXAMPLES=OFF
    cmake --build "$BUILD" --target audiocpp_cli --parallel "$PARALEL"
    [[ -x "$MOTOR" ]] || { echo "Engine missing: $MOTOR" >&2; exit 1; }
    echo DERLE_OK
fi
if adim python; then
    if [[ ! -x "$REPO/.venv/bin/python" ]]; then "$PY" -m venv "$REPO/.venv"; fi
    "$REPO/.venv/bin/python" -m pip install --disable-pip-version-check -r "$REPO/requirements.txt"
    "$REPO/.venv/bin/python" -c 'import numpy, soundfile'
    echo PYTHON_OK
fi
if adim ayar; then
    "$REPO/.venv/bin/python" - "$REPO/ayarlar.json" "$MOTOR" "$MODEL" <<'PY'
import datetime, json, shutil, sys
from pathlib import Path
path, engine, model = sys.argv[1:]
p = Path(path)
if p.exists():
    # Preserve user choices and back up before updating the Linux engine paths.
    shutil.copy2(p, str(p) + '.bak-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    settings = json.loads(p.read_text(encoding='utf-8'))
else:
    settings = {}
settings.update(motor=engine, model=model, backend='cuda', cuda_bin='')
for key, value in dict(sesler='sesler', hazir_sesler='hazir_sesler', onbellek='onbellek',
                       audiovae_threads=6, motor_threads=4, port=8765).items():
    settings.setdefault(key, value)
p.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
PY
    echo AYAR_OK
fi
if adim kontrol; then
    "$REPO/.venv/bin/python" - "$REPO/ayarlar.json" <<'PY'
import sys
from ses_tasarim import ayarlar, motor
settings = ayarlar.load(sys.argv[1])
devices = motor.list_devices(settings)
print(devices)
if 'CUDA:' not in devices:
    raise SystemExit('CUDA device missing; check driver, runtime libraries and container GPU access')
PY
    echo KONTROL_OK
fi
echo KURULUM_OK

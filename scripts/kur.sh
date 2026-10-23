#!/usr/bin/env bash
# Kurulum, macOS (Apple Silicon, Metal) / installer for macOS:  model + yamalı motor (kaynaktan Metal derlemesi) + Python + ayarlar.json
#   bash scripts/kur.sh                      # kök ~/vox / root ~/vox
#   bash scripts/kur.sh --kok ~/vox          # başka kök / other root
# Adım seçmek / select steps:  --adim model,kaynak,derle,python,ayar,kontrol
# Her adım yeniden çalıştırılabilir: mevcut ve sha256'sı doğru dosya atlanır. / Idempotent: verified files are skipped.
# Gerekenler / prerequisites:  Xcode Command Line Tools (xcode-select --install), Homebrew: brew install cmake python@3.12
set -euo pipefail

KOK="$HOME/vox"
ADIM=""
PARALEL="$(sysctl -n hw.perflevel0.physicalcpu 2>/dev/null || sysctl -n hw.ncpu)"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --kok) KOK="$2"; shift 2 ;;
        --adim) ADIM="$2"; shift 2 ;;
        --paralel) PARALEL="$2"; shift 2 ;;
        -h|--help) sed -n 2,7p "$0"; exit 0 ;;
        *) echo "bilinmeyen seçenek / unknown option: $1" >&2; exit 2 ;;
    esac
done
[[ -n "$ADIM" ]] || ADIM="model,kaynak,derle,python,ayar,kontrol"
for a in ${ADIM//,/ }; do
    case "$a" in model|kaynak|derle|python|ayar|kontrol) ;; *) echo "bilinmeyen adım '$a'" >&2; exit 2 ;; esac
done
adim() { [[ ",$ADIM," == *",$1,"* ]]; }
echo "adımlar: $ADIM  (kök $KOK)"

[[ "$(uname -s)" == "Darwin" ]] || { echo "bu betik macOS içindir; Windows: scripts\\kur.ps1" >&2; exit 1; }
[[ "$(uname -m)" == "arm64" ]] || echo "UYARI: Apple Silicon değil ($(uname -m)); Metal yolu yalnız M1-M4'te denendi" >&2
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$KOK"
KOK="$(cd "$KOK" && pwd)"

# --- sabitler / pinned downloads (kur.ps1 ile aynı) ----------------------------------------------------------------
MODEL_URL="https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/661a224e9d9adbd49c01626f85e426f5f425d771/VoxCPM2-GGUF/voxcpm2-q8_0.gguf"
MODEL_SHA="c8e01ab4416011e12a28f24ede298a1aa5ce64b43f8e8aaad53b1e2fe7c96432"
SRC_URL="https://github.com/0xShug0/audio.cpp/archive/refs/tags/v0.7.2.tar.gz"
SRC_SHA="cab8db31cec26ef8f1e39eabea1df5f02a87e8de87a5ae334b1e66217339c6bf"
PATCH="$REPO/patches/0001-voxcpm2-4gb-ve-hiz.patch"
MODEL="$KOK/model/voxcpm2-q8_0.gguf"
MOTOR="$KOK/motor/build/bin/audiocpp_cli"

sha_ok() { [[ -f "$1" ]] && [[ "$(shasum -a 256 "$1" | cut -d' ' -f1)" == "$2" ]]; }
indir() {  # url hedef sha
    if sha_ok "$2" "$3"; then echo "  var, sha256 doğru: $2"; return; fi
    mkdir -p "$(dirname "$2")"
    curl -L --fail --retry 3 -C - -o "$2.part" "$1" || curl -L --fail --retry 3 -o "$2.part" "$1"
    mv "$2.part" "$2"
    sha_ok "$2" "$3" || { echo "sha256 tutmadı: $2" >&2; exit 1; }
    echo "  indirildi, sha256 doğru: $2"
}

if adim model; then
    echo "== model (2.95 GB)"
    indir "$MODEL_URL" "$MODEL" "$MODEL_SHA"
    echo "MODEL_OK"
fi

if adim kaynak; then
    echo "== audio.cpp v0.7.2 kaynağı + yama"
    indir "$SRC_URL" "$KOK/motor/v0.7.2.tar.gz" "$SRC_SHA"
    SRC="$KOK/motor/src"
    if [[ ! -f "$SRC/CMakeLists.txt" ]]; then
        mkdir -p "$SRC" && tar -xzf "$KOK/motor/v0.7.2.tar.gz" -C "$SRC" --strip-components 1
    fi
    if (cd "$SRC" && git apply --reverse --check "$PATCH" 2>/dev/null); then
        echo "  yama zaten uygulanmış"
    else
        (cd "$SRC" && git apply --check "$PATCH") || { echo "yama uygulanamıyor (kaynak saf v0.7.2 mi?)" >&2; exit 1; }
        (cd "$SRC" && git apply "$PATCH" && git apply --reverse --check "$PATCH")
        echo "  yama uygulandı ve doğrulandı"
    fi
    echo "KAYNAK_OK"
fi

if adim derle; then
    echo "== Metal derlemesi (~5-10 dk, $PARALEL iş)"
    for tool in cmake xcrun; do command -v "$tool" >/dev/null || { echo "eksik: $tool (brew install cmake; xcode-select --install)" >&2; exit 1; }; done
    xcrun --sdk macosx --find metal >/dev/null 2>&1 || { echo "Metal derleyicisi yok: Xcode ya da 'xcodebuild -downloadComponent MetalToolchain'" >&2; exit 1; }
    (cd "$KOK/motor/src" && scripts/build_metal.sh --build-dir "$KOK/motor/build" --build-type Release --archs "$(uname -m)" \
        --model-set custom --models voxcpm2 --deployment-build --openmp OFF --target audiocpp_cli -j "$PARALEL")
    [[ -x "$MOTOR" ]] || { echo "derleme bitti ama motor yok: $MOTOR" >&2; exit 1; }
    echo "DERLE_OK"
fi

if adim python; then
    echo "== Python paketleri (.venv + numpy, soundfile)"
    PY=""
    for c in python3.13 python3.12 python3.11 python3.10 python3; do
        if command -v "$c" >/dev/null && "$c" -c 'import sys; sys.exit(0 if (3, 10) <= sys.version_info[:2] <= (3, 13) else 1)' 2>/dev/null; then
            PY="$(command -v "$c")"; break
        fi
    done
    [[ -n "$PY" ]] || { echo "Python 3.10-3.13 bulunamadı. Kurun: brew install python@3.12" >&2; exit 1; }
    echo "  python: $PY"
    [[ -x "$REPO/.venv/bin/python" ]] || "$PY" -m venv "$REPO/.venv"
    "$REPO/.venv/bin/python" -m pip install --quiet --disable-pip-version-check -r "$REPO/requirements.txt"
    "$REPO/.venv/bin/python" -c "import numpy, soundfile"
    echo "PYTHON_OK"
fi

if adim ayar; then
    echo "== ayarlar.json"
    "${REPO}/.venv/bin/python" - "$REPO/ayarlar.json" "$MOTOR" "$MODEL" <<'PY'
import json, sys
hedef, motor, model = sys.argv[1:]
ayar = {"motor": motor, "model": model, "cuda_bin": "", "backend": "metal", "sesler": "sesler",
        "hazir_sesler": "hazir_sesler", "onbellek": "onbellek", "audiovae_threads": 6, "motor_threads": 4, "port": 8765}
open(hedef, "w", encoding="utf-8").write(json.dumps(ayar, ensure_ascii=False, indent=2) + "\n")
PY
    echo "  yazıldı: $REPO/ayarlar.json"
    echo "AYAR_OK"
fi

if adim kontrol; then
    echo "== kontrol: motor + Metal cihazı"
    [[ -x "$MOTOR" ]] || { echo "motor yok: $MOTOR (adım: derle)" >&2; exit 1; }
    [[ -f "$MODEL" ]] || { echo "model yok: $MODEL (adım: model)" >&2; exit 1; }
    cikti="$("$MOTOR" --list-devices 2>&1 || true)"
    gpu="$(grep "^MTL:" <<<"$cikti" || true)"
    [[ -n "$gpu" ]] || { echo "$cikti"; echo "motor Metal cihazı görmedi" >&2; exit 1; }
    echo "  $gpu"
    echo "KONTROL_OK"
fi
echo "KURULUM_OK"
echo "Arayüz / web UI:  ./baslat.command   (ya da .venv/bin/python -m ses_tasarim.arayuz, sonra http://127.0.0.1:8765/ )"

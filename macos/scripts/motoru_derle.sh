#!/usr/bin/env bash
# Yamalı audio.cpp motorunu (audiocpp_cli) uygulamaya gömmek için Metal ile derler.
# Builds the patched audio.cpp engine (audiocpp_cli) with Metal, to be embedded in the app.
#
#   bash macos/scripts/motoru_derle.sh      # → macos/Vendor/motor/audiocpp_cli
#
# Kaynak: audio.cpp v0.7.2 (sha256 sabit) + reponun patches/0001-voxcpm2-4gb-ve-hiz.patch yaması (kur.sh ile aynı).
# Dağıtım derlemesi: --native-cpu OFF (yalnız derleyen makinenin işlemcisine özel komut yok, M1-M4'te çalışır),
# macOS 14 alt sınırı, arm64. Gerekenler (yalnız geliştirici için): Xcode, cmake (brew install cmake).
# Distribution build: no host-specific CPU flags, macOS 14 minimum, arm64. Developer prerequisites: Xcode, cmake.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$ROOT/.build/motor"
SRC_URL="https://github.com/0xShug0/audio.cpp/archive/refs/tags/v0.7.2.tar.gz"
SRC_SHA="cab8db31cec26ef8f1e39eabea1df5f02a87e8de87a5ae334b1e66217339c6bf"
PATCH="$ROOT/../patches/0001-voxcpm2-4gb-ve-hiz.patch"
OUT="$ROOT/Vendor/motor/audiocpp_cli"
JOBS="$(sysctl -n hw.perflevel0.physicalcpu 2>/dev/null || sysctl -n hw.ncpu)"

for tool in cmake xcrun git; do
    command -v "$tool" >/dev/null || { echo "eksik / missing: $tool (brew install cmake; xcode-select --install)" >&2; exit 1; }
done
xcrun --sdk macosx --find metal >/dev/null 2>&1 \
    || { echo "Metal derleyicisi yok / no Metal compiler: xcodebuild -downloadComponent MetalToolchain" >&2; exit 1; }

sha_ok() { [[ -f "$1" ]] && [[ "$(shasum -a 256 "$1" | cut -d' ' -f1)" == "$2" ]]; }
mkdir -p "$WORK"
TARBALL="$WORK/v0.7.2.tar.gz"
# kur.sh daha önce indirdiyse onu kullan (aynı sha256) / reuse kur.sh's download
[[ -f "$TARBALL" ]] || ! sha_ok "$HOME/vox/motor/v0.7.2.tar.gz" "$SRC_SHA" || ln -s "$HOME/vox/motor/v0.7.2.tar.gz" "$TARBALL"
if ! sha_ok "$TARBALL" "$SRC_SHA"; then
    curl -L --fail --retry 3 -o "$TARBALL.part" "$SRC_URL"
    mv "$TARBALL.part" "$TARBALL"
    sha_ok "$TARBALL" "$SRC_SHA" || { echo "sha256 tutmadı / mismatch: $TARBALL" >&2; exit 1; }
fi

SRC="$WORK/src"
if [[ ! -f "$SRC/CMakeLists.txt" ]]; then
    mkdir -p "$SRC" && tar -xzf "$TARBALL" -C "$SRC" --strip-components 1
fi
if ! (cd "$SRC" && git apply --reverse --check "$PATCH" 2>/dev/null); then
    (cd "$SRC" && git apply --check "$PATCH" && git apply "$PATCH")
fi
(cd "$SRC" && git apply --reverse --check "$PATCH") || { echo "yama doğrulanamadı / patch not verified" >&2; exit 1; }

(cd "$SRC" && scripts/build_metal.sh --build-dir "$WORK/build" --build-type Release --archs arm64 \
    --deployment-target 14.0 --native-cpu OFF --embed-metal ON \
    --model-set custom --models voxcpm2 --deployment-build --openmp OFF --target audiocpp_cli -j "$JOBS")

mkdir -p "$(dirname "$OUT")"
cp "$WORK/build/bin/audiocpp_cli" "$OUT"
"$OUT" --list-devices 2>&1 | grep -q "^MTL:" || { echo "motor Metal cihazı görmedi / engine sees no Metal device" >&2; exit 1; }
shasum -a 256 "$OUT"
echo "MOTOR_OK: $OUT"

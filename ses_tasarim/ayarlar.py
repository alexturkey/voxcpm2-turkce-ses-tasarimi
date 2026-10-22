"""Ayar dosyası: motor, model ve klasör yolları. Kodda sabit yol yoktur. / Settings file: engine, model, folders."""
import json
import os
from pathlib import Path

ENV_NAME = "SES_TASARIM_AYARLAR"
DEFAULTS = {
    "motor": "",            # audiocpp_cli.exe (yamalı derleme) / patched audiocpp_cli.exe
    "model": "",            # voxcpm2-q8_0.gguf
    "cuda_bin": "",         # CUDA 12.8 bin klasörü (cudart64_12.dll, cublas64_12.dll, cublasLt64_12.dll, cufft64_11.dll)
    "backend": "cuda",      # cuda | cpu (cpu çok yavaştır, yalnız deneme için)
    "sesler": "sesler",             # tasarlanan sesler (ayar dosyasına göre göreli) / designed voices
    "hazir_sesler": "hazir_sesler", # repodaki hazır sesler / bundled voices
    "onbellek": "onbellek",         # referans kodlama disk önbelleği / reference-encoding cache
    "audiovae_threads": 6,  # AudioVAE kodlayıcı CPU iş parçacığı / CPU threads for the AudioVAE encoder
    "motor_threads": 4,     # motor --threads
    "port": 8765,           # arayüz (127.0.0.1) / web UI port
}
PATH_KEYS = ("motor", "model", "cuda_bin", "sesler", "hazir_sesler", "onbellek")


class AyarHatasi(RuntimeError):
    pass


def find_file(explicit=None) -> Path:
    for candidate in (explicit, os.environ.get(ENV_NAME), "ayarlar.json"):
        if candidate and Path(candidate).is_file():
            return Path(candidate).resolve()
    raise AyarHatasi("ayar dosyası yok: --ayarlar <yol>, %s ortam değişkeni ya da ./ayarlar.json "
                     "(örnek: ayarlar.example.json; kur.ps1 bunu kendisi yazar)" % ENV_NAME)


def load(explicit=None) -> dict:
    path = find_file(explicit)
    data = {**DEFAULTS, **json.loads(path.read_text(encoding="utf-8"))}
    base = path.parent
    for key in PATH_KEYS:
        value = str(data.get(key) or "").strip()
        data[key] = (base / value).resolve() if value and not Path(value).is_absolute() else (Path(value) if value else None)
    problems = []
    if not data["motor"] or not data["motor"].is_file():
        problems.append(f"motor bulunamadı: {data['motor']}")
    if not data["model"] or not data["model"].is_file():
        problems.append(f"model bulunamadı: {data['model']}")
    if data["backend"] == "cuda" and (not data["cuda_bin"] or not (data["cuda_bin"] / "cudart64_12.dll").is_file()):
        problems.append(f"cuda_bin içinde cudart64_12.dll yok: {data['cuda_bin']}")
    if problems:
        raise AyarHatasi(f"{path}:\n  - " + "\n  - ".join(problems))
    for key in ("sesler", "hazir_sesler", "onbellek"):
        data[key].mkdir(parents=True, exist_ok=True)
    data["_dosya"] = path
    return data

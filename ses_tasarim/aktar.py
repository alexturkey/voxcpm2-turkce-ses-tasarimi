"""Kendi veya izinli ses kaydını yerel ses kitaplığına ekle.

python -m ses_tasarim.aktar --ad kendi_sesim --kayit kayit.wav --metin @kayit_metni.txt
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from . import ayarlar, okunus
from .tasarla import slug, read_arg_text


def aktar(settings, name, recording, text):
    problems = okunus.problems(text, "kayıtta söylenen metin")
    if problems:
        raise ValueError("\n".join(problems))
    info = sf.info(recording)
    if not 8 <= info.duration <= 35:
        raise ValueError("Kayıt sekiz ile otuz beş saniye arasında olmalı.")
    if hasattr(recording, "seek"):
        recording.seek(0)
    audio, rate = sf.read(recording, dtype="float32", always_2d=True)
    if not np.isfinite(audio).all() or np.max(np.abs(audio)) < 0.0001:
        raise ValueError("Kayıt sessiz veya geçersiz örnekler içeriyor.")
    audio = audio.mean(axis=1)
    if np.max(np.abs(audio)) < 0.0001:
        raise ValueError("Mono dönüşümünde ses kayboluyor; mono kayıt kullanın.")
    voice_dir = settings["sesler"] / slug(name)
    voice_dir.mkdir(parents=True, exist_ok=True)
    number = 1
    while (voice_dir / f"cesit_{number:02d}").exists():
        number += 1
    trial = voice_dir / f"cesit_{number:02d}"
    trial.mkdir()
    try:
        sf.write(trial / "referans.wav", audio, rate, subtype="PCM_16")
        card = {"ad": voice_dir.name, "gorunen_ad": name.strip(), "cesit": number,
                "ses_yaratici_ingilizce_prompt": "",
                "ses_yaratilirken_okutulan_metin": " ".join(text.split()),
                "okuma_tohumu": 42, "referans": "referans.wav", "referans_sn": info.duration,
                "kaynak": "izinli_kayit", "tanitim_tr": "Kendi veya izinli ses kaydı",
                "yapay": False, "tarih": time.strftime("%Y-%m-%d %H:%M")}
        (trial / "ses.json").write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        for file in trial.iterdir():
            file.unlink()
        trial.rmdir()
        raise
    return f"{voice_dir.name}/{number}"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ayarlar")
    parser.add_argument("--ad", required=True)
    parser.add_argument("--kayit", required=True, type=Path)
    parser.add_argument("--metin", required=True, help="Kayıtta söylenen metnin birebir dökümü veya @dosya")
    args = parser.parse_args(argv)
    identity = aktar(ayarlar.load(args.ayarlar), args.ad, args.kayit, read_arg_text(args.metin))
    print(f"Ses eklendi: {identity}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

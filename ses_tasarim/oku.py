"""Adım 2: referanslı okuma. Tasarım kaydı motorun iki girişine birden (audio + voice_ref), yanında ses yaratılırken
okutulan metin (reference_text), okunacak metin ve sesin tohumu. Cümle cümle okunur, aralara durak konur.
Step 2: reference-based reading with the designed (or bundled) voice.

python -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti/deneme
python -m ses_tasarim.oku --ses deniz_feneri/2 --metin "Merhaba dünya." --cikti cikti/deneme
"""
import argparse
import json
import sys
import time
from pathlib import Path

from . import ayarlar, motor, okunus


def list_voices(settings: dict) -> dict:
    """{'hazir': [kart], 'tasarlanan': [kart]}; her kartta 'kimlik' ('hazir/<ad>' ya da '<ad>/<çeşit>') ve 'klasor'."""
    out = {"hazir": [], "tasarlanan": []}
    for folder in sorted(p for p in settings["hazir_sesler"].iterdir() if (p / "ses.json").is_file()):
        card = json.loads((folder / "ses.json").read_text(encoding="utf-8"))
        out["hazir"].append({**card, "kimlik": f"hazir/{folder.name}", "klasor": str(folder)})
    for voice in sorted(p for p in settings["sesler"].iterdir() if p.is_dir() and not p.name.startswith("_")):
        for trial in sorted(p for p in voice.glob("cesit_*") if (p / "ses.json").is_file()):
            card = json.loads((trial / "ses.json").read_text(encoding="utf-8"))
            number = int(trial.name.split("_")[1])
            out["tasarlanan"].append({**card, "kimlik": f"{voice.name}/{number}", "klasor": str(trial)})
    return out


def find_voice(settings: dict, identity: str) -> Path:
    """'hazir/<ad>', '<ad>/<çeşit>' ya da doğrudan klasör yolu. / Resolve a voice identity to its folder."""
    direct = Path(identity)
    if (direct / "ses.json").is_file():
        return direct
    if identity.startswith("hazir/"):
        folder = settings["hazir_sesler"] / identity[6:]
    elif "/" in identity:
        name, number = identity.rsplit("/", 1)
        folder = settings["sesler"] / name / f"cesit_{int(number):02d}"
    else:
        folder = settings["hazir_sesler"] / identity
        if not (folder / "ses.json").is_file():
            trials = sorted(settings["sesler"].joinpath(identity).glob("cesit_*"))
            folder = trials[-1] if trials else folder
    if not (folder / "ses.json").is_file():
        raise FileNotFoundError(f"ses bulunamadı: {identity} (bak: python -m ses_tasarim.oku --liste)")
    return folder


def oku(settings: dict, voice_dir: Path, text: str, out_dir: Path, progress=None) -> dict:
    found = okunus.problems(text)
    if found:
        raise ValueError("metin:\n  - " + "\n  - ".join(found))
    card = json.loads((voice_dir / "ses.json").read_text(encoding="utf-8"))
    seed = int(card["okuma_tohumu"])  # okumada sesin kendi tohumu sabittir (tutarlılık)
    parsed = okunus.lines(okunus.spoken(text))
    out_dir = Path(out_dir)
    work_dir = out_dir / "_motor"
    reference = motor.reference_wav(voice_dir / card.get("referans", "referans.wav"), work_dir)
    requests = [motor.read_request(f"s{index}", line, seed, reference, card["ses_yaratilirken_okutulan_metin"])
                for index, (line, _) in enumerate(parsed, 1)]
    result = motor.run_sequence(settings, requests, work_dir, progress)
    if result["bad"]:
        numbers = [int(b[1:]) for b in result["bad"]]
        raise motor.MotorHatasi(f"şu satırlar düzgün bitmedi (EOS yok): {numbers}; cümleyi kısalt ya da yeniden dene")
    audios = [result["audios"][r["id"]] for r in requests]
    joined = motor.join_lines(audios, [pause for _, pause in parsed])
    wav = out_dir / "okuma.wav"
    motor.write_wav(wav, joined)
    cursor, records = 0, []
    for index, (audio, (line, pause)) in enumerate(zip(audios, parsed), 1):
        start = cursor / motor.SAMPLE_RATE
        cursor += len(audio)
        records.append({"satir": index, "metin": line, "t0": round(start, 3), "t1": round(cursor / motor.SAMPLE_RATE, 3)})
        cursor += int(pause * motor.SAMPLE_RATE)
    summary = {"ses": card.get("ad"), "kimlik_klasoru": str(voice_dir), "tohum": seed, "adim": motor.FIXED["adim"],
               "cfg": motor.FIXED["cfg"], "ses_sn": round(len(joined) / motor.SAMPLE_RATE, 2),
               "sure_sn": result["seconds"], "vram_tepe_mb": result["vram_peak_mb"], "wav": str(wav),
               "satirlar": records, "yapay": True, "tarih": time.strftime("%Y-%m-%d %H:%M")}
    (out_dir / "ozet.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ayarlar")
    parser.add_argument("--liste", action="store_true", help="sesleri listele / list voices")
    parser.add_argument("--ses", help="hazir/<ad>, <ad>/<çeşit> ya da klasör")
    parser.add_argument("--metin", help="okunacak metin ya da @dosya; satır = cümle, 'cümle || paragraf' durak")
    parser.add_argument("--cikti", type=Path, help="çıktı klasörü (okuma.wav, ozet.json)")
    args = parser.parse_args(argv)
    settings = ayarlar.load(args.ayarlar)
    if args.liste:
        voices = list_voices(settings)
        for group, title in (("hazir", "Hazır sesler"), ("tasarlanan", "Tasarlanan sesler")):
            print(title)
            for card in voices[group]:
                print(f"  {card['kimlik']:28} tohum {card['okuma_tohumu']:<11} {card.get('tanitim_tr', card.get('ses_yaratici_ingilizce_prompt', ''))[:70]}")
        return 0
    if not (args.ses and args.metin and args.cikti):
        parser.error("--ses, --metin ve --cikti gerekli (ya da --liste)")
    text = Path(args.metin[1:]).read_text(encoding="utf-8") if args.metin.startswith("@") else args.metin
    voice_dir = find_voice(settings, args.ses)

    def progress(done, total, elapsed):
        print(f"  {done}/{total} cümle, {elapsed:.0f} sn", flush=True)

    summary = oku(settings, voice_dir, text, args.cikti, progress)
    print(f"bitti: {summary['ses_sn']} sn ses, {summary['sure_sn']} sn, VRAM tepe {summary['vram_tepe_mb']} MB → {summary['wav']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

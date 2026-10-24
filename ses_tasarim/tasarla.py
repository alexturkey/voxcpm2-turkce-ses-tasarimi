"""Adım 1: ses tasarımı. İngilizce tarif + ses yaratılırken okutulan Türkçe metin + çeşit sayısı → her çeşide bir tohum,
her tohum için bir tasarım kaydı (referans). / Step 1: voice design.

python -m ses_tasarim.tasarla --ad deniz_feneri --tarif "A calm Turkish woman..." --metin @metin.txt --cesit 3
python -m ses_tasarim.tasarla --ad narrator_fr --dil fr --tarif "A deep-voiced French man..." --metin @texte.txt --cesit 3

Tarif her dilde İngilizcedir; tasarım metni sesin konuşacağı dilde yazılır; dil kartta ("dil") saklanır ve okumada
kullanılır. / The description is always English; the design text is written in the voice's own language; the
language is stored in the card ("dil") and used when reading.
"""
import argparse
import json
import secrets
import sys
import time
from pathlib import Path

from . import ayarlar, motor, okunus

DEFAULT_VARIANTS = 3


def resolve_seeds(count: int = None, seeds: list = None) -> list:
    if seeds:
        return [int(s) for s in seeds]
    chosen = set()
    while len(chosen) < (count or DEFAULT_VARIANTS):
        chosen.add(secrets.randbelow(2**32))
    return sorted(chosen)


def slug(name: str) -> str:
    ascii_name = name.translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")).lower()
    return "_".join("".join(ch if ch.isalnum() else " " for ch in ascii_name).split()) or "ses"


def check(description: str, text: str, dil: str = okunus.DEFAULT_LANGUAGE) -> list:
    found = []
    if not description.strip():
        found.append("tarif boş")
    if "(" in description or ")" in description:
        found.append("tarifte parantez olmaz (motor parantezi tarif sınırı sayar)")
    found += okunus.problems(text, "ses yaratılırken okutulan metin", dil)
    return found


def tasarla(settings: dict, name: str, description: str, text: str, count: int = None, seeds: list = None,
            progress=None, dil: str = okunus.DEFAULT_LANGUAGE) -> dict:
    found = check(description, text, dil)
    if found:
        raise ValueError("form eksik:\n  - " + "\n  - ".join(found))
    dil = okunus.language(dil)
    spoken_text = " ".join(line for line, _ in okunus.lines(okunus.spoken(text, dil)))
    voice_dir = settings["sesler"] / slug(name)
    voice_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(p for p in voice_dir.glob("cesit_*") if p.is_dir())
    seeds = resolve_seeds(count, seeds)
    requests = [motor.design_request(f"t_{seed}", description, spoken_text, seed) for seed in seeds]
    work_dir = settings["onbellek"].parent / "_calisma" / f"tasarim_{time.strftime('%Y%m%d_%H%M%S')}"
    result = motor.run_sequence(settings, requests, work_dir, progress)
    variants, number = [], len(existing)
    for request in requests:
        if request["id"] in result["bad"]:
            variants.append({"tohum": request["seed"], "hata": "EOS gelmedi (yarım ses); başka tohumla yeniden dene"})
            continue
        number += 1
        audio = result["audios"][request["id"]]
        trial = voice_dir / f"cesit_{number:02d}"
        trial.mkdir()
        motor.write_wav(trial / "referans.wav", audio)
        seconds = round(len(audio) / motor.SAMPLE_RATE, 2)
        card = {"ad": voice_dir.name, "gorunen_ad": name.strip(), "cesit": number, "dil": dil,
                "ses_yaratici_ingilizce_prompt": description.strip(),
                "ses_yaratilirken_okutulan_metin": spoken_text,
                "tasarim_tohumu": request["seed"], "okuma_tohumu": request["seed"],
                "referans": "referans.wav", "referans_sn": seconds, "model": settings["model"].name,
                "adim": motor.FIXED["adim"], "cfg": motor.FIXED["cfg"], "yapay": True,
                "tarih": time.strftime("%Y-%m-%d %H:%M")}
        (trial / "ses.json").write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if seconds < motor.MIN_REFERENCE_SECONDS:
            card["uyari"] = f"referans {seconds} sn < {motor.MIN_REFERENCE_SECONDS} sn; tasarım metnini uzat"
        variants.append({**card, "klasor": str(trial)})
    return {"ses": voice_dir.name, "klasor": str(voice_dir), "cesitler": variants,
            "sure_sn": result["seconds"], "vram_tepe_mb": result["vram_peak_mb"]}


def read_arg_text(value: str) -> str:
    return Path(value[1:]).read_text(encoding="utf-8") if value.startswith("@") else value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ayarlar", help="ayar dosyası (varsayılan ./ayarlar.json)")
    parser.add_argument("--ad", required=True, help="sesin adı / voice name")
    parser.add_argument("--tarif", required=True, help="İngilizce ses tarifi (parantezsiz) ya da @dosya")
    parser.add_argument("--metin", required=True,
                        help="ses yaratılırken okutulan metin, sesin dilinde, ya da @dosya (rakamsız)")
    parser.add_argument("--dil", default=okunus.DEFAULT_LANGUAGE,
                        help="sesin dili / voice language: " + ", ".join(okunus.LANGUAGES) + " (varsayılan tr)")
    parser.add_argument("--cesit", type=int, default=DEFAULT_VARIANTS, help="çeşit sayısı / number of variants")
    parser.add_argument("--tohum", type=int, nargs="*", help="tohumları kendin ver / explicit seeds")
    args = parser.parse_args(argv)
    settings = ayarlar.load(args.ayarlar)
    description, text = read_arg_text(args.tarif), read_arg_text(args.metin)

    def progress(done, total, elapsed):
        print(f"  {done}/{total} çeşit, {elapsed:.0f} sn", flush=True)

    print(f"tasarım: {args.ad} ({args.dil}), {len(args.tohum) if args.tohum else args.cesit} çeşit, {motor.FIXED['adim']} adım, cfg {motor.FIXED['cfg']}",
          flush=True)
    result = tasarla(settings, args.ad, description, text, args.cesit, args.tohum, progress, args.dil)
    for variant in result["cesitler"]:
        if "hata" in variant:
            print(f"  tohum {variant['tohum']}: {variant['hata']}")
        else:
            print(f"  çeşit {variant['cesit']}: tohum {variant['tasarim_tohumu']}, {variant['referans_sn']} sn → {variant['klasor']}")
    print(f"süre {result['sure_sn']} sn, VRAM tepe {result['vram_tepe_mb']} MB")
    return 0 if all("hata" not in v for v in result["cesitler"]) else 1


if __name__ == "__main__":
    sys.exit(main())

"""Adım 1: ses tasarımı. İngilizce tarif + ses yaratılırken okutulan Türkçe metin + çeşit sayısı → her çeşide bir tohum,
her tohum için bir tasarım kaydı (referans). / Step 1: voice design.

python -m ses_tasarim.tasarla --ad deniz_feneri --tarif "A calm Turkish woman..." --metin @metin.txt --cesit 3
python -m ses_tasarim.tasarla --ad narrator_fr --dil fr --tarif "A deep-voiced French man..." --metin @texte.txt --cesit 3
python -m ses_tasarim.tasarla --ornek de_belgesel_erkek --cesit 3      # hazır örnek / ready example (ornekler.py)

Tarif her dilde İngilizcedir; tasarım metni sesin konuşacağı dilde yazılır; dil metinden tanınır (ya da --dil), kartta ("dil") saklanır ve okumada
kullanılır. / The description is always English; the design text is written in the voice's own language; the
language is stored in the card ("dil") and used when reading.
"""
import argparse
import json
import re
import secrets
import shutil
import sys
import time
import unicodedata
from pathlib import Path

from . import utf8_cikti, ayarlar, motor, okunus, ornekler

DEFAULT_VARIANTS = 3

# Tasarım metni sesi tanımak için kısa bir örnektir (1-2 cümle). VoxCPM2 tek üretimde ~25 sn'yi aşınca ritim bozulur
# (duraklama, es); uzun metin okuma adımında cümle cümle okunur. Arayüz 20 sn gösterir, %10 pay ile 22 sn üstü reddedilir.
# The design text is a short sample to get to know the voice (1-2 sentences). Past ~25 s in one generation VoxCPM2
# loses its rhythm; long text belongs in the reading step. The UI shows 20 s; above 22 s (10 % margin) it is rejected.
DESIGN_LIMIT_SECONDS = 20.0
DESIGN_HARD_LIMIT_SECONDS = DESIGN_LIMIT_SECONDS * 1.1
# Konuşma hızı, karakter/saniye (boşluk ve noktalama dahil, ardışık boşluk tek sayılır). Ölçüm 2026-10-31: hazır seslerin
# tasarım kaydı (metin + referans süresi) ve örnek okuması (metin + mp3 süresi, satır arası duraklar düşülerek).
# Speaking rate in characters per second (spaces and punctuation count, runs of whitespace count once), measured on the
# bundled voices' design recordings and sample readings.
CHARS_PER_SECOND = {
    "tr": 14.5,  # 78 tasarım kaydı medyanı 14,7 (10,5-18,9) + 7 okuma medyanı 14,0
    "en": 17.0,  # tasarım 16,0 + okuma 17,9 (tek ses)
    "de": 16.5,  # tasarım 16,4 + okuma 16,6 (tek ses)
    "fr": 21.5,  # tasarım 22,0 + okuma 21,2 (tek ses)
    "es": 13.5,  # tasarım 12,0 ve 13,8 + okuma 14,0
    "ru": 14.0,  # tasarım 13,2 + okuma 15,4 (tek ses)
    "ja": 7.5,   # tasarım 7,9 + okuma 7,6 (tek ses)
    "zh": 5.0,   # tasarım 5,3 + okuma 4,7 (tek ses)
    "ko": 7.0,   # ölçülmedi, varsayılan (hece yazısı, Japoncaya yakın) / not measured, default
}
DEFAULT_CHARS_PER_SECOND = 14.0  # ölçülmedi, varsayılan (diğer diller) / not measured, default for other languages
_HANGUL = re.compile("[ᄀ-ᇿ㄰-㆏가-힯]")


def estimate_seconds(text: str, dil: str = None) -> float:
    """Metnin okunuş süresi tahmini (sn), dile göre karakter hızıyla. dil yoksa metinden tanınır.
    Estimated spoken length in seconds from the character count and the language's rate."""
    text = re.sub(r"\s+", " ", text or "").strip()
    dil = dil or okunus.detect(text)
    if _HANGUL.search(text) and dil not in ("ja", "zh"):
        dil = "ko"  # okunus.detect Korece tanımaz / detect() has no Korean rule
    return round(len(text) / CHARS_PER_SECOND.get(dil, DEFAULT_CHARS_PER_SECOND), 1)


def resolve_seeds(count: int = None, seeds: list = None) -> list:
    if seeds:
        return [int(s) for s in seeds]
    chosen = set()
    while len(chosen) < (count or DEFAULT_VARIANTS):
        chosen.add(secrets.randbelow(2**32))
    return sorted(chosen)


def slug(name: str) -> str:
    ascii_name = name.translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")).lower()
    keep = lambda ch: unicodedata.category(ch)[0] in "LNM"  # M: Tay, Hint, Birman ünlü işaretleri harfin parçası
    return "_".join("".join(ch if keep(ch) else " " for ch in ascii_name).split()) or "ses"


def check(description: str, text: str, dil: str = None) -> list:
    found = []
    if not description.strip():
        found.append(okunus.Sorun("tarif boş", "tarif_bos"))
    if "(" in description or ")" in description:
        found.append(okunus.Sorun("tarifte parantez olmaz (motor parantezi tarif sınırı sayar)", "tarif_parantez"))
    dil = dil or okunus.detect(text)
    found += okunus.problems(text, "ses yaratılırken okutulan metin", dil)
    seconds = estimate_seconds(text, dil)
    if seconds > DESIGN_HARD_LIMIT_SECONDS:
        limit = round(DESIGN_LIMIT_SECONDS)
        found.append(okunus.Sorun(f"ses yaratılırken okutulan metin örnek için çok uzun (~{seconds:.0f} sn > {limit} sn); "
                                  "1-2 cümle yeter, uzun metni okuma adımında okut / design text too long, keep 1-2 "
                                  "sentences and read long text in the reading step",
                                  "tasarim_uzun", sn=round(seconds), sinir=limit))
    return found


def tasarla(settings: dict, name: str, description: str, text: str, count: int = None, seeds: list = None,
            progress=None, dil: str = None, dinleme: str = None) -> dict:
    """dil verilmezse metinden tanınır (okunus.detect). dinleme: her çeşidin kalıcı sesiyle (referans + kendi tohumu)
    okunacak metin; verilirse tasarımdan sonra okunur, çeşidin klasörüne dinleme.wav yazılır (kart: "Sürekli duyacağın
    ses bu"). / dinleme: text read with each variant's lasting voice (reference + its own seed) after the design."""
    dil = okunus.language(dil) if dil else okunus.detect(text)
    found = check(description, text, dil)
    dinleme = (dinleme or "").strip()
    if dinleme:
        found += okunus.problems(dinleme, "duymak istediğin metin", okunus.detect(dinleme, dil))
    if found:
        raise ValueError("form eksik:\n  - " + "\n  - ".join(found))
    spoken_text = " ".join(line for line, _ in okunus.lines(okunus.spoken(text, dil)))
    voice_dir = settings["sesler"] / slug(name)
    voice_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(p for p in voice_dir.glob("cesit_*") if p.is_dir())
    seeds = resolve_seeds(count, seeds)
    requests = [motor.design_request(f"t_{seed}", description, spoken_text, seed) for seed in seeds]
    work_dir = settings["onbellek"].parent / "_calisma" / f"tasarim_{time.strftime('%Y%m%d_%H%M%S')}"
    # İlerleme iki aşamayı tek sayaçta gösterir: önce tasarım, sonra okuma satırları / one counter for both phases
    lines = okunus.lines(okunus.spoken(dinleme, okunus.detect(dinleme, dil))) if dinleme else []
    total = len(requests) * (1 + len(lines))
    design_progress = (lambda done, _total, elapsed: progress(done, total, elapsed)) if progress else None
    result = motor.run_sequence(settings, requests, work_dir, design_progress)
    _remove_empty(work_dir)  # motor ara dosyalarını sildi; boş çalışma klasörü de kalmasın
    variants, number = [], len(existing)
    run_id, run_date = time.strftime("%Y%m%d_%H%M%S"), time.strftime("%Y-%m-%d %H:%M")  # bir Tasarla = bir üretim
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
                "tarih": run_date, "uretim": run_id}
        (trial / "ses.json").write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if seconds < motor.MIN_REFERENCE_SECONDS:
            card["uyari"] = f"referans {seconds} sn < {motor.MIN_REFERENCE_SECONDS} sn; tasarım metnini uzat"
        variants.append({**card, "klasor": str(trial)})
    seconds, vram = result["seconds"], result["vram_peak_mb"]
    good = [v for v in variants if "hata" not in v]
    if lines and good:
        # Yarım tasarım okunmaz: toplam küçülür, sayaç yine geri gitmez; saat tasarım süresinden devam eder.
        # Broken designs are not read: the total shrinks, the counter never goes back; the clock continues.
        total, base = len(requests) + len(good) * len(lines), result["seconds"] or 0
        read_progress = (lambda done, _total, elapsed: progress(len(requests) + done, total, base + elapsed)) if progress else None
        # Okuma dinleme metni kullanıcının yazdığıysa saklanır (üretim yeniden açılınca kutuya döner; örnek cümleyse boş kalır)
        typed = dinleme if dinleme != text.strip() else None
        try:
            read = _read_variants(settings, good, lines, work_dir.parent / f"{work_dir.name}_okuma", read_progress, typed)
            seconds, vram = round(seconds + read["seconds"], 1), motor.vram_max(vram, read["vram_peak_mb"])
        except motor.MotorHatasi as error:  # tasarım diske yazıldı, okumanın çökmesi onu düşürmez / keep the design
            for variant in good:
                _update_card(Path(variant["klasor"]), {"dinleme_hata": f"okuma motoru durdu: {error}"}, variant)
    return {"ses": voice_dir.name, "klasor": str(voice_dir), "cesitler": variants,
            "sure_sn": seconds, "vram_tepe_mb": vram}


def _update_card(trial: Path, fields: dict, variant: dict) -> None:
    card_path = trial / "ses.json"
    card = json.loads(card_path.read_text(encoding="utf-8"))
    card.update(fields)
    card_path.write_text(json.dumps(card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    variant.update(fields)


def _read_variants(settings: dict, variants: list, lines: list, work_dir: Path, progress=None, typed: str = None) -> dict:
    """Her çeşidin kalıcı sesi: tasarım kaydı referans, çeşidin kendi tohumu, aynı metin; hepsi tek motor oturumunda
    (model bir kez yüklenir). Çeşidin klasörüne dinleme.wav, kartına dinleme alanları yazılır. Yarım kalan çeşit
    tasarımı bozmaz, kartına dinleme_hata düşer.
    Each variant's lasting voice, all in one engine session; a failed reading does not fail the design."""
    requests = []
    for variant in variants:
        trial = Path(variant["klasor"])
        reference = motor.reference_wav(trial / variant["referans"], work_dir)
        requests += [motor.read_request(f"v{variant['cesit']}_s{index}", line, variant["okuma_tohumu"], reference,
                                        variant["ses_yaratilirken_okutulan_metin"])
                     for index, (line, _) in enumerate(lines, 1)]
    if not requests:
        return {"seconds": 0, "vram_peak_mb": None}
    result = motor.run_sequence(settings, requests, work_dir, progress)
    _remove_empty(work_dir)
    text = "\n".join(line for line, _ in lines)
    for variant in variants:
        ids = [f"v{variant['cesit']}_s{index}" for index in range(1, len(lines) + 1)]
        trial = Path(variant["klasor"])
        if any(i not in result["audios"] for i in ids):
            fields = {"dinleme_hata": "okuma yarım kaldı (EOS gelmedi); Bu sesle oku ile yeniden dene"}
        else:
            joined = motor.join_lines([result["audios"][i] for i in ids], [pause for _, pause in lines])
            motor.write_wav(trial / "dinleme.wav", joined)
            fields = {"dinleme": "dinleme.wav", "dinleme_metni": text, "dinleme_sn": round(len(joined) / motor.SAMPLE_RATE, 2)}
        if typed:
            fields["dinleme_girdi"] = typed  # kullanıcının yazdığı hali (durak işaretleri, boş satırlar) / as typed
        _update_card(trial, fields, variant)
    return result


def _remove_empty(folder: Path) -> None:
    """Boş kalan çalışma klasörünü ve boşsa üstündeki `_calisma` klasörünü siler (dolu klasöre dokunmaz)."""
    for path in (folder, folder.parent):
        try:
            path.rmdir()
        except OSError:
            return


def read_arg_text(value: str) -> str:
    return Path(value[1:]).read_text(encoding="utf-8") if value.startswith("@") else value


def main(argv=None) -> int:
    utf8_cikti()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ayarlar", help="ayar dosyası (varsayılan ./ayarlar.json)")
    parser.add_argument("--ornek", help="örnek tarif kimliği / example id (python -m ses_tasarim.ornekler): tarif, "
                        "metin, dil ve ad buradan gelir; --tarif / --metin / --ad verilirse onlar geçerli")
    parser.add_argument("--ad", help="sesin adı / voice name (--ornek ile isteğe bağlı)")
    parser.add_argument("--tarif", help="İngilizce ses tarifi (parantezsiz) ya da @dosya")
    parser.add_argument("--metin", help="ses yaratılırken okutulan metin, sesin dilinde, ya da @dosya (rakamsız)")
    parser.add_argument("--dil", default=None,
                        help="isteğe bağlı / optional: " + okunus.DIL_YARDIM + " (verilmezse metinden tanınır / auto-detected)")
    parser.add_argument("--cesit", type=int, default=DEFAULT_VARIANTS, help="çeşit sayısı / number of variants")
    parser.add_argument("--tohum", type=int, nargs="*", help="tohumları kendin ver / explicit seeds")
    parser.add_argument("--dinleme", help="her çeşidin kalıcı sesiyle okunacak metin ya da @dosya (satır = cümle); "
                        "çeşit klasörüne dinleme.wav / text read with each variant's lasting voice")
    args = parser.parse_args(argv)
    if args.ornek:
        item = ornekler.bul(args.ornek)
        args.ad = args.ad or item["id"]
        args.tarif = args.tarif or item["tarif"]
        args.metin = args.metin or item["metin"]
        args.dil = args.dil or item["dil"]
    missing = [f"--{k}" for k in ("ad", "tarif", "metin") if not getattr(args, k)]
    if missing:
        parser.error(", ".join(missing) + " gerekli (ya da --ornek) / required (or --ornek)")
    settings = ayarlar.load(args.ayarlar)
    description, text = read_arg_text(args.tarif), read_arg_text(args.metin)

    def progress(done, total, elapsed):
        print(f"  {done}/{total} hazır, {elapsed:.0f} sn", flush=True)

    print(f"tasarım: {args.ad} ({args.dil}), {len(args.tohum) if args.tohum else args.cesit} çeşit, {motor.FIXED['adim']} adım, cfg {motor.FIXED['cfg']}",
          flush=True)
    result = tasarla(settings, args.ad, description, text, args.cesit, args.tohum, progress, args.dil,
                     read_arg_text(args.dinleme) if args.dinleme else None)
    for variant in result["cesitler"]:
        if "hata" in variant:
            print(f"  tohum {variant['tohum']}: {variant['hata']}")
        else:
            print(f"  çeşit {variant['cesit']}: tohum {variant['tasarim_tohumu']}, {variant['referans_sn']} sn → {variant['klasor']}")
    print(f"süre {result['sure_sn']} sn, {motor.vram_metni(result['vram_tepe_mb'])}")
    return 0 if all("hata" not in v for v in result["cesitler"]) else 1


if __name__ == "__main__":
    sys.exit(main())

"""Örnek ses tarifleri: 18 rol × 8 dil. Tarif İngilizcedir ve içinde milliyet + yerli aksan geçer; tasarım metni
(ses yaratılırken okutulan metin) rolün türüne göre o dilde hazırdır. / Example voice prompts: 18 roles × 8 languages.

python -m ses_tasarim.ornekler            # hepsini listele / list all
python -m ses_tasarim.ornekler --dil de   # yalnız bir dil / one language

Kimlik / id: <dil>_<rol>, ör. de_belgesel_erkek. Tasarım: python -m ses_tasarim.tasarla --ornek de_belgesel_erkek
"""
import argparse
import json
import sys
from functools import lru_cache
from pathlib import Path

KLASOR = Path(__file__).with_name("ornek_tarifler")


@lru_cache(maxsize=1)
def _yukle() -> tuple:
    roles = json.loads((KLASOR / "roller.json").read_text(encoding="utf-8"))["roller"]
    langs = {}
    for path in sorted(KLASOR.glob("*.json")):
        if path.name != "roller.json":
            data = json.loads(path.read_text(encoding="utf-8"))
            langs[data["dil"]] = data
    return roles, langs


def diller() -> list:
    return sorted(_yukle()[1])


def listele(dil: str = None) -> list:
    """Her örnek: id, dil, rol, tur, cinsiyet, yas, ad_tr, ad_en, tarif, metin."""
    roles, langs = _yukle()
    out = []
    for code in ([dil] if dil else sorted(langs)):
        if code not in langs:
            raise ValueError(f"örnek tarif yok / no example prompts for: {code!r} ({', '.join(sorted(langs))})")
        lang = langs[code]
        for role in roles:
            tarif = role["sablon"].format(man=lang["man"], woman=lang["woman"], native=lang["native"])
            out.append({"id": f"{code}_{role['rol']}", "dil": code, "rol": role["rol"], "tur": role["tur"],
                        "cinsiyet": role["cinsiyet"], "yas": role["yas"], "ad_tr": role["ad_tr"],
                        "ad_en": role["ad_en"], "tarif": tarif, "metin": lang["metinler"][role["tur"]]})
    return out


def bul(ornek_id: str) -> dict:
    for item in listele():
        if item["id"] == ornek_id:
            return item
    raise ValueError(f"örnek bulunamadı / unknown example: {ornek_id!r} (liste: python -m ses_tasarim.ornekler)")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dil", help="yalnız bu dil / only this language: " + ", ".join(diller()))
    parser.add_argument("--tam", action="store_true", help="tarif ve metni de yaz / print prompt and text too")
    args = parser.parse_args(argv)
    for item in listele(args.dil):
        print(f"{item['id']:<28} {item['cinsiyet']:<6} {item['yas']:<4} {item['ad_tr']} / {item['ad_en']}")
        if args.tam:
            print(f"    tarif: {item['tarif']}\n    metin: {item['metin']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

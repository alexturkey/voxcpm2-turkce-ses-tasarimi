"""Arayüz dilleri: 30 dil dosyası, anahtar ve yer tutucu tutarlılığı (GPU ve ağ gerekmez).
Interface languages: 30 language files, key and placeholder consistency (no GPU, no network).

python -m unittest discover -s tests -v
"""
import json
import re
import unittest
from pathlib import Path

from ses_tasarim import arayuz

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "ses_tasarim" / "arayuz_dilleri"
FLAGS = ROOT / "ses_tasarim" / "bayraklar"
DILLER = re.findall(r"\['([a-z]{2})',\s*'([a-z]{2})'", arayuz.HTML.split("const DILLER", 1)[1].split("];", 1)[0])
SOURCE = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "ses_tasarim").glob("*.py"))
CODES = {"ad_bos", "tarif_bos", "tarif_parantez", "isaret_tr", "isaret", "uzun_satir", "bos", "onay_yok",
         "kayit_metni", "kayit_yok", "kayit_buyuk", "ses_yok", "durak", "kayit_kisa", "kayit_cozulemedi",
         "not_kirpildi", "not_oneri", "tasarim_uzun"}
STATES = {"sirada", "yukleniyor", "ilerleme", "bitti_tasarla", "bitti_klon", "bitti", "is_yok"}


def load(code):
    return json.loads((DIR / f"{code}.json").read_text(encoding="utf-8"))


def holes(text):
    return sorted(re.findall(r"\{\w+\}", text))


class ArayuzDilleri(unittest.TestCase):
    def test_thirty_languages_with_flags(self):
        self.assertEqual(len(DILLER), 30)
        self.assertEqual({c for c, _ in DILLER}, {p.stem for p in DIR.glob("*.json")})
        for _, flag in DILLER:
            self.assertTrue((FLAGS / f"{flag}.svg").is_file(), flag)

    def test_same_keys_and_placeholders(self):
        ref = load("tr")
        for code, _ in DILLER:
            data = load(code)
            self.assertEqual(set(data), set(ref), code)
            for key, text in data.items():
                self.assertTrue(text.strip(), f"{code}.{key}")
                self.assertEqual(holes(text), holes(ref[key]), f"{code}.{key}")
            self.assertIn("|| paragraf", data["ometin"], code)

    def test_every_used_key_exists(self):
        ref = load("tr")
        used = set(re.findall(r'data-(?:t(?:-ph|-val|-title|-bas)?|sekme-t)="([a-z_0-9]+)"', arayuz.HTML))
        used |= set(re.findall(r"\bt\('([a-z_0-9]*[a-z0-9])'", arayuz.HTML))
        used |= {f"e_{c}" for c in CODES} | {f"d_{s}" for s in STATES}
        self.assertFalse(used - set(ref), used - set(ref))

    def test_server_codes_are_translated(self):
        for code in CODES:
            self.assertIn(f'"{code}"', SOURCE, code)
        for state in STATES:
            self.assertIn(f'"{state}"', SOURCE, state)


if __name__ == "__main__":
    unittest.main()

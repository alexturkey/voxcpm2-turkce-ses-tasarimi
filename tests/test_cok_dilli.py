"""Çok dilli metin hazırlığı ve hazır ses kartları (GPU ve ağ gerekmez).
Multilingual text preparation and bundled voice cards (no GPU, no network).

python -m unittest discover -s tests -v
"""
import json
import unittest
from pathlib import Path

from ses_tasarim import oku, okunus

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {"tr": "Kapadokya, Anadolunun tam kalbinde.",
           "en": "Cappadocia is one of those places.",
           "fr": "La Cappadoce est l'un de ces lieux.",
           "de": "Kappadokien ist so ein Ort.",
           "es": "Capadocia es uno de esos lugares.",
           "ru": "Каппадокия — именно такое место.",
           "zh": "卡帕多奇亚就是这样的地方。",
           "ja": "カッパドキアは、そんな場所です。"}


class Languages(unittest.TestCase):
    def test_all_eight_languages_listed(self):
        self.assertEqual(set(SAMPLES), set(okunus.LANGUAGES))

    def test_sample_sentence_passes_and_is_unchanged(self):
        for dil, text in SAMPLES.items():
            with self.subTest(dil=dil):
                self.assertEqual(okunus.problems(text, dil=dil), [])
                self.assertEqual(okunus.spoken(text, dil), text)

    def test_apostrophe_kept_outside_turkish(self):
        self.assertIn("l'un", okunus.spoken("«La Cappadoce» est l'un de ces lieux.", "fr"))
        self.assertTrue(okunus.problems("La Cappadoce est l'un de ces lieux.", dil="tr"))

    def test_turkish_dictionary_not_applied_to_foreign_text(self):
        rules = okunus.load_rules()
        if not rules:
            self.skipTest("okunuş sözlüğü boş / dictionary empty")
        written = rules[-1][0]
        self.assertEqual(okunus.spoken(written, "en"), written)

    def test_digits_rejected_in_every_language(self):
        for dil in SAMPLES:
            self.assertTrue(okunus.problems("1990", dil=dil), dil)

    def test_bad_code(self):
        self.assertTrue(okunus.problems("hello", dil="english!"))


class SpeedGate(unittest.TestCase):
    def test_outlier_found(self):
        records = [{"satir": i, "metin": "x" * 40, "t0": 0.0, "t1": d} for i, d in enumerate([3, 3.2, 2.9, 9, 3.1], 1)]
        self.assertEqual(oku.speed_outliers(records), [4])


class BundledVoices(unittest.TestCase):
    def test_every_language_has_a_voice(self):
        cards = [json.loads(p.read_text(encoding="utf-8")) for p in ROOT.glob("hazir_sesler/*/ses.json")]
        self.assertEqual({c.get("dil", "tr") for c in cards}, set(SAMPLES))

    def test_cards_complete(self):
        for path in ROOT.glob("hazir_sesler/*/ses.json"):
            card = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(voice=path.parent.name):
                for key in ("ses_yaratici_ingilizce_prompt", "ses_yaratilirken_okutulan_metin", "okuma_tohumu", "referans"):
                    self.assertTrue(card.get(key), key)
                self.assertEqual((card["adim"], card["cfg"]), (16, 2.0))
                self.assertTrue((path.parent / card["referans"]).is_file())
                if card.get("ornek_okuma"):
                    self.assertTrue((path.parent / card["ornek_okuma"]).is_file())
                if card.get("dil"):  # çok dilli kartlar / multilingual cards
                    self.assertEqual(okunus.problems(card["ses_yaratilirken_okutulan_metin"], dil=card["dil"]), [])
                self.assertLess(sum(f.stat().st_size for f in path.parent.iterdir()), 2_500_000)


if __name__ == "__main__":
    unittest.main()

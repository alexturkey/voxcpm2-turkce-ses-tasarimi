"""Hata imza dosyasi (kit KL-13) kodla ve belgeyle ayni kalir / error signatures stay in step with the code and the doc."""
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOSYA = {"kur.ps1": REPO / "scripts" / "kur.ps1", "oku.py": REPO / "ses_tasarim" / "oku.py", "okunus.py": REPO / "ses_tasarim" / "okunus.py"}


class HataImzalari(unittest.TestCase):
    def setUp(self):
        self.veri = json.loads((REPO / "docs" / "hata_imzalari.json").read_text(encoding="utf-8"))
        self.hatalar = self.veri["hatalar"]

    def test_kodlar_tekil_ve_bicimli(self):
        kodlar = [h["kod"] for h in self.hatalar]
        self.assertEqual(len(kodlar), len(set(kodlar)))
        for k in kodlar:
            self.assertRegex(k, r"^SES-E-[A-Z0-9-]+$")

    def test_alanlar_dolu_ve_iki_dil(self):
        for h in self.hatalar:
            for alan in ("kod", "imza", "kaynak", "ilk_adim_en", "ilk_adim_tr"):
                self.assertTrue(h.get(alan), (h.get("kod"), alan))
            self.assertIn(h["kaynak"], ("repo", "motor", "isletim_sistemi"))

    def test_repo_kaynakli_imza_gercekten_kodda_var(self):
        for h in self.hatalar:
            if h["kaynak"] != "repo":
                continue
            yol = DOSYA[h["betik"]]
            metin = yol.read_text(encoding="utf-8-sig")
            aranan = h.get("kodda", h["imza"])
            with self.subTest(kod=h["kod"]):
                self.assertIn(aranan, metin, "%s: %r %s icinde yok (kod degisti, imza kaydi eskidi)" % (h["kod"], aranan, h["betik"]))

    def test_her_kod_sik_hatalar_belgesinde(self):
        belge = (REPO / "docs" / "SIK_HATALAR.md").read_text(encoding="utf-8")
        for h in self.hatalar:
            self.assertIn(h["kod"], belge, h["kod"])
        self.assertEqual(len(set(re.findall(r"SES-E-[A-Z0-9-]+", belge))), len(self.hatalar))


if __name__ == "__main__":
    unittest.main()

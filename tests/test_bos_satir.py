"""Boş satır paragraf durağı sayılır; açık '||' işareti korunur (GPU gerekmez).
A blank line becomes a paragraph pause; an explicit '||' marker wins (no GPU).
"""
import unittest

from ses_tasarim import okunus


class BosSatir(unittest.TestCase):
    def test_bos_satir_paragraf(self):
        self.assertEqual(okunus.lines("Bir.\n\nIki.\nUc."),
                         [("Bir.", okunus.PAUSES["paragraf"]), ("Iki.", okunus.GAP_SECONDS), ("Uc.", okunus.GAP_SECONDS)])

    def test_acik_isaret_korunur(self):
        self.assertEqual(okunus.lines("Bir. || agir\n\n\nIki."),
                         [("Bir.", okunus.PAUSES["agir"]), ("Iki.", okunus.GAP_SECONDS)])

    def test_uzun_satir_numarasi_fiziksel(self):
        found = okunus.problems("Bir.\n\nIki.\n\n" + "y " * 1100)
        self.assertEqual([f.veri["satir"] for f in found if f.kod == "uzun_satir"], [5])

    def test_ozel_sure(self):
        self.assertEqual(okunus.lines("Bir. || 0,8\nIki. || 1.2s\nUc."),
                         [("Bir.", 0.8), ("Iki.", 1.2), ("Uc.", okunus.GAP_SECONDS)])
        self.assertFalse([f for f in okunus.problems("Bir. || 0,8\nIki.") if f.kod == "isaret_tr"])
        with self.assertRaises(ValueError):
            okunus.lines("Bir. || 9\nIki.")

    def test_bastaki_bos_satir_etkisiz(self):
        self.assertEqual(okunus.lines("\n\nBir.\nIki."), [("Bir.", okunus.GAP_SECONDS), ("Iki.", okunus.GAP_SECONDS)])


if __name__ == "__main__":
    unittest.main()

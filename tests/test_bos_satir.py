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

    def test_bastaki_bos_satir_etkisiz(self):
        self.assertEqual(okunus.lines("\n\nBir.\nIki."), [("Bir.", okunus.GAP_SECONDS), ("Iki.", okunus.GAP_SECONDS)])


if __name__ == "__main__":
    unittest.main()

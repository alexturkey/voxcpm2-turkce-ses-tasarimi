"""Taslaklar: ekle, üzerine yaz, yeniden adlandır, sil; sınırlar ve bozuk dosya (GPU'suz).
Drafts: add, overwrite, rename, delete; limits and a corrupt file (no GPU).

python -m unittest discover -s tests -v
"""
import shutil
import tempfile
import unittest
from pathlib import Path

from ses_tasarim import taslaklar


class Taslaklar(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.ayar = {"sesler": self.tmp / "sesler"}

    def test_akis(self):
        self.assertEqual(taslaklar.oku(self.ayar), [])
        liste = taslaklar.degistir(self.ayar, "ekle", ad="  Ece   tanıtım ", metin="Merhaba. || 1\r\nİkinci satır.")
        self.assertEqual((liste[0]["ad"], liste[0]["metin"]), ("Ece tanıtım", "Merhaba. || 1\nİkinci satır."))
        kimlik = liste[0]["id"]
        taslaklar.degistir(self.ayar, "ekle", ad="İkinci", metin="Bir.")
        self.assertEqual([x["ad"] for x in taslaklar.oku(self.ayar)], ["İkinci", "Ece tanıtım"])  # yeni en üstte
        taslaklar.degistir(self.ayar, "guncelle", kimlik, metin="Yeni metin.")
        taslaklar.degistir(self.ayar, "ad", kimlik, ad="Ece 2")
        x = next(x for x in taslaklar.oku(self.ayar) if x["id"] == kimlik)
        self.assertEqual((x["ad"], x["metin"]), ("Ece 2", "Yeni metin."))
        self.assertEqual(len(taslaklar.degistir(self.ayar, "sil", kimlik)), 1)
        self.assertFalse((self.tmp / "sesler" / "taslaklar.json.tmp").exists())

    def test_sinirlar(self):
        for islem, kw in (("ekle", {"ad": "", "metin": "a"}), ("ekle", {"ad": "a", "metin": "  "}),
                          ("ekle", {"ad": "x" * 61, "metin": "a"}), ("sil", {"kimlik": "yok"}), ("uydur", {"kimlik": "yok"})):
            with self.assertRaises(ValueError):
                taslaklar.degistir(self.ayar, islem, **kw)

    def test_bozuk_dosya(self):
        (self.tmp / "sesler").mkdir()
        (self.tmp / "sesler" / "taslaklar.json").write_text("{bozuk", encoding="utf-8")
        self.assertEqual(taslaklar.oku(self.ayar), [])
        self.assertEqual(len(taslaklar.degistir(self.ayar, "ekle", ad="a", metin="b")), 1)


if __name__ == "__main__":
    unittest.main()

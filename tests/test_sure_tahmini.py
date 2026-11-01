"""Süre tahmini testi (GPU ve ağ gerekmez). / Duration estimate test (no GPU, no network).

Varsayılanla başlar, ilk ölçüm varsayılanın yerine geçer, sonrakiler üstel ortalamayla girer; açılış hızdan ayrılır;
sesin kendi katsayısı öğrenilir; aykırı ölçüm ve bozuk dosya modeli bozmaz.

python -m unittest discover -s tests -v
"""
import json
import tempfile
import unittest
from pathlib import Path

from ses_tasarim import sure_tahmini as st


class SureTahmini(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ayar = {"onbellek": Path(self.tmp.name) / "onbellek"}

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_then_learns(self):
        self.assertEqual(st.tahmin(self.ayar, "oku", 1000), {"sn": 235.0, "n": 0})  # 35 + 1000 × 0.2
        # 4 cümle, 1000 karakter: açılış 20 sn, sonra cümle başına 25 sn (250 kr) → 0.1 sn/kr; motor 0 biten de bildirir
        self.assertTrue(st.kaydet(self.ayar, "oku", 1000, [(0, 4, 3), (0, 4, 30), (1, 4, 45), (2, 4, 70), (3, 4, 95)], 120))
        m = json.loads((self.ayar["onbellek"] / "sure_olcumu.json").read_text(encoding="utf-8"))["oku"]
        self.assertEqual((m["acilis"], m["sn_karakter"], m["n"]), (20.0, 0.1, 1))
        self.assertEqual(st.tahmin(self.ayar, "oku", 1000)["sn"], 120.0)
        # İkinci ölçüm %30 ağırlıkla girer / the second measurement weighs 30 %
        st.kaydet(self.ayar, "oku", 1000, [(0, 2, 10), (1, 2, 70)], 120)  # açılış 20, 0.1 sn/kr: aynı
        st.kaydet(self.ayar, "oku", 1000, [(0, 4, 3), (2, 4, 72)], 120)  # ilk görülen anda 2 parça birden bitmiş
        self.assertEqual(st.tahmin(self.ayar, "oku", 1000)["sn"], 120.0)

    def test_voice_factor_and_kinds(self):
        st.kaydet(self.ayar, "oku", 1000, [(1, 4, 45)], 120)
        st.kaydet(self.ayar, "oku", 1000, [(1, 4, 85)], 240, "yavas/1")  # bu ses iki kat sürüyor
        self.assertGreater(st.tahmin(self.ayar, "oku", 1000, "yavas/1")["sn"], st.tahmin(self.ayar, "oku", 1000)["sn"] * 1.5)
        self.assertEqual(st.tahmin(self.ayar, "tasarla", 100)["n"], 0)  # tasarla ayrı model / separate per kind
        self.assertEqual(st.karakter("ab c\nd", 3), 12)

    def test_outlier_and_broken_file(self):
        for _ in range(3):
            st.kaydet(self.ayar, "oku", 1000, [(1, 4, 45)], 120)
        once = st.tahmin(self.ayar, "oku", 1000)
        self.assertFalse(st.kaydet(self.ayar, "oku", 1000, [(1, 4, 500)], 900))  # GPU başka işte gibi
        self.assertEqual(st.tahmin(self.ayar, "oku", 1000), once)
        # Art arda üç aykırı: makine değişmiş, model yeniden kurulur / three outliers in a row rebuild the model
        st.kaydet(self.ayar, "oku", 1000, [(1, 4, 500)], 900)
        self.assertTrue(st.kaydet(self.ayar, "oku", 1000, [(1, 4, 500)], 900))
        self.assertEqual(st.tahmin(self.ayar, "oku", 1000)["n"], 1)
        self.assertGreater(st.tahmin(self.ayar, "oku", 1000)["sn"], 800)
        (self.ayar["onbellek"] / "sure_olcumu.json").write_text("{bozuk", encoding="utf-8")
        self.assertEqual(st.tahmin(self.ayar, "oku", 1000)["n"], 0)
        self.assertFalse(st.kaydet(self.ayar, "oku", 0, [(1, 1, 5)], 5))
        st.kaydet(self.ayar, "oku", 100, [(0, 1, 3)], 40)  # tek parça: açılış eskisi kalır, hız sonradan / single part


if __name__ == "__main__":
    unittest.main()

"""Tasarımla birlikte kalıcı ses okuması (GPU'suz; motor taklit edilir).

Her çeşit tasarlanır, sonra aynı metni kendi referansı ve tohumuyla tek motor oturumunda okur: çeşit klasörüne
dinleme.wav, kartına dinleme alanları. Yarım kalan okuma tasarımı bozmaz; ilerleme iki aşamayı tek sayaçta sayar;
metin boşsa sunucu örnek cümleyi okutur.
Design plus the lasting-voice reading (no GPU, the engine is faked).

python -m unittest discover -s tests -v
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from ses_tasarim import arayuz, motor, tasarla

TARIF = "A warm young woman, clear studio voice."
METIN = "Merhaba, ben yeni sesim. Bugün sizinle tanışmaya geldim."


class Dinleme(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.settings = {"sesler": self.tmp / "sesler", "onbellek": self.tmp / "onbellek", "model": Path("model.gguf")}
        self.oturumlar, self.adimlar, self.yarim = [], [], set()

    def _sahte(self, settings, requests, work_dir, progress=None):
        self.oturumlar.append([dict(r) for r in requests])
        if progress:
            for i in range(len(requests) + 1):
                progress(i, len(requests), float(i))
        bad = [r["id"] for r in requests if r["id"] in self.yarim]
        return {"audios": {r["id"]: np.full(48000, 0.1, dtype=np.float32) for r in requests if r["id"] not in bad},
                "bad": bad, "seconds": 2.0, "vram_peak_mb": 900}

    def _tasarla(self, dinleme, seeds=(11, 22)):
        with mock.patch.object(motor, "run_sequence", self._sahte):
            return tasarla.tasarla(self.settings, "Deneme", TARIF, METIN, seeds=list(seeds),
                                   progress=lambda *a: self.adimlar.append(a), dil="tr", dinleme=dinleme)

    def test_her_cesit_kendi_sesiyle_okur(self):
        sonuc = self._tasarla("Birinci cümle.\nİkinci cümle.")
        self.assertEqual(len(self.oturumlar), 2)  # tasarım + tek okuma oturumu / design + one reading session
        okuma = self.oturumlar[1]
        self.assertEqual([r["id"] for r in okuma], ["v1_s1", "v1_s2", "v2_s1", "v2_s2"])
        self.assertEqual([r["seed"] for r in okuma], [11, 11, 22, 22])
        self.assertTrue(okuma[0]["voice_ref"].endswith(str(Path("cesit_01") / "referans.wav")))
        self.assertEqual(okuma[0]["reference_text"], METIN)
        for cesit in sonuc["cesitler"]:
            kart = json.loads((Path(cesit["klasor"]) / "ses.json").read_text(encoding="utf-8"))
            self.assertEqual((kart["dinleme"], kart["dinleme_metni"]), ("dinleme.wav", "Birinci cümle.\nİkinci cümle."))
            self.assertTrue((Path(cesit["klasor"]) / "dinleme.wav").is_file())
            self.assertGreater(kart["dinleme_sn"], 2)  # iki satır + aradaki durak / two lines and the pause
            self.assertEqual(cesit["dinleme"], "dinleme.wav")
        # tek sayaç: toplam 2 çeşit × (1 tasarım + 2 satır) = 6, hiç geri gitmez / one counter, never goes back
        self.assertEqual({a[1] for a in self.adimlar}, {6})
        self.assertEqual([a[0] for a in self.adimlar], sorted(a[0] for a in self.adimlar))
        self.assertEqual(self.adimlar[-1][0], 6)
        self.assertEqual(sonuc["sure_sn"], 4.0)

    def test_yarim_okuma_tasarimi_bozmaz(self):
        self.yarim = {"v2_s1"}
        sonuc = self._tasarla("Tek cümle.")
        ilk, ikinci = sonuc["cesitler"]
        self.assertEqual(ilk["dinleme"], "dinleme.wav")
        self.assertNotIn("dinleme", ikinci)
        self.assertIn("dinleme_hata", ikinci)
        self.assertTrue((Path(ikinci["klasor"]) / "referans.wav").is_file())
        self.assertFalse((Path(ikinci["klasor"]) / "dinleme.wav").exists())

    def test_okuma_motoru_cokse_tasarim_kalir(self):
        asil = self._sahte

        def coken(settings, requests, work_dir, progress=None):
            if requests[0]["id"].startswith("v"):
                raise motor.MotorHatasi("bellek yetmedi")
            return asil(settings, requests, work_dir, progress)

        self._sahte = coken
        sonuc = self._tasarla("Tek cümle.")
        for cesit in sonuc["cesitler"]:
            self.assertIn("bellek yetmedi", cesit["dinleme_hata"])
            kart = json.loads((Path(cesit["klasor"]) / "ses.json").read_text(encoding="utf-8"))
            self.assertIn("dinleme_hata", kart)
            self.assertTrue((Path(cesit["klasor"]) / "referans.wav").is_file())

    def test_yazilan_metin_saklanir_ornek_cumle_saklanmaz(self):
        self.assertEqual(self._tasarla("Bir.\n\nİki. || agir")["cesitler"][0]["dinleme_girdi"], "Bir.\n\nİki. || agir")
        self.assertNotIn("dinleme_girdi", self._tasarla(METIN)["cesitler"][0])  # boş kutu: örnek cümle okundu

    def test_yarim_tasarim_toplami_kucultur(self):
        self.yarim = {"t_22"}
        self._tasarla("Bir.\nİki.")
        self.assertEqual(self.adimlar[-1][:2], (4, 4))  # 2 tasarım + 1 iyi çeşit × 2 satır / bar reaches the end
        self.assertEqual([a[2] for a in self.adimlar], sorted(a[2] for a in self.adimlar))  # saat geri gitmez

    def test_metinsiz_eski_davranis(self):
        sonuc = self._tasarla(None)
        self.assertEqual(len(self.oturumlar), 1)
        self.assertNotIn("dinleme", sonuc["cesitler"][0])

    def test_rakamli_metin_reddedilir(self):
        with self.assertRaises(ValueError):
            self._tasarla("Fiyatı 25 lira.")
        self.assertEqual(self.oturumlar, [])  # motor hiç açılmadı / the engine never started

    def test_sunucu_bos_metinde_ornek_cumle(self):
        self.assertEqual(arayuz._dinleme({"metin": METIN, "dinleme": "  "}), METIN)
        self.assertEqual(arayuz._dinleme({"metin": METIN, "dinleme": "Başka."}), "Başka.")
        # süre tahmini iki okumayı da sayar / the estimate counts both readings
        self.assertGreater(arayuz._karakter("tasarla", {"metin": METIN, "dinleme": "Uzun bir dinleme metni.", "cesit": 2}),
                           arayuz._karakter("tasarla", {"metin": METIN, "dinleme": "Kısa.", "cesit": 2}))


if __name__ == "__main__":
    unittest.main()

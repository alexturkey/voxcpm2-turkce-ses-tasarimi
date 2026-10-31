"""Tasarım metni süre sınırı: dile göre süre tahmini, sunucu reddi, arayüz parçaları (GPU ve ağ gerekmez).
Design-text length limit: per-language estimate, server rejection, UI pieces (no GPU, no network).

python -m unittest discover -s tests -v
"""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from ses_tasarim import arayuz, ornekler, tasarla

TARIF = "A calm woman in her forties with a warm, low voice, clean studio recording, no background noise"
TR_KISA = "Merhaba, ben bir belgesel anlatıcısıyım. Yıllardır tarihin derinliklerinden hikâyeler anlatırım."
TR_UZUN = " ".join([TR_KISA] * 5)  # ~490 karakter, ~34 sn


class SureTahmini(unittest.TestCase):
    def test_turkce(self):
        self.assertAlmostEqual(tasarla.estimate_seconds("a" * 145, "tr"), 10.0)
        self.assertAlmostEqual(tasarla.estimate_seconds(TR_KISA), round(len(TR_KISA) / 14.5, 1))

    def test_ingilizce(self):
        text = "Hello, I am a documentary narrator. For years I have told stories from the depths of history."
        self.assertAlmostEqual(tasarla.estimate_seconds(text), round(len(text) / 17.0, 1))

    def test_cince_ve_korece_ayri_hiz(self):
        zh = "大家好，我是一名纪录片解说员。多年来，我一直在讲述来自历史深处的故事。"
        self.assertAlmostEqual(tasarla.estimate_seconds(zh), round(len(zh) / 5.0, 1))
        # aynı karakter sayısında Çince Latin yazıdan çok daha uzun sürer / CJK is far slower per character
        self.assertGreater(tasarla.estimate_seconds(zh), 2.5 * tasarla.estimate_seconds("a" * len(zh), "en"))
        ko = "안녕하세요, 다큐멘터리 내레이터입니다."
        self.assertAlmostEqual(tasarla.estimate_seconds(ko), round(len(ko) / 7.0, 1))

    def test_bosluklar_tek_sayilir_ve_olculmeyen_dil_varsayilan(self):
        self.assertEqual(tasarla.estimate_seconds("  bir   iki\n\nüç  ", "tr"), tasarla.estimate_seconds("bir iki üç", "tr"))
        self.assertAlmostEqual(tasarla.estimate_seconds("a" * 140, "sw"), 10.0)
        self.assertEqual(tasarla.estimate_seconds(""), 0.0)

    def test_hazir_ornekler_sinirin_altinda(self):
        for item in ornekler.listele():
            with self.subTest(item["id"]):
                self.assertLessEqual(tasarla.estimate_seconds(item["metin"], item["dil"]), tasarla.DESIGN_LIMIT_SECONDS)


class SinirDenetimi(unittest.TestCase):
    def test_uzun_metin_reddedilir_kisa_ve_hafif_asan_gecer(self):
        self.assertEqual(tasarla.check(TARIF, TR_KISA, "tr"), [])
        found = tasarla.check(TARIF, TR_UZUN, "tr")
        self.assertEqual([p.kod for p in found], ["tasarim_uzun"])
        self.assertEqual(found[0].veri["sinir"], 20)
        # 20 sn'yi %10'a kadar aşan metin geçer (arayüzle aynı pay) / up to 10 % over the limit is allowed
        self.assertEqual(tasarla.check(TARIF, "a" * int(14.5 * 21.5), "tr"), [])
        self.assertTrue(tasarla.check(TARIF, "a" * int(14.5 * 22.5), "tr"))


def _post(base, path, body):
    req = urllib.request.Request(base + path, json.dumps(body).encode("utf-8"),
                                 {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


class Sunucu(unittest.TestCase):
    def test_api_sure_ve_tasarla_siniri(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = {"hazir_sesler": Path(tmp), "sesler": Path(tmp)}
            server = ThreadingHTTPServer(("127.0.0.1", 0), arayuz.make_handler(settings, None))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                base = f"http://127.0.0.1:{server.server_address[1]}"
                code, sure = _post(base, "/api/sure", {"metin": TR_KISA})
                self.assertEqual(code, 200)
                self.assertEqual((sure["dil"], sure["sinir"], sure["sert"]), ("tr", 20.0, 22.0))
                self.assertEqual(sure["sn"], tasarla.estimate_seconds(TR_KISA, "tr"))
                code, sure = _post(base, "/api/sure", {"metin": TR_UZUN})
                self.assertGreater(sure["sn"], sure["sert"])
                # jobs=None: geçerli istek iş kuyruğuna gider, uzun metin oraya varmadan 400 döner
                code, cevap = _post(base, "/api/tasarla", {"ad": "deneme", "tarif": TARIF, "metin": TR_UZUN})
                self.assertEqual(code, 400)
                self.assertEqual([s["kod"] for s in cevap["sorunlar"]], ["tasarim_uzun"])
            finally:
                server.shutdown()
                server.server_close()

    def test_arayuz_parcalari(self):
        for parca in ('id="sure"', 'id="uzun_uyari"', 'id="okumaya_tasi"', 'id="tmetin_ipucu"', 'rows="3"',
                      "'/api/sure'", "sekmeAc('p2')"):
            self.assertIn(parca, arayuz.HTML)


if __name__ == "__main__":
    unittest.main()

"""Örnek ses tarifleri (GPU ve ağ gerekmez). / Example voice prompts (no GPU, no network).

python -m unittest discover -s tests -v
"""
import json
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from ses_tasarim import arayuz, okunus, ornekler, tasarla

# Tasarım metni referans olur; MIN_REFERENCE_SECONDS (8 sn) altına düşmemesi için yeterince uzun olmalı.
# The design text becomes the reference; long enough to stay above 8 s.
MIN_WORDS, MIN_CJK_CHARS = 28, 70


class OrnekTarifler(unittest.TestCase):
    def test_her_dil_ayni_roller(self):
        self.assertEqual(ornekler.diller(), sorted(okunus.LANGUAGES))
        items = ornekler.listele()
        self.assertEqual(len(items), 18 * len(okunus.LANGUAGES))
        self.assertEqual(len({i["id"] for i in items}), len(items))

    def test_tarif_ve_metin_tasarim_denetiminden_gecer(self):
        for item in ornekler.listele():
            with self.subTest(item["id"]):
                self.assertEqual(tasarla.check(item["tarif"], item["metin"], item["dil"]), [])
                self.assertNotIn("{", item["tarif"])
                self.assertIn("native", item["tarif"])

    def test_metin_referans_icin_yeterince_uzun(self):
        for item in ornekler.listele():
            with self.subTest(item["id"]):
                if item["dil"] in ("zh", "ja"):
                    self.assertGreaterEqual(len(item["metin"]), MIN_CJK_CHARS)
                else:
                    self.assertGreaterEqual(len(item["metin"].split()), MIN_WORDS)

    def test_bul(self):
        item = ornekler.bul("de_belgesel_erkek")
        self.assertEqual(item["dil"], "de")
        self.assertIn("German man", item["tarif"])
        with self.assertRaises(ValueError):
            ornekler.bul("xx_yok")


class ArayuzOrnekler(unittest.TestCase):
    def test_api_ornekler_ve_secim_kutusu(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = {"hazir_sesler": Path(tmp), "sesler": Path(tmp)}
            server = ThreadingHTTPServer(("127.0.0.1", 0), arayuz.make_handler(settings, None))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                base = f"http://127.0.0.1:{server.server_address[1]}"
                with urllib.request.urlopen(base + "/api/ornekler", timeout=10) as r:
                    data = json.loads(r.read().decode("utf-8"))
                with urllib.request.urlopen(base + "/", timeout=10) as r:
                    page = r.read().decode("utf-8")
            finally:
                server.shutdown()
                server.server_close()
        self.assertEqual(len(data), len(ornekler.listele()))
        self.assertIn('id="ornek"', page)


if __name__ == "__main__":
    unittest.main()

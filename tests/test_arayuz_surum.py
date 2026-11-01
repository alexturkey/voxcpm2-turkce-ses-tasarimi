"""Başlıktaki sürüm yazısı (GPU ve ağ gerekmez). / The version text in the header (no GPU, no network).

python -m unittest discover -s tests -v
"""
import re
import shutil
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from ses_tasarim import __version__, arayuz

BICIM = re.compile(r"^v\d+\.\d+\.\d+( · [0-9a-f]{4,40}\+?)?$")


class Surum(unittest.TestCase):
    def test_tek_kaynak(self):
        self.assertRegex(__version__, r"^\d+\.\d+\.\d+$")
        self.assertTrue(arayuz.surum_yazisi().startswith("v" + __version__))

    def test_git_yoksa_yalniz_surum(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(arayuz.surum_yazisi(Path(tmp)), "v" + __version__)

    @unittest.skipUnless(shutil.which("git") and (arayuz.REPO_KOKU / ".git").exists(), "git ya da .git yok")
    def test_git_varsa_kisa_commit(self):
        yazi = arayuz.surum_yazisi()
        self.assertRegex(yazi, BICIM)
        self.assertIn(" · ", yazi)

    def test_bozuk_git_klasoru_yalniz_surum(self):
        # .git var ama depo değil: git hata verir, sayfa yine açılır / a broken .git still serves the page
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".git").mkdir()
            self.assertEqual(arayuz.surum_yazisi(Path(tmp)), "v" + __version__)

    def test_sayfada_baslikta(self):
        self.assertEqual(arayuz.HTML.count("__SURUM__"), 2)  # yazı + title
        with tempfile.TemporaryDirectory() as tmp:
            settings = {"hazir_sesler": Path(tmp), "sesler": Path(tmp)}
            server = ThreadingHTTPServer(("127.0.0.1", 0), arayuz.make_handler(settings, None))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{server.server_address[1]}/", timeout=10) as r:
                    page = r.read().decode("utf-8")
            finally:
                server.shutdown()
                server.server_close()
        self.assertNotIn("__SURUM__", page)
        m = re.search(r'<small class="surum"[^>]*>([^<]*)</small>', page)
        self.assertIsNotNone(m)
        self.assertRegex(m.group(1), BICIM)
        self.assertIn("</h1>", page[m.end():m.end() + 6])


if __name__ == "__main__":
    unittest.main()

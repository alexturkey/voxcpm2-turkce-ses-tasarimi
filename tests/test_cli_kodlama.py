"""Komut satırı çıktısı yönlendirilince de UTF-8 (GPU ve ağ gerekmez).
CLI output stays UTF-8 when redirected (no GPU, no network).

Windows'ta çıktı boruya ya da dosyaya gidince Python yerel kod sayfasını (ör. cp1254) seçer; "→" ya da Çince yazı
UnicodeEncodeError verirdi. / On Windows redirected output used the locale code page and crashed on "→" or Chinese.

python -m unittest discover -s tests -v
"""
import os
import subprocess
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CLILER = ("arayuz", "klonla", "oku", "ornekler", "tasarla")


def calistir(*argumanlar):
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    return subprocess.run([sys.executable, *argumanlar], cwd=KOK, env=env, capture_output=True, timeout=60,
                          creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


class YonlendirilenCikti(unittest.TestCase):
    def test_ok_ve_cince_yazilir(self):
        r = calistir("-c", "from ses_tasarim import utf8_cikti; utf8_cikti(); print('→ 中文 العربية ş')")
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        self.assertEqual(r.stdout.decode("utf-8").strip(), "→ 中文 العربية ş")

    def test_ornekler_cince_tam_liste(self):
        r = calistir("-m", "ses_tasarim.ornekler", "--dil", "zh", "--tam")
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        cikti = r.stdout.decode("utf-8")
        self.assertIn("zh_", cikti)
        self.assertTrue(any("一" <= c <= "鿿" for c in cikti), "Çince metin yok / no Chinese text")

    def test_tasarla_son_satir_ok_isareti(self):
        # Motor taklit edilir; bildirilen "çeşit 1: ... → klasör" satırı yönlendirilmiş çıktıya yazılmalı.
        # The engine is faked; the reported "variant 1: ... → folder" line must reach redirected output.
        kod = (
            "import sys\n"
            "from ses_tasarim import tasarla, ayarlar\n"
            "ayarlar.load = lambda yol=None: {}\n"
            "tasarla.tasarla = lambda *a, **k: {'cesitler': [{'cesit': 1, 'tohum': 7, 'tasarim_tohumu': 7,"
            " 'referans_sn': 9.1, 'klasor': 'sesler/örnek_中文/cesit_01'}], 'sure_sn': 1, 'vram_tepe_mb': 0}\n"
            "sys.exit(tasarla.main(['--ornek', 'zh_haber_kadin', '--cesit', '1']))\n")
        r = calistir("-c", kod)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        self.assertIn("→ sesler/örnek_中文/cesit_01", r.stdout.decode("utf-8"))

    def test_her_cli_main_basinda_cagirir(self):
        for ad in CLILER:
            with self.subTest(ad):
                kaynak = (KOK / "ses_tasarim" / f"{ad}.py").read_text(encoding="utf-8")
                govde = kaynak.split("def main(argv=None) -> int:\n", 1)[1]
                self.assertTrue(govde.startswith("    utf8_cikti()\n"), ad)

    def test_yardim_yonlendirilince(self):
        for ad in CLILER:
            with self.subTest(ad):
                r = calistir("-m", f"ses_tasarim.{ad}", "--help")
                self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
                r.stdout.decode("utf-8")


if __name__ == "__main__":
    unittest.main()

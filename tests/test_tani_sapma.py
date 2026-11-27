"""scripts/tani.ps1 SAPMA / DEVIATIONS bolumu (kit KL-23): salt okur, SES_* ezmesi gorunur, kisisel ad sizmaz, hicbir sey yazmaz.
The SAPMA section is read-only: it shows a SES_* override, keeps the name filter and writes nothing. No network, no GPU.
"""
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PS = shutil.which("powershell") if sys.platform == "win32" else None
TANI = REPO / "scripts" / "tani.ps1"


def kos(env_ek=None):
    env = dict(os.environ)
    env.update(env_ek or {})
    p = subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(TANI)], capture_output=True, env=env, timeout=120)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def git_durum():
    if not shutil.which("git"):
        return None
    return subprocess.run(["git", "--no-optional-locks", "-C", str(REPO), "status", "--porcelain", "-uno"], capture_output=True, timeout=60).stdout


@unittest.skipUnless(PS, "Windows PowerShell gerekir")
class Sapma(unittest.TestCase):
    def test_bolum_ve_ses_ezmesi(self):
        kod, c = kos({"SES_TEST_EZME": "1"})
        self.assertEqual(kod, 0, c[-300:])
        self.assertIn("SAPMA / DEVIATIONS", c)
        self.assertIn("SES_TEST_EZME", c)

    def test_ezme_degerindeki_ad_gizlenir(self):
        ad = "Gizli" + "Kisi" + "Adi"
        kod, c = kos({"SES_TEST_EZME": ad, "USERNAME": ad})
        self.assertEqual(kod, 0, c[-300:])
        self.assertNotIn(ad, c)

    def test_hicbir_sey_yazmaz(self):
        once = git_durum()
        kod, _ = kos()
        self.assertEqual(kod, 0)
        self.assertEqual(git_durum(), once)

    def test_betik_ascii(self):
        self.assertTrue(all(b < 128 for b in TANI.read_bytes()))


if __name__ == "__main__":
    unittest.main()

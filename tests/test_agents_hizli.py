"""Ajan hizli karti (AGENTS_HIZLI.md) betige ve belgeye baglidir: kart kayarsa test kirmizi (kit KL-18, KL-21).
The agent quick card is tied to the real scripts: if the card drifts, this test goes red. Ag yok, GPU yok.
"""
import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PS = shutil.which("powershell") if sys.platform == "win32" else None


def oku(yol):
    return (REPO / yol).read_text(encoding="utf-8")


class Kart(unittest.TestCase):
    def test_kartin_andigi_kodlar_kayitta(self):
        kodlar = {h["kod"] for h in json.loads(oku("docs/hata_imzalari.json"))["hatalar"]}
        for k in re.findall(r"SES-E-[A-Z0-9-]+", oku("AGENTS_HIZLI.md")):
            self.assertIn(k, kodlar, k)

    def test_kartin_andigi_dosyalar_var(self):
        for yol in set(re.findall(r"`((?:scripts|docs)[/\][A-Za-z0-9_./\-]+)`", oku("AGENTS_HIZLI.md"))):
            yol = yol.split(" ")[0].replace("\\", "/")
            self.assertTrue((REPO / yol).exists(), yol)

    def test_kart_iki_dilde_ve_12_adim(self):
        t = oku("AGENTS_HIZLI.md")
        self.assertEqual(len(re.findall(r"(?m)^\d+\. ", t)), 24)

    def test_denetim_cikis_kodu_karttaki_gibi(self):
        c = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(REPO / "scripts" / "denetim.py")], capture_output=True, cwd=str(REPO))
        self.assertEqual(c.returncode, 3)   # karttaki "3: argüman ya da git yok"

    @unittest.skipUnless(PS, "Windows PowerShell gerekir")
    def test_kur_ascii_disi_kok_hata_1(self):
        c = subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(REPO / "scripts" / "kur.ps1"), "-Kok", "C:/v" + chr(0xF6) + "x", "-Kuru"],
                           capture_output=True)
        self.assertEqual(c.returncode, 1)   # karttaki "kur.ps1 1: hata firlatildi"

    @unittest.skipUnless(PS, "Windows PowerShell gerekir")
    def test_tani_hata_bulundu_0_bulunamadi_1(self):
        def kos(metin):
            return subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(REPO / "scripts" / "tani.ps1"), "-Hata", metin],
                                  capture_output=True).returncode
        self.assertEqual(kos("GGML_ASSERT mem_buffer failed"), 0)
        self.assertEqual(kos("hic-bilinmeyen-ileti-xyz"), 1)

    @unittest.skipUnless(PS, "Windows PowerShell gerekir")
    def test_kuru_hicbir_sey_yazmaz(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            kok = Path(d) / "kok"
            c = subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(REPO / "scripts" / "kur.ps1"), "-Kok", str(kok), "-Kuru"], capture_output=True)
            self.assertIn(c.returncode, (0, 1, 3))
            self.assertFalse(kok.exists(), "-Kuru kok klasoru olusturdu")


class Yonlendiriciler(unittest.TestCase):
    def test_ince_ve_agents_e_bagli(self):
        for yol in ("CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md", ".aider.conf.yml"):
            t = oku(yol)
            self.assertLessEqual(len(t.strip().split("\n")), 15, yol)
            self.assertIn("AGENTS.md", t, yol)
        for yol in ("CLAUDE.md", "GEMINI.md"):
            self.assertIn("@AGENTS.md", oku(yol))

    def test_agents_32kib_alti(self):
        self.assertLess((REPO / "AGENTS.md").stat().st_size, 32768)

    def test_llms_txt_baglantilari_var_olan_dosyalar(self):
        for yol in re.findall(r"/blob/main/([A-Za-z0-9_./-]+)\)", oku("llms.txt")):
            self.assertTrue((REPO / yol).exists(), yol)

    def test_readme_ilk_40_satirda_agents(self):
        for yol in sorted(REPO.glob("README*.md")):
            ilk = "\n".join(yol.read_text(encoding="utf-8").split("\n")[:40])
            self.assertIn("AGENTS.md", ilk, yol.name)


if __name__ == "__main__":
    unittest.main()

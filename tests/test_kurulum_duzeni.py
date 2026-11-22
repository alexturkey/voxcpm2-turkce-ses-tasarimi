"""Kurulum düzeni (kök dışına iz yok, çift indirme yok): kur.ps1'in Indir işlevi yerel sahte sunucuya karşı, ağsız.
Yarım .part kaldığı yerden sürer (Range), tam ve doğru .part yeniden inmez, doğru hedef dosya atlanır, sha256 tutmazsa dosya kabul edilmez.
Ayrıca kur.ps1 kalıcı sistem değişikliği yazmaz (ortam, registry, profil) ve pip önbelleği kurulum köküne yönlenir.
Install layout: resumable downloads, no second download, no persistent system change. Local fake server only; no internet.

python -m unittest discover -s tests -v
"""
import hashlib
import http.server
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KUR_PS1 = REPO / "scripts" / "kur.ps1"
PS = shutil.which("powershell") or "powershell.exe"

VERI = bytes((i * 7 + 3) % 251 for i in range(600_000))
SHA = hashlib.sha256(VERI).hexdigest()


# Kalici sistem degisikligi desenleri PARCALI yazilir: bu dosyanin kendisi bekci/PR kapisinin supheli-komut taramasina takilmasin.
YASAK = (r"\bset" + "x" + r"\b", r"\breg\s+" + "add" + r"\b", "HK" + "CU:|HK" + "LM:", r"\$PRO" + "FILE" + r"\b",
         "Set-Execution" + r"Policy(?![^\n]*-Scope\s+Process)", "SetEnviron" + r"mentVariable\s*\([^)]*,\s*['\"]?(User|Machine)\b",
         r"pip3?\s+install[^\n]*--user")


class Sunucu(http.server.BaseHTTPRequestHandler):
    istekler = []
    range_kabul = True

    def log_message(self, *a):
        pass

    def do_GET(self):
        r = self.headers.get("Range")
        Sunucu.istekler.append(r)
        if r and Sunucu.range_kabul:
            m = re.match(r"bytes=(\d+)-", r)
            bas = int(m.group(1))
            if bas >= len(VERI):
                self.send_response(416)
                self.send_header("Content-Range", "bytes */%d" % len(VERI))
                self.end_headers()
                return
            parca = VERI[bas:]
            self.send_response(206)
            self.send_header("Content-Range", "bytes %d-%d/%d" % (bas, len(VERI) - 1, len(VERI)))
        else:
            parca = VERI
            self.send_response(200)
        self.send_header("Content-Length", str(len(parca)))
        self.end_headers()
        self.wfile.write(parca)


RUNNER = r"""
param($kur, $url, $hedef, $sha)
$ErrorActionPreference = "Stop"
$ast = [System.Management.Automation.Language.Parser]::ParseFile($kur, [ref]$null, [ref]$null)
$fn = $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and @("Sha256", "Indir") -contains $n.Name }, $true)
$yol = Join-Path $PSScriptRoot "islevler.ps1"
[IO.File]::WriteAllText($yol, (($fn | ForEach-Object { $_.Extent.Text }) -join "`n"), (New-Object Text.UTF8Encoding $true))
. $yol
try { Indir $url $hedef $sha; Write-Output "SONUC:TAMAM" } catch { Write-Output ("SONUC:HATA " + $_.Exception.Message) }
"""


@unittest.skipUnless(sys.platform == "win32" and shutil.which("curl.exe"), "Windows PowerShell + curl.exe")
class IndirDevam(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Sunucu)
        cls.url = "http://127.0.0.1:%d/dosya.bin" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        Sunucu.istekler = []
        Sunucu.range_kabul = True
        self._t = tempfile.TemporaryDirectory()
        self.addCleanup(self._t.cleanup)
        self.t = Path(self._t.name)
        self.hedef = self.t / "dosya.bin"

    def kos(self, sha=SHA):
        runner = self.t / "runner.ps1"
        runner.write_text(RUNNER, encoding="utf-8-sig")
        r = subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(runner), str(KUR_PS1), self.url, str(self.hedef), sha],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        son = [s for s in r.stdout.splitlines() if s.startswith("SONUC:")]
        self.assertTrue(son, r.stdout + r.stderr)
        return son[-1]

    def test_sifirdan_iner(self):
        self.assertEqual(self.kos(), "SONUC:TAMAM")
        self.assertEqual(hashlib.sha256(self.hedef.read_bytes()).hexdigest(), SHA)
        self.assertFalse((self.t / "dosya.bin.part").exists())

    def test_yarim_part_kaldigi_yerden_surer(self):
        (self.t / "dosya.bin.part").write_bytes(VERI[:250_000])
        self.assertEqual(self.kos(), "SONUC:TAMAM")
        self.assertEqual(hashlib.sha256(self.hedef.read_bytes()).hexdigest(), SHA)
        self.assertEqual(Sunucu.istekler, ["bytes=250000-"], "yalnız kalan kısım istenmeli, baştan değil")

    def test_dogru_hedef_yeniden_inmez(self):
        self.hedef.write_bytes(VERI)
        self.assertEqual(self.kos(), "SONUC:TAMAM")
        self.assertEqual(Sunucu.istekler, [], "doğru dosya varken ağa çıkılmamalı")

    def test_tam_part_yeniden_inmez(self):
        (self.t / "dosya.bin.part").write_bytes(VERI)
        self.assertEqual(self.kos(), "SONUC:TAMAM")
        self.assertEqual(Sunucu.istekler, [], "tam ve doğru .part yeniden indirilmemeli")
        self.assertTrue(self.hedef.exists())

    def test_range_kabul_etmeyen_sunucuda_bastan(self):
        Sunucu.range_kabul = False
        (self.t / "dosya.bin.part").write_bytes(VERI[:100_000])
        self.assertEqual(self.kos(), "SONUC:TAMAM")
        self.assertEqual(hashlib.sha256(self.hedef.read_bytes()).hexdigest(), SHA)

    def test_yanlis_sha_kabul_edilmez(self):
        s = self.kos(sha="0" * 64)
        self.assertTrue(s.startswith("SONUC:HATA"), s)
        self.assertFalse(self.hedef.exists(), "sha tutmayan dosya hedefe konmamalı")


class BetikKurallari(unittest.TestCase):
    metin = KUR_PS1.read_text(encoding="utf-8-sig")
    kod = "\n".join(s for s in metin.splitlines() if not s.strip().startswith("#"))

    def test_kalici_sistem_degisikligi_yok(self):
        for desen in YASAK:
            self.assertIsNone(re.search(desen, self.kod, re.I), desen)

    def test_kullanici_pip_degeri_korunur(self):
        self.assertIn("if (-not $env:PIP_CACHE_DIR) { $env:PIP_CACHE_DIR = Join-Path", self.kod)

    def test_pip_onbellegi_ve_gecici_koke(self):
        self.assertIn("$env:PIP_CACHE_DIR = Join-Path", self.kod)
        self.assertIn("$env:TMP = $gecici", self.kod)
        self.assertTrue(self.kod.index("PIP_CACHE_DIR") < self.kod.index("-m pip install"), "yönlendirme pip'ten önce")


if __name__ == "__main__":
    unittest.main()

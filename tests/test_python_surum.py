"""Python sürüm aralığı: kurulum betikleri yalnız 64-bit Python 3.10-3.13 kabul eder (3.14+ için numpy tekerleği yok).
Ağsız, indirmesiz: kur.ps1'in PythonBul / VenvDenetle işlevleri sahte sürüm tablosuyla (PowerShell, yalnız Windows), kur.sh ve kur-linux.sh'nin
var olan .venv denetimi sahte .venv ile (bash). Olay: X kullanıcısı Python 3.15 ile `Unknown compiler(s)` hatası aldı; betik üst sınıra bakmıyordu.
Python version range: the installers accept only 64-bit Python 3.10-3.13; an existing .venv from another version is refused, never deleted.

python -m unittest discover -s tests -v
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KUR_PS1 = REPO / "scripts" / "kur.ps1"
PS = shutil.which("powershell") or "powershell.exe"

PS_RUNNER = r"""
param($kur, $senaryo)
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = New-Object Text.UTF8Encoding $false
$ast = [System.Management.Automation.Language.Parser]::ParseFile($kur, [ref]$null, [ref]$null)
$atama = $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.AssignmentStatementAst] -and
                        $n.Left -is [System.Management.Automation.Language.VariableExpressionAst] -and
                        @("PY_MIN", "PY_MAX") -contains $n.Left.VariablePath.UserPath }, $true)
$fn = $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and
                     @("PythonSurum", "PythonBul", "PythonYokMesaji", "VenvDenetle") -contains $n.Name }, $true)
$yol = Join-Path $PSScriptRoot "islevler.ps1"   # kur.ps1'in yalnız bu işlevleri ve iki sabiti, ayrı dosyadan yüklenir
[IO.File]::WriteAllText($yol, ((($atama | ForEach-Object { $_.Extent.Text }) + ($fn | ForEach-Object { $_.Extent.Text })) -join "`n"), (New-Object Text.UTF8Encoding $true))
. $yol
$s = Get-Content -LiteralPath $senaryo -Raw -Encoding UTF8 | ConvertFrom-Json
if ($s.probe -ne $null) {
    $script:Sahte = @{}
    foreach ($p in $s.probe.PSObject.Properties) { $script:Sahte[$p.Name] = [string]$p.Value }
    function PythonSurum([string]$cmd, [string[]]$on = @()) {
        $k = (@($cmd) + $on) -join " "
        if ($script:Sahte.ContainsKey($k)) { return $script:Sahte[$k] }
        return $null
    }
}
$sonuc = @{}
if ($s.islem -eq "bul") {
    $sonuc.yol = PythonBul
    $sonuc.reddedilen = @($script:PyReddedilen)
    $sonuc.mesaj = PythonYokMesaji
} else {
    $sonuc.hata = VenvDenetle $s.vpy
}
$sonuc.aralik = @($PY_MIN, $PY_MAX)
Write-Output ($sonuc | ConvertTo-Json -Compress)
"""


@unittest.skipUnless(sys.platform == "win32", "Windows PowerShell")
class PowerShellPythonBul(unittest.TestCase):
    def kos(self, **senaryo):
        with tempfile.TemporaryDirectory() as t:
            runner = Path(t) / "runner.ps1"
            runner.write_text(PS_RUNNER, encoding="utf-8-sig")
            sen = Path(t) / "senaryo.json"
            sen.write_text(json.dumps(senaryo), encoding="utf-8")
            r = subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(runner), str(KUR_PS1), str(sen)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout.strip().splitlines()[-1])

    def bul(self, probe):
        return self.kos(islem="bul", probe=probe)

    def test_aralik_sabitleri(self):
        s = self.bul({})
        self.assertEqual(s["aralik"], [10, 13])

    def test_hic_python_yok(self):
        s = self.bul({})
        self.assertIsNone(s["yol"])
        self.assertEqual(s["reddedilen"], [])
        self.assertIn("3.10-3.13", s["mesaj"])
        self.assertIn("winget install Python.Python.3.12", s["mesaj"])

    def test_yalniz_3_15_reddedilir_mesaj_surumu_soyler(self):
        # olayin kendisi: py -3, python ve python3 hepsi 3.15
        p = {"py -3": r"3 15 64 C:\Py315\python.exe", "python": r"3 15 64 C:\Py315\python.exe", "python3": r"3 15 64 C:\Py315\python.exe"}
        s = self.bul(p)
        self.assertIsNone(s["yol"])
        self.assertEqual(s["reddedilen"], [r"3.15 (64-bit, C:\Py315\python.exe)"], "ayni yol tekrar yazilmaz")
        self.assertIn("3.15", s["mesaj"])
        self.assertIn("3.14 ve üstü desteklenmez", s["mesaj"])
        self.assertIn("winget install Python.Python.3.12", s["mesaj"])

    def test_3_14_reddedilir(self):
        s = self.bul({"py -3": r"3 14 64 C:\Py314\python.exe"})
        self.assertIsNone(s["yol"])
        self.assertIn("3.14", s["mesaj"])

    def test_py_3_15_varken_3_12_secilir(self):
        # birden cok Python: py -3 en yeniyi (3.15) verir ama 3.12 kurulu: 3.12 secilmeli
        p = {"py -3": r"3 15 64 C:\Py315\python.exe", "py -3.12": r"3 12 64 C:\Py312\python.exe", "python": r"3 15 64 C:\Py315\python.exe"}
        self.assertEqual(self.bul(p)["yol"], r"C:\Py312\python.exe")

    def test_sira_3_12_3_13_3_11_3_10(self):
        tum = {"py -3.10": r"3 10 64 C:\P310\python.exe", "py -3.11": r"3 11 64 C:\P311\python.exe",
               "py -3.13": r"3 13 64 C:\P313\python.exe", "py -3.12": r"3 12 64 C:\P312\python.exe"}
        self.assertEqual(self.bul(tum)["yol"], r"C:\P312\python.exe")
        del tum["py -3.12"]
        self.assertEqual(self.bul(tum)["yol"], r"C:\P313\python.exe")
        del tum["py -3.13"]
        self.assertEqual(self.bul(tum)["yol"], r"C:\P311\python.exe")
        del tum["py -3.11"]
        self.assertEqual(self.bul(tum)["yol"], r"C:\P310\python.exe")

    def test_3_9_reddedilir(self):
        s = self.bul({"py -3": r"3 9 64 C:\P39\python.exe", "python": r"3 9 64 C:\P39\python.exe"})
        self.assertIsNone(s["yol"])
        self.assertIn("3.9", s["mesaj"])

    def test_32_bit_reddedilir(self):
        s = self.bul({"py -3.12": r"3 12 32 C:\P312x86\python.exe"})
        self.assertIsNone(s["yol"])
        self.assertIn("32-bit", s["mesaj"])

    def test_py_baslatici_yoksa_python_komutuna_dusulur(self):
        self.assertEqual(self.bul({"python": r"3 11 64 C:\P311\python.exe"})["yol"], r"C:\P311\python.exe")
        self.assertEqual(self.bul({"python3": r"3 13 64 C:\P313\python.exe"})["yol"], r"C:\P313\python.exe")

    def test_store_takma_adi_ve_python2_atlanir(self):
        # Store takma adi sürüm satiri basmaz; python 2 "2 7 64 ..." basar: ikisi de eslesmez
        p = {"python": "Python was not found; run without arguments to install from the Microsoft Store", "python3": "2 7 64 C:\\Py27\\python.exe"}
        s = self.bul(p)
        self.assertIsNone(s["yol"])
        self.assertEqual(s["reddedilen"], [])

    def test_gercek_makine_yolu_aralikta(self):
        """Sahte tablo yok: gerçek py/python. Bu makinede aralikta bir Python yoksa atlanir."""
        s = self.kos(islem="bul")
        if not s["yol"]:
            self.skipTest("bu makinede 3.10-3.13 64-bit Python yok")
        self.assertTrue(Path(s["yol"]).exists(), s)
        sur = subprocess.run([s["yol"], "-c", "import sys; print(sys.version_info[1])"], capture_output=True, text=True).stdout.strip()
        self.assertTrue(10 <= int(sur) <= 13, s)

    # ---- var olan .venv
    def venv(self, surum_satiri):
        return self.kos(islem="venv", vpy=r"C:\kok\.venv\Scripts\python.exe", probe={r"C:\kok\.venv\Scripts\python.exe": surum_satiri} if surum_satiri else {})

    def test_venv_yoksa_sorun_yok(self):
        with tempfile.TemporaryDirectory() as t:   # gerçek dosya yok: Test-Path yanlis -> $null
            s = self.kos(islem="venv", vpy=str(Path(t) / ".venv" / "Scripts" / "python.exe"))
        self.assertIsNone(s["hata"])

    def test_venv_uyumsuz_hata_yolu_ve_silme_adimini_soyler_silmez(self):
        with tempfile.TemporaryDirectory() as t:
            venv = Path(t) / ".venv"
            (venv / "Scripts").mkdir(parents=True)
            vpy = venv / "Scripts" / "python.exe"
            vpy.write_bytes(b"")
            (venv / "isaret.txt").write_text("kullanici dosyasi")
            s = self.kos(islem="venv", vpy=str(vpy), probe={str(vpy): "3 15 64 " + str(vpy)})
            self.assertIn("Python 3.15", s["hata"])
            self.assertIn(str(venv), s["hata"])
            self.assertIn("silmez", s["hata"])
            self.assertIn("yeniden çalıştırın", s["hata"])
            self.assertTrue((venv / "isaret.txt").exists(), ".venv'e dokunulmamali")
            self.assertTrue(vpy.exists())

    def test_venv_uygun_surumler_gecer(self):
        for minor in (10, 11, 12, 13):
            with self.subTest(minor=minor), tempfile.TemporaryDirectory() as t:
                vpy = Path(t) / ".venv" / "Scripts" / "python.exe"
                vpy.parent.mkdir(parents=True)
                vpy.write_bytes(b"")
                self.assertIsNone(self.kos(islem="venv", vpy=str(vpy), probe={str(vpy): "3 %d 64 %s" % (minor, vpy)})["hata"])

    def test_venv_sinir_disi_3_14_3_9_ve_32_bit_ve_calismayan(self):
        for ad, satir in (("3.14", "3 14 64 X"), ("3.9", "3 9 64 X"), ("32-bit", "3 12 32 X"), ("çalışmayan", None)):
            with self.subTest(ad=ad), tempfile.TemporaryDirectory() as t:
                vpy = Path(t) / ".venv" / "Scripts" / "python.exe"
                vpy.parent.mkdir(parents=True)
                vpy.write_bytes(b"")
                probe = {str(vpy): satir} if satir else {}
                s = self.kos(islem="venv", vpy=str(vpy), probe=probe)
                self.assertIsNotNone(s["hata"], ad)
                self.assertIn(ad, s["hata"])

    # ---- kur.ps1 yapısı ve gerçek betik: büyük indirmeden ÖNCE başarısız olur
    def test_on_kontrol_model_adimindan_once(self):
        metin = KUR_PS1.read_text(encoding="utf-8-sig")
        self.assertRegex(metin, r"\$PY_MIN = 10; \$PY_MAX = 13")
        self.assertLess(metin.index("VenvDenetle (Join-Path"), metin.index('if ($Adim -contains "model")'))
        self.assertLess(metin.index("PythonBul\n"), metin.index('if ($Adim -contains "model")'))
        self.assertNotIn("-ge 10) { return", metin, "eski ust sinirsiz kosul kalmamali")

    def test_betik_python_yokken_indirmeden_once_durur(self):
        """PATH'te Python yok: kur.ps1 -Adim python hata verir, hiçbir klasör (indirme/, model/) oluşturmaz."""
        with tempfile.TemporaryDirectory() as t:
            kok = Path(t) / "rk"
            (kok / "scripts").mkdir(parents=True)
            shutil.copy(KUR_PS1, kok / "scripts" / "kur.ps1")
            vox = Path(t) / "vox"
            sistem = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32")
            env = dict(os.environ, PATH=sistem + ";" + os.path.dirname(PS))
            r = subprocess.run([PS, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(kok / "scripts" / "kur.ps1"), "-Kok", str(vox), "-Adim", "python"],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=120)
            cikti = r.stdout + r.stderr
            if "bulunamadı" not in cikti:
                self.skipTest("bu makinede System32 PATH'iyle bile Python bulundu: " + cikti[:200])
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("3.10-3.13", cikti)
            self.assertFalse(vox.exists(), "indirme klasörü oluşmamalı")
            self.assertFalse((kok / ".venv").exists())


def _bash():
    if sys.platform != "win32":
        return shutil.which("bash")
    git = shutil.which("git")   # Windows: Git Bash (System32\bash.exe WSL olabilir / may be WSL)
    if not git:
        return None
    for up in Path(git).resolve().parents:
        cand = up / "bin" / "bash.exe"
        if cand.exists():
            return str(cand)
    return None


BASH = _bash()


def _blok(betik, baslangic):
    """Betikten, `baslangic` satırından ilk `fi` satırına kadar olan blok (iç içe fi'yi hesaba katarak)."""
    satirlar = (REPO / betik).read_text(encoding="utf-8").split("\n")
    i = next(k for k, s in enumerate(satirlar) if s.strip().startswith(baslangic))
    derin, cikti = 0, []
    for s in satirlar[i:]:
        cikti.append(s)
        d = s.strip()
        if re.match(r"^(if|case)\b", d):
            derin += 1
        if d == "fi" or d == "esac":
            derin -= 1
            if derin == 0:
                break
    return "\n".join(cikti)


@unittest.skipUnless(BASH, "bash yok")
class ShellVenvDenetimi(unittest.TestCase):
    """kur.sh ve kur-linux.sh: var olan .venv aralık dışıysa indirmeden önce durur (sahte .venv/bin/python betiği), silmez."""

    def sahte_repo(self, t, cikis):
        repo = Path(t) / "repo"
        (repo / "scripts").mkdir(parents=True)
        py = repo / ".venv" / "bin" / "python"
        py.parent.mkdir(parents=True)
        py.write_text("#!/bin/sh\nexit %d\n" % cikis, encoding="utf-8", newline="\n")
        py.chmod(0o755)
        (repo / ".venv" / "isaret.txt").write_text("kullanici dosyasi")
        return repo

    def kos(self, betik, baslangic, cikis, adim="python"):
        with tempfile.TemporaryDirectory() as t:
            repo = self.sahte_repo(t, cikis)
            blok = _blok(betik, baslangic)
            if betik.endswith("kur.sh"):
                kod = 'ADIM="%s"\nadim() { [[ ",$ADIM," == *",$1,"* ]]; }\n%s\necho GECTI\n' % (adim, blok)
            else:
                kod = 'REPO="%s"\n%s\necho GECTI\n' % (repo.as_posix(), blok)
            script = repo / "scripts" / "kur-test.sh"
            script.write_text(kod, encoding="utf-8", newline="\n")
            r = subprocess.run([BASH, str(script.as_posix())], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
            silinmedi = (repo / ".venv" / "isaret.txt").exists()
            return r.returncode, r.stdout + r.stderr, silinmedi

    def test_kur_sh_uyumsuz_venv_durur_silmez(self):
        kod, c, silinmedi = self.kos("scripts/kur.sh", "if adim python &&", 1)
        self.assertEqual(kod, 1, c)
        self.assertNotIn("GECTI", c)
        self.assertIn("desteklenmeyen", c)
        self.assertTrue(silinmedi)

    def test_kur_sh_uygun_venv_gecer(self):
        kod, c, _ = self.kos("scripts/kur.sh", "if adim python &&", 0)
        self.assertEqual(kod, 0, c)
        self.assertIn("GECTI", c)

    def test_kur_sh_python_adimi_secilmediyse_bakmaz(self):
        kod, c, _ = self.kos("scripts/kur.sh", "if adim python &&", 1, adim="model,ayar")
        self.assertEqual(kod, 0, c)

    def test_kur_linux_uyumsuz_venv_durur_silmez(self):
        kod, c, silinmedi = self.kos("scripts/kur-linux.sh", "if [[ -x \"$REPO/.venv/bin/python\" ]] &&", 1)
        self.assertEqual(kod, 1, c)
        self.assertNotIn("GECTI", c)
        self.assertIn("unsupported", c)
        self.assertTrue(silinmedi)

    def test_kur_linux_uygun_venv_gecer(self):
        kod, c, _ = self.kos("scripts/kur-linux.sh", "if [[ -x \"$REPO/.venv/bin/python\" ]] &&", 0)
        self.assertEqual(kod, 0, c)
        self.assertIn("GECTI", c)

    def test_adaylar_ve_aralik_betiklerde(self):
        for betik in ("scripts/kur.sh", "scripts/kur-linux.sh"):
            metin = (REPO / betik).read_text(encoding="utf-8")
            self.assertIn("(3, 10) <= sys.version_info[:2] <= (3, 13)" if betik.endswith("kur.sh") else "(3,10) <= sys.version_info[:2] <= (3,13)", metin)
            self.assertIn("python3.13 python3.12 python3.11 python3.10 python3", metin)


if __name__ == "__main__":
    unittest.main()

"""Yama imzası: kurulum betikleri eski yamalı kaynağı sessizce derlemez (v0.3.2).
Ağsız, derlemesiz: küçük sahte kaynak + sahte yamalarla kur.ps1, kur.sh, kur-linux.sh ve motoru_derle.sh'nin yama işlevi.
Patch signature: the installers refuse a source patched with older patches instead of building it silently.

python -m unittest discover -s tests -v
"""
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SHELL_SCRIPTS = ["scripts/kur.sh", "scripts/kur-linux.sh", "macos/scripts/motoru_derle.sh"]


def _diff(name, old, new):
    return (f"diff --git a/{name} b/{name}\n--- a/{name}\n+++ b/{name}\n"
            f"@@ -1 +1 @@\n-{old}\n+{new}\n")


def _txt(path):
    return path.read_bytes().replace(b"\r\n", b"\n")   # git core.autocrlf Windows'ta CRLF yazabilir


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


def _shell_functions(script):
    text = (REPO / script).read_text(encoding="utf-8")
    parts = [re.search(r"^%s\(\) \{\n.*?^\}\n" % name, text, re.S | re.M) for name in ("yama_imzasi", "yamalari_uygula")]
    assert all(parts), script
    return "".join(p.group(0) for p in parts)


PS_RUNNER = r"""
param($kur, $src)
$yamalar = [string[]]$args
$ErrorActionPreference = "Stop"
$ast = [System.Management.Automation.Language.Parser]::ParseFile($kur, [ref]$null, [ref]$null)
$fn = $ast.FindAll({ param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and
                     @("GitApply", "YamaImzasi", "YamalariUygula") -contains $n.Name }, $true)
$islevler = Join-Path $PSScriptRoot "islevler.ps1"   # kur.ps1'in yalnız bu üç işlevi, ayrı dosyadan yüklenir
[IO.File]::WriteAllText($islevler, (($fn | ForEach-Object { $_.Extent.Text }) -join "`n"), (New-Object Text.UTF8Encoding $true))
. $islevler
try { YamalariUygula $src $yamalar } catch { [Console]::Error.WriteLine($_.Exception.Message); exit 1 }
exit 0
"""


class _Base:
    """Ortak senaryolar; alt sınıf run(src, patches) -> (returncode, out) verir."""

    def setUp(self):
        if not shutil.which("git"):
            self.skipTest("git yok")
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.src = self.root / "motor" / "src"
        self.src.mkdir(parents=True)
        (self.src / "a.txt").write_bytes(b"x\n")
        (self.src / "b.txt").write_bytes(b"1\n")
        pdir = self.root / "patches"
        pdir.mkdir()
        self.p1, self.p2, self.p1_new = pdir / "0001.patch", pdir / "0002.patch", pdir / "new" / "0001.patch"
        self.p1_new.parent.mkdir()
        self.p1.write_bytes(_diff("a.txt", "x", "y").encode())
        self.p2.write_bytes(_diff("b.txt", "1", "2").encode())
        self.p1_new.write_bytes(_diff("a.txt", "x", "z").encode())

    def test_fresh_source_patched_signed_and_rerun_skips(self):
        code, out = self.run_patches([self.p1, self.p2])
        self.assertEqual(code, 0, out)
        self.assertEqual(_txt(self.src / "a.txt"), b"y\n")
        self.assertEqual(_txt(self.src / "b.txt"), b"2\n")
        self.assertTrue((self.src / ".yama_imzasi").is_file())
        code, out = self.run_patches([self.p1, self.p2])
        self.assertEqual(code, 0, out)
        self.assertIn("imza tutuyor", out)

    def test_old_patched_source_fails_loudly(self):
        code, out = self.run_patches([self.p1, self.p2])
        self.assertEqual(code, 0, out)
        code, out = self.run_patches([self.p1_new, self.p2])   # yeni sürüm, 0001 değişti
        self.assertNotEqual(code, 0, out)
        self.assertIn("delete motor/src and run again", out)
        self.assertEqual(_txt(self.src / "a.txt"), b"y\n")   # dokunulmadı

    def test_unsigned_patched_source_fails_loudly(self):
        # v0.3.1 ve öncesi: yamalar uygulanmış, imza yok -> tutmuyor sayılır
        subprocess.run(["git", "apply", str(self.p1)], cwd=self.src, check=True)
        code, out = self.run_patches([self.p1, self.p2])
        self.assertNotEqual(code, 0, out)
        self.assertIn("delete motor/src and run again", out)
        self.assertFalse((self.src / ".yama_imzasi").exists())


class ShellInstallers(_Base, unittest.TestCase):
    def setUp(self):
        self.bash = _bash()
        if not self.bash:
            self.skipTest("bash yok")
        super().setUp()
        self.script = None

    def run_patches(self, patches):
        fn = self.root / "fn.sh"
        fn.write_text(_shell_functions(self.script), encoding="utf-8", newline="\n")
        args = [p.as_posix() for p in [fn, self.src, *patches]]
        r = subprocess.run([self.bash, "-c", 'source "$1"; shift; yamalari_uygula "$@"', "_", *args],
                           capture_output=True, timeout=60)
        return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")

    def test_same_function_in_all_shell_scripts(self):
        self.assertEqual(len({_shell_functions(s) for s in SHELL_SCRIPTS}), 1)

    def _each(self, name):
        for script in SHELL_SCRIPTS:
            with self.subTest(script=script):
                self.script = script
                for f in (self.src / ".yama_imzasi",):
                    if f.exists():
                        f.unlink()
                (self.src / "a.txt").write_bytes(b"x\n")
                (self.src / "b.txt").write_bytes(b"1\n")
                getattr(_Base, name)(self)

    def test_fresh_source_patched_signed_and_rerun_skips(self):
        self._each("test_fresh_source_patched_signed_and_rerun_skips")

    def test_old_patched_source_fails_loudly(self):
        self._each("test_old_patched_source_fails_loudly")

    def test_unsigned_patched_source_fails_loudly(self):
        self._each("test_unsigned_patched_source_fails_loudly")


class PowerShellInstaller(_Base, unittest.TestCase):
    def setUp(self):
        self.ps = shutil.which("powershell") or shutil.which("pwsh")
        if not self.ps:
            self.skipTest("PowerShell yok")
        super().setUp()

    def run_patches(self, patches):
        runner = self.root / "runner.ps1"
        runner.write_text(PS_RUNNER, encoding="utf-8-sig")
        r = subprocess.run([self.ps, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(runner),
                            str(REPO / "scripts" / "kur.ps1"), str(self.src), *map(str, patches)],
                           capture_output=True, timeout=120)
        return r.returncode, (r.stdout + r.stderr).decode("utf-8", "replace")


if __name__ == "__main__":
    unittest.main()

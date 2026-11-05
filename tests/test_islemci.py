"""Vulkan paket seçimi (ses_tasarim/islemci.py): AVX2 paketi yalnız gereken komut aileleri varken seçilir; bilinmeyen
aileler AVX2 exe'sinin deneme çalışmasına kalır (geçersiz komut -> uyumlu)."""
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from ses_tasarim import islemci

REPO = Path(__file__).resolve().parents[1]
TAM = {ad: True for ad in islemci.KESIN + islemci.EK}
ESKI_NUMPY = {ad: True for ad in islemci.KESIN}   # numpy 2.2.6: BMI/BMI2/LZCNT anahtarı yok


class PaketSecimi(unittest.TestCase):
    def test_hepsi_varsa_avx2(self):
        self.assertEqual(islemci.paket(dict(TAM, AVX512F=False)), ("avx2", [], []))

    def test_kesin_aile_eksikse_uyumlu(self):
        for ad in islemci.KESIN:
            with self.subTest(eksik=ad):
                self.assertEqual(islemci.paket(dict(TAM, **{ad: False}))[:2], ("uyumlu", [ad]))

    def test_ek_aile_biliniyor_ve_eksikse_uyumlu(self):
        # AVX2 var ama BMI2 yok (ör. özellikleri kısılmış sanal makine): AVX2 paketi açılışta shlx'te düşerdi
        for ad in islemci.EK:
            with self.subTest(eksik=ad):
                self.assertEqual(islemci.paket(dict(TAM, **{ad: False}))[:2], ("uyumlu", [ad]))

    def test_eski_numpy_ek_aileler_bilinmiyor(self):
        self.assertEqual(islemci.paket(ESKI_NUMPY), ("avx2", [], list(islemci.EK)))
        self.assertEqual(islemci.paket(dict(ESKI_NUMPY, AVX2=False)), ("uyumlu", ["AVX2"], list(islemci.EK)))

    def test_denetlenemezse_uyumlu(self):
        with mock.patch.object(islemci, "ozellikler", return_value=None):
            self.assertEqual(islemci.paket(), ("uyumlu", ["denetlenemedi"], []))
        self.assertEqual(islemci.paket({}), ("uyumlu", ["denetlenemedi"], []))

    def test_gercek_tespit_okunur(self):
        oz = islemci.ozellikler()
        self.assertIsInstance(oz, dict)  # numpy kurulu (requirements.txt)
        ad, eksik, _ = islemci.paket(oz)
        self.assertIn(ad, ("avx2", "uyumlu"))
        self.assertEqual(ad == "avx2", not eksik)

    def test_komut_satiri_ilk_satir_karar(self):
        cikti = subprocess.run([sys.executable, "-m", "ses_tasarim.islemci"], cwd=REPO, capture_output=True, text=True,
                               timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        self.assertEqual(cikti.returncode, 0)
        self.assertIn(cikti.stdout.splitlines()[0], ("avx2", "uyumlu"))


class Deneme(unittest.TestCase):
    def _kod(self, kod):
        return mock.patch.object(islemci.subprocess, "run", return_value=subprocess.CompletedProcess([], kod))

    def test_gecersiz_komut_ayirt_edilir(self):
        with self._kod(0xC000001D):          # Windows: işaretsiz çıkış kodu
            self.assertEqual(islemci.dene("motor.exe"), "gecersiz_komut")
        with self._kod(-1073741795):         # aynı kod işaretli tamsayı olarak
            self.assertEqual(islemci.dene("motor.exe"), "gecersiz_komut")

    def test_basari_ve_baska_hata(self):
        with self._kod(0):
            self.assertEqual(islemci.dene("motor.exe"), "ok")
        with self._kod(1):                   # ör. Vulkan sürücüsü yok: paket değiştirmek çözmez
            self.assertEqual(islemci.dene("motor.exe"), "hata 0x1")

    def test_zaman_asimi_hata(self):
        with mock.patch.object(islemci.subprocess, "run", side_effect=subprocess.TimeoutExpired("motor.exe", 1)):
            self.assertEqual(islemci.dene("motor.exe"), "hata TimeoutExpired")

    def test_komut_satiri_dene(self):
        with self._kod(0xC000001D), mock.patch("builtins.print") as yaz:
            self.assertEqual(islemci.main(["--dene", "motor.exe"]), 0)
        yaz.assert_called_once_with("gecersiz_komut")

    @unittest.skipUnless(sys.platform == "win32", "Windows hata kipi / Windows error mode")
    def test_hata_kutusu_kapali_ve_geri_alinir(self):
        import ctypes
        k32 = ctypes.windll.kernel32
        once = k32.GetErrorMode()
        gorulen = []
        with mock.patch.object(islemci.subprocess, "run",
                               side_effect=lambda *a, **kw: gorulen.append(k32.GetErrorMode()) or subprocess.CompletedProcess([], 0)):
            self.assertEqual(islemci.dene("motor.exe"), "ok")
        self.assertEqual(gorulen[0] & islemci.SESSIZ_HATA, islemci.SESSIZ_HATA)   # çocuk süreç bu kiple başlar
        self.assertEqual(k32.GetErrorMode(), once)                               # sonra eski kip

    def test_exe_yoksa_hata(self):
        self.assertTrue(islemci.dene(REPO / "yok" / "motor.exe").startswith("hata "))

    @unittest.skipUnless(sys.platform == "win32", "Windows çıkış kodu / Windows exit code")
    def test_gercek_surec_gecersiz_komut_kodu(self):
        # gerçek bir süreç 0xC000001D ile biterse dene() bunu tanır (exe yerine python, aynı çıkış kodu)
        gercek_run = subprocess.run

        def calistir(argv, **kw):
            return gercek_run([sys.executable, "-c", "import ctypes; ctypes.windll.kernel32.ExitProcess(0xC000001D)"], **kw)
        with mock.patch.object(islemci.subprocess, "run", side_effect=calistir):
            self.assertEqual(islemci.dene("motor.exe"), "gecersiz_komut")


if __name__ == "__main__":
    unittest.main()

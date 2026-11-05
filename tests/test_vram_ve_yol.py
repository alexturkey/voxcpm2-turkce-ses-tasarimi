"""AMD/Intel topluluk testi bulguları (issue #6): VRAM ölçülemezse 0 değil None; ASCII olmayan yolda anlaşılır ipucu.
GPU'suz, ağsız; motor ve ölçüm aracı taklit edilir.
Findings from the AMD/Intel community test (issue #6): unmeasured VRAM is None, not 0; clear hint for non-ASCII paths.

python -m unittest discover -s tests -v
"""
import ctypes
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from ses_tasarim import arayuz, motor


class VramOlcumu(unittest.TestCase):
    def _izle(self, degerler):
        """Döngü aynı iş parçacığında, beklemesiz koşar; değerler bitince durur. / Loop runs inline, no waiting."""
        izci = motor.VramWatcher()
        kalan = list(degerler)

        def olcum(*_args):
            if not kalan:
                izci._stop.set()
                raise RuntimeError("son")
            deger = kalan.pop(0)
            if isinstance(deger, BaseException):
                raise deger
            return deger

        with mock.patch.object(motor, "_gpu_used_mb", olcum), mock.patch.object(izci._stop, "wait"):
            izci._loop()
        return izci.peak_mb

    def test_olcum_araci_yoksa_none(self):
        # AMD/Intel: nvidia-smi yok → 0 değil None (0 "bellek kullanmadı" diye okunurdu); döngü hemen biter
        self.assertIsNone(self._izle([FileNotFoundError("nvidia-smi"), 900]))

    def test_olcum_varsa_tepe(self):
        self.assertEqual(self._izle([300, 900, RuntimeError("anlik"), 500]), 900)

    def test_windows_vulkan_motor_pid_sayacini_kullanir(self):
        completed = SimpleNamespace(stdout="2815\n")
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor.subprocess, "run", return_value=completed) as run:
            self.assertEqual(motor._gpu_used_mb("vulkan", 1234), 2815)

        command = run.call_args.args[0]
        self.assertEqual(command[:4], ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command"])
        self.assertIn("pid_1234_%", command[4])
        self.assertIn("GPUProcessMemory", command[4])
        self.assertIn("DedicatedUsage", command[4])

    def test_windows_vulkan_sayac_yoksa_olculemedi(self):
        # sayaç satırı yoksa betik 0 basar; bu ölçüm sayılmaz, tepe None kalır (özet "VRAM ölçülemedi")
        completed = SimpleNamespace(stdout="0\n")
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor.subprocess, "run", return_value=completed):
            with self.assertRaises(ValueError):
                motor._gpu_used_mb("vulkan", 1234)
            izci = motor.VramWatcher("vulkan", 1234)
            with mock.patch.object(izci._stop, "wait", side_effect=lambda _s: izci._stop.set()):
                izci._loop()
        self.assertIsNone(izci.peak_mb)
        self.assertEqual(motor.vram_metni(izci.peak_mb), "VRAM ölçülemedi")

    def test_pdh_satirlarindan_pid_toplami(self):
        # #17: aynı PID'nin bütün bağdaştırıcı satırları toplanır; başka PID, geçersiz durum sayılmaz
        mb = 1024 * 1024
        ogeler = [("pid_1234_luid_0x0_0x1_phys_0", 0, 2000 * mb), ("pid_1234_luid_0x0_0x2_phys_0", 1, 810 * mb),
                  ("pid_12345_luid_0x0_0x1_phys_0", 0, 999 * mb), ("pid_1234_luid_0x0_0x3_phys_0", 0xC0000BC6, 5 * mb),
                  (None, 0, 7 * mb)]
        self.assertEqual(motor._pid_toplam_mb(ogeler, 1234), 2810)
        with self.assertRaises(ValueError):  # satır yok ya da 0: ölçülemedi / no row or 0: not a reading
            motor._pid_toplam_mb([("pid_1234_luid_0x0_0x1_phys_0", 0, 0)], 1234)
        with self.assertRaises(ValueError):
            motor._pid_toplam_mb([], 1234)

    def test_pdh_varsa_surec_acilmaz_aralik_kisa(self):
        # #17: PDH açılınca PowerShell çağrılmaz, aralık 0,5 sn, tepe alınır, sorgu kapanır
        sahte = mock.Mock()
        sahte.oku_mb.side_effect = [1500, ValueError("anlik yok"), 2810, 2000]
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor, "PdhGpuBellek", return_value=sahte), \
                mock.patch.object(motor.subprocess, "run") as run:
            izci = motor.VramWatcher("vulkan", 1234)
            self.assertEqual(izci.interval, 2.0)  # PDH denenmeden önce yedek yolun aralığı / before PDH is tried
            bekleme = []
            with mock.patch.object(izci._stop, "wait",
                                   side_effect=lambda s: (bekleme.append(s), len(bekleme) >= 4 and izci._stop.set())):
                izci._loop()
        run.assert_not_called()
        self.assertEqual(izci.peak_mb, 2810)
        self.assertEqual(set(bekleme), {0.5})
        sahte.oku_mb.assert_called_with(1234)
        sahte.kapat.assert_called_once()

    def test_pdh_yoksa_powershell_yedegi(self):
        # #17: PDH açılamazsa (eski Windows, sayaç yok) PowerShell yolu 2 sn aralıkla sürer
        completed = SimpleNamespace(stdout="2815\n")
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor, "PdhGpuBellek", side_effect=OSError("sayaç yok")), \
                mock.patch.object(motor.subprocess, "run", return_value=completed) as run:
            izci = motor.VramWatcher("vulkan", 1234)
            bekleme = []
            with mock.patch.object(izci._stop, "wait", side_effect=lambda s: (bekleme.append(s), izci._stop.set())):
                izci._loop()
        self.assertEqual(izci.peak_mb, 2815)
        self.assertEqual(bekleme, [2.0])
        self.assertEqual(run.call_args.args[0][0], "powershell.exe")

    def test_pdh_okunamazsa_powershell_yedegine_gecer(self):
        # #17: PDH açıldı ama okuma art arda OSError veriyor: sınırda sorgu kapanır, PowerShell 2 sn aralıkla sürer.
        # ValueError (o an değer yok) sayaca girmez.
        sahte = mock.Mock()
        # araya giren ValueError sayacı sıfırlar (art arda değil); ArgumentError gibi OSError dışı hata da sayılır
        sahte.oku_mb.side_effect = [OSError("x"), ValueError("0"), OSError("a"), ctypes.ArgumentError("b"), OSError("c")]
        completed = SimpleNamespace(stdout="2815\n")
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor, "PdhGpuBellek", return_value=sahte), \
                mock.patch.object(motor.subprocess, "run", return_value=completed) as run:
            izci = motor.VramWatcher("vulkan", 1234)
            bekleme = []
            with mock.patch.object(izci._stop, "wait",
                                   side_effect=lambda s: (bekleme.append(s), len(bekleme) >= 6 and izci._stop.set())):
                izci._loop()
        self.assertEqual(sahte.oku_mb.call_count, 5)
        sahte.kapat.assert_called_once()
        self.assertEqual(bekleme, [0.5, 0.5, 0.5, 0.5, 2.0, 2.0])
        self.assertEqual(run.call_args.args[0][0], "powershell.exe")
        self.assertEqual(izci.peak_mb, 2815)

    def test_cuda_pdh_denemez(self):
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor, "PdhGpuBellek") as pdh:
            self.assertIsNone(motor.VramWatcher("cuda", 1234)._vulkan_pdh())
            self.assertIsNone(motor.VramWatcher("vulkan", None)._vulkan_pdh())
        pdh.assert_not_called()

    @unittest.skipUnless(motor.WINDOWS, "yalnız Windows: gerçek PDH sayacı / Windows only")
    def test_gercek_pdh_acilir_ve_gpusuz_surec_olculemedi(self):
        import os
        try:
            pdh = motor.PdhGpuBellek()
        except OSError as hata:  # sayaç bu Windows'ta yoksa (1709 öncesi) atla / counter missing on old Windows
            self.skipTest(f"PDH GPU sayacı yok: {hata}")
        try:
            self.assertIsInstance(pdh.ogeler(), list)
            with self.assertRaises(ValueError):  # test süreci GPU belleği ayırmaz / the test process holds no VRAM
                pdh.oku_mb(os.getpid())
        finally:
            pdh.kapat()

    def test_olcum_araligi(self):
        # Windows Vulkan her ölçümde PowerShell açar: 2 sn; CUDA ve macOS 0,5 sn kalır
        with mock.patch.object(motor, "WINDOWS", True):
            self.assertEqual(motor.VramWatcher("vulkan", 1234).interval, 2.0)
            self.assertEqual(motor.VramWatcher("cuda", 1234).interval, 0.5)
            self.assertEqual(motor.VramWatcher("vulkan", None).interval, 0.5)
        with mock.patch.object(motor, "WINDOWS", False):  # macOS (ioreg) ve Linux
            self.assertEqual(motor.VramWatcher("metal", 1234).interval, 0.5)
            self.assertEqual(motor.VramWatcher("vulkan", 1234).interval, 0.5)
        # döngü bu aralıkla bekler / the loop waits with this interval
        izci = motor.VramWatcher("cuda", None)
        izci.interval = 2.0
        bekleme = []
        with mock.patch.object(motor, "_gpu_used_mb", return_value=100), \
                mock.patch.object(izci._stop, "wait", side_effect=lambda s: (bekleme.append(s), izci._stop.set())):
            izci._loop()
        self.assertEqual(bekleme, [2.0])

    def test_cuda_nvidia_smi_yolunu_korur(self):
        completed = SimpleNamespace(stdout="3072\n")
        with mock.patch.object(motor, "WINDOWS", True), \
                mock.patch.object(motor.subprocess, "run", return_value=completed) as run:
            self.assertEqual(motor._gpu_used_mb("cuda", 1234), 3072)

        self.assertEqual(run.call_args.args[0][0], "nvidia-smi")

    def test_birlestirme_ve_metin(self):
        self.assertIsNone(motor.vram_max(None, None))
        self.assertEqual(motor.vram_max(None, 700), 700)
        self.assertEqual(motor.vram_max(900, 700), 900)
        self.assertEqual(motor.vram_metni(900), "VRAM tepe 900 MB")
        self.assertEqual(motor.vram_metni(None), "VRAM ölçülemedi")

    def test_arayuz_vramsiz_ozet(self):
        # sunucu VRAM ölçülemediyse ayrı durum kodu verir, arayüz VRAM'siz özeti seçer
        self.assertIn('"bitti_tasarla_vramsiz"', Path(arayuz.__file__).read_text(encoding="utf-8"))
        self.assertIn("r.vram_tepe_mb==null?t('okuma_ozet_vramsiz'", arayuz.HTML)


def _yok():
    raise FileNotFoundError("nvidia-smi")


class _DusenMotor:
    returncode = 1

    def poll(self):
        return 1


class AsciiYol(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_ascii_olmayan_ilk_yol(self):
        self.assertIsNone(motor.ascii_olmayan_yol(["C:/vox/model.gguf", None, ""]))
        self.assertEqual(motor.ascii_olmayan_yol(["C:/vox/a.wav", "D:/Sesler/Varsayılan/b.wav"]),
                         "D:/Sesler/Varsayılan/b.wav")

    def _calistir(self, klasor, windows):
        ayar = {"motor": Path("C:/vox/motor.exe"), "model": Path("C:/vox/model.gguf"), "onbellek": self.tmp / "onb"}
        istek = [motor.read_request("s1", "Merhaba.", 7, klasor / "referans.wav", "Merhaba dünya.")]
        with mock.patch.object(motor, "WINDOWS", windows), \
                mock.patch.object(motor, "_gpu_used_mb", _yok), \
                mock.patch.object(motor.subprocess, "Popen", lambda *a, **k: _DusenMotor()):
            with self.assertRaises(motor.MotorHatasi) as hata:
                motor.run_sequence(ayar, istek, klasor)
        return str(hata.exception)

    def test_windows_turkce_klasorde_ipucu(self):
        mesaj = self._calistir(self.tmp / "Varsayılan", windows=True)
        self.assertIn("ASCII", mesaj)
        self.assertIn("Varsayılan", mesaj)
        self.assertIn("C:\\vox", mesaj)

    def test_ascii_klasorde_ipucu_yok(self):
        self.assertNotIn("ASCII", self._calistir(self.tmp / "deneme", windows=True))

    def test_windows_disinda_ipucu_yok(self):
        self.assertNotIn("ASCII", self._calistir(self.tmp / "Varsayılan", windows=False))


if __name__ == "__main__":
    unittest.main()

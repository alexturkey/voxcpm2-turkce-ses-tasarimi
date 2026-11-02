"""AMD/Intel topluluk testi bulguları (issue #6): VRAM ölçülemezse 0 değil None; ASCII olmayan yolda anlaşılır ipucu.
GPU'suz, ağsız; motor ve ölçüm aracı taklit edilir.
Findings from the AMD/Intel community test (issue #6): unmeasured VRAM is None, not 0; clear hint for non-ASCII paths.

python -m unittest discover -s tests -v
"""
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ses_tasarim import arayuz, motor


class VramOlcumu(unittest.TestCase):
    def _izle(self, degerler):
        """Döngü aynı iş parçacığında, beklemesiz koşar; değerler bitince durur. / Loop runs inline, no waiting."""
        izci = motor.VramWatcher()
        kalan = list(degerler)

        def olcum():
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

    def test_birlestirme_ve_metin(self):
        self.assertIsNone(motor.vram_max(None, None))
        self.assertEqual(motor.vram_max(None, 700), 700)
        self.assertEqual(motor.vram_max(900, 700), 900)
        self.assertEqual(motor.vram_metni(900), "VRAM tepe 900 MB")
        self.assertIn("ölçülemedi", motor.vram_metni(None))

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

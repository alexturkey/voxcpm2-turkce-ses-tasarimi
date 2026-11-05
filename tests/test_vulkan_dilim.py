"""Vulkan kartının iş kümesi sınırına göre AudioVAE GPU dilim boyu (Intel HD 630 30 sn tasarım çökmesi).
GPU'suz: kart listesi taklit edilir; gerçek Vulkan sorgusu yalnız kitaplık varsa denenir.
AudioVAE GPU chunk chosen from the Vulkan device work-group limit; GPU-free except the optional real query.

python -m unittest discover -s tests -v
"""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from ses_tasarim import motor, vulkan_sinir

INTEL = {"ad": "Intel(R) HD Graphics 630", "tur": 1, "is_kumesi": 65536, "paylasimli_bellek": 32768}
NVIDIA = {"ad": "NVIDIA GeForce GTX 1050 Ti", "tur": 2, "is_kumesi": 2147483647, "paylasimli_bellek": 49152}
AMD = {"ad": "AMD Radeon RX 6900 XT", "tur": 2, "is_kumesi": 4294967295, "paylasimli_bellek": 65536}


class DilimBoyu(unittest.TestCase):
    def test_dusuk_sinirli_kart_kisa_dilim(self):
        liste = [INTEL, NVIDIA]
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": 0}, liste), (5.0, INTEL["ad"]))
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": None}, liste), (5.0, INTEL["ad"]))

    def test_nvidia_amd_10_sn_kalir(self):
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": 1}, [INTEL, NVIDIA]),
                         (10.0, NVIDIA["ad"]))
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": "0"}, [AMD]), (10.0, AMD["ad"]))

    def test_cuda_ve_metal_sorgulamaz(self):
        with mock.patch.object(vulkan_sinir, "aygitlar") as sorgu:
            self.assertEqual(vulkan_sinir.dilim_sn({"backend": "cuda", "cihaz": 0}), (10.0, None))
            self.assertEqual(vulkan_sinir.dilim_sn({"backend": "metal"}), (10.0, None))
        sorgu.assert_not_called()

    def test_sorgu_duserse_ya_da_numara_disi_varsayilan(self):
        # sürücü/kitaplık yok ya da cihaz numarası listede yok: davranış eskisi gibi 10 sn
        with mock.patch.object(vulkan_sinir, "aygitlar", side_effect=OSError("vulkan-1 yok")):
            self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": 0}), (10.0, None))
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": 5}, [NVIDIA]), (10.0, None))
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": 0}, [dict(INTEL, is_kumesi=0)]),
                         (10.0, INTEL["ad"]))
        # negatif numara listenin sonundaki kartı seçmez / a negative index never wraps to the last device
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": -1}, [NVIDIA, INTEL]), (10.0, None))
        self.assertIsNone(vulkan_sinir.motor_adi("ggml_vulkan: 0 = X (Y) | uma: 0", "abc"))

    def test_esik_siniri(self):
        az = dict(INTEL, is_kumesi=vulkan_sinir.DUSUK_SINIR - 1)
        tam = dict(INTEL, is_kumesi=vulkan_sinir.DUSUK_SINIR)
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan"}, [az])[0], 5.0)
        self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan"}, [tam])[0], 10.0)


def _ham(ad, tur, uuid, luid=None, sinir=65536):
    return {"ad": ad, "tur": tur, "is_kumesi": sinir, "paylasimli_bellek": 32768, "_uuid": uuid, "_luid": luid}


class MotorSirasi(unittest.TestCase):
    """ggml-vulkan numaralandırması (ggml-vulkan.cpp ggml_vk_instance_init) / ggml device numbering."""

    def test_yalniz_ayrik_ve_gomulu_ciftler_atlanir(self):
        hepsi = [_ham("llvmpipe", 4, b"c"), _ham("Intel", 1, b"i", b"L1"), _ham("NVIDIA", 2, b"n", b"L2"),
                 _ham("NVIDIA ikinci surucu", 2, b"n2", b"L2"), _ham("Sanal", 3, b"v")]
        self.assertEqual([a["ad"] for a in vulkan_sinir.sirala(hepsi)], ["Intel", "NVIDIA"])
        self.assertNotIn("_uuid", vulkan_sinir.sirala(hepsi)[0])

    def test_kart_yoksa_cpu_olmayan_ilk_aygit(self):
        hepsi = [_ham("llvmpipe", 4, b"c"), _ham("Sanal", 3, b"v"), _ham("Sanal2", 3, b"w")]
        self.assertEqual([a["ad"] for a in vulkan_sinir.sirala(hepsi)], ["Sanal"])

    def test_gorunur_aygitlar_ham_sirayi_kullanir(self):
        # GGML_VK_VISIBLE_DEVICES varken ggml süzgeç uygulamaz, ham numaraları verilen sırayla alır
        hepsi = [_ham("llvmpipe", 4, b"c"), _ham("Intel", 1, b"i"), _ham("NVIDIA", 2, b"n")]
        self.assertEqual([a["ad"] for a in vulkan_sinir.sirala(hepsi, "2,0")], ["NVIDIA", "llvmpipe"])
        with mock.patch.object(vulkan_sinir, "_ham_aygitlar", return_value=tuple(hepsi)), \
                mock.patch.dict(vulkan_sinir.os.environ, {"GGML_VK_VISIBLE_DEVICES": "2"}):
            self.assertEqual(vulkan_sinir.aygitlar()[0]["ad"], "NVIDIA")

    def test_eski_yukleyici_oserror(self):
        # Vulkan 1.1 öncesi yükleyicide vkGetPhysicalDeviceProperties2 yok: OSError, dilim 10 sn
        class EskiKitaplik:
            vkCreateInstance = vkEnumeratePhysicalDevices = vkDestroyInstance = mock.Mock()

        vulkan_sinir._ham_aygitlar.cache_clear()
        try:
            with mock.patch.object(vulkan_sinir, "_kitaplik", return_value=EskiKitaplik()):
                with self.assertRaises(OSError):
                    vulkan_sinir._ham_aygitlar()
                self.assertEqual(vulkan_sinir.dilim_sn({"backend": "vulkan", "cihaz": 0}), (10.0, None))
        finally:
            vulkan_sinir._ham_aygitlar.cache_clear()

    def test_motor_ortami_dilimi_tasir(self):
        ayar = {"backend": "vulkan", "cihaz": 0, "onbellek": Path(tempfile.gettempdir())}
        with mock.patch.object(vulkan_sinir, "aygitlar", return_value=[INTEL, NVIDIA]):
            self.assertEqual(motor.engine_env(ayar, Path("."))["VOXCPM2_AUDIOVAE_GPU_CHUNK"], "5")
            self.assertEqual(motor.engine_env(dict(ayar, cihaz=1), Path("."))["VOXCPM2_AUDIOVAE_GPU_CHUNK"], "10")
        self.assertEqual(motor.engine_env(dict(ayar, backend="cuda"), Path("."))["VOXCPM2_AUDIOVAE_GPU_CHUNK"], "10")

    def test_motorun_kart_adi_okunur(self):
        metin = ("ggml_vulkan: Found 2 Vulkan devices:\n"
                 "ggml_vulkan: 0 = Intel(R) HD Graphics 630 (Intel Corporation) | uma: 1 | fp16: 1 | bf16: 0\n"
                 "ggml_vulkan: 1 = NVIDIA GeForce GTX 1050 Ti (NVIDIA) | uma: 0 | fp16: 0 | bf16: 0\n")
        self.assertEqual(vulkan_sinir.motor_adi(metin, 0), INTEL["ad"])
        self.assertEqual(vulkan_sinir.motor_adi(metin, "1"), NVIDIA["ad"])
        self.assertIsNone(vulkan_sinir.motor_adi(metin, 2))

    def test_kart_uyusmazsa_uyari(self):
        with tempfile.TemporaryDirectory() as klasor:
            yol = Path(klasor) / "stdout.txt"
            yol.write_text("ggml_vulkan: 0 = NVIDIA GeForce GTX 1050 Ti (NVIDIA) | uma: 0\n", encoding="utf-8")
            with mock.patch.object(vulkan_sinir, "aygitlar", return_value=[INTEL]), \
                    mock.patch("builtins.print") as yaz:
                motor._dilim_karti_denetle({"backend": "vulkan", "cihaz": 0}, yol)
            self.assertIn("uyarı", yaz.call_args.args[0])
            with mock.patch.object(vulkan_sinir, "aygitlar", return_value=[NVIDIA]), \
                    mock.patch("builtins.print") as yaz:
                motor._dilim_karti_denetle({"backend": "vulkan", "cihaz": 0}, yol)
            yaz.assert_not_called()


class GercekSorgu(unittest.TestCase):
    def test_kitaplik_varsa_liste_tutarli(self):
        try:
            liste = vulkan_sinir.aygitlar()
        except OSError as hata:  # Vulkan sürücüsü yok (CI, macOS) / no Vulkan driver
            self.skipTest(f"Vulkan yok: {hata}")
        for aygit in liste:
            self.assertTrue(aygit["ad"])
            self.assertGreater(aygit["is_kumesi"], 0)
            self.assertGreaterEqual(aygit["paylasimli_bellek"], 16384)  # Vulkan asgarisi / spec minimum


if __name__ == "__main__":
    unittest.main()

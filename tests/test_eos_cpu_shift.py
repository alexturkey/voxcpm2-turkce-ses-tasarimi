"""CPU arka ucunda EOS blok eşleşmesi: aynı istekteki fazla kod çözücü satırları bloğu kaydırmamalı.

CPU backend EOS blocks: extra AudioVAE decoder timing lines inside one request must not shift the next request.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from ses_tasarim import motor


class EosCpuBlokKaymasi(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _log_yaz(self, satirlar):
        path = self.tmp / "motor.log"
        path.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        return path

    def _eski_cpu_sayaci(self, log_path, count):
        """PR #14'ün düzeltme öncesi CPU dalı: her audiovae_decoder_ms satırı yeni blok sayılır."""
        ok, block = [False] * count, 0
        for line in log_path.read_text(encoding="utf-8").splitlines():
            if block < count and "eos_accepted_at_patch" in line:
                ok[block] = True
            if "voxcpm2.toplu_coz.deferred" in line or "voxcpm2.audiovae_decoder_ms" in line:
                block += 1
        return ok

    def test_cpu_tek_decode_satirinda_eslesme_dogru(self):
        log = self._log_yaz([
            "eos_accepted_at_patch 12",
            "voxcpm2.audiovae_decoder_ms 900.0",
            "eos_accepted_at_patch 13",
            "voxcpm2.audiovae_decoder_ms 800.0",
        ])
        self.assertEqual(motor._eos_by_block(log, 2, cpu=True), [True, True])

    def test_cpu_fazla_decode_satiri_eski_sayaci_kaydiriyor(self):
        log = self._log_yaz([
            "eos_accepted_at_patch 12",
            "voxcpm2.audiovae_decoder_ms 900.0",
            "voxcpm2.audiovae_decoder_ms 120.0",
            "eos_accepted_at_patch 13",
            "voxcpm2.audiovae_decoder_ms 800.0",
        ])
        self.assertEqual(self._eski_cpu_sayaci(log, 2), [True, False])
        self.assertEqual(motor._eos_by_block(log, 2, cpu=True), [True, True])

    def test_gpu_yolu_degismedi(self):
        log = self._log_yaz([
            "eos_accepted_at_patch 1",
            "voxcpm2.toplu_coz.deferred 1.0",
            "eos_accepted_at_patch 2",
            "voxcpm2.toplu_coz.deferred 1.0",
        ])
        self.assertEqual(motor._eos_by_block(log, 2), [True, True])


if __name__ == "__main__":
    unittest.main()

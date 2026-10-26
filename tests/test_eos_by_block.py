"""CPU blok sonları ve eski GPU davranışı (model, GPU ve ses üretimi gerekmez).
CPU block endings and legacy GPU behavior (no model, GPU or audio generation).

python -m unittest discover -s tests -p 'test_eos_by_block.py' -v
"""
import tempfile
import unittest
from pathlib import Path

from ses_tasarim import motor


class EosByBlock(unittest.TestCase):
    def test_iki_cumle_cpu_logu(self):
        log = ("eos_accepted_at_patch 12\n"
               "voxcpm2.audiovae_decoder_ms 100\n"
               "eos_accepted_at_patch 15\n"
               "voxcpm2.audiovae_decoder_ms 120\n")
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "motor.log"
            log_path.write_text(log, encoding="utf-8")
            for cpu, expected in ((True, [True, True]), (False, [True, False])):
                with self.subTest(cpu=cpu):
                    # CPU değilse decoder satırı blok ilerletmez; iki EOS da ilk bloğa yazılır.
                    self.assertEqual(motor._eos_by_block(log_path, 2, cpu=cpu), expected)
            self.assertEqual(motor._eos_by_block(log_path, 2), [True, False])

    def test_gpu_deferred_blok_sonlari(self):
        log = ("eos_accepted_at_patch 12\n"
               "voxcpm2.toplu_coz.deferred\n"
               "eos_accepted_at_patch 15\n"
               "voxcpm2.toplu_coz.deferred\n")
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "motor.log"
            log_path.write_text(log, encoding="utf-8")
            self.assertEqual(motor._eos_by_block(log_path, 2, cpu=False), [True, True])


if __name__ == "__main__":
    unittest.main()

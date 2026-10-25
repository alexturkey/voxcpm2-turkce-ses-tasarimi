"""Motor ara dosyaları: iş başarıyla bitince silinir, yarım satır ya da hata olursa inceleme için kalır (GPU'suz).

Engine scratch files: removed after a successful run, kept when a line failed (no GPU; the engine is faked).
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from ses_tasarim import motor


class SahteMotor:
    """Gerçek motorun bıraktığı dosyaları yazar: dizi, log (EOS işaretleri), çıktı wav'ları, PCM dökümü."""

    eos = True

    def __init__(self, command, env=None, stdout=None, stderr=None, creationflags=0):
        arg = dict(zip(command, command[1:]))
        requests = json.loads(Path(arg["--request-sequence"]).read_text(encoding="utf-8"))["requests"]
        out = Path(arg["--out-dir"])
        out.mkdir(parents=True, exist_ok=True)
        with open(arg["--log-file"], "w", encoding="utf-8") as log:
            for request in requests:
                motor.write_wav(out / f"{request['id']}.wav", np.zeros(4800, dtype=np.float32))
                if self.eos:
                    log.write("eos_accepted_at_patch 12\n")
                log.write("voxcpm2.toplu_coz.deferred\n")
        (Path(env["VOXCPM2_PROBE_PCM_DIR"]) / "decoded_pcm.f32").write_bytes(b"\0" * 64)
        self.returncode = 0

    def poll(self):
        return self.returncode


class AraDosya(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.settings = {"motor": "motor.exe", "model": "model.gguf", "onbellek": self.tmp / "onbellek"}
        self.requests = [{"id": "s1", "text": "bir"}, {"id": "s2", "text": "iki"}]
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def _calistir(self, eos=True, env=None):
        SahteMotor.eos = eos
        with mock.patch.object(motor.subprocess, "Popen", SahteMotor), \
                mock.patch.dict(os.environ, env or {}, clear=False):
            return motor.run_sequence(self.settings, [dict(r) for r in self.requests], self.tmp / "is")

    def test_basarida_silinir(self):
        sonuc = self._calistir()
        self.assertEqual(sorted(sonuc["audios"]), ["s1", "s2"])
        self.assertEqual(sonuc["bad"], [])
        self.assertFalse((self.tmp / "is" / motor.ENGINE_DIR).exists())

    def test_yarim_satirda_kalir(self):
        sonuc = self._calistir(eos=False)
        self.assertEqual(sonuc["bad"], ["s1", "s2"])
        self.assertTrue((self.tmp / "is" / motor.ENGINE_DIR / "motor.log").exists())

    def test_saklama_degiskeni(self):
        self._calistir(env={motor.KEEP_ENV: "1"})
        self.assertTrue((self.tmp / "is" / motor.ENGINE_DIR / "decoded_pcm.f32").exists())


if __name__ == "__main__":
    unittest.main()

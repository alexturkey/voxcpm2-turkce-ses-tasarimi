"""CUDA runtime validation: Windows DLLs are required only on Windows (no GPU needed)."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ses_tasarim import ayarlar


class CudaSettings(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        (self.root / 'engine').touch()
        (self.root / 'model.gguf').touch()
        self.config = self.root / 'ayarlar.json'
        self.data = dict(motor='engine', model='model.gguf', backend='cuda', cuda_bin='')

    def load(self, platform):
        self.config.write_text(json.dumps(self.data), encoding='utf-8')
        # Path selects its implementation via os.name, not sys.platform.
        with patch.object(ayarlar.sys, 'platform', platform):
            return ayarlar.load(self.config)

    def test_linux_uses_system_cuda_libraries(self):
        settings = self.load('linux')
        self.assertIsNone(settings['cuda_bin'])
        self.assertEqual(settings['motor'], self.root / 'engine')

    def test_windows_still_requires_cuda_dll(self):
        with self.assertRaisesRegex(ayarlar.AyarHatasi, 'cudart64_12.dll'):
            self.load('win32')
        dll_dir = self.root / 'cuda'
        dll_dir.mkdir()
        (dll_dir / 'cudart64_12.dll').touch()
        self.data['cuda_bin'] = 'cuda'
        self.assertEqual(self.load('win32')['cuda_bin'], dll_dir)

    def test_linux_still_requires_engine_and_model(self):
        (self.root / 'engine').unlink()
        (self.root / 'model.gguf').unlink()
        with self.assertRaises(ayarlar.AyarHatasi) as error:
            self.load('linux')
        self.assertIn('motor bulunamadı', str(error.exception))
        self.assertIn('model bulunamadı', str(error.exception))

    def test_metal_does_not_require_cuda(self):
        self.data['backend'] = 'metal'
        self.assertEqual(self.load('darwin')['backend'], 'metal')

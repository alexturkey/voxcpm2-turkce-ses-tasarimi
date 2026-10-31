"""Linux installer failure/re-run behavior, without network, CUDA or a real model."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(sys.platform.startswith('linux'), 'Linux installer')
class LinuxInstaller(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.repo = self.root / 'repo with spaces'
        (self.repo / 'scripts').mkdir(parents=True)
        self.script = self.repo / 'scripts/kur-linux.sh'
        shutil.copyfile(Path(__file__).resolve().parents[1] / 'scripts/kur-linux.sh', self.script)
        self.data = self.root / 'engine and model'
        (self.repo / '.venv/bin').mkdir(parents=True)
        (self.repo / '.venv/bin/python').symlink_to(sys.executable)

    def run_installer(self, *args, env=None):
        return subprocess.run(['bash', str(self.script), '--kok', str(self.data), *args],
                              cwd=self.root, env=env, capture_output=True, text=True, timeout=20)

    def test_settings_rerun_preserves_choices_and_backs_up(self):
        config = self.repo / 'ayarlar.json'
        original = dict(port=8800, motor_threads=2, sesler='my voices')
        config.write_text(json.dumps(original), encoding='utf-8')
        for _ in range(2):
            result = self.run_installer('--adim', 'ayar')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        settings = json.loads(config.read_text(encoding='utf-8'))
        for key, value in original.items():
            self.assertEqual(settings[key], value)
        self.assertEqual(settings['backend'], 'cuda')
        self.assertEqual(settings['cuda_bin'], '')
        self.assertEqual(settings['model'], str(self.data / 'model/voxcpm2-q8_0.gguf'))
        backups = list(self.repo.glob('ayarlar.json.bak-*'))
        self.assertEqual(len(backups), 2)
        self.assertIn(original, [json.loads(p.read_text(encoding='utf-8')) for p in backups])

    def test_invalid_options_fail_before_creating_root(self):
        for args in [('--adim', 'unknown'), ('--adim', 'model,,ayar'),
                     ('--paralel', '0'), ('--kok',)]:
            with self.subTest(args=args):
                result = self.run_installer(*args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse(self.data.exists())

    def test_bad_download_is_not_installed(self):
        fake_bin = self.root / 'bin'
        fake_bin.mkdir()
        curl = fake_bin / 'curl'
        curl.write_text('#!' + sys.executable + '\n'
                        'import pathlib,sys\n'
                        'pathlib.Path(sys.argv[sys.argv.index("-o")+1]).write_bytes(b"bad download")\n',
                        encoding='utf-8')
        curl.chmod(0o755)
        env = dict(os.environ, PATH=str(fake_bin) + os.pathsep + os.environ['PATH'])
        result = self.run_installer('--adim', 'model', env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SHA256 mismatch', result.stderr)
        self.assertFalse((self.data / 'model/voxcpm2-q8_0.gguf').exists())
        self.assertFalse((self.data / 'model/voxcpm2-q8_0.gguf.part').exists())

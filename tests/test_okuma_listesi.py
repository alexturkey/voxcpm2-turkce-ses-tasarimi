"""Okuma listesi: kayıt dosyası, kimlik denetimi ve arayüz sunucusu uçları (GPU ve ağ gerekmez; geçici klasörde).
Reading list: storage file, identity checks and the web UI endpoints (no GPU, no network; runs in a temp folder).

python -m unittest discover -s tests -v
"""
import http.client
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

from ses_tasarim import arayuz, oku, okuma_listesi, okunus


def ses_yaz(folder: Path, **card):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "ses.json").write_text(json.dumps({"okuma_tohumu": 1, **card}), encoding="utf-8")


class Ortam(unittest.TestCase):
    """Geçici ayar: iki hazır ses (biri dil alansız, eski kart gibi) ve iki çeşitli bir tasarlanan ses.
    Temp settings: two bundled voices (one without a language field, like the old cards) and one designed voice."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.settings = {"sesler": root / "sesler", "hazir_sesler": root / "hazir"}
        ses_yaz(root / "hazir" / "anlatici_fr", ad="anlatici_fr", dil="fr")
        ses_yaz(root / "hazir" / "belgesel_hanim", ad="belgesel_hanim")
        ses_yaz(root / "sesler" / "deniz" / "cesit_01", ad="deniz", dil="tr")
        ses_yaz(root / "sesler" / "deniz" / "cesit_02", ad="deniz", dil="tr")
        (root / "sesler" / "_okumalar").mkdir()
        self.hazir_once = sorted(p.name for p in (root / "hazir").rglob("*"))
        self.dosya = self.settings["sesler"] / okuma_listesi.DOSYA

    def tearDown(self):
        self._tmp.cleanup()

    def gecerli(self):
        voices = oku.list_voices(self.settings)
        return {card["kimlik"] for group in ("hazir", "tasarlanan") for card in voices[group]}

    def degistir(self, kimlik, ekle=True):
        return okuma_listesi.degistir(self.settings, kimlik, ekle, self.gecerli())


class Modul(Ortam):
    def test_empty_when_missing(self):
        self.assertEqual(okuma_listesi.oku(self.settings), [])

    def test_add_keeps_order_and_no_duplicates(self):
        self.assertEqual(self.degistir("deniz/2"), ["deniz/2"])
        self.assertEqual(self.degistir("hazir/anlatici_fr"), ["deniz/2", "hazir/anlatici_fr"])
        self.assertEqual(self.degistir("deniz/2"), ["deniz/2", "hazir/anlatici_fr"])  # ikinci ekleme etkisiz
        self.assertEqual(okuma_listesi.oku(self.settings), ["deniz/2", "hazir/anlatici_fr"])
        data = json.loads(self.dosya.read_text(encoding="utf-8"))
        self.assertEqual(data, {"surum": 1, "sesler": ["deniz/2", "hazir/anlatici_fr"]})
        self.assertFalse(self.dosya.with_name(self.dosya.name + ".tmp").exists())

    def test_remove(self):
        self.degistir("deniz/1")
        self.degistir("hazir/belgesel_hanim")
        self.assertEqual(self.degistir("deniz/1", False), ["hazir/belgesel_hanim"])
        self.assertEqual(self.degistir("deniz/1", False), ["hazir/belgesel_hanim"])  # zaten yok: etkisiz

    def test_unknown_and_unsafe_ids_are_refused(self):
        kotu = ["yok/1", "hazir/yok", "../deniz/1", "deniz/../1", "C:/x/1", "deniz\\1", "/deniz/1", "deniz",
                "a/b/c", "", "   ", "x" * 300, None, 5, ["deniz/1"], str(self.settings["sesler"] / "deniz" / "cesit_01")]
        for kimlik in kotu:
            with self.subTest(kimlik=kimlik), self.assertRaises(ValueError) as ctx:
                self.degistir(kimlik)
            if isinstance(kimlik, str) and len(kimlik) < 300:
                sorun = ctx.exception.args[0]
                self.assertIsInstance(sorun, okunus.Sorun)
                self.assertEqual(sorun.kod, "ses_yok")
        self.assertFalse(self.dosya.exists())

    def test_ekle_must_be_bool(self):
        for ekle in ("true", 1, None):
            with self.subTest(ekle=ekle), self.assertRaises(ValueError):
                okuma_listesi.degistir(self.settings, "deniz/1", ekle, self.gecerli())

    def test_deleted_voice_kept_in_file_hidden_from_ui(self):
        self.degistir("deniz/2")
        self.degistir("deniz/1")
        gecerli = self.gecerli() - {"deniz/2"}  # klasörü silinmiş gibi / as if its folder was deleted
        self.assertEqual(okuma_listesi.degistir(self.settings, "hazir/anlatici_fr", True, gecerli),
                         ["deniz/1", "hazir/anlatici_fr"])
        self.assertEqual(okuma_listesi.oku(self.settings), ["deniz/2", "deniz/1", "hazir/anlatici_fr"])
        # silinmiş sesin kaydı yine de çıkarılabilir / a deleted voice can still be removed
        self.assertEqual(okuma_listesi.degistir(self.settings, "deniz/2", False, gecerli), ["deniz/1", "hazir/anlatici_fr"])
        self.assertEqual(okuma_listesi.oku(self.settings), ["deniz/1", "hazir/anlatici_fr"])

    def test_corrupt_file_reads_empty_and_is_set_aside(self):
        self.dosya.write_text("{bozuk", encoding="utf-8")
        self.assertEqual(okuma_listesi.oku(self.settings), [])
        self.assertTrue(self.dosya.exists())  # okuma dosyaya dokunmaz / reading does not touch the file
        self.assertEqual(self.degistir("deniz/1"), ["deniz/1"])
        self.assertEqual(self.dosya.with_name(self.dosya.name + ".bozuk").read_text(encoding="utf-8"), "{bozuk")
        for icerik in ('["deniz/1"]', '{"sesler": "deniz/1"}'):
            self.dosya.write_text(icerik, encoding="utf-8")
            self.assertEqual(okuma_listesi.oku(self.settings), [], icerik)

    def test_list_file_is_not_a_voice(self):
        self.degistir("deniz/1")
        self.assertEqual(self.gecerli(), {"hazir/anlatici_fr", "hazir/belgesel_hanim", "deniz/1", "deniz/2"})

    def test_cap(self):
        self.dosya.write_text(json.dumps({"surum": 1, "sesler": [f"x/{i}" for i in range(okuma_listesi.EN_COK)]}),
                              encoding="utf-8")
        with self.assertRaises(ValueError):
            self.degistir("deniz/1")
        self.assertEqual(len(okuma_listesi.oku(self.settings)), okuma_listesi.EN_COK)

    def test_bundled_folder_untouched(self):
        self.degistir("hazir/anlatici_fr")
        self.degistir("hazir/anlatici_fr", False)
        self.assertEqual(sorted(p.name for p in self.settings["hazir_sesler"].rglob("*")), self.hazir_once)

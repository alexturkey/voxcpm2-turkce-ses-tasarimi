"""Ses yönetimi: takma ad, gizleme, çöpe taşıma ve geri getirme (GPU ve ağ gerekmez; geçici klasörde).
Voice management: alias, hide, trash and restore (no GPU, no network; runs in a temp folder).

python -m unittest discover -s tests -v
"""
import json
import tempfile
import unittest
from pathlib import Path

from ses_tasarim import oku, okunus, ses_yonetimi


def ses_yaz(folder: Path, **card):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "ses.json").write_text(json.dumps({"okuma_tohumu": 1, **card}), encoding="utf-8")
    (folder / "referans.wav").write_bytes(b"RIFF")


class SesYonetimi(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.settings = {"sesler": root / "sesler", "hazir_sesler": root / "hazir"}
        ses_yaz(root / "hazir" / "belgesel_hanim", ad="belgesel_hanim", gorunen_ad="Zeynep Belgesel Anlatıcı")
        ses_yaz(root / "sesler" / "deniz" / "cesit_01", ad="deniz", gorunen_ad="Deniz", cesit=1)
        ses_yaz(root / "sesler" / "deniz" / "cesit_02", ad="deniz", gorunen_ad="Deniz", cesit=2)
        self.hazir_once = sorted((str(p), p.stat().st_mtime_ns) for p in (root / "hazir").rglob("*"))
        self.sesjson_once = (root / "sesler" / "deniz" / "cesit_01" / "ses.json").read_bytes()

    def tearDown(self):
        self._tmp.cleanup()

    def gecerli(self):
        v = oku.list_voices(self.settings)
        return {c["kimlik"] for g in ("hazir", "tasarlanan") for c in v[g]}

    def yonet(self, kimlik, islem, ad=None, cop=None):
        return ses_yonetimi.yonet(self.settings, kimlik, islem, ad, self.gecerli(), cop)

    def gorunen(self):
        return ses_yonetimi.uygula(oku.list_voices(self.settings), ses_yonetimi.katman(self.settings))

    def sorun_kodu(self, *a, **k):
        with self.assertRaises(ValueError) as ctx:
            self.yonet(*a, **k)
        self.assertIsInstance(ctx.exception.args[0], okunus.Sorun)
        return ctx.exception.args[0].kod

    def test_rename_and_back(self):
        self.yonet("hazir/belgesel_hanim", "ad", "  Zeynep   Hanım ")
        self.yonet("deniz/2", "ad", "Deniz kızı")
        v = self.gorunen()
        self.assertEqual((v["hazir"][0]["gorunen_ad"], v["hazir"][0]["asil_ad"]), ("Zeynep Hanım", "Zeynep Belgesel Anlatıcı"))
        self.assertEqual([c.get("gorunen_ad") for c in v["tasarlanan"]], ["Deniz", "Deniz kızı"])
        self.yonet("deniz/2", "ad", "")
        self.assertNotIn("asil_ad", self.gorunen()["tasarlanan"][1])
        self.assertEqual(self.sesjson_once, (self.settings["sesler"] / "deniz" / "cesit_01" / "ses.json").read_bytes())

    def test_bad_names(self):
        self.assertEqual(self.sorun_kodu("deniz/1", "ad", "x" * 81), "ad_uzun")
        self.assertEqual(self.sorun_kodu("deniz/1", "ad", "a\nb"), "ad_uzun")
        self.assertEqual(self.sorun_kodu("deniz/1", "ad", 5), "ad_uzun")

    def test_hide_and_show_bundled(self):
        self.yonet("hazir/belgesel_hanim", "gizle")
        v = self.gorunen()
        self.assertEqual((v["hazir"], [c["kimlik"] for c in v["gizli"]]), ([], ["hazir/belgesel_hanim"]))
        self.yonet("hazir/belgesel_hanim", "goster")
        self.assertEqual(self.gorunen()["gizli"], [])
        self.assertEqual(self.sorun_kodu("deniz/1", "gizle"), "islem_yok")
        self.assertEqual(self.sorun_kodu("hazir/belgesel_hanim", "sil"), "islem_yok")

    def test_trash_and_restore(self):
        self.yonet("deniz/2", "sil")
        self.assertNotIn("deniz/2", self.gecerli())
        cop = ses_yonetimi.cop_listesi(self.settings)
        self.assertEqual([(c["kimlik"], c["gorunen_ad"]) for c in cop], [("deniz/2", "Deniz")])
        self.assertTrue((ses_yonetimi.cop_kok(self.settings) / cop[0]["cop"] / "referans.wav").is_file())
        self.yonet(None, "geri", cop=cop[0]["cop"])
        self.assertIn("deniz/2", self.gecerli())
        self.assertFalse((self.settings["sesler"] / "deniz" / "cesit_02" / "kaynak.json").exists())
        self.assertEqual(ses_yonetimi.cop_listesi(self.settings), [])

    def test_restore_refuses_occupied_place(self):
        self.yonet("deniz/2", "sil")
        ses_yaz(self.settings["sesler"] / "deniz" / "cesit_02", ad="deniz", cesit=2)  # yeni tasarım aynı numarayı aldı
        cop = ses_yonetimi.cop_listesi(self.settings)[0]["cop"]
        self.assertEqual(self.sorun_kodu(None, "geri", cop=cop), "hedef_dolu")
        self.assertEqual(len(ses_yonetimi.cop_listesi(self.settings)), 1)

    def test_unsafe_input(self):
        for kimlik in ("../deniz/1", "deniz\\1", "C:/x/1", "/deniz/1", "yok/1", None):
            with self.subTest(kimlik=kimlik):
                self.assertEqual(self.sorun_kodu(kimlik, "sil"), "ses_yok")
        for cop in ("..", "../sesler", "a/b", "a\\b", "", None, "yok"):
            with self.subTest(cop=cop):
                self.assertEqual(self.sorun_kodu(None, "geri", cop=cop), "ses_yok")
        self.assertEqual(self.sorun_kodu("deniz/1", "kalici_sil"), "islem_yok")
        self.assertTrue((self.settings["sesler"] / "deniz" / "cesit_01").is_dir())

    def test_bundled_files_untouched_and_corrupt_layer(self):
        ses_yonetimi.yol(self.settings).write_text("{bozuk", encoding="utf-8")
        self.assertEqual(ses_yonetimi.katman(self.settings), {"surum": 1, "ad": {}, "gizli": []})
        self.yonet("hazir/belgesel_hanim", "ad", "Zeynep")
        self.yonet("hazir/belgesel_hanim", "gizle")
        self.assertTrue(ses_yonetimi.yol(self.settings).with_name("yerel_katman.json.bozuk").is_file())
        self.assertEqual(sorted((str(p), p.stat().st_mtime_ns) for p in self.settings["hazir_sesler"].rglob("*")),
                         self.hazir_once)

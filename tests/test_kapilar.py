"""Repo kapilari (kit KL-01/03/04/05/06/07) kendi kendini sinar: temiz depoda yesil, sahte kotu girdide kirmizi.
Gates test themselves: green on the clean repo, red on synthetic bad input. Ag yok, GPU yok.
Sahte sir/yol/gizli karakter calisma aninda parcalardan uretilir (bu dosya kendi kapisindan temiz gecer).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import dil_eslik_denetimi  # noqa: E402
import gizlilik_denetimi  # noqa: E402
import pr_kapi  # noqa: E402
import yama_bekcisi  # noqa: E402


class Gizlilik(unittest.TestCase):
    def test_sahte_kotu_girdiler_kirmizi(self):
        yol = "C:" + chr(92) + "Users" + chr(92) + "bir" + "kisi" + chr(92) + "x.wav"
        eposta = "ad" + "@" + "gizli-alan" + ".org"
        sir = "gh" + "p_" + "A" * 36
        bidi = "a" + chr(0x202E) + "b"
        for metin, kural in ((yol, "kisisel_yol"), (eposta, "e_posta"), (sir, "sir"), (bidi, "bidi")):
            self.assertIn(kural, [k for k, _, _ in gizlilik_denetimi.tara_metin("docs/x.md", metin)], kural)

    def test_cikti_degeri_basmaz(self):
        yol = "C:" + chr(92) + "Users" + chr(92) + "gizliad" + chr(92) + "x"
        ac = " ".join(a for _, _, a in gizlilik_denetimi.tara_metin("docs/x.md", yol))
        self.assertNotIn("gizliad", ac)

    def test_serbest_olanlar_gecer(self):
        ok = ["noreply@users.noreply.github.com", "C:" + chr(92) + "Users" + chr(92) + "Public" + chr(92) + "x", "ssh git@github.com"]
        for m in ok:
            self.assertEqual(gizlilik_denetimi.tara_metin("docs/x.md", m), [], m)

    def test_sifir_genislik_yalniz_dil_dosyasinda_serbest(self):
        zw = "a" + chr(0x200D) + "b"
        self.assertTrue(gizlilik_denetimi.tara_metin("docs/x.md", zw))
        self.assertEqual(gizlilik_denetimi.tara_metin("README.hi.md", zw), [])
        self.assertTrue(gizlilik_denetimi.tara_metin("README.hi.md", "a" + chr(0x202E) + "b"))   # bidi her yerde yasak

    def test_temiz_repo(self):
        s = gizlilik_denetimi.tara(str(REPO))
        self.assertIsNotNone(s)
        self.assertEqual(s[0], [], s[0][:5])


class YamaBekcisi(unittest.TestCase):
    def kur(self, icerik, ga="*.patch -text\n"):
        k = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, k, True)
        (k / "patches").mkdir()
        (k / "patches" / "0001-a.patch").write_bytes(icerik)
        (k / ".gitattributes").write_text(ga, encoding="utf-8")
        (k / "tablo.json").write_text(json.dumps({"0001-a.patch": yama_bekcisi.sha(str(k / "patches" / "0001-a.patch"))}), encoding="utf-8")
        return k

    def test_temiz(self):
        k = self.kur(b"a\nb\n")
        self.assertEqual(yama_bekcisi.denetle(str(k), str(k / "tablo.json")), [])

    def test_crlf_kirmizi(self):
        k = self.kur(b"a\r\nb\r\n")
        self.assertTrue(any("CRLF" in s for s in yama_bekcisi.denetle(str(k), str(k / "tablo.json"))))

    def test_degisen_hash_kirmizi(self):
        k = self.kur(b"a\n")
        (k / "patches" / "0001-a.patch").write_bytes(b"degisti\n")
        self.assertTrue(any("sha256" in s for s in yama_bekcisi.denetle(str(k), str(k / "tablo.json"))))

    def test_gitattributes_eksik_kirmizi(self):
        k = self.kur(b"a\n", ga="* text=auto\n")
        self.assertTrue(any(".gitattributes" in s for s in yama_bekcisi.denetle(str(k), str(k / "tablo.json"))))

    def test_gercek_yamalar(self):
        self.assertEqual(yama_bekcisi.denetle(), [])


class DilEslik(unittest.TestCase):
    def test_gercek_repo_kirmizisiz(self):
        kirmizi, uyari, n = dil_eslik_denetimi.denetle()
        self.assertEqual(kirmizi, [])
        self.assertGreaterEqual(n, 29)

    def test_eksik_ceviri_ve_bozuk_baglanti_kirmizi(self):
        k = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, k, True)
        (k / "scripts").mkdir()
        (k / "README.md").write_text("# A\n[x](https://example.com/a)\n```\nc\n```\n", encoding="utf-8")
        (k / "README.tr.md").write_text("# A\n[x](https://example.com/b)\n```\nc\n```\n", encoding="utf-8")
        (k / "scripts" / "dil_profili.json").write_text(json.dumps(
            {"kaynak": "README.md", "ceviri_deseni": "README.{dil}.md", "kademe": {"A": ["tr", "de"]}}), encoding="utf-8")
        kirmizi, _, _ = dil_eslik_denetimi.denetle(str(k))
        self.assertTrue(any("baglanti" in s for s in kirmizi))
        self.assertTrue(any("de:" in s and "yok" in s for s in kirmizi))


class PrKapi(unittest.TestCase):
    def test_kombinasyon_betigi_gecer(self):
        c = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(REPO / "scripts" / "pr_kombinasyon.py")], capture_output=True)
        self.assertEqual(c.returncode, 0, c.stdout.decode("utf-8", "replace")[-400:])

    def test_bos_diff_gecer(self):
        self.assertEqual(pr_kapi.degerlendir(pr_kapi.diff_coz("")), [])


class Denetim(unittest.TestCase):
    def test_hizli_yesil(self):
        c = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(REPO / "scripts" / "denetim.py"), "--hizli"], capture_output=True, cwd=str(REPO))
        cikti = c.stdout.decode("utf-8", "replace")
        self.assertEqual(c.returncode, 0, cikti[-600:])
        self.assertEqual(cikti.strip().split("\n")[-1][:13], "SONUC: GECTI ")

    def test_arguman_yoksa_3(self):
        c = subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(REPO / "scripts" / "denetim.py")], capture_output=True, cwd=str(REPO))
        self.assertEqual(c.returncode, 3)


if __name__ == "__main__":
    unittest.main()

"""Okuma sonucu: inen dosyanın adı (GPU ve ağ gerekmez; davranış testi node ister, yoksa atlanır).
Reading result: the downloaded file name (no GPU, no network; the behaviour test needs node, skipped otherwise).

python -m unittest discover -s tests -v
"""
import json
import shutil
import subprocess
import unittest

from ses_tasarim import arayuz

JS = arayuz.HTML.split("<script>")[-1].split("</script>")[0]


def kes(bas, son):
    i = JS.index(bas)
    return JS[i:JS.index(son, i)]


def node(kod):
    r = subprocess.run(["node", "-"], input=kod, capture_output=True, text=True, encoding="utf-8", timeout=30,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout)


class IndirmeAdi(unittest.TestCase):
    def test_baglanti_okuma_wav_degil(self):
        self.assertNotIn("'okuma.wav')", JS)  # indirilen ad sabit değil / not a fixed name
        self.assertIn("indirmeAdi(", kes("function okumaCiz(", "// ── Açılır menü"))

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_ad_guvenli(self):
        parca = kes("const indirmeAdi=", "function okumaCiz(")
        R = node(parca + r"""
const T='2026-11-02 01:52';
console.log(JSON.stringify([
 indirmeAdi('Zeynep Belgesel Anlatıcı',T),
 indirmeAdi('Şule: "Gece" / Ölçü*?<>|',T),
 indirmeAdi('  ..gizli.  ',T),
 indirmeAdi('',T),
 indirmeAdi('\u2068صوت الراوي\u2069',T),
 indirmeAdi('Ad',undefined),
 indirmeAdi('x'.repeat(200),T).length,
 indirmeAdi('a\\b\tc',T)]));""")
        self.assertEqual(R[0], "Zeynep_Belgesel_Anlatıcı_2026-11-02_0152.wav")
        self.assertEqual(R[1], "Şule_Gece_Ölçü_2026-11-02_0152.wav")
        self.assertEqual(R[2], "gizli_2026-11-02_0152.wav")
        self.assertEqual(R[3], "okuma_2026-11-02_0152.wav")
        self.assertEqual(R[4], "صوت_الراوي_2026-11-02_0152.wav")
        self.assertEqual(R[5], "Ad.wav")
        self.assertEqual(R[6], 60 + len("_2026-11-02_0152.wav"))
        self.assertEqual(R[7], "a_b_c_2026-11-02_0152.wav")
        for ad in R[:6] + R[7:]:
            self.assertNotRegex(ad, r'[\\/:*?"<>|\x00-\x1f]')


if __name__ == "__main__":
    unittest.main()

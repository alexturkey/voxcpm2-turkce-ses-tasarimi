"""Ses menüsü bekçisi ve sıralama testi (GPU ve ağ gerekmez; davranış testi node ister, yoksa atlanır).
Voice menu guard and ordering test (no GPU, no network; the behaviour test needs node, skipped otherwise).

Sayfanın JS'inden saf parçalar (dil listesi, ses yardımcıları, üretim gruplama, SesMenu) çıkarılır, node'da çalıştırılır.

python -m unittest discover -s tests -v
"""
import json
import shutil
import subprocess
import unittest

from ses_tasarim import arayuz

HTML = arayuz.HTML
JS = HTML.split("<script>")[-1].split("</script>")[0]


def kes(bas, son):
    i = JS.index(bas)
    return JS[i:JS.index(son, i)]


PARCA = "\n".join([
    kes("const DILLER=", "const ESDEGER"),
    kes("const sesDili=", "const listeDugmesi="),  # ses yardımcıları (dil, bayrak, ad, sıralama) / voice helpers
    kes("function uretimler(", "function cesitCiz("),
    kes("const SesMenu={", "SesMenu.kur();"),
])

SAHTE = r"""
const t=(k,v)=>k+(v?JSON.stringify(v):''),esc=s=>String(s),hafiza=()=>null;
let okumaListesi=[],dil='tr';
const h=(ad,d,gor)=>({kimlik:'hazir/'+ad,ad,gorunen_ad:gor,...(d?{dil:d}:{})});
const c=(ad,n,u,tarih)=>({kimlik:ad+'/'+n,ad,gorunen_ad:ad,cesit:n,dil:'tr',uretim:u,tarih});
const sesler={hazir:[h('anlatici_fr','fr','Anlatici FR'),h('anlatici_en','en','Anlatici EN'),h('yasli_bilge',null,'Yasli Bilge'),h('belgesel_hanim',null,'Belgesel Hanim')],
 tasarlanan:[c('deniz',2,'u1','2026-10-30 10:00'),c('deniz',1,'u1','2026-10-30 10:00'),c('yeni',1,'u2','2026-10-31 09:00')]};
"""

DENEME = r"""
const ad=g=>({liste:g.liste.map(k=>k.kimlik),hazir:g.hazir.map(k=>k.kimlik),tasarlanan:g.tasarlanan.map(k=>k.kimlik)});
const R={};
R.tr=ad(SesMenu.bolumler(sesler,['deniz/2','hazir/anlatici_fr','yok/1'],'tr'));
R.fr=ad(SesMenu.bolumler(sesler,[],'fr'));
R.bayrak=[sesDili(sesler.hazir[2]),bayrakImg('en'),bayrakImg('zz')];
R.adlar=[sesAdi(sesler.hazir[0]),sesAdi(sesler.tasarlanan[0])];
console.log(JSON.stringify(R));
"""


class SesMenusu(unittest.TestCase):
    def test_select_is_gone_and_menu_reuses_popup(self):
        self.assertNotIn('<select id="ses"', HTML)
        self.assertIn('id="ses" class="sesdugme" aria-haspopup="menu"', HTML)
        menu = kes("const SesMenu={", "SesMenu.kur();")
        self.assertIn("Acilir.ac(", menu)
        self.assertIn("Acilir.baslik(", menu)
        self.assertNotIn("$('ses').value", JS)  # tek kapı: SesMenu.sec / okumayaGonder
        self.assertIn("/bayrak/", kes("const bayrakImg=", "\n"))

    def test_choices_are_remembered(self):
        self.assertIn("hafiza('ses',", JS)
        self.assertIn("hafiza('hazir_dil'", JS)

    def test_popup_owners_unchanged_for_line_menu_tests(self):
        # test_arayuz_satir.py bu aralığı keser; ses menüsü dışında kalmalı / the line-menu test cuts this range
        i = JS.index("// ── Açılır menü")
        self.assertNotIn("SesMenu", JS[i:JS.index("Acilir.kur();Durak.kur();Satir.kur();")])

    @unittest.skipUnless(shutil.which("node"), "node yok / node not installed")
    def test_sections_order(self):
        out = subprocess.run(["node", "-e", SAHTE + PARCA + DENEME], capture_output=True, text=True, encoding="utf-8",
                             timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        self.assertEqual(out.returncode, 0, out.stderr)
        R = json.loads(out.stdout.strip().splitlines()[-1])
        # Okuma listesi üstte, eklenme sırasıyla; silinmiş ses (yok/1) çizilmez; listedeki ses aşağıda tekrar etmez.
        self.assertEqual(R["tr"], {"liste": ["deniz/2", "hazir/anlatici_fr"],
                                   "hazir": ["hazir/belgesel_hanim", "hazir/yasli_bilge", "hazir/anlatici_en"],
                                   "tasarlanan": ["yeni/1", "deniz/1"]})
        # Arayüz dili önce, sonra dil listesi sırası (tr, en, ...); dil alanı olmayan eski kart Türkçe sayılır.
        self.assertEqual(R["fr"]["hazir"], ["hazir/anlatici_fr", "hazir/belgesel_hanim", "hazir/yasli_bilge",
                                            "hazir/anlatici_en"])
        self.assertEqual(R["fr"]["tasarlanan"], ["yeni/1", "deniz/1", "deniz/2"])
        self.assertEqual(R["bayrak"], ["tr", '<img src="/bayrak/gb.svg" alt="">', ""])
        self.assertEqual(R["adlar"][0], "Anlatici FR")
        self.assertTrue(R["adlar"][1].startswith("deniz · cesit_n"), R["adlar"][1])


if __name__ == "__main__":
    unittest.main()

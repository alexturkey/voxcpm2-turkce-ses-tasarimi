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
    kes("const SesYonet={", "// Defter:"),
])

SAHTE = r"""
const t=(k,v)=>k+(v?JSON.stringify(v):''),esc=s=>String(s),hafiza=()=>null,KALP='<svg></svg>';
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
// Aynı adla iki ayrı üretim: ekte üretim zamanı; tek üretimli ad kısa kalır
sesler.tasarlanan.push(c('ay',1,'p1','2026-10-29 08:00'),c('ay',2,'p2','2026-10-29 09:30'));
R.iki=[sesAdi(sesler.tasarlanan[3]),sesAdi(sesler.tasarlanan[4]),sesAdi(sesler.tasarlanan[0])];
// Klasör adı olarak kalmış ad yalnız görünümde güzelleşir; bilerek yazılmış ad ve takma ad aynen kalır
R.guzel=[adGoster({kimlik:'cocuk_anlatici/1',ad:'cocuk_anlatici',gorunen_ad:'cocuk_anlatici',dil:'tr'}),
 adGoster({kimlik:'ilginc/1',ad:'ilginç_ses',gorunen_ad:'ilginç_ses',dil:'tr'}),
 adGoster({kimlik:'b/1',ad:'benim_sesim',gorunen_ad:'Benim Sesim',dil:'tr'}),
 adGoster({kimlik:'c/1',ad:'x_y',gorunen_ad:'x_y',asil_ad:'X y',dil:'tr'})];
// Yönetim menüsü (aynı Acilir): hazırda Gizle, tasarlananda Sil; takma ad varsa "asıl ada dön"; ses menüsünden gelince Geri
const Acilir={ac(tetik,x,html,sahip){Acilir.html=html;Acilir.sahip=sahip;},baslik:(b,a)=>'<b>'+a+'</b>',kapat(){Acilir.html='';}};
const $=()=>({getBoundingClientRect:()=>({left:0,right:0})}),rtl=()=>false,tetik=$();
const ogeler=()=>[...Acilir.html.matchAll(/data-is="([a-z]+)"([^>]*)>(.*?)<\/button>/g)]
 .map(m=>m[1]+':'+m[3].replace(/<[^>]*>/g,'')+(/aria-checked="true"/.test(m[2])?' ✓':''));
sesler.hazir[3].asil_ad='Belgesel Hanim';sesler.hazir[3].gorunen_ad='Zeynep';okumaListesi=['deniz/1'];
SesYonet.menu('hazir/belgesel_hanim',tetik,true);R.yh=[ogeler(),Acilir.sahip===SesYonet,/class="disli oge"/.test(Acilir.html)];
SesYonet.menu('deniz/1',tetik,false);R.yt=ogeler();
SesYonet.menu('yok/9',tetik,false);R.yyok=Acilir.html;
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
        self.assertTrue(R["adlar"][1].startswith("Deniz · cesit_n"), R["adlar"][1])
        # Aynı adla iki kez Tasarla: iki üretim satırda zamanla ayrılır (kullanıcı 19:00) / same name, two productions
        self.assertTrue(R["iki"][0].startswith("Ay · 10-29 08:00 · cesit_n"), R["iki"][0])
        self.assertTrue(R["iki"][1].startswith("Ay · 10-29 09:30 · cesit_n"), R["iki"][1])
        self.assertTrue(R["iki"][2].startswith("Deniz · cesit_n"), R["iki"][2])
        self.assertEqual(R["guzel"], ["Cocuk anlatici", "İlginç ses", "Benim Sesim", "x_y"])  # beyin 19:27
        # Yönetim menüsü (kullanıcı 19:14): hazır ses gizlenir (silinmez), tasarlanan çöpe silinir; yeniden adlandır
        # yerinde kutu; takma ad varsa asıl ada dön; listede olan ses "çıkar" der; olmayan ses menü açmaz.
        # Liste öğesi kart düğmesiyle aynı dil: ad tekrarlanmaz (beyin 19:27) / no repeated name in the list item
        hazir, sahip, kutu = R["yh"]
        self.assertEqual(hazir, ["geri:‹ geri", "oku:oku", "liste:liste_ekle",
                                 'asil:asil_ada_don{"ad":"Belgesel Hanim"}', "sil:gizle"])
        self.assertTrue(sahip and kutu)
        self.assertEqual([x.split(":")[0] for x in R["yt"]], ["oku", "liste", "sil"])
        self.assertEqual(R["yt"][1:], ["liste:listede ✓", "sil:sil_ses"])
        self.assertEqual(R["yyok"], "")


if __name__ == "__main__":
    unittest.main()

"""Kısa bilgi satırı: geçici yazı geçici yazıyı geri getirmez, durum satırı sabit yer kaplar (GPU ve ağ gerekmez; davranış testi node ister).
Short notice line: a notice never brings back another notice, the status line keeps a fixed height (no GPU, no network; needs node).

Eskiden çeşit kartında ad + "Okuma listeme ekle" iki bilgi yazıyordu; ikincisi birincisini "önceki durum" sandığı için
3 sn sonra "Ad değişti" geri gelip kalıyordu, boş satır da gizlendiği için kartlar 26 px aşağı kayıyordu.
The card flow used to show two notices; the second kept the first as its "previous state", so "Name changed" came back and stayed.

python -m unittest discover -s tests -v
"""
import json
import re
import shutil
import subprocess
import unittest

from ses_tasarim import arayuz

JS = arayuz.HTML.split("<script>")[-1].split("</script>")[0]
CSS = arayuz.HTML.split("<style>")[1].split("</style>")[0]


def kes(bas, son):
    i = JS.index(bas)
    return JS[i:JS.index(son, i)]


# Sahte saat ve öğe / fake clock and element
SAHTE = r"""
let simdi=0,sira=[],no=0;
function setTimeout(f,ms){const id=++no;sira.push({id,f,t:simdi+ms});return id;}
function clearTimeout(id){sira=sira.filter(x=>x.id!==id);}
function ilerle(ms){simdi+=ms;for(;;){const h=sira.filter(x=>x.t<=simdi).sort((a,b)=>a.t-b.t)[0];if(!h)break;sira=sira.filter(x=>x!==h);h.f();}}
const S={d_ad_degisti:'Ad degisti',d_liste_eklendi:'Listeye eklendi',d_liste_cikti:'Listeden cikti'},YEDEK={};
const t=k=>S[k]||k,sorunMetni=s=>s.kod;
const oge=()=>({textContent:'',title:'',className:''});
"""


def node(kod):
    r = subprocess.run(["node", "-"], input=kod, capture_output=True, text=True, encoding="utf-8", timeout=30,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout)


class BilgiSatiri(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_gecici_yazi_ust_uste(self):
        kod = SAHTE + kes("function durumYaz(", "\nlet ornekler") + kes("function bilgi(", "\n// Tek liste") + r"""
const o={};let e;
// 1) kart akışı eski hali: iki bilgi art arda -> 3 sn sonra boş, eski yazı dönmez
e=oge();bilgi(e,{durum:'bitti',kod:'ad_degisti'});bilgi(e,{durum:'bitti',kod:'liste_eklendi'});
o.hemen=e.textContent;ilerle(3000);o.sn3=e.textContent;ilerle(5000);o.sn8=e.textContent;
// 2) kalıcı durum varken iki bilgi -> kalıcı durum geri gelir
e=oge();durumYaz(e,{durum:'bitti',mesaj:'Tasarim bitti'});bilgi(e,{durum:'bitti',kod:'ad_degisti'});ilerle(1000);
bilgi(e,{durum:'bitti',kod:'liste_eklendi'});ilerle(2500);o.ara=e.textContent;ilerle(1000);o.kalici=e.textContent;
// 3) bilgi sürerken kalıcı yazı gelirse zamanlayıcı onu silmez
e=oge();bilgi(e,{durum:'bitti',kod:'liste_eklendi'});durumYaz(e,{durum:'hata',hata:'Sunucu yok'});ilerle(4000);
o.hata=e.textContent;o.hata_sinif=e.className;
// 4) üçüncü kart: bir önceki akıştan sonra yeni bilgi eski yazıyı geri getirmez
e=oge();bilgi(e,{durum:'bitti',kod:'ad_degisti'});bilgi(e,{durum:'bitti',kod:'liste_eklendi'});ilerle(4000);
bilgi(e,{durum:'bitti',kod:'liste_eklendi'});ilerle(4000);o.ucuncu=e.textContent;o.zamanlayici=sira.length;
console.log(JSON.stringify(o));"""
        r = node(kod)
        self.assertEqual(r["hemen"], "Listeye eklendi")
        self.assertEqual((r["sn3"], r["sn8"]), ("", ""))
        self.assertEqual((r["ara"], r["kalici"]), ("Listeye eklendi", "Tasarim bitti"))
        self.assertEqual((r["hata"], r["hata_sinif"]), ("Sunucu yok", "durum hata"))
        self.assertEqual((r["ucuncu"], r["zamanlayici"]), ("", 0))

    def test_kart_akisi_tek_mesaj(self):
        # Ses listede değilse ad kaydı sessiz, tek mesajı liste ekleme yazar / the name save is silent, the list add writes the one message
        kaydet = kes("async kaydet(x,fare)", "async function yenile(")
        self.assertIn("SesYonet.yonet(k,'ad',v,undefined,$('d_tasarla'),!okumaListesi.includes(k))", kaydet)
        yonet = kes("async yonet(kimlik,islem,ad,cop,yer,sessiz)", "odak(){")
        self.assertIn("if(!sessiz)bilgi(el,", yonet)

    def test_durum_satiri_sabit(self):
        # Boş satır gizlenmez (gizlenince kartlar kayıyordu); tek satır, sabit yükseklik; hata satırı açılabilir
        self.assertFalse(re.search(r"\.ubas \.durum:empty\{display:none", CSS), "bos durum satiri gizleniyor")
        kural = re.search(r"\.ubas \.durum\{([^}]*)\}", CSS).group(1)
        for p in ("height:1.35em", "white-space:nowrap", "overflow:hidden", "text-overflow:ellipsis"):
            self.assertIn(p, kural)
        self.assertRegex(CSS, r"\.ubas \.durum\.hata\{height:auto")


if __name__ == "__main__":
    unittest.main()

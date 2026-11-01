"""Çeşit kartındaki ad kutusu testi (GPU ve ağ gerekmez; node ister, yoksa atlanır).
Design-card name box test (no GPU, no network; needs node, skipped otherwise).

"Okuma listeme ekle" kartta ad kutusu açar: ✓ önce adı (değiştiyse) sonra listeyi yazar; Vazgeç hiçbir şey yazmaz;
sınırı aşan ad hiçbir şey yazmaz; ses kutu açıkken başka yerden listeye girdiyse ✓ onu listeden çıkarmaz.

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


PARCA = "\n".join([
    kes("// Ad kutusundaki değer", "const listeDugmesi="),
    kes("const KartAd={", "function cesitCiz("),
])

SAHTE = r"""
const t=k=>k,esc=s=>String(s),adGoster=s=>s.ad;
let okumaListesi=[],cagri=[],yonetSonuc=true,veri={};
const SesMenu={bul:k=>({kimlik:k,ad:'Tarif'})};
const SesYonet={async yonet(k,islem,ad){cagri.push('ad:'+ad);return yonetSonuc;}};
async function listeDegistir(k){cagri.push('liste:'+k);okumaListesi.push(k);return true;}
const $=()=>({}),veriBul=()=>null;
// En küçük sahte kart: düğmeler alanı, kutu, gizlenen iki düğme / the smallest fake card
function kart(k){const sinif=new Set(),girdi={value:'',classList:{add:x=>sinif.add(x),remove:x=>sinif.delete(x)},sinif,focus(){},select(){}};
 const dugme=[{hidden:false,dataset:{oku:k}},{hidden:false,dataset:{liste:k},focus(){}}];let kutu=false;
 const sinifD=new Set();const d={dugme,girdi,offsetHeight:48,style:{},classList:{add:x=>sinifD.add(x),remove:x=>sinifD.delete(x)},sinifD,get kutu(){return kutu;},
  querySelector(q){if(q==='.adkutu')return kutu?{remove(){kutu=false;}}:null;if(q==='.adkutu input')return kutu?girdi:null;
   if(q==='[data-adkaydet]')return kutu?{dataset:{adkaydet:k}}:null;if(q==='[data-liste]')return dugme[1];return null;},
  querySelectorAll(){return dugme;},
  insertAdjacentHTML(){kutu=true;girdi.value='Tarif';}};
 dugme[1].closest=()=>d;girdi.closest=()=>d;return d;}
"""

DENEME = r"""
(async()=>{const R={};
 // ✓, ad değişti: önce ad, sonra liste
 let d=kart('a/1');KartAd.ac(d.dugme[1]);R.acik=[d.kutu,d.dugme[0].hidden,d.dugme[1].hidden,d.style.height];
 d.girdi.value='Mavi Ses';await KartAd.kaydet(d.girdi);R.degisti=cagri;
 // ✓, ad aynı: yalnız liste
 cagri=[];d=kart('a/2');KartAd.ac(d.dugme[1]);await KartAd.kaydet(d.girdi);R.ayni=cagri;
 // Vazgeç: hiçbir şey yazılmaz, düğmeler geri gelir
 cagri=[];d=kart('a/3');KartAd.ac(d.dugme[1]);KartAd.kapat(d.girdi,true);R.vazgec=[cagri,d.kutu,d.dugme[0].hidden,d.dugme[1].hidden,d.style.height];
 // Sınırı aşan ad: hiçbir şey yazılmaz, kutu açık kalır ve kırmızı olur
 cagri=[];d=kart('a/4');KartAd.ac(d.dugme[1]);d.girdi.value='x'.repeat(AD_EN_UZUN+1);await KartAd.kaydet(d.girdi);
 R.uzun=[cagri,d.kutu,d.girdi.sinif.has('yanlis')];
 // Ad kaydı hata verirse listeye eklenmez
 cagri=[];yonetSonuc=false;d=kart('a/5');KartAd.ac(d.dugme[1]);d.girdi.value='Yeni';await KartAd.kaydet(d.girdi);R.hata=cagri;yonetSonuc=true;
 // Kutu açıkken ses başka yerden listeye girdi: ✓ onu çıkarmaz (listeDegistir çağrılmaz)
 cagri=[];d=kart('a/6');KartAd.ac(d.dugme[1]);okumaListesi.push('a/6');await KartAd.kaydet(d.girdi);R.zaten=cagri;
 console.log(JSON.stringify(R));})();
"""


@unittest.skipUnless(shutil.which("node"), "node yok / node missing")
class KartAdKutusu(unittest.TestCase):
    def test_card_name_box(self):
        out = subprocess.run(["node", "-e", SAHTE + PARCA + DENEME], capture_output=True, text=True, encoding="utf-8",
                             timeout=60, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        self.assertEqual(out.returncode, 0, out.stderr)
        R = json.loads(out.stdout.strip().splitlines()[-1])
        self.assertEqual(R["acik"], [True, True, True, "48px"])  # kart yerinden oynamaz / the card keeps its height
        self.assertEqual(R["degisti"], ["ad:Mavi Ses", "liste:a/1"])
        self.assertEqual(R["ayni"], ["liste:a/2"])
        self.assertEqual(R["vazgec"], [[], False, False, False, ""])
        self.assertEqual(R["uzun"], [[], True, True])
        self.assertEqual(R["hata"], ["ad:Yeni"])
        self.assertEqual(R["zaten"], [])


if __name__ == "__main__":
    unittest.main()

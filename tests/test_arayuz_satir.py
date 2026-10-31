"""Satır menüsü bekçisi ve davranış testleri (GPU ve ağ gerekmez; davranış testleri node ister, yoksa atlanır).
Line menu guard and behaviour tests (no GPU, no network; behaviour tests need node, skipped otherwise).

Davranış testleri sayfanın JS'inden saf modülleri (Acilir, Durak, Satir) çıkarır, küçük bir sahte DOM ile node'da çalıştırır.

python -m unittest discover -s tests -v
"""
import json
import re
import shutil
import subprocess
import unittest

from ses_tasarim import arayuz

HTML = arayuz.HTML
JS = HTML.split("<script>")[-1].split("</script>")[0]
MODUL = JS[JS.index("// ── Açılır menü"):JS.index("Acilir.kur();Durak.kur();Satir.kur();")]

SAHTE = r"""
const ta={value:'',selectionStart:0,selectionEnd:0,focus(){},setSelectionRange(a,b){this.selectionStart=a;this.selectionEnd=b;}};
const kap={setAttribute(){},removeAttribute(){},querySelectorAll(){return [];},querySelector(){return null;}};
const $=id=>id==='okuma_metni'?ta:kap;
const document={documentElement:{dir:'ltr',lang:'tr'}};
const t=(k,v)=>k+(v?JSON.stringify(v):'');
const hafiza=()=>null,esc=s=>String(s),defterNo=()=>{},satirBoyu=()=>28,bantKaydir=()=>{};
"""

DENEME = r"""
const R={},A=['A','B','C','D'],DA=[null,1,null,0.5];
const h=o=>{const r=Satir.hesapla(A,DA,o);return [r.s,r.d];};
R.k1=h({tur:'tasi',a:1,hedef:3});R.k2=h({tur:'tasi',a:3,hedef:0});R.k3=h({tur:'cogalt',a:1});R.k4=h({tur:'sil',a:1});
R.k5u=h({tur:'ekle',a:1,yon:'ust'});R.k5a=h({tur:'ekle',a:1,yon:'alt'});R.k6=h({tur:'tasi',a:0,b:1,hedef:1});
R.k4bos=(r=>[r.s,r.d])(Satir.hesapla([''],[null],{tur:'sil',a:0}));
R.k7=(r=>[r.s,r.d])(Durak.bosEmekli(['A','','','B','C || 1,5',''],[null,null,null,null,null,null]));
R.k7b=(r=>[r.s,r.d])(Durak.bosEmekli(['A','','B'],[0.5,null,null]));
R.k8=(r=>[r.s,r.d,r.imlec])(Satir.yapistir(A,DA,1,1,'X\n\nY'));
ta.value='A\n\nB\nC';Durak.dur=[null,null,1,0.5];R.metin=Durak.metin();
// Alt+ok seçim aralığı: tam satır seçimi blokla birlikte kalır, ikinci basışta blok bölünmez
const sec=(s,a,b)=>{ta.value=s.join('\n');ta.selectionStart=Math.min(a,ta.value.length);ta.selectionEnd=Math.min(b,ta.value.length);return Satir.secim();};
const bas=(c,yon)=>{const r=Satir.hesapla(c.s,c.s.map(()=>null),{tur:'tasi',a:c.a,b:c.b,hedef:c.a+yon}),k=Satir.secimKaydir(c,c.a,c.b,r.kay);
 return {s:r.s,c:sec(r.s,Satir.ofs(r.s,...k.bas),Satir.ofs(r.s,...k.son))};};
let c=sec(A,2,6);R.asagi1=bas(c,1);R.asagi1={s:R.asagi1.s,a:R.asagi1.c.a,b:R.asagi1.c.b};
c=sec(A,2,6);R.yukari1=bas(c,-1);R.yukari1={s:R.yukari1.s,a:R.yukari1.c.a,b:R.yukari1.c.b};
c=sec(A,0,6);let x=bas(c,1);x=bas(x.c,-1);R.gidisDonus={s:x.s,a:x.c.a,b:x.c.b};
// Bant geçmişi: taşı, 110 harf yaz, geri al → bantlar doğru (düz yazma haritayı doldurmaz)
Durak.gecmis.clear();ta.value=A.join('\n');Durak.eski=A.slice();Durak.dur=DA.slice();Durak.tur=null;Durak.anlik();
const T1='A\nC\nD\nB';ta.value=T1;Durak.dur=[null,null,0.5,1];Durak.eski=T1.split('\n');Durak.anlik();
let y=T1;for(let i=0;i<110;i++){y='x'+y;ta.value=y;Durak.tur='insertText';Durak.hizala(ta);}
ta.value=T1;Durak.tur='historyUndo';Durak.hizala(ta);R.geri1=Durak.dur.slice();
ta.value=A.join('\n');Durak.hizala(ta);R.geri2=Durak.dur.slice();Durak.tur=null;R.harita=Durak.gecmis.size;
// Sıraya taşı kutusu: ilk rakamla açılınca imleç sona (ikinci rakam arkaya eklenir)
const g={value:'4',focus(){},select(){this.sel='hepsi';},setSelectionRange(a,b){this.sel=[a,b];}};
Acilir.sayiAc({querySelectorAll:()=>[],querySelector:()=>g},'1');R.sayi={value:g.value,sel:g.sel};
// Elle '|| 0.7': rakam yazılırken '|| 0' banda taşınmaz; bekleyen işaret metin()'de olduğu gibi gider
ta.value='A || 0\nB';ta.selectionStart=ta.selectionEnd=6;Durak.eski=['A','B'];Durak.dur=[null,null];Durak.tur='insertText';
R.bekle=Durak.isaretTasi(ta);Durak.tur=null;ta.value='A || 0.7\n\nB';Durak.dur=[null,null,null];R.ham=Durak.metin();
// Görünen = giden: bant 1 sn iken satır sonunda '|| 0.7' bekliyorsa bant 0,7 gösterir, metin() 0.7 gönderir;
// imleç başka satıra geçince işaret banda taşınır. Geçersiz işaret (9, '0.', bilinmeyen ad) banda çevrilmez, hata listesine girer.
ta.value='A || 0.7\nB';ta.selectionStart=ta.selectionEnd=8;Durak.eski=['A','B'];Durak.dur=[1,null];Durak.tur='insertText';
R.bekA=[Durak.isaretTasi(ta),Durak.bekleyen];Durak.tur=null;
R.gorunen=[/"0,7"/.test(Durak.ciz(ta.value.split('\n'),[28,28],9).bant),Durak.metin()];
ta.selectionStart=ta.selectionEnd=10;Durak.bekleyenTasi(false);R.tasindi=[ta.value,Durak.dur.slice(),Durak.bekleyen];
ta.value='A || 9\nB || 0.\nC || hizli\nD';Durak.dur=[null,null,null,null];Durak.bekleyen=null;
R.hata=Durak.hatalar().map(h=>[h.i,h.veri.durak]);R.yanlis=(Durak.ciz(ta.value.split('\n'),[28,28,28,28],9).bant.match(/yanlis/g)||[]).length;
console.log(JSON.stringify(R));
"""


class ArayuzSatir(unittest.TestCase):
    def test_tek_menu_kabi(self):
        self.assertNotIn("durakmenu", HTML)
        self.assertEqual(HTML.count('id="acilir"'), 1)
        # Ortak parçalar bir kez tanımlı: ikinci menü için kopya CSS yok
        self.assertEqual(HTML.count("#acilir .onay{"), 1)
        self.assertEqual(HTML.count("#acilir .ozel{"), 1)
        self.assertEqual(HTML.count("#acilir .baslik{"), 1)

    def test_tek_yazma_kapisi(self):
        # okuma_metni'ne doğrudan value ataması yalnız: açılış ve uygula yedek yolu (elle '||' de kapıdan geçer)
        kutu = JS[JS.index("// ── Açılır menü"):JS.index("function dosyaAdi")]
        self.assertLessEqual(len(re.findall(r"\bta\.value=(?!=)", kutu)), 2)
        self.assertNotIn("o.value=o.value", JS)  # okumaya taşı da kapıdan geçer
        self.assertIn("execCommand('insertText'", JS)

    def test_bos_satir_anlami_kalkti(self):
        self.assertNotIn("bosSonra", JS)

    def test_klavye_ime_erisilebilirlik(self):
        self.assertIn("isComposing", JS)
        self.assertIn('tabindex="-1"', JS)
        self.assertIn("aria-expanded", JS)
        self.assertIn("role=\"menuitemradio\"", JS)
        self.assertIn("prefers-reduced-motion", HTML)
        self.assertEqual(MODUL.count("'Escape'"), 1)  # tek Esc dinleyicisi (Acilir)

    def test_birim_dilden(self):
        # Süre birimi kodda sabit ' s' değil, dilin sn anahtarı
        kutu = JS[JS.index("// ── Açılır menü"):JS.index("function dosyaAdi")]
        self.assertNotIn("+' s'", kutu)
        self.assertNotIn("} s`", kutu)
        self.assertIn("-u-nu-latn", kutu)

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_davranis(self):
        cikti = subprocess.run(["node", "-"], input=SAHTE + MODUL + DENEME, capture_output=True, text=True, encoding="utf-8",
                               timeout=30, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        self.assertEqual(cikti.returncode, 0, cikti.stderr)
        R = json.loads(cikti.stdout)
        A, DA = ["A", "B", "C", "D"], [None, 1, None, 0.5]
        beklenen = {
            "k1": [["A", "C", "D", "B"], [None, None, 0.5, 1]], "k2": [["D", "A", "B", "C"], [0.5, None, 1, None]],
            "k3": [["A", "B", "B", "C", "D"], [None, 1, 1, None, 0.5]], "k4": [["A", "C", "D"], [None, None, 0.5]],
            "k5u": [["A", "", "B", "C", "D"], [None, None, 1, None, 0.5]], "k5a": [["A", "B", "", "C", "D"], [None, 1, None, None, 0.5]],
            "k6": [["C", "A", "B", "D"], [None, None, 1, 0.5]], "k4bos": [[""], [None]],
            "k7": [["A", "B", "C"], [1, None, 1.5]], "k7b": [["A", "B"], [0.5, None]],
            "k8": [["AX", "Y", "B", "C", "D"], [1, None, 1, None, 0.5], [1, 1]],
            "metin": "A || 0.35\n\nB || 1\nC",
            "asagi1": {"s": ["A", "D", "B", "C"], "a": 2, "b": 3},
            "yukari1": {"s": ["B", "C", "A", "D"], "a": 0, "b": 1},
            "gidisDonus": {"s": A, "a": 0, "b": 2},
            "geri1": [None, None, 0.5, 1], "geri2": DA,
            "sayi": {"value": "1", "sel": [1, 1]},
            "bekle": False, "ham": "A || 0.7\n\nB",
            "bekA": [False, 0], "gorunen": [True, "A || 0.7\nB"], "tasindi": ["A\nB", [0.7, None], None],
            "hata": [[0, "9"], [1, "0."], [2, "hizli"]], "yanlis": 3,
        }
        for k, v in beklenen.items():
            self.assertEqual(R[k], v, k)
        self.assertLessEqual(R["harita"], 3)  # 110 harf haritayı doldurmadı


if __name__ == "__main__":
    unittest.main()

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


class MetinHafizasi(unittest.TestCase):
    def test_tek_kapi(self):
        # Kayıt defterNo'dan seyreltilerek tetiklenir, açılış bitmeden yazmaz, sayfadan çıkarken yazar
        self.assertIn("Kayit.sonra();", kes("function defterNo(", "// Kutu boyu"))
        self.assertIn("Durak.acilis();Kayit.hazir=true;", JS)
        self.assertIn("addEventListener('pagehide',()=>Kayit.yaz())", JS)
        self.assertIn("try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e)", JS)

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_geri_gelir(self):
        sahte = r"""
const ta={value:'',clientWidth:0};const $=id=>ta;let D={},yazim=0;
const hafiza=(k,v)=>{if(v===undefined)return k in D?D[k]:null;D[k]=String(v);yazim++;};
const defterNo=()=>{},snb=x=>x+' s',t=k=>k,Satir={isik:()=>({k:new Set()})};
"""
        parca = kes("const Durak={", "const KALP=") + kes("const Kayit={", "addEventListener('pagehide'")
        R = node(sahte + parca + r"""
const R={};
D={okuma_metni:'A\n\nB || 1,5\nC',okuma_bantlar:'[0.5,null,null,null]'};ta.value='';Durak.acilis();R.a=[ta.value,Durak.dur];
D={};ta.value='X\nY';Durak.dur=[];Durak.eski=[];Durak.acilis();R.b=[ta.value,Durak.dur];
D={okuma_metni:'K\nL',okuma_bantlar:'{'};Durak.acilis();R.c=[ta.value,Durak.dur];
D={okuma_metni:'K\nL',okuma_bantlar:'[9,"x"]'};Durak.acilis();R.d=Durak.dur;
D={};yazim=0;Kayit.hazir=false;Kayit.son=null;ta.value='M\nN';Durak.dur=[1,null];Kayit.yaz();R.e=[yazim,'okuma_metni' in D];
Kayit.hazir=true;Kayit.yaz();Kayit.yaz();R.f=[yazim,D.okuma_metni,D.okuma_bantlar];
Durak.dur=[1,null,0.7];Kayit.yaz();R.g=D.okuma_bantlar;
console.log(JSON.stringify(R));""")
        self.assertEqual(R["a"], ["A\nB\nC", [0.5, 1.5, None]])
        self.assertEqual(R["b"], ["X\nY", [None, None]])
        self.assertEqual(R["c"], ["K\nL", [None, None]])
        self.assertEqual(R["d"], [5, None])
        self.assertEqual(R["e"], [0, False])  # açılış bitmeden yazmaz / no write before load finishes
        self.assertEqual(R["f"], [2, "M\nN", "[1,null]"])  # aynı içerik ikinci kez yazılmaz / unchanged content not rewritten
        self.assertEqual(R["g"], "[1,null]")  # satır sayısı kadar bant / one band per line


class KisaYol(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_ctrl_enter(self):
        R = node(kes("const anaIs=", "const KISAYOL=") + r"""
const E=o=>({key:'Enter',ctrlKey:false,metaKey:false,altKey:false,shiftKey:false,isComposing:false,repeat:false,defaultPrevented:false,...o});
console.log(JSON.stringify([anaIs(E({ctrlKey:true}),'p1'),anaIs(E({metaKey:true}),'p2'),anaIs(E({ctrlKey:true}),'p3'),
 anaIs(E({}),'p2'),anaIs(E({altKey:true}),'p2'),anaIs(E({ctrlKey:true,altKey:true}),'p2'),anaIs(E({ctrlKey:true,shiftKey:true}),'p2'),
 anaIs(E({ctrlKey:true,isComposing:true}),'p2'),anaIs(E({ctrlKey:true,repeat:true}),'p2'),anaIs(E({ctrlKey:true,defaultPrevented:true}),'p1'),
 anaIs(E({ctrlKey:true,key:'a'}),'p1')]));""")
        self.assertEqual(R, ["btn_tasarla", "btn_oku", None, None, None, None, None, None, None, None, None])

    def test_pasif_dugme_ve_menu(self):
        k = kes("const anaIs=", "function dosyaAdi")
        self.assertIn("if(Acilir.acikMi())return;", k)
        self.assertIn("if(!b.disabled)b.click();", k)
        self.assertNotIn(".focus(", k)  # kısayol odak taşımaz / the shortcut never moves focus
        # Defterin kendi Enter'ı Ctrl/Meta'lı Enter'a karışmaz / the notebook's own Enter ignores Ctrl/Meta+Enter
        self.assertIn("if(e.key!=='Enter'||e.shiftKey||e.ctrlKey||e.metaKey", JS)


if __name__ == "__main__":
    unittest.main()

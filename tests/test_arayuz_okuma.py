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
 indirmeAdi('a\\b\tc',T),
 Array.from(indirmeAdi('a'+'\u{1F600}'.repeat(80),T)).some(c=>c.length===1&&/[\uD800-\uDFFF]/.test(c)),
 indirmeAdi('\u061C\u200BAd\uFEFF\u2060',T)]));""")
        self.assertEqual(R[0], "Zeynep_Belgesel_Anlatıcı_2026-11-02_0152.wav")
        self.assertEqual(R[1], "Şule_Gece_Ölçü_2026-11-02_0152.wav")
        self.assertEqual(R[2], "gizli_2026-11-02_0152.wav")
        self.assertEqual(R[3], "okuma_2026-11-02_0152.wav")
        self.assertEqual(R[4], "صوت_الراوي_2026-11-02_0152.wav")
        self.assertEqual(R[5], "Ad.wav")
        self.assertEqual(R[6], 60 + len("_2026-11-02_0152.wav"))
        self.assertEqual(R[7], "a_b_c_2026-11-02_0152.wav")
        self.assertFalse(R[8])  # yarım vekil çift yok / no lone surrogate after the length cut
        self.assertEqual(R[9], "Ad_2026-11-02_0152.wav")
        for ad in R[:6] + [R[7], R[9]]:
            self.assertNotRegex(ad, r'[\\/:*?"<>|\x00-\x1f]')


class MetinHafizasi(unittest.TestCase):
    def test_tek_kapi(self):
        # Kayıt defterNo'dan seyreltilerek tetiklenir, açılış bitmeden yazmaz, sayfadan çıkarken yazar
        self.assertIn("Kayit.sonra();", kes("function defterNo(", "// Kutu boyu"))
        self.assertIn("Durak.acilis();Kayit.formGeri();Kayit.hazir=true;", JS)
        self.assertIn("addEventListener('pagehide',()=>Kayit.yaz())", JS)
        self.assertIn("try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e)", JS)

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_geri_gelir(self):
        sahte = r"""
const ta={value:'',clientWidth:0};const $=id=>ta;let D={},yazim=0;
const hafiza=(k,v)=>{if(v===undefined)return k in D?D[k]:null;D[k]=String(v);yazim++;};
const defterNo=()=>{},snb=x=>x+' s',t=k=>k,Satir={isik:()=>({k:new Set()})},DinlemeDefter={deger:''};
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
        self.assertEqual(R["f"], [3, "M\nN", "[1,null]"])  # metin + bant + form; aynı içerik ikinci kez yazılmaz / unchanged content not rewritten
        self.assertEqual(R["g"], "[1,null]")  # satır sayısı kadar bant / one band per line

    def test_tasarla_formu_ayni_kapida(self):
        # Tasarla formunun her alanı yazınca aynı seyreltilmiş kayda gider; diyalog kapanınca da yazılır
        self.assertIn("if(d.classList.contains('hata'))durumYaz(d,null);Kayit.sonra();", JS)
        self.assertIn("Kayit.hazir=true;Kayit.sonra();", kes("const DinlemeDefter={", "$('dinleme_metni').addEventListener('click'"))

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_tasarla_formu_geri_gelir(self):
        sahte = r"""
const E={};const $=id=>E[id]||(E[id]={value:'',options:[]});let D={};
const hafiza=(k,v)=>{if(v===undefined)return k in D?D[k]:null;D[k]=String(v);};
const DinlemeDefter={deger:'',yaz(v){this.deger=v;}},Durak={dur:[]};
"""
        R = node(sahte + kes("const Kayit={", "addEventListener('pagehide'") + r"""
const R={};$('ornek').options=[{value:''},{value:'anlatici_tr'}];
Kayit.hazir=true;$('okuma_metni').value='';$('ad').value='Zeynep';$('cesit').value='5';$('ornek').value='anlatici_tr';
$('tarif').value='A warm voice';$('tasarim_metni').value='Merhaba.';DinlemeDefter.deger='Bir\nIki || 1';Kayit.yaz();R.kayit=JSON.parse(D.tasarla_form);
for(const k in E)E[k].value='';DinlemeDefter.deger='';Kayit.formGeri();
R.geri=[$('ad').value,$('cesit').value,$('ornek').value,$('tarif').value,$('tasarim_metni').value,DinlemeDefter.deger];
D.tasarla_form=JSON.stringify({ad:'X',ornek:'yok_boyle',cesit:7});$('ornek').value='';$('cesit').value='3';Kayit.formGeri();
R.suzgec=[$('ad').value,$('ornek').value,$('cesit').value];
D.tasarla_form='{bozuk';Kayit.formGeri();R.bozuk=$('ad').value;
console.log(JSON.stringify(R));""")
        self.assertEqual(R["kayit"]["dinleme"], "Bir\nIki || 1")
        self.assertEqual(R["geri"], ["Zeynep", "5", "anlatici_tr", "A warm voice", "Merhaba.", "Bir\nIki || 1"])
        self.assertEqual(R["suzgec"], ["X", "", "3"])  # listede olmayan örnek ve metin olmayan değer alınmaz
        self.assertEqual(R["bozuk"], "X")  # bozuk kayıt formu bozmaz / a broken record leaves the form alone


class OkunanSatir(unittest.TestCase):
    def test_baglanti(self):
        self.assertIn("Okunan.bagla(", kes("function okumaCiz(", "const Okunan={"))
        self.assertIn("...kaynak};okumaCiz();", JS)  # gönderilen metnin satırları sonuçla saklanır
        self.assertIn("Okunan.i===k", kes("function defterNo(", "// Kutu boyu"))
        menu = kes(" menu(i,x,b){", " yenile(){")
        self.assertIn("t('buradan_dinle')", menu)
        self.assertIn("if(d.is==='dinle')Okunan.dinle(i);", JS)
        self.assertNotIn(".focus(", kes("const Okunan={", "// ── Açılır menü"))  # parlama odak almaz

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_bos_satir_ve_bant_eslemesi(self):
        sahte = r"""
const $=id=>({value:''});const hafiza=()=>null,defterNo=()=>{},snb=x=>x+' s',t=k=>k,Satir={isik:()=>({k:new Set()})};let sonOkuma=null;
"""
        parca = kes("const Durak={", "const KALP=") + kes("const Okunan={", "// ── Açılır menü")
        R = node(sahte + parca + r"""
const R={},gonderilen=['A','','B || 0.7','C'],k=Okunan.kaynak(gonderilen);
// Sunucu: boş satırı atlar, 3 kayıt (oku.py satirlar) / the server skips the blank line
const r={satirlar:[{satir:1,t0:0,t1:1.5},{satir:2,t0:2,t1:3.5},{satir:3,t0:4,t1:5}],...k};
R.kaynak=k;R.esle=[0,1,2].map(j=>Okunan.satir(r,j,['A','','B','C']));
R.duzenlendi=[0,1,2].map(j=>Okunan.satir(r,j,['X','A','B','C']));
R.silindi=Okunan.satir(r,0,['B','C']);
R.zaman=[-1,0,1.6,1.9,2,3.9,4.5,99].map(x=>Okunan.kayit(r.satirlar,x));
R.bul=[0,1,2,3].map(i=>Okunan.kayitBul(r,i,['A','','B','C']));
R.tutmaz=Okunan.kayitBul({...r,satirlar:r.satirlar.slice(0,2)},0,['A','','B','C']);
R.eski=Okunan.kayitBul({satirlar:r.satirlar},0,['A']);
console.log(JSON.stringify(R));""")
        self.assertEqual(R["kaynak"], {"kaynak": ["A", "", "B", "C"], "dolu": [0, 2, 3]})
        self.assertEqual(R["esle"], [0, 2, 3])  # bekleyen işaret banda taşınmış olsa da aynı satır
        self.assertEqual(R["duzenlendi"], [1, 2, 3])  # üste satır eklendi: cümle aranır
        self.assertEqual(R["silindi"], -1)
        self.assertEqual(R["zaman"], [-1, 0, 0, 0, 1, 1, 2, 2])  # bekleme önceki cümlenin
        self.assertEqual(R["bul"], [0, -1, 1, 2])  # boş satırda "Buradan dinle" yok
        self.assertEqual(R["tutmaz"], -1)  # sayı tutmazsa eşleme yok
        self.assertEqual(R["eski"], -1)  # kaynak yoksa (eski sonuç) eşleme yok


class SunucuSatirSirasi(unittest.TestCase):
    def test_kayit_sirasi_dolu_satirlar(self):
        # Arayüz eşlemesinin dayandığı sözleşme: sunucu (oku.py satirlar ← okunus.lines) yalnız dolu satırları, sırayla verir.
        # The UI mapping relies on this: the server yields only non-blank lines, in order.
        from ses_tasarim import okunus
        gonderilen = "Bir. || 0.35\n\nIki uzun cumle. || 1\n   \nUc."
        satirlar = okunus.lines(okunus.spoken(gonderilen, "tr"))
        dolu = [i for i, l in enumerate(gonderilen.split("\n")) if l.strip()]
        self.assertEqual(len(satirlar), len(dolu))
        self.assertEqual([m for m, _ in satirlar], ["Bir.", "Iki uzun cumle.", "Uc."])


class AralikIstegi(unittest.TestCase):
    def test_aralik_ayristir(self):
        A = arayuz._aralik
        self.assertIsNone(A(None, 100))
        self.assertEqual(A("bytes=0-", 100), (0, 99))
        self.assertEqual(A("bytes=10-19", 100), (10, 19))
        self.assertEqual(A("bytes=90-500", 100), (90, 99))
        self.assertEqual(A("bytes=-10", 100), (90, 99))
        self.assertEqual(A("bytes=100-", 100), "gecersiz")
        self.assertEqual(A("bytes=20-10", 100), "gecersiz")
        self.assertIsNone(A("bytes=0-1,5-6", 100))  # çoklu aralık: tam dosya
        self.assertIsNone(A("items=0-1", 100))
        self.assertIsNone(A("bytes=x-1", 100))

    def test_oynatici_atlayabilir(self):
        import tempfile
        import threading
        import urllib.error
        import urllib.request
        from http.server import ThreadingHTTPServer
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "_okumalar" / "is1"
            d.mkdir(parents=True)
            (d / "okuma.wav").write_bytes(bytes(range(200)))
            server = ThreadingHTTPServer(("127.0.0.1", 0), arayuz.make_handler({"hazir_sesler": Path(tmp), "sesler": Path(tmp)}, None))
            threading.Thread(target=server.serve_forever, daemon=True).start()
            url = f"http://127.0.0.1:{server.server_address[1]}/okuma/is1/okuma.wav"
            try:
                with urllib.request.urlopen(url, timeout=10) as r:
                    tam = (r.status, r.headers["Accept-Ranges"], len(r.read()))
                with urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=100-109"}), timeout=10) as r:
                    parca = (r.status, r.headers["Content-Range"], r.read())
                with self.assertRaises(urllib.error.HTTPError) as h:
                    urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=500-"}), timeout=10)
            finally:
                server.shutdown()
                server.server_close()
        self.assertEqual(tam, (200, "bytes", 200))
        self.assertEqual(parca, (206, "bytes 100-109/200", bytes(range(100, 110))))
        self.assertEqual(h.exception.code, 416)


class KisaYol(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_ctrl_enter(self):
        R = node(kes("const anaIs=", "const KISAYOL=") + r"""
const E=o=>({key:'Enter',ctrlKey:false,metaKey:false,altKey:false,shiftKey:false,isComposing:false,repeat:false,defaultPrevented:false,...o});
console.log(JSON.stringify([anaIs(E({ctrlKey:true}),'p1'),anaIs(E({metaKey:true}),'p2'),anaIs(E({ctrlKey:true}),'p3'),
 anaIs(E({}),'p2'),anaIs(E({altKey:true}),'p2'),anaIs(E({ctrlKey:true,altKey:true}),'p2'),anaIs(E({ctrlKey:true,shiftKey:true}),'p2'),
 anaIs(E({ctrlKey:true,isComposing:true}),'p2'),anaIs(E({ctrlKey:true,repeat:true}),'p2'),anaIs(E({ctrlKey:true,defaultPrevented:true}),'p1'),
 anaIs(E({ctrlKey:true,key:'a'}),'p1'),anaIs(E({ctrlKey:true,keyCode:229}),'p2')]));""")
        self.assertEqual(R, ["btn_tasarla", "btn_oku", None, None, None, None, None, None, None, None, None, None])

    def test_pasif_dugme_ve_menu(self):
        k = kes("const anaIs=", "function dosyaAdi")
        self.assertIn("if(Acilir.acikMi())return;", k)
        self.assertIn("if(!b.disabled)b.click();", k)
        self.assertNotIn(".focus(", k)  # kısayol odak taşımaz / the shortcut never moves focus
        # Defterin kendi Enter'ı Ctrl/Meta'lı Enter'a karışmaz / the notebook's own Enter ignores Ctrl/Meta+Enter
        self.assertIn("if(e.key!=='Enter'||e.shiftKey||e.ctrlKey||e.metaKey", JS)


if __name__ == "__main__":
    unittest.main()

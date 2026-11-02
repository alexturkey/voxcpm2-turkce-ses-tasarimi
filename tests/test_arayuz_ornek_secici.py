"""Örnek tarif seçicisi: aynı seçenek iki kez görünmez (GPU ve ağ gerekmez; davranış testi node ister).
Example prompt picker: no option shows twice (no GPU, no network; the behaviour test needs node).

18 rol 8 dilde aynı adla gelir; eskiden Türkçe arayüzde her dil grubu aynı 18 adı gösteriyordu.
The 18 roles share names across 8 languages; every group used to show the same 18 names.

python -m unittest discover -s tests -v
"""
import json
import shutil
import subprocess
import unittest

from ses_tasarim import arayuz, ornekler

JS = arayuz.HTML.split("<script>")[-1].split("</script>")[0]


def kes(bas, son):
    i = JS.index(bas)
    return JS[i:JS.index(son, i)]


# Yalnız ornekDoldur'un kullandığı DOM parçası / only the DOM that ornekDoldur touches
SAHTE_DOM = r"""
function oge(tag){return {tag,children:[],value:'',label:'',textContent:'',set innerHTML(v){this.children=[];},
 appendChild(c){this.children.push(c);return c;}};}
const document={createElement:oge};
const secici=oge('select');const $=id=>secici;
"""


def node(kod):
    r = subprocess.run(["node", "-"], input=kod, capture_output=True, text=True, encoding="utf-8", timeout=30,
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode:
        raise AssertionError(r.stderr)
    return json.loads(r.stdout)


class OrnekSecici(unittest.TestCase):
    def test_tek_doldurucu(self):
        # Seçenekler tek yerde yazılır ve her doldurma önce temizler / one filler, which clears first
        self.assertEqual(JS.count("$('ornek').appendChild"), 0)
        self.assertIn("s.innerHTML='';", kes("function ornekDoldur(", "$('ornek').addEventListener"))

    @unittest.skipUnless(shutil.which("node"), "node yok")
    def test_secenek_yazilari_tekil(self):
        parca = kes("let dil='tr',S={},YEDEK={};", "function ilkDil(") + kes("let ornekler=[];", "$('ornek').addEventListener")
        veri = json.dumps(ornekler.listele(), ensure_ascii=False)
        sonuc = node(SAHTE_DOM + kes("const DILLER=", "const ESDEGER=") + parca + r"""
ornekler=""" + veri + r""";
const out={};
for(const k of ['tr','en','de','ar']){dil=k;S={kendim:'-'};ornekDoldur();ornekDoldur();
 const yazilar=[];for(const c of secici.children)for(const o of (c.children.length?c.children:[c]))yazilar.push(o.textContent);
 out[k]={n:yazilar.length,tekil:new Set(yazilar).size,ilk:secici.children[1].children[0].textContent,
  grup:secici.children[1].label,son:secici.children.at(-1).children.at(-1).textContent};}
console.log(JSON.stringify(out));""")
        toplam = len(ornekler.listele()) + 1
        for k, r in sonuc.items():
            with self.subTest(k):
                self.assertEqual(r["n"], toplam)          # iki kez doldurmak çoğaltmaz / refilling does not duplicate
                self.assertEqual(r["tekil"], toplam)      # her seçenek yazısı tekil / every option text unique
        self.assertEqual(sonuc["tr"]["ilk"], "Belgesel anlatıcısı, erkek")  # arayüz dili grubu sade / UI group plain
        self.assertTrue(sonuc["tr"]["grup"].startswith("━━  Türkçe"))  # önce arayüz dili / UI language first
        self.assertTrue(sonuc["tr"]["son"].endswith(" · 中文"))
        self.assertEqual(sonuc["de"]["ilk"], "Documentary narrator, male")
        self.assertTrue(sonuc["ar"]["ilk"].endswith(" · English"))  # örneği olmayan dilde hepsi dil adlı


if __name__ == "__main__":
    unittest.main()

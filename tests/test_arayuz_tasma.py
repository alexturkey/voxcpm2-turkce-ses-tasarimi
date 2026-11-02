"""Taşma kuralları: kart zemindir, her şey onun içinde kalır (GPU ve ağ gerekmez).
Overflow rules: the card is the ground, everything stays inside it (no GPU, no network).

Ekran ölçümü (30 dil × 768/390 × durumlar) tarayıcıda yapılır; bu test bulunan hataların kurallarının geri gelmesini önler.
The screen check runs in a browser; this test keeps the fixed rules from regressing.

python -m unittest discover -s tests -v
"""
import re
import unittest

from ses_tasarim import arayuz

CSS = arayuz.HTML.split("<style>")[1].split("</style>")[0]
JS = arayuz.HTML.split("<script>")[-1].split("</script>")[0]


class KartIcinde(unittest.TestCase):
    def test_ad_kutusu_kalici_cercevede_eksi_pay_yok(self):
        # Düğmeler turuncu çerçeveye taşınınca eski karttaki eksi pay Vazgeç'i 22 px dışarı itiyordu
        self.assertIn(".kalici .dugmeler.adli{margin-inline-end:0}", CSS)

    def test_liste_dugmesi_daralabilir(self):
        # Uzun dilde (el, sw) "Okuma listeme ekle" tek satıra sığmayınca çerçeveden 7-10 px taşıyordu
        self.assertIn(".dugmeler .listebtn{flex:0 1 auto;min-width:0;max-width:100%}", CSS)
        self.assertIn(".listebtn .iki>span{overflow-wrap:anywhere}", CSS)


class SolFormKaydirmasiz(unittest.TestCase):
    def test_bos_kutuda_yer_tutucu_cubuk_cikarmaz(self):
        # Uzun yer tutucu (tl, el, my) boş kutuda 15 px kaydırma çubuğu çiziyordu
        self.assertIn("textarea:placeholder-shown{overflow:hidden}", CSS)

    def test_myanmar_satir_yuksekligi(self):
        # Myanmar yazı tipinin "normal" satır yüksekliği formu 767x794'te 42 px uzatıyordu
        self.assertIn(":root:lang(my) body{line-height:1.45}", CSS)


class MenuGorunurAlanda(unittest.TestCase):
    def test_kutu_acilinca_menu_yeniden_sigar(self):
        # Yeniden adlandır kutusu menüyü genişletiyordu (de, ru, nl, el: sağdan 2-29 px dışarı)
        sayi_ac = re.search(r"sayiAc\(o,rakam\)\{[^\n]*", JS).group(0)
        self.assertIn("this.sigdir(o)", sayi_ac)
        sigdir = re.search(r"sigdir\(o\)\{[^\n]*\n[^\n]*", JS).group(0)
        self.assertIn("this.altYer()", sigdir)          # alt menü kendi yerleştiricisiyle
        self.assertIn("B.r-w", sigdir)                   # sağ kenar görünür alanda
        self.assertIn("rtl()?this.x-w", sigdir)          # RTL: sağ kenar tetikte
        self.assertIn("#acilir .ozel.ad input{flex:0 1 14em;min-width:5em}", CSS)


if __name__ == "__main__":
    unittest.main()

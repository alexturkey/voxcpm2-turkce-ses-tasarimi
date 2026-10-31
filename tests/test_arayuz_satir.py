"""Satır menüsü bekçisi: tek menü kabı, tek yazma kapısı, boş satırın arayüzdeki anlamı yok (GPU ve ağ gerekmez).
Line menu guard: one popup container, one write gate, blank lines carry no meaning in the UI (no GPU, no network).

python -m unittest discover -s tests -v
"""
import re
import unittest

from ses_tasarim import arayuz

HTML = arayuz.HTML
JS = HTML.split("<script>")[-1].split("</script>")[0]


class ArayuzSatir(unittest.TestCase):
    def test_tek_menu_kabi(self):
        self.assertNotIn("durakmenu", HTML)
        self.assertEqual(HTML.count('id="acilir"'), 1)
        # Ortak parçalar bir kez tanımlı: ikinci menü için kopya CSS yok
        self.assertEqual(HTML.count("#acilir .onay{"), 1)
        self.assertEqual(HTML.count("#acilir .ozel{"), 1)
        self.assertEqual(HTML.count("#acilir .baslik{"), 1)

    def test_tek_yazma_kapisi(self):
        # okuma_metni'ne doğrudan value ataması yalnız: elle yazılan '||' işareti (hizala), açılış, uygula yedek yolu
        kutu = JS[JS.index("// ── Açılır menü"):JS.index("function dosyaAdi")]
        self.assertLessEqual(len(re.findall(r"\bta\.value=(?!=)", kutu)), 3)
        self.assertNotIn("o.value=o.value", JS)  # okumaya taşı da kapıdan geçer
        self.assertIn("execCommand('insertText'", JS)
        self.assertIn("gecmis", JS)

    def test_bos_satir_anlami_kalkti(self):
        self.assertNotIn("bosSonra", JS)

    def test_klavye_ime_korumasi(self):
        self.assertIn("isComposing", JS)
        self.assertIn('tabindex="-1"', JS)

    def test_hareket_azaltma(self):
        self.assertIn("prefers-reduced-motion", HTML)


if __name__ == "__main__":
    unittest.main()

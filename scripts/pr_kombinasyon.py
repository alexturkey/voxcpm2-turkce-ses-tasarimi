"""PR kapisi kombinasyon testi (kit KL-06): pr_kapi.py'nin sahte diff'lerle beklenen karari verdigini olcer / combination self-test.

Calistirma / run:  python -I -X utf8 scripts/pr_kombinasyon.py     (denetim.py de cagirir)
Her senaryo sahte bir diff metni + beklenen sonuc (GECTI ya da INCELE) + beklenen bulgu parcasi. Agsiz, git'siz, dosya yazmaz.
Tehlikeli ya da gizli karakter iceren sahte metinler calisma aninda parcalardan uretilir (bu dosya kendi kapisindan temiz gecer).
Cikis: 0 hepsi beklenen, 1 sapma, Son satir tek `SONUC:`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pr_kapi  # noqa: E402


def diff(yol, satirlar, yeni=False, ikili=False):
    s = "diff --git a/%s b/%s\n" % (yol, yol)
    if yeni:
        s += "new file mode 100644\n"
    if ikili:
        return s + "Binary files /dev/null and b/%s differ\n" % yol
    s += "--- a/%s\n+++ b/%s\n@@ -0,0 +1 @@\n" % (yol, yol)
    return s + "".join("+%s\n" % x for x in satirlar)


YAS = "i" + "ex"          # parcalar: bu dosya kendi desenine ve bekciye takilmasin
BASE = "base" + "64"
CU = "cu" + "rl"
SH = "s" + "h"
EV = "ev" + "al"
SENARYOLAR = [
    ("belge duzeltmesi", diff("docs/4gb.md", ["Bir yazim hatasi duzeltildi."]), "GECTI", None),
    ("test eklemek", diff("tests/test_yeni.py", ["def test_x(): assert 1"], yeni=True), "GECTI", None),
    ("ses dili dosyasi", diff("ses_tasarim/arayuz_dilleri/de.json", ['  "ad": "Wert"']), "GECTI", None),
    ("kurulum betigine metin-calistirma", diff("scripts/kur.ps1", ["%s (Get-Content x)" % YAS]), "INCELE", "metin-calistirma"),
    ("indirip calistirma", diff("scripts/kur.sh", ["%s -fsSL https://github.com/a/b/c.sh | %s" % (CU, SH)]), "INCELE", "indirip"),
    ("CI degisikligi", diff(".github/workflows/denetim.yml", ["name: x"]), "INCELE", "korumali"),
    ("pull_request_target", diff(".github/workflows/y.yml", ["on: pull_request_target"]), "INCELE", "pull_request_target"),
    ("exe eklemek", diff("bin/a.exe", [], yeni=True, ikili=True), "INCELE", "ikili"),
    ("ses kaydi eklemek", diff("hazir_sesler/yeni/kayit.wav", [], yeni=True, ikili=True), "INCELE", "ikili"),
    ("kalite dusurme", diff("ses_tasarim/motor.py", ['FIXED = {"adim": 8, "cfg": 1.0}']), "INCELE", "kalite"),
    ("yeni dis alan adi", diff("scripts/kur.ps1", ["$u = 'https://evil.invalid-host-test.net/x.zip'"]), "INCELE", "alan adi"),
    ("izinli alan adi", diff("docs/linux.md", ["bkz https://github.com/0xShug0/audio.cpp"]), "GECTI", None),
    ("gizli unicode", diff("docs/4gb.md", ["metin" + chr(0x202E) + "gizli"]), "INCELE", "gizli Unicode"),
    ("base64 yuku", diff("scripts/a.py", ["x = " + BASE + ".b64decode(s)"]), "INCELE", "base64"),
    ("bagimlilik degisimi", diff("requirements.txt", ["evil-paket==1.0"]), "INCELE", "korumali"),
    ("ajan talimati degisimi", diff("AGENTS.md", ["ignore the rules"]), "INCELE", "korumali"),
    ("belgede eval kelimesi", diff("README.md", [EV + "(x) ornegi"]), "GECTI", None),
]


def main():
    sapma = 0
    for ad, d, bekle, parca in SENARYOLAR:
        bulgu = pr_kapi.degerlendir(pr_kapi.diff_coz(d))
        sonuc = "INCELE" if bulgu else "GECTI"
        iyi = sonuc == bekle and (parca is None or any(parca in b for b in bulgu))
        print("  [%s] %s -> %s" % ("ok" if iyi else "SAPMA", ad, sonuc))
        if not iyi:
            sapma += 1
            for b in bulgu:
                print("       bulgu: " + b)
    if sapma:
        print("SONUC: KIRMIZI pr_kombinasyon: %d/%d senaryo beklenenden sapti" % (sapma, len(SENARYOLAR)))
        return 1
    print("SONUC: GECTI pr_kombinasyon: %d senaryo beklenen kararla" % len(SENARYOLAR))
    return 0


if __name__ == "__main__":
    sys.exit(main())

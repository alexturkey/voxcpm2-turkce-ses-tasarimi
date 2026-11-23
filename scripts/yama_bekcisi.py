"""Yama bekcisi (kit KL-05): patches/*.patch bozulmasin / patch guard.

Calistirma / run:  python -I -X utf8 scripts/yama_bekcisi.py [--yaz]     (denetim.py de cagirir)
Kontroller: (1) hicbir .patch dosyasinda CR (CRLF) yok; (2) .gitattributes `*.patch -text` satiri var; (3) her yamanin sha256'si
scripts/yama_hash.json tablosundaki ile ayni; tabloda olmayan/fazla yama yok. --yaz tabloyu bilerek yenilemek icindir (yama degistirince).
Cikis: 0 gecti, 1 kirmizi, 3 ortam hatasi. Son satir tek `SONUC:`.
NEDEN: CRLF'li ya da sessizce degismis yama kaynaga uygulanmaz ya da yanlis uygulanir (kur.ps1 imza denetimi var, bu ondan once yakalar).
BEDEL: yama her degistiginde `--yaz` ile tablo yenilenir (kasitli surtunme: degisiklik gozle gorulur olur). GEVSETME: yok; kasitli degisiklik --yaz ile.
"""
import glob
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLO = os.path.join(KOK, "scripts", "yama_hash.json")


def yamalar(kok=KOK):
    return sorted(glob.glob(os.path.join(kok, "patches", "*.patch")))


def sha(yol):
    with open(yol, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def denetle(kok=KOK, tablo=TABLO):
    kirmizi = []
    ys = yamalar(kok)
    if not ys:
        return ["patches/ altinda yama yok"]
    for y in ys:
        ad = os.path.basename(y)
        with open(y, "rb") as f:
            if b"\r" in f.read():
                kirmizi.append("%s: CR (CRLF) iceriyor; yama LF olmali" % ad)
    try:
        with open(os.path.join(kok, ".gitattributes"), encoding="utf-8") as f:
            ga = f.read()
    except OSError:
        ga = ""
    if "*.patch -text" not in ga:
        kirmizi.append(".gitattributes icinde `*.patch -text` yok")
    try:
        with open(tablo, encoding="utf-8") as f:
            bekle = json.load(f)
    except (OSError, ValueError):
        return kirmizi + ["scripts/yama_hash.json okunamadi (olusturmak icin --yaz)"]
    var = {os.path.basename(y): sha(y) for y in ys}
    for ad, h in sorted(var.items()):
        if ad not in bekle:
            kirmizi.append("%s: sha256 tablosunda yok (kasitliysa --yaz)" % ad)
        elif bekle[ad] != h:
            kirmizi.append("%s: sha256 degismis (kasitliysa --yaz ile tabloyu yenile)" % ad)
    for ad in sorted(set(bekle) - set(var)):
        kirmizi.append("%s: tabloda var ama dosya yok" % ad)
    return kirmizi


def main(argv):
    if "--yaz" in argv:
        t = {os.path.basename(y): sha(y) for y in yamalar()}
        with open(TABLO, "w", encoding="utf-8", newline="\n") as f:
            json.dump(t, f, indent=2, sort_keys=True)
            f.write("\n")
        print("yazildi: scripts/yama_hash.json (%d yama)" % len(t))
    kirmizi = denetle()
    for s in kirmizi:
        print("  [KIRMIZI] " + s)
    if kirmizi:
        print("SONUC: KIRMIZI yama_bekcisi: %d bulgu" % len(kirmizi))
        return 1
    print("SONUC: GECTI yama_bekcisi: %d yama, CRLF yok, sha256 tablosu esit" % len(yamalar()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

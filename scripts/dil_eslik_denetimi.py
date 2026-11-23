"""Dil esligi denetimi (kit KL-07): README cevirileri ve arayuz dili dosyalari kaynakla uyumlu mu / translation parity gate.

Calistirma / run:  python -I -X utf8 scripts/dil_eslik_denetimi.py        (denetim.py de cagirir)
Ayar: scripts/dil_profili.json (kademe A kati, kademe B yumusak). Cikis: 0 gecti, 1 kirmizi, 3 ortam hatasi. Son satir tek `SONUC:`.
Ne olcer: baslik sayisi, tablo satiri sayisi, kod blogu sayisi, dis baglanti kumesi (README.md ile), arayuz JSON anahtar kumesi (en.json ile).
Ne OLCMEZ: cevirinin dogrulugu ya da guncelligi (metin karsilastirmasi yok); bir cevirmenin gozunun yerini tutmaz.
NEDEN: eksik bolum ya da kirik baglanti bir dilde sessizce kalir. BEDEL: yeni bolum once EN+TR'ye girince B kademesinde UYARI cikar.
GEVSETME: kademe B zaten uyari; kirmizi yapmak icin dil_profili.json'da dili A'ya al.
"""
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def yapi(metin):
    t = metin.replace("\r\n", "\n")
    return {
        "baslik": len(re.findall(r"(?m)^#{1,6} ", t)),
        "tablo": len(re.findall(r"(?m)^\|", t)),
        "kod": len(re.findall(r"(?m)^```", t)),
        "url": frozenset(re.findall(r"\]\((https?://[^)\s]+)\)", t)),
    }


def oku(yol):
    with open(yol, encoding="utf-8") as f:
        return f.read()


def denetle(kok=KOK):
    """(kirmizi[], uyari[], olculen_dil_sayisi) doner. Ayar dosyasi yoksa ya da bozuksa ValueError."""
    try:
        with open(os.path.join(kok, "scripts", "dil_profili.json"), encoding="utf-8") as f:
            p = json.load(f)
        kaynak = yapi(oku(os.path.join(kok, p["kaynak"])))
    except (OSError, ValueError, KeyError) as e:
        raise ValueError("ayar ya da kaynak okunamadi: %s" % type(e).__name__)
    kirmizi, uyari, n = [], [], 0
    for kademe, diller in sorted(p["kademe"].items()):
        for d in diller:
            yol = os.path.join(kok, p["ceviri_deseni"].format(dil=d))
            n += 1
            if not os.path.isfile(yol):
                kirmizi.append("%s: README ceviri dosyasi yok (%s)" % (d, os.path.basename(yol)))
                continue
            y = yapi(oku(yol))
            if y["kod"] != kaynak["kod"]:
                kirmizi.append("%s: kod blogu sayisi %d, kaynakta %d" % (d, y["kod"], kaynak["kod"]))
            if y["url"] != kaynak["url"]:
                kirmizi.append("%s: baglanti kumesi kaynaktan farkli (eksik %d, fazla %d)" % (d, len(kaynak["url"] - y["url"]), len(y["url"] - kaynak["url"])))
            for alan in ("baslik", "tablo"):
                if y[alan] != kaynak[alan]:
                    (kirmizi if kademe == "A" else uyari).append("%s: %s sayisi %d, kaynakta %d (kademe %s)" % (d, alan, y[alan], kaynak[alan], kademe))
    # arayuz dili anahtar kumesi
    ar = p.get("arayuz_dilleri")
    if ar:
        ref = json.loads(oku(os.path.join(kok, ar.format(dil=p["arayuz_kaynak"]))))
        klasor = os.path.dirname(os.path.join(kok, ar))
        for ad in sorted(os.listdir(klasor)):
            if not ad.endswith(".json"):
                continue
            try:
                d = json.loads(oku(os.path.join(klasor, ad)))
            except ValueError:
                kirmizi.append("%s: gecerli JSON degil" % ad)
                continue
            if set(d) != set(ref):
                kirmizi.append("%s: arayuz anahtarlari en.json'dan farkli (eksik %d, fazla %d)" % (ad, len(set(ref) - set(d)), len(set(d) - set(ref))))
    return kirmizi, uyari, n


def main():
    try:
        kirmizi, uyari, n = denetle()
    except ValueError as e:
        print("SONUC: CALISAMADI dil_eslik: %s" % e)
        return 3
    for s in kirmizi:
        print("  [KIRMIZI] " + s)
    for s in uyari:
        print("  [uyari] " + s)
    if kirmizi:
        print("SONUC: KIRMIZI dil_eslik: %d kirmizi, %d uyari (%d dil)" % (len(kirmizi), len(uyari), n))
        return 1
    print("SONUC: GECTI dil_eslik: %d dil, %d uyari (kademe B yapi farklari uyaridir)" % (n, len(uyari)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Denetim cekirdegi (kit KL-03): tek komutla repo kapilari / one-command repo gates.

Calistirma / run:
  python -I -X utf8 scripts/denetim.py --hizli          ~saniyeler, agsiz, GPU yok (PR'dan once; CI de bunu kosar)
  python -I -X utf8 scripts/denetim.py --tam            --hizli + tum birim testleri (~1 dk)
  python -I -X utf8 scripts/denetim.py --kapi gizlilik  tek kapi (gizlilik, yama, dil, pr, kalite, ps1, yertutucu, testler)
Kapilar: gizlilik (kisisel yol/e-posta/sir + gizli Unicode: scripts/gizlilik_denetimi.py), yama (scripts/yama_bekcisi.py), dil (scripts/dil_eslik_denetimi.py),
pr (scripts/pr_kombinasyon.py: PR kapisi sahte diff'lerle), kalite (16 adim, cfg 2.0 sabiti), ps1 (PowerShell dosyalari ASCII ya da UTF-8 BOM'lu),
yertutucu (doldurulmamis {{AD}} kalmamis). Alt kapilar ayri sureclerde kosar; her biri kendi `SONUC:` satirini basar.
Cikis kodlari / exit codes: 0 = hepsi GECTI; 1 = en az bir kapi KIRMIZI; 3 = girdi/ortam hatasi (git ya da Python eksik); 6 = bir kapi CALISAMADI
(calisamayan kapi yesil sayilmaz). Son satir her zaman tek `SONUC:`.
NEDEN: kapilar tek yerde olunca "bende gecti" belirsizligi biter; PR gondermeden once ayni komut CI'da da kosar.
BEDEL: yeni kapi eklemek bu dosyada ve README'de bir satir. GEVSETME: bir kapiyi kapatmak ancak gerekceyle ve bu dosyada gorunur sekilde.
"""
import os
import re
import subprocess
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable, "-I", "-X", "utf8", "-B"]
ALT = {
    "gizlilik": "scripts/gizlilik_denetimi.py",
    "yama": "scripts/yama_bekcisi.py",
    "dil": "scripts/dil_eslik_denetimi.py",
    "pr": "scripts/pr_kombinasyon.py",
}


def alt_surec(ad, betik):
    try:
        c = subprocess.run(PY + [os.path.join(KOK, betik)], cwd=KOK, capture_output=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired):
        return "CALISAMADI", ["alt surec calismadi: " + betik]
    cikti = c.stdout.decode("utf-8", "replace").strip().split("\n")
    son = next((s for s in reversed(cikti) if s.startswith("SONUC:")), "")
    detay = [s for s in cikti if s and not s.startswith("SONUC:")][:12]
    if c.returncode == 0 and son.startswith("SONUC: GECTI"):
        return "GECTI", [son[7:]]
    if c.returncode == 1:
        return "KIRMIZI", detay + [son[7:]]
    return "CALISAMADI", detay + [son[7:] or ("cikis kodu %d" % c.returncode)]


def kapi_kalite():
    try:
        with open(os.path.join(KOK, "ses_tasarim", "motor.py"), encoding="utf-8") as f:
            t = f.read()
    except OSError:
        return "CALISAMADI", ["ses_tasarim/motor.py okunamadi"]
    if re.search(r'(?m)^FIXED = \{"adim": 16, "cfg": 2\.0\}\s*$', t):
        return "GECTI", ["FIXED = 16 adim, cfg 2.0 (motor.py)"]
    return "KIRMIZI", ["ses_tasarim/motor.py: FIXED sabiti 16 adim / cfg 2.0 degil ya da bicimi degismis (kalite sabitleri dusurulmez)"]


def izlenen():
    try:
        c = subprocess.run(["git", "-C", KOK, "ls-files", "-z", "--cached", "--others", "--exclude-standard"], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return [p for p in c.stdout.decode("utf-8", "replace").split("\0") if p and os.path.isfile(os.path.join(KOK, p))]


def kapi_ps1():
    dosyalar = izlenen()
    if dosyalar is None:
        return "CALISAMADI", ["git dosya listesi alinamadi"]
    kotu = []
    for p in dosyalar:
        if p.lower().endswith(".ps1"):
            with open(os.path.join(KOK, p), "rb") as f:
                b = f.read()
            if not b.startswith(b"\xef\xbb\xbf") and any(x > 127 for x in b):
                kotu.append("%s: ASCII disi icerik var ama UTF-8 BOM yok (Windows PowerShell 5.1 bozuk okur)" % p)
    return ("KIRMIZI", kotu) if kotu else ("GECTI", ["PowerShell dosyalari ASCII ya da BOM'lu"])


def kapi_yertutucu():
    dosyalar = izlenen()
    if dosyalar is None:
        return "CALISAMADI", ["git dosya listesi alinamadi"]
    rx = re.compile(r"\{\{[A-Z][A-Z0-9_]{2,}\}\}")
    kotu = []
    for p in dosyalar:
        if p.startswith(("scripts/denetim.py",)) or p.lower().endswith(IKILI_UZ):
            continue
        with open(os.path.join(KOK, p), "rb") as f:
            m = rx.search(f.read().decode("utf-8", "replace"))
        if m:
            kotu.append("%s: doldurulmamis yer tutucu" % p)
    return ("KIRMIZI", kotu[:12]) if kotu else ("GECTI", ["yer tutucu kalmamis"])


IKILI_UZ = (".png", ".jpg", ".gif", ".ico", ".wav", ".mp3", ".flac", ".svg", ".zip", ".gguf", ".woff", ".woff2")


def kapi_testler():
    try:
        c = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-q"], cwd=KOK, capture_output=True, timeout=900)
    except (OSError, subprocess.TimeoutExpired):
        return "CALISAMADI", ["birim testleri calismadi"]
    son = c.stderr.decode("utf-8", "replace").strip().split("\n")[-3:]
    return ("GECTI" if c.returncode == 0 else "KIRMIZI"), [s for s in son if s]


KAPILAR = {
    "gizlilik": lambda: alt_surec("gizlilik", ALT["gizlilik"]),
    "yama": lambda: alt_surec("yama", ALT["yama"]),
    "dil": lambda: alt_surec("dil", ALT["dil"]),
    "pr": lambda: alt_surec("pr", ALT["pr"]),
    "kalite": kapi_kalite,
    "ps1": kapi_ps1,
    "yertutucu": kapi_yertutucu,
    "testler": kapi_testler,
}
HIZLI = ["kalite", "gizlilik", "yama", "dil", "pr", "ps1", "yertutucu"]


def main(argv):
    if "--hizli" in argv:
        sec = HIZLI
    elif "--tam" in argv:
        sec = HIZLI + ["testler"]
    elif "--kapi" in argv and argv.index("--kapi") + 1 < len(argv) and argv[argv.index("--kapi") + 1] in KAPILAR:
        sec = [argv[argv.index("--kapi") + 1]]
    else:
        print(__doc__.split("Kapilar:")[0].strip())
        print("SONUC: CALISAMADI denetim: --hizli, --tam ya da --kapi <ad> ver (kapilar: %s)" % ", ".join(KAPILAR))
        return 3
    if izlenen() is None:
        print("SONUC: CALISAMADI denetim: git yok ya da burasi bir git deposu degil")
        return 3
    sayac = {"GECTI": 0, "KIRMIZI": 0, "CALISAMADI": 0}
    for ad in sec:
        d, satirlar = KAPILAR[ad]()
        sayac[d] += 1
        print("[%s] %s" % (d, ad))
        for s in satirlar:
            print("    " + s)
    ozet = "%d gecti, %d kirmizi, %d calisamadi" % (sayac["GECTI"], sayac["KIRMIZI"], sayac["CALISAMADI"])
    if sayac["CALISAMADI"]:
        print("SONUC: CALISAMADI denetim (cikis 6): %s" % ozet)
        return 6
    if sayac["KIRMIZI"]:
        print("SONUC: KIRMIZI denetim (cikis 1): %s" % ozet)
        return 1
    print("SONUC: GECTI denetim (cikis 0): %s" % ozet)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

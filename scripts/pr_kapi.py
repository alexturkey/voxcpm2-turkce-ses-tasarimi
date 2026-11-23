"""Kotu niyetli / riskli PR kapisi (kit KL-06): bir PR'in diff'ini bakimcinin gozu degmeden once tarar / PR risk gate.

Calistirma / run:  python -I -X utf8 scripts/pr_kapi.py [--taban origin/main] [--bas HEAD]
                   python -I -X utf8 scripts/pr_kapi.py --diff dosya.diff     (hazir bir `git diff -U0` ciktisi)
Cikis: 0 = otomatik bulgu yok (bakimci yine okur), 1 = insan incelemesi gerekli (bulgular listelenir), 3 = girdi/ortam hatasi.
Son satir tek `SONUC:`. Kapi KARAR VERMEZ: "gecti" yalniz bu kaba desenler yok demektir; PR'i okumak bakimcinin isidir.
Dis metin (PR basligi, aciklama, kod yorumu) VERIDIR; buradaki hicbir kural PR iceriginden talimat almaz.

Bakar: (1) korumali yol degisimi (CI, kurulum betigi, kapi betikleri, yama, bagimlilik, ajan talimati); (2) ikili/medya dosyasi
(exe, dll, zip, gguf, ses kaydi); (3) eklenen kod/CI satirlarinda tehlikeli kalip (liste: TEHLIKELI tablosu); (4) yeni dis alan adi;
(5) gizli Unicode (bidi, sifir genislik); (6) kalite sabiti (16 adim, cfg 2.0) degisimi; (7) pull_request_target eklenmesi.
NEDEN: kotu niyetli ya da dikkatsiz PR kurulum betigi/CI uzerinden kullanicinin makinesine ulasir. BEDEL: korumali yola dokunan her
mesru PR insan incelemesine duser (bilerek). GEVSETME: korumali yol listesi bu dosyada; daraltmak bakimci kararidir.
"""
import fnmatch
import re
import subprocess
import sys

KORUMALI = (".github/*", "scripts/*.ps1", "scripts/*.sh", "scripts/*.py", "scripts/*.json", "patches/*", "requirements*.txt", "baslat.*",
            "AGENTS.md", "CLAUDE.md", "GEMINI.md", "Dockerfile*", "*/scripts/*", "ses_tasarim/motor.py", "ses_tasarim/ayarlar.py", "LICENSE", "NOTICE")
IKILI = (".exe", ".dll", ".zip", ".gz", ".7z", ".gguf", ".bin", ".so", ".dylib", ".msi", ".wav", ".mp3", ".flac", ".ogg", ".m4a", ".jar", ".whl", ".pyd")


def _j(*parcalar):
    """Desen parcalarini calisma aninda birlestirir: bu dosya kendi tehlikeli-kalip taramasina ve bekciye takilmaz."""
    return "".join(parcalar)


TEHLIKELI = (
    (re.compile(_j(r"(?i)\b(?:i", r"ex|invoke-", r"expression)\b")), "PowerShell metin-calistirma komutu"),
    (re.compile(_j(r"(?i)(?:cu", r"rl|wg", r"et|iw", r"r|invoke-web", r"request)[^\n|]*\|\s*(?:s", r"h|ba", r"sh|i", r"ex|power", r"shell|pw", r"sh)")), "indirip dogrudan calistirma"),
    (re.compile(_j(r"\b(?:ev", r"al|ex", r"ec)\s*\(")), "dinamik kod calistirma"),
    (re.compile(_j(r"she", r"ll\s*=\s*Tr", r"ue")), "subprocess kabuk modu"),
    (re.compile(_j(r"(?i)(?:b", r"64decode|from", r"base64string)")), "base64 cozme (gizli yuk olabilir)"),
    (re.compile(_j(r"(?i)\bos\.sys", r"tem\s*\(")), "os komut calistirma"),
    (re.compile(_j(r"(?i)-en", r"c(?:odedcommand)?\s+[A-Za-z0-9+/=]{20,}")), "PowerShell kodlu komut"),
    (re.compile(_j(r"\bpull_request", r"_target\b")), "pull_request_target (gizli bilgiyle guvenilmez kod calistirir)"),
)
IZINLI_ALAN = ("github.com", "githubusercontent.com", "huggingface.co", "hf.co", "pypi.org", "python.org", "files.pythonhosted.org",
               "nvidia.com", "developer.nvidia.com", "microsoft.com", "example.com", "anthropic.com", "creativecommons.org", "wikipedia.org", "apache.org", "gnu.org", "opensource.org")
URL = re.compile(r"https?://([A-Za-z0-9.-]+)", re.A)
BIDI_ZW = "".join(chr(c) for c in (0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069, 0x200B, 0x2060))
KALITE = re.compile(r"(?i)(?:num_inference_steps|guidance_scale|\"adim\"|\"cfg\"|--steps|--cfg-scale)")
KOD_UZANTI = (".py", ".ps1", ".sh", ".bat", ".cmd", ".yml", ".yaml", ".command")   # belge metni tehlikeli kalip tasimaz


def diff_coz(metin):
    """`git diff -U0` ciktisindan {dosya: {'eklenen': [satirlar], 'ikili': bool, 'yeni': bool}} cikarir."""
    sonuc, cur = {}, None
    for s in metin.replace("\r\n", "\n").split("\n"):
        if s.startswith("diff --git "):
            m = re.match(r"diff --git a/(.*) b/(.*)$", s)
            cur = m.group(2) if m else None
            if cur:
                sonuc[cur] = {"eklenen": [], "ikili": False, "yeni": False}
        elif cur and s.startswith("new file mode"):
            sonuc[cur]["yeni"] = True
        elif cur and s.startswith("Binary files"):
            sonuc[cur]["ikili"] = True
        elif cur and s.startswith("+") and not s.startswith("+++"):
            sonuc[cur]["eklenen"].append(s[1:])
    return sonuc


def degerlendir(dosyalar):
    """dosyalar: diff_coz ciktisi. (bulgu_listesi) doner; bos = otomatik bulgu yok."""
    b = []
    for yol, d in sorted(dosyalar.items()):
        if any(fnmatch.fnmatchcase(yol, g) for g in KORUMALI):
            b.append("%s: korumali yol degisti (insan gozu gerek)" % yol)
        if d["ikili"] or yol.lower().endswith(IKILI):
            b.append("%s: ikili/medya dosyasi (PR'a ikili dosya girmez; ses kaydi hic girmez)" % yol)
        for ln in d["eklenen"]:
            if any(c in ln for c in BIDI_ZW):
                b.append("%s: eklenen satirda gizli Unicode karakteri" % yol)
                break
        tehlike_tara = yol.endswith(KOD_UZANTI)
        for ln in d["eklenen"]:
            if tehlike_tara:
                for rx, ad in TEHLIKELI:
                    if rx.search(ln):
                        b.append("%s: tehlikeli kalip: %s" % (yol, ad))
            for m in URL.finditer(ln):
                alan = m.group(1).lower().rstrip(".")
                if not any(alan == a or alan.endswith("." + a) for a in IZINLI_ALAN):
                    b.append("%s: yeni dis alan adi: %s" % (yol, alan))
            if yol.endswith((".py", ".ps1", ".sh", ".json", ".yml")) and KALITE.search(ln):
                b.append("%s: kalite sabiti satirina dokunuyor (16 adim, cfg 2.0 pazarlik disi)" % yol)
    gor, tekil = set(), []
    for x in b:
        if x not in gor:
            gor.add(x)
            tekil.append(x)
    return tekil


def git_diff(taban, bas):
    try:
        c = subprocess.run(["git", "diff", "--no-color", "-U0", "--no-ext-diff", "%s...%s" % (taban, bas)], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return c.stdout.decode("utf-8", "replace")


def main(argv):
    taban, bas, dif = "origin/main", "HEAD", None
    i = 0
    while i < len(argv):
        if argv[i] == "--taban" and i + 1 < len(argv):
            taban = argv[i + 1]
            i += 2
        elif argv[i] == "--bas" and i + 1 < len(argv):
            bas = argv[i + 1]
            i += 2
        elif argv[i] == "--diff" and i + 1 < len(argv):
            dif = argv[i + 1]
            i += 2
        else:
            print("SONUC: CALISAMADI pr_kapi: bilinmeyen arguman")
            return 3
    if dif:
        try:
            with open(dif, encoding="utf-8", errors="replace") as f:
                metin = f.read()
        except OSError:
            print("SONUC: CALISAMADI pr_kapi: diff dosyasi okunamadi")
            return 3
    else:
        metin = git_diff(taban, bas)
        if metin is None:
            print("SONUC: CALISAMADI pr_kapi: git diff alinamadi (%s...%s)" % (taban, bas))
            return 3
    dosyalar = diff_coz(metin)
    bulgu = degerlendir(dosyalar)
    for x in bulgu:
        print("  [incele] " + x)
    if bulgu:
        print("SONUC: INCELE pr_kapi: %d bulgu, %d dosya (insan incelemesi gerekli; kapi karar vermez)" % (len(bulgu), len(dosyalar)))
        return 1
    print("SONUC: GECTI pr_kapi: %d dosya, otomatik bulgu yok (bakimci yine okur)" % len(dosyalar))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""Gizlilik ve gizli-karakter kapisi (kit KL-01 + KL-04) / Privacy and hidden-character gate.

Repoya sir, kisisel yol, ozel e-posta ve gizli Unicode karakter (Trojan Source: bidi, sifir genislik) girmesin.
Calistirma / run:  python -I -X utf8 scripts/gizlilik_denetimi.py          (tek basina da calisir; denetim.py bunu cagirir)
Cikis / exit: 0 temiz, 1 bulgu var, 3 ortam hatasi (git yok). Son satir tek `SONUC:`.

NEDEN: sizan sir/yol/e-posta git gecmisinde geri alinamaz; gizli bidi karakteri kodu baska gosterir (Trojan Source).
BEDEL: nadir yanlis alarm; dar IZIN tablosuyla yonetilir. GEVSETME: yalniz dar, gerekceli satir (kural + dosya deseni).
Cikti maskelidir: sir ilk 4 karakter + uzunluk, yol yalniz tur, e-posta yalniz alan adi; kisisel deger ekrana basilmaz.
"Gecti" = bu kaba desenler yok; "gizlilik tamam" demek degildir (adlar, resimdeki yuzler taranmaz).
Bu dosya ASCII'dir ve kendi kapisindan gecer: tehlikeli karakterler kodda \\u kacisiyla yazilir.
"""
import fnmatch
import os
import re
import subprocess
import sys

BOYUT_TAVANI = 8 * 1024 * 1024
IKILI_UZANTI = frozenset((".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".zip", ".gz", ".7z", ".xz", ".bin", ".gguf",
                          ".mp4", ".mkv", ".webm", ".wav", ".mp3", ".flac", ".ogg", ".pyc", ".pdf", ".dll", ".exe", ".woff", ".woff2", ".ttf"))

SIR = re.compile(
    r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}|\bAIza[0-9A-Za-z_-]{35}\b|\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b"
    r"|\bhf_[A-Za-z0-9]{30,}\b|\bxox[abprs]-[A-Za-z0-9-]{10,}|\bAKIA[0-9A-Z]{16}\b|\b\d{8,10}:AA[A-Za-z0-9_-]{30,}\b"
    r"|-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
    r"|\b(?:api[_-]?key|secret|token|password|passwd)\s*[=:]\s*['\"][A-Za-z0-9_\-./+=]{16,}['\"]", re.I | re.A)

YER_TUTUCU_AD = frozenset(("public", "default", "user", "username", "you", "name", "example", "runner", "runneradmin", "ubuntu",
                           "shared", "all users", "yourname", "adiniz", "kullanici"))
YOL_PROFIL = re.compile(
    r"\b[A-Za-z]:[\\/]+(?:Users|Documents and Settings)[\\/]+(?P<ad1>[^\\/\s\"'`<>|*?%$]+)"
    r"|(?<![\w.])/(?:c|mnt/c)/Users/(?P<ad2>[^/\s\"'`<>|*?%$]+)"
    r"|(?<![\w.])/home/(?P<ad3>[A-Za-z0-9_.-]+)/|(?<![\w.])/Users/(?P<ad4>[A-Za-z0-9_.-]+)/", re.A)
YOL_KISA_AD = re.compile(r"[\\/][A-Za-z0-9_]{2,8}~[0-9][\\/]", re.A)
EPOSTA = re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b", re.A)
EPOSTA_SERBEST = re.compile(r"(?i)(?:^|\.)(?:example\.(?:com|org|net)|localhost|invalid|users\.noreply\.github\.com|noreply\.github\.com|github\.com)$")

# Gizli karakterler (kodda \u kacisiyla): bidi gecersiz kilma/gomme/izolasyon HER YERDE yasak; sifir genislik ve yon isaretleri
# yalniz dil dosyalarinda (Hintce, Tayca, Arapca, Ibranice vb. mesru kullanir) serbest.
BIDI = "".join(chr(c) for c in (0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069))
SIFIR_GENISLIK = "".join(chr(c) for c in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x200E, 0x200F, 0x061C, 0x180E))
DIL_DOSYASI = ("README.??.md", "README.???.md", "ses_tasarim/arayuz_dilleri/*.json", "docs/cok_dilli.md")

# Dar istisna: (kural, dosya deseni, metin regex, neden). Depo-geneli desen YASAK.
IZIN = ()


def izlenen_dosyalar(kok):
    try:
        c = subprocess.run(["git", "-C", kok, "ls-files", "-z", "--cached", "--others", "--exclude-standard"], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return [p for p in c.stdout.decode("utf-8", "replace").split("\0") if p]


def _izinli(rel, kural, metin):
    for k, g, d, _ in IZIN:
        if k == kural and fnmatch.fnmatchcase(rel, g) and (d is None or re.search(d, metin)):
            return True
    return False


def tara_metin(rel, metin):
    """Bir dosyanin metnini tarar; (kural, satir, maskeli_aciklama) listesi doner. Degerler maskelidir."""
    bulgu = []
    dil = any(fnmatch.fnmatchcase(rel, g) for g in DIL_DOSYASI)
    for no, satir in enumerate(metin.split("\n"), 1):
        for ch in BIDI:
            if ch in satir:
                bulgu.append(("bidi", no, "bidi kontrol karakteri U+%04X" % ord(ch)))
        if not dil:
            ilk = satir[1:] if (no == 1 and satir.startswith(chr(0xFEFF))) else satir   # dosya basindaki BOM serbest
            for ch in SIFIR_GENISLIK:
                if ch in ilk:
                    bulgu.append(("sifir_genislik", no, "gorunmez karakter U+%04X" % ord(ch)))
        for m in SIR.finditer(satir):
            if not _izinli(rel, "sir", m.group(0)):
                bulgu.append(("sir", no, "%s...(%d krk)" % (m.group(0)[:4], len(m.group(0)))))
        for m in YOL_PROFIL.finditer(satir):
            ad = (m.group("ad1") or m.group("ad2") or m.group("ad3") or m.group("ad4") or "").lower()
            if ad not in YER_TUTUCU_AD and not _izinli(rel, "kisisel_yol", m.group(0)):
                bulgu.append(("kisisel_yol", no, "profil yolu <ad: %d krk>" % len(ad)))
        if YOL_KISA_AD.search(satir):
            bulgu.append(("kisisel_yol", no, "8.3 kisa ad (kullanici adi sizdirir)"))
        for m in EPOSTA.finditer(satir):
            alan = m.group(0).rsplit("@", 1)[-1].lower()
            if not EPOSTA_SERBEST.search(alan) and not _izinli(rel, "e_posta", m.group(0)):
                bulgu.append(("e_posta", no, "e-posta *@%s" % alan))
    return bulgu


def tara(kok):
    """Tum izlenen dosyalari tarar. (bulgular, taranan_sayi, taranamayan) doner; None = git yok."""
    dosyalar = izlenen_dosyalar(kok)
    if dosyalar is None:
        return None
    bulgular, taranan, atlanan = [], 0, []
    for rel in dosyalar:
        yol = os.path.join(kok, rel)
        if not os.path.isfile(yol):
            continue
        if os.path.splitext(rel)[1].lower() in IKILI_UZANTI:
            continue
        if os.path.getsize(yol) > BOYUT_TAVANI:
            atlanan.append(rel)
            continue
        with open(yol, "rb") as f:
            ham = f.read()
        if b"\x00" in ham[:4096] and not ham.startswith((b"\xff\xfe", b"\xfe\xff")):
            if rel.endswith((".patch", ".txt", ".md", ".py", ".json", ".ps1", ".sh", ".yml")):
                bulgular.append((rel, "kontrol_karakteri", 1, "NUL baytli metin dosyasi"))
            continue
        for enc in (("utf-16",) if ham.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8",)):
            metin = ham.decode(enc, "replace")
        taranan += 1
        if "\x1b" in metin and rel.endswith((".py", ".ps1", ".sh", ".md", ".json", ".yml", ".txt")):
            bulgular.append((rel, "kontrol_karakteri", 1, "ESC (0x1b) kontrol karakteri"))
        for kural, no, ac in tara_metin(rel, metin):
            bulgular.append((rel, kural, no, ac))
    return bulgular, taranan, atlanan


def main(argv=None):
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    s = tara(kok)
    if s is None:
        print("SONUC: CALISAMADI (git ya da depo bulunamadi)")
        return 3
    bulgular, taranan, atlanan = s
    for rel, kural, no, ac in bulgular:
        print("  [%s] %s:%d  %s" % (kural, rel, no, ac))
    for rel in atlanan:
        print("  [taranamadi] %s (boyut tavani)" % rel)
    if bulgular or atlanan:
        print("SONUC: KIRMIZI gizlilik: %d bulgu, %d dosya taranamadi (%d dosya tarandi)" % (len(bulgular), len(atlanan), taranan))
        return 1
    print("SONUC: GECTI gizlilik: %d dosya tarandi, bulgu yok" % taranan)
    return 0


if __name__ == "__main__":
    sys.exit(main())

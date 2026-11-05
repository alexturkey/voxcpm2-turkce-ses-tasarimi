"""Vulkan motor paketi seçimi: bu işlemci AVX2 paketini çalıştırabilir mi?
Which Vulkan engine package fits this CPU: the AVX2 build or the compatible (no-AVX) build?

AVX2 paketi (MSVC /arch:AVX2) yalnız AVX2 değil FMA, F16C ve BMI2 komutları da içerir (exe taraması 2026-11-05: AVX2 342,
FMA 461, F16C 111, BMI2 36 komut; Intel SDE Sandy Bridge taklidinde açılışta `--list-devices` sırasında bile BMI2 `shlx`
ile durur). İki katmanlı denetim / two layers:
1. `paket()`: numpy'nin çalışma anındaki işlemci tespiti (CPUID + işletim sisteminin AVX durum desteği). AVX, AVX2, FMA3,
   F16C her numpy sürümünde var; biri eksikse uyumlu. BMI, BMI2, LZCNT yalnız yeni numpy'de listelenir (2.2.6'da yok):
   listedeyse denetlenir, değilse "bilinmiyor" döner ve 2. katmana kalır. numpy okunamazsa uyumlu.
2. `dene(exe)`: seçilen AVX2 exe'si `--list-devices` ile bir kez çalıştırılır; işlemci komutu tanımazsa Windows süreci
   STATUS_ILLEGAL_INSTRUCTION (0xC000001D) ile bitirir. kur.ps1 exe'yi yerleştirmeden önce geçici klasörde dener;
   "ok" dışındaki her sonuçta uyumlu paketi kurar.
numpy reports AVX/AVX2/FMA3/F16C in every version; BMI/BMI2/LZCNT only in newer ones. Unknown families are left to a test
run of the AVX2 exe: an illegal-instruction exit makes the installer switch to the compatible package.

Kullanım / usage:
  python -m ses_tasarim.islemci              -> 1. satır "avx2" | "uyumlu", 2. satır gerekçe
  python -m ses_tasarim.islemci --dene EXE   -> "ok" | "gecersiz_komut" | "hata <kod>"
"""
import subprocess
import sys

KESIN = ("AVX", "AVX2", "FMA3", "F16C")      # her numpy sürümünde listelenir / listed by every numpy version
EK = ("BMI", "BMI2", "LZCNT")                # yalnız yeni numpy'de / only newer numpy
GECERSIZ_KOMUT = 0xC000001D                  # STATUS_ILLEGAL_INSTRUCTION


def ozellikler():
    """numpy'nin tespit ettiği işlemci özellikleri (ad -> bool); okunamazsa None. / numpy's runtime CPU features."""
    for yol in ("numpy._core._multiarray_umath", "numpy.core._multiarray_umath"):
        try:
            modul = __import__(yol, fromlist=["__cpu_features__"])
            return dict(modul.__cpu_features__)
        except Exception:  # noqa: BLE001 — numpy yok ya da iç yol değişmiş: denetlenemedi
            continue
    return None


def paket(oz=None) -> tuple:
    """('avx2' | 'uyumlu', eksik, bilinmeyen). Özellik listesi yoksa ('uyumlu', ['denetlenemedi'], [])."""
    if oz is None:
        oz = ozellikler()
    if not oz:
        return "uyumlu", ["denetlenemedi"], []
    eksik = [ad for ad in KESIN if not oz.get(ad)] + [ad for ad in EK if ad in oz and not oz[ad]]
    bilinmeyen = [ad for ad in EK if ad not in oz]
    return ("uyumlu" if eksik else "avx2"), eksik, bilinmeyen


SESSIZ_HATA = 0x0001 | 0x0002   # SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX


def _hata_kutusu_kapali():
    """Çöken çocuk süreç Windows'un "çalışmayı durdurdu" kutusunu açmasın (hata kipi çocuğa geçer); eski kipi döner.
    A crashing child must not open the Windows error dialog (the error mode is inherited); returns the old mode."""
    if sys.platform != "win32":
        return None
    import ctypes
    return ctypes.windll.kernel32.SetErrorMode(SESSIZ_HATA)


def dene(exe, zaman_asimi: float = 120) -> str:
    """AVX2 exe'sini `--list-devices` ile bir kez çalıştırır: 'ok' | 'gecersiz_komut' | 'hata <kod>'."""
    eski = _hata_kutusu_kapali()
    try:
        r = subprocess.run([str(exe), "--list-devices"], capture_output=True, timeout=zaman_asimi,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except (OSError, subprocess.TimeoutExpired) as hata:
        return f"hata {type(hata).__name__}"
    finally:
        if eski is not None:
            import ctypes
            ctypes.windll.kernel32.SetErrorMode(eski)
    kod = r.returncode & 0xFFFFFFFF
    if kod == GECERSIZ_KOMUT:
        return "gecersiz_komut"
    return "ok" if kod == 0 else f"hata {kod:#x}"


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) == 2 and argv[0] == "--dene":
        print(dene(argv[1]))
        return 0
    ad, eksik, bilinmeyen = paket()
    print(ad)
    if ad == "avx2":
        ek = f"; bilinmiyor / unknown (deneme calismasina kalir / left to the test run): {', '.join(bilinmeyen)}" if bilinmeyen else ""
        print("var / present: " + ", ".join([a for a in KESIN + EK if a not in bilinmeyen]) + ek)
    else:
        print("eksik / missing: " + ", ".join(eksik))
    return 0


if __name__ == "__main__":
    sys.exit(main())

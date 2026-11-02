"""VoxCPM2 ile Türkçe ses tasarımı ve referanslı okuma (audio.cpp motoru, 4 GB GPU).

Turkish voice design and reference-based reading with VoxCPM2 on a 4 GB GPU (audio.cpp engine).
"""
import sys

__version__ = "0.2.0"


def utf8_cikti() -> None:
    """Komut satırı çıktısı her zaman UTF-8: Windows'ta çıktı dosyaya ya da boruya yönlendirilince Python yerel kod
    sayfasını (ör. cp1254) seçer ve "→", Çince, Arapça yazı UnicodeEncodeError verir. Her CLI main() başında çağırır.
    CLI output is always UTF-8: redirected output on Windows otherwise uses the locale code page and crashes on
    "→", Chinese or Arabic text. Every CLI main() calls this first."""
    for akis in (sys.stdout, sys.stderr):
        kodlama = (getattr(akis, "encoding", None) or "").lower().replace("-", "").replace("_", "")
        if kodlama != "utf8" and hasattr(akis, "reconfigure"):
            akis.reconfigure(encoding="utf-8", errors="replace")

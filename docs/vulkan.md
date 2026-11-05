# Vulkan engine (AMD, Intel, NVIDIA) / Vulkan motoru

## Integrated graphics: RAM / Dahili (gömülü) kart: RAM

An integrated GPU (for example Intel HD/UHD Graphics) has no memory of its own: the model and the engine's buffers live
in system RAM. On a dedicated card the same data sits in the card's memory.

**With integrated graphics the engine uses up to about 8 GB of RAM** (measured: 8.0 GB while reading, 6.5 GB while
designing a voice). On a computer with 8 GB of RAM in total this may not be enough together with Windows and other
programs (not tested on such a machine). Generation is also much slower: the same two-line reading took 446 s on the
integrated Intel HD Graphics 630 and 110 s on a GTX 1050 Ti (both Vulkan, first reading of the voice).

**Dahili kartla üretimde motor en çok yaklaşık 8 GB RAM kullanır** (ölçüm: okumada 8,0 GB, ses tasarımında 6,5 GB).
Toplam 8 GB RAM'li bilgisayarda Windows ve diğer programlarla birlikte yetmeyebilir (böyle bir makinede denenmedi).
Üretim de çok daha yavaştır: aynı iki satırlık okuma dahili Intel HD Graphics 630'da 446 sn, GTX 1050 Ti'de 110 sn
sürdü (ikisi de Vulkan, sesin ilk okuması).

Measurement / Ölçüm: Intel HD Graphics 630, 16 GB RAM, Windows 10, Vulkan AVX2 build, first reading of the voice
(reference not cached yet). "Engine peak RAM" is the engine process's peak working set as reported by Windows;
"lowest free RAM" is free memory of the whole system (Windows and background programs included), sampled every 5 s.
/ "Motor tepe RAM" Windows'un bildirdiği motor sürecinin en yüksek çalışma kümesi; "en az boş RAM" bütün sistemin boş
belleği (Windows ve arka plan programları dahil), 5 sn'de bir örnek.

| Job / İş | Engine peak RAM / Motor tepe RAM | Lowest free RAM / En az boş RAM | Time / Süre | Audio / Ses |
|---|---|---|---|---|
| Reading, 2 lines / Okuma, 2 satır | 8,001 MB | 2,561 MB (10,540 MB before start / başlamadan önce) | 446 s | 9.2 s |
| Voice design, 30 s text / Ses tasarımı, 30 sn metin | 6,506 MB | 3,907 MB | 902 s | 26.9 s |

Windows also counted more committed memory for the engine than it kept in RAM (peak private bytes 16,050 MB in the
reading above). Committed memory must fit within RAM plus the page file (the Windows commit limit), so leave the page
file on (the Windows default); with it turned off the engine may run out of memory (not tested).
/ Windows motor için RAM'de tuttuğundan fazla ayrılmış bellek saydı (yukarıdaki okumada en çok 16.050 MB). Ayrılmış
bellek RAM ile sayfa dosyasının toplamına sığmalıdır (Windows'un ayırma sınırı); sayfa dosyasını açık bırakın (Windows
varsayılanı), kapalıyken bellek yetmeyebilir (denenmedi).

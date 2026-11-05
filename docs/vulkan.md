# Vulkan engine (AMD, Intel, NVIDIA) / Vulkan motoru

## Integrated graphics: RAM / Dahili (gömülü) kart: RAM

An integrated GPU (for example Intel HD/UHD Graphics) has no memory of its own: the model and the engine's buffers live
in system RAM. On a dedicated card the same data sits in the card's memory.

**With integrated graphics the engine uses about 8 GB of RAM.** On a computer with 8 GB of RAM in total this may not
be enough together with Windows and other programs (not tested on such a machine). Generation is also much slower than
on a dedicated card.

Dahili kartla üretimde motor yaklaşık 8 GB RAM kullanır. Toplam 8 GB RAM'li bilgisayarda Windows ve diğer programlarla
birlikte yetmeyebilir (böyle bir makinede denenmedi). Üretim ayrı ekran kartına göre çok daha yavaştır.

Measurement (Intel HD Graphics 630, 16 GB RAM, Windows 10, Vulkan engine v0.3.1, AVX2 build, first reading with an
empty reference cache; the engine's peak working set as reported by Windows, sampled every 5 s):

| Job | Engine peak RAM | Lowest free RAM | Time | Audio |
|---|---|---|---|---|
| Reading, 2 lines | 8,001 MB | 2,561 MB (10,540 MB before start) | 446 s | 9.2 s |
| Voice design, 30 s text | 6,506 MB | 3,907 MB | 902 s | 26.9 s |

The engine also reserves more virtual memory than it keeps in RAM (peak private bytes 16,050 MB in the reading above);
this has to fit in RAM plus the page file (on by default in Windows). With the page file turned off the engine may
not have enough memory (not tested).

[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · **Dansk** · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Tyrkisk stemmedesign med VoxCPM2 på en GPU med 4 GB.** Beskriv en stemme på engelsk, lad modellen skabe den, vælg
den variant, du kan lide, og læs derefter en hvilken som helst tyrkisk tekst op med den stemme. Projektet indeholder et
installationsprogram med én kommando, en patchet [audio.cpp](https://github.com/0xShug0/audio.cpp)-motor, der kan køre på
et GTX 1050 Ti (4 GB), en lille lokal webbrugerflade og fjorten færdige syntetiske stemmer: syv tyrkiske og syv
fortællere med engelsk, fransk, tysk, spansk, russisk, kinesisk og japansk som modersmål.

- Appen læser op på 30 sprog; brugerfladen findes også på 30 sprog.
- 14 færdige stemmer: 7 tyrkiske plus én hver på engelsk, fransk, tysk, spansk, russisk, kinesisk og japansk.
- Webbrugerflade (v0.2.0): hvert variantkort har to stemmer, den rå designstemme og den stemme, du hører fremover; en
  læseliste med en stemmemenu; omdøb, skjul eller slet stemmer; kladder til de tekster, du læser op. Se
  "Webbrugerflade" under "Brug".

[Sådan passer det i 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Installationsvejledning til AI-agenter](AGENTS.md) · [Ansvarlig brug](ETHICS.md)

> De medfølgende stemmer er syntetiske og designet ud fra en tekstbeskrivelse. Afsnittet om stemmekloning er kun til din
> egen stemme eller en stemme, der bruges med ejerens udtrykkelige tilladelse; brugerfladen beder dig bekræfte denne
> tilladelse. Efterligning, svindel og vildledning er forbudt. Mærk det, du genererer, som AI-genereret. Se
> [ETHICS.md](ETHICS.md).

## 30 sprog

Vi lavede én dokumentarvideo om Kappadokien på 8 sprog: tyrkisk, engelsk, fransk, tysk, spansk, russisk, kinesisk og
japansk. Hvert sprog har sin egen **fortæller med sproget som modersmål**, designet med VoxCPM2 ud fra en engelsk
beskrivelse. Det hele blev genereret helt lokalt på et GTX 1050 Ti med 4 GB og med samme faste kvalitet (16 trin, cfg
2.0). De syv fortællere følger med her, sammen med deres prompt, designtekst, seed og referenceoptagelse.

| Kode | Sprog | Stemme | Lyt | Video |
|---|---|---|---|---|
| `tr` | Tyrkisk | `hazir/belgesel_hanim` (og 6 til) | [eksempel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Engelsk | `hazir/anlatici_en` | [eksempel](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Fransk | `hazir/anlatici_fr` | [eksempel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Tysk | `hazir/anlatici_de` | [eksempel](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Spansk | `hazir/anlatici_es` | [eksempel](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Russisk | `hazir/anlatici_ru` | [eksempel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Kinesisk (mandarin) | `hazir/anlatici_zh` | [eksempel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Japansk | `hazir/anlatici_ja` | [eksempel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Hvorfor sætning for sætning.** VoxCPM2 er ikke stabil ved én lang generering (cirka over 30 sekunder): rytmen bliver
hurtigere, og stemmen kan glide. Her bæres stemmen af en fast referenceoptagelse og et fast seed, og lang tekst læses
med én sætning pr. linje, så klang og stil forbliver de samme fra første til sidste sætning. For andre sprog end tyrkisk
bruges den tyrkiske udtaleordbog ikke. Alle 30 sprog, som VoxCPM2 understøtter, er testet og virker; brug `--dil <code>`
til dem uden en medfølgende stemme. Kommandoer pr. sprog og det, vi har lært undervejs:
[docs/cok_dilli.md](docs/cok_dilli.md). Claude Code-skill til hele designforløbet:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 eksempelprompter at starte fra.** 18 roller (dokumentarfortæller, nyhedsoplæser, reklamestemme, lydbog,
historiefortællende bedstemor, podcastvært, lærer, filmtrailer, meditationsguide, sportskommentator og flere, både
mandlige og kvindelige) på hvert af de 8 sprog. Prompten er på engelsk med talerens nationalitet og modersmålsaccent;
teksten, der læses, mens stemmen skabes, følger med, på det pågældende sprog og tilpasset rollen. Vælg en, lyt til
varianterne, og behold den, du kan lide: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, eller
vælg *Eksempelbeskrivelse* i webbrugerfladen. Fuld liste: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dub dine videoer med din egen stemme.** [DubWorld](https://github.com/alexturkey/dubworld) er vores lokale program til
videodubbing; det installerer dette repository som sin VoxCPM2-stemmemotor. En stemme, du designer her, bruges der med
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Hurtig start (Windows, 3 trin)

1. **Download** koden: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Den færdige motorpakke til dit grafikkort hentes af installationsprogrammet i trin 3:
   NVIDIA → [CUDA-pakke](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan-pakke, eksperimentel](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (har du allerede downloadet en? Tilføj `-HazirZip <path to the zip>` til kommandoen nedenfor).
2. **Udpak** zip-filen, åbn mappen `voxcpm2-turkce-ses-tasarimi-main`, skriv `powershell` i Stifinderens adresselinje,
   og tryk på Enter.
3. **Kør** installationsprogrammet (kræver 64-bit Python 3.10-3.13 og til CUDA en NVIDIA-driver ≥ 570), og dobbeltklik
   derefter på **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: tilføj `-Vulkan` til sidst. Brugerfladen åbner på http://127.0.0.1:8765/.

Motor-zip-filen er ikke et selvstændigt program (dens exe skal bruge modellen og de DLL'er, som installationsprogrammet
sætter op). Detaljer, GPU-liste og almindelige problemer: "Hurtig installation" nedenfor.

## Ubuntu / Linux (NVIDIA CUDA, eksperimentel)

Byg den patchede motor med `bash scripts/kur-linux.sh`, eller brug `Dockerfile.linux` til at bygge og køre i et
Ubuntu 24.04 / CUDA 12.8.1-miljø. Kræver en NVIDIA-GPU og en kompatibel driver; det native installationsprogram skal
også bruge CUDA Toolkit og Python 3.10-3.13. Brugerfladen lytter kun på loopback, også på fjernservere
(SSH-videresendelse). Forudsætninger, kommandoer, valg af arkitektur og valideringens omfang:
[docs/linux.md](docs/linux.md).

## Hurtig start (macOS, Apple Silicon)

Kræver Xcode Command Line Tools (`xcode-select --install`) og [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Installationsprogrammet downloader modellen, bygger den patchede motor med Metal (~1 min) og sætter det hele op under
`~/vox`. Dobbeltklik derefter på **`baslat.command`**. På en MacBook Air M4 16 GB: ~2 s beregning pr. 1 s tale, samme
seed giver byte-identisk lyd, højst ~5,3 GB RAM og ingen termisk nedbremsning over 12 min uafbrudt oplæsning.
Detaljer og målinger: [docs/mac.md](docs/mac.md).

**Native Mac-app (uden Python, Homebrew eller Terminal):** [macos/README.md](macos/README.md). Den indeholder den samme
patchede motor og downloader modellen ved første start; indtil videre bygges den fra kildekoden med Xcode.

## Til Mac-brugere (Apple Silicon)

Der findes også en uafhængig tilpasning, lavet af fællesskabet, til Mac med Apple Silicon, som kører VoxCPM2 med Apples
MLX-framework: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Den udvikles og vedligeholdes af Emre Koç ([@emre-koc](https://github.com/emre-koc)) i hans eget repository, ikke her;
installationstrin og supportspørgsmål hører hjemme der. Tak, Emre, fordi du bragte projektet til Mac!

## Sådan virker det

1. **Stemmedesign.** En engelsk *stemmebeskrivelse* + en *tekst, der læses, mens stemmen skabes* (på stemmens sprog) + et
   antal varianter. Hver variant får sit eget seed; motoren modtager `(description)text` og returnerer én
   designoptagelse pr. seed. Teksten er en kort prøve til at lære stemmen at kende: 1-3 sætninger, højst ~30 s
   (brugerfladen viser estimatet og starter ikke over 33 s); lang tekst hører til i trin 2.
2. **Referencebaseret oplæsning.** Designoptagelsen sendes til **begge** motorindgange (`audio` og `voice_ref`) sammen
   med dens transskription (`reference_text`) og den nye tekst, der skal læses, med samme seed. Stemmen bæres af
   optagelsen, ikke af beskrivelsen, så den glider ikke fra tekst til tekst. Teksten læses sætning for sætning.
3. Kvaliteten er fast: 16 diffusionstrin, CFG 2.0. Seedet er ikke en kvalitetsindstilling.
4. **Ordtider, samme lyd hver gang.** Under oplæsning angiver motoren selv, hvor hvert ord begynder og slutter (patch 0002, ingen ekstra model). Tiderne skrives til `kelimeler.json`, og linjerne beskæres, så mellemrummet mellem linjer svarer til pauseindstillingen. Nøjagtighed i forhold til tvungen justering med CTC (forced alignment, CTC = 100 %): 89,66 % (tyrkisk, 12 stemmer; indstilling `kelime_zamani`, slået til som standard). Med patch 0003 giver samme seed byte-identisk lyd ved hver kørsel.

Den rå designoptagelse er en engangsprøve af stemmen; ingen senere oplæsning lyder præcis som den. Det, du hører i hver
senere oplæsning, er trin 2: designoptagelsen som reference plus variantens eget seed. Derfor udfører webbrugerfladen
trin 2 lige efter designet og viser begge dele på variantkortet.

Motoren er audio.cpp v0.7.2 med vores patch (`patches/`), modellen er VoxCPM2 Q8_0 GGUF. Højeste VRAM-forbrug ≈ 2,8 GB;
omkring 2 s beregning pr. 1 s tale på et GTX 1050 Ti. Detaljer og målinger: [docs/4gb.md](docs/4gb.md).

## Medfølgende stemmer (`hazir_sesler/`)

Alle fjorten er designet ud fra de prompter, der er gemt i deres `ses.json`; ingen er klonet fra en optagelse (kloning
foregår på den separate fane *Stemmekloning*, som kræver samtykke).

| Stemme | Kort beskrivelse | Lyt |
|---|---|---|
| `belgesel_hanim` | Moden kvinde i halvtredserne, dyb og varm alt; rolig dokumentarfortæller | [eksempel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [reference](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Dyb, kraftfuld og mystisk mandlig fortæller | [eksempel](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Erfaren nyhedsoplæser omkring de halvfjerds, rolig og autoritativ | [eksempel](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [reference](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Karismatisk aftennyhedsoplæser i trediverne, fløjlsblød og udtryksfuld | [eksempel](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [reference](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Eventyrheks: dyb, let nasal, listigt sød | [eksempel](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [reference](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Usædvanligt dyb, fyldig og myndig mandlig fortæller | [eksempel](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [reference](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Gammel vis mand, dyb og rungende, en smule mystisk | [eksempel](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Mandlig dokumentarfortæller i halvtredserne med engelsk som modersmål (General American); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Mandlig dokumentarfortæller i halvtredserne med fransk som modersmål (Paris); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Mandlig dokumentarfortæller i halvtredserne med tysk som modersmål (højtysk); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Mandlig dokumentarfortæller i halvtredserne med spansk som modersmål (castiliansk (Madrid)); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Mandlig dokumentarfortæller i halvtredserne med russisk som modersmål (Moskva); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Mandlig dokumentarfortæller i halvtredserne med kinesisk (mandarin) som modersmål (Beijing-putonghua); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Mandlig dokumentarfortæller i halvtredserne med japansk som modersmål (Tokyo-standard); dyb, rolig, varm | [eksempel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ja/referans.flac) |

Hver mappe indeholder: `referans.flac` (tabsfri designoptagelse), `ses.json` (prompt, transskription, designseed,
oplæsningsseed, beskrivelse; `dil` = sprog for fortællerne), `ornek_okuma.mp3` (+ dens tekst). Brug dem direkte:
`--ses hazir/<name>`. Fortællernes referenceoptagelser er korte (5,6-10 s); deres eksempler er de tre første sætninger
af Kappadokien-manuskriptet, klippet ud af den færdige produktionsoplæsning.

## Hurtig installation uden compiler (Windows 10/11, NVIDIA-GPU ≥ 4 GB)

Forudsætninger: NVIDIA-driver ≥ 570 og 64-bit Python 3.10-3.13 (`winget install Python.Python.3.12`). Intet andet:
ingen Visual Studio, intet CUDA-installationsprogram. Usikker på, hvilket grafikkort du har? Kør `nvidia-smi` i
PowerShell: den viser GPU-navn, driverversion og hukommelse. Intet NVIDIA-kort? Se "AMD / Intel" nedenfor.

Med [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Uden Git: klik på **Code → Download ZIP** på denne side, udpak filen, åbn den udpakkede mappe
`voxcpm2-turkce-ses-tasarimi-main`, skriv `powershell` i Stifinderens adresselinje, tryk på Enter, og kør så den sidste
linje ovenfor. Git er kun nødvendig, hvis du bygger fra kildekoden.

`-ExecutionPolicy Bypass` gælder kun for denne ene proces og ændrer ingen systemindstillinger; læs `scripts\kur.ps1`,
før du kører det, som med ethvert installationsscript. Én kommando, ~10 min, ~3,7 GB download, alt verificeret med
sha256: modellen (2,95 GB), CUDA 12.8-runtime-DLL'erne som portable zip-filer (ingen systeminstallation, PATH røres
ikke), den **færdigbyggede motor** fra Releases-siden, en `.venv` med de to Python-pakker, `ayarlar.json` og et
afsluttende GPU-tjek (`KONTROL_OK`). Kør det igen efter en fejl; verificerede filer springes over. Start derefter
webbrugerfladen: dobbeltklik på **`baslat.bat`** i repository-mappen. Den starter brugerfladen og åbner
**http://127.0.0.1:8765/** i din browser, når den er klar; luk det sorte vindue (eller tryk Ctrl+C der) for at stoppe
den. Det samme fra PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
og åbn derefter selv **http://127.0.0.1:8765/** (startet på denne måde åbner brugerfladen ikke browseren; den lytter
kun på localhost).

> **`audiocpp_cli.exe` i release-zip-filen er ikke beregnet til at blive dobbeltklikket.** Det er en
> kommandolinjemotor, der skal have CUDA-DLL'erne og modellen ved siden af sig; `kur.ps1` sætter alt på plads, og
> Python-pakken styrer den. Et dobbeltklik på den viser kun "cudart64_12.dll not found".

**Understøttede GPU'er (release v0.1.1):** native kode til GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86),
RTX 40xx (sm_89) og RTX 50xx (sm_120a); alle andre CUDA-GPU'er fra Pascal og frem kører den indlejrede PTX via driveren
(langsommere første start). Maxwell (GTX 9xx) og ældre understøttes ikke af CUDA 12.8. Testet af os på et GTX 1050 Ti
4 GB (også via Docker Desktop/WSL2 på Windows, kun CLI); målt af @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04
Docker, CUDA 12.8.1 (detaljer i [docs/linux.md](docs/linux.md)). Rapporter fra andre kort modtages gerne i
[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (eksperimentel):** en separat Vulkan-motor-zip (`...-win64-vulkan.zip`, ingen CUDA) installeres med
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Den er kun verificeret på vores NVIDIA-kort via Vulkan-backenden (der kørte den
langsommere end CUDA, men gav samme lyd for samme seed; målingen blev taget, mens disken var optaget af et andet job, så
en ren hastighedssammenligning mangler stadig), og vi har **ikke** selv testet den på AMD- eller Intel-hardware: hvis
du prøver den, så skriv gerne resultatet i Discussions. Med mere end én Vulkan-enhed (integreret + dedikeret) skriver
installationsprogrammet den dedikerede GPU's indeks som `cihaz` i `ayarlar.json`.

**Bemærk:** Vulkan-understøttelsen er i øjeblikket eksperimentel. Den er bygget og testet med succes på et GTX 1050 Ti.
En ekstern bruger (mitra_tr) har desuden rapporteret, at den kører på et AMD 6900 XT. Der er stadig brug for bredere
test på AMD/Intel-kort.

**Fællesskabstest (AMD):** @mitraTR kørte v0.1.1 med Vulkan på et AMD Radeon RX 6900 XT under Windows 11: installation, stemmedesign, oplæsning, webgrænsefladen og testene virkede alle; oplæsningen tog ca. 0,8-0,9 s beregning pr. sekund tale ([rapport i #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Installer i en kort mappe, hvis sti kun indeholder ASCII-tegn (f.eks. `C:\vox`): på Windows kan motoren ikke åbne stier med æ, ø, å eller andre ikke-ASCII-tegn. Alle rapporter indtil nu: [testet hardware](docs/donanim_testleri.md).

### Alternativ: byg motoren fra kildekoden

Kræver Visual Studio 2022 Build Tools med "Desktop development with C++" (inkl. C++ CMake tools), ~7 GB. Derefter:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Det downloader også nvcc, henter kildekoden til audio.cpp v0.7.2, anvender `patches/0001-voxcpm2-4gb-ve-hiz.patch` og
bygger til din GPU (`-Mimari native`, standard; eller fx `-Mimari 61`), ~15-25 min. Hold roden kort (`C:\vox`): nvcc
fejler ved lange stier. Trin for trin med kontroller: [AGENTS.md](AGENTS.md).

### Almindelige installationsproblemer

| Du ser | Hvad det betyder, og hvad du skal gøre |
|---|---|
| `cudart64_12.dll not found` efter dobbeltklik på exe-filen | Motoren er ikke beregnet til at blive startet manuelt. Kør `kur.ps1`-kommandoen ovenfor, og start derefter webbrugerfladen. |
| `64-bit Python 3.10+ bulunamadı` (Python blev ikke fundet) | Installer Python (`winget install Python.Python.3.12`), luk PowerShell, åbn et nyt vindue, og kør den samme kommando igen. |
| `motor ekran kartını görmedi` (motoren kunne ikke se GPU'en) | Opdater NVIDIA-driveren til 570 eller nyere; kontrollér, at `nvidia-smi` kan køre. |
| `indirme başarısız` / `sha256 tutmadı` (download mislykkedes / kontrolsummen passer ikke) | Som regel en afbrudt download. Kør den samme kommando igen; verificerede filer springes over. |
| Bygning fra kildekoden: `nvcc` fejler | Hold installationsroden kort (`-Kok C:\vox`). |
| Siden åbner ikke | Start brugerfladen med `baslat.bat`, eller åbn selv http://127.0.0.1:8765/. Er porten optaget? Ret `"port"` i `ayarlar.json`. |

Problemer? [Discussions (spørgsmål og svar)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) eller et
[installationsissue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
med din GPU, Windows-version, kommandoen og dens sidste linjer.

## Brug

Kommandolinje:
```powershell
# list voices
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# read with a bundled voice (one sentence per line; blank line or "|| paragraf" = longer pause, "|| 0,8" = 0.8 s)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# design a new voice: 3 variants, 3 seeds
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# read with variant 2 of it
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
# design, then read a text with each variant's lasting voice (dinleme.wav in each variant folder)
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt --dinleme @metin.txt
```
Tekstregler: skriv tal med bogstaver, ingen anførselstegn (værktøjet afviser cifre og anførselstegn), én sætning pr.
linje, ≤ 2000 tegn pr. linje. Pause efter en linje: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s,
`|| agir` 1,5 s eller din egen længde `|| 0,8` (0-5 s; markørens cifre er tilladt). `ayarlar/okunus_sozlugu.tsv` retter
udtalen af fremmedord i tyrkisk tekst. Sproget genkendes ud fra teksten (tyrkiske bogstaver, skriftsystem, almindelige
ord; stemmekortets `dil`, hvis det er usikkert; `--dil <code>` er valgfri). I ikke-tyrkisk tekst er apostroffer
tilladt, den tyrkiske ordbog springes over, og cifre afvises stadig. Hvis en oplæsning udskriver
`speed gate: satır [...]`, så lyt til de linjer.

### Webbrugerflade

Kun lokalt (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → åbn selv http://127.0.0.1:8765/ (en anden
port: `--port 8800`), eller dobbeltklik på `baslat.bat`. Stop serveren med Ctrl+C. Tre faner: *Design en stemme*,
*Læs op med denne stemme*, *Stemmekloning*. Den typiske vej: *Design* → lyt til varianterne → *Føj til min læseliste* →
*Læs op med denne stemme* → download. Eller vælg en medfølgende stemme i stemmemenuen, og læs op.

- **Version i sidehovedet.** Et lille, svagt `v0.2.0 · <short commit>` (med `+`, når sporede filer har ændringer, der
  ikke er committet; kun versionen uden git), så skærmbilleder og videoer viser, hvilken version der blev brugt.
- **To stemmer på hvert variantkort.** Øverst, i gråt, *Rå designstemme*: den genereres én gang og bliver aldrig helt
  ens igen. Under den, i en orange ramme, *↻ Det er den stemme, du hører fremover*: designoptagelsen læst tilbage som
  reference med variantens eget seed (vist på kortet). Sådan lyder stemmen i hver senere oplæsning. Herunder står
  *Læs op med denne stemme* og *Føj til min læseliste*. Ét tryk på *Design* klarer begge dele: det designer alle
  varianter og læser derefter din tekst med hver varig stemme; én statuslinje tæller begge faser. Variantmappen får
  `dinleme.wav`. Hvis den oplæsning stopper for tidligt, beholdes designet, og kortet viser en note.
- **Vinduet "Tekst, du vil høre".** I *Design en stemme* indeholder feltet *↻ Tekst, du vil høre* det, som hver varig
  stemme læser op (står det tomt, læses eksempelsætningen). Et klik på feltet åbner læsehæftet i et vindue: linjenumre,
  linjemenu, pausebånd. *OK* skriver teksten og dens pauser tilbage i feltet; *Annuller* eller Esc ændrer intet.
  Oplæsningsfanen beholder sin egen tekst.
- **Læsehæftet.** Én sætning pr. linje. Klik på et linjenummer for at få linjemenuen (flyt op eller ned, flyt til en
  position, dupliker, slet; Alt+↑/↓, Alt+Shift+↓ eller træk i nummeret; Ctrl+Z fortryder tekst og pauser samtidig).
  Klik på det tynde bånd mellem to linjer for at vælge pausen (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, eller
  din egen 0-5 s med tandhjulet); tryk Enter to gange for et afsnit (1 s), og tomme linjer bliver til pausebånd. Mens
  resultatet afspilles, lyser den linje, der læses, op og rulles frem i visningen; *▶ Lyt herfra* i linjemenuen afspiller
  fra den linje. Teksten og dens pauser overlever en genindlæsning af siden (browserens lager).
- **Kladder.** Knappen *📄 Kladder* findes i begge hæfter (oplæsningsfanen og vinduet). Gem den aktuelle tekst med dens
  pauser som en kladde, indlæs en med et klik (Ctrl+Z fortryder), og brug ⋯ til at overskrive, omdøbe eller slette den.
  Kladder gemmes i `sesler/taslaklar.json`, aldrig i repositoryet.
- **Læseliste og stemmemenu.** På et variantkort åbner *Føj til min læseliste* et navnefelt: giv varianten sit eget
  navn, og ✓ tilføjer den. *Navn på generering* bliver stående på alle varianter fra den kørsel. I *Læs op med denne
  stemme* åbner stemmeknappen (flag + navn) stemmemenuen: *Min læseliste* øverst, derefter de medfølgende stemmer med
  flag (brugerfladens sprog først). Hver række har ▶ lyt (den varige stemme, hvis der er en), hjertet (tilføj eller
  fjern) og ⋯; ↑/↓ og Enter vælger, Esc lukker, og den sidste stemme huskes. Listen ligger i
  `sesler/okuma_listesi.json`, uden for repositoryet, og overlever genstarter.
- **Administration af stemmer.** ⋯-menuen (en række i stemmemenuen eller et variantkort) har *Læs op med denne stemme*,
  tilføj til eller fjern fra listen, *Omdøb* (et tomt navn gendanner det oprindelige; *Tilbage til det oprindelige
  navn*), *Slet* for designede stemmer og *Skjul* for medfølgende; begge spørger først. En slettet stemme flyttes til
  `sesler/_cop/`; skjul rører aldrig repositoryets filer. *Skjulte og slettede stemmer (N)* nederst i stemmemenuen har
  *Gendan*. Egne navne og skjulte stemmer gemmes i `sesler/yerel_katman.json`. En omdøbt stemme viser sin oprindelse i
  gråt (*navn på generering · variant N*); ⋯ → *Gå til generering* åbner dens design.
- **Genveje og filer.** Ctrl+Enter (⌘+Enter på Mac) starter *Design* eller *Læs op med denne stemme* på den åbne fane.
  Statuslinjen viser *forløbet / ~i alt* med et estimat, der er lært af tidligere job på din maskine. Den downloadede fil
  får navn efter stemmen og tidspunktet (`Voice_Name_2026-11-02_0152.wav`).

**Stemmekloning (din egen stemme eller en stemme med samtykke).** På fanen *Stemmekloning* i brugerfladen angiver du din
optagelse (wav/mp3/flac/ogg, 5-30 s ren tale anbefales; under 3 s afvises, over 36 s beskæres), dens nøjagtige
transskription og den tekst, der skal læses op. Knappen er deaktiveret, indtil du sætter flueben ved "Denne stemme er
min, eller jeg har ejerens udtrykkelige tilladelse". Optagelsen sendes kun til den lokale server (127.0.0.1), behandles
i en midlertidig mappe sammen med sin referencekodning, og mappen slettes, når jobbet slutter, også hvis det mislykkes;
intet sendes over netværket. Kun det syntetiske resultat beholdes (brugerflade: `sesler/_okumalar/<job>/`, CLI:
`--cikti`). Resultatet er `klon_synthetic.wav` med et "synthetic"-mærke; mærk det som AI-genereret, når du deler det.
CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Ofte stillede spørgsmål

**Model eller motor? Hvad er hvad?** VoxCPM2 (OpenBMB) er *modellen*: det neurale netværk med 2 milliarder parametre,
der omdanner tekst til tale. audio.cpp er *motoren*: det C++/CUDA-program, der kører modellen på din GPU
(`audiocpp_cli.exe`). Vores patch ændrer motoren, ikke modellen: den får VoxCPM2 til at passe i 4 GB og sørger for, at
samme seed giver samme lyd hver gang. Python-pakken i dette repository forbereder kun teksten, kalder motoren og samler
filerne.

**Hvilke GPU'er?** Se "Understøttede GPU'er" ovenfor: NVIDIA fra GTX 10xx og op, 4 GB VRAM eller mere, driver ≥ 570.
Releasen indeholder native kode til sm_61/75/86/89/120a; andre kort fra Pascal og nyere bruger den indlejrede PTX
(langsommere første start). AMD/Intel: eksperimentel Vulkan-zip, `kur.ps1 -Vulkan`; en ekstern bruger har rapporteret,
at den kører på et AMD 6900 XT, men der er stadig brug for bredere test på AMD/Intel (se "AMD / Intel" ovenfor). Kun CPU
(`"backend": "cpu"` i `ayarlar.json`) kører, men er ~6× langsommere end et GTX 1050 Ti (motormåling, 535 s mod 94 s for
48 s tale); det er ikke en understøttet vej.

**Hvor hurtigt?** Målt på et GTX 1050 Ti 4 GB (i7-7700HQ): én designvariant (≈ 25 s optagelse) 55 s; oplæsning ≈ 2 s
beregning pr. 1 s tale (realtidsfaktor 1,9-2,8) efter en engangs referencekodning på ~50 s pr. stemme (gemt i cache på
disken) og 10-20 s modelindlæsning pr. batch; højeste VRAM-forbrug 2,6-2,9 GB. Nyere kort er hurtigere; tal og metode:
[docs/4gb.md](docs/4gb.md).

**Kan den klone en stemme?** Den underliggende VoxCPM2-model kan efterligne en stemme ud fra en referenceoptagelse, og
kloningsafsnittet bruger det. Brug det kun med din egen stemme eller med udtrykkelig tilladelse fra den person, stemmen
tilhører; brugerfladen beder dig bekræfte denne tilladelse. Stemmedesign kræver ingen optagelse: det tager udgangspunkt i
en tekstbeskrivelse på engelsk eller kinesisk, og den "reference", der bruges til oplæsning med en designet stemme, er
modellens egen syntetiske designoptagelse. Efterligning, svindel og vildledning er forbudt. Se [ETHICS.md](ETHICS.md).
Mærk det, du offentliggør, som AI-genereret.

**Hvordan skriver jeg en god stemmebeskrivelse?** På engelsk, 1-3 sætninger: alder og køn, klang (dyb/lys, varm,
nasal, hæs), tone og rolle (rolig dokumentarfortæller, energisk vært), tempo (langsomt, afmålt) og "clean studio
recording, no background noise". Hold det som en beskrivelse, ikke et manuskript; ingen parenteser. Bed om 3-5
varianter, og lyt: seedet ændrer stemmen meget. Brug 1-3 naturlige sætninger på stemmens sprog som skabelsestekst, i den
stemning, du ønsker (højst ~30 s tale). Ved oplæsning: én sætning pr. linje; del lange sætninger op, og skriv tal med
bogstaver.

## Bidrag

Ved du ikke, hvor du skal starte? Disse fire små issues er et godt første skridt:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Prøv det på din GPU, og rapportér grafikkort, driver og tider
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: prøv det eksperimentelle Vulkan-build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Tilføj en sætning til testsættet
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Del en stemme, du har designet, med dens beskrivelse og seed

**Test dit grafikkort, skriv en rapport:** du behøver ikke kunne kode, bare brug [formularen til hardwaretestrapporter](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); der er endnu ingen rapport fra et Intel-grafikkort.

Fælles testsæt: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); guide til brandstemme:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); sådan sender du kode: [CONTRIBUTING.md](CONTRIBUTING.md).
Installationsproblemer: [issue-formular](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); spørgsmål og resultater: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Alle, der deltager, følger [adfærdskodeksen](CODE_OF_CONDUCT.md): vær venlig, og hold feedback til arbejdet.

## Bidragydere

- [@alexturkey](https://github.com/alexturkey): vedligeholder; kode, medfølgende stemmer, dokumentation
- [@cayir21](https://github.com/cayir21): Metal-understøttelse til macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): rettelse af sætningsslut (EOS) ved oplæsning af flere sætninger på CPU-backenden, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): eksperimentel CUDA-installation til Ubuntu/Linux og Docker-understøttelse, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Dit navn hører også til her: et testresultat fra din GPU, en sætning til testsættet, en stemme, du har designet, en
tydelig fejlrapport eller en pull request tæller alle som bidrag. Tak til alle, der prøver det og skriver tilbage.

## Licens og kreditering

Kode og medfølgende stemmer: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Bygget på VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) og GGUF-konverteringen af audio.cpp. Fuld liste: [THIRD_PARTY.md](THIRD_PARTY.md).
Ikke tilknyttet OpenBMB, ModelBest eller audio.cpp-projektet.

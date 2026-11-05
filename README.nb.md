[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · **Norsk** · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Tyrkisk stemmedesign med VoxCPM2 på en GPU med 4 GB.** Beskriv en stemme på engelsk, la modellen lage den, velg
varianten du liker, og les deretter opp hvilken som helst tyrkisk tekst med den stemmen. Prosjektet inneholder et
installasjonsprogram med én kommando, en patchet [audio.cpp](https://github.com/0xShug0/audio.cpp)-motor som får plass
på et GTX 1050 Ti (4 GB), et lite lokalt nettgrensesnitt og fjorten ferdige syntetiske stemmer: sju tyrkiske og sju
fortellere med engelsk, fransk, tysk, spansk, russisk, kinesisk og japansk som morsmål.

- Appen leser opp på 30 språk; grensesnittet finnes også på 30 språk.
- 14 ferdige stemmer: 7 tyrkiske, pluss én hver på engelsk, fransk, tysk, spansk, russisk, kinesisk og japansk.
- Nettgrensesnitt (v0.2.0): hvert variantkort har to stemmer, den rå designstemmen og stemmen du vil høre videre; en
  leseliste med en stemmemeny; gi nytt navn til, skjul eller slett stemmer; utkast for tekstene du leser opp. Se
  "Nettgrensesnitt" under "Bruk".

[Slik får det plass i 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Installasjonsveiledning for KI-agenter](AGENTS.md) · [Ansvarlig bruk](ETHICS.md)

> De medfølgende stemmene er syntetiske og designet ut fra en tekstbeskrivelse. Delen om stemmekloning er bare for din
> egen stemme eller en stemme som brukes med eierens uttrykkelige tillatelse; grensesnittet ber deg bekrefte denne
> tillatelsen. Etterligning, svindel og villedning er forbudt. Merk det du genererer, som KI-generert. Se
> [ETHICS.md](ETHICS.md).

## 30 språk

Vi laget én dokumentarvideo om Kappadokia på 8 språk: tyrkisk, engelsk, fransk, tysk, spansk, russisk, kinesisk og
japansk. Hvert språk har sin egen **forteller med språket som morsmål**, designet med VoxCPM2 ut fra en engelsk
beskrivelse. Alt ble generert helt lokalt på et GTX 1050 Ti med 4 GB, med den samme faste kvaliteten (16 steg, cfg
2.0). De sju fortellerne følger med her, sammen med prompt, designtekst, seed og referanseopptak.

| Kode | Språk | Stemme | Lytt | Video |
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

**Hvorfor setning for setning.** VoxCPM2 er ikke stabil ved én lang generering (omtrent over 30 sekunder): rytmen går
fortere, og stemmen kan drive. Her bæres stemmen av et fast referanseopptak og et fast seed, og lang tekst leses med én
setning per linje, slik at klang og stil er den samme fra første til siste setning. For andre språk enn tyrkisk brukes
ikke den tyrkiske uttaleordboken. Alle de 30 språkene VoxCPM2 støtter, er testet og fungerer; bruk `--dil <code>` for
dem uten en medfølgende stemme. Kommandoer per språk og det vi har lært: [docs/cok_dilli.md](docs/cok_dilli.md).
Claude Code-ferdighet for hele designflyten: [.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 eksempelprompter å starte fra.** 18 roller (dokumentarforteller, nyhetsoppleser, reklamestemme, lydbok,
eventyrfortellende bestemor, podkastvert, lærer, filmtrailer, meditasjonsguide, sportskommentator med flere, både
mannlige og kvinnelige) på hvert av de 8 språkene. Prompten er på engelsk med talerens nasjonalitet og
morsmålsaksent; teksten som leses mens stemmen lages, følger med, på det aktuelle språket og tilpasset rollen. Velg én,
lytt til variantene, og behold den du liker: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`,
eller velg *Eksempelbeskrivelse* i nettgrensesnittet. Full liste: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dubb videoene dine med din egen stemme.** [DubWorld](https://github.com/alexturkey/dubworld) er vårt lokale program
for videodubbing; det installerer dette repositoriet som sin VoxCPM2-stemmemotor. En stemme du designer her, brukes der
med `ses.voxcpm2_ses = "<name>/<variant>"`.

## Hurtigstart (Windows, 3 steg)

1. **Last ned** koden: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Den ferdige motorpakken for skjermkortet ditt hentes av installasjonsprogrammet i steg 3:
   NVIDIA → [CUDA-pakke](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan-pakke, eksperimentell](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (har du allerede lastet ned en? Legg til `-HazirZip <path to the zip>` i kommandoen nedenfor).
2. **Pakk ut** zip-filen, åpne mappen `voxcpm2-turkce-ses-tasarimi-main`, skriv `powershell` i adresselinjen i
   Filutforsker, og trykk Enter.
3. **Kjør** installasjonsprogrammet (krever 64-biters Python 3.10-3.13, og for CUDA en NVIDIA-driver ≥ 570), og
   dobbeltklikk deretter på **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: legg til `-Vulkan` til slutt. Grensesnittet åpnes på http://127.0.0.1:8765/.

Motor-zip-filen er ikke et frittstående program (exe-filen trenger modellen og DLL-ene som installasjonsprogrammet setter
opp). Detaljer, GPU-liste og vanlige problemer: "Hurtiginstallasjon" nedenfor.

## Ubuntu / Linux (NVIDIA CUDA, eksperimentell)

Bygg den patchede motoren med `bash scripts/kur-linux.sh`, eller bruk `Dockerfile.linux` til å bygge og kjøre i et
Ubuntu 24.04 / CUDA 12.8.1-miljø. Krever en NVIDIA-GPU og en kompatibel driver; det native installasjonsprogrammet
trenger i tillegg CUDA Toolkit og Python 3.10-3.13. Grensesnittet lytter bare på loopback, også på eksterne servere
(SSH-videresending). Forutsetninger, kommandoer, valg av arkitektur og hva som er validert: [docs/linux.md](docs/linux.md).

## Hurtigstart (macOS, Apple Silicon)

Krever Xcode Command Line Tools (`xcode-select --install`) og [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Installasjonsprogrammet laster ned modellen, bygger den patchede motoren med Metal (~1 min) og setter opp alt under
`~/vox`. Dobbeltklikk deretter på **`baslat.command`**. På en MacBook Air M4 16 GB: ~2 s beregning per 1 s tale, samme
seed gir byte-identisk lyd, maks ~5,3 GB RAM og ingen termisk struping i løpet av 12 min sammenhengende opplesing.
Detaljer og målinger: [docs/mac.md](docs/mac.md).

**Native Mac-app (uten Python, Homebrew eller Terminal):** [macos/README.md](macos/README.md). Den inneholder den samme
patchede motoren og laster ned modellen ved første oppstart; foreløpig bygges den fra kildekoden med Xcode.

## For Mac-brukere (Apple Silicon)

Det finnes også en uavhengig tilpasning laget av fellesskapet for Mac med Apple Silicon, som kjører VoxCPM2 med Apples
MLX-rammeverk: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Den utvikles og vedlikeholdes av Emre Koç ([@emre-koc](https://github.com/emre-koc)) i hans eget repositorium, ikke her;
installasjonssteg og spørsmål om støtte hører hjemme der. Takk, Emre, for at du tok med prosjektet til Mac!

## Slik fungerer det

1. **Stemmedesign.** En engelsk *stemmebeskrivelse* + en *tekst som leses mens stemmen lages* (på stemmens språk) + et
   antall varianter. Hver variant får sitt eget seed; motoren mottar `(description)text` og returnerer ett designopptak
   per seed. Teksten er en kort prøve for å bli kjent med stemmen: 1-3 setninger, maks ~30 s (grensesnittet viser
   anslaget og starter ikke over 33 s); lang tekst hører hjemme i steg 2.
2. **Referansebasert opplesing.** Designopptaket sendes til **begge** motorinngangene (`audio` og `voice_ref`) sammen
   med transkripsjonen (`reference_text`) og den nye teksten som skal leses, med samme seed. Stemmen bæres av opptaket,
   ikke av beskrivelsen, så den driver ikke fra tekst til tekst. Teksten leses setning for setning.
3. Kvaliteten er fast: 16 diffusjonssteg, CFG 2.0. Seedet er ikke en kvalitetsinnstilling.
4. **Ordtider, samme lyd hver gang.** Under opplesning oppgir motoren selv hvor hvert ord begynner og slutter (patch 0002, ingen ekstra modell). Tidene skrives til `kelimeler.json`, og linjene beskjæres slik at mellomrommet mellom linjer tilsvarer pauseinnstillingen. Nøyaktighet mot tvungen justering med CTC (forced alignment, CTC = 100 %): 89,66 % (tyrkisk, 12 stemmer; innstilling `kelime_zamani`, på som standard). Med patch 0003 gir samme seed byte-identisk lyd ved hver kjøring.

Det rå designopptaket er en engangsprøve av stemmen; ingen senere opplesing høres nøyaktig slik ut. Det du hører i hver
senere opplesing, er steg 2: designopptaket som referanse pluss variantens eget seed. Derfor gjør nettgrensesnittet
steg 2 rett etter designet og viser begge deler på variantkortet.

Motoren er audio.cpp v0.7.2 med vår patch (`patches/`), modellen er VoxCPM2 Q8_0 GGUF. Maks VRAM-bruk ≈ 2,8 GB; omtrent
2 s beregning per 1 s tale på et GTX 1050 Ti. Detaljer og målinger: [docs/4gb.md](docs/4gb.md).

## Medfølgende stemmer (`hazir_sesler/`)

Alle fjorten er designet ut fra promptene som er lagret i deres `ses.json`; ingen er klonet fra et opptak (kloning skjer
i den separate fanen *Stemmekloning*, som krever samtykke).

| Stemme | Kort beskrivelse | Lytt |
|---|---|---|
| `belgesel_hanim` | Moden kvinne i femtiårene, dyp og varm alt; rolig dokumentarforteller | [eksempel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referanse](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Dyp, kraftfull og mystisk mannlig forteller | [eksempel](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referanse](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Erfaren nyhetsoppleser rundt sytti, rolig og autoritativ | [eksempel](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referanse](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Karismatisk kveldsnyhetsoppleser i trettiårene, fløyelsmyk og uttrykksfull | [eksempel](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referanse](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Eventyrheks: dyp, litt nasal, lurt søt | [eksempel](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referanse](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Uvanlig dyp, fyldig og myndig mannlig forteller | [eksempel](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referanse](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Gammel, vis mann, dyp og drønnende, litt mystisk | [eksempel](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referanse](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Mannlig dokumentarforteller i femtiårene med engelsk som morsmål (General American); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Mannlig dokumentarforteller i femtiårene med fransk som morsmål (Paris); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Mannlig dokumentarforteller i femtiårene med tysk som morsmål (høytysk); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Mannlig dokumentarforteller i femtiårene med spansk som morsmål (kastiljansk (Madrid)); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Mannlig dokumentarforteller i femtiårene med russisk som morsmål (Moskva); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Mannlig dokumentarforteller i femtiårene med kinesisk (mandarin) som morsmål (Beijing-putonghua); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Mannlig dokumentarforteller i femtiårene med japansk som morsmål (Tokyo-standard); dyp, rolig, varm | [eksempel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referanse](hazir_sesler/anlatici_ja/referans.flac) |

Hver mappe inneholder: `referans.flac` (tapsfritt designopptak), `ses.json` (prompt, transkripsjon, designseed,
opplesingsseed, beskrivelse; `dil` = språk for fortellerne), `ornek_okuma.mp3` (+ teksten til den). Bruk dem direkte:
`--ses hazir/<name>`. Fortellernes referanseopptak er korte (5,6-10 s); eksemplene deres er de tre første setningene av
Kappadokia-manuset, klippet ut av den ferdige produksjonsopplesingen.

## Hurtiginstallasjon uten kompilator (Windows 10/11, NVIDIA-GPU ≥ 4 GB)

Forutsetninger: NVIDIA-driver ≥ 570 og 64-biters Python 3.10-3.13 (`winget install Python.Python.3.12`). Ikke noe
annet: ingen Visual Studio, ingen CUDA-installasjon. Usikker på hvilket skjermkort du har? Kjør `nvidia-smi` i
PowerShell: det viser GPU-navn, driverversjon og minne. Ikke NVIDIA-kort? Se "AMD / Intel" nedenfor.

Med [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Uten Git: klikk på **Code → Download ZIP** på denne siden, pakk ut filen, åpne den utpakkede mappen
`voxcpm2-turkce-ses-tasarimi-main`, skriv `powershell` i adresselinjen i Filutforsker, trykk Enter, og kjør så den siste
linjen ovenfor. Git trengs bare hvis du bygger fra kildekoden.

`-ExecutionPolicy Bypass` gjelder bare for denne ene prosessen og endrer ingen systeminnstillinger; les
`scripts\kur.ps1` før du kjører det, som med alle installasjonsskript. Én kommando, ~10 min, ~3,7 GB nedlasting, alt
verifisert med sha256: modellen (2,95 GB), CUDA 12.8-kjøretids-DLL-ene som portable zip-filer (ingen systeminstallasjon,
PATH røres ikke), den **ferdigbygde motoren** fra Releases-siden, en `.venv` med de to Python-pakkene, `ayarlar.json`
og en avsluttende GPU-sjekk (`KONTROL_OK`). Kjør det på nytt etter en feil; verifiserte filer hoppes over. Start
deretter nettgrensesnittet: dobbeltklikk på **`baslat.bat`** i repositoriemappen. Den starter grensesnittet og åpner
**http://127.0.0.1:8765/** i nettleseren når det er klart; lukk det svarte vinduet (eller trykk Ctrl+C der) for å stoppe
det. Det samme fra PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
og åpne så **http://127.0.0.1:8765/** selv (startet på denne måten åpner ikke grensesnittet nettleseren; det lytter bare
på localhost).

> **`audiocpp_cli.exe` i release-zip-filen er ikke ment for dobbeltklikk.** Det er en kommandolinjemotor som trenger
> CUDA-DLL-ene og modellen ved siden av seg; `kur.ps1` setter alt på plass, og Python-pakken styrer den. Dobbeltklikker
> du på den, vises bare "cudart64_12.dll not found".

**Støttede GPU-er (release v0.1.1):** native kode for GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) og RTX 50xx (sm_120a); alle andre CUDA-GPU-er fra Pascal og nyere kjører den innebygde PTX-en via driveren
(tregere første oppstart). Maxwell (GTX 9xx) og eldre støttes ikke av CUDA 12.8. Testet av oss på et GTX 1050 Ti 4 GB
(også via Docker Desktop/WSL2 på Windows, bare CLI); målt av @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (detaljer i [docs/linux.md](docs/linux.md)). Rapporter fra andre kort tas gjerne imot i
[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (eksperimentell):** en egen Vulkan-motor-zip (`...-win64-vulkan.zip`, uten CUDA) installeres med
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Den er bare verifisert på vårt NVIDIA-kort via Vulkan-backenden (der gikk den
tregere enn CUDA, men ga samme lyd for samme seed; målingen ble tatt mens disken var opptatt med en annen jobb, så en ren
hastighetssammenligning gjenstår), og vi har **ikke** selv testet den på AMD- eller Intel-maskinvare: prøver du den, så
legg gjerne ut resultatet i Discussions. Med mer enn én Vulkan-enhet (integrert + dedikert) skriver
installasjonsprogrammet indeksen til den dedikerte GPU-en som `cihaz` i `ayarlar.json`.

**Merk:** Vulkan-støtten er foreløpig eksperimentell. Den er bygget og testet med hell på et GTX 1050 Ti. En ekstern
bruker (mitra_tr) har i tillegg rapportert at den kjører på et AMD 6900 XT. Det trengs fortsatt bredere testing på
AMD/Intel-kort.

**Fellesskapstest (AMD):** @mitraTR kjørte v0.1.1 med Vulkan på et AMD Radeon RX 6900 XT under Windows 11: installasjon, stemmedesign, opplesning, nettgrensesnittet og testene fungerte; opplesningen tok omtrent 0,8-0,9 s beregning per sekund tale ([rapport i #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Installer i en kort mappe der stien bare har ASCII-tegn (f.eks. `C:\vox`): på Windows kan motoren ikke åpne stier med æ, ø, å eller andre ikke-ASCII-tegn. Alle rapporter så langt: [testet maskinvare](docs/donanim_testleri.md).

**Merknader om Vulkan:** ordtider finnes foreløpig bare på NVIDIA (CUDA) og Mac; på AMD/Intel lages de ikke før Vulkan-motoren er oppdatert (opplesingen virker likevel). Første oppstart med Vulkan kan ta noen minutter fordi GPU-shaderne kompileres; senere opplesninger går raskere.

### Alternativ: bygg motoren fra kildekoden

Krever Visual Studio 2022 Build Tools med "Desktop development with C++" (inkl. C++ CMake tools), ~7 GB. Deretter:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Dette laster også ned nvcc, henter kildekoden til audio.cpp v0.7.2, legger på `patches/0001-voxcpm2-4gb-ve-hiz.patch`
og bygger for GPU-en din (`-Mimari native`, standard; eller f.eks. `-Mimari 61`), ~15-25 min. Hold rotmappen kort
(`C:\vox`): nvcc feiler på lange stier. Steg for steg med kontroller: [AGENTS.md](AGENTS.md).

### Vanlige installasjonsproblemer

| Du ser | Hva det betyr, hva du gjør |
|---|---|
| `cudart64_12.dll not found` etter dobbeltklikk på exe-filen | Motoren er ikke ment å startes manuelt. Kjør `kur.ps1`-kommandoen ovenfor, og start deretter nettgrensesnittet. |
| `64-bit Python 3.10+ bulunamadı` (Python ble ikke funnet) | Installer Python (`winget install Python.Python.3.12`), lukk PowerShell, åpne et nytt vindu og kjør den samme kommandoen på nytt. |
| `motor ekran kartını görmedi` (motoren så ikke GPU-en) | Oppdater NVIDIA-driveren til 570 eller nyere; sjekk at `nvidia-smi` kjører. |
| `indirme başarısız` / `sha256 tutmadı` (nedlastingen mislyktes / sjekksummen stemmer ikke) | Som regel en avbrutt nedlasting. Kjør den samme kommandoen på nytt; verifiserte filer hoppes over. |
| Bygging fra kildekode: `nvcc` feiler | Hold installasjonsroten kort (`-Kok C:\vox`). |
| Siden åpnes ikke | Start grensesnittet med `baslat.bat`, eller åpne http://127.0.0.1:8765/ selv. Porten opptatt? Endre `"port"` i `ayarlar.json`. |

Problemer? [Discussions (spørsmål og svar)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) eller en
[installasjonssak](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
med GPU, Windows-versjon, kommandoen og de siste linjene den skrev ut.

## Bruk

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
Tekstregler: skriv tall med bokstaver, ingen anførselstegn (verktøyet avviser sifre og anførselstegn), én setning per
linje, ≤ 2000 tegn per linje. Pause etter en linje: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s,
`|| agir` 1,5 s eller din egen lengde `|| 0,8` (0-5 s; sifrene i markøren er tillatt). `ayarlar/okunus_sozlugu.tsv`
retter uttalen av fremmedord i tyrkisk tekst. Språket gjenkjennes ut fra teksten (tyrkiske bokstaver, skriftsystem,
vanlige ord; stemmekortets `dil` ved tvil; `--dil <code>` er valgfritt). I ikke-tyrkisk tekst er apostrofer tillatt, den
tyrkiske ordboken hoppes over, og sifre avvises fortsatt. Skriver en opplesing ut `speed gate: satır [...]`, så lytt
til de linjene.

### Nettgrensesnitt

Bare lokalt (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → åpne http://127.0.0.1:8765/ selv (en annen
port: `--port 8800`), eller dobbeltklikk på `baslat.bat`. Stopp serveren med Ctrl+C. Tre faner: *Lag en stemme*,
*Les opp med denne stemmen*, *Stemmekloning*. Den vanlige veien: *Lag* → lytt til variantene → *Legg til i leselisten
min* → *Les opp med denne stemmen* → last ned. Eller velg en medfølgende stemme i stemmemenyen og les opp.

- **Versjon i toppfeltet.** En liten, svak `v0.2.0 · <short commit>` (med `+` når sporede filer har endringer som ikke
  er committet; bare versjonen uten git), slik at skjermbilder og videoer viser hvilken versjon som ble brukt.
- **To stemmer på hvert variantkort.** Øverst, i grått, *Rå designstemme*: den genereres én gang og blir aldri helt lik
  igjen. Under den, i en oransje ramme, *↻ Dette er stemmen du vil høre videre*: designopptaket lest tilbake som
  referanse med variantens eget seed (vist på kortet). Slik høres stemmen ut i hver senere opplesing. Under den ligger
  *Les opp med denne stemmen* og *Legg til i leselisten min*. Ett trykk på *Lag* gjør begge deler: det designer alle
  variantene og leser deretter teksten din med hver varige stemme; én fremdriftslinje teller begge fasene.
  Variantmappen får `dinleme.wav`. Stopper den opplesingen for tidlig, beholdes designet, og kortet viser en merknad.
- **Vinduet "Tekst du vil høre".** I *Lag en stemme* inneholder feltet *↻ Tekst du vil høre* det hver varige stemme
  leser (står det tomt, leses eksempelsetningen). Klikker du på det, åpnes leseheftet i et vindu: linjenumre, linjemeny,
  pausebånd. *OK* skriver teksten og pausene tilbake i feltet; *Avbryt* eller Esc endrer ingenting. Opplesingsfanen
  beholder sin egen tekst.
- **Leseheftet.** Én setning per linje. Klikk på et linjenummer for linjemenyen (flytt opp eller ned, flytt til en
  posisjon, dupliser, slett; Alt+↑/↓, Alt+Shift+↓ eller dra i nummeret; Ctrl+Z angrer tekst og pauser samtidig). Klikk
  på det tynne båndet mellom to linjer for å velge pausen (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, eller din
  egen 0-5 s med tannhjulet); trykk Enter to ganger for et avsnitt (1 s), og tomme linjer blir til pausebånd. Mens
  resultatet spilles av, lyser linjen som leses, opp og rulles inn i synsfeltet; *▶ Lytt herfra* i linjemenyen spiller
  av fra den linjen. Teksten og pausene overlever en ny innlasting av siden (nettleserens lagring).
- **Utkast.** Knappen *📄 Utkast* finnes i begge leseheftene (opplesingsfanen og vinduet). Lagre den gjeldende teksten
  med pausene som et utkast, last inn et med ett klikk (Ctrl+Z angrer), og bruk ⋯ til å overskrive, gi nytt navn eller
  slette det. Utkast lagres i `sesler/taslaklar.json`, aldri i repositoriet.
- **Leseliste og stemmemeny.** På et variantkort åpner *Legg til i leselisten min* et navnefelt: gi varianten et eget
  navn, og ✓ legger den til. *Navn på genereringen* blir stående på alle variantene fra den kjøringen. I *Les opp med
  denne stemmen* åpner stemmeknappen (flagg + navn) stemmemenyen: *Leselisten min* øverst, deretter de medfølgende
  stemmene med flagg (grensesnittspråket først). Hver rad har ▶ lytt (den varige stemmen når den finnes), hjertet (legg
  til eller fjern) og ⋯; ↑/↓ og Enter velger, Esc lukker, og den siste stemmen huskes. Listen ligger i
  `sesler/okuma_listesi.json`, utenfor repositoriet, og overlever omstarter.
- **Håndtere stemmer.** ⋯-menyen (rad i stemmemenyen eller variantkort) har *Les opp med denne stemmen*, legg til i
  eller fjern fra listen, *Gi nytt navn* (et tomt navn gjenoppretter det opprinnelige; *Tilbake til opprinnelig navn*),
  *Slett* for designede stemmer og *Skjul* for medfølgende; begge spør først. En slettet stemme flyttes til
  `sesler/_cop/`; skjuling rører aldri filene i repositoriet. *Skjulte og slettede stemmer (N)* nederst i stemmemenyen
  har *Gjenopprett*. Egne navn og skjulte stemmer lagres i `sesler/yerel_katman.json`. En stemme med nytt navn viser
  opprinnelsen i grått (*navn på genereringen · variant N*); ⋯ → *Gå til genereringen* åpner designet.
- **Snarveier og filer.** Ctrl+Enter (⌘+Enter på Mac) starter *Lag* eller *Les opp med denne stemmen* i den åpne
  fanen. Fremdriftslinjen viser *medgått / ~totalt*, med et anslag som er lært fra tidligere jobber på maskinen din.
  Nedlastingen får navn etter stemmen og tidspunktet (`Voice_Name_2026-11-02_0152.wav`).

**Stemmekloning (din egen stemme eller en stemme med samtykke).** I fanen *Stemmekloning* i grensesnittet oppgir du
opptaket ditt (wav/mp3/flac/ogg, 5-30 s ren tale anbefales; under 3 s avvises, over 36 s kuttes), den nøyaktige
transkripsjonen og teksten som skal leses. Knappen er deaktivert til du krysser av for "Denne stemmen er min, eller jeg
har eierens uttrykkelige tillatelse". Opptaket går bare til den lokale serveren (127.0.0.1), behandles i en midlertidig
mappe sammen med referansekodingen, og mappen slettes når jobben er ferdig, også når den mislykkes; ingenting sendes over
nettverket. Bare det syntetiske resultatet beholdes (grensesnitt: `sesler/_okumalar/<job>/`, CLI: `--cikti`).
Resultatet er `klon_synthetic.wav` med en "synthetic"-merking; merk det som KI-generert når du deler det. CLI:
`python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Ofte stilte spørsmål

**Modell eller motor? Hva er hva?** VoxCPM2 (OpenBMB) er *modellen*: det nevrale nettverket med 2 milliarder parametere som
gjør tekst om til tale. audio.cpp er *motoren*: C++/CUDA-programmet som kjører modellen på GPU-en din
(`audiocpp_cli.exe`). Patchen vår endrer motoren, ikke modellen: den får VoxCPM2 til å få plass i 4 GB og sørger for at
samme seed gir samme lyd hver gang. Python-pakken i dette repositoriet forbereder bare teksten, kaller motoren og samler
filene.

**Hvilke GPU-er?** Se "Støttede GPU-er" ovenfor: NVIDIA fra GTX 10xx og oppover, 4 GB VRAM eller mer, driver ≥ 570.
Releasen har native kode for sm_61/75/86/89/120a; andre kort fra Pascal og nyere bruker den innebygde PTX-en (tregere
første oppstart). AMD/Intel: eksperimentell Vulkan-zip, `kur.ps1 -Vulkan`; en ekstern bruker har rapportert at den
kjører på et AMD 6900 XT, men det trengs fortsatt bredere testing på AMD/Intel (se "AMD / Intel" ovenfor). Bare CPU
(`"backend": "cpu"` i `ayarlar.json`) fungerer, men er ~6× tregere enn et GTX 1050 Ti (motormåling, 535 s mot 94 s for
48 s tale); det er ikke en støttet vei.

**Hvor raskt?** Målt på et GTX 1050 Ti 4 GB (i7-7700HQ): én designvariant (≈ 25 s opptak) 55 s; opplesing ≈ 2 s
beregning per 1 s tale (sanntidsfaktor 1,9-2,8) etter en engangs referansekoding på ~50 s per stemme (bufret på disk) og
10-20 s modellinnlasting per bunt; maks VRAM-bruk 2,6-2,9 GB. Nyere kort er raskere; tall og metode:
[docs/4gb.md](docs/4gb.md).

**Kan den klone en stemme?** Den underliggende VoxCPM2-modellen kan etterligne en stemme ut fra et referanseopptak, og
kloningsdelen bruker dette. Bruk det bare med din egen stemme eller med uttrykkelig tillatelse fra personen stemmen
tilhører; grensesnittet ber deg bekrefte denne tillatelsen. Stemmedesign krever ikke noe opptak: det tar utgangspunkt i
en tekstbeskrivelse på engelsk eller kinesisk, og "referansen" som brukes til opplesing med en designet stemme, er
modellens eget syntetiske designopptak. Etterligning, svindel og villedning er forbudt. Se [ETHICS.md](ETHICS.md). Merk
det du publiserer, som KI-generert.

**Hvordan skriver jeg en god stemmebeskrivelse?** På engelsk, 1-3 setninger: alder og kjønn, klang (dyp/lys, varm,
nasal, ru), tone og rolle (rolig dokumentarforteller, energisk programleder), tempo (sakte, avmålt) og "clean studio
recording, no background noise". La det være en beskrivelse, ikke et manus; ingen parenteser. Be om 3-5 varianter og
lytt: seedet endrer stemmen mye. Bruk 1-3 naturlige setninger på stemmens språk som tekst når stemmen lages, i den
stemningen du ønsker (maks ~30 s tale). Ved opplesing: én setning per linje; del opp lange setninger, og skriv tall med
bokstaver.

## Bidra

Usikker på hvor du skal begynne? Disse fire små sakene er et godt første steg:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Prøv det på GPU-en din og rapporter kort, driver og tider
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: prøv det eksperimentelle Vulkan-bygget
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Legg til en setning i testsettet
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Del en stemme du har designet, med beskrivelse og seed

**Test skjermkortet ditt, skriv en rapport:** du trenger ikke kunne kode, bare bruk [skjemaet for maskinvaretestrapporter](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); det finnes ennå ingen rapport fra et Intel-skjermkort.

Felles testsett: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); veiledning for merkevarestemme:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); slik sender du kode: [CONTRIBUTING.md](CONTRIBUTING.md).
Installasjonsproblemer: [sakskjema](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); spørsmål og resultater: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Alle som deltar, følger [atferdsreglene](CODE_OF_CONDUCT.md): vær vennlig, og hold tilbakemeldinger til arbeidet.

## Bidragsytere

- [@alexturkey](https://github.com/alexturkey): vedlikeholder; kode, medfølgende stemmer, dokumentasjon
- [@cayir21](https://github.com/cayir21): Metal-støtte for macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): retting av setningsslutt (EOS) ved opplesing av flere setninger på CPU-backenden, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): eksperimentell CUDA-installasjon for Ubuntu/Linux og Docker-støtte, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Navnet ditt hører også hjemme her: et testresultat fra GPU-en din, en setning til testsettet, en stemme du har designet,
en tydelig feilrapport eller en pull request teller alle som bidrag. Takk til alle som prøver det og gir tilbakemelding.

## Lisens og kreditering

Kode og medfølgende stemmer: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Bygget på VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) og GGUF-konverteringen av audio.cpp. Full liste: [THIRD_PARTY.md](THIRD_PARTY.md).
Ikke tilknyttet OpenBMB, ModelBest eller audio.cpp-prosjektet.

[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · **Nederlands** · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Turkse stemontwerpen met VoxCPM2 op een GPU van 4 GB.** Beschrijf een stem in het Engels, laat het model hem maken, kies
de variant die je mooi vindt en lees daarna elke Turkse tekst met die stem. Inclusief een installatieprogramma met één
commando, een gepatchte [audio.cpp](https://github.com/0xShug0/audio.cpp)-engine die past op een GTX 1050 Ti (4 GB), een kleine
lokale webinterface en veertien kant-en-klare synthetische stemmen: zeven Turkse en zeven moedertaalvertellers in het Engels,
Frans, Duits, Spaans, Russisch, Chinees en Japans.

- De app leest in 30 talen; de interface is ook in 30 talen beschikbaar.
- 14 kant-en-klare stemmen: 7 Turkse, plus één in het Engels, Frans, Duits, Spaans, Russisch, Chinees en Japans.
- Webinterface (v0.2.0): elke variantkaart heeft twee stemmen, de ruwe ontwerpstem en de stem die je steeds hoort; een
  leeslijst met een stemmenmenu; stemmen hernoemen, verbergen of verwijderen; concepten voor de teksten die je laat voorlezen. Zie "Webinterface" onder "Gebruik".

[Hoe het in 4 GB past](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Installatiegids voor AI-agents](AGENTS.md) · [Verantwoord gebruik](ETHICS.md)

> De meegeleverde stemmen zijn synthetisch, ontworpen op basis van een tekstbeschrijving. Het onderdeel stemklonen is alleen
> bedoeld voor je eigen stem of een stem die je gebruikt met uitdrukkelijke toestemming van de eigenaar; de interface vraagt
> je die toestemming te bevestigen. Imitatie, fraude en misleiding zijn verboden. Vermeld bij wat je genereert dat het door AI is gemaakt. Zie [ETHICS.md](ETHICS.md).

## 30 talen

We hebben één documentaire over Cappadocië gemaakt in 8 talen: Turks, Engels, Frans, Duits, Spaans, Russisch, Chinees
en Japans. Elke taal heeft een eigen **moedertaalverteller**, met VoxCPM2 ontworpen op basis van een Engelse beschrijving.
Alles is volledig lokaal gegenereerd op een GTX 1050 Ti van 4 GB, met dezelfde vaste kwaliteit (16 stappen, cfg 2.0). De
zeven vertellers worden hier meegeleverd, met hun prompt, ontwerptekst, seed en referentieopname.

| Code | Taal | Stem | Beluisteren | Video |
|---|---|---|---|---|
| `tr` | Turks | `hazir/belgesel_hanim` (en nog 6) | [voorbeeld](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Engels | `hazir/anlatici_en` | [voorbeeld](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Frans | `hazir/anlatici_fr` | [voorbeeld](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Duits | `hazir/anlatici_de` | [voorbeeld](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Spaans | `hazir/anlatici_es` | [voorbeeld](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Russisch | `hazir/anlatici_ru` | [voorbeeld](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Chinees (Mandarijn) | `hazir/anlatici_zh` | [voorbeeld](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Japans | `hazir/anlatici_ja` | [voorbeeld](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Waarom zin voor zin.** VoxCPM2 is niet stabiel bij één lange generatie (ongeveer boven de 30 seconden): het ritme
versnelt en de stem kan afdrijven. Hier wordt de stem gedragen door een vaste referentieopname en seed, en lange tekst wordt
per regel één zin voorgelezen, zodat klankkleur en stijl gelijk blijven van de eerste tot de laatste zin. Voor andere talen
dan het Turks wordt het Turkse uitspraakwoordenboek niet toegepast. Alle 30 talen die VoxCPM2 ondersteunt zijn getest en werken; gebruik
`--dil <code>` voor de talen zonder meegeleverde stem. Commando's per taal en wat we geleerd hebben:
[docs/cok_dilli.md](docs/cok_dilli.md). Claude Code-skill voor de hele ontwerpflow:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 voorbeeldprompts om mee te beginnen.** 18 rollen (documentaireverteller, nieuwslezer, reclamestem, luisterboek,
oma die verhalen vertelt, podcasthost, leraar, filmtrailer, meditatiegids, sportcommentator en meer, mannelijk en
vrouwelijk) in elk van de 8 talen. De prompt is Engels, met de nationaliteit en het moedertaalaccent van de spreker; de tekst
die wordt voorgelezen terwijl de stem wordt gemaakt hoort erbij, in die taal en passend bij de rol. Kies er een, beluister de
varianten en houd de variant die je bevalt: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, of kies
*Voorbeeldbeschrijving* in de webinterface. Volledige lijst: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dub je video's met je eigen stem.** [DubWorld](https://github.com/alexturkey/dubworld) is ons lokale programma voor het
dubben van video's; het installeert deze repository als zijn VoxCPM2-stemengine. Een stem die je hier ontwerpt, gebruik je daar met
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Snel aan de slag (Windows, 3 stappen)

1. **Download** de code: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Het kant-en-klare enginepakket voor jouw kaart haalt het installatieprogramma op in stap 3:
   NVIDIA → [CUDA-pakket](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan-pakket, experimenteel](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (al een gedownload? voeg `-HazirZip <path to the zip>` toe aan het commando hieronder).
2. **Pak** de zip **uit**, open de map `voxcpm2-turkce-ses-tasarimi-main`, typ `powershell` in de adresbalk van Verkenner
   en druk op Enter.
3. **Start** het installatieprogramma (vereist 64-bit Python 3.10-3.13; NVIDIA-driver ≥ 570 voor CUDA) en dubbelklik daarna op **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: voeg `-Vulkan` toe aan het eind. De interface opent op http://127.0.0.1:8765/.

De engine-zip is geen zelfstandige app (de exe heeft het model en de DLL's nodig die het installatieprogramma klaarzet).
Details, GPU-lijst en veelvoorkomende problemen: "Snelle installatie" hieronder.

## Ubuntu / Linux (NVIDIA CUDA, experimenteel)

Bouw de gepatchte engine met `bash scripts/kur-linux.sh`, of gebruik `Dockerfile.linux` om te bouwen en te draaien in een
Ubuntu 24.04 / CUDA 12.8.1-omgeving. Vereist een NVIDIA-GPU en een compatibele driver; het native installatieprogramma heeft
ook de CUDA toolkit en Python 3.10-3.13 nodig. De interface blijft alleen via loopback bereikbaar, ook op externe servers (SSH-forwarding).
Vereisten, commando's, architectuurkeuze en reikwijdte van de validatie: [docs/linux.md](docs/linux.md).

## Snel aan de slag (macOS, Apple Silicon)

Vereist de Xcode Command Line Tools (`xcode-select --install`) en [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Het installatieprogramma downloadt het model, bouwt de gepatchte engine met Metal (~1 min) en zet alles klaar onder `~/vox`.
Dubbelklik daarna op **`baslat.command`**. Op een MacBook Air M4 16 GB: ~2 s rekentijd per 1 s spraak, dezelfde seed geeft
byte-voor-byte identieke audio, piek ~5,3 GB RAM, geen thermische vertraging tijdens 12 min onafgebroken voorlezen. Details
en metingen: [docs/mac.md](docs/mac.md).

**Native Mac-app (zonder Python, Homebrew of Terminal):** [macos/README.md](macos/README.md). Deze bevat dezelfde gepatchte
engine en downloadt het model bij de eerste start; voorlopig wordt hij met Xcode vanuit de broncode gebouwd.

## Voor Mac-gebruikers (Apple Silicon)

Er is ook een onafhankelijke, door de community gemaakte versie voor Macs met Apple Silicon die VoxCPM2 draait met Apples
MLX-framework: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Die wordt ontwikkeld en onderhouden door Emre Koç ([@emre-koc](https://github.com/emre-koc)) in zijn eigen repository, niet
hier; installatiestappen en supportvragen horen daar thuis. Bedankt, Emre, dat je dit project naar de Mac hebt gebracht!

## Hoe het werkt

1. **Stemontwerp.** Een Engelse *stembeschrijving* + een *tekst die wordt voorgelezen terwijl de stem wordt gemaakt* (in de taal van de stem) + een aantal
   varianten. Elke variant krijgt een eigen seed; de engine krijgt `(description)text` en geeft per seed één
   ontwerpopname terug. De tekst is een kort voorbeeld om de stem te leren kennen: 1-2 zinnen, hooguit ~20 s (de interface
   toont de schatting en start niet boven 22 s); lange tekst hoort bij stap 2.
2. **Voorlezen op basis van een referentie.** De ontwerpopname gaat naar **beide** engine-ingangen (`audio` en `voice_ref`),
   samen met de transcriptie (`reference_text`) en de nieuwe voor te lezen tekst, met dezelfde seed. De stem wordt gedragen
   door de opname, niet door de beschrijving, en drijft dus niet af van tekst tot tekst. Tekst wordt zin voor zin voorgelezen.
3. De kwaliteit ligt vast: 16 diffusiestappen, CFG 2.0. De seed is geen kwaliteitsknop.

De ruwe ontwerpopname is een eenmalig voorbeeld van de stem; geen enkele latere voorlezing klinkt precies zo. Wat je bij
elke latere voorlezing hoort, is stap 2: de ontwerpopname als referentie plus de eigen seed van de variant. Daarom voert de
webinterface stap 2 direct na het ontwerp uit en toont hij beide op de variantkaart.

De engine is audio.cpp v0.7.2 met onze patch (`patches/`), het model is VoxCPM2 Q8_0 GGUF. Piek-VRAM ≈ 2,8 GB;
ongeveer 2 s rekentijd per 1 s spraak op een GTX 1050 Ti. Details en metingen: [docs/4gb.md](docs/4gb.md).

## Meegeleverde stemmen (`hazir_sesler/`)

Alle veertien zijn ontworpen op basis van de prompts in hun `ses.json`; geen enkele is gekloond uit een opname (klonen is het
aparte tabblad *Stem klonen*, alleen met toestemming).

| Stem | Korte beschrijving | Beluisteren |
|---|---|---|
| `belgesel_hanim` | Rijpe vrouw van in de vijftig, diepe warme alt; rustige documentaireverteller | [voorbeeld](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referentie](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Diepe, krachtige, mysterieuze mannelijke verteller | [voorbeeld](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referentie](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Ervaren nieuwslezer van rond de zeventig, kalm en gezaghebbend | [voorbeeld](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referentie](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Charismatische presentatrice van het avondnieuws van in de dertig, fluweelzacht en expressief | [voorbeeld](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referentie](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Sprookjesheks: laag, licht nasaal, sluw zoet | [voorbeeld](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referentie](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Uitzonderlijk diepe, volle, gebiedende mannelijke verteller | [voorbeeld](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referentie](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Oude wijze man, diep en galmend, een tikje mysterieus | [voorbeeld](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referentie](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Engelstalige mannelijke documentaireverteller van in de vijftig, moedertaalspreker (General American); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Franstalige mannelijke documentaireverteller van in de vijftig, moedertaalspreker (Parijs); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Duitstalige mannelijke documentaireverteller van in de vijftig, moedertaalspreker (Hochdeutsch); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Spaanstalige mannelijke documentaireverteller van in de vijftig, moedertaalspreker (Castiliaans (Madrid)); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Russischtalige mannelijke documentaireverteller van in de vijftig, moedertaalspreker (Moskou); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Chineestalige (Mandarijn) mannelijke documentaireverteller van in de vijftig, moedertaalspreker (Pekings Putonghua); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Japanstalige mannelijke documentaireverteller van in de vijftig, moedertaalspreker (Tokio-standaard); diep, kalm, warm | [voorbeeld](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referentie](hazir_sesler/anlatici_ja/referans.flac) |

Elke map: `referans.flac` (verliesvrije ontwerpopname), `ses.json` (prompt, transcriptie, ontwerpseed, voorleesseed,
beschrijving; `dil` = taal bij de vertellers), `ornek_okuma.mp3` (+ de bijbehorende tekst). Gebruik ze direct: `--ses hazir/<name>`.
De referentieopnamen van de vertellers zijn kort (5,6-10 s); hun voorbeelden zijn de eerste drie zinnen van het
Cappadocië-script, geknipt uit de volledige productievoorlezing.

## Snelle installatie, zonder compiler (Windows 10/11, NVIDIA-GPU ≥ 4 GB)

Vereisten: NVIDIA-driver ≥ 570 en 64-bit Python 3.10-3.13 (`winget install Python.Python.3.12`). Verder niets:
geen Visual Studio, geen CUDA-installatieprogramma. Weet je niet welke kaart je hebt? Voer `nvidia-smi` uit in PowerShell: het toont
de GPU-naam, de driverversie en het geheugen. Geen NVIDIA-kaart? Zie "AMD / Intel" hieronder.

Met [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Zonder Git: klik op deze pagina op **Code → Download ZIP**, pak het uit, open de uitgepakte map
`voxcpm2-turkce-ses-tasarimi-main`, typ `powershell` in de adresbalk van Verkenner en druk op Enter, en voer daarna de
laatste regel hierboven uit. Git is alleen nodig om vanuit de broncode te bouwen.

`-ExecutionPolicy Bypass` geldt alleen voor dit ene proces en wijzigt geen systeeminstelling; lees `scripts\kur.ps1`
voordat je het uitvoert, zoals bij elk installatiescript. Eén commando, ~10 min, ~3,7 GB downloaden, alles gecontroleerd met sha256: het model (2,95 GB), de CUDA 12.8-runtime-DLL's als
draagbare zips (geen systeeminstallatie, PATH blijft onaangeroerd), de **voorgebouwde engine** van de Releases-pagina, een `.venv` met de twee
Python-pakketten, `ayarlar.json` en een afsluitende GPU-controle (`KONTROL_OK`). Voer het na een fout gewoon opnieuw uit; gecontroleerde
bestanden worden overgeslagen. Start daarna de webinterface: dubbelklik op **`baslat.bat`** in de repomap. Die start de interface en opent
**http://127.0.0.1:8765/** in je browser zodra alles klaar is; sluit het zwarte venster (of druk daarin op Ctrl+C) om te stoppen.
Hetzelfde vanuit PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
open daarna zelf **http://127.0.0.1:8765/** (op deze manier gestart opent de interface de browser niet; hij luistert alleen op
localhost).

> **De `audiocpp_cli.exe` in de release-zip is niet bedoeld om op te dubbelklikken.** Het is een command-line-engine die
> de CUDA-DLL's en het model naast zich nodig heeft; `kur.ps1` zet alles op zijn plek en het Python-pakket stuurt hem aan.
> Dubbelklikken toont alleen "cudart64_12.dll not found".

**Ondersteunde GPU's (release v0.1.1):** native code voor GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) en RTX 50xx (sm_120a); elke andere CUDA-GPU vanaf Pascal draait de ingebouwde PTX via de driver (tragere eerste
start). Maxwell (GTX 9xx) en ouder worden niet ondersteund door CUDA 12.8. Door ons getest op een GTX 1050 Ti 4 GB (ook via Docker Desktop/WSL2 op Windows, alleen CLI); gemeten door @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (details in [docs/linux.md](docs/linux.md)). Resultaten van andere kaarten zijn welkom in [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (experimenteel):** een aparte Vulkan-engine-zip (`...-win64-vulkan.zip`, zonder CUDA) installeer je met
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Hij is alleen geverifieerd op onze NVIDIA-kaart via de Vulkan-backend (daar draaide hij
trager dan CUDA, maar gaf hij met dezelfde seed dezelfde audio; die meting is gedaan terwijl de schijf bezig was met een
andere taak, dus een zuivere snelheidsvergelijking staat nog uit) en we hebben hem zelf **niet** getest op AMD- of
Intel-hardware: probeer je het, plaats dan alsjeblieft het resultaat in Discussions. Met meer dan één Vulkan-apparaat
(geïntegreerd + los) schrijft het installatieprogramma de index van de losse GPU als `cihaz` in `ayarlar.json`.

**Let op:** Vulkan-ondersteuning is op dit moment experimenteel. Ze is met succes gebouwd en getest op een GTX 1050 Ti. Daarnaast heeft een externe gebruiker (mitra_tr) gemeld dat hij het op een AMD 6900 XT heeft gedraaid. Er zijn nog bredere tests op AMD/Intel-kaarten nodig.

### Alternatief: de engine vanuit de broncode bouwen

Vereist Visual Studio 2022 Build Tools met "Desktop development with C++" (incl. C++ CMake tools), ~7 GB. Daarna:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Dit downloadt ook nvcc, haalt de broncode van audio.cpp v0.7.2 op, past `patches/0001-voxcpm2-4gb-ve-hiz.patch` toe en
bouwt voor jouw GPU (`-Mimari native`, standaard; of bijvoorbeeld `-Mimari 61`), ~15-25 min. Houd de hoofdmap kort (`C:\vox`):
nvcc faalt bij lange paden. Stap voor stap met controles: [AGENTS.md](AGENTS.md).

### Veelvoorkomende installatieproblemen

| Wat je ziet | Wat het betekent, wat je doet |
|---|---|
| `cudart64_12.dll not found` na dubbelklikken op de exe | De engine is niet bedoeld om met de hand te starten. Voer het `kur.ps1`-commando hierboven uit en start daarna de webinterface. |
| `64-bit Python 3.10+ bulunamadı` (Python niet gevonden) | Installeer Python (`winget install Python.Python.3.12`), sluit PowerShell, open een nieuw venster en voer hetzelfde commando opnieuw uit. |
| `motor ekran kartını görmedi` (de engine zag de GPU niet) | Werk de NVIDIA-driver bij naar 570 of nieuwer; controleer of `nvidia-smi` werkt. |
| `indirme başarısız` / `sha256 tutmadı` (download mislukt / checksum klopt niet) | Meestal een onderbroken download. Voer hetzelfde commando opnieuw uit; gecontroleerde bestanden worden overgeslagen. |
| Bouwen: `nvcc` faalt | Houd de installatiemap kort (`-Kok C:\vox`). |
| De pagina opent niet | Start de interface met `baslat.bat`, of open zelf http://127.0.0.1:8765/. Poort bezet? Wijzig `"port"` in `ayarlar.json`. |

Problemen? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) of een
[installatie-issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
met je GPU, Windows-versie, het commando en de laatste regels van de uitvoer.

## Gebruik

Command line:
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
Tekstregels: schrijf getallen voluit, geen aanhalingstekens (het hulpmiddel weigert cijfers en aanhalingstekens), één zin per regel,
≤ 2000 tekens per regel. Pauze na een regel: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s, `|| agir` 1,5 s
of een eigen lengte `|| 0,8` (0-5 s; de cijfers van deze markering zijn toegestaan). `ayarlar/okunus_sozlugu.tsv` corrigeert de uitspraak van buitenlandse woorden in Turkse tekst.
De taal wordt uit de tekst afgeleid (Turkse letters, schrift, veelvoorkomende woorden; bij twijfel de `dil` van de stemkaart; `--dil <code>` is optioneel). In niet-Turkse tekst zijn apostrofs toegestaan, wordt het Turkse woordenboek
overgeslagen en worden cijfers nog steeds geweigerd. Toont een voorlezing `speed gate: satır [...]`, beluister die regels dan.

### Webinterface

Alleen lokaal (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → open zelf http://127.0.0.1:8765/
(andere poort: `--port 8800`), of dubbelklik op `baslat.bat`. Stop de server met Ctrl+C. Drie tabbladen: *Ontwerp een stem*,
*Voorlezen met deze stem*, *Stem klonen*. De gebruikelijke route: *Ontwerpen* → beluister de varianten → *Aan mijn leeslijst toevoegen* →
*Voorlezen met deze stem* → downloaden. Of kies een meegeleverde stem in het stemmenmenu en laat voorlezen.

- **Versie in de kop.** Een kleine, vage `v0.2.0 · <short commit>` (met `+` als gevolgde bestanden niet-gecommitte
  wijzigingen hebben; zonder git alleen de versie), zodat screenshots en video's laten zien welke versie gebruikt is.
- **Twee stemmen op elke variantkaart.** Bovenaan, in het grijs, de *Ruwe ontwerpstem*: die wordt één keer gemaakt en komt
  nooit precies zo terug. Daaronder, in een oranje kader, *↻ Dit is de stem die je steeds hoort*: de ontwerpopname opnieuw
  voorgelezen als referentie met de eigen seed van de variant (die op de kaart staat). Zo klinkt de stem bij elke latere voorlezing.
  Daaronder staan *Voorlezen met deze stem* en *Aan mijn leeslijst toevoegen*. Eén druk op *Ontwerpen* doet beide: het ontwerpt alle
  varianten en leest daarna je tekst voor met elke blijvende stem; één voortgangsbalk telt beide fasen. De variantmap
  krijgt `dinleme.wav`. Stopt die voorlezing voortijdig, dan blijft het ontwerp bewaard en toont de kaart een melding.
- **Het venster "Tekst die je wilt horen".** In *Ontwerp een stem* bevat het vak *↻ Tekst die je wilt horen* wat elke blijvende
  stem voorleest (leeg gelaten wordt de voorbeeldzin voorgelezen). Klik erop en het voorleesschrift opent in een venster: regelnummers,
  regelmenu, pauzebanden. *OK* schrijft de tekst en de pauzes terug in het vak; *Annuleren* of Esc verandert niets. Het
  voorleestabblad houdt zijn eigen tekst.
- **Het voorleesschrift.** Eén zin per regel. Klik op een regelnummer voor het regelmenu (omhoog of omlaag, naar een
  positie verplaatsen, dupliceren, verwijderen; Alt+↑/↓, Alt+Shift+↓, of slepen aan het nummer; Ctrl+Z maakt tekst en pauzes samen ongedaan).
  Klik op de dunne band tussen twee regels om de pauze te kiezen (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, of een
  eigen 0-5 s via het tandwiel); druk twee keer op Enter voor een alinea (1 s), en lege regels worden pauzebanden. Terwijl het resultaat
  speelt, licht de regel die wordt voorgelezen op en scrolt hij in beeld; *▶ Vanaf hier beluisteren* in het regelmenu speelt vanaf die regel af.
  De tekst en de pauzes blijven bewaard na het herladen van de pagina (browseropslag).
- **Concepten.** De knop *📄 Concepten* zit in beide schriften (voorleestabblad en venster). Sla de huidige tekst met de
  pauzes op als concept, laad er een met één klik (Ctrl+Z maakt ongedaan) en gebruik ⋯ om het te overschrijven, te hernoemen of te verwijderen. Concepten worden
  opgeslagen in `sesler/taslaklar.json`, nooit in de repository.
- **Leeslijst en stemmenmenu.** Op een variantkaart opent *Aan mijn leeslijst toevoegen* een naamvak: geef de variant een
  eigen naam en ✓ voegt hem toe. De *Naam van de generatie* blijft op elke variant van die run staan. In *Voorlezen met deze stem* opent de
  stemknop (vlag + naam) het stemmenmenu: bovenaan *Mijn leeslijst*, daarna de meegeleverde stemmen met vlaggen (interfacetaal
  eerst). Elke rij heeft ▶ beluisteren (de blijvende stem als die er is), het hartje (toevoegen of verwijderen) en ⋯; ↑/↓ en
  Enter kiezen, Esc sluit, de laatste stem wordt onthouden. De lijst staat in `sesler/okuma_listesi.json`, buiten de
  repository, en blijft bewaard na een herstart.
- **Stemmen beheren.** Het ⋯-menu (rij in het stemmenmenu of variantkaart) bevat *Voorlezen met deze stem*, toevoegen aan of verwijderen uit de
  lijst, *Hernoemen* (een lege naam herstelt de oorspronkelijke; *Terug naar oorspronkelijke naam*), *Verwijderen* voor ontworpen stemmen en *Verbergen*
  voor meegeleverde; beide vragen eerst om bevestiging. Een verwijderde stem gaat naar `sesler/_cop/`; verbergen raakt nooit repositorybestanden aan.
  *Verborgen en verwijderde stemmen (N)* onderaan het stemmenmenu heeft *Terugzetten*. Eigen namen en verborgen stemmen worden bewaard
  in `sesler/yerel_katman.json`. Een hernoemde stem toont zijn herkomst in het grijs (*naam van de generatie · variant N*); ⋯ → *Naar de
  generatie* opent het ontwerp ervan.
- **Sneltoetsen en bestanden.** Ctrl+Enter (⌘+Enter op de Mac) start *Ontwerpen* of *Voorlezen met deze stem* op het open tabblad. De
  voortgangsbalk toont *verstreken / ~totaal*, met een schatting die is geleerd van eerdere taken op jouw computer. De download krijgt de naam
  van de stem en het tijdstip (`Voice_Name_2026-11-02_0152.wav`).

**Stem klonen (je eigen stem of een stem met toestemming).** Geef in het tabblad *Stem klonen* van de interface je opname op (wav/mp3/flac/ogg, 5-30 s heldere spraak aanbevolen; korter dan 3 s wordt geweigerd, langer dan 36 s wordt ingekort), de exacte transcriptie ervan en de tekst die moet worden voorgelezen. De knop blijft uitgeschakeld tot je "Deze stem is van mij of ik heb uitdrukkelijke toestemming van de eigenaar" aanvinkt. De opname gaat alleen naar de lokale server (127.0.0.1), wordt verwerkt in een tijdelijke map samen met de referentiecodering ervan, en die map wordt verwijderd als de taak klaar is, ook als die mislukt; er wordt niets over het netwerk verstuurd. Alleen de synthetische uitvoer wordt bewaard (interface: `sesler/_okumalar/<job>/`, CLI: `--cikti`). De uitvoer is `klon_synthetic.wav` met een tag "synthetic"; vermeld bij het delen dat hij door AI is gegenereerd. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Veelgestelde vragen

**Model of engine? Wat is wat?** VoxCPM2 (OpenBMB) is het *model*: het netwerk met 2 miljard parameters dat tekst omzet
in spraak. audio.cpp is de *engine*: het C++/CUDA-programma dat het model op je GPU draait (`audiocpp_cli.exe`). Onze
patch verandert de engine, niet het model: VoxCPM2 past er daardoor in 4 GB en dezelfde seed geeft elke keer dezelfde
audio. Het Python-pakket in deze repo bereidt alleen de tekst voor, roept de engine aan en verzamelt de bestanden.

**Welke GPU's?** Zie "Ondersteunde GPU's" hierboven: NVIDIA vanaf GTX 10xx, 4 GB VRAM of meer, driver ≥ 570. De release bevat
native code voor sm_61/75/86/89/120a; andere kaarten vanaf Pascal gebruiken de ingebouwde PTX (tragere eerste start). AMD/Intel:
experimentele Vulkan-zip, `kur.ps1 -Vulkan`; een externe gebruiker heeft gemeld dat hij hem op een AMD 6900 XT heeft gedraaid, maar bredere
tests op AMD/Intel zijn nog nodig (zie "AMD / Intel" hierboven). Alleen CPU (`"backend": "cpu"` in `ayarlar.json`) werkt, maar is
~6× trager dan een GTX 1050 Ti (enginemeting, 535 s tegenover 94 s voor 48 s spraak); geen ondersteunde route.

**Hoe snel?** Gemeten op een GTX 1050 Ti 4 GB (i7-7700HQ): één ontwerpvariant (opname van ≈ 25 s) 55 s; voorlezen ≈ 2 s
rekentijd per 1 s spraak (real-time factor 1,9-2,8) na een eenmalige referentiecodering van ~50 s per stem (gecachet op
schijf) en 10-20 s laadtijd van het model per batch; piek-VRAM 2,6-2,9 GB. Nieuwere kaarten zijn sneller; cijfers en methode:
[docs/4gb.md](docs/4gb.md).

**Kan het een stem klonen?** Het onderliggende VoxCPM2-model kan een stem nabootsen op basis van een referentieopname, en het
onderdeel klonen maakt daar gebruik van. Gebruik het alleen met je eigen stem of met uitdrukkelijke toestemming van degene van wie de stem is; de
interface vraagt je die toestemming te bevestigen. Stemontwerp heeft geen opname nodig: het begint bij een tekstbeschrijving in het Engels of Chinees, en
de "referentie" die wordt gebruikt om met een ontworpen stem voor te lezen, is de eigen synthetische ontwerpopname van het model. Imitatie, fraude
en misleiding zijn verboden. Zie [ETHICS.md](ETHICS.md). Vermeld bij wat je publiceert dat het door AI is gegenereerd.

**Hoe schrijf ik een goede stembeschrijving?** In het Engels, 1-3 zinnen: leeftijd en geslacht, klankkleur (diep/helder, warm,
nasaal, schor), toon en rol (rustige documentaireverteller, energieke presentator), tempo (langzaam, afgemeten) en
"clean studio recording, no background noise". Houd het bij een beschrijving, geen script; geen haakjes. Vraag om 3-5
varianten en luister: de seed verandert de stem flink. Gebruik voor de aanmaaktekst 1-2 natuurlijke zinnen in de taal van de stem, in de
sfeer die je wilt (hooguit ~20 s spraak). Bij het voorlezen één zin per regel; splits lange zinnen en schrijf getallen voluit.

## Bijdragen

Weet je niet waar je moet beginnen? Deze vier kleine issues zijn een goede eerste stap:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Probeer het op je GPU en meld de kaart, de driver en de tijden
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: probeer de experimentele Vulkan-build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Voeg een zin toe aan de testset
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Deel een stem die je hebt ontworpen, met de beschrijving en de seed

Gedeelde testset: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); gids voor een merkstem:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); hoe je code instuurt: [CONTRIBUTING.md](CONTRIBUTING.md).
Installatieproblemen: [issueformulier](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); vragen en resultaten: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Iedereen die meedoet, volgt de [gedragscode](CODE_OF_CONDUCT.md): wees vriendelijk en houd feedback bij het werk.

## Bijdragers

- [@alexturkey](https://github.com/alexturkey): maintainer; code, meegeleverde stemmen, documentatie
- [@cayir21](https://github.com/cayir21): Metal-ondersteuning voor macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): fix voor het einde van de zin (EOS) bij het voorlezen van meerdere zinnen op de CPU-backend, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): experimentele CUDA-installatie voor Ubuntu/Linux en Docker-ondersteuning, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Ook jouw naam hoort hier: een testresultaat van je GPU, een zin voor de testset, een stem die je hebt ontworpen, een duidelijke
bugmelding of een pull request tellen allemaal als bijdrage. Dank aan iedereen die het uitprobeert en van zich laat horen.

## Licentie en credits

Code en meegeleverde stemmen: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Gebouwd op VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) en de GGUF-conversie van audio.cpp. Volledige lijst: [THIRD_PARTY.md](THIRD_PARTY.md).
Niet verbonden aan OpenBMB, ModelBest of het audio.cpp-project.

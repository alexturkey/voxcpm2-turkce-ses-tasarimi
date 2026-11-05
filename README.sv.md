[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · **Svenska** · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Turkisk röstdesign med VoxCPM2 på ett grafikkort med 4 GB.** Beskriv en röst på engelska, låt modellen skapa den,
välj den variant du gillar och läs sedan upp vilken turkisk text som helst med den rösten. Projektet innehåller ett
installationsprogram med ett enda kommando, en patchad [audio.cpp](https://github.com/0xShug0/audio.cpp)-motor som ryms
på ett GTX 1050 Ti (4 GB), ett litet lokalt webbgränssnitt och fjorton färdiga syntetiska röster: sju turkiska och sju
berättare med engelska, franska, tyska, spanska, ryska, kinesiska och japanska som modersmål.

- Appen läser upp på 30 språk; gränssnittet finns också på 30 språk.
- 14 färdiga röster: 7 turkiska plus en vardera på engelska, franska, tyska, spanska, ryska, kinesiska och japanska.
- Webbgränssnitt (v0.2.0): varje variantkort har två röster, den råa designrösten och rösten du kommer att fortsätta
  höra; en läslista med en röstmeny; byt namn på, dölj eller ta bort röster; utkast för texterna du läser upp. Se
  "Webbgränssnitt" under "Användning".

[Så ryms det i 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Installationsguide för AI-agenter](AGENTS.md) · [Ansvarsfull användning](ETHICS.md)

> De medföljande rösterna är syntetiska och designade utifrån en textbeskrivning. Avsnittet om röstkloning gäller bara
> din egen röst eller en röst som används med ägarens uttryckliga tillstånd; gränssnittet ber dig bekräfta detta
> tillstånd. Imitation, bedrägeri och vilseledning är förbjudet. Märk det du genererar som AI-genererat. Se
> [ETHICS.md](ETHICS.md).

## 30 språk

Vi gjorde en dokumentärvideo om Kappadokien på 8 språk: turkiska, engelska, franska, tyska, spanska, ryska, kinesiska
och japanska. Varje språk har sin egen **berättare med språket som modersmål**, designad med VoxCPM2 utifrån en engelsk
beskrivning. Allt genererades helt lokalt på ett GTX 1050 Ti med 4 GB, med samma fasta kvalitet (16 steg, cfg 2.0). De
sju berättarna följer med här, tillsammans med sin prompt, designtext, seed och referensinspelning.

| Kod | Språk | Röst | Lyssna | Video |
|---|---|---|---|---|
| `tr` | Turkiska | `hazir/belgesel_hanim` (och 6 till) | [exempel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Engelska | `hazir/anlatici_en` | [exempel](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Franska | `hazir/anlatici_fr` | [exempel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Tyska | `hazir/anlatici_de` | [exempel](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Spanska | `hazir/anlatici_es` | [exempel](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Ryska | `hazir/anlatici_ru` | [exempel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Kinesiska (mandarin) | `hazir/anlatici_zh` | [exempel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Japanska | `hazir/anlatici_ja` | [exempel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Varför mening för mening.** VoxCPM2 är inte stabil vid en enda lång generering (ungefär över 30 sekunder): rytmen
blir snabbare och rösten kan glida iväg. Här bärs rösten av en fast referensinspelning och ett fast seed, och lång text
läses med en mening per rad, så att klang och stil förblir desamma från första till sista meningen. För andra språk än
turkiska används inte den turkiska uttalsordlistan. Alla 30 språk som VoxCPM2 stöder har testats och fungerar; använd
`--dil <code>` för dem som saknar en medföljande röst. Kommandon per språk och det vi har lärt oss:
[docs/cok_dilli.md](docs/cok_dilli.md). Claude Code-skill för hela designflödet:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 exempelprompter att utgå från.** 18 roller (dokumentärberättare, nyhetsuppläsare, reklamröst, ljudbok,
sagoberättande mormor, poddvärd, lärare, filmtrailer, meditationsguide, sportkommentator med flera, både manliga och
kvinnliga) på vart och ett av de 8 språken. Prompten är på engelska med talarens nationalitet och modersmålsaccent;
texten som läses medan rösten skapas följer med, på det språket och anpassad till rollen. Välj en, lyssna på
varianterna och behåll den du gillar: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, eller välj
*Exempelbeskrivning* i webbgränssnittet. Hela listan: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dubba dina videor med din egen röst.** [DubWorld](https://github.com/alexturkey/dubworld) är vårt lokala program för
videodubbning; det installerar det här repot som sin VoxCPM2-röstmotor. En röst som du designar här används där med
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Snabbstart (Windows, 3 steg)

1. **Ladda ned** koden: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Det färdiga motorpaketet för ditt grafikkort hämtas av installationsprogrammet i steg 3:
   NVIDIA → [CUDA-paket](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.0/voxcpm2-turkce-ses-tasarimi-motor-v0.3.0-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan-paket, experimentellt](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan.zip)
   (har du redan laddat ned ett? Lägg till `-HazirZip <path to the zip>` i kommandot nedan).
2. **Packa upp** zip-filen, öppna mappen `voxcpm2-turkce-ses-tasarimi-main`, skriv `powershell` i adressfältet i
   Utforskaren och tryck på Enter.
3. **Kör** installationsprogrammet (kräver 64-bitars Python 3.10-3.13 och för CUDA en NVIDIA-drivrutin ≥ 570) och
   dubbelklicka sedan på **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: lägg till `-Vulkan` sist. Gränssnittet öppnas på http://127.0.0.1:8765/.

Motorns zip-fil är inget fristående program (dess exe-fil behöver modellen och de DLL-filer som installationsprogrammet
sätter upp). Detaljer, GPU-lista och vanliga problem: "Snabbinstallation" nedan.

## Ubuntu / Linux (NVIDIA CUDA, experimentellt)

Bygg den patchade motorn med `bash scripts/kur-linux.sh`, eller använd `Dockerfile.linux` för att bygga och köra i en
Ubuntu 24.04 / CUDA 12.8.1-miljö. Kräver ett NVIDIA-grafikkort och en kompatibel drivrutin; det inbyggda
installationsprogrammet behöver dessutom CUDA Toolkit och Python 3.10-3.13. Gränssnittet lyssnar bara på loopback, även
på fjärrservrar (SSH-vidarebefordran). Förutsättningar, kommandon, val av arkitektur och vad som har validerats:
[docs/linux.md](docs/linux.md).

## Snabbstart (macOS, Apple Silicon)

Kräver Xcode Command Line Tools (`xcode-select --install`) och [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Installationsprogrammet laddar ned modellen, bygger den patchade motorn med Metal (~1 min) och sätter upp allt under
`~/vox`. Dubbelklicka sedan på **`baslat.command`**. På en MacBook Air M4 16 GB: ~2 s beräkning per 1 s tal, samma seed
ger byte-identiskt ljud, högst ~5,3 GB RAM och ingen termisk nedsaktning under 12 min oavbruten uppläsning. Detaljer och
mätningar: [docs/mac.md](docs/mac.md).

**Inbyggd Mac-app (utan Python, Homebrew eller Terminal):** [macos/README.md](macos/README.md). Den innehåller samma
patchade motor och laddar ned modellen vid första starten; tills vidare byggs den från källkod med Xcode.

## För Mac-användare (Apple Silicon)

Det finns också en fristående anpassning, gjord av communityn, för Mac med Apple Silicon som kör VoxCPM2 med Apples
MLX-ramverk: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Den utvecklas och underhålls av Emre Koç ([@emre-koc](https://github.com/emre-koc)) i hans eget repo, inte här;
installationssteg och supportfrågor hör hemma där. Tack, Emre, för att du tog projektet till Mac!

## Så fungerar det

1. **Röstdesign.** En engelsk *röstbeskrivning* + en *text som läses medan rösten skapas* (på röstens språk) + ett antal
   varianter. Varje variant får sitt eget seed; motorn tar emot `(description)text` och returnerar en designinspelning
   per seed. Texten är ett kort prov för att lära känna rösten: 1-3 meningar, högst ~30 s (gränssnittet visar
   uppskattningen och startar inte över 33 s); lång text hör hemma i steg 2.
2. **Referensbaserad uppläsning.** Designinspelningen skickas till **båda** motorns ingångar (`audio` och `voice_ref`)
   tillsammans med dess transkription (`reference_text`) och den nya text som ska läsas, med samma seed. Rösten bärs av
   inspelningen, inte av beskrivningen, så den glider inte iväg från text till text. Texten läses mening för mening.
3. Kvaliteten är fast: 16 diffusionssteg, CFG 2.0. Seedet är inte en kvalitetsinställning.
4. **Ordtider, samma ljud varje gång.** Vid uppläsning anger motorn själv var varje ord börjar och slutar (patch 0002, ingen extra modell). Tiderna skrivs till `kelimeler.json` och raderna beskärs så att mellanrummet mellan rader blir lika med pausinställningen. Noggrannhet mot tvingad justering med CTC (forced alignment, CTC = 100 %): 89,66 % (turkiska, 12 röster; inställning `kelime_zamani`, på som standard). Med patch 0003 ger samma seed byte-identiskt ljud vid varje körning.

Den råa designinspelningen är ett engångsprov av rösten; ingen senare uppläsning låter exakt som den. Det du hör i varje
senare uppläsning är steg 2: designinspelningen som referens plus variantens eget seed. Därför gör webbgränssnittet
steg 2 direkt efter designen och visar båda på variantkortet.

Motorn är audio.cpp v0.7.2 med vår patch (`patches/`), modellen är VoxCPM2 Q8_0 GGUF. Högsta VRAM-användning ≈ 2,8 GB;
ungefär 2 s beräkning per 1 s tal på ett GTX 1050 Ti. Detaljer och mätningar: [docs/4gb.md](docs/4gb.md).

## Medföljande röster (`hazir_sesler/`)

Alla fjorton är designade utifrån promptarna som finns sparade i deras `ses.json`; ingen är klonad från en inspelning
(kloning sker på den separata fliken *Röstkloning*, som kräver samtycke).

| Röst | Kort beskrivning | Lyssna |
|---|---|---|
| `belgesel_hanim` | Mogen kvinna i femtioårsåldern, djup och varm alt; lugn dokumentärberättare | [exempel](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referens](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Djup, kraftfull och mystisk manlig berättare | [exempel](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referens](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Erfaren nyhetsuppläsare i sjuttioårsåldern, lugn och auktoritativ | [exempel](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referens](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Karismatisk kvällsnyhetsuppläsare i trettioårsåldern, sammetslen och uttrycksfull | [exempel](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referens](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Sagohäxa: låg, lätt nasal, listigt söt | [exempel](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referens](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Ovanligt djup, fyllig och myndig manlig berättare | [exempel](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referens](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Gammal vis man, djup och mullrande, lite mystisk | [exempel](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referens](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Manlig dokumentärberättare i femtioårsåldern med engelska som modersmål (General American); djup, lugn, varm | [exempel](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Manlig dokumentärberättare i femtioårsåldern med franska som modersmål (Paris); djup, lugn, varm | [exempel](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Manlig dokumentärberättare i femtioårsåldern med tyska som modersmål (högtyska); djup, lugn, varm | [exempel](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Manlig dokumentärberättare i femtioårsåldern med spanska som modersmål (kastilianska (Madrid)); djup, lugn, varm | [exempel](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Manlig dokumentärberättare i femtioårsåldern med ryska som modersmål (Moskva); djup, lugn, varm | [exempel](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Manlig dokumentärberättare i femtioårsåldern med kinesiska (mandarin) som modersmål (Pekings putonghua); djup, lugn, varm | [exempel](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Manlig dokumentärberättare i femtioårsåldern med japanska som modersmål (Tokyo-standard); djup, lugn, varm | [exempel](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referens](hazir_sesler/anlatici_ja/referans.flac) |

Varje mapp innehåller: `referans.flac` (förlustfri designinspelning), `ses.json` (prompt, transkription, designseed,
uppläsningsseed, beskrivning; `dil` = språk för berättarna), `ornek_okuma.mp3` (+ dess text). Använd dem direkt:
`--ses hazir/<name>`. Berättarnas referensinspelningar är korta (5,6-10 s); deras exempel är de tre första meningarna i
Kappadokien-manuset, klippta ur den färdiga produktionsuppläsningen.

## Snabbinstallation utan kompilator (Windows 10/11, NVIDIA-grafikkort ≥ 4 GB)

Förutsättningar: NVIDIA-drivrutin ≥ 570 och 64-bitars Python 3.10-3.13 (`winget install Python.Python.3.12`). Inget
annat: ingen Visual Studio, inget CUDA-installationsprogram. Osäker på vilket grafikkort du har? Kör `nvidia-smi` i
PowerShell: det visar GPU-namn, drivrutinsversion och minne. Inget NVIDIA-kort? Se "AMD / Intel" nedan.

Med [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Utan Git: klicka på **Code → Download ZIP** på den här sidan, packa upp filen, öppna den uppackade mappen
`voxcpm2-turkce-ses-tasarimi-main`, skriv `powershell` i adressfältet i Utforskaren, tryck på Enter och kör sedan den
sista raden ovan. Git behövs bara om du bygger från källkod.

`-ExecutionPolicy Bypass` gäller bara den här enda processen och ändrar inga systeminställningar; läs `scripts\kur.ps1`
innan du kör det, som med alla installationsskript. Ett kommando, ~10 min, ~3,7 GB nedladdning, allt verifierat med
sha256: modellen (2,95 GB), CUDA 12.8-körtids-DLL:erna som portabla zip-filer (ingen systeminstallation, PATH lämnas
orörd), den **förbyggda motorn** från Releases-sidan, en `.venv` med de två Python-paketen, `ayarlar.json` och en
avslutande GPU-kontroll (`KONTROL_OK`). Kör det igen efter ett fel; verifierade filer hoppas över. Starta sedan
webbgränssnittet: dubbelklicka på **`baslat.bat`** i repomappen. Det startar gränssnittet och öppnar
**http://127.0.0.1:8765/** i webbläsaren när det är klart; stäng det svarta fönstret (eller tryck Ctrl+C där) för att
stoppa det. Samma sak från PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
och öppna sedan **http://127.0.0.1:8765/** själv (startat på det här sättet öppnar gränssnittet inte webbläsaren; det
lyssnar bara på localhost).

> **`audiocpp_cli.exe` i release-zip-filen är inte tänkt att dubbelklickas.** Det är en kommandoradsmotor som behöver
> CUDA-DLL:erna och modellen bredvid sig; `kur.ps1` lägger allt på plats och Python-paketet styr den. Dubbelklickar du
> på den visas bara "cudart64_12.dll not found".

**Grafikkort som stöds (release v0.1.1):** inbyggd kod för GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86),
RTX 40xx (sm_89) och RTX 50xx (sm_120a); alla andra CUDA-grafikkort från Pascal och framåt kör den inbäddade PTX-koden
via drivrutinen (långsammare första start). Maxwell (GTX 9xx) och äldre stöds inte av CUDA 12.8. Testat av oss på ett
GTX 1050 Ti 4 GB (även via Docker Desktop/WSL2 på Windows, bara CLI); uppmätt av @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB,
Ubuntu 24.04 Docker, CUDA 12.8.1 (detaljer i [docs/linux.md](docs/linux.md)). Rapporter från andra kort tas gärna emot
i [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (experimentellt):** en separat Vulkan-motor (utan CUDA) installeras med `scripts\kur.ps1 -Kok C:\vox -Vulkan`. Vi har testat den på vårt NVIDIA-kort via Vulkan-backend (där långsammare än CUDA, samma ljud med samma seed; en ren hastighetsjämförelse återstår) och på det integrerade Intel HD Graphics 630 (cirka 35-50 s beräkning per 1 s tal); på AMD har vi **inte** testat den själva: om du provar, lägg resultatet i Discussions. Med fler än en Vulkan-enhet (integrerad + separat) skriver installationsprogrammet det separata grafikkortets index som `cihaz` i `ayarlar.json`.

**Obs:** Vulkan-stödet är för närvarande experimentellt. Det har byggts och testats med lyckat resultat på ett
GTX 1050 Ti. En extern användare (mitra_tr) har dessutom rapporterat att det körs på ett AMD 6900 XT. Bredare tester på
AMD/Intel-kort behövs fortfarande.

**Communitytest (AMD):** @mitraTR körde v0.1.1 med Vulkan på ett AMD Radeon RX 6900 XT under Windows 11: installation, röstdesign, uppläsning, webbgränssnittet och testerna fungerade; uppläsningen tog ungefär 0,8-0,9 s beräkning per sekund tal ([rapport i #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Installera i en kort mapp vars sökväg bara har ASCII-tecken (t.ex. `C:\vox`): på Windows kan motorn inte öppna sökvägar med å, ä, ö eller andra icke-ASCII-tecken. Alla rapporter hittills: [testad hårdvara](docs/donanim_testleri.md).

**Om Vulkan:** sedan motor v0.3.1 fungerar ordtider även på Vulkan. Två paket: `vulkan` kräver en processor med AVX2 (de flesta Intel Core från 2013, AMD från 2015; många Pentium/Celeron saknar det); [`vulkan-uyumlu`](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan-uyumlu.zip) körs på alla 64-bitars x86-processorer, men en rösts första uppläsning tar ungefär 2,2 gånger så lång tid (senare uppläsningar går lika fort). `kur.ps1 -Vulkan` kontrollerar processorn och väljer paketet själv. Med integrerad grafik använder motorn cirka 8 GB RAM under uppläsning. Första starten på Vulkan kan ta några minuter eftersom GPU-shaders kompileras; senare uppläsningar går snabbare. Detaljer: [docs/vulkan.md](docs/vulkan.md).

### Alternativ: bygg motorn från källkod

Kräver Visual Studio 2022 Build Tools med "Desktop development with C++" (inkl. C++ CMake tools), ~7 GB. Sedan:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Det laddar också ned nvcc, hämtar källkoden för audio.cpp v0.7.2, applicerar `patches/0001-voxcpm2-4gb-ve-hiz.patch`
och bygger för ditt grafikkort (`-Mimari native`, standard; eller t.ex. `-Mimari 61`), ~15-25 min. Håll rotmappen kort
(`C:\vox`): nvcc misslyckas med långa sökvägar. Steg för steg med kontroller: [AGENTS.md](AGENTS.md).

### Vanliga installationsproblem

| Du ser | Vad det betyder, vad du ska göra |
|---|---|
| `cudart64_12.dll not found` efter dubbelklick på exe-filen | Motorn är inte tänkt att startas för hand. Kör kommandot `kur.ps1` ovan och starta sedan webbgränssnittet. |
| `64-bit Python 3.10+ bulunamadı` (Python hittades inte) | Installera Python (`winget install Python.Python.3.12`), stäng PowerShell, öppna ett nytt fönster och kör samma kommando igen. |
| `motor ekran kartını görmedi` (motorn såg inte grafikkortet) | Uppdatera NVIDIA-drivrutinen till 570 eller senare; kontrollera att `nvidia-smi` går att köra. |
| `indirme başarısız` / `sha256 tutmadı` (nedladdningen misslyckades / kontrollsumman stämmer inte) | Oftast en avbruten nedladdning. Kör samma kommando igen; verifierade filer hoppas över. |
| Bygge från källkod: `nvcc` misslyckas | Håll installationsroten kort (`-Kok C:\vox`). |
| Sidan öppnas inte | Starta gränssnittet med `baslat.bat`, eller öppna http://127.0.0.1:8765/ själv. Är porten upptagen? Ändra `"port"` i `ayarlar.json`. |

Problem? [Discussions (frågor och svar)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) eller ett
[installationsärende](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
med ditt grafikkort, Windows-version, kommandot och dess sista rader.

## Användning

Kommandorad:
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
Textregler: skriv tal med bokstäver, inga citattecken (verktyget avvisar siffror och citattecken), en mening per rad,
≤ 2000 tecken per rad. Paus efter en rad: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s, `|| agir` 1,5 s
eller en egen längd `|| 0,8` (0-5 s; markörens siffror är tillåtna). `ayarlar/okunus_sozlugu.tsv` rättar uttalet av
främmande ord i turkisk text. Språket känns igen utifrån texten (turkiska bokstäver, skriftsystem, vanliga ord;
röstkortets `dil` vid osäkerhet; `--dil <code>` är valfritt). I icke-turkisk text är apostrofer tillåtna, den turkiska
ordlistan hoppas över och siffror avvisas fortfarande. Om en uppläsning skriver ut `speed gate: satır [...]`, lyssna på
de raderna.

### Webbgränssnitt

Bara lokalt (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → öppna http://127.0.0.1:8765/ själv (en
annan port: `--port 8800`), eller dubbelklicka på `baslat.bat`. Stoppa servern med Ctrl+C. Tre flikar: *Designa en
röst*, *Läs upp med den här rösten*, *Röstkloning*. Den vanliga vägen: *Designa* → lyssna på varianterna → *Lägg till i
min läslista* → *Läs upp med den här rösten* → ladda ned. Eller välj en medföljande röst i röstmenyn och läs upp.

- **Version i sidhuvudet.** En liten, blek `v0.2.0 · <short commit>` (med `+` när spårade filer har ändringar som inte
  är committade; bara versionen utan git), så att skärmbilder och videor visar vilken version som användes.
- **Två röster på varje variantkort.** Överst, i grått, *Rå designröst*: den genereras en gång och blir aldrig exakt
  likadan igen. Under den, i en orange ram, *↻ Det här är rösten du kommer att höra*: designinspelningen uppläst igen
  som referens med variantens eget seed (visas på kortet). Så här låter rösten i varje senare uppläsning. Under den
  finns *Läs upp med den här rösten* och *Lägg till i min läslista*. Ett tryck på *Designa* gör båda: det designar alla
  varianter och läser sedan din text med varje bestående röst; en enda förloppsindikator räknar båda faserna.
  Variantmappen får `dinleme.wav`. Om den uppläsningen avbryts i förtid behålls designen och kortet visar en notering.
- **Fönstret "Text du vill höra".** I *Designa en röst* innehåller rutan *↻ Text du vill höra* det som varje bestående
  röst läser upp (lämnas den tom läses exempelmeningen). Klickar du på den öppnas läshäftet i ett fönster: radnummer,
  radmeny, pausband. *OK* skriver tillbaka texten och dess pauser till rutan; *Avbryt* eller Esc ändrar ingenting.
  Uppläsningsfliken behåller sin egen text.
- **Läshäftet.** En mening per rad. Klicka på ett radnummer för radmenyn (flytta upp eller ned, flytta till en position,
  duplicera, ta bort; Alt+↑/↓, Alt+Shift+↓ eller dra i numret; Ctrl+Z ångrar text och pauser tillsammans). Klicka på
  det tunna bandet mellan två rader för att välja paus (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, eller en egen
  0-5 s med kugghjulet); tryck Enter två gånger för ett stycke (1 s), och tomma rader blir pausband. Medan resultatet
  spelas upp lyser raden som läses upp och rullas in i bild; *▶ Lyssna härifrån* i radmenyn spelar upp från den raden.
  Texten och dess pauser finns kvar efter att sidan laddats om (webbläsarens lagring).
- **Utkast.** Knappen *📄 Utkast* finns i båda häftena (uppläsningsfliken och fönstret). Spara den aktuella texten med
  dess pauser som ett utkast, läs in ett med ett klick (Ctrl+Z ångrar) och använd ⋯ för att skriva över, byta namn på
  eller ta bort det. Utkast sparas i `sesler/taslaklar.json`, aldrig i repot.
- **Läslista och röstmeny.** På ett variantkort öppnar *Lägg till i min läslista* en namnruta: ge varianten ett eget
  namn så lägger ✓ till den. *Namn på genereringen* finns kvar på varje variant från den körningen. I *Läs upp med den
  här rösten* öppnar röstknappen (flagga + namn) röstmenyn: *Min läslista* överst, sedan de medföljande rösterna med
  flaggor (gränssnittets språk först). Varje rad har ▶ lyssna (den bestående rösten när en sådan finns), hjärtat (lägg
  till eller ta bort) och ⋯; ↑/↓ och Enter väljer, Esc stänger, och den senast valda rösten sparas. Listan finns i
  `sesler/okuma_listesi.json`, utanför repot, och finns kvar efter omstarter.
- **Hantera röster.** ⋯-menyn (rad i röstmenyn eller variantkort) har *Läs upp med den här rösten*, lägg till i eller ta
  bort från listan, *Byt namn* (ett tomt namn återställer originalet; *Tillbaka till ursprungligt namn*), *Ta bort* för
  designade röster och *Dölj* för medföljande; båda frågar först. En borttagen röst flyttas till `sesler/_cop/`; att dölja
  rör aldrig repots filer. *Dolda och borttagna röster (N)* längst ned i röstmenyn har *Återställ*. Egna namn och dolda
  röster sparas i `sesler/yerel_katman.json`. En röst med nytt namn visar sitt ursprung i grått (*namn på genereringen ·
  variant N*); ⋯ → *Gå till genereringen* öppnar dess design.
- **Kortkommandon och filer.** Ctrl+Enter (⌘+Enter på Mac) startar *Designa* eller *Läs upp med den här rösten* på den
  öppna fliken. Förloppsindikatorn visar *förfluten / ~total*, med en uppskattning som lärts in från tidigare jobb på
  din dator. Den nedladdade filen namnges efter rösten och tiden (`Voice_Name_2026-11-02_0152.wav`).

**Röstkloning (din egen röst eller en röst med samtycke).** På fliken *Röstkloning* i gränssnittet anger du din
inspelning (wav/mp3/flac/ogg, 5-30 s rent tal rekommenderas; under 3 s avvisas, över 36 s kortas), dess exakta
transkription och texten som ska läsas. Knappen är inaktiverad tills du kryssar i "Den här rösten är min eller jag har
ägarens uttryckliga tillstånd". Inspelningen går bara till den lokala servern (127.0.0.1), bearbetas i en tillfällig mapp
tillsammans med sin referenskodning, och mappen raderas när jobbet är klart, även om det misslyckas; inget skickas över
nätverket. Bara det syntetiska resultatet behålls (gränssnitt: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Resultatet är
`klon_synthetic.wav` med en "synthetic"-märkning; märk det som AI-genererat när du delar det. CLI:
`python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Vanliga frågor

**Modell eller motor? Vad är vad?** VoxCPM2 (OpenBMB) är *modellen*: det neurala nätverket med 2 miljarder parametrar
som omvandlar text till tal. audio.cpp är *motorn*: C++/CUDA-programmet som kör modellen på ditt grafikkort
(`audiocpp_cli.exe`). Vår patch ändrar motorn, inte modellen: den får VoxCPM2 att rymmas i 4 GB och gör att samma seed
ger samma ljud varje gång. Python-paketet i det här repot förbereder bara texten, anropar motorn och samlar ihop filerna.

**Vilka grafikkort?** Se "Grafikkort som stöds" ovan: NVIDIA från GTX 10xx och uppåt, 4 GB VRAM eller mer, drivrutin
≥ 570. Releasen innehåller inbyggd kod för sm_61/75/86/89/120a; andra kort från Pascal och nyare använder den inbäddade
PTX-koden (långsammare första start). AMD/Intel: experimentell Vulkan-zip, `kur.ps1 -Vulkan`; en extern användare har
rapporterat att den körs på ett AMD 6900 XT, men bredare tester på AMD/Intel behövs fortfarande (se "AMD / Intel" ovan).
Endast CPU (`"backend": "cpu"` i `ayarlar.json`) fungerar men är ~6× långsammare än ett GTX 1050 Ti (motormätning,
535 s mot 94 s för 48 s tal); det är ingen väg som stöds.

**Hur snabbt?** Uppmätt på ett GTX 1050 Ti 4 GB (i7-7700HQ): en designvariant (≈ 25 s inspelning) 55 s; uppläsning
≈ 2 s beräkning per 1 s tal (realtidsfaktor 1,9-2,8) efter en engångs referenskodning på ~50 s per röst (cachad på disk)
och 10-20 s modellinläsning per batch; högsta VRAM-användning 2,6-2,9 GB. Nyare kort är snabbare; siffror och metod:
[docs/4gb.md](docs/4gb.md).

**Kan den klona en röst?** Den underliggande VoxCPM2-modellen kan imitera en röst utifrån en referensinspelning, och
kloningsdelen använder det. Använd det bara med din egen röst eller med uttryckligt tillstånd från den person vars röst
det är; gränssnittet ber dig bekräfta detta tillstånd. Röstdesign kräver ingen inspelning: den utgår från en
textbeskrivning på engelska eller kinesiska, och den "referens" som används vid uppläsning med en designad röst är
modellens egen syntetiska designinspelning. Imitation, bedrägeri och vilseledning är förbjudet. Se
[ETHICS.md](ETHICS.md). Märk det du publicerar som AI-genererat.

**Hur skriver jag en bra röstbeskrivning?** På engelska, 1-3 meningar: ålder och kön, klangfärg (djup/ljus, varm,
nasal, raspig), ton och roll (lugn dokumentärberättare, energisk programledare), tempo (långsamt, avvägt) och "clean
studio recording, no background noise". Håll det till en beskrivning, inte ett manus; inga parenteser. Be om 3-5
varianter och lyssna: seedet ändrar rösten mycket. Som text när rösten skapas använder du 1-3 naturliga meningar på
röstens språk, i den stämning du vill ha (högst ~30 s tal). Vid uppläsning: en mening per rad; dela upp långa meningar
och skriv tal med bokstäver.

## Bidra

Osäker på var du ska börja? De här fyra små ärendena är ett bra första steg:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Prova på ditt grafikkort och rapportera kort, drivrutin och tider
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: prova det experimentella Vulkan-bygget
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Lägg till en mening i testuppsättningen
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Dela en röst du har designat, med beskrivning och seed

**Testa ditt grafikkort, skriv en rapport:** du behöver inte kunna koda, bara använda [formuläret för hårdvarutestrapporter](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); det finns ännu ingen rapport från ett Intel-grafikkort.

Gemensam testuppsättning: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); guide för varumärkesröst:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); så skickar du kod: [CONTRIBUTING.md](CONTRIBUTING.md).
Installationsproblem: [ärendeformulär](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); frågor och resultat: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Alla som deltar följer vår [uppförandekod](CODE_OF_CONDUCT.md): var vänlig och håll återkopplingen till arbetet.

## Bidragsgivare

- [@alexturkey](https://github.com/alexturkey): förvaltare; kod, medföljande röster, dokumentation
- [@cayir21](https://github.com/cayir21): Metal-stöd för macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): rättning av meningsslut (EOS) vid uppläsning av flera meningar på CPU-backenden, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): experimentell CUDA-installation för Ubuntu/Linux och Docker-stöd, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Ditt namn hör också hemma här: ett testresultat från ditt grafikkort, en mening till testuppsättningen, en röst du har
designat, en tydlig felrapport eller en pull request räknas alla som bidrag. Tack till alla som provar och hör av sig.

## Licens och tack

Kod och medföljande röster: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Bygger på VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) och GGUF-konverteringen av audio.cpp. Hela listan: [THIRD_PARTY.md](THIRD_PARTY.md).
Inte knutet till OpenBMB, ModelBest eller audio.cpp-projektet.

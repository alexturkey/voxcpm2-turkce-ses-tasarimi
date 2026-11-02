[Türkçe](README.tr.md) · [English](README.md) · **Deutsch** · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Türkisches Voice Design mit VoxCPM2 auf einer 4-GB-GPU.** Beschreibe eine Stimme auf Englisch, lass das Modell sie
erzeugen, wähle die Variante, die dir gefällt, und lies dann beliebigen türkischen Text mit dieser Stimme vor. Enthalten
sind ein Installer mit einem einzigen Befehl, eine gepatchte [audio.cpp](https://github.com/0xShug0/audio.cpp)-Engine,
die auf eine GTX 1050 Ti (4 GB) passt, eine kleine lokale Weboberfläche und vierzehn fertige synthetische Stimmen:
sieben türkische und sieben muttersprachliche Sprecher für Englisch, Französisch, Deutsch, Spanisch, Russisch,
Chinesisch und Japanisch.

- Die App liest in 30 Sprachen vor; auch die Oberfläche gibt es in 30 Sprachen.
- 14 fertige Stimmen: 7 türkische sowie je eine für Englisch, Französisch, Deutsch, Spanisch, Russisch, Chinesisch und Japanisch.
- Weboberfläche (v0.2.0): Jede Variantenkarte hat zwei Stimmen, die rohe Entwurfsstimme und die Stimme, die du ab jetzt
  hörst; eine Leseliste mit Stimmenmenü; Stimmen umbenennen, ausblenden oder löschen; Entwürfe für die Texte, die du
  vorliest. Siehe »Weboberfläche« unter »Verwendung«.

[Wie es in 4 GB passt](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Installationsanleitung für KI-Agenten](AGENTS.md) · [Verantwortungsvoller Einsatz](ETHICS.md)

> Die mitgelieferten Stimmen sind synthetisch und aus einer Textbeschreibung entworfen. Der Abschnitt zum Stimmklonen ist
> nur für die eigene Stimme oder eine Stimme gedacht, deren Inhaber ausdrücklich zugestimmt hat; die Oberfläche lässt
> dich diese Erlaubnis bestätigen. Identitätsanmaßung, Betrug und Täuschung sind verboten. Kennzeichne Erzeugtes als
> KI-generiert. Siehe [ETHICS.md](ETHICS.md).

## 30 Sprachen

Wir haben ein Kappadokien-Dokumentarvideo in 8 Sprachen produziert: Türkisch, Englisch, Französisch, Deutsch, Spanisch,
Russisch, Chinesisch und Japanisch. Jede Sprache hat ihren eigenen **muttersprachlichen Sprecher**, mit VoxCPM2 aus
einer englischen Beschreibung entworfen. Alles wurde vollständig lokal auf einer GTX 1050 Ti mit 4 GB erzeugt, mit
derselben festen Qualität (16 Schritte, cfg 2.0). Die sieben Sprecher liegen hier bei, jeweils mit Prompt,
Entwurfstext, Seed und Referenzaufnahme.

| Code | Sprache | Stimme | Anhören | Video |
|---|---|---|---|---|
| `tr` | Türkisch | `hazir/belgesel_hanim` (und 6 weitere) | [Hörprobe](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Englisch | `hazir/anlatici_en` | [Hörprobe](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113791986763440439) |
| `fr` | Französisch | `hazir/anlatici_fr` | [Hörprobe](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113790681575804962) |
| `de` | Deutsch | `hazir/anlatici_de` | [Hörprobe](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113791351645262249) |
| `es` | Spanisch | `hazir/anlatici_es` | [Hörprobe](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113807365611122705) |
| `ru` | Russisch | `hazir/anlatici_ru` | [Hörprobe](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113801574136848884) |
| `zh` | Chinesisch (Mandarin) | `hazir/anlatici_zh` | [Hörprobe](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113802229606121794) |
| `ja` | Japanisch | `hazir/anlatici_ja` | [Hörprobe](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [Video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Warum Satz für Satz.** VoxCPM2 ist bei einer einzigen langen Generierung (etwa ab 30 Sekunden) nicht stabil: Das
Tempo zieht an, und die Stimme kann abdriften. Hier wird die Stimme von einer festen Referenzaufnahme und einem festen
Seed getragen, und langer Text wird mit einem Satz pro Zeile vorgelesen, sodass Klangfarbe und Stil vom ersten bis zum
letzten Satz gleich bleiben. Für andere Sprachen als Türkisch wird das türkische Aussprachewörterbuch nicht angewendet.
Alle 30 von VoxCPM2 unterstützten Sprachen wurden getestet und funktionieren; für Sprachen ohne mitgelieferte Stimme
nutze `--dil <code>`. Befehle pro Sprache und unsere Erkenntnisse: [docs/cok_dilli.md](docs/cok_dilli.md).
Claude-Code-Skill für den gesamten Entwurfsablauf:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 Beispiel-Prompts als Ausgangspunkt.** 18 Rollen (Dokumentarsprecher, Nachrichtensprecher, Werbestimme,
Hörbuch, erzählende Großmutter, Podcast-Host, Lehrer, Kinotrailer, Meditationsanleitung, Sportkommentator und mehr,
männlich und weiblich) in jeder der 8 Sprachen. Der Prompt ist englisch und nennt Nationalität und muttersprachlichen
Akzent des Sprechers; der Text, der beim Erzeugen der Stimme gelesen wird, ist gleich dabei, in der jeweiligen Sprache
und passend zur Rolle. Wähle einen aus, hör dir die Varianten an und behalte die, die dir gefällt:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, oder wähle in der Weboberfläche
*Beispielvorlage*. Vollständige Liste: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Vertone deine Videos mit deiner eigenen Stimme.** [DubWorld](https://github.com/alexturkey/dubworld) ist unser lokales
Programm zum Synchronisieren von Videos; es installiert dieses Repository als seine VoxCPM2-Stimm-Engine. Eine hier
entworfene Stimme wird dort mit `ses.voxcpm2_ses = "<name>/<variant>"` verwendet.

## Schnellstart (Windows, 3 Schritte)

1. **Lade** den Code herunter: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Das fertige Engine-Paket für deine Grafikkarte holt der Installer in Schritt 3:
   NVIDIA → [CUDA-Paket](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan-Paket, experimentell](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (schon eines heruntergeladen? Hänge `-HazirZip <path to the zip>` an den Befehl unten an).
2. **Entpacke** das ZIP, öffne den Ordner `voxcpm2-turkce-ses-tasarimi-main`, tippe `powershell` in die Adressleiste
   des Explorers und drücke Enter.
3. **Starte** den Installer (benötigt 64-Bit-Python 3.10-3.13; für CUDA NVIDIA-Treiber ≥ 570) und doppelklicke danach auf **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: Hänge `-Vulkan` ans Ende an. Die Oberfläche öffnet sich unter http://127.0.0.1:8765/.

Das Engine-ZIP ist keine eigenständige App (seine exe braucht das Modell und die DLLs, die der Installer einrichtet).
Details, GPU-Liste und häufige Probleme: »Schnellinstallation« weiter unten.

## Ubuntu / Linux (NVIDIA CUDA, experimentell)

Baue die gepatchte Engine mit `bash scripts/kur-linux.sh`, oder nutze `Dockerfile.linux`, um in einer Umgebung mit
Ubuntu 24.04 / CUDA 12.8.1 zu bauen und auszuführen. Voraussetzung sind eine NVIDIA-GPU und ein passender Treiber; der
native Installer braucht außerdem das CUDA Toolkit und Python 3.10-3.13. Die Oberfläche lauscht nur auf Loopback, auch
auf entfernten Servern (SSH-Weiterleitung). Voraussetzungen, Befehle, Wahl der Architektur und Umfang der Validierung:
[docs/linux.md](docs/linux.md).

## Schnellstart (macOS, Apple Silicon)

Benötigt die Xcode Command Line Tools (`xcode-select --install`) und [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Der Installer lädt das Modell herunter, baut die gepatchte Engine mit Metal (~1 min) und richtet alles unter `~/vox` ein.
Doppelklicke danach auf **`baslat.command`**. Auf einem MacBook Air M4 mit 16 GB: ~2 s Rechenzeit pro 1 s Sprache,
derselbe Seed liefert byteidentisches Audio, Spitze ~5,3 GB RAM, keine thermische Drosselung über 12 min
ununterbrochenes Vorlesen. Details und Messungen: [docs/mac.md](docs/mac.md).

**Native Mac-App (ohne Python, Homebrew oder Terminal):** [macos/README.md](macos/README.md). Sie enthält dieselbe
gepatchte Engine und lädt das Modell beim ersten Start herunter; vorerst wird sie mit Xcode aus dem Quellcode gebaut.

## Für Mac-Nutzer (Apple Silicon)

Es gibt außerdem eine unabhängige Adaption aus der Community für Macs mit Apple Silicon, die VoxCPM2 mit Apples
MLX-Framework ausführt: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Sie wird von Emre Koç ([@emre-koc](https://github.com/emre-koc)) in seinem eigenen Repository entwickelt und gepflegt,
nicht hier; Installationsschritte und Supportfragen gehören dorthin. Danke, Emre, dass du dieses Projekt auf den Mac
gebracht hast!

## So funktioniert es

1. **Voice Design.** Eine englische *Stimmbeschreibung* + ein *Text, der beim Erzeugen der Stimme gelesen wird* (in der
   Sprache der Stimme) + eine Anzahl von Varianten. Jede Variante bekommt ihren eigenen Seed; die Engine erhält
   `(description)text` und liefert pro Seed eine Entwurfsaufnahme. Der Text ist eine kurze Probe zum Kennenlernen der
   Stimme: 1-2 Sätze, höchstens ~20 s (die Oberfläche zeigt die Schätzung an und startet nicht über 22 s); langer Text
   gehört in Schritt 2.
2. **Referenzbasiertes Vorlesen.** Die Entwurfsaufnahme wird an **beide** Engine-Eingänge (`audio` und `voice_ref`)
   übergeben, zusammen mit ihrem Transkript (`reference_text`) und dem neuen Text, mit demselben Seed. Die Stimme wird
   von der Aufnahme getragen, nicht von der Beschreibung, und driftet deshalb von Text zu Text nicht ab. Der Text wird
   Satz für Satz vorgelesen.
3. Die Qualität ist fest: 16 Diffusionsschritte, CFG 2.0. Der Seed ist kein Qualitätsregler.

Die rohe Entwurfsaufnahme ist eine einmalige Probe der Stimme; keine spätere Lesung klingt genau so. Was du in jeder
späteren Lesung hörst, ist Schritt 2: die Entwurfsaufnahme als Referenz plus der eigene Seed der Variante. Deshalb führt
die Weboberfläche Schritt 2 direkt nach dem Entwurf aus und zeigt beides auf der Variantenkarte.

Die Engine ist audio.cpp v0.7.2 mit unserem Patch (`patches/`), das Modell ist VoxCPM2 Q8_0 GGUF. Spitzen-VRAM
≈ 2,8 GB; etwa 2 s Rechenzeit pro 1 s Sprache auf einer GTX 1050 Ti. Details und Messungen: [docs/4gb.md](docs/4gb.md).

## Mitgelieferte Stimmen (`hazir_sesler/`)

Alle vierzehn wurden aus den Prompts in ihrer `ses.json` entworfen; keine wurde aus einer Aufnahme geklont (Klonen ist
der separate, an eine Einwilligung gebundene Tab *Stimmklonen*).

| Stimme | Kurzbeschreibung | Anhören |
|---|---|---|
| `belgesel_hanim` | Reife Frau in den Fünfzigern, tiefer warmer Alt; ruhige Dokumentarsprecherin | [Hörprobe](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [Referenz](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Tiefer, kraftvoller, geheimnisvoller Sprecher | [Hörprobe](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [Referenz](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Erfahrener Nachrichtensprecher um die siebzig, ruhig und souverän | [Hörprobe](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [Referenz](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Charismatische Abendnachrichtensprecherin in den Dreißigern, samtig und ausdrucksstark | [Hörprobe](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [Referenz](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Märchenhexe: tief, leicht nasal, verschlagen süß | [Hörprobe](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [Referenz](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Außergewöhnlich tiefer, voller, gebieterischer Sprecher | [Hörprobe](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [Referenz](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Alter weiser Mann, tief und dröhnend, leicht geheimnisvoll | [Hörprobe](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [Referenz](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Englischer Muttersprachler, Dokumentarsprecher in den Fünfzigern (General American); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Französischer Muttersprachler, Dokumentarsprecher in den Fünfzigern (Pariser Französisch); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Deutscher Muttersprachler, Dokumentarsprecher in den Fünfzigern (Hochdeutsch); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Spanischer Muttersprachler, Dokumentarsprecher in den Fünfzigern (Kastilisch (Madrid)); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Russischer Muttersprachler, Dokumentarsprecher in den Fünfzigern (Moskau); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Chinesischer (Mandarin-)Muttersprachler, Dokumentarsprecher in den Fünfzigern (Pekinger Putonghua); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Japanischer Muttersprachler, Dokumentarsprecher in den Fünfzigern (Tokioter Standardsprache); tief, ruhig, warm | [Hörprobe](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [Referenz](hazir_sesler/anlatici_ja/referans.flac) |

Jeder Ordner enthält: `referans.flac` (verlustfreie Entwurfsaufnahme), `ses.json` (Prompt, Transkript, Entwurfs-Seed,
Lese-Seed, Beschreibung; `dil` = Sprache bei den Sprechern), `ornek_okuma.mp3` (+ zugehöriger Text). Direkt verwendbar:
`--ses hazir/<name>`. Die Referenzaufnahmen der Sprecher sind kurz (5,6-10 s); ihre Hörproben sind die ersten drei Sätze
des Kappadokien-Skripts, herausgeschnitten aus der vollständigen Produktionslesung.

## Schnellinstallation ohne Compiler (Windows 10/11, NVIDIA-GPU ≥ 4 GB)

Voraussetzungen: NVIDIA-Treiber ≥ 570 und 64-Bit-Python 3.10-3.13 (`winget install Python.Python.3.12`). Sonst nichts:
kein Visual Studio, kein CUDA-Installer. Du weißt nicht, welche Grafikkarte du hast? Führe `nvidia-smi` in PowerShell
aus: Es zeigt GPU-Name, Treiberversion und Speicher. Keine NVIDIA-Karte? Siehe »AMD / Intel« weiter unten.

Mit [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Ohne Git: Klicke auf dieser Seite auf **Code → Download ZIP**, entpacke das Archiv, öffne den entpackten Ordner
`voxcpm2-turkce-ses-tasarimi-main`, tippe `powershell` in die Adressleiste des Explorers, drücke Enter und führe dann
die letzte Zeile oben aus. Git wird nur für den Bau aus dem Quellcode gebraucht.

`-ExecutionPolicy Bypass` gilt nur für diesen einen Prozess und ändert keine Systemeinstellung; lies `scripts\kur.ps1`,
bevor du es ausführst, wie bei jedem Installer-Skript. Ein Befehl, ~10 min, ~3,7 GB Download, alles per sha256
geprüft: das Modell (2,95 GB), die CUDA-12.8-Laufzeit-DLLs als portable ZIPs (keine Systeminstallation, PATH bleibt
unverändert), die **vorgefertigte Engine** von der Releases-Seite, eine `.venv` mit den zwei Python-Paketen,
`ayarlar.json` und eine abschließende GPU-Prüfung (`KONTROL_OK`). Nach einem Fehler einfach erneut ausführen; bereits
geprüfte Dateien werden übersprungen. Starte dann die Weboberfläche: Doppelklicke im Repo-Ordner auf **`baslat.bat`**.
Das startet die Oberfläche und öffnet **http://127.0.0.1:8765/** im Browser, sobald sie bereit ist; schließe das
schwarze Fenster (oder drücke dort Strg+C), um sie zu beenden. Dasselbe in PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
öffne dann **http://127.0.0.1:8765/** selbst (so gestartet öffnet die Oberfläche keinen Browser; sie lauscht nur auf
localhost).

> **Die `audiocpp_cli.exe` im Release-ZIP ist nicht zum Doppelklicken gedacht.** Sie ist eine Kommandozeilen-Engine,
> die die CUDA-DLLs und das Modell neben sich braucht; `kur.ps1` legt alles an die richtige Stelle, und das
> Python-Paket steuert sie. Ein Doppelklick zeigt nur »cudart64_12.dll not found«.

**Unterstützte GPUs (Release v0.1.1):** nativer Code für GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) und RTX 50xx (sm_120a); jede andere CUDA-GPU ab Pascal führt das eingebettete PTX über den Treiber aus
(langsamerer erster Start). Maxwell (GTX 9xx) und älter werden von CUDA 12.8 nicht unterstützt. Von uns getestet auf
einer GTX 1050 Ti 4 GB (auch über Docker Desktop/WSL2 unter Windows, nur CLI); gemessen von @mslmyilmaz5 (#15):
RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (Details in [docs/linux.md](docs/linux.md)). Berichte zu anderen
Karten sind in den [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) willkommen.

**AMD / Intel (experimentell):** Ein separates Vulkan-Engine-ZIP (`...-win64-vulkan.zip`, ohne CUDA) wird mit
`scripts\kur.ps1 -Kok C:\vox -Vulkan` installiert. Es ist nur auf unserer NVIDIA-Karte über das Vulkan-Backend geprüft
(dort lief es langsamer als CUDA, lieferte aber für denselben Seed dasselbe Audio; diese Messung entstand, während die
Festplatte mit einem anderen Auftrag beschäftigt war, ein sauberer Geschwindigkeitsvergleich steht also noch aus), und
auf AMD- oder Intel-Hardware haben wir es selbst **nicht** getestet: Wenn du es ausprobierst, poste das Ergebnis bitte
in den Discussions. Bei mehr als einem Vulkan-Gerät (integriert + dediziert) schreibt der Installer den Index der
dedizierten GPU als `cihaz` in `ayarlar.json`.

*Hinweis: Die Vulkan-Unterstützung ist derzeit experimentell. Sie wurde auf einer GTX 1050 Ti erfolgreich gebaut und
getestet. Außerdem hat ein externer Nutzer (mitra_tr) berichtet, dass sie auf einer AMD 6900 XT läuft. Auf AMD/Intel-Karten
sind noch breitere Tests nötig.*

**Community-Test (AMD):** @mitraTR hat v0.1.1 mit Vulkan auf einer AMD Radeon RX 6900 XT unter Windows 11 ausgeführt: Installation, Stimmdesign, Vorlesen, Weboberfläche und Tests liefen fehlerfrei; das Vorlesen brauchte etwa 0,8-0,9 s Rechenzeit pro 1 s Sprache ([Bericht in #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Installiere in einen kurzen Ordner, dessen Pfad nur ASCII-Zeichen enthält (z. B. `C:\vox`): Unter Windows kann die Engine keine Pfade mit Umlauten oder anderen Nicht-ASCII-Zeichen öffnen. Alle bisherigen Berichte: [getestete Hardware](docs/donanim_testleri.md).

### Alternative: Engine aus dem Quellcode bauen

Benötigt die Visual Studio 2022 Build Tools mit »Desktopentwicklung mit C++« (inkl. C++-CMake-Tools), ~7 GB. Dann:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Das lädt zusätzlich nvcc herunter, holt den Quellcode von audio.cpp v0.7.2, wendet `patches/0001-voxcpm2-4gb-ve-hiz.patch`
an und baut für deine GPU (`-Mimari native`, Standard; oder z. B. `-Mimari 61`), ~15-25 min. Halte das Stammverzeichnis
kurz (`C:\vox`): nvcc scheitert an langen Pfaden. Schritt für Schritt mit Prüfungen: [AGENTS.md](AGENTS.md).

### Häufige Installationsprobleme

| Du siehst | Was es bedeutet, was zu tun ist |
|---|---|
| `cudart64_12.dll not found` nach Doppelklick auf die exe | Die Engine ist nicht zum manuellen Starten gedacht. Führe den `kur.ps1`-Befehl oben aus und starte dann die Weboberfläche. |
| `64-bit Python 3.10+ bulunamadı` (Python nicht gefunden) | Installiere Python (`winget install Python.Python.3.12`), schließe PowerShell, öffne ein neues Fenster und führe denselben Befehl erneut aus. |
| `motor ekran kartını görmedi` (die Engine hat die GPU nicht erkannt) | Aktualisiere den NVIDIA-Treiber auf 570 oder neuer; prüfe, ob `nvidia-smi` läuft. |
| `indirme başarısız` / `sha256 tutmadı` (Download fehlgeschlagen / Prüfsumme stimmt nicht) | Meist ein abgebrochener Download. Führe denselben Befehl erneut aus; bereits geprüfte Dateien werden übersprungen. |
| Bau aus dem Quellcode: `nvcc` scheitert | Halte das Installationsverzeichnis kurz (`-Kok C:\vox`). |
| Die Seite öffnet sich nicht | Starte die Oberfläche mit `baslat.bat` oder öffne http://127.0.0.1:8765/ selbst. Port belegt? Ändere `"port"` in `ayarlar.json`. |

Probleme? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) oder ein
[Installations-Issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
mit deiner GPU, Windows-Version, dem Befehl und seinen letzten Zeilen.

## Verwendung

Kommandozeile:
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
Textregeln: Zahlen in Worten schreiben, keine Anführungszeichen (das Tool lehnt Ziffern und Anführungszeichen ab), ein
Satz pro Zeile, ≤ 2000 Zeichen pro Zeile. Pause nach einer Zeile: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf`
1 s, `|| agir` 1,5 s oder eine eigene Länge `|| 0,8` (0-5 s; die Ziffern der Markierung sind erlaubt).
`ayarlar/okunus_sozlugu.tsv` korrigiert die Aussprache fremder Wörter in türkischem Text. Die Sprache wird aus dem Text
erkannt (türkische Buchstaben, Schrift, häufige Wörter; im Zweifel `dil` der Stimmkarte; `--dil <code>` ist optional).
Bei nicht-türkischem Text sind Apostrophe dort erlaubt, das türkische Wörterbuch wird übersprungen, Ziffern werden
weiterhin abgelehnt. Gibt eine Lesung `speed gate: satır [...]` aus, hör dir diese Zeilen an.

### Weboberfläche

Nur lokal (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → http://127.0.0.1:8765/ selbst öffnen
(anderer Port: `--port 8800`), oder auf `baslat.bat` doppelklicken. Den Server beendest du mit Strg+C. Drei Tabs:
*Stimme entwerfen*, *Mit dieser Stimme vorlesen*, *Stimmklonen*. Der übliche Weg: *Entwerfen* → Varianten anhören →
*Zu meiner Leseliste* → *Mit dieser Stimme vorlesen* → herunterladen. Oder wähle im Stimmenmenü eine mitgelieferte
Stimme und lies vor.

- **Version im Kopfbereich.** Ein kleines, blasses `v0.2.0 · <short commit>` (mit `+`, wenn versionierte Dateien
  nicht committete Änderungen haben; ohne git nur die Version), damit Screenshots und Videos zeigen, welche Version
  verwendet wurde.
- **Zwei Stimmen auf jeder Variantenkarte.** Oben, in Grau, die Stimme *Roher Entwurf*: Sie wird einmal erzeugt und kommt
  nie wieder genau so heraus. Darunter, in einem orangefarbenen Rahmen, *↻ Diese Stimme hörst du ab jetzt*: die
  Entwurfsaufnahme als Referenz zurückgelesen, mit dem eigenen Seed der Variante (auf der Karte angezeigt). So klingt
  die Stimme in jeder späteren Lesung. Darunter stehen *Mit dieser Stimme vorlesen* und *Zu meiner Leseliste*. Ein
  Druck auf *Entwerfen* erledigt beides: Es entwirft jede Variante und liest dann deinen Text mit jeder bleibenden
  Stimme vor; ein einziger Fortschrittsbalken zählt beide Phasen. Der Variantenordner erhält `dinleme.wav`. Bricht diese
  Lesung vorzeitig ab, bleibt der Entwurf erhalten, und die Karte zeigt einen Hinweis.
- **Das Fenster »Text, den du hören möchtest«.** In *Stimme entwerfen* enthält das Feld *↻ Text, den du hören möchtest*,
  was jede bleibende Stimme vorliest (leer gelassen, wird der Beispielsatz gelesen). Ein Klick darauf öffnet das
  Leseheft in einem Fenster: Zeilennummern, Zeilenmenü, Pausenbänder. *OK* schreibt den Text samt Pausen zurück ins
  Feld; *Abbrechen* oder Esc ändert nichts. Der Vorlese-Tab behält seinen eigenen Text.
- **Das Leseheft.** Ein Satz pro Zeile. Klicke auf eine Zeilennummer für das Zeilenmenü (nach oben oder unten
  verschieben, an eine Position verschieben, duplizieren, löschen; Alt+↑/↓, Alt+Shift+↓ oder an der Nummer ziehen;
  Strg+Z macht Text und Pausen gemeinsam rückgängig). Klicke auf das schmale Band zwischen zwei Zeilen, um die Pause zu
  wählen (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, oder eigene 0-5 s über das Zahnrad); zweimal Enter ergibt
  einen Absatz (1 s), und Leerzeilen werden zu Pausenbändern. Während das Ergebnis abgespielt wird, leuchtet die gerade
  gelesene Zeile auf und wird ins Bild gescrollt; *▶ Ab hier anhören* im Zeilenmenü spielt ab dieser Zeile. Text und
  Pausen überstehen ein Neuladen der Seite (Browserspeicher).
- **Entwürfe.** Die Schaltfläche *📄 Entwürfe* sitzt in beiden Heften (Vorlese-Tab und Fenster). Speichere den
  aktuellen Text samt Pausen als Entwurf, lade einen per Klick (Strg+Z macht es rückgängig) und nutze ⋯, um ihn zu
  überschreiben, umzubenennen oder zu löschen. Entwürfe werden in `sesler/taslaklar.json` gespeichert, nie im
  Repository.
- **Leseliste und Stimmenmenü.** Auf einer Variantenkarte öffnet *Zu meiner Leseliste* ein Namensfeld: Gib der Variante
  einen eigenen Namen, und ✓ fügt sie hinzu. Der *Name der Generierung* bleibt auf jeder Variante dieses Durchlaufs
  erhalten. In *Mit dieser Stimme vorlesen* öffnet die Stimmen-Schaltfläche (Flagge + Name) das Stimmenmenü: oben
  *Meine Leseliste*, dann die mitgelieferten Stimmen mit Flaggen (Sprache der Oberfläche zuerst). Jede Zeile hat ▶
  anhören (die bleibende Stimme, falls vorhanden), das Herz (hinzufügen oder entfernen) und ⋯; ↑/↓ und Enter wählen,
  Esc schließt, die zuletzt gewählte Stimme wird gemerkt. Die Liste liegt in `sesler/okuma_listesi.json`, außerhalb des
  Repositorys, und übersteht Neustarts.
- **Stimmen verwalten.** Das ⋯-Menü (Zeile im Stimmenmenü oder Variantenkarte) bietet *Mit dieser Stimme vorlesen*, zur
  Liste hinzufügen oder daraus entfernen, *Umbenennen* (ein leerer Name stellt den ursprünglichen wieder her; *Zurück
  zum ursprünglichen Namen*), *Löschen* für entworfene Stimmen und *Ausblenden* für mitgelieferte; beide fragen vorher
  nach. Eine gelöschte Stimme wandert nach `sesler/_cop/`; Ausblenden fasst nie Dateien im Repository an.
  *Ausgeblendete und gelöschte Stimmen (N)* unten im Stimmenmenü bietet *Wiederherstellen*. Eigene Namen und
  ausgeblendete Stimmen werden in `sesler/yerel_katman.json` gespeichert. Eine umbenannte Stimme zeigt ihre Herkunft in
  Grau (*Name der Generierung · Variante N*); ⋯ → *Zur Generierung* öffnet ihren Entwurf.
- **Tastenkürzel und Dateien.** Strg+Enter (⌘+Enter auf dem Mac) startet *Entwerfen* oder *Mit dieser Stimme vorlesen*
  im geöffneten Tab. Der Fortschrittsbalken zeigt *vergangen / ~gesamt*, mit einer Schätzung, die aus früheren
  Aufträgen auf deinem Rechner gelernt wird. Der Download wird nach Stimme und Uhrzeit benannt
  (`Voice_Name_2026-11-02_0152.wav`).

**Stimmklonen (die eigene oder eine genehmigte Stimme).** Im Tab *Stimmklonen* der Oberfläche gibst du deine Aufnahme
(wav/mp3/flac/ogg, empfohlen 5-30 s saubere Sprache; unter 3 s wird abgelehnt, über 36 s wird gekürzt), ihr exaktes
Transkript und den vorzulesenden Text an. Die Schaltfläche bleibt deaktiviert, bis du »Diese Stimme gehört mir oder ich
habe die ausdrückliche Erlaubnis des Inhabers« ankreuzt. Die Aufnahme geht nur an den lokalen Server (127.0.0.1), wird
zusammen mit ihrer Referenzkodierung in einem temporären Ordner verarbeitet, und dieser Ordner wird gelöscht, wenn der
Auftrag endet, auch bei einem Fehler; nichts wird über das Netzwerk gesendet. Nur die synthetische Ausgabe bleibt
erhalten (Oberfläche: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Die Ausgabe ist `klon_synthetic.wav` mit einem Tag
»synthetic«; kennzeichne sie beim Teilen als KI-generiert. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## FAQ

**Modell oder Engine? Was ist was?** VoxCPM2 (OpenBMB) ist das *Modell*: das Netz mit 2 Milliarden Parametern, das
Text in Sprache umwandelt. audio.cpp ist die *Engine*: das C++/CUDA-Programm, das das Modell auf deiner GPU ausführt
(`audiocpp_cli.exe`). Unser Patch ändert die Engine, nicht das Modell: Er sorgt dafür, dass VoxCPM2 in 4 GB passt und
derselbe Seed jedes Mal dasselbe Audio liefert. Das Python-Paket in diesem Repo bereitet nur den Text vor, ruft die
Engine auf und sammelt die Dateien ein.

**Welche GPUs?** Siehe »Unterstützte GPUs« oben: NVIDIA ab GTX 10xx, 4 GB VRAM oder mehr, Treiber ≥ 570. Nativer Code
ist im Release für sm_61/75/86/89/120a enthalten; andere Karten ab Pascal nutzen das eingebettete PTX (langsamerer
erster Start). AMD/Intel: experimentelles Vulkan-ZIP, `kur.ps1 -Vulkan`; ein externer Nutzer hat berichtet, dass es
auf einer AMD 6900 XT läuft, breitere Tests auf AMD/Intel sind aber noch nötig (siehe »AMD / Intel« oben). Nur CPU
(`"backend": "cpu"` in `ayarlar.json`) läuft, ist aber ~6× langsamer als eine GTX 1050 Ti (Engine-Messung, 535 s
gegenüber 94 s für 48 s Sprache); kein unterstützter Weg.

**Wie schnell?** Gemessen auf einer GTX 1050 Ti 4 GB (i7-7700HQ): eine Entwurfsvariante (≈ 25 s Aufnahme) 55 s;
Vorlesen ≈ 2 s Rechenzeit pro 1 s Sprache (Echtzeitfaktor 1,9-2,8) nach einer einmaligen Referenzkodierung von ~50 s
pro Stimme (auf der Festplatte zwischengespeichert) und 10-20 s Modellladezeit pro Durchgang; Spitzen-VRAM 2,6-2,9 GB.
Neuere Karten sind schneller; Zahlen und Methode: [docs/4gb.md](docs/4gb.md).

**Kann es eine Stimme klonen?** Das zugrunde liegende Modell VoxCPM2 kann eine Stimme aus einer Referenzaufnahme
nachahmen, und der Abschnitt zum Klonen nutzt das. Verwende es nur mit deiner eigenen Stimme oder mit ausdrücklicher
Erlaubnis der Person, der die Stimme gehört; die Oberfläche lässt dich diese Erlaubnis bestätigen. Voice Design braucht
keine Aufnahme: Es beginnt mit einer Textbeschreibung auf Englisch oder Chinesisch, und die »Referenz«, die beim
Vorlesen mit einer entworfenen Stimme verwendet wird, ist die eigene synthetische Entwurfsaufnahme des Modells.
Identitätsanmaßung, Betrug und Täuschung sind verboten. Siehe [ETHICS.md](ETHICS.md). Kennzeichne Veröffentlichtes als
KI-generiert.

**Wie schreibe ich eine gute Stimmbeschreibung?** Auf Englisch, 1-3 Sätze: Alter und Geschlecht, Klangfarbe
(tief/hell, warm, nasal, rau), Tonfall und Rolle (ruhiger Dokumentarsprecher, energiegeladener Moderator), Tempo
(langsam, gemessen) und »clean studio recording, no background noise«. Bleib bei einer Beschreibung, nicht bei einem
Skript; keine Klammern. Lass 3-5 Varianten erzeugen und hör sie dir an: Der Seed verändert die Stimme stark. Für den
Erzeugungstext nimm 1-2 natürliche Sätze in der Sprache der Stimme, in der gewünschten Stimmung (höchstens ~20 s
Sprache). Beim Vorlesen ein Satz pro Zeile; lange Sätze aufteilen, Zahlen in Worten schreiben.

## Mitmachen

Du weißt nicht, wo du anfangen sollst? Diese vier kleinen Issues sind ein guter erster Schritt:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Probiere es auf deiner GPU aus und melde Karte, Treiber und Zeiten
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: Teste den experimentellen Vulkan-Build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Füge dem Testsatz einen Satz hinzu
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Teile eine selbst entworfene Stimme mit Beschreibung und Seed

**Teste deine Grafikkarte, schreib einen Bericht:** Programmierkenntnisse brauchst du nicht, nur das [Formular für Hardware-Testberichte](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); von Intel-Grafikkarten gibt es noch keinen Bericht.

Gemeinsamer Testsatz: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); Leitfaden für Markenstimmen:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); wie du Code einreichst: [CONTRIBUTING.md](CONTRIBUTING.md).
Installationsprobleme: [Issue-Formular](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); Fragen und Ergebnisse: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Alle Beteiligten folgen dem [Verhaltenskodex](CODE_OF_CONDUCT.md): Sei freundlich und halte Feedback sachbezogen.

## Mitwirkende

- [@alexturkey](https://github.com/alexturkey): Maintainer; Code, mitgelieferte Stimmen, Dokumentation
- [@cayir21](https://github.com/cayir21): Metal-Unterstützung für macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): Satzende-Fix (EOS) für das Vorlesen mehrerer Sätze im CPU-Backend, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): experimentelle CUDA-Installation für Ubuntu/Linux und Docker-Unterstützung, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Auch dein Name gehört hierher: ein Testergebnis von deiner GPU, ein Satz für den Testsatz, eine selbst entworfene
Stimme, ein klarer Fehlerbericht oder ein Pull Request, all das zählt als Beitrag. Danke an alle, die es ausprobieren
und sich zurückmelden.

## Lizenz und Danksagung

Code und mitgelieferte Stimmen: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Basiert auf VoxCPM2 (OpenBMB,
Apache-2.0), audio.cpp (ShugoAI LLC, Apache-2.0) und der GGUF-Konvertierung von audio.cpp. Vollständige Liste:
[THIRD_PARTY.md](THIRD_PARTY.md). Nicht verbunden mit OpenBMB, ModelBest oder dem audio.cpp-Projekt.

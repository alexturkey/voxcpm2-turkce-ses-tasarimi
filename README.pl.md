[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · **Polski** · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Projektowanie tureckich głosów z VoxCPM2 na karcie graficznej z 4 GB.** Opisz głos po angielsku, pozwól modelowi go
stworzyć, wybierz wariant, który ci się podoba, a potem czytaj tym głosem dowolny turecki tekst. W zestawie: instalator
uruchamiany jednym poleceniem, silnik [audio.cpp](https://github.com/0xShug0/audio.cpp) z naszą łatką, który mieści się na GTX 1050 Ti (4 GB),
mały lokalny interfejs webowy i czternaście gotowych syntetycznych głosów: siedem tureckich i siedmiu natywnych lektorów
w językach angielskim, francuskim, niemieckim, hiszpańskim, rosyjskim, chińskim i japońskim.

- Aplikacja czyta w 30 językach; interfejs również jest dostępny w 30 językach.
- 14 gotowych głosów: 7 tureckich oraz po jednym w językach angielskim, francuskim, niemieckim, hiszpańskim, rosyjskim, chińskim i japońskim.
- Interfejs webowy (v0.2.0): każda karta wariantu ma dwa głosy, surowy głos projektu i głos, który będziesz słyszeć zawsze;
  lista czytania z menu głosów; zmiana nazwy, ukrywanie i usuwanie głosów; szkice czytanych tekstów. Zobacz «Interfejs webowy» w sekcji «Użycie».

[Jak to mieści się w 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Instrukcja instalacji dla agentów AI](AGENTS.md) · [Odpowiedzialne użycie](ETHICS.md)

> Dołączone głosy są syntetyczne, zaprojektowane na podstawie opisu tekstowego. Sekcja klonowania głosu służy wyłącznie do
> twojego własnego głosu lub głosu używanego za wyraźną zgodą jego właściciela; interfejs prosi o potwierdzenie tej zgody.
> Podszywanie się, oszustwa i wprowadzanie w błąd są zabronione. Oznaczaj to, co wygenerujesz, jako wygenerowane przez AI. Zobacz [ETHICS.md](ETHICS.md).

## 30 języków

Zrobiliśmy jeden film dokumentalny o Kapadocji w 8 językach: tureckim, angielskim, francuskim, niemieckim, hiszpańskim,
rosyjskim, chińskim i japońskim. Każdy język ma własnego **natywnego lektora**, zaprojektowanego w VoxCPM2 na podstawie
angielskiego opisu. Całość wygenerowano w pełni lokalnie na GTX 1050 Ti z 4 GB, przy tej samej stałej jakości (16 kroków,
cfg 2.0). Siedmiu lektorów jest dołączonych tutaj, razem z promptem, tekstem projektu, ziarnem i nagraniem referencyjnym.

| Kod | Język | Głos | Odsłuchaj | Wideo |
|---|---|---|---|---|
| `tr` | turecki | `hazir/belgesel_hanim` (i 6 innych) | [próbka](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | angielski | `hazir/anlatici_en` | [próbka](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113791986763440439) |
| `fr` | francuski | `hazir/anlatici_fr` | [próbka](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113790681575804962) |
| `de` | niemiecki | `hazir/anlatici_de` | [próbka](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113791351645262249) |
| `es` | hiszpański | `hazir/anlatici_es` | [próbka](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113807365611122705) |
| `ru` | rosyjski | `hazir/anlatici_ru` | [próbka](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113801574136848884) |
| `zh` | chiński (mandaryński) | `hazir/anlatici_zh` | [próbka](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113802229606121794) |
| `ja` | japoński | `hazir/anlatici_ja` | [próbka](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [wideo](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Dlaczego zdanie po zdaniu.** VoxCPM2 nie jest stabilny przy jednej długiej generacji (mniej więcej powyżej 30 sekund):
tempo przyspiesza, a głos może odpłynąć. Tutaj głos niesie stałe nagranie referencyjne i stałe ziarno, a długi tekst jest
czytany po jednym zdaniu w wierszu, więc barwa i styl pozostają takie same od pierwszego do ostatniego zdania. Dla języków
innych niż turecki turecki słownik wymowy nie jest stosowany. Wszystkie 30 języków obsługiwanych przez VoxCPM2 zostało przetestowanych i działa; dla
tych bez dołączonego głosu użyj `--dil <code>`. Polecenia dla poszczególnych języków i wyciągnięte przez nas wnioski:
[docs/cok_dilli.md](docs/cok_dilli.md). Umiejętność (skill) Claude Code dla całego procesu projektowania:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 przykładowe prompty na start.** 18 ról (lektor dokumentalny, prezenter wiadomości, głos reklamowy, audiobook,
babcia opowiadająca bajki, prowadzący podcast, nauczyciel, zwiastun filmowy, przewodnik medytacji, komentator sportowy
i inne, męskie i żeńskie) w każdym z 8 języków. Prompt jest po angielsku, z narodowością i natywnym akcentem mówcy; dołączony
jest do niego tekst czytany podczas tworzenia głosu, w danym języku i dopasowany do roli. Wybierz jeden, odsłuchaj warianty,
zachowaj ten, który ci się podoba: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3` albo wybierz
*Przykładowy opis* w interfejsie webowym. Pełna lista: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dubbinguj swoje filmy własnym głosem.** [DubWorld](https://github.com/alexturkey/dubworld) to nasz lokalny program do dubbingu
wideo; instaluje to repozytorium jako swój silnik głosowy VoxCPM2. Głos zaprojektowany tutaj jest tam używany przez
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Szybki start (Windows, 3 kroki)

1. **Pobierz** kod: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Gotowy pakiet silnika dla twojej karty pobierze instalator w kroku 3:
   NVIDIA → [pakiet CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.2/voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-cuda12.8.zip),
   AMD / Intel → [pakiet Vulkan, eksperymentalny](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.2/voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-vulkan.zip)
   (masz już pobrany? dodaj `-HazirZip <path to the zip>` do poniższego polecenia).
2. **Rozpakuj** zip, otwórz folder `voxcpm2-turkce-ses-tasarimi-main`, wpisz `powershell` w pasku adresu Eksploratora
   i naciśnij Enter.
3. **Uruchom** instalator (wymaga 64-bitowego Pythona 3.10-3.13; dla CUDA sterownik NVIDIA ≥ 570), a potem kliknij dwukrotnie **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: dodaj na końcu `-Vulkan`. Interfejs otwiera się pod adresem http://127.0.0.1:8765/.

Zip silnika nie jest samodzielną aplikacją (jego exe potrzebuje modelu i bibliotek DLL, które konfiguruje instalator).
Szczegóły, lista kart i częste problemy: «Szybka instalacja» poniżej.

## Ubuntu / Linux (NVIDIA CUDA, eksperymentalnie)

Zbuduj silnik z łatką poleceniem `bash scripts/kur-linux.sh` albo użyj `Dockerfile.linux`, aby zbudować i uruchomić go
w środowisku Ubuntu 24.04 / CUDA 12.8.1. Wymaga karty NVIDIA i zgodnego sterownika; natywny instalator potrzebuje też CUDA
toolkit i Pythona 3.10-3.13. Interfejs pozostaje dostępny tylko przez loopback, także na zdalnych serwerach (przekierowanie SSH).
Wymagania, polecenia, wybór architektury i zakres weryfikacji: [docs/linux.md](docs/linux.md).

## Szybki start (macOS, Apple Silicon)

Wymaga Xcode Command Line Tools (`xcode-select --install`) i [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Instalator pobiera model, buduje silnik z łatką z obsługą Metal (~1 min) i konfiguruje wszystko w `~/vox`.
Następnie kliknij dwukrotnie **`baslat.command`**. Na MacBooku Air M4 16 GB: ~2 s obliczeń na 1 s mowy, to samo ziarno daje
identyczny co do bajtu dźwięk, szczyt ~5,3 GB RAM, bez spowolnienia termicznego przez 12 min ciągłego czytania. Szczegóły
i pomiary: [docs/mac.md](docs/mac.md).

**Natywna aplikacja na Maca (bez Pythona, Homebrew i Terminala):** [macos/README.md](macos/README.md). Zawiera ten sam
silnik z łatką i pobiera model przy pierwszym uruchomieniu; na razie buduje się ją ze źródeł w Xcode.

## Dla użytkowników Maca (Apple Silicon)

Istnieje też niezależna adaptacja stworzona przez społeczność dla Maców z Apple Silicon, która uruchamia VoxCPM2 na
frameworku Apple MLX: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Rozwija i utrzymuje ją Emre Koç ([@emre-koc](https://github.com/emre-koc)) we własnym repozytorium, nie tutaj; instrukcje
instalacji i pytania o wsparcie kieruj tam. Dziękujemy, Emre, że przeniosłeś ten projekt na Maca!

## Jak to działa

1. **Projektowanie głosu.** Angielski *opis głosu* + *tekst czytany podczas tworzenia głosu* (w języku głosu) + liczba
   wariantów. Każdy wariant dostaje własne ziarno; silnik otrzymuje `(description)text` i zwraca jedno nagranie projektu
   na każde ziarno. Tekst to krótka próbka, by poznać głos: 1-3 zdania, najwyżej ~30 s (interfejs pokazuje szacunek
   i nie wystartuje powyżej 33 s); długi tekst należy do kroku 2.
2. **Czytanie na podstawie referencji.** Nagranie projektu trafia na **oba** wejścia silnika (`audio` i `voice_ref`),
   razem z transkrypcją (`reference_text`) i nowym tekstem do przeczytania, z tym samym ziarnem. Głos niesie nagranie,
   a nie opis, więc nie odpływa od tekstu do tekstu. Tekst jest czytany zdanie po zdaniu.
3. Jakość jest stała: 16 kroków dyfuzji, CFG 2.0. Ziarno nie jest pokrętłem jakości.
4. **Czas słów, ten sam dźwięk przy każdym uruchomieniu.** Podczas czytania sam silnik podaje, gdzie każde słowo się zaczyna i kończy (łatka 0002, bez dodatkowego modelu). Czasy trafiają do `kelimeler.json`, a wiersze są przycinane tak, by odstęp między nimi był równy ustawieniu pauzy. Dokładność względem wymuszonego dopasowania CTC (forced alignment, CTC = 100%): 89,66% (turecki, 12 głosów; ustawienie `kelime_zamani`, domyślnie włączone). Dzięki łatce 0003 to samo ziarno daje identyczny co do bajtu dźwięk przy każdym uruchomieniu.

Surowe nagranie projektu to jednorazowa próbka głosu; żadne późniejsze czytanie nie brzmi dokładnie tak samo. W każdym
kolejnym czytaniu słyszysz krok 2: nagranie projektu jako referencję plus własne ziarno wariantu. Dlatego interfejs webowy
wykonuje krok 2 zaraz po projektowaniu i pokazuje oba głosy na karcie wariantu.

Silnik to audio.cpp v0.7.2 z naszą łatką (`patches/`), model to VoxCPM2 Q8_0 GGUF. Szczytowe zużycie VRAM ≈ 2,8 GB;
około 2 s obliczeń na 1 s mowy na GTX 1050 Ti. Szczegóły i pomiary: [docs/4gb.md](docs/4gb.md).

## Dołączone głosy (`hazir_sesler/`)

Wszystkie czternaście zaprojektowano z promptów zapisanych w ich `ses.json`; żadnego nie sklonowano z nagrania (klonowanie
to osobna karta *Klonowanie głosu*, dostępna tylko za zgodą).

| Głos | Krótki opis | Odsłuchaj |
|---|---|---|
| `belgesel_hanim` | Dojrzała kobieta po pięćdziesiątce, głęboki ciepły alt; spokojna lektorka dokumentalna | [próbka](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referencja](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Głęboki, mocny, tajemniczy męski narrator | [próbka](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referencja](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Doświadczony prezenter wiadomości około siedemdziesiątki, spokojny i budzący zaufanie | [próbka](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referencja](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Charyzmatyczna prezenterka wieczornych wiadomości po trzydziestce, aksamitna i ekspresyjna | [próbka](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referencja](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Baśniowa czarownica: niski, lekko nosowy, chytrze słodki głos | [próbka](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referencja](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Wyjątkowo głęboki, gęsty, władczy męski narrator | [próbka](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referencja](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Stary mędrzec, głęboki i dudniący, nieco tajemniczy | [próbka](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referencja](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Natywny anglojęzyczny lektor dokumentalny po pięćdziesiątce (General American); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Natywny francuskojęzyczny lektor dokumentalny po pięćdziesiątce (paryski); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Natywny niemieckojęzyczny lektor dokumentalny po pięćdziesiątce (Hochdeutsch); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Natywny hiszpańskojęzyczny lektor dokumentalny po pięćdziesiątce (kastylijski (Madryt)); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Natywny rosyjskojęzyczny lektor dokumentalny po pięćdziesiątce (moskiewski); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Natywny chińskojęzyczny (mandaryński) lektor dokumentalny po pięćdziesiątce (pekiński putonghua); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Natywny japońskojęzyczny lektor dokumentalny po pięćdziesiątce (standard tokijski); głęboki, spokojny, ciepły | [próbka](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referencja](hazir_sesler/anlatici_ja/referans.flac) |

W każdym folderze: `referans.flac` (bezstratne nagranie projektu), `ses.json` (prompt, transkrypcja, ziarno projektu, ziarno
czytania, opis; `dil` = język, u lektorów), `ornek_okuma.mp3` (+ jego tekst). Używaj ich bezpośrednio: `--ses hazir/<name>`.
Nagrania referencyjne lektorów są krótkie (5,6-10 s); ich próbki to pierwsze trzy zdania scenariusza o Kapadocji, wycięte
z pełnego czytania produkcyjnego.

## Szybka instalacja, bez kompilatora (Windows 10/11, karta NVIDIA ≥ 4 GB)

Wymagania: sterownik NVIDIA ≥ 570 i 64-bitowy Python 3.10-3.13 (`winget install Python.Python.3.12`). Nic więcej:
bez Visual Studio, bez instalatora CUDA. Nie wiesz, jaką masz kartę? Uruchom `nvidia-smi` w PowerShellu: wypisze nazwę
karty, wersję sterownika i pamięć. Nie masz karty NVIDIA? Zobacz «AMD / Intel» poniżej.

Z [Gitem](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Bez Gita: na tej stronie kliknij **Code → Download ZIP**, rozpakuj archiwum, otwórz rozpakowany folder
`voxcpm2-turkce-ses-tasarimi-main`, wpisz `powershell` w pasku adresu Eksploratora i naciśnij Enter, a potem uruchom
ostatni wiersz powyżej. Git jest potrzebny tylko do budowania ze źródeł.

`-ExecutionPolicy Bypass` dotyczy tylko tego jednego procesu i nie zmienia żadnych ustawień systemu; przeczytaj `scripts\kur.ps1`
przed uruchomieniem, jak w przypadku każdego skryptu instalacyjnego. Jedno polecenie, ~10 min, ~3,7 GB do pobrania, wszystko weryfikowane sha256: model (2,95 GB), biblioteki DLL środowiska uruchomieniowego CUDA 12.8 jako
przenośne zipy (bez instalacji w systemie, PATH nietknięty), **gotowy silnik** ze strony Releases, `.venv` z dwoma
pakietami Pythona, `ayarlar.json` i końcowy test karty (`KONTROL_OK`). Po każdym błędzie uruchom ponownie; zweryfikowane
pliki są pomijane. Potem uruchom interfejs webowy: kliknij dwukrotnie **`baslat.bat`** w folderze repozytorium. Uruchamia on
interfejs i otwiera **http://127.0.0.1:8765/** w przeglądarce, gdy wszystko jest gotowe; zamknij czarne okno (lub naciśnij w nim Ctrl+C), aby zatrzymać.
To samo z PowerShella:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
a potem sam otwórz **http://127.0.0.1:8765/** (uruchomiony w ten sposób interfejs nie otwiera przeglądarki; nasłuchuje tylko
na localhost).

> **`audiocpp_cli.exe` z zipa wydania nie jest przeznaczony do uruchamiania dwuklikiem.** To silnik wiersza poleceń, który
> potrzebuje obok siebie bibliotek DLL CUDA i modelu; `kur.ps1` układa wszystko na miejscu, a steruje nim pakiet Pythona.
> Dwuklik pokaże tylko «cudart64_12.dll not found».

**Obsługiwane karty (wydanie v0.3.2):** natywny kod dla GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) i RTX 50xx (sm_120a); każda inna karta CUDA od Pascala wzwyż uruchamia wbudowany PTX przez sterownik (wolniejszy
pierwszy start). Maxwell (GTX 9xx) i starsze nie są obsługiwane przez CUDA 12.8. Testowane przez nas na GTX 1050 Ti 4 GB (także przez Docker Desktop/WSL2 w Windows, tylko CLI); zmierzone przez @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (szczegóły w [docs/linux.md](docs/linux.md)). Raporty z innych kart mile widziane w [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (eksperymentalnie):** osobny silnik Vulkan (bez CUDA) instaluje się poleceniem `scripts\kur.ps1 -Kok C:\vox -Vulkan`. Przetestowaliśmy go na naszej karcie NVIDIA przez backend Vulkan (tam wolniej niż CUDA, ten sam dźwięk dla tego samego ziarna; czyste porównanie szybkości jeszcze przed nami) i na zintegrowanej grafice Intel HD Graphics 630 (około 35-50 s obliczeń na 1 s mowy); na AMD sami go **nie** testowaliśmy: jeśli spróbujesz, opisz wynik w Discussions. Przy więcej niż jednym urządzeniu Vulkan (zintegrowane + dedykowane) instalator zapisuje indeks dedykowanej karty jako `cihaz` w `ayarlar.json`.

**Test społeczności (AMD):** @mitraTR uruchomił v0.1.1 z Vulkanem na AMD Radeon RX 6900 XT w Windows 11: instalacja, projektowanie głosu, czytanie, interfejs WWW i testy zadziałały; czytanie zajęło ok. 0,8-0,9 s obliczeń na 1 s mowy ([raport w #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Instaluj w krótkim folderze, którego ścieżka ma tylko znaki ASCII (np. `C:\vox`): w Windows silnik nie otwiera ścieżek z polskimi znakami ani innymi znakami spoza ASCII. Wszystkie dotychczasowe raporty: [przetestowany sprzęt](docs/donanim_testleri.md).

**Uwagi o Vulkanie:** od silnika v0.3.1 znaczniki czasu słów działają także na Vulkanie. Dwa pakiety: `vulkan` wymaga procesora z AVX2 (większość Intel Core od 2013, AMD od 2015; wielu Pentiumom/Celeronom go brakuje); [`vulkan-uyumlu`](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.2/voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-vulkan-uyumlu.zip) działa na każdym 64-bitowym procesorze x86, ale pierwsze czytanie głosu trwa około 2,2 raza dłużej (kolejne czytania mają tę samą szybkość). `kur.ps1 -Vulkan` sprawdza procesor i sam wybiera pakiet. Na grafice zintegrowanej silnik zużywa podczas czytania około 8 GB RAM. Pierwsze uruchomienie na Vulkanie może potrwać kilka minut, bo kompilowane są shadery GPU; kolejne czytania są szybsze. Szczegóły: [docs/vulkan.md](docs/vulkan.md).

### Alternatywa: zbuduj silnik ze źródeł

Wymaga Visual Studio 2022 Build Tools z «Desktop development with C++» (w tym C++ CMake tools), ~7 GB. Następnie:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
To polecenie pobiera też nvcc, ściąga źródła audio.cpp v0.7.2, nakłada `patches/0001-voxcpm2-4gb-ve-hiz.patch` i buduje
dla twojej karty (`-Mimari native`, domyślnie; albo np. `-Mimari 61`), ~15-25 min. Trzymaj krótki katalog główny (`C:\vox`):
nvcc zawodzi przy długich ścieżkach. Krok po kroku z kontrolami: [AGENTS.md](AGENTS.md).

### Częste problemy z instalacją

| Co widzisz | Co to znaczy, co zrobić |
|---|---|
| `cudart64_12.dll not found` po dwukliku na exe | Silnik nie jest przeznaczony do ręcznego uruchamiania. Uruchom powyższe polecenie `kur.ps1`, a potem interfejs webowy. |
| `64-bit Python 3.10+ bulunamadı` (nie znaleziono Pythona) | Zainstaluj Pythona (`winget install Python.Python.3.12`), zamknij PowerShell, otwórz nowy i uruchom to samo polecenie ponownie. |
| `motor ekran kartını görmedi` (silnik nie widzi karty graficznej) | Zaktualizuj sterownik NVIDIA do wersji 570 lub nowszej; sprawdź, czy `nvidia-smi` działa. |
| `indirme başarısız` / `sha256 tutmadı` (pobieranie nieudane / suma kontrolna się nie zgadza) | Zwykle to przerwane pobieranie. Uruchom to samo polecenie ponownie; zweryfikowane pliki są pomijane. |
| Budowanie: `nvcc` zawodzi | Trzymaj krótki katalog instalacji (`-Kok C:\vox`). |
| Strona się nie otwiera | Uruchom interfejs przez `baslat.bat` albo sam otwórz http://127.0.0.1:8765/. Port zajęty? Zmień `"port"` w `ayarlar.json`. |

Problemy? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) albo
[zgłoszenie problemu z instalacją](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
z podaniem karty, wersji Windows, polecenia i jego ostatnich wierszy.

## Użycie

Wiersz poleceń:
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
Zasady tekstu: liczby pisz słownie, bez cudzysłowów (narzędzie odrzuca cyfry i cudzysłowy), jedno zdanie w wierszu,
≤ 2000 znaków w wierszu. Pauza po wierszu: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s, `|| agir` 1,5 s
albo własna długość `|| 0,8` (0-5 s; cyfry w tym znaczniku są dozwolone). `ayarlar/okunus_sozlugu.tsv` poprawia wymowę obcych słów w tureckim tekście.
Język jest wykrywany z tekstu (tureckie litery, pismo, częste słowa; w razie wątpliwości `dil` z karty głosu; `--dil <code>` jest opcjonalne). W tekście nietureckim apostrofy są dozwolone, turecki słownik
jest pomijany, a cyfry nadal są odrzucane. Jeśli czytanie wypisze `speed gate: satır [...]`, odsłuchaj te wiersze.

### Interfejs webowy

Tylko lokalnie (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → sam otwórz http://127.0.0.1:8765/
(inny port: `--port 8800`) albo kliknij dwukrotnie `baslat.bat`. Serwer zatrzymasz przez Ctrl+C. Trzy karty: *Zaprojektuj głos*,
*Czytaj tym głosem*, *Klonowanie głosu*. Typowa ścieżka: *Projektuj* → odsłuchaj warianty → *Dodaj do mojej listy czytania* →
*Czytaj tym głosem* → pobierz. Albo wybierz dołączony głos z menu głosów i czytaj.

- **Wersja w nagłówku.** Mały, blady napis `v0.3.1 · <short commit>` (z `+`, gdy śledzone pliki mają niezatwierdzone
  zmiany; bez gita sama wersja), żeby na zrzutach ekranu i filmach było widać, której wersji użyto.
- **Dwa głosy na każdej karcie wariantu.** Na górze, na szaro, *Surowy głos projektu*: generowany jest raz i drugi raz nie
  wyjdzie taki sam. Pod nim, w pomarańczowej ramce, *↻ Ten głos będziesz słyszeć zawsze*: nagranie projektu przeczytane
  ponownie jako referencja z własnym ziarnem wariantu (widocznym na karcie). Tak brzmi głos w każdym późniejszym czytaniu.
  Pod spodem są *Czytaj tym głosem* i *Dodaj do mojej listy czytania*. Jedno naciśnięcie *Projektuj* robi oba kroki: projektuje wszystkie
  warianty, a potem czyta twój tekst każdym stałym głosem; jeden pasek postępu liczy obie fazy. Folder wariantu
  dostaje `dinleme.wav`. Jeśli to czytanie zatrzyma się przedwcześnie, projekt zostaje zachowany, a karta pokazuje uwagę.
- **Okno «Tekst, który chcesz usłyszeć».** W *Zaprojektuj głos* pole *↻ Tekst, który chcesz usłyszeć* zawiera to, co przeczyta każdy
  stały głos (jeśli zostawisz je puste, czytane jest przykładowe zdanie). Kliknięcie otwiera notatnik czytania w oknie: numery wierszy,
  menu wiersza, pasma pauz. *OK* zapisuje tekst i pauzy z powrotem w polu; *Anuluj* lub Esc niczego nie zmienia.
  Karta czytania ma własny tekst.
- **Notatnik czytania.** Jedno zdanie w wierszu. Kliknij numer wiersza, aby otworzyć menu wiersza (w górę lub w dół, przenieś na
  pozycję, duplikuj, usuń; Alt+↑/↓, Alt+Shift+↓ albo przeciągnij za numer; Ctrl+Z cofa tekst i pauzy razem).
  Kliknij cienkie pasmo między dwoma wierszami, aby wybrać pauzę (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s albo
  własna 0-5 s przez zębatkę); dwukrotne Enter daje akapit (1 s), a puste wiersze stają się pasmami pauz. Podczas odtwarzania
  wyniku czytany wiersz się podświetla i przewija do widoku; *▶ Odsłuchaj od tego miejsca* w menu wiersza odtwarza od tego wiersza.
  Tekst i pauzy przetrwają przeładowanie strony (pamięć przeglądarki).
- **Szkice.** Przycisk *📄 Szkice* jest w obu notatnikach (karta czytania i okno). Zapisz bieżący tekst z pauzami
  jako szkic, wczytaj szkic jednym kliknięciem (Ctrl+Z cofa) i użyj ⋯, aby go nadpisać, zmienić nazwę lub usunąć. Szkice są
  przechowywane w `sesler/taslaklar.json`, nigdy w repozytorium.
- **Lista czytania i menu głosów.** Na karcie wariantu *Dodaj do mojej listy czytania* otwiera pole nazwy: nadaj wariantowi
  własną nazwę, a ✓ go doda. *Nazwa generacji* pozostaje przy każdym wariancie z tego uruchomienia. W *Czytaj tym głosem* przycisk
  głosu (flaga + nazwa) otwiera menu głosów: na górze *Moja lista czytania*, potem dołączone głosy z flagami (najpierw język
  interfejsu). Każdy wiersz ma ▶ odsłuchaj (stały głos, jeśli istnieje), serce (dodaj lub usuń) i ⋯; ↑/↓ i
  Enter wybierają, Esc zamyka, ostatni głos jest zapamiętywany. Lista jest w `sesler/okuma_listesi.json`, poza
  repozytorium, i przetrwa ponowne uruchomienie.
- **Zarządzanie głosami.** Menu ⋯ (wiersz menu głosów lub karta wariantu) zawiera *Czytaj tym głosem*, dodanie do listy lub usunięcie z niej,
  *Zmień nazwę* (pusta nazwa przywraca oryginalną; *Przywróć pierwotną nazwę*), *Usuń* dla zaprojektowanych głosów i *Ukryj*
  dla dołączonych; obie akcje najpierw pytają. Usunięty głos trafia do `sesler/_cop/`; ukrywanie nigdy nie zmienia plików repozytorium.
  *Ukryte i usunięte głosy (N)* na dole menu głosów ma *Przywróć*. Własne nazwy i ukryte głosy są przechowywane
  w `sesler/yerel_katman.json`. Głos ze zmienioną nazwą pokazuje na szaro swoje pochodzenie (*nazwa generacji · wariant N*); ⋯ → *Przejdź do
  generacji* otwiera jego projekt.
- **Skróty i pliki.** Ctrl+Enter (⌘+Enter na Macu) uruchamia *Projektuj* lub *Czytaj tym głosem* na otwartej karcie.
  Pasek postępu pokazuje *upłynęło / ~łącznie*, z szacunkiem wyuczonym na wcześniejszych zadaniach na twoim komputerze. Pobrany plik
  ma nazwę od głosu i czasu (`Voice_Name_2026-11-02_0152.wav`).

**Klonowanie głosu (twojego własnego lub za zgodą).** Na karcie *Klonowanie głosu* podaj swoje nagranie (wav/mp3/flac/ogg, zalecane 5-30 s czystej mowy; poniżej 3 s jest odrzucane, powyżej 36 s przycinane), jego dokładną transkrypcję i tekst do przeczytania. Przycisk pozostaje nieaktywny, dopóki nie zaznaczysz «Ten głos należy do mnie lub mam wyraźną zgodę właściciela». Nagranie trafia tylko do lokalnego serwera (127.0.0.1), jest przetwarzane w folderze tymczasowym razem z jego kodowaniem referencyjnym, a folder ten jest usuwany po zakończeniu zadania, także gdy zadanie się nie powiedzie; nic nie jest wysyłane przez sieć. Zachowywany jest tylko syntetyczny wynik (interfejs: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Wynik to `klon_synthetic.wav` ze znacznikiem «synthetic»; udostępniając go, oznacz go jako wygenerowany przez AI. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## FAQ

**Model czy silnik? Co jest czym?** VoxCPM2 (OpenBMB) to *model*: sieć o 2 miliardach parametrów, która zamienia tekst
na mowę. audio.cpp to *silnik*: program w C++/CUDA, który uruchamia model na twojej karcie (`audiocpp_cli.exe`). Nasza
łatka zmienia silnik, nie model: sprawia, że VoxCPM2 mieści się w 4 GB, a to samo ziarno za każdym razem daje ten sam
dźwięk. Pakiet Pythona w tym repozytorium tylko przygotowuje tekst, wywołuje silnik i zbiera pliki.

**Jakie karty?** Zobacz «Obsługiwane karty» powyżej: NVIDIA od GTX 10xx wzwyż, 4 GB VRAM lub więcej, sterownik ≥ 570. Wydanie
zawiera natywny kod dla sm_61/75/86/89/120a; inne karty od Pascala wzwyż używają wbudowanego PTX (wolniejszy pierwszy start). AMD/Intel: eksperymentalny zip Vulkan, `kur.ps1 -Vulkan`; przetestowany przez nas na zintegrowanej Intel HD Graphics 630; @mitraTR uruchomił wcześniejszą v0.1.1 na AMD RX 6900 XT, nowych pakietów v0.3.1 nie próbowano jeszcze na AMD (zobacz «AMD / Intel» powyżej). Tryb tylko z CPU (`"backend": "cpu"` w `ayarlar.json`) działa, ale jest
~6× wolniejszy niż GTX 1050 Ti (pomiar silnika: 535 s wobec 94 s dla 48 s mowy); to nie jest obsługiwana ścieżka.

**Jak szybko?** Zmierzone na GTX 1050 Ti 4 GB (i7-7700HQ): jeden wariant projektu (nagranie ≈ 25 s) 55 s; czytanie ≈ 2 s
obliczeń na 1 s mowy (współczynnik czasu rzeczywistego 1,9-2,8) po jednorazowym ~50 s kodowaniu referencji na głos (w pamięci
podręcznej na dysku) i 10-20 s wczytywania modelu na partię; szczyt VRAM 2,6-2,9 GB. Nowsze karty są szybsze; liczby i metoda:
[docs/4gb.md](docs/4gb.md).

**Czy może sklonować głos?** Bazowy model VoxCPM2 potrafi naśladować głos na podstawie nagrania referencyjnego i sekcja
klonowania z tego korzysta. Używaj jej tylko z własnym głosem albo za wyraźną zgodą osoby, do której głos należy;
interfejs prosi o potwierdzenie tej zgody. Projektowanie głosu nie wymaga nagrania: zaczyna się od opisu tekstowego po angielsku lub chińsku, a
«referencja» używana do czytania zaprojektowanym głosem to własne syntetyczne nagranie projektu stworzone przez model. Podszywanie się,
oszustwa i wprowadzanie w błąd są zabronione. Zobacz [ETHICS.md](ETHICS.md). Oznaczaj to, co publikujesz, jako wygenerowane przez AI.

**Jak napisać dobry opis głosu?** Po angielsku, 1-3 zdania: wiek i płeć, barwa (głęboka/jasna, ciepła,
nosowa, chrapliwa), ton i rola (spokojny lektor dokumentalny, energiczny prezenter), tempo (wolne, miarowe) oraz
«clean studio recording, no background noise». To ma być opis, nie scenariusz; bez nawiasów. Poproś o 3-5
wariantów i odsłuchaj: ziarno mocno zmienia głos. Jako tekst tworzenia użyj 1-3 naturalnych zdań w języku głosu,
w pożądanym nastroju (najwyżej ~30 s mowy). Przy czytaniu jedno zdanie w wierszu; dziel długie zdania, liczby pisz słownie.

## Jak pomóc

Nie wiesz, od czego zacząć? Te cztery małe zgłoszenia to dobry pierwszy krok:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Wypróbuj na swojej karcie i podaj model karty, sterownik i czasy
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: wypróbuj eksperymentalną wersję Vulkan
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Dodaj zdanie do zestawu testowego
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Podziel się zaprojektowanym głosem, razem z opisem i ziarnem

**Przetestuj swoją kartę i napisz raport:** nie musisz programować, wystarczy [formularz raportu z testu sprzętu](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); zintegrowaną Intel HD Graphics 630 przetestowaliśmy sami; z Intel Arc nie mamy jeszcze raportu, z AMD dla v0.3.1 również.

Wspólny zestaw testowy: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); przewodnik po głosie marki:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); jak przesłać kod: [CONTRIBUTING.md](CONTRIBUTING.md).
Problemy z instalacją: [formularz zgłoszenia](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); pytania i wyniki: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Wszyscy uczestnicy przestrzegają [Kodeksu postępowania](CODE_OF_CONDUCT.md): bądź życzliwy, a uwagi kieruj do pracy, nie do ludzi.

## Współtwórcy

- [@alexturkey](https://github.com/alexturkey): opiekun projektu; kod, dołączone głosy, dokumentacja
- [@cayir21](https://github.com/cayir21): obsługa Metal w macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): poprawka końca zdania (EOS) przy czytaniu wielu zdań na backendzie CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): eksperymentalna instalacja CUDA dla Ubuntu/Linux i obsługa Dockera, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Twoje nazwisko też może się tu znaleźć: wynik testu z twojej karty, zdanie do zestawu testowego, zaprojektowany przez ciebie głos,
jasny raport o błędzie albo pull request, wszystko to liczy się jako wkład. Dziękujemy wszystkim, którzy próbują i dają znać.

## Licencja i podziękowania

Kod i dołączone głosy: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Zbudowane na VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) i konwersji GGUF audio.cpp. Pełna lista: [THIRD_PARTY.md](THIRD_PARTY.md).
Projekt nie jest powiązany z OpenBMB, ModelBest ani projektem audio.cpp.

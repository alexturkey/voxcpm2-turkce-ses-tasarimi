[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · **Italiano** · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Voice design in turco con VoxCPM2 su una GPU da 4 GB.** Descrivi una voce in inglese, lascia che il modello la crei,
scegli la variante che ti piace e poi leggi qualsiasi testo turco con quella voce. Il progetto include un installer a
comando singolo, un motore [audio.cpp](https://github.com/0xShug0/audio.cpp) con patch che entra in una GTX 1050 Ti
(4 GB), una piccola interfaccia web locale e quattordici voci sintetiche pronte all'uso: sette turche e sette narratori
madrelingua in inglese, francese, tedesco, spagnolo, russo, cinese e giapponese.

- L'app legge in 30 lingue; anche l'interfaccia è disponibile in 30 lingue.
- 14 voci pronte all'uso: 7 turche, più una ciascuna in inglese, francese, tedesco, spagnolo, russo, cinese e giapponese.
- Interfaccia web (v0.2.0): ogni scheda di variante ha due voci, la voce di design grezza e la voce che sentirai
  sempre; una lista di lettura con menu delle voci; rinomina, nascondi o elimina le voci; bozze per i testi che leggi.
  Vedi «Interfaccia web» in «Utilizzo».

[Come ci sta in 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Guida all'installazione per agenti IA](AGENTS.md) · [Uso responsabile](ETHICS.md)

> Le voci incluse sono sintetiche, progettate a partire da una descrizione testuale. La sezione di clonazione vocale è
> riservata alla tua voce o a una voce usata con il permesso esplicito del proprietario; l'interfaccia ti chiede di
> confermare questo permesso. Sono vietati furto d'identità, frode e inganno. Indica che ciò che generi è prodotto con
> l'IA. Vedi [ETHICS.md](ETHICS.md).

## 30 lingue

Abbiamo realizzato un video documentario sulla Cappadocia in 8 lingue: turco, inglese, francese, tedesco, spagnolo,
russo, cinese e giapponese. Ogni lingua ha il suo **narratore madrelingua**, progettato con VoxCPM2 a partire da una
descrizione in inglese. Tutto è stato generato interamente in locale su una GTX 1050 Ti da 4 GB, con la stessa qualità
fissa (16 passi, cfg 2.0). I sette narratori sono inclusi qui, con prompt, testo di design, seed e registrazione di
riferimento.

| Codice | Lingua | Voce | Ascolta | Video |
|---|---|---|---|---|
| `tr` | Turco | `hazir/belgesel_hanim` (e altre 6) | [esempio](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Inglese | `hazir/anlatici_en` | [esempio](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Francese | `hazir/anlatici_fr` | [esempio](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Tedesco | `hazir/anlatici_de` | [esempio](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Spagnolo | `hazir/anlatici_es` | [esempio](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Russo | `hazir/anlatici_ru` | [esempio](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Cinese (mandarino) | `hazir/anlatici_zh` | [esempio](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Giapponese | `hazir/anlatici_ja` | [esempio](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Perché frase per frase.** VoxCPM2 non è stabile in una singola generazione lunga (oltre i 30 secondi circa): il ritmo
accelera e la voce può derivare. Qui la voce è sostenuta da una registrazione di riferimento e da un seed fissi, e il
testo lungo viene letto una frase per riga, così timbro e stile restano uguali dalla prima all'ultima frase. Per le
lingue diverse dal turco il dizionario di pronuncia turco non viene applicato. Tutte le 30 lingue supportate da VoxCPM2
sono state provate e funzionano; per quelle senza una voce inclusa usa `--dil <code>`. Comandi per ogni lingua e lezioni
imparate: [docs/cok_dilli.md](docs/cok_dilli.md). Skill di Claude Code per l'intero flusso di design:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 prompt di esempio da cui partire.** 18 ruoli (narratore di documentari, conduttore di telegiornale, voce
pubblicitaria, audiolibro, nonna cantastorie, conduttore di podcast, insegnante, trailer cinematografico, guida alla
meditazione, telecronista sportivo e altri, maschili e femminili) in ciascuna delle 8 lingue. Il prompt è in inglese e
indica nazionalità e accento nativo di chi parla; il testo letto durante la creazione della voce è già incluso, nella
lingua corrispondente e adatto al ruolo. Scegline uno, ascolta le varianti e tieni quella che ti piace:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, oppure scegli *Modello di esempio*
nell'interfaccia web. Elenco completo: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Doppia i tuoi video con la tua voce.** [DubWorld](https://github.com/alexturkey/dubworld) è il nostro programma locale
di doppiaggio video; installa questo repository come motore vocale VoxCPM2. Una voce progettata qui si usa lì con
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Avvio rapido (Windows, 3 passi)

1. **Scarica** il codice: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Il pacchetto del motore già pronto per la tua scheda viene scaricato dall'installer al passo 3:
   NVIDIA → [pacchetto CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [pacchetto Vulkan, sperimentale](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (ne hai già scaricato uno? aggiungi `-HazirZip <path to the zip>` al comando qui sotto).
2. **Estrai** lo zip, apri la cartella `voxcpm2-turkce-ses-tasarimi-main`, digita `powershell` nella barra degli
   indirizzi di Esplora file e premi Invio.
3. **Esegui** l'installer (richiede Python 3.10-3.13 a 64 bit; driver NVIDIA ≥ 570 per CUDA), poi fai doppio clic su **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: aggiungi `-Vulkan` alla fine. L'interfaccia si apre su http://127.0.0.1:8765/.

Lo zip del motore non è un'app autonoma (il suo exe ha bisogno del modello e delle DLL che l'installer predispone).
Dettagli, elenco delle GPU e problemi comuni: «Installazione rapida» più sotto.

## Ubuntu / Linux (NVIDIA CUDA, sperimentale)

Compila il motore con patch con `bash scripts/kur-linux.sh`, oppure usa `Dockerfile.linux` per compilare ed eseguire in
un ambiente Ubuntu 24.04 / CUDA 12.8.1. Servono una GPU NVIDIA e un driver compatibile; l'installer nativo richiede
anche il CUDA Toolkit e Python 3.10-3.13. L'interfaccia resta solo su loopback, anche sui server remoti (inoltro SSH).
Prerequisiti, comandi, scelta dell'architettura e ambito della validazione: [docs/linux.md](docs/linux.md).

## Avvio rapido (macOS, Apple Silicon)

Servono gli Xcode Command Line Tools (`xcode-select --install`) e [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
L'installer scarica il modello, compila il motore con patch con Metal (~1 min) e prepara tutto in `~/vox`. Poi fai
doppio clic su **`baslat.command`**. Su un MacBook Air M4 da 16 GB: ~2 s di calcolo per 1 s di parlato, lo stesso seed
dà un audio identico byte per byte, picco di ~5,3 GB di RAM, nessun rallentamento termico in 12 min di lettura
continua. Dettagli e misure: [docs/mac.md](docs/mac.md).

**App nativa per Mac (senza Python, Homebrew o Terminale):** [macos/README.md](macos/README.md). Include lo stesso
motore con patch e scarica il modello al primo avvio; per ora si compila dal sorgente con Xcode.

## Per chi usa Mac (Apple Silicon)

Esiste anche un adattamento indipendente, realizzato dalla community, per i Mac con Apple Silicon che esegue VoxCPM2 con
il framework MLX di Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
È sviluppato e mantenuto da Emre Koç ([@emre-koc](https://github.com/emre-koc)) nel suo repository, non qui; i passi di
installazione e le richieste di supporto vanno lì. Grazie, Emre, per aver portato questo progetto su Mac!

## Come funziona

1. **Design della voce.** Una *descrizione della voce* in inglese + un *testo letto durante la creazione della voce*
   (nella lingua della voce) + un numero di varianti. Ogni variante riceve il proprio seed; il motore riceve
   `(description)text` e restituisce una registrazione di design per ogni seed. Il testo è un breve campione per
   conoscere la voce: 1-2 frasi, al massimo ~20 s (l'interfaccia mostra la stima e non parte oltre i 22 s); il testo
   lungo va al passo 2.
2. **Lettura basata sul riferimento.** La registrazione di design viene passata a **entrambi** gli ingressi del motore
   (`audio` e `voice_ref`), insieme alla sua trascrizione (`reference_text`) e al nuovo testo da leggere, con lo stesso
   seed. La voce è sostenuta dalla registrazione, non dalla descrizione, quindi non deriva da un testo all'altro. Il
   testo viene letto frase per frase.
3. La qualità è fissa: 16 passi di diffusione, CFG 2.0. Il seed non è una manopola della qualità.

La registrazione di design grezza è un campione unico della voce; nessuna lettura successiva suona esattamente uguale.
Ciò che senti in ogni lettura successiva è il passo 2: la registrazione di design come riferimento più il seed proprio
della variante. Per questo l'interfaccia web esegue il passo 2 subito dopo il design e mostra entrambe sulla scheda
della variante.

Il motore è audio.cpp v0.7.2 con la nostra patch (`patches/`), il modello è VoxCPM2 Q8_0 GGUF. Picco di VRAM ≈ 2,8 GB;
circa 2 s di calcolo per 1 s di parlato su una GTX 1050 Ti. Dettagli e misure: [docs/4gb.md](docs/4gb.md).

## Voci incluse (`hazir_sesler/`)

Tutte e quattordici sono state progettate a partire dai prompt salvati nel loro `ses.json`; nessuna è stata clonata da
una registrazione (la clonazione è la scheda separata *Clonazione vocale*, vincolata al consenso).

| Voce | Breve descrizione | Ascolta |
|---|---|---|
| `belgesel_hanim` | Donna matura sulla cinquantina, contralto profondo e caldo; narratrice di documentari pacata | [esempio](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [riferimento](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Narratore maschile profondo, potente, misterioso | [esempio](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [riferimento](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Esperto conduttore di telegiornale sulla settantina, calmo e autorevole | [esempio](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [riferimento](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Carismatica conduttrice del telegiornale della sera sulla trentina, vellutata ed espressiva | [esempio](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [riferimento](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Strega delle fiabe: bassa, leggermente nasale, di una dolcezza sorniona | [esempio](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [riferimento](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Narratore maschile eccezionalmente profondo, denso, autoritario | [esempio](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [riferimento](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Vecchio saggio, voce profonda e tonante, un po' misteriosa | [esempio](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [riferimento](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Narratore di documentari madrelingua inglese sulla cinquantina (General American); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Narratore di documentari madrelingua francese sulla cinquantina (parigino); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Narratore di documentari madrelingua tedesco sulla cinquantina (Hochdeutsch); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Narratore di documentari madrelingua spagnolo sulla cinquantina (castigliano (Madrid)); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Narratore di documentari madrelingua russo sulla cinquantina (Mosca); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Narratore di documentari madrelingua cinese (mandarino) sulla cinquantina (putonghua di Pechino); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Narratore di documentari madrelingua giapponese sulla cinquantina (giapponese standard di Tokyo); profondo, calmo, caldo | [esempio](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [riferimento](hazir_sesler/anlatici_ja/referans.flac) |

Ogni cartella contiene: `referans.flac` (registrazione di design senza perdita), `ses.json` (prompt, trascrizione, seed
di design, seed di lettura, descrizione; `dil` = lingua, per i narratori), `ornek_okuma.mp3` (+ il suo testo). Usale
direttamente: `--ses hazir/<name>`. Le registrazioni di riferimento dei narratori sono brevi (5,6-10 s); i loro esempi
sono le prime tre frasi del copione sulla Cappadocia, tagliate dalla lettura completa della produzione.

## Installazione rapida, senza compilatore (Windows 10/11, GPU NVIDIA ≥ 4 GB)

Prerequisiti: driver NVIDIA ≥ 570 e Python 3.10-3.13 a 64 bit (`winget install Python.Python.3.12`). Nient'altro:
niente Visual Studio, niente installer CUDA. Non sai quale scheda hai? Esegui `nvidia-smi` in PowerShell: mostra il
nome della GPU, la versione del driver e la memoria. Nessuna scheda NVIDIA? Vedi «AMD / Intel» più sotto.

Con [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Senza Git: in questa pagina fai clic su **Code → Download ZIP**, estrai l'archivio, apri la cartella estratta
`voxcpm2-turkce-ses-tasarimi-main`, digita `powershell` nella barra degli indirizzi di Esplora file, premi Invio e poi
esegui l'ultima riga qui sopra. Git serve solo per la compilazione dal sorgente.

`-ExecutionPolicy Bypass` vale solo per questo processo e non modifica alcuna impostazione di sistema; leggi
`scripts\kur.ps1` prima di eseguirlo, come per qualsiasi script di installazione. Un comando, ~10 min, ~3,7 GB di
download, tutto verificato con sha256: il modello (2,95 GB), le DLL di runtime di CUDA 12.8 come zip portabili (nessuna
installazione di sistema, PATH invariato), il **motore precompilato** dalla pagina Releases, un `.venv` con i due
pacchetti Python, `ayarlar.json` e un controllo finale della GPU (`KONTROL_OK`). Dopo un errore basta rieseguirlo; i
file già verificati vengono saltati. Poi avvia l'interfaccia web: fai doppio clic su **`baslat.bat`** nella cartella del
repository. Avvia l'interfaccia e apre **http://127.0.0.1:8765/** nel browser quando è pronta; chiudi la finestra nera
(o premi Ctrl+C al suo interno) per fermarla. Lo stesso da PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
poi apri tu **http://127.0.0.1:8765/** (avviata così, l'interfaccia non apre il browser; ascolta solo su localhost).

> **L'`audiocpp_cli.exe` contenuto nello zip della release non va aperto con un doppio clic.** È un motore a riga di
> comando che ha bisogno delle DLL CUDA e del modello accanto a sé; `kur.ps1` mette tutto al posto giusto e il
> pacchetto Python lo pilota. Con un doppio clic compare solo «cudart64_12.dll not found».

**GPU supportate (release v0.1.1):** codice nativo per GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) e RTX 50xx (sm_120a); qualsiasi altra GPU CUDA da Pascal in poi esegue il PTX incorporato tramite il driver
(primo avvio più lento). Maxwell (GTX 9xx) e precedenti non sono supportate da CUDA 12.8. Provato da noi su una
GTX 1050 Ti 4 GB (anche tramite Docker Desktop/WSL2 su Windows, solo CLI); misurato da @mslmyilmaz5 (#15):
RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (dettagli in [docs/linux.md](docs/linux.md)). Le segnalazioni da
altre schede sono benvenute nelle [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (sperimentale):** uno zip separato del motore Vulkan (`...-win64-vulkan.zip`, senza CUDA) si installa con
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. È verificato solo sulla nostra scheda NVIDIA tramite il backend Vulkan (lì è
risultato più lento di CUDA ma ha dato lo stesso audio con lo stesso seed; quella misura è stata presa mentre il disco
era occupato da un altro lavoro, quindi un confronto di velocità pulito è ancora da fare) e **non** lo abbiamo provato
di persona su hardware AMD o Intel: se lo provi, pubblica il risultato nelle Discussions. Con più di un dispositivo
Vulkan (integrato + dedicato) l'installer scrive l'indice della GPU dedicata come `cihaz` in `ayarlar.json`.

*Nota: il supporto Vulkan è attualmente sperimentale. È stato compilato e provato con successo su una GTX 1050 Ti. Inoltre
un utente esterno (mitra_tr) ha segnalato di averlo fatto funzionare su una AMD 6900 XT. Servono ancora test più ampi
sulle schede AMD/Intel.*

### Alternativa: compilare il motore dal sorgente

Servono i Build Tools di Visual Studio 2022 con «Sviluppo di applicazioni desktop con C++» (inclusi gli strumenti CMake
C++), ~7 GB. Poi:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Questo scarica anche nvcc, recupera il sorgente di audio.cpp v0.7.2, applica `patches/0001-voxcpm2-4gb-ve-hiz.patch` e
compila per la tua GPU (`-Mimari native`, predefinito; oppure ad es. `-Mimari 61`), ~15-25 min. Tieni corta la radice
(`C:\vox`): nvcc fallisce con i percorsi lunghi. Passo per passo, con verifiche: [AGENTS.md](AGENTS.md).

### Problemi di installazione comuni

| Vedi | Cosa significa, cosa fare |
|---|---|
| `cudart64_12.dll not found` dopo il doppio clic sull'exe | Il motore non va avviato a mano. Esegui il comando `kur.ps1` qui sopra, poi avvia l'interfaccia web. |
| `64-bit Python 3.10+ bulunamadı` (Python non trovato) | Installa Python (`winget install Python.Python.3.12`), chiudi PowerShell, aprine uno nuovo ed esegui di nuovo lo stesso comando. |
| `motor ekran kartını görmedi` (il motore non ha visto la GPU) | Aggiorna il driver NVIDIA alla versione 570 o successiva; controlla che `nvidia-smi` funzioni. |
| `indirme başarısız` / `sha256 tutmadı` (download non riuscito / checksum non corrispondente) | Di solito un download interrotto. Esegui di nuovo lo stesso comando; i file già verificati vengono saltati. |
| Compilazione dal sorgente: `nvcc` fallisce | Tieni corta la radice di installazione (`-Kok C:\vox`). |
| La pagina non si apre | Avvia l'interfaccia con `baslat.bat`, oppure apri tu http://127.0.0.1:8765/. Porta occupata? Cambia `"port"` in `ayarlar.json`. |

Problemi? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) oppure una
[issue di installazione](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
con la tua GPU, la versione di Windows, il comando e le sue ultime righe.

## Utilizzo

Riga di comando:
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
Regole per il testo: scrivi i numeri in lettere, niente virgolette (lo strumento rifiuta cifre e virgolette), una frase
per riga, ≤ 2000 caratteri per riga. Pausa dopo una riga: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s,
`|| agir` 1,5 s oppure una durata a scelta `|| 0,8` (0-5 s; le cifre del marcatore sono ammesse).
`ayarlar/okunus_sozlugu.tsv` corregge la pronuncia delle parole straniere nel testo turco. La lingua viene rilevata dal
testo (lettere turche, sistema di scrittura, parole comuni; in caso di dubbio il `dil` della scheda della voce;
`--dil <code>` è facoltativo). Per il testo non turco lì gli apostrofi sono ammessi, il dizionario turco viene saltato e
le cifre restano rifiutate. Se una lettura stampa `speed gate: satır [...]`, ascolta quelle righe.

### Interfaccia web

Solo in locale (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → apri tu http://127.0.0.1:8765/ (altra
porta: `--port 8800`), oppure fai doppio clic su `baslat.bat`. Ferma il server con Ctrl+C. Tre schede: *Progetta una
voce*, *Leggi con questa voce*, *Clonazione vocale*. Il percorso abituale: *Progetta* → ascolta le varianti →
*Aggiungi alla mia lista di lettura* → *Leggi con questa voce* → scarica. Oppure scegli una voce inclusa dal menu delle
voci e leggi.

- **Versione nell'intestazione.** Un piccolo `v0.2.0 · <short commit>` sbiadito (con `+` quando i file tracciati hanno
  modifiche non committate; senza git, solo la versione), così screenshot e video mostrano quale versione è stata usata.
- **Due voci su ogni scheda di variante.** In alto, in grigio, la *Voce di design grezza*: viene generata una sola volta
  e non esce mai più uguale. Sotto, in una cornice arancione, *↻ Questa è la voce che sentirai sempre*: la
  registrazione di design riletta come riferimento con il seed proprio della variante (mostrato sulla scheda). Così
  suonerà la voce in ogni lettura successiva. Sotto ci sono *Leggi con questa voce* e *Aggiungi alla mia lista di
  lettura*. Una sola pressione su *Progetta* fa entrambe le cose: progetta ogni variante, poi legge il tuo testo con
  ogni voce duratura; un'unica barra di avanzamento conta entrambe le fasi. La cartella della variante riceve
  `dinleme.wav`. Se quella lettura si interrompe prima del tempo, il design viene conservato e la scheda mostra una
  nota.
- **La finestra «Testo che vuoi ascoltare».** In *Progetta una voce*, la casella *↻ Testo che vuoi ascoltare* contiene
  ciò che legge ogni voce duratura (se resta vuota, viene letta la frase di esempio). Un clic sulla casella apre il
  quaderno di lettura in una finestra: numeri di riga, menu di riga, bande di pausa. *OK* riscrive il testo e le sue
  pause nella casella; *Annulla* o Esc non cambiano nulla. La scheda di lettura mantiene il proprio testo.
- **Il quaderno di lettura.** Una frase per riga. Fai clic su un numero di riga per il menu di riga (sposta su o giù,
  sposta in una posizione, duplica, elimina; Alt+↑/↓, Alt+Maiusc+↓, oppure trascina dal numero; Ctrl+Z annulla insieme
  testo e pause). Fai clic sulla sottile banda tra due righe per scegliere la pausa (bagli 0,25 · normal 0,5 ·
  paragraf 1 · agir 1,5 s, oppure una durata a scelta di 0-5 s con l'ingranaggio); premi Invio due volte per un
  paragrafo (1 s), e le righe vuote diventano bande di pausa. Mentre il risultato è in riproduzione, la riga in lettura
  si illumina e scorre in vista; *▶ Ascolta da qui* nel menu di riga riproduce da quella riga. Il testo e le sue pause
  sopravvivono al ricaricamento della pagina (memoria del browser).
- **Bozze.** Il pulsante *📄 Bozze* si trova in entrambi i quaderni (scheda di lettura e finestra). Salva il testo
  corrente con le sue pause come bozza, caricane una con un clic (Ctrl+Z annulla) e usa ⋯ per sovrascriverla,
  rinominarla o eliminarla. Le bozze sono salvate in `sesler/taslaklar.json`, mai nel repository.
- **Lista di lettura e menu delle voci.** Su una scheda di variante, *Aggiungi alla mia lista di lettura* apre una
  casella per il nome: dai alla variante un nome tutto suo e ✓ la aggiunge. Il *Nome della generazione* resta su ogni
  variante di quell'esecuzione. In *Leggi con questa voce*, il pulsante della voce (bandiera + nome) apre il menu delle
  voci: in alto *La mia lista di lettura*, poi le voci incluse con le bandiere (prima la lingua dell'interfaccia). Ogni
  riga ha ▶ ascolta (la voce duratura, se c'è), il cuore (aggiungi o rimuovi) e ⋯; ↑/↓ e Invio scelgono, Esc chiude,
  l'ultima voce viene ricordata. La lista si trova in `sesler/okuma_listesi.json`, fuori dal repository, e sopravvive ai
  riavvii.
- **Gestire le voci.** Il menu ⋯ (riga del menu delle voci o scheda di variante) offre *Leggi con questa voce*,
  aggiungi alla lista o rimuovi, *Rinomina* (un nome vuoto ripristina l'originale; *Torna al nome originale*),
  *Elimina* per le voci progettate e *Nascondi* per quelle incluse; entrambe chiedono conferma. Una voce eliminata
  finisce in `sesler/_cop/`; nascondere non tocca mai i file del repository. *Voci nascoste ed eliminate (N)*, in fondo
  al menu delle voci, offre *Ripristina*. I nomi personalizzati e le voci nascoste sono salvati in
  `sesler/yerel_katman.json`. Una voce rinominata mostra la sua origine in grigio (*nome della generazione ·
  variante N*); ⋯ → *Vai alla generazione* apre il suo design.
- **Scorciatoie e file.** Ctrl+Invio (⌘+Invio su Mac) avvia *Progetta* o *Leggi con questa voce* nella scheda aperta.
  La barra di avanzamento mostra *trascorso / ~totale*, con una stima appresa dai lavori precedenti sul tuo computer. Il
  file scaricato prende il nome dalla voce e dall'ora (`Voice_Name_2026-11-02_0152.wav`).

**Clonazione vocale (la tua voce o una voce autorizzata).** Nella scheda *Clonazione vocale* dell'interfaccia fornisci
la tua registrazione (wav/mp3/flac/ogg, consigliati 5-30 s di parlato pulito; sotto i 3 s viene rifiutata, oltre i 36 s
viene tagliata), la sua trascrizione esatta e il testo da leggere. Il pulsante resta disattivato finché non spunti
«Questa voce è mia o ho il permesso esplicito del proprietario». La registrazione va solo al server locale
(127.0.0.1), viene elaborata in una cartella temporanea insieme alla sua codifica di riferimento, e quella cartella
viene eliminata al termine del lavoro, anche in caso di errore; nulla viene inviato in rete. Si conserva solo l'output
sintetico (interfaccia: `sesler/_okumalar/<job>/`, CLI: `--cikti`). L'output è `klon_synthetic.wav` con un'etichetta
«synthetic»; quando lo condividi, indica che è generato con l'IA. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Domande frequenti

**Modello o motore? Che cos'è cosa?** VoxCPM2 (OpenBMB) è il *modello*: la rete da 2 miliardi di parametri che
trasforma il testo in parlato. audio.cpp è il *motore*: il programma C++/CUDA che esegue il modello sulla tua GPU
(`audiocpp_cli.exe`). La nostra patch modifica il motore, non il modello: fa entrare VoxCPM2 in 4 GB e fa sì che lo
stesso seed dia ogni volta lo stesso audio. Il pacchetto Python di questo repository si limita a preparare il testo,
chiamare il motore e raccogliere i file.

**Quali GPU?** Vedi «GPU supportate» più sopra: NVIDIA dalla GTX 10xx in su, 4 GB di VRAM o più, driver ≥ 570. La
release contiene codice nativo per sm_61/75/86/89/120a; le altre schede Pascal o più recenti usano il PTX incorporato
(primo avvio più lento). AMD/Intel: zip Vulkan sperimentale, `kur.ps1 -Vulkan`; un utente esterno ha segnalato di
averlo fatto funzionare su una AMD 6900 XT, ma servono ancora test più ampi su AMD/Intel (vedi «AMD / Intel» più
sopra). Solo CPU (`"backend": "cpu"` in `ayarlar.json`) funziona, ma è ~6× più lento di una GTX 1050 Ti (misura del
motore, 535 s contro 94 s per 48 s di parlato); non è un percorso supportato.

**Quanto è veloce?** Misurato su una GTX 1050 Ti 4 GB (i7-7700HQ): una variante di design (registrazione di ≈ 25 s) in
55 s; lettura ≈ 2 s di calcolo per 1 s di parlato (fattore di tempo reale 1,9-2,8) dopo una codifica di riferimento una
tantum di ~50 s per voce (in cache su disco) e 10-20 s di caricamento del modello per ogni lotto; picco di VRAM
2,6-2,9 GB. Le schede più recenti sono più veloci; numeri e metodo: [docs/4gb.md](docs/4gb.md).

**Può clonare una voce?** Il modello VoxCPM2 sottostante può imitare una voce a partire da una registrazione di
riferimento, e la sezione di clonazione sfrutta questa capacità. Usala solo con la tua voce o con il permesso esplicito
della persona a cui appartiene la voce; l'interfaccia ti chiede di confermare questo permesso. Il design vocale non
richiede alcuna registrazione: parte da una descrizione testuale in inglese o in cinese, e il «riferimento» usato per
leggere con una voce progettata è la registrazione di design sintetica prodotta dal modello stesso. Sono vietati furto
d'identità, frode e inganno. Vedi [ETHICS.md](ETHICS.md). Indica che ciò che pubblichi è generato con l'IA.

**Come scrivo una buona descrizione della voce?** In inglese, 1-3 frasi: età e genere, timbro (profondo/brillante,
caldo, nasale, roco), tono e ruolo (narratore di documentari pacato, presentatore energico), tempo (lento, misurato) e
«clean studio recording, no background noise». Che resti una descrizione, non un copione; niente parentesi. Chiedi 3-5
varianti e ascoltale: il seed cambia molto la voce. Per il testo di creazione usa 1-2 frasi naturali nella lingua della
voce, con lo stato d'animo che desideri (al massimo ~20 s di parlato). In lettura, una frase per riga; spezza le frasi
lunghe, scrivi i numeri in lettere.

## Contribuire

Non sai da dove cominciare? Queste quattro piccole issue sono un buon primo passo:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Provalo sulla tua GPU e segnala scheda, driver e tempi
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: prova la build Vulkan sperimentale
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Aggiungi una frase al set di test
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Condividi una voce che hai progettato, con la sua descrizione e il seed

Set di test condiviso: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); guida alla voce del brand:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); come inviare codice: [CONTRIBUTING.md](CONTRIBUTING.md).
Problemi di installazione: [modulo issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); domande e risultati: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Chiunque partecipi segue il [Codice di condotta](CODE_OF_CONDUCT.md): sii gentile e mantieni i commenti sul lavoro.

## Contributori

- [@alexturkey](https://github.com/alexturkey): maintainer; codice, voci incluse, documentazione
- [@cayir21](https://github.com/cayir21): supporto Metal per macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): correzione della fine frase (EOS) per la lettura di più frasi sul backend CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)

Anche il tuo nome ha posto qui: un risultato di test sulla tua GPU, una frase per il set di test, una voce che hai
progettato, una segnalazione di bug chiara o una pull request contano tutti come contributi. Grazie a chi lo prova e ci
scrive.

## Licenza e riconoscimenti

Codice e voci incluse: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Basato su VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) e sulla conversione GGUF di audio.cpp. Elenco completo: [THIRD_PARTY.md](THIRD_PARTY.md).
Non affiliato con OpenBMB, ModelBest o il progetto audio.cpp.

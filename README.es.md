[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · **Español** · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Diseño de voces en turco con VoxCPM2 en una GPU de 4 GB.** Describe una voz en inglés, deja que el modelo la cree,
elige la variante que te guste y lee cualquier texto en turco con esa voz. Incluye un instalador de un solo comando, un
motor [audio.cpp](https://github.com/0xShug0/audio.cpp) parcheado que cabe en una GTX 1050 Ti (4 GB), una pequeña
interfaz web local y catorce voces sintéticas listas para usar: siete turcas y siete narradores nativos en inglés,
francés, alemán, español, ruso, chino y japonés.

- La aplicación lee en 30 idiomas; la interfaz también está en 30 idiomas.
- 14 voces listas para usar: 7 turcas, más una en cada uno de estos idiomas: inglés, francés, alemán, español, ruso, chino y japonés.
- Interfaz web (v0.2.0): cada tarjeta de variante tiene dos voces, la voz de diseño en bruto y la voz que oirás
  siempre; una lista de lectura con menú de voces; cambiar el nombre, ocultar o eliminar voces; borradores para los
  textos que lees. Consulta «Interfaz web» en «Uso».

[Cómo cabe en 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Guía de instalación para agentes de IA](AGENTS.md) · [Uso responsable](ETHICS.md)

> Las voces incluidas son sintéticas, diseñadas a partir de una descripción de texto. La sección de clonación de voz es
> solo para tu propia voz o para una voz que uses con el permiso explícito de su dueño; la interfaz te pide que
> confirmes ese permiso. Se prohíben la suplantación de identidad, el fraude y el engaño. Indica que lo que generes está
> hecho con IA. Consulta [ETHICS.md](ETHICS.md).

## 30 idiomas

Hicimos un vídeo documental sobre Capadocia en 8 idiomas: turco, inglés, francés, alemán, español, ruso, chino y
japonés. Cada idioma tiene su propio **narrador nativo**, diseñado con VoxCPM2 a partir de una descripción en inglés.
Todo se generó de forma totalmente local en una GTX 1050 Ti de 4 GB, con la misma calidad fija (16 pasos, cfg 2.0).
Los siete narradores se incluyen aquí, con su prompt, su texto de diseño, su semilla y su grabación de referencia.

| Código | Idioma | Voz | Escuchar | Vídeo |
|---|---|---|---|---|
| `tr` | Turco | `hazir/belgesel_hanim` (y 6 más) | [muestra](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Inglés | `hazir/anlatici_en` | [muestra](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113791986763440439) |
| `fr` | Francés | `hazir/anlatici_fr` | [muestra](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113790681575804962) |
| `de` | Alemán | `hazir/anlatici_de` | [muestra](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113791351645262249) |
| `es` | Español | `hazir/anlatici_es` | [muestra](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113807365611122705) |
| `ru` | Ruso | `hazir/anlatici_ru` | [muestra](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113801574136848884) |
| `zh` | Chino (mandarín) | `hazir/anlatici_zh` | [muestra](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113802229606121794) |
| `ja` | Japonés | `hazir/anlatici_ja` | [muestra](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Por qué frase a frase.** VoxCPM2 no es estable en una sola generación larga (aproximadamente, más de 30 segundos): el
ritmo se acelera y la voz puede desviarse. Aquí la voz la sostienen una grabación de referencia y una semilla fijas, y
el texto largo se lee con una frase por línea, de modo que el timbre y el estilo se mantienen iguales de la primera a la
última frase. En los idiomas distintos del turco no se aplica el diccionario de pronunciación turco. Se probaron los 30
idiomas que admite VoxCPM2 y todos funcionan; para los que no tienen voz incluida, usa `--dil <code>`. Comandos por
idioma y lo que aprendimos: [docs/cok_dilli.md](docs/cok_dilli.md). Skill de Claude Code para todo el flujo de diseño:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 prompts de ejemplo para empezar.** 18 papeles (narrador de documentales, presentador de noticias, voz
publicitaria, audiolibro, abuela cuentacuentos, presentador de pódcast, profesor, tráiler de cine, guía de meditación,
comentarista deportivo y más, en versión masculina y femenina) en cada uno de los 8 idiomas. El prompt está en inglés e
indica la nacionalidad y el acento nativo del hablante; el texto que se lee mientras se crea la voz viene incluido, en
ese idioma y adaptado al papel. Elige uno, escucha las variantes y quédate con la que te guste:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, o elige *Plantilla de ejemplo* en la interfaz
web. Lista completa: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dobla tus vídeos con tu propia voz.** [DubWorld](https://github.com/alexturkey/dubworld) es nuestro programa local de
doblaje de vídeo; instala este repositorio como su motor de voz VoxCPM2. Una voz que diseñes aquí se usa allí con
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Inicio rápido (Windows, 3 pasos)

1. **Descarga** el código: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   El paquete del motor ya compilado para tu tarjeta lo descarga el instalador en el paso 3:
   NVIDIA → [paquete CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [paquete Vulkan, experimental](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (¿ya descargaste uno? añade `-HazirZip <path to the zip>` al comando de abajo).
2. **Descomprime** el zip, abre la carpeta `voxcpm2-turkce-ses-tasarimi-main`, escribe `powershell` en la barra de
   direcciones del Explorador y pulsa Intro.
3. **Ejecuta** el instalador (requiere Python 3.10-3.13 de 64 bits; controlador NVIDIA ≥ 570 para CUDA) y luego haz doble clic en **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: añade `-Vulkan` al final. La interfaz se abre en http://127.0.0.1:8765/.

El zip del motor no es una aplicación independiente (su exe necesita el modelo y las DLL que prepara el instalador).
Detalles, lista de GPU y problemas frecuentes: «Instalación rápida», más abajo.

## Ubuntu / Linux (NVIDIA CUDA, experimental)

Compila el motor parcheado con `bash scripts/kur-linux.sh`, o usa `Dockerfile.linux` para compilarlo y ejecutarlo en un
entorno Ubuntu 24.04 / CUDA 12.8.1. Requiere una GPU NVIDIA y un controlador compatible; el instalador nativo necesita
además el CUDA Toolkit y Python 3.10-3.13. La interfaz solo escucha en loopback, también en servidores remotos
(reenvío por SSH). Requisitos, comandos, elección de arquitectura y alcance de la validación:
[docs/linux.md](docs/linux.md).

## Inicio rápido (macOS, Apple Silicon)

Necesita las Xcode Command Line Tools (`xcode-select --install`) y [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
El instalador descarga el modelo, compila el motor parcheado con Metal (~1 min) y lo deja todo listo en `~/vox`. Después,
haz doble clic en **`baslat.command`**. En un MacBook Air M4 de 16 GB: ~2 s de cálculo por cada 1 s de voz, la misma
semilla da un audio idéntico byte a byte, pico de ~5,3 GB de RAM y ninguna ralentización térmica en 12 min de lectura
continua. Detalles y mediciones: [docs/mac.md](docs/mac.md).

**App nativa para Mac (sin Python, Homebrew ni Terminal):** [macos/README.md](macos/README.md). Incluye el mismo motor
parcheado y descarga el modelo la primera vez que se abre; por ahora se compila desde el código fuente con Xcode.

## Para usuarios de Mac (Apple Silicon)

También existe una adaptación independiente, hecha por la comunidad, para Mac con Apple Silicon que ejecuta VoxCPM2 con
el framework MLX de Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
La desarrolla y mantiene Emre Koç ([@emre-koc](https://github.com/emre-koc)) en su propio repositorio, no aquí; los
pasos de instalación y las preguntas de soporte van allí. ¡Gracias, Emre, por llevar este proyecto al Mac!

## Cómo funciona

1. **Diseño de la voz.** Una *descripción de la voz* en inglés + un *texto que se lee mientras se crea la voz* (en el
   idioma de la voz) + un número de variantes. Cada variante recibe su propia semilla; el motor recibe
   `(description)text` y devuelve una grabación de diseño por semilla. El texto es una muestra breve para conocer la
   voz: 1-2 frases, ~20 s como máximo (la interfaz muestra la estimación y no arranca por encima de 22 s); el texto
   largo corresponde al paso 2.
2. **Lectura basada en la referencia.** La grabación de diseño se pasa a **las dos** entradas del motor (`audio` y
   `voice_ref`), junto con su transcripción (`reference_text`) y el nuevo texto que se va a leer, con la misma semilla.
   La voz la sostiene la grabación, no la descripción, así que no se desvía de un texto a otro. El texto se lee frase a
   frase.
3. La calidad es fija: 16 pasos de difusión, CFG 2.0. La semilla no es un ajuste de calidad.

La grabación de diseño en bruto es una muestra irrepetible de la voz; ninguna lectura posterior suena exactamente
igual. Lo que oyes en cada lectura posterior es el paso 2: la grabación de diseño como referencia más la semilla propia
de la variante. Por eso la interfaz web hace el paso 2 justo después del diseño y muestra ambas en la tarjeta de
variante.

El motor es audio.cpp v0.7.2 con nuestro parche (`patches/`), y el modelo es VoxCPM2 Q8_0 GGUF. VRAM máxima ≈ 2,8 GB;
unos 2 s de cálculo por cada 1 s de voz en una GTX 1050 Ti. Detalles y mediciones: [docs/4gb.md](docs/4gb.md).

## Voces incluidas (`hazir_sesler/`)

Las catorce se diseñaron a partir de los prompts guardados en su `ses.json`; ninguna se clonó de una grabación (la
clonación es la pestaña aparte *Clonación de voz*, que exige consentimiento).

| Voz | Descripción breve | Escuchar |
|---|---|---|
| `belgesel_hanim` | Mujer madura de unos cincuenta años, contralto grave y cálida; narradora de documentales serena | [muestra](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referencia](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Narrador masculino grave, potente y misterioso | [muestra](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referencia](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Veterano presentador de noticias de unos setenta años, sereno y con autoridad | [muestra](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referencia](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Carismática presentadora del informativo de la noche, de unos treinta años, aterciopelada y expresiva | [muestra](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referencia](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Bruja de cuento: grave, algo nasal, de una dulzura taimada | [muestra](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referencia](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Narrador masculino excepcionalmente grave, denso e imponente | [muestra](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referencia](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Anciano sabio, voz grave y retumbante, algo misteriosa | [muestra](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referencia](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Narrador de documentales nativo de inglés, de unos cincuenta años (General American); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Narrador de documentales nativo de francés, de unos cincuenta años (parisino); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Narrador de documentales nativo de alemán, de unos cincuenta años (Hochdeutsch); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Narrador de documentales nativo de español, de unos cincuenta años (castellano (Madrid)); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Narrador de documentales nativo de ruso, de unos cincuenta años (Moscú); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Narrador de documentales nativo de chino (mandarín), de unos cincuenta años (putonghua de Pekín); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Narrador de documentales nativo de japonés, de unos cincuenta años (japonés estándar de Tokio); grave, sereno, cálido | [muestra](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referencia](hazir_sesler/anlatici_ja/referans.flac) |

Cada carpeta contiene: `referans.flac` (grabación de diseño sin pérdida), `ses.json` (prompt, transcripción, semilla de
diseño, semilla de lectura, descripción; `dil` = idioma en el caso de los narradores), `ornek_okuma.mp3` (+ su texto).
Úsalas directamente: `--ses hazir/<name>`. Las grabaciones de referencia de los narradores son cortas (5,6-10 s); sus
muestras son las tres primeras frases del guion de Capadocia, recortadas de la lectura completa de la producción.

## Instalación rápida, sin compilador (Windows 10/11, GPU NVIDIA ≥ 4 GB)

Requisitos: controlador NVIDIA ≥ 570 y Python 3.10-3.13 de 64 bits (`winget install Python.Python.3.12`). Nada más: ni
Visual Studio ni instalador de CUDA. ¿No sabes qué tarjeta tienes? Ejecuta `nvidia-smi` en PowerShell: muestra el nombre
de la GPU, la versión del controlador y la memoria. ¿No tienes tarjeta NVIDIA? Consulta «AMD / Intel» más abajo.

Con [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Sin Git: en esta página haz clic en **Code → Download ZIP**, descomprímelo, abre la carpeta extraída
`voxcpm2-turkce-ses-tasarimi-main`, escribe `powershell` en la barra de direcciones del Explorador, pulsa Intro y
ejecuta la última línea de arriba. Git solo hace falta para compilar desde el código fuente.

`-ExecutionPolicy Bypass` se aplica solo a este proceso y no cambia ningún ajuste del sistema; lee `scripts\kur.ps1`
antes de ejecutarlo, como con cualquier script de instalación. Un comando, ~10 min, ~3,7 GB de descarga, todo verificado
con sha256: el modelo (2,95 GB), las DLL de runtime de CUDA 12.8 como zips portables (sin instalación en el sistema y sin
tocar el PATH), el **motor precompilado** de la página de Releases, un `.venv` con los dos paquetes de Python,
`ayarlar.json` y una comprobación final de la GPU (`KONTROL_OK`). Si algo falla, vuelve a ejecutarlo; los archivos ya
verificados se omiten. Después inicia la interfaz web: haz doble clic en **`baslat.bat`** en la carpeta del repositorio.
Arranca la interfaz y abre **http://127.0.0.1:8765/** en tu navegador cuando está lista; cierra la ventana negra (o
pulsa Ctrl+C en ella) para detenerla. Lo mismo desde PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
y luego abre tú mismo **http://127.0.0.1:8765/** (iniciada así, la interfaz no abre el navegador; solo escucha en
localhost).

> **El `audiocpp_cli.exe` del zip de la release no está pensado para abrirse con doble clic.** Es un motor de línea de
> comandos que necesita a su lado las DLL de CUDA y el modelo; `kur.ps1` lo coloca todo en su sitio y el paquete de
> Python lo controla. Si le haces doble clic, solo verás «cudart64_12.dll not found».

**GPU compatibles (release v0.1.1):** código nativo para GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) y RTX 50xx (sm_120a); cualquier otra GPU CUDA a partir de Pascal ejecuta el PTX integrado a través del
controlador (primer arranque más lento). Maxwell (GTX 9xx) y anteriores no son compatibles con CUDA 12.8. Probado por
nosotros en una GTX 1050 Ti de 4 GB (también mediante Docker Desktop/WSL2 en Windows, solo CLI); medido por
@mslmyilmaz5 (#15): RTX 3060 Ti de 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (detalles en [docs/linux.md](docs/linux.md)).
Los informes de otras tarjetas son bienvenidos en [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (experimental):** un zip de motor Vulkan aparte (`...-win64-vulkan.zip`, sin CUDA) se instala con
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Solo se ha verificado en nuestra tarjeta NVIDIA mediante el backend Vulkan (allí
fue más lento que CUDA, pero dio el mismo audio con la misma semilla; esa medición se tomó mientras el disco estaba
ocupado con otro trabajo, así que aún falta una comparación de velocidad limpia) y **no** lo hemos probado nosotros
mismos en hardware AMD o Intel: si lo pruebas, publica el resultado en Discussions. Con más de un dispositivo Vulkan
(integrado + dedicado), el instalador escribe el índice de la GPU dedicada como `cihaz` en `ayarlar.json`.

*Nota: la compatibilidad con Vulkan es experimental por ahora. Se ha compilado y probado con éxito en una GTX 1050 Ti.
Además, un usuario externo (mitra_tr) ha informado de que lo ha ejecutado en una AMD 6900 XT. Todavía hacen falta
pruebas más amplias en tarjetas AMD/Intel.*

### Alternativa: compilar el motor desde el código fuente

Necesita Visual Studio 2022 Build Tools con «Desarrollo para el escritorio con C++» (incluidas las herramientas de CMake
para C++), ~7 GB. Después:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Esto también descarga nvcc, obtiene el código fuente de audio.cpp v0.7.2, aplica `patches/0001-voxcpm2-4gb-ve-hiz.patch`
y compila para tu GPU (`-Mimari native`, por defecto; o, por ejemplo, `-Mimari 61`), ~15-25 min. Usa una raíz corta
(`C:\vox`): nvcc falla con rutas largas. Paso a paso con comprobaciones: [AGENTS.md](AGENTS.md).

### Problemas frecuentes de instalación

| Ves | Qué significa y qué hacer |
|---|---|
| `cudart64_12.dll not found` tras hacer doble clic en el exe | El motor no está pensado para iniciarse a mano. Ejecuta el comando `kur.ps1` de arriba y luego inicia la interfaz web. |
| `64-bit Python 3.10+ bulunamadı` (no se encuentra Python) | Instala Python (`winget install Python.Python.3.12`), cierra PowerShell, abre uno nuevo y vuelve a ejecutar el mismo comando. |
| `motor ekran kartını görmedi` (el motor no ha detectado la GPU) | Actualiza el controlador NVIDIA a la versión 570 o posterior; comprueba que `nvidia-smi` funciona. |
| `indirme başarısız` / `sha256 tutmadı` (descarga fallida / suma de comprobación incorrecta) | Normalmente es una descarga interrumpida. Vuelve a ejecutar el mismo comando; los archivos ya verificados se omiten. |
| Compilación desde el código fuente: falla `nvcc` | Usa una raíz de instalación corta (`-Kok C:\vox`). |
| La página no se abre | Inicia la interfaz con `baslat.bat`, o abre tú mismo http://127.0.0.1:8765/. ¿Puerto ocupado? Cambia `"port"` en `ayarlar.json`. |

¿Problemas? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) o una
[incidencia de instalación](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
con tu GPU, tu versión de Windows, el comando y sus últimas líneas.

## Uso

Línea de comandos:
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
Reglas del texto: escribe los números con letras, sin comillas (la herramienta rechaza cifras y comillas), una frase por
línea, ≤ 2000 caracteres por línea. Pausa tras una línea: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s,
`|| agir` 1,5 s o tu propia duración `|| 0,8` (0-5 s; las cifras del marcador están permitidas).
`ayarlar/okunus_sozlugu.tsv` corrige la pronunciación de palabras extranjeras en texto turco. El idioma se detecta a
partir del texto (letras turcas, sistema de escritura, palabras frecuentes; si hay dudas, el `dil` de la ficha de la
voz; `--dil <code>` es opcional). En texto que no es turco, ahí se permiten los apóstrofos, el diccionario turco se omite
y las cifras se siguen rechazando. Si una lectura muestra `speed gate: satır [...]`, escucha esas líneas.

### Interfaz web

Solo en local (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → abre tú mismo http://127.0.0.1:8765/
(otro puerto: `--port 8800`), o haz doble clic en `baslat.bat`. Detén el servidor con Ctrl+C. Tres pestañas: *Diseñar
una voz*, *Leer con esta voz*, *Clonación de voz*. El camino habitual: *Diseñar* → escuchar las variantes → *Añadir a
mi lista de lectura* → *Leer con esta voz* → descargar. O elige una voz incluida en el menú de voces y lee.

- **Versión en la cabecera.** Un `v0.2.0 · <short commit>` pequeño y tenue (con `+` cuando hay archivos con seguimiento
  con cambios sin confirmar; sin git, solo la versión), para que las capturas de pantalla y los vídeos muestren qué
  versión se usó.
- **Dos voces en cada tarjeta de variante.** Arriba, en gris, la *Voz de diseño en bruto*: se genera una sola vez y
  nunca vuelve a salir igual. Debajo, en un marco naranja, *↻ Esta es la voz que oirás siempre*: la grabación de diseño
  releída como referencia con la semilla propia de la variante (que se muestra en la tarjeta). Así sonará la voz en
  cada lectura posterior. Debajo están *Leer con esta voz* y *Añadir a mi lista de lectura*. Una sola pulsación de
  *Diseñar* hace ambas cosas: diseña cada variante y luego lee tu texto con cada voz duradera; una única barra de
  progreso cuenta las dos fases. La carpeta de la variante recibe `dinleme.wav`. Si esa lectura se detiene antes de
  tiempo, el diseño se conserva y la tarjeta muestra un aviso.
- **La ventana «Texto que quieres escuchar».** En *Diseñar una voz*, el cuadro *↻ Texto que quieres escuchar* contiene
  lo que lee cada voz duradera (si se deja vacío, se lee la frase de ejemplo). Al hacer clic en él se abre el cuaderno
  de lectura en una ventana: números de línea, menú de línea, bandas de pausa. *Aceptar* devuelve el texto y sus pausas
  al cuadro; *Cancelar* o Esc no cambian nada. La pestaña de lectura conserva su propio texto.
- **El cuaderno de lectura.** Una frase por línea. Haz clic en un número de línea para abrir el menú de línea (subir o
  bajar, mover a una posición, duplicar, eliminar; Alt+↑/↓, Alt+Mayús+↓, o arrastrar por el número; Ctrl+Z deshace a la
  vez el texto y las pausas). Haz clic en la banda fina entre dos líneas para elegir la pausa (bagli 0,25 · normal 0,5 ·
  paragraf 1 · agir 1,5 s, o tu propia duración de 0-5 s con el engranaje); pulsa Intro dos veces para un párrafo (1 s),
  y las líneas en blanco se convierten en bandas de pausa. Mientras suena el resultado, la línea que se está leyendo se
  ilumina y se desplaza a la vista; *▶ Escuchar desde aquí* en el menú de línea reproduce desde esa línea. El texto y sus
  pausas sobreviven a una recarga de la página (almacenamiento del navegador).
- **Borradores.** El botón *📄 Borradores* está en los dos cuadernos (pestaña de lectura y ventana). Guarda el texto
  actual con sus pausas como borrador, carga uno con un clic (Ctrl+Z lo deshace) y usa ⋯ para sobrescribirlo, cambiarle
  el nombre o eliminarlo. Los borradores se guardan en `sesler/taslaklar.json`, nunca en el repositorio.
- **Lista de lectura y menú de voces.** En una tarjeta de variante, *Añadir a mi lista de lectura* abre un cuadro de
  nombre: dale a la variante su propio nombre y ✓ la añade. El *Nombre de la generación* se mantiene en todas las
  variantes de esa ejecución. En *Leer con esta voz*, el botón de voz (bandera + nombre) abre el menú de voces: *Mi
  lista de lectura* arriba y luego las voces incluidas con sus banderas (primero el idioma de la interfaz). Cada fila
  tiene ▶ escuchar (la voz duradera, si la hay), el corazón (añadir o quitar) y ⋯; ↑/↓ e Intro eligen, Esc cierra y se
  recuerda la última voz. La lista está en `sesler/okuma_listesi.json`, fuera del repositorio, y sobrevive a los
  reinicios.
- **Gestionar voces.** El menú ⋯ (fila del menú de voces o tarjeta de variante) tiene *Leer con esta voz*, añadir a la
  lista o quitar de ella, *Cambiar nombre* (un nombre vacío restaura el original; *Volver al nombre original*),
  *Eliminar* para las voces diseñadas y *Ocultar* para las incluidas; ambas piden confirmación. Una voz eliminada pasa a
  `sesler/_cop/`; ocultar nunca toca los archivos del repositorio. *Voces ocultas y eliminadas (N)*, al final del menú
  de voces, tiene *Restaurar*. Los nombres personalizados y las voces ocultas se guardan en `sesler/yerel_katman.json`.
  Una voz renombrada muestra su origen en gris (*nombre de la generación · variante N*); ⋯ → *Ir a la generación* abre
  su diseño.
- **Atajos y archivos.** Ctrl+Intro (⌘+Intro en Mac) inicia *Diseñar* o *Leer con esta voz* en la pestaña abierta. La
  barra de progreso muestra *transcurrido / ~total*, con una estimación aprendida de trabajos anteriores en tu equipo.
  La descarga lleva el nombre de la voz y la hora (`Voice_Name_2026-11-02_0152.wav`).

**Clonación de voz (tu propia voz o una voz autorizada).** En la pestaña *Clonación de voz* de la interfaz, aporta tu
grabación (wav/mp3/flac/ogg; se recomiendan 5-30 s de voz limpia; por debajo de 3 s se rechaza y por encima de 36 s se
recorta), su transcripción exacta y el texto que se va a leer. El botón sigue desactivado hasta que marques «Esta voz es
mía o tengo el permiso explícito de su dueño». La grabación solo va al servidor local (127.0.0.1), se procesa en una
carpeta temporal junto con su codificación de referencia, y esa carpeta se borra cuando termina el trabajo, también si
falla; no se envía nada por la red. Solo se conserva la salida sintética (interfaz: `sesler/_okumalar/<job>/`, CLI:
`--cikti`). La salida es `klon_synthetic.wav` con una etiqueta «synthetic»; indica que está generada con IA cuando la
compartas. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Preguntas frecuentes

**¿Modelo o motor? ¿Qué es cada cosa?** VoxCPM2 (OpenBMB) es el *modelo*: la red de 2000 millones de parámetros que
convierte texto en voz. audio.cpp es el *motor*: el programa en C++/CUDA que ejecuta el modelo en tu GPU
(`audiocpp_cli.exe`). Nuestro parche cambia el motor, no el modelo: hace que VoxCPM2 quepa en 4 GB y que la misma
semilla dé siempre el mismo audio. El paquete de Python de este repositorio solo prepara el texto, llama al motor y
recoge los archivos.

**¿Qué GPU?** Consulta «GPU compatibles» más arriba: NVIDIA a partir de la GTX 10xx, 4 GB de VRAM o más, controlador
≥ 570. La release incluye código nativo para sm_61/75/86/89/120a; las demás tarjetas Pascal o posteriores usan el PTX
integrado (primer arranque más lento). AMD/Intel: zip Vulkan experimental, `kur.ps1 -Vulkan`; un usuario externo ha
informado de que lo ha ejecutado en una AMD 6900 XT, pero aún hacen falta pruebas más amplias en AMD/Intel (consulta
«AMD / Intel» más arriba). Solo CPU (`"backend": "cpu"` en `ayarlar.json`) funciona, pero es ~6× más lento que una
GTX 1050 Ti (medición del motor: 535 s frente a 94 s para 48 s de voz); no es una vía compatible.

**¿Qué velocidad tiene?** Medido en una GTX 1050 Ti de 4 GB (i7-7700HQ): una variante de diseño (grabación de ≈ 25 s),
55 s; lectura ≈ 2 s de cálculo por cada 1 s de voz (factor de tiempo real 1,9-2,8) tras una codificación de referencia
única de ~50 s por voz (en caché en el disco) y 10-20 s de carga del modelo por lote; VRAM máxima 2,6-2,9 GB. Las
tarjetas más nuevas son más rápidas; cifras y método: [docs/4gb.md](docs/4gb.md).

**¿Puede clonar una voz?** El modelo VoxCPM2 en el que se basa puede imitar una voz a partir de una grabación de
referencia, y la sección de clonación lo aprovecha. Úsala solo con tu propia voz o con el permiso explícito de la
persona a quien pertenece la voz; la interfaz te pide que confirmes ese permiso. El diseño de voces no necesita ninguna
grabación: parte de una descripción de texto en inglés o en chino, y la «referencia» que se usa para leer con una voz
diseñada es la propia grabación de diseño sintética del modelo. Se prohíben la suplantación de identidad, el fraude y
el engaño. Consulta [ETHICS.md](ETHICS.md). Indica que lo que publiques está generado con IA.

**¿Cómo escribo una buena descripción de voz?** En inglés, 1-3 frases: edad y género, timbre (grave/brillante, cálido,
nasal, ronco), tono y papel (narrador de documentales sereno, presentador enérgico), tempo (lento, pausado) y «clean
studio recording, no background noise». Que sea una descripción, no un guion; sin paréntesis. Pide 3-5 variantes y
escúchalas: la semilla cambia mucho la voz. Para el texto de creación, usa 1-2 frases naturales en el idioma de la voz,
con el tono que quieras (como máximo ~20 s de voz). Al leer, una frase por línea; divide las frases largas y escribe los
números con letras.

## Cómo contribuir

¿No sabes por dónde empezar? Estas cuatro pequeñas incidencias son un buen primer paso:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Pruébalo en tu GPU e informa de la tarjeta, el controlador y los tiempos
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: prueba la compilación experimental de Vulkan
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Añade una frase al conjunto de pruebas
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Comparte una voz que hayas diseñado, con su descripción y su semilla

Conjunto de pruebas compartido: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); guía de voz de marca:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); cómo enviar código: [CONTRIBUTING.md](CONTRIBUTING.md).
Problemas de instalación: [formulario de incidencia](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); preguntas y resultados: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Todas las personas que participan siguen el [Código de conducta](CODE_OF_CONDUCT.md): sé amable y centra tus
comentarios en el trabajo.

## Colaboradores

- [@alexturkey](https://github.com/alexturkey): mantenedor; código, voces incluidas, documentación
- [@cayir21](https://github.com/cayir21): compatibilidad con Metal en macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): corrección del fin de frase (EOS) para leer varias frases en el backend de CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)

Tu nombre también tiene su sitio aquí: un resultado de prueba de tu GPU, una frase para el conjunto de pruebas, una voz
que hayas diseñado, un informe de error claro o una pull request cuentan como contribuciones. Gracias a todas las
personas que lo prueban y nos escriben.

## Licencia y créditos

Código y voces incluidas: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Basado en VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) y la conversión a GGUF de audio.cpp. Lista completa: [THIRD_PARTY.md](THIRD_PARTY.md).
Sin relación con OpenBMB, ModelBest ni con el proyecto audio.cpp.

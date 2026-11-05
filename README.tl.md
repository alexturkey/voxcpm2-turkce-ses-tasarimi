[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · **Tagalog** · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Pagdidisenyo ng boses sa Turkish gamit ang VoxCPM2 sa isang 4 GB na GPU.** Ilarawan ang isang boses sa Ingles,
hayaang likhain ito ng model, piliin ang variant na gusto mo, at basahin ang kahit anong tekstong Turkish gamit ang
boses na iyon. Kasama rito ang installer na isang command lang, isang patched na
[audio.cpp](https://github.com/0xShug0/audio.cpp) engine na kasya sa GTX 1050 Ti (4 GB), isang maliit na lokal na web
UI, at labing-apat na handang synthetic na boses: pito sa Turkish at pitong katutubong narrator sa Ingles, Pranses,
Aleman, Espanyol, Ruso, Chinese at Hapon.

- Nakababasa ang app sa 30 wika; nasa 30 wika rin ang interface.
- 14 na handang boses: 7 sa Turkish, at tig-iisa sa Ingles, Pranses, Aleman, Espanyol, Ruso, Chinese at Hapon.
- Web UI (v0.2.0): may dalawang boses ang bawat variant card, ang hilaw na boses ng disenyo at ang boses na palagi mong
  maririnig; reading list na may voice menu; palitan ang pangalan, itago o burahin ang mga boses; mga draft para sa
  mga tekstong binabasa mo. Tingnan ang "Web UI" sa ilalim ng "Paggamit".

[Paano ito kumakasya sa 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Gabay sa pag-install para sa mga AI agent](AGENTS.md) · [Responsableng paggamit](ETHICS.md)

> Synthetic ang mga kasamang boses, idinisenyo mula sa isang tekstong paglalarawan. Ang bahaging voice cloning ay para
> lamang sa sarili mong boses o sa boses na ginagamit nang may malinaw na pahintulot ng may-ari nito; hihilingin ng UI
> na kumpirmahin mo ang pahintulot na iyon. Bawal ang panggagaya sa ibang tao, panloloko at panlilinlang. Lagyan ng
> label na AI-generated ang anumang nililikha mo. Tingnan ang [ETHICS.md](ETHICS.md).

## 30 wika

Gumawa kami ng isang dokumentaryong video tungkol sa Cappadocia sa 8 wika: Turkish, Ingles, Pranses, Aleman,
Espanyol, Ruso, Chinese at Hapon. May sariling **katutubong narrator** ang bawat wika, idinisenyo gamit ang VoxCPM2 mula
sa isang paglalarawang nasa Ingles. Lahat ng ito ay ganap na nilikha nang lokal sa isang 4 GB na GTX 1050 Ti, sa iisang
nakapirming kalidad (16 na hakbang, cfg 2.0). Kasama rito ang pitong narrator, pati ang kanilang prompt, design text,
seed at reference recording.

| Code | Wika | Boses | Pakinggan | Video |
|---|---|---|---|---|
| `tr` | Turkish | `hazir/belgesel_hanim` (at 6 pa) | [sample](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Ingles | `hazir/anlatici_en` | [sample](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Pranses | `hazir/anlatici_fr` | [sample](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Aleman | `hazir/anlatici_de` | [sample](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Espanyol | `hazir/anlatici_es` | [sample](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Ruso | `hazir/anlatici_ru` | [sample](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Chinese (Mandarin) | `hazir/anlatici_zh` | [sample](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Hapon | `hazir/anlatici_ja` | [sample](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Bakit pangungusap-bawat-pangungusap.** Hindi stable ang VoxCPM2 sa isang mahabang generation (humigit-kumulang lampas
30 segundo): bumibilis ang ritmo at maaaring lumihis ang boses. Dito, dala ng isang nakapirming reference recording at
seed ang boses, at binabasa ang mahabang teksto nang isang pangungusap bawat linya, kaya pareho ang timbre at estilo mula
unang pangungusap hanggang huli. Para sa mga wikang hindi Turkish, hindi ginagamit ang Turkish na diksiyunaryo ng
pagbigkas. Nasubukan at gumagana ang lahat ng 30 wikang sinusuportahan ng VoxCPM2; gamitin ang `--dil <code>` para sa
mga wikang wala pang kasamang boses. Mga command bawat wika at ang mga natutunan namin:
[docs/cok_dilli.md](docs/cok_dilli.md). Claude Code skill para sa buong daloy ng pagdidisenyo:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 na halimbawang prompt na mapagsisimulan.** 18 papel (documentary narrator, news anchor, boses ng commercial,
audiobook, lolang nagkukuwento, podcast host, guro, movie trailer, gabay sa meditasyon, sports commentator at iba pa,
lalaki at babae) sa bawat isa sa 8 wika. Nasa Ingles ang prompt, kasama ang nasyonalidad at katutubong accent ng
nagsasalita; kasama nito ang tekstong binabasa habang nililikha ang boses, nasa wikang iyon at bagay sa papel. Pumili ng
isa, pakinggan ang mga variant, at itabi ang gusto mo:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, o piliin ang *Halimbawang paglalarawan* sa web
UI. Buong listahan: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**I-dub ang mga video mo gamit ang sarili mong boses.** Ang [DubWorld](https://github.com/alexturkey/dubworld) ay ang
aming lokal na programa sa pag-dub ng video; ini-install nito ang repository na ito bilang VoxCPM2 voice engine nito.
Ang boses na idinisenyo mo rito ay ginagamit doon gamit ang `ses.voxcpm2_ses = "<name>/<variant>"`.

## Mabilisang simula (Windows, 3 hakbang)

1. **I-download** ang code: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Ang handang engine package para sa card mo ay kukunin ng installer sa hakbang 3:
   NVIDIA → [CUDA package](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.0/voxcpm2-turkce-ses-tasarimi-motor-v0.3.0-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan package, eksperimental](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan.zip)
   (na-download mo na ang isa? idagdag ang `-HazirZip <path to the zip>` sa command sa ibaba).
2. **I-extract** ang zip, buksan ang folder na `voxcpm2-turkce-ses-tasarimi-main`, i-type ang `powershell` sa address
   bar ng Explorer at pindutin ang Enter.
3. **Patakbuhin** ang installer (kailangan ng 64-bit na Python 3.10-3.13; NVIDIA driver ≥ 570 para sa CUDA), saka i-double-click ang **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: idagdag ang `-Vulkan` sa dulo. Bubukas ang UI sa http://127.0.0.1:8765/.

Hindi standalone na app ang engine zip (kailangan ng exe nito ang model at mga DLL na inihahanda ng installer). Mga
detalye, listahan ng GPU at karaniwang problema: tingnan ang "Mabilisang pag-install" sa ibaba.

## Ubuntu / Linux (NVIDIA CUDA, eksperimental)

I-build ang patched na engine gamit ang `bash scripts/kur-linux.sh`, o gamitin ang `Dockerfile.linux` para mag-build at
magpatakbo sa isang Ubuntu 24.04 / CUDA 12.8.1 na environment. Kailangan ng NVIDIA GPU at compatible na driver;
kailangan din ng native installer ang CUDA toolkit at Python 3.10-3.13. Nananatiling loopback-only ang UI, kahit sa mga
remote server (SSH forwarding). Mga kailangan, command, pagpili ng architecture at saklaw ng validation:
[docs/linux.md](docs/linux.md).

## Mabilisang simula (macOS, Apple Silicon)

Kailangan ng Xcode Command Line Tools (`xcode-select --install`) at [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Dina-download ng installer ang model, bina-build ang patched na engine gamit ang Metal (~1 minuto) at inihahanda ang
lahat sa ilalim ng `~/vox`. Pagkatapos ay i-double-click ang **`baslat.command`**. Sa MacBook Air M4 16 GB: ~2 segundo
ng compute bawat 1 segundo ng pananalita, byte-identical na audio sa parehong seed, peak na ~5.3 GB RAM, at walang
thermal slowdown sa loob ng 12 minuto ng tuloy-tuloy na pagbasa. Mga detalye at sukat: [docs/mac.md](docs/mac.md).

**Native na Mac app (walang Python, Homebrew o Terminal):** [macos/README.md](macos/README.md). Kasama rito ang parehong
patched na engine at dina-download nito ang model sa unang pagbukas; sa ngayon, bina-build ito mula sa source gamit ang
Xcode.

## Para sa mga gumagamit ng Mac (Apple Silicon)

Mayroon ding hiwalay na adaptation na gawa ng komunidad para sa mga Apple Silicon na Mac, na nagpapatakbo ng VoxCPM2
gamit ang MLX framework ng Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Si Emre Koç ([@emre-koc](https://github.com/emre-koc)) ang gumagawa at nagme-maintain nito sa sarili niyang repository,
hindi rito; doon itanong ang mga hakbang sa pag-install at mga tanong sa suporta. Salamat, Emre, sa pagdadala ng
proyektong ito sa Mac!

## Paano ito gumagana

1. **Pagdidisenyo ng boses.** Isang *paglalarawan ng boses* sa Ingles + isang *tekstong binabasa habang nililikha ang
   boses* (sa wika ng boses) + bilang ng mga variant. May sariling seed ang bawat variant; tinatanggap ng engine ang
   `(description)text` at nagbabalik ng isang design recording bawat seed. Ang teksto ay maikling sample para makilala
   ang boses: 1-3 pangungusap, hanggang ~30 segundo (ipinapakita ng UI ang tantiya at hindi ito magsisimula kapag
   lampas 33 segundo); ang mahabang teksto ay para sa hakbang 2.
2. **Pagbasa batay sa reference.** Ipinapasa ang design recording sa **parehong** input ng engine (`audio` at
   `voice_ref`), kasama ang transcript nito (`reference_text`) at ang bagong tekstong babasahin, sa parehong seed. Ang
   recording ang nagdadala ng boses, hindi ang paglalarawan, kaya hindi ito lumilihis sa bawat teksto. Binabasa ang
   teksto nang pangungusap-bawat-pangungusap.
3. Nakapirmi ang kalidad: 16 na diffusion step, CFG 2.0. Hindi pang-adjust ng kalidad ang seed.
4. **Oras ng bawat salita, parehong audio sa bawat pagpapatakbo.** Habang nagbabasa, ang engine mismo ang nagsasabi kung saan nagsisimula at nagtatapos ang bawat salita (patch 0002, walang dagdag na model). Isinusulat ang mga oras sa `kelimeler.json`, at pinuputol ang mga linya para ang puwang sa pagitan ng mga linya ay katumbas ng setting ng paghinto. Katumpakan kumpara sa CTC forced alignment (CTC = 100%): 89.66% (Turkish, 12 boses; setting `kelime_zamani`, naka-on bilang default). Sa patch 0003, ang parehong seed ay nagbibigay ng byte-identical na audio sa bawat pagpapatakbo.

Ang hilaw na design recording ay isang beses lang na sample ng boses; walang susunod na pagbasa ang eksaktong kapareho
nito. Ang naririnig mo sa bawat susunod na pagbasa ay ang hakbang 2: ang design recording bilang reference kasama ang
sariling seed ng variant. Kaya ginagawa ng web UI ang hakbang 2 kaagad pagkatapos ng disenyo at ipinapakita ang
dalawa sa variant card.

Ang engine ay audio.cpp v0.7.2 kasama ang aming patch (`patches/`), at ang model ay VoxCPM2 Q8_0 GGUF. Peak na VRAM ≈
2.8 GB; mga 2 segundo ng compute bawat 1 segundo ng pananalita sa GTX 1050 Ti. Mga detalye at sukat:
[docs/4gb.md](docs/4gb.md).

## Mga kasamang boses (`hazir_sesler/`)

Lahat ng labing-apat ay idinisenyo mula sa mga prompt na nakatago sa kani-kanilang `ses.json`; walang kinopya mula sa
isang recording (ang cloning ay ang hiwalay na *Voice cloning* tab na nangangailangan ng pahintulot).

| Boses | Maikling paglalarawan | Pakinggan |
|---|---|---|
| `belgesel_hanim` | Mature na babae sa edad singkuwenta, malalim at mainit na alto; kalmadong documentary narrator | [sample](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [reference](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Malalim, malakas at misteryosong lalaking narrator | [sample](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Beteranong news anchor na nasa edad pitumpu, kalmado at may awtoridad | [sample](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [reference](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Karismatikong babaeng anchor ng balita sa gabi na nasa edad trenta, malambot na parang pelus at ekspresibo | [sample](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [reference](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Bruha ng fairy tale: mababa, bahagyang ngongo, pilyang matamis | [sample](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [reference](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Napakalalim, siksik at maawtoridad na lalaking narrator | [sample](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [reference](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Matandang pantas na lalaki, malalim at umuugong, medyo misteryoso | [sample](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Katutubong English na lalaking documentary narrator sa edad singkuwenta (General American); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Katutubong French na lalaking documentary narrator sa edad singkuwenta (Parisian); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Katutubong German na lalaking documentary narrator sa edad singkuwenta (Hochdeutsch); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Katutubong Spanish na lalaking documentary narrator sa edad singkuwenta (Castilian (Madrid)); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Katutubong Russian na lalaking documentary narrator sa edad singkuwenta (Moscow); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Katutubong Chinese (Mandarin) na lalaking documentary narrator sa edad singkuwenta (Beijing Putonghua); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Katutubong Japanese na lalaking documentary narrator sa edad singkuwenta (Tokyo standard); malalim, kalmado, mainit | [sample](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ja/referans.flac) |

Laman ng bawat folder: `referans.flac` (lossless na design recording), `ses.json` (prompt, transcript, design seed,
reading seed, paglalarawan; `dil` = wika para sa mga narrator), `ornek_okuma.mp3` (+ ang teksto nito). Gamitin ang mga
ito nang direkta: `--ses hazir/<name>`. Maiikli ang reference recording ng mga narrator (5.6-10 segundo); ang mga sample
nila ay ang unang tatlong pangungusap ng script tungkol sa Cappadocia, hinango mula sa buong production reading.

## Mabilisang pag-install, walang kailangang compiler (Windows 10/11, NVIDIA GPU ≥ 4 GB)

Mga kailangan: NVIDIA driver ≥ 570 at 64-bit na Python 3.10-3.13 (`winget install Python.Python.3.12`). Wala nang iba:
walang Visual Studio, walang CUDA installer. Hindi sigurado kung anong card ang mayroon ka? Patakbuhin ang `nvidia-smi`
sa PowerShell: ipinapakita nito ang pangalan ng GPU, bersyon ng driver at memory. Walang NVIDIA card? Tingnan ang "AMD /
Intel" sa ibaba.

Gamit ang [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Walang Git: sa page na ito, i-click ang **Code → Download ZIP**, i-extract ito, buksan ang na-extract na folder na
`voxcpm2-turkce-ses-tasarimi-main`, i-type ang `powershell` sa address bar ng Explorer at pindutin ang Enter, saka
patakbuhin ang huling linya sa itaas. Kailangan lang ang Git kung magbi-build mula sa source.

Ang `-ExecutionPolicy Bypass` ay para lang sa prosesong ito at walang binabagong setting ng system; basahin muna ang
`scripts\kur.ps1` bago ito patakbuhin, gaya ng sa anumang installer script. Isang command, ~10 minuto, ~3.7 GB na
download, lahat ay sha256-verified: ang model (2.95 GB), ang CUDA 12.8 runtime DLL bilang mga portable zip (walang
system install, hindi ginagalaw ang PATH), ang **prebuilt na engine** mula sa Releases page, isang `.venv` na may
dalawang Python package, `ayarlar.json`, at isang huling GPU check (`KONTROL_OK`). Patakbuhin itong muli kapag may
pumalya; nilalaktawan ang mga file na na-verify na. Pagkatapos, simulan ang web UI: i-double-click ang
**`baslat.bat`** sa folder ng repo. Sinisimulan nito ang UI at binubuksan ang **http://127.0.0.1:8765/** sa browser mo
kapag handa na; isara ang itim na window (o pindutin ang Ctrl+C doon) para ihinto ito. Ganito naman mula sa PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
saka ikaw mismo ang magbukas ng **http://127.0.0.1:8765/** (kapag sinimulan sa ganitong paraan, hindi binubuksan ng UI
ang browser; sa localhost lang ito nakikinig).

> **Hindi dapat i-double-click ang `audiocpp_cli.exe` na nasa release zip.** Command-line engine ito na nangangailangan
> ng mga CUDA DLL at ng model sa tabi nito; inilalagay ng `kur.ps1` ang lahat sa tamang lugar at ang Python package ang
> nagpapatakbo rito. Kapag dinouble-click ito, "cudart64_12.dll not found" lang ang lalabas.

**Mga sinusuportahang GPU (release v0.1.1):** native code para sa GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86),
RTX 40xx (sm_89) at RTX 50xx (sm_120a); ang ibang CUDA GPU mula Pascal pataas ay nagpapatakbo ng naka-embed na PTX sa
pamamagitan ng driver (mas mabagal ang unang start). Hindi sinusuportahan ng CUDA 12.8 ang Maxwell (GTX 9xx) at mas luma. Nasubukan namin sa GTX 1050 Ti 4 GB (pati sa Docker Desktop/WSL2 sa Windows, CLI lang); sinukat ni @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (mga detalye sa [docs/linux.md](docs/linux.md)). Malugod naming tinatanggap ang mga ulat mula sa ibang card sa [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (eksperimental):** isang hiwalay na Vulkan engine (walang CUDA) ang ini-install gamit ang `scripts\kur.ps1 -Kok C:\vox -Vulkan`. Sinubukan namin ito sa aming NVIDIA card sa pamamagitan ng Vulkan backend (doon mas mabagal kaysa CUDA, parehong audio sa parehong seed; wala pang malinis na paghahambing ng bilis) at sa integrated na Intel HD Graphics 630 (mga 35-50 segundong compute bawat 1 segundong pananalita); sa AMD ay **hindi** pa namin ito mismo nasubukan: kung susubukan mo, i-post ang resulta sa Discussions. Kapag may higit sa isang Vulkan device (integrated + discrete), isinusulat ng installer ang index ng discrete GPU bilang `cihaz` sa `ayarlar.json`.

*Paalala: Eksperimental pa ang suporta sa Vulkan. Matagumpay itong na-build at nasubukan sa GTX 1050 Ti. May isang
external na user (mitra_tr) din na nag-ulat na napatakbo niya ito sa AMD 6900 XT. Kailangan pa ng mas malawak na
pagsubok sa mga AMD/Intel na card.*

**Pagsubok ng komunidad (AMD):** Pinatakbo ni @mitraTR ang v0.1.1 gamit ang Vulkan sa AMD Radeon RX 6900 XT sa Windows 11: gumana ang pag-install, pagdisenyo ng boses, pagbasa, web interface at mga test; ang pagbasa ay umabot nang mga 0.8-0.9 seg na compute bawat 1 seg ng pananalita ([ulat sa #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Mag-install sa maikling folder na ASCII lang ang laman ng path (hal. `C:\vox`): sa Windows, hindi mabuksan ng engine ang mga path na may ñ o iba pang hindi ASCII na karakter. Lahat ng ulat sa ngayon: [nasubukang hardware](docs/donanim_testleri.md).

**Mga tala sa Vulkan:** mula engine v0.3.1, gumagana na rin sa Vulkan ang timing ng bawat salita. Dalawang package: ang `vulkan` ay nangangailangan ng CPU na may AVX2 (karamihan ng Intel Core mula 2013, AMD mula 2015; wala nito ang maraming Pentium/Celeron); ang [`vulkan-uyumlu`](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan-uyumlu.zip) ay tumatakbo sa anumang 64-bit x86 CPU, pero mga 2.2 beses na mas matagal ang unang pagbasa ng isang boses (pareho ang bilis ng mga susunod na pagbasa). Sinusuri ng `kur.ps1 -Vulkan` ang CPU at ito na mismo ang pumipili ng package. Sa integrated graphics, gumagamit ang engine ng mga 8 GB RAM habang nagbabasa. Maaaring ilang minuto ang unang pagbukas sa Vulkan dahil kino-compile ang mga GPU shader; mas mabilis ang mga susunod na pagbasa. Detalye: [docs/vulkan.md](docs/vulkan.md).

### Alternatibo: i-build ang engine mula sa source

Kailangan ng Visual Studio 2022 Build Tools na may "Desktop development with C++" (kasama ang C++ CMake tools), ~7 GB. Pagkatapos:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Dina-download din nito ang nvcc, kinukuha ang source ng audio.cpp v0.7.2, ina-apply ang
`patches/0001-voxcpm2-4gb-ve-hiz.patch` at bina-build para sa GPU mo (`-Mimari native`, default; o halimbawa
`-Mimari 61`), ~15-25 minuto. Panatilihing maikli ang root (`C:\vox`): pumapalya ang nvcc sa mahahabang path.
Hakbang-hakbang na may mga check: [AGENTS.md](AGENTS.md).

### Mga karaniwang problema sa pag-install

| Nakikita mo | Ano ang ibig sabihin, ano ang gagawin |
|---|---|
| `cudart64_12.dll not found` matapos i-double-click ang exe | Hindi dapat manu-manong simulan ang engine. Patakbuhin ang `kur.ps1` command sa itaas, saka simulan ang web UI. |
| `64-bit Python 3.10+ bulunamadı` (hindi nahanap ang Python) | I-install ang Python (`winget install Python.Python.3.12`), isara ang PowerShell, magbukas ng bago at patakbuhing muli ang parehong command. |
| `motor ekran kartını görmedi` (hindi nakita ng engine ang GPU) | I-update ang NVIDIA driver sa 570 o mas bago; tiyaking tumatakbo ang `nvidia-smi`. |
| `indirme başarısız` / `sha256 tutmadı` (pumalya ang download / hindi tugma ang checksum) | Kadalasan ay naputol na download. Patakbuhing muli ang parehong command; nilalaktawan ang mga file na na-verify na. |
| Build path: pumapalya ang `nvcc` | Panatilihing maikli ang install root (`-Kok C:\vox`). |
| Hindi bumubukas ang page | Simulan ang UI gamit ang `baslat.bat`, o ikaw mismo ang magbukas ng http://127.0.0.1:8765/. Ginagamit na ang port? Palitan ang `"port"` sa `ayarlar.json`. |

May problema? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) o isang
[install issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
kasama ang GPU mo, bersyon ng Windows, ang command at ang mga huling linya ng output nito.

## Paggamit

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
Mga tuntunin sa teksto: isulat ang mga numero sa salita, walang panipi (tinatanggihan ng tool ang mga digit at panipi),
isang pangungusap bawat linya, ≤ 2000 character bawat linya. Paghinto pagkatapos ng linya: `|| bagli` 0.25 s,
`|| normal` 0.5 s, `|| paragraf` 1 s, `|| agir` 1.5 s o sarili mong haba `|| 0,8` (0-5 s; pinapayagan ang mga digit ng
marker). Inaayos ng `ayarlar/okunus_sozlugu.tsv` ang pagbigkas ng mga banyagang salita sa tekstong Turkish. Natutukoy
ang wika mula sa teksto (mga titik na Turkish, sistema ng pagsulat, karaniwang salita; ang `dil` ng voice card kapag
hindi sigurado; opsyonal ang `--dil <code>`). Para sa tekstong hindi Turkish, pinapayagan doon ang apostrophe,
nilalaktawan ang Turkish na diksiyunaryo, at tinatanggihan pa rin ang mga digit. Kapag nag-print ang isang pagbasa ng
`speed gate: satır [...]`, pakinggan ang mga linyang iyon.

### Web UI

Lokal lang (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → ikaw mismo ang magbukas ng
http://127.0.0.1:8765/ (ibang port: `--port 8800`), o i-double-click ang `baslat.bat`. Ihinto ang server gamit ang
Ctrl+C. Tatlong tab: *Magdisenyo ng boses*, *Basahin gamit ang boses na ito*, *Voice cloning*. Ang karaniwang daloy:
*Idisenyo* → pakinggan ang mga variant → *Idagdag sa aking babasahin* → *Basahin gamit ang boses na ito* → i-download.
O pumili ng kasamang boses mula sa voice menu at magbasa.

- **Bersyon sa header.** Isang maliit at malabong `v0.2.0 · <short commit>` (may `+` kapag may hindi pa naka-commit na
  pagbabago ang mga tracked file; bersyon lang kapag walang git), para makita sa mga screenshot at video kung aling
  bersyon ang ginamit.
- **Dalawang boses sa bawat variant card.** Sa itaas, kulay abo, ang *Hilaw na boses ng disenyo*: isang beses lang itong
  ginagawa at hindi na lalabas nang pareho. Sa ibaba nito, sa kulay-dalandan na frame, ang *↻ Ito ang boses na palagi
  mong maririnig*: ang design recording na binasa pabalik bilang reference gamit ang sariling seed ng variant
  (ipinapakita sa card). Ganito ang tunog ng boses sa bawat susunod na pagbasa. Sa ilalim nito ang *Basahin gamit ang
  boses na ito* at *Idagdag sa aking babasahin*. Isang pindot sa *Idisenyo* ang gumagawa ng dalawa: dinidisenyo nito
  ang bawat variant, saka binabasa ang teksto mo gamit ang bawat pangmatagalang boses; iisang progress bar ang
  nagbibilang sa dalawang yugto. Nagkakaroon ng `dinleme.wav` ang folder ng variant. Kapag maagang huminto ang pagbasang
  iyon, naitatabi pa rin ang disenyo at may lalabas na paalala sa card.
- **Ang window na "Tekstong gusto mong marinig".** Sa *Magdisenyo ng boses*, ang kahong *↻ Tekstong gusto mong marinig*
  ang naglalaman ng babasahin ng bawat pangmatagalang boses (kapag iniwang blangko, ang halimbawang pangungusap ang
  babasahin). Kapag kinlik ito, bubukas ang reading notebook sa isang window: mga numero ng linya, line menu, mga pause
  band. Isinusulat ng *OK* ang teksto at ang mga paghinto nito pabalik sa kahon; walang binabago ang *Kanselahin* o Esc.
  May sariling teksto ang reading tab.
- **Ang reading notebook.** Isang pangungusap bawat linya. I-click ang numero ng linya para sa line menu (ilipat pataas
  o pababa, ilipat sa isang posisyon, i-duplicate, burahin; Alt+↑/↓, Alt+Shift+↓, o i-drag gamit ang numero; sabay na
  ina-undo ng Ctrl+Z ang teksto at mga paghinto). I-click ang manipis na band sa pagitan ng dalawang linya para piliin
  ang paghinto (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 s, o sarili mong 0-5 s gamit ang gear); pindutin ang
  Enter nang dalawang beses para sa talata (1 s), at nagiging pause band ang mga blangkong linya. Habang pinapatugtog
  ang resulta, umiilaw ang linyang binabasa at nag-i-scroll ito papasok sa view; pinapatugtog ng *▶ Pakinggan mula
  rito* sa line menu mula sa linyang iyon. Nananatili ang teksto at mga paghinto nito kahit i-reload ang page (browser
  storage).
- **Mga draft.** Nasa parehong notebook (reading tab at ang window) ang button na *📄 Mga draft*. I-save ang kasalukuyang
  teksto kasama ang mga paghinto nito bilang draft, mag-load ng isa sa isang click (ina-undo ng Ctrl+Z), at gamitin ang
  ⋯ para i-overwrite, palitan ang pangalan o burahin ito. Nakatago ang mga draft sa `sesler/taslaklar.json`, hindi
  kailanman sa repository.
- **Reading list at voice menu.** Sa isang variant card, binubuksan ng *Idagdag sa aking babasahin* ang isang kahon ng
  pangalan: bigyan ang variant ng sarili nitong pangalan at idinadagdag ito ng ✓. Nananatili ang *Pangalan ng
  generation* sa bawat variant ng run na iyon. Sa *Basahin gamit ang boses na ito*, binubuksan ng voice button (watawat
  + pangalan) ang voice menu: *Aking listahan ng babasahin* sa itaas, saka ang mga kasamang boses na may watawat (nauuna
  ang wika ng interface). May ▶ pakinggan (ang pangmatagalang boses kapag mayroon), puso (idagdag o alisin) at ⋯ ang
  bawat row; ↑/↓ at Enter para pumili, Esc para isara, at naaalala ang huling boses. Nasa
  `sesler/okuma_listesi.json` ang listahan, labas sa repository, at nananatili ito kahit mag-restart.
- **Pamamahala ng mga boses.** Ang ⋯ menu (row ng voice menu o variant card) ay may *Basahin gamit ang boses na ito*,
  idagdag sa o alisin sa listahan, *Palitan ang pangalan* (ibinabalik ng blangkong pangalan ang orihinal; *Ibalik sa
  orihinal na pangalan*), *Burahin* para sa mga idinisenyong boses at *Itago* para sa mga kasamang boses; parehong
  nagtatanong muna. Inililipat ang binurang boses sa `sesler/_cop/`; hindi kailanman ginagalaw ng pagtatago ang mga
  file ng repository. May *Ibalik* ang *Mga nakatago at binurang boses (N)* sa ibaba ng voice menu. Nakatago ang mga
  custom na pangalan at mga nakatagong boses sa `sesler/yerel_katman.json`. Ipinapakita ng boses na pinalitan ang
  pangalan ang pinagmulan nito sa kulay abo (*pangalan ng generation · variant N*); binubuksan ng ⋯ → *Pumunta sa
  generation* ang disenyo nito.
- **Mga shortcut at file.** Sinisimulan ng Ctrl+Enter (⌘+Enter sa Mac) ang *Idisenyo* o *Basahin gamit ang boses na
  ito* sa nakabukas na tab. Ipinapakita ng progress bar ang *lumipas / ~kabuuan*, na may tantiyang natutunan mula sa
  mga naunang trabaho sa makina mo. Pinapangalanan ang download ayon sa boses at oras
  (`Voice_Name_2026-11-02_0152.wav`).

**Voice cloning (sarili mong boses o boses na may pahintulot).** Sa *Voice cloning* tab ng UI, ibigay ang recording mo (wav/mp3/flac/ogg, iminumungkahi ang 5-30 s ng malinis na pananalita; tinatanggihan ang wala pang 3 s, pinuputol ang lampas 36 s), ang eksaktong transcript nito at ang tekstong babasahin. Naka-disable ang button hangga't hindi mo nilalagyan ng tsek ang "Akin ang boses na ito o may malinaw akong pahintulot mula sa may-ari". Sa lokal na server (127.0.0.1) lang napupunta ang recording, pinoproseso ito sa isang temp folder kasama ang reference encoding nito, at binubura ang folder na iyon kapag natapos ang trabaho, pati kapag pumalya ito; walang ipinapadala sa network. Ang synthetic na output lang ang itinatabi (UI: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Ang output ay `klon_synthetic.wav` na may tag na "synthetic"; lagyan ito ng label na AI-generated kapag ibinabahagi. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## FAQ

**Model o engine? Alin ang alin?** Ang VoxCPM2 (OpenBMB) ang *model*: ang network na may 2 bilyong parameter na
ginagawang pananalita ang teksto. Ang audio.cpp ang *engine*: ang C++/CUDA na programang nagpapatakbo ng model sa GPU
mo (`audiocpp_cli.exe`). Ang engine ang binabago ng aming patch, hindi ang model: pinagkakasya nito ang VoxCPM2 sa 4 GB
at tinitiyak na laging parehong audio ang ibinibigay ng parehong seed. Ang Python package sa repo na ito ay naghahanda
lang ng teksto, tumatawag sa engine at nagtitipon ng mga file.

**Aling mga GPU?** Tingnan ang "Mga sinusuportahang GPU" sa itaas: NVIDIA mula GTX 10xx pataas, 4 GB VRAM o higit pa,
driver ≥ 570. May native code sa release para sa sm_61/75/86/89/120a; ang ibang card na Pascal o mas bago ay gumagamit
ng naka-embed na PTX (mas mabagal ang unang start). AMD/Intel: eksperimental na Vulkan zip, `kur.ps1 -Vulkan`; may
external na user na nag-ulat na napatakbo niya ito sa AMD 6900 XT, pero kailangan pa ng mas malawak na pagsubok sa
AMD/Intel (tingnan ang "AMD / Intel" sa itaas). Tumatakbo ang CPU-only (`"backend": "cpu"` sa `ayarlar.json`) pero
~6× na mas mabagal kaysa GTX 1050 Ti (sukat ng engine, 535 s laban sa 94 s para sa 48 s na pananalita); hindi ito
sinusuportahang paraan.

**Gaano kabilis?** Sinukat sa GTX 1050 Ti 4 GB (i7-7700HQ): isang design variant (≈ 25 s na recording) 55 s; pagbasa ≈
2 s ng compute bawat 1 s ng pananalita (real-time factor 1.9-2.8) pagkatapos ng isang beses na ~50 s na reference
encoding bawat boses (naka-cache sa disk) at 10-20 s na pag-load ng model bawat batch; peak na VRAM 2.6-2.9 GB. Mas
mabilis ang mas bagong card; mga numero at pamamaraan: [docs/4gb.md](docs/4gb.md).

**Kaya ba nitong mag-clone ng boses?** Kayang gayahin ng VoxCPM2 model ang isang boses mula sa reference recording, at
iyon ang ginagamit ng bahaging cloning. Gamitin lang ito sa sarili mong boses o nang may malinaw na pahintulot ng taong
may-ari ng boses; hihilingin ng UI na kumpirmahin mo ang pahintulot na iyon. Hindi kailangan ng recording sa
pagdidisenyo ng boses: nagsisimula ito sa isang tekstong paglalarawan sa Ingles o Chinese, at ang "reference" na
ginagamit sa pagbasa ng idinisenyong boses ay ang sariling synthetic na design recording ng model. Bawal ang
panggagaya sa ibang tao, panloloko at panlilinlang. Tingnan ang [ETHICS.md](ETHICS.md). Lagyan ng label na
AI-generated ang anumang inilalathala mo.

**Paano sumulat ng mahusay na paglalarawan ng boses?** Sa Ingles, 1-3 pangungusap: edad at kasarian, timbre
(malalim/maliwanag, mainit, ngongo, paos), tono at papel (kalmadong documentary narrator, masiglang presenter), tempo
(mabagal, may sukat), at "clean studio recording, no background noise". Panatilihin itong paglalarawan, hindi script;
walang panaklong. Humingi ng 3-5 variant at pakinggan: malaki ang nababago ng seed sa boses. Para sa tekstong
paglikha, gumamit ng 1-3 natural na pangungusap sa wika ng boses, sa mood na gusto mo (hanggang ~30 s na pananalita).
Kapag nagbabasa, isang pangungusap bawat linya; hatiin ang mahahabang pangungusap, isulat ang mga numero sa salita.

## Pag-aambag

Hindi sigurado kung saan magsisimula? Magandang unang hakbang ang apat na maliliit na issue na ito:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Subukan ito sa GPU mo at iulat ang card, driver at mga oras
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: subukan ang eksperimental na Vulkan build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Magdagdag ng pangungusap sa test set
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Ibahagi ang isang boses na idinisenyo mo, kasama ang paglalarawan at seed nito

**Subukan ang graphics card mo, magsulat ng ulat:** hindi kailangang marunong mag-code, sapat na ang [form ng ulat sa pagsubok ng hardware](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); wala pang ulat mula sa Intel graphics card.

Pinagsasaluhang test set: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); gabay sa brand voice:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); paano magpadala ng code: [CONTRIBUTING.md](CONTRIBUTING.md).
Mga problema sa pag-install: [issue form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); mga tanong at resulta: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Sinusunod ng lahat ng kalahok ang [Code of Conduct](CODE_OF_CONDUCT.md): maging mabait, at panatilihing tungkol sa
trabaho ang feedback.

## Mga nag-ambag

- [@alexturkey](https://github.com/alexturkey): maintainer; code, mga kasamang boses, docs
- [@cayir21](https://github.com/cayir21): suporta sa Metal para sa macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): ayos sa end-of-sentence (EOS) para sa pagbasa ng maraming pangungusap sa CPU backend, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): eksperimental na pag-install ng CUDA para sa Ubuntu/Linux at suporta sa Docker, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Nararapat din dito ang pangalan mo: resulta ng test mula sa GPU mo, isang pangungusap para sa test set, isang boses na
idinisenyo mo, malinaw na bug report o pull request, lahat ng iyan ay binibilang na ambag. Salamat sa lahat ng
sumusubok at nagbibigay ng balita.

## Lisensya at pagkilala

Code at mga kasamang boses: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Binuo sa ibabaw ng VoxCPM2 (OpenBMB,
Apache-2.0), audio.cpp (ShugoAI LLC, Apache-2.0) at ang GGUF conversion ng audio.cpp. Buong listahan:
[THIRD_PARTY.md](THIRD_PARTY.md). Walang kaugnayan sa OpenBMB, ModelBest o sa proyektong audio.cpp.

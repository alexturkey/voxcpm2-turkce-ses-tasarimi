[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · **Kiswahili**

# voxcpm2-turkce-ses-tasarimi

**Ubunifu wa sauti za Kituruki kwa VoxCPM2 kwenye GPU ya 4 GB.** Eleza sauti kwa Kiingereza, acha modeli iiunde, chagua
toleo unalolipenda, kisha soma maandishi yoyote ya Kituruki kwa sauti hiyo. Mradi unajumuisha kisakinishi cha amri moja,
injini ya [audio.cpp](https://github.com/0xShug0/audio.cpp) iliyorekebishwa inayotosha kwenye GTX 1050 Ti (4 GB), kiolesura
kidogo cha wavuti kinachoendeshwa kwenye kompyuta yako, na sauti kumi na nne bandia zilizo tayari: saba za Kituruki na
wasimulizi saba wazawa wa Kiingereza, Kifaransa, Kijerumani, Kihispania, Kirusi, Kichina na Kijapani.

- Programu inasoma katika lugha 30; kiolesura nacho kinapatikana katika lugha 30.
- Sauti 14 zilizo tayari: 7 za Kituruki, pamoja na moja kwa kila lugha ya Kiingereza, Kifaransa, Kijerumani, Kihispania, Kirusi, Kichina na Kijapani.
- Kiolesura cha wavuti (v0.2.0): kila kadi ya toleo ina sauti mbili, sauti ghafi ya muundo na sauti utakayoendelea kuisikia;
  orodha ya kusoma yenye menyu ya sauti; badilisha jina, ficha au futa sauti; rasimu za maandishi unayoyasoma. Tazama
  "Kiolesura cha wavuti" chini ya "Matumizi".

[Jinsi inavyotosha kwenye 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Mwongozo wa usakinishaji kwa mawakala wa AI](AGENTS.md) · [Matumizi ya kuwajibika](ETHICS.md)

> Sauti zilizojumuishwa ni bandia, zimebuniwa kutokana na maelezo ya maandishi. Sehemu ya kunakili sauti ni kwa ajili ya sauti
> yako mwenyewe tu, au sauti inayotumiwa kwa ruhusa ya wazi ya mmiliki wake; kiolesura kinakuomba uthibitishe ruhusa hiyo.
> Kuiga watu wengine, ulaghai na udanganyifu ni marufuku. Weka alama kwamba ulichotengeneza kimetengenezwa na AI. Tazama
> [ETHICS.md](ETHICS.md).

## Lugha 30

Tulitengeneza video moja ya makala kuhusu Kapadokia katika lugha 8: Kituruki, Kiingereza, Kifaransa, Kijerumani,
Kihispania, Kirusi, Kichina na Kijapani. Kila lugha ina **msimulizi wake mzawa**, aliyebuniwa kwa VoxCPM2 kutokana na
maelezo ya Kiingereza. Yote yalitengenezwa kikamilifu kwenye kompyuta yetu, kwa GTX 1050 Ti ya 4 GB, kwa ubora uleule
usiobadilika (hatua 16, cfg 2.0). Wasimulizi saba wamejumuishwa hapa, pamoja na maelezo yao, maandishi ya ubunifu, mbegu
(seed) na rekodi ya marejeo.

| Msimbo | Lugha | Sauti | Sikiliza | Video |
|---|---|---|---|---|
| `tr` | Kituruki | `hazir/belgesel_hanim` (na nyingine 6) | [mfano](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Kiingereza | `hazir/anlatici_en` | [mfano](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Kifaransa | `hazir/anlatici_fr` | [mfano](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Kijerumani | `hazir/anlatici_de` | [mfano](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Kihispania | `hazir/anlatici_es` | [mfano](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Kirusi | `hazir/anlatici_ru` | [mfano](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Kichina (Kimandarini) | `hazir/anlatici_zh` | [mfano](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Kijapani | `hazir/anlatici_ja` | [mfano](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Kwa nini sentensi moja moja.** VoxCPM2 haiko thabiti katika uzalishaji mmoja mrefu (takriban zaidi ya sekunde 30): mdundo
unaongezeka kasi na sauti inaweza kupotoka. Hapa sauti inabebwa na rekodi ya marejeo na mbegu zisizobadilika, na maandishi
marefu yanasomwa sentensi moja kwa kila mstari, hivyo rangi ya sauti na mtindo hubaki vilevile kuanzia sentensi ya kwanza
hadi ya mwisho. Kwa lugha zisizo Kituruki, kamusi ya matamshi ya Kituruki haitumiki. Lugha zote 30 zinazoungwa mkono na
VoxCPM2 zimejaribiwa na zinafanya kazi; kwa zile zisizo na sauti iliyojumuishwa tumia `--dil <code>`. Amri za kila lugha na
mafunzo tuliyopata: [docs/cok_dilli.md](docs/cok_dilli.md). Ujuzi (skill) wa Claude Code kwa mtiririko mzima wa ubunifu:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**Mifano 144 ya maelezo ya kuanzia.** Majukumu 18 (msimulizi wa makala, mtangazaji wa habari, sauti ya matangazo, kitabu
cha sauti, bibi msimulizi wa hadithi, mwendeshaji wa podikasti, mwalimu, kionjo cha filamu, kiongozi wa tafakari,
mtangazaji wa michezo na mengine, ya kiume na ya kike) katika kila moja ya lugha 8. Maelezo ni ya Kiingereza, yakitaja
uraia wa msemaji na lafudhi yake ya asili; maandishi yanayosomwa wakati sauti inaundwa yanakuja pamoja nayo, katika lugha
hiyo na yakilingana na jukumu. Chagua mmoja, sikiliza matoleo, baki na lile unalolipenda:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, au chagua *Maelezo ya mfano* kwenye kiolesura cha
wavuti. Orodha kamili: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Tafsiri video zako kwa sauti yako mwenyewe.** [DubWorld](https://github.com/alexturkey/dubworld) ni programu yetu ya
kutafsiri na kuweka sauti kwenye video (dubbing) inayofanya kazi kwenye kompyuta yako; inasakinisha hazina hii kama injini
yake ya sauti ya VoxCPM2. Sauti unayoibuni hapa inatumika huko kwa `ses.voxcpm2_ses = "<name>/<variant>"`.

## Kuanza haraka (Windows, hatua 3)

1. **Pakua** msimbo: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Kifurushi cha injini kilicho tayari kwa kadi yako kinapakuliwa na kisakinishi katika hatua ya 3:
   NVIDIA → [kifurushi cha CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [kifurushi cha Vulkan, cha majaribio](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (umeshapakua kimoja? ongeza `-HazirZip <path to the zip>` kwenye amri iliyo hapa chini).
2. **Fungua** zip, ingia kwenye folda ya `voxcpm2-turkce-ses-tasarimi-main`, andika `powershell` kwenye upau wa anwani wa
   Explorer kisha bonyeza Enter.
3. **Endesha** kisakinishi (kinahitaji Python ya 64-bit 3.10-3.13; kiendeshi (driver) cha NVIDIA ≥ 570 kwa CUDA), kisha bofya mara mbili **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: ongeza `-Vulkan` mwishoni. Kiolesura kinafunguka kwenye http://127.0.0.1:8765/.

Zip ya injini si programu inayojitegemea (exe yake inahitaji modeli na DLL zinazowekwa na kisakinishi). Maelezo zaidi,
orodha ya GPU na matatizo ya kawaida: "Usakinishaji wa haraka" hapa chini.

## Ubuntu / Linux (NVIDIA CUDA, ya majaribio)

Jenga injini iliyorekebishwa kwa `bash scripts/kur-linux.sh`, au tumia `Dockerfile.linux` kujenga na kuendesha ndani ya
mazingira ya Ubuntu 24.04 / CUDA 12.8.1. Inahitaji GPU ya NVIDIA na kiendeshi kinachoendana; kisakinishi cha moja kwa moja
kinahitaji pia CUDA toolkit na Python 3.10-3.13. Kiolesura kinabaki kwenye loopback pekee, hata kwenye seva za mbali
(usambazaji kupitia SSH). Mahitaji ya awali, amri, uchaguzi wa usanifu (architecture) na wigo wa uthibitishaji:
[docs/linux.md](docs/linux.md).

## Kuanza haraka (macOS, Apple Silicon)

Inahitaji Xcode Command Line Tools (`xcode-select --install`) na [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Kisakinishi kinapakua modeli, kinajenga injini iliyorekebishwa kwa Metal (~dakika 1) na kuweka kila kitu chini ya `~/vox`.
Kisha bofya mara mbili **`baslat.command`**. Kwenye MacBook Air M4 16 GB: ~s 2 za ukokotoaji kwa kila s 1 ya usemi, mbegu
ileile inatoa sauti inayofanana baiti kwa baiti, kilele cha RAM ~5.3 GB, hakuna kupungua kwa kasi kutokana na joto katika
dakika 12 za usomaji mfululizo. Maelezo na vipimo: [docs/mac.md](docs/mac.md).

**Programu asilia ya Mac (bila Python, Homebrew wala Terminal):** [macos/README.md](macos/README.md). Inajumuisha injini
ileile iliyorekebishwa na inapakua modeli inapofunguliwa kwa mara ya kwanza; kwa sasa inajengwa kutoka msimbo chanzo kwa Xcode.

## Kwa watumiaji wa Mac (Apple Silicon)

Pia kuna marekebisho huru, yaliyotengenezwa na jamii, kwa Mac zenye Apple Silicon yanayoendesha VoxCPM2 kwa mfumo wa MLX
wa Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Yanatengenezwa na kutunzwa na Emre Koç ([@emre-koc](https://github.com/emre-koc)) katika hazina yake mwenyewe, si hapa;
hatua za usakinishaji na maswali ya msaada yapelekwe huko. Asante, Emre, kwa kuuleta mradi huu kwenye Mac!

## Jinsi inavyofanya kazi

1. **Ubunifu wa sauti.** *Maelezo ya sauti* kwa Kiingereza + *maandishi yanayosomwa wakati sauti inaundwa* (katika lugha
   ya sauti hiyo) + idadi ya matoleo. Kila toleo linapata mbegu yake; injini inapokea `(description)text` na kurudisha
   rekodi ya ubunifu kwa kila mbegu. Maandishi ni mfano mfupi wa kuifahamu sauti: sentensi 1-3, si zaidi ya ~s 30
   (kiolesura kinaonyesha makadirio na hakianzi ikiwa ni zaidi ya s 33); maandishi marefu ni ya hatua ya 2.
2. **Usomaji unaotegemea marejeo.** Rekodi ya ubunifu inapelekwa kwenye pembejeo **zote mbili** za injini (`audio` na
   `voice_ref`), pamoja na nakala yake ya maandishi (`reference_text`) na maandishi mapya ya kusoma, kwa mbegu ileile.
   Sauti inabebwa na rekodi, si na maelezo, hivyo haipotoki kutoka maandishi moja hadi mengine. Maandishi yanasomwa
   sentensi moja moja.
3. Ubora haubadiliki: hatua 16 za diffusion, CFG 2.0. Mbegu si kitufe cha ubora.
4. **Muda wa kila neno, sauti ileile kila mara.** Wakati wa kusoma, injini yenyewe huonyesha mahali kila neno linapoanza na kuishia (marekebisho 0002, bila modeli ya ziada). Nyakati huandikwa kwenye `kelimeler.json`, na mistari hupunguzwa ili pengo kati ya mistari liwe sawa na mpangilio wa kituo. Usahihi ukilinganishwa na upangaji wa lazima wa CTC (forced alignment, CTC = 100%): 88% (Kituruki, sauti 12; mpangilio `kelime_zamani`, umewashwa kwa chaguo-msingi). Kwa marekebisho 0003, mbegu ileile hutoa sauti inayofanana baiti kwa baiti kila mara.

Rekodi ghafi ya ubunifu ni mfano wa mara moja tu wa sauti; hakuna usomaji wa baadaye unaosikika sawa kabisa nayo. Unachosikia
katika kila usomaji wa baadaye ni hatua ya 2: rekodi ya ubunifu kama marejeo pamoja na mbegu ya toleo hilo. Ndiyo maana
kiolesura cha wavuti kinafanya hatua ya 2 mara tu baada ya ubunifu na kuonyesha zote mbili kwenye kadi ya toleo.

Injini ni audio.cpp v0.7.2 pamoja na marekebisho yetu (`patches/`), na modeli ni VoxCPM2 Q8_0 GGUF. Kilele cha VRAM ≈ 2.8 GB;
takriban s 2 za ukokotoaji kwa kila s 1 ya usemi kwenye GTX 1050 Ti. Maelezo na vipimo: [docs/4gb.md](docs/4gb.md).

## Sauti zilizojumuishwa (`hazir_sesler/`)

Zote kumi na nne zimebuniwa kutokana na maelezo yaliyohifadhiwa katika `ses.json` zao; hakuna hata moja iliyonakiliwa
kutoka rekodi (kunakili ni kichupo tofauti cha *Kunakili sauti*, kinachohitaji ridhaa).

| Sauti | Maelezo mafupi | Sikiliza |
|---|---|---|
| `belgesel_hanim` | Mwanamke mkomavu wa miaka hamsini, alto nzito na ya joto; msimulizi mtulivu wa makala | [mfano](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [marejeo](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Msimulizi wa kiume mwenye sauti nzito, yenye nguvu na ya kifumbo | [mfano](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [marejeo](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Mtangazaji wa habari mzoefu wa takriban miaka sabini, mtulivu na mwenye mamlaka | [mfano](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [marejeo](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Mtangazaji wa kike wa habari za jioni mwenye haiba, wa miaka thelathini, sauti laini kama velveti na yenye hisia | [mfano](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [marejeo](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Mchawi wa hadithi za kale: sauti ya chini, ya puani kidogo, tamu kwa ujanja | [mfano](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [marejeo](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Msimulizi wa kiume mwenye sauti nzito kupita kawaida, iliyoshiba na ya kuamrisha | [mfano](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [marejeo](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Mzee mwenye busara, sauti nzito na inayovuma, ya kifumbo kidogo | [mfano](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [marejeo](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Msimulizi wa kiume wa makala, mzawa wa Kiingereza, wa miaka hamsini (General American); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Msimulizi wa kiume wa makala, mzawa wa Kifaransa, wa miaka hamsini (Paris); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Msimulizi wa kiume wa makala, mzawa wa Kijerumani, wa miaka hamsini (Hochdeutsch); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Msimulizi wa kiume wa makala, mzawa wa Kihispania, wa miaka hamsini (Kikastilia (Madrid)); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Msimulizi wa kiume wa makala, mzawa wa Kirusi, wa miaka hamsini (Moscow); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Msimulizi wa kiume wa makala, mzawa wa Kichina (Kimandarini), wa miaka hamsini (Putonghua ya Beijing); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Msimulizi wa kiume wa makala, mzawa wa Kijapani, wa miaka hamsini (lafudhi sanifu ya Tokyo); sauti nzito, tulivu, ya joto | [mfano](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [marejeo](hazir_sesler/anlatici_ja/referans.flac) |

Kila folda: `referans.flac` (rekodi ya ubunifu isiyopoteza ubora), `ses.json` (maelezo, nakala ya maandishi, mbegu ya
ubunifu, mbegu ya usomaji, maelezo mafupi; `dil` = lugha kwa wasimulizi), `ornek_okuma.mp3` (+ maandishi yake). Zitumie
moja kwa moja: `--ses hazir/<name>`. Rekodi za marejeo za wasimulizi ni fupi (s 5.6-10); mifano yao ni sentensi tatu za
kwanza za hati ya Kapadokia, zilizokatwa kutoka usomaji kamili wa uzalishaji.

## Usakinishaji wa haraka, bila compiler (Windows 10/11, GPU ya NVIDIA ≥ 4 GB)

Mahitaji ya awali: kiendeshi cha NVIDIA ≥ 570 na Python ya 64-bit 3.10-3.13 (`winget install Python.Python.3.12`). Hakuna
kingine: hakuna Visual Studio, hakuna kisakinishi cha CUDA. Huna uhakika una kadi gani? Endesha `nvidia-smi` katika
PowerShell: inaonyesha jina la GPU, toleo la kiendeshi na kumbukumbu. Huna kadi ya NVIDIA? Tazama "AMD / Intel" hapa chini.

Ukiwa na [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Bila Git: kwenye ukurasa huu bofya **Code → Download ZIP**, ifungue, ingia kwenye folda iliyofunguliwa ya
`voxcpm2-turkce-ses-tasarimi-main`, andika `powershell` kwenye upau wa anwani wa Explorer na ubonyeze Enter, kisha endesha
mstari wa mwisho ulio hapo juu. Git inahitajika tu kwa njia ya kujenga kutoka msimbo chanzo.

`-ExecutionPolicy Bypass` inahusu mchakato huu mmoja tu na haibadilishi mpangilio wowote wa mfumo; soma `scripts\kur.ps1`
kabla ya kuiendesha, kama ilivyo kwa hati yoyote ya usakinishaji. Amri moja, ~dakika 10, upakuaji wa ~3.7 GB, kila kitu
kimethibitishwa kwa sha256: modeli (2.95 GB), DLL za runtime za CUDA 12.8 kama zip zinazobebeka (hakuna usakinishaji wa
mfumo, PATH haiguswi), **injini iliyojengwa tayari** kutoka ukurasa wa Releases, `.venv` yenye vifurushi viwili vya Python,
`ayarlar.json`, na ukaguzi wa mwisho wa GPU (`KONTROL_OK`). Iendeshe tena baada ya hitilafu yoyote; faili zilizothibitishwa
zinarukwa. Kisha anzisha kiolesura cha wavuti: bofya mara mbili **`baslat.bat`** kwenye folda ya hazina. Kinaanzisha
kiolesura na kufungua **http://127.0.0.1:8765/** kwenye kivinjari chako kikiwa tayari; funga dirisha jeusi (au bonyeza
Ctrl+C humo) ili kukisimamisha. Vivyo hivyo kutoka PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
kisha fungua **http://127.0.0.1:8765/** mwenyewe (kikianzishwa hivi, kiolesura hakifungui kivinjari; kinasikiliza
localhost pekee).

> **`audiocpp_cli.exe` iliyo ndani ya zip ya toleo haikusudiwi kubofywa mara mbili.** Ni injini ya mstari wa amri
> inayohitaji DLL za CUDA na modeli kando yake; `kur.ps1` inaweka kila kitu mahali pake na kifurushi cha Python ndicho
> kinachoiendesha. Ukiibofya mara mbili utaona tu "cudart64_12.dll not found".

**GPU zinazoungwa mkono (toleo v0.1.1):** msimbo asilia kwa GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) na RTX 50xx (sm_120a); GPU nyingine yoyote ya CUDA kuanzia Pascal inaendesha PTX iliyopachikwa kupitia kiendeshi
(uanzishaji wa kwanza ni wa polepole zaidi). Maxwell (GTX 9xx) na za zamani zaidi haziungwi mkono na CUDA 12.8.
Imejaribiwa nasi kwenye GTX 1050 Ti 4 GB (pia kupitia Docker Desktop/WSL2 kwenye Windows, CLI pekee); imepimwa na
@mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (maelezo katika [docs/linux.md](docs/linux.md)).
Ripoti kutoka kadi nyingine zinakaribishwa katika [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (ya majaribio):** zip tofauti ya injini ya Vulkan (`...-win64-vulkan.zip`, bila CUDA) inasakinishwa kwa
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Imethibitishwa tu kwenye kadi yetu ya NVIDIA kupitia backend ya Vulkan (huko
ilienda polepole kuliko CUDA lakini ilitoa sauti ileile kwa mbegu ileile; kipimo hicho kilichukuliwa wakati diski
ilikuwa na shughuli nyingine, hivyo ulinganisho safi wa kasi bado unasubiriwa) na **hatujaijaribu** sisi wenyewe kwenye
vifaa vya AMD wala Intel: ukiijaribu, tafadhali weka matokeo katika Discussions. Kukiwa na zaidi ya kifaa kimoja cha Vulkan
(kilichojengwa ndani + cha pekee), kisakinishi kinaandika namba ya GPU ya pekee kama `cihaz` ndani ya `ayarlar.json`.

**Kumbuka:** Usaidizi wa Vulkan kwa sasa ni wa majaribio. Umejengwa na kujaribiwa kwa mafanikio kwenye GTX 1050 Ti.
Mtumiaji wa nje (mitra_tr) pia ameripoti kuuendesha kwenye AMD 6900 XT. Majaribio mapana zaidi kwenye kadi za AMD/Intel
bado yanahitajika.

**Jaribio la jamii (AMD):** @mitraTR aliendesha v0.1.1 kwa Vulkan kwenye AMD Radeon RX 6900 XT katika Windows 11: usakinishaji, kubuni sauti, kusoma, kiolesura cha wavuti na majaribio vyote vilifanya kazi; kusoma kulichukua takriban sek 0.8-0.9 za hesabu kwa kila sek 1 ya usemi ([ripoti katika #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Sakinisha kwenye folda fupi ambayo njia yake ina herufi za ASCII pekee (k.m. `C:\vox`): kwenye Windows injini haiwezi kufungua njia zenye herufi zisizo za ASCII. Ripoti zote hadi sasa: [vifaa vilivyojaribiwa](docs/donanim_testleri.md).

### Njia mbadala: jenga injini kutoka msimbo chanzo

Inahitaji Visual Studio 2022 Build Tools pamoja na "Desktop development with C++" (ikijumuisha C++ CMake tools), ~7 GB. Kisha:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Hii pia inapakua nvcc, inaleta msimbo chanzo wa audio.cpp v0.7.2, inatumia `patches/0001-voxcpm2-4gb-ve-hiz.patch` na
kujenga kwa ajili ya GPU yako (`-Mimari native`, chaguo-msingi; au mfano `-Mimari 61`), ~dakika 15-25. Weka mzizi mfupi
(`C:\vox`): nvcc inashindwa kwenye njia ndefu. Hatua kwa hatua pamoja na ukaguzi: [AGENTS.md](AGENTS.md).

### Matatizo ya kawaida ya usakinishaji

| Unachokiona | Maana yake, nini cha kufanya |
|---|---|
| `cudart64_12.dll not found` baada ya kubofya exe mara mbili | Injini haikusudiwi kuanzishwa kwa mkono. Endesha amri ya `kur.ps1` iliyo juu, kisha anzisha kiolesura cha wavuti. |
| `64-bit Python 3.10+ bulunamadı` (Python haikupatikana) | Sakinisha Python (`winget install Python.Python.3.12`), funga PowerShell, fungua mpya na uendeshe amri ileile tena. |
| `motor ekran kartını görmedi` (injini haikuiona GPU) | Sasisha kiendeshi cha NVIDIA hadi 570 au mpya zaidi; hakikisha `nvidia-smi` inafanya kazi. |
| `indirme başarısız` / `sha256 tutmadı` (upakuaji umeshindwa / checksum hailingani) | Kwa kawaida ni upakuaji uliokatika. Endesha amri ileile tena; faili zilizothibitishwa zinarukwa. |
| Njia ya kujenga: `nvcc` inashindwa | Weka mzizi wa usakinishaji mfupi (`-Kok C:\vox`). |
| Ukurasa haufunguki | Anzisha kiolesura kwa `baslat.bat`, au fungua http://127.0.0.1:8765/ mwenyewe. Port ina shughuli? Badilisha `"port"` ndani ya `ayarlar.json`. |

Matatizo? [Discussions (Maswali na Majibu)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) au
[tatizo la usakinishaji (issue)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
pamoja na GPU yako, toleo la Windows, amri uliyoendesha na mistari yake ya mwisho.

## Matumizi

Mstari wa amri:
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
Kanuni za maandishi: andika namba kwa maneno, bila alama za nukuu (zana inakataa tarakimu na alama za nukuu), sentensi moja
kwa kila mstari, herufi ≤ 2000 kwa kila mstari. Kituo baada ya mstari: `|| bagli` s 0.25, `|| normal` s 0.5, `|| paragraf`
s 1, `|| agir` s 1.5 au urefu wako mwenyewe `|| 0,8` (s 0-5; tarakimu za alama hii zinaruhusiwa).
`ayarlar/okunus_sozlugu.tsv` inarekebisha matamshi ya maneno ya kigeni katika maandishi ya Kituruki. Lugha inatambuliwa
kutokana na maandishi (herufi za Kituruki, mfumo wa maandishi, maneno ya kawaida; `dil` ya kadi ya sauti ikiwa hakuna
uhakika; `--dil <code>` ni ya hiari). Kwa maandishi yasiyo ya Kituruki, apostrofi zinaruhusiwa hapo, kamusi ya Kituruki
inarukwa, na tarakimu bado zinakataliwa. Usomaji ukichapisha `speed gate: satır [...]`, sikiliza mistari hiyo.

### Kiolesura cha wavuti

Ndani ya kompyuta pekee (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → fungua http://127.0.0.1:8765/
mwenyewe (port nyingine: `--port 8800`), au bofya mara mbili `baslat.bat`. Simamisha seva kwa Ctrl+C. Vichupo vitatu:
*Buni sauti*, *Soma kwa sauti hii*, *Kunakili sauti*. Njia ya kawaida: *Buni* → sikiliza matoleo → *Ongeza kwenye orodha
yangu ya kusoma* → *Soma kwa sauti hii* → pakua. Au chagua sauti iliyojumuishwa kutoka menyu ya sauti na usome.

- **Toleo kwenye kichwa cha ukurasa.** `v0.2.0 · <short commit>` ndogo na hafifu (pamoja na `+` faili zinazofuatiliwa
  zinapokuwa na mabadiliko ambayo hayajafanyiwa commit; toleo pekee bila git), ili picha za skrini na video zionyeshe
  toleo lililotumika.
- **Sauti mbili kwenye kila kadi ya toleo.** Juu, kwa rangi ya kijivu, *Sauti ghafi ya muundo*: inatengenezwa mara moja na
  haitoki sawa tena. Chini yake, ndani ya fremu ya rangi ya chungwa, *↻ Hii ndiyo sauti utakayoisikia kila wakati*: rekodi
  ya ubunifu ikisomwa tena kama marejeo kwa mbegu ya toleo hilo (inaonyeshwa kwenye kadi). Hivi ndivyo sauti inavyosikika
  katika kila usomaji wa baadaye. Chini yake kuna *Soma kwa sauti hii* na *Ongeza kwenye orodha yangu ya kusoma*. Mbonyezo
  mmoja wa *Buni* unafanya yote mawili: unabuni kila toleo, kisha unasoma maandishi yako kwa kila sauti ya kudumu; upau
  mmoja wa maendeleo unahesabu awamu zote mbili. Folda ya toleo inapata `dinleme.wav`. Usomaji huo ukisimama mapema,
  ubunifu unabaki na kadi inaonyesha dokezo.
- **Dirisha la "Maandishi unayotaka kusikia".** Katika *Buni sauti*, kisanduku cha *↻ Maandishi unayotaka kusikia* kinashika
  kile ambacho kila sauti ya kudumu inasoma (kikiachwa wazi, sentensi ya mfano ndiyo inasomwa). Ukikibofya kinafungua
  daftari la kusoma ndani ya dirisha: namba za mistari, menyu ya mstari, mikanda ya vituo. *Sawa* inaandika maandishi na
  vituo vyake kurudi kwenye kisanduku; *Ghairi* au Esc haibadilishi chochote. Kichupo cha kusoma kinaweka maandishi yake
  mwenyewe.
- **Daftari la kusoma.** Sentensi moja kwa kila mstari. Bofya namba ya mstari kupata menyu ya mstari (sogeza juu au chini,
  peleka kwenye nafasi fulani, nakili, futa; Alt+↑/↓, Alt+Shift+↓, au buruta kwa namba; Ctrl+Z inatengua maandishi na vituo
  pamoja). Bofya mkanda mwembamba kati ya mistari miwili kuchagua kituo (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 s,
  au chako mwenyewe cha s 0-5 kwa gia); bonyeza Enter mara mbili kwa aya (s 1), na mistari mitupu inakuwa mikanda ya vituo.
  Matokeo yanapocheza, mstari unaosomwa unang'aa na kusogea kuonekana; *▶ Sikiliza kuanzia hapa* katika menyu ya mstari
  inacheza kuanzia mstari huo. Maandishi na vituo vyake vinabaki hata ukurasa ukipakiwa upya (hifadhi ya kivinjari).
- **Rasimu.** Kitufe cha *📄 Rasimu* kipo kwenye madaftari yote mawili (kichupo cha kusoma na dirisha). Hifadhi maandishi ya
  sasa pamoja na vituo vyake kama rasimu, pakia moja kwa mbofyo (Ctrl+Z inatengua), na tumia ⋯ kuiandika upya, kuibadilisha
  jina au kuifuta. Rasimu zinahifadhiwa katika `sesler/taslaklar.json`, kamwe si ndani ya hazina.
- **Orodha ya kusoma na menyu ya sauti.** Kwenye kadi ya toleo, *Ongeza kwenye orodha yangu ya kusoma* inafungua kisanduku
  cha jina: lipe toleo jina lake mwenyewe na ✓ inaliongeza. *Jina la uundaji* linabaki kwenye kila toleo la uzalishaji huo.
  Katika *Soma kwa sauti hii*, kitufe cha sauti (bendera + jina) kinafungua menyu ya sauti: *Orodha yangu ya kusoma* juu,
  kisha sauti zilizojumuishwa pamoja na bendera (lugha ya kiolesura kwanza). Kila safu ina ▶ sikiliza (sauti ya kudumu
  ikiwepo), moyo (ongeza au ondoa) na ⋯; ↑/↓ na Enter huchagua, Esc hufunga, sauti ya mwisho inakumbukwa. Orodha
  inahifadhiwa katika `sesler/okuma_listesi.json`, nje ya hazina, na inadumu hata baada ya kuanzisha upya.
- **Kusimamia sauti.** Menyu ya ⋯ (safu ya menyu ya sauti au kadi ya toleo) ina *Soma kwa sauti hii*, kuongeza au kuondoa
  kwenye orodha, *Badilisha jina* (jina tupu linarudisha la asili; *Rudi kwenye jina la asili*), *Futa* kwa sauti
  zilizobuniwa na *Ficha* kwa zilizojumuishwa; zote mbili zinauliza kwanza. Sauti iliyofutwa inahamia `sesler/_cop/`;
  kuficha hakugusi kamwe faili za hazina. *Sauti zilizofichwa na kufutwa (N)* chini ya menyu ya sauti ina *Rejesha*. Majina
  maalum na sauti zilizofichwa zinahifadhiwa katika `sesler/yerel_katman.json`. Sauti iliyobadilishwa jina inaonyesha
  asili yake kwa kijivu (*jina la uundaji · toleo N*); ⋯ → *Nenda kwenye uundaji* inafungua ubunifu wake.
- **Njia za mkato na faili.** Ctrl+Enter (⌘+Enter kwenye Mac) inaanzisha *Buni* au *Soma kwa sauti hii* kwenye kichupo
  kilicho wazi. Upau wa maendeleo unaonyesha *muda uliopita / ~jumla*, kwa makadirio yanayojifunza kutoka kazi za awali
  kwenye kompyuta yako. Faili inayopakuliwa inapewa jina la sauti na wakati (`Voice_Name_2026-11-02_0152.wav`).

**Kunakili sauti (yako mwenyewe au sauti yenye ridhaa).** Katika kichupo cha *Kunakili sauti* cha kiolesura, weka rekodi
yako (wav/mp3/flac/ogg, inashauriwa s 5-30 za usemi safi; chini ya s 3 inakataliwa, zaidi ya s 36 inakatwa), nakala yake
kamili ya maandishi na maandishi ya kusoma. Kitufe kinabaki kimezimwa hadi uweke tiki kwenye "Sauti hii ni yangu au nina
ruhusa ya wazi ya mmiliki". Rekodi inakwenda tu kwenye seva ya ndani (127.0.0.1), inachakatwa ndani ya folda ya muda
pamoja na usimbaji wake wa marejeo, na folda hiyo inafutwa kazi inapoisha, hata ikishindwa; hakuna kinachotumwa kupitia
mtandao. Matokeo bandia pekee ndiyo yanabaki (kiolesura: `sesler/_okumalar/<job>/`, CLI: `--cikti`). Matokeo ni
`klon_synthetic.wav` yenye lebo ya "synthetic"; unaposhiriki, weka alama kwamba yametengenezwa na AI. CLI:
`python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Maswali yanayoulizwa mara kwa mara

**Modeli au injini? Kipi ni kipi?** VoxCPM2 (OpenBMB) ni *modeli*: mtandao wa vigezo bilioni 2 unaogeuza maandishi kuwa
usemi. audio.cpp ni *injini*: programu ya C++/CUDA inayoendesha modeli kwenye GPU yako (`audiocpp_cli.exe`). Marekebisho
yetu yanabadilisha injini, si modeli: yanaifanya VoxCPM2 itoshe kwenye 4 GB na kufanya mbegu ileile itoe sauti ileile kila
mara. Kifurushi cha Python katika hazina hii kinaandaa maandishi tu, kinaita injini na kukusanya faili.

**GPU zipi?** Tazama "GPU zinazoungwa mkono" hapo juu: NVIDIA kuanzia GTX 10xx, VRAM ya 4 GB au zaidi, kiendeshi ≥ 570.
Msimbo asilia upo katika toleo kwa sm_61/75/86/89/120a; kadi nyingine za Pascal au mpya zaidi zinatumia PTX iliyopachikwa
(uanzishaji wa kwanza ni wa polepole zaidi). AMD/Intel: zip ya Vulkan ya majaribio, `kur.ps1 -Vulkan`; mtumiaji wa nje
ameripoti kuiendesha kwenye AMD 6900 XT, lakini majaribio mapana zaidi ya AMD/Intel bado yanahitajika (tazama "AMD /
Intel" hapo juu). CPU pekee (`"backend": "cpu"` ndani ya `ayarlar.json`) inafanya kazi lakini ni ~mara 6 polepole kuliko
GTX 1050 Ti (kipimo cha injini, s 535 dhidi ya s 94 kwa s 48 za usemi); si njia inayoungwa mkono.

**Kasi kiasi gani?** Imepimwa kwenye GTX 1050 Ti 4 GB (i7-7700HQ): toleo moja la ubunifu (rekodi ya ≈ s 25) s 55; usomaji
≈ s 2 za ukokotoaji kwa kila s 1 ya usemi (real-time factor 1.9-2.8) baada ya usimbaji wa marejeo wa mara moja wa ~s 50
kwa kila sauti (unahifadhiwa kwenye diski) na upakiaji wa modeli wa s 10-20 kwa kila kundi; kilele cha VRAM 2.6-2.9 GB.
Kadi mpya zaidi ni za kasi zaidi; namba na mbinu: [docs/4gb.md](docs/4gb.md).

**Je, inaweza kunakili sauti?** Modeli ya msingi ya VoxCPM2 inaweza kuiga sauti kutoka rekodi ya marejeo, na sehemu ya
kunakili inatumia uwezo huo. Itumie tu kwa sauti yako mwenyewe au kwa ruhusa ya wazi ya mtu mwenye sauti hiyo; kiolesura
kinakuomba uthibitishe ruhusa hiyo. Ubunifu wa sauti hauhitaji rekodi: unaanza kutoka maelezo ya maandishi kwa Kiingereza
au Kichina, na "marejeo" yanayotumika kusoma sauti iliyobuniwa ni rekodi ya ubunifu bandia ya modeli yenyewe. Kuiga watu
wengine, ulaghai na udanganyifu ni marufuku. Tazama [ETHICS.md](ETHICS.md). Weka alama kwamba unachochapisha
kimetengenezwa na AI.

**Ninaandikaje maelezo mazuri ya sauti?** Kwa Kiingereza, sentensi 1-3: umri na jinsia, rangi ya sauti (nzito/angavu, ya
joto, ya puani, yenye kwaruza), toni na jukumu (msimulizi mtulivu wa makala, mtangazaji mchangamfu), kasi (polepole,
iliyopimwa), na "clean studio recording, no background noise". Yabaki kuwa maelezo, si hati ya kusoma; bila mabano. Omba
matoleo 3-5 na usikilize: mbegu inabadilisha sauti sana. Kwa maandishi ya uundaji tumia sentensi 1-3 za kawaida katika
lugha ya sauti hiyo, kwa hisia unayoitaka (si zaidi ya ~s 30 za usemi). Wakati wa kusoma, sentensi moja kwa kila mstari;
gawanya sentensi ndefu, andika namba kwa maneno.

## Kuchangia

Hujui uanzie wapi? Masuala haya manne madogo ni hatua nzuri ya kwanza:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Ijaribu kwenye GPU yako na uripoti kadi, kiendeshi na muda
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: jaribu toleo la majaribio la Vulkan
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Ongeza sentensi kwenye seti ya majaribio
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Shiriki sauti uliyoibuni, pamoja na maelezo yake na mbegu

**Jaribu kadi yako ya michoro, andika ripoti:** huhitaji kujua kuandika msimbo, inatosha [fomu ya ripoti ya majaribio ya vifaa](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); bado hakuna ripoti kutoka kadi ya Intel.

Seti ya majaribio ya pamoja: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); mwongozo wa sauti ya chapa:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); jinsi ya kutuma msimbo: [CONTRIBUTING.md](CONTRIBUTING.md).
Matatizo ya usakinishaji: [fomu ya issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); maswali na matokeo: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Kila anayeshiriki anafuata [Kanuni za Maadili](CODE_OF_CONDUCT.md): kuwa mpole, maoni yahusu kazi.

## Wachangiaji

- [@alexturkey](https://github.com/alexturkey): mtunzaji; msimbo, sauti zilizojumuishwa, nyaraka
- [@cayir21](https://github.com/cayir21): usaidizi wa Metal kwa macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): marekebisho ya mwisho wa sentensi (EOS) kwa usomaji wa sentensi nyingi kwenye backend ya CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): usakinishaji wa majaribio wa CUDA kwa Ubuntu/Linux na usaidizi wa Docker, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Jina lako linastahili kuwa hapa pia: matokeo ya majaribio kutoka GPU yako, sentensi kwa seti ya majaribio, sauti
uliyoibuni, ripoti ya hitilafu iliyo wazi au pull request, vyote vinahesabika kama michango. Asante kwa kila anayeijaribu
na kutuandikia.

## Leseni na shukrani

Msimbo na sauti zilizojumuishwa: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Imejengwa juu ya VoxCPM2 (OpenBMB,
Apache-2.0), audio.cpp (ShugoAI LLC, Apache-2.0) na ubadilishaji wa audio.cpp kwenda GGUF. Orodha kamili:
[THIRD_PARTY.md](THIRD_PARTY.md). Haihusiani na OpenBMB, ModelBest wala mradi wa audio.cpp.

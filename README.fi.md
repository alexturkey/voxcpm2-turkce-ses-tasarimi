[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · **Suomi** · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Turkinkielistä äänisuunnittelua VoxCPM2:lla 4 Gt:n näytönohjaimella.** Kuvaile ääni englanniksi, anna mallin luoda
se, valitse mieleisesi muunnelma ja lue sitten mikä tahansa turkinkielinen teksti tuolla äänellä. Mukana on yhden
komennon asennusohjelma, paikattu [audio.cpp](https://github.com/0xShug0/audio.cpp)-moottori, joka mahtuu
GTX 1050 Ti -näytönohjaimeen (4 Gt), pieni paikallinen verkkokäyttöliittymä ja neljätoista valmista synteettistä
ääntä: seitsemän turkkilaista sekä seitsemän kertojaa, joiden äidinkieli on englanti, ranska, saksa, espanja, venäjä,
kiina tai japani.

- Sovellus lukee 30 kielellä; myös käyttöliittymä on saatavilla 30 kielellä.
- 14 valmista ääntä: 7 turkkilaista sekä yksi kutakin kieltä kohden englanniksi, ranskaksi, saksaksi, espanjaksi,
  venäjäksi, kiinaksi ja japaniksi.
- Verkkokäyttöliittymä (v0.2.0): jokaisessa muunnelmakortissa on kaksi ääntä, raaka suunnitteluääni ja ääni, jota
  kuulet jatkossa; lukulista ja äänivalikko; äänten uudelleennimeäminen, piilottaminen ja poistaminen; luonnokset
  lukemillesi teksteille. Katso "Verkkokäyttöliittymä" kohdasta "Käyttö".

[Miten se mahtuu 4 Gt:hen](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Asennusohje tekoälyagenteille](AGENTS.md) · [Vastuullinen käyttö](ETHICS.md)

> Mukana tulevat äänet ovat synteettisiä ja suunniteltu tekstikuvauksen pohjalta. Äänen kloonaus on tarkoitettu vain
> omalle äänellesi tai äänelle, jonka käyttöön omistaja on antanut nimenomaisen luvan; käyttöliittymä pyytää sinua
> vahvistamaan luvan. Toisena esiintyminen, petokset ja harhaanjohtaminen on kielletty. Merkitse tuottamasi sisältö
> tekoälyn tuottamaksi. Katso [ETHICS.md](ETHICS.md).

## 30 kieltä

Teimme yhden Kappadokiaa käsittelevän dokumenttivideon 8 kielellä: turkiksi, englanniksi, ranskaksi, saksaksi,
espanjaksi, venäjäksi, kiinaksi ja japaniksi. Jokaisella kielellä on oma **äidinkielinen kertojansa**, joka on
suunniteltu VoxCPM2:lla englanninkielisen kuvauksen pohjalta. Kaikki tuotettiin täysin paikallisesti 4 Gt:n
GTX 1050 Ti:llä samalla kiinteällä laadulla (16 askelta, cfg 2.0). Seitsemän kertojaa ovat mukana tässä repositoriossa
kehotteineen, suunnittelutekstineen, siemenineen ja referenssitallenteineen.

| Koodi | Kieli | Ääni | Kuuntele | Video |
|---|---|---|---|---|
| `tr` | Turkki | `hazir/belgesel_hanim` (ja 6 muuta) | [näyte](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Englanti | `hazir/anlatici_en` | [näyte](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791986763440439) |
| `fr` | Ranska | `hazir/anlatici_fr` | [näyte](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [video](https://x.com/i/status/2113790681575804962) |
| `de` | Saksa | `hazir/anlatici_de` | [näyte](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [video](https://x.com/i/status/2113791351645262249) |
| `es` | Espanja | `hazir/anlatici_es` | [näyte](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [video](https://x.com/i/status/2113807365611122705) |
| `ru` | Venäjä | `hazir/anlatici_ru` | [näyte](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [video](https://x.com/i/status/2113801574136848884) |
| `zh` | Kiina (mandariini) | `hazir/anlatici_zh` | [näyte](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [video](https://x.com/i/status/2113802229606121794) |
| `ja` | Japani | `hazir/anlatici_ja` | [näyte](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [video](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Miksi lause kerrallaan.** VoxCPM2 ei pysy vakaana yhdessä pitkässä tuotossa (noin yli 30 sekuntia): rytmi kiihtyy ja
ääni voi ajautua. Tässä äänen kantaa kiinteä referenssitallenne ja kiinteä siemen, ja pitkä teksti luetaan yksi lause
riviä kohden, joten sointi ja tyyli pysyvät samoina ensimmäisestä lauseesta viimeiseen. Muille kielille kuin turkille
turkin ääntämissanakirjaa ei käytetä. Kaikki 30 kieltä, joita VoxCPM2 tukee, on testattu ja ne toimivat; käytä
`--dil <code>` niille, joille ei ole valmista ääntä. Kielikohtaiset komennot ja oppimamme asiat:
[docs/cok_dilli.md](docs/cok_dilli.md). Claude Code -taito koko suunnitteluprosessiin:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 esimerkkikehotetta alkuun.** 18 roolia (dokumenttikertoja, uutisankkuri, mainosääni, äänikirja, satuja kertova
isoäiti, podcastin juontaja, opettaja, elokuvatraileri, meditaatio-ohjaaja, urheiluselostaja ja muita, sekä miehiä että
naisia) kullakin 8 kielestä. Kehote on englanniksi, ja siinä mainitaan puhujan kansallisuus ja äidinkielinen aksentti;
mukana tulee myös teksti, joka luetaan äänen luomisen aikana, kyseisellä kielellä ja rooliin sopivana. Valitse yksi,
kuuntele muunnelmat ja pidä mieleisesi: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, tai
valitse verkkokäyttöliittymässä *Esimerkkikuvaus*. Koko luettelo: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Dubbaa videosi omalla äänelläsi.** [DubWorld](https://github.com/alexturkey/dubworld) on paikallinen
videodubbausohjelmamme; se asentaa tämän repositorion VoxCPM2-äänimoottorikseen. Täällä suunnittelemaasi ääntä käytetään
siellä asetuksella `ses.voxcpm2_ses = "<name>/<variant>"`.

## Pika-aloitus (Windows, 3 vaihetta)

1. **Lataa** koodi: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Asennusohjelma hakee näytönohjaimellesi sopivan valmiin moottoripaketin vaiheessa 3:
   NVIDIA → [CUDA-paketti](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan-paketti, kokeellinen](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (oletko jo ladannut paketin? Lisää alla olevaan komentoon `-HazirZip <path to the zip>`).
2. **Pura** zip-tiedosto, avaa kansio `voxcpm2-turkce-ses-tasarimi-main`, kirjoita `powershell` Resurssienhallinnan
   osoiteriville ja paina Enter.
3. **Suorita** asennusohjelma (vaatii 64-bittisen Python 3.10-3.13:n ja CUDAa varten NVIDIA-ajurin ≥ 570) ja
   kaksoisnapsauta sitten **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: lisää loppuun `-Vulkan`. Käyttöliittymä avautuu osoitteessa http://127.0.0.1:8765/.

Moottorin zip-tiedosto ei ole itsenäinen sovellus (sen exe tarvitsee mallin ja DLL-tiedostot, jotka asennusohjelma
asettaa paikoilleen). Lisätiedot, näytönohjainluettelo ja yleiset ongelmat: "Pika-asennus" alempana.

## Ubuntu / Linux (NVIDIA CUDA, kokeellinen)

Käännä paikattu moottori komennolla `bash scripts/kur-linux.sh`, tai käytä `Dockerfile.linux`-tiedostoa kääntämiseen ja
ajamiseen Ubuntu 24.04 / CUDA 12.8.1 -ympäristössä. Vaatii NVIDIA-näytönohjaimen ja yhteensopivan ajurin; natiivi
asennusohjelma tarvitsee lisäksi CUDA Toolkitin ja Python 3.10-3.13:n. Käyttöliittymä kuuntelee vain loopback-osoitetta
myös etäpalvelimilla (SSH-uudelleenohjaus). Esivaatimukset, komennot, arkkitehtuurin valinta ja validoinnin laajuus:
[docs/linux.md](docs/linux.md).

## Pika-aloitus (macOS, Apple Silicon)

Vaatii Xcode Command Line Toolsin (`xcode-select --install`) ja [Homebrew'n](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
Asennusohjelma lataa mallin, kääntää paikatun moottorin Metal-tuella (~1 min) ja asentaa kaiken hakemistoon `~/vox`.
Kaksoisnapsauta sen jälkeen **`baslat.command`**. MacBook Air M4 16 Gt: ~2 s laskentaa 1 s puhetta kohden, sama siemen
tuottaa tavulleen identtisen äänen, enintään ~5,3 Gt RAM-muistia eikä lämpörajoitusta 12 minuutin yhtäjaksoisen
lukemisen aikana. Lisätiedot ja mittaukset: [docs/mac.md](docs/mac.md).

**Natiivi Mac-sovellus (ilman Pythonia, Homebrew'ta tai Terminaalia):** [macos/README.md](macos/README.md). Siinä on
sama paikattu moottori, ja se lataa mallin ensimmäisellä käynnistyskerralla; toistaiseksi se käännetään lähdekoodista
Xcodella.

## Mac-käyttäjille (Apple Silicon)

Apple Silicon -Maceille on myös yhteisön tekemä itsenäinen sovitus, joka ajaa VoxCPM2:ta Applen MLX-kehyksellä:
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Sitä kehittää ja ylläpitää Emre Koç ([@emre-koc](https://github.com/emre-koc)) omassa repositoriossaan, ei täällä;
asennusohjeet ja tukikysymykset kuuluvat sinne. Kiitos, Emre, että toit projektin Macille!

## Näin se toimii

1. **Äänisuunnittelu.** Englanninkielinen *äänen kuvaus* + *teksti, joka luetaan äänen luomisen aikana* (äänen
   kielellä) + muunnelmien määrä. Jokainen muunnelma saa oman siemenensä; moottori vastaanottaa `(description)text`
   ja palauttaa yhden suunnittelutallenteen siementä kohden. Teksti on lyhyt näyte, jonka avulla ääneen tutustutaan:
   1-3 lausetta, enintään ~30 s (käyttöliittymä näyttää arvion eikä käynnisty yli 33 s:n kohdalla); pitkä teksti
   kuuluu vaiheeseen 2.
2. **Referenssiin perustuva lukeminen.** Suunnittelutallenne annetaan moottorin **molempiin** syötteisiin (`audio` ja
   `voice_ref`) yhdessä sen litteroinnin (`reference_text`) ja uuden luettavan tekstin kanssa, samalla siemenellä.
   Äänen kantaa tallenne, ei kuvaus, joten ääni ei ajaudu tekstistä toiseen. Teksti luetaan lause kerrallaan.
3. Laatu on kiinteä: 16 diffuusioaskelta, CFG 2.0. Siemen ei ole laatuasetus.
4. **Sanojen ajoitus, sama ääni joka kerta.** Luennan aikana moottori itse kertoo, missä kukin sana alkaa ja päättyy (paikka 0002, ei lisämallia). Ajat tallennetaan tiedostoon `kelimeler.json`, ja rivit rajataan niin, että rivien väli on sama kuin taukoasetus. Tarkkuus CTC-pakkokohdistukseen (forced alignment, CTC = 100 %) verrattuna: 89,66 % (turkki, 12 ääntä; asetus `kelime_zamani`, oletuksena päällä). Paikan 0003 ansiosta sama siemen tuottaa joka ajolla tavulleen saman äänen.

Raaka suunnittelutallenne on äänen kertaluonteinen näyte; mikään myöhempi lukeminen ei kuulosta täsmälleen samalta.
Jokaisessa myöhemmässä lukemisessa kuulet vaiheen 2: suunnittelutallenteen referenssinä sekä muunnelman oman siemenen.
Siksi verkkokäyttöliittymä tekee vaiheen 2 heti suunnittelun jälkeen ja näyttää molemmat muunnelmakortissa.

Moottori on audio.cpp v0.7.2 omalla paikallamme (`patches/`), malli on VoxCPM2 Q8_0 GGUF. VRAM-huippu ≈ 2,8 Gt; noin
2 s laskentaa 1 s puhetta kohden GTX 1050 Ti:llä. Lisätiedot ja mittaukset: [docs/4gb.md](docs/4gb.md).

## Valmiit äänet (`hazir_sesler/`)

Kaikki neljätoista on suunniteltu niiden `ses.json`-tiedostoon tallennettujen kehotteiden pohjalta; yhtäkään ei ole
kloonattu tallenteesta (kloonaus tapahtuu erillisellä, suostumusta vaativalla *Äänen kloonaus* -välilehdellä).

| Ääni | Lyhyt kuvaus | Kuuntele |
|---|---|---|
| `belgesel_hanim` | Kypsä viisikymppinen nainen, syvä ja lämmin altto; rauhallinen dokumenttikertoja | [näyte](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referenssi](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Syvä, voimakas ja salaperäinen miespuolinen kertoja | [näyte](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referenssi](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Kokenut, noin seitsemänkymppinen uutisankkuri, rauhallinen ja arvovaltainen | [näyte](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referenssi](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Karismaattinen kolmekymppinen iltauutisten ankkuri, samettinen ja ilmeikäs | [näyte](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referenssi](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Sadun noita: matala, hieman nasaali, viekkaan makea | [näyte](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referenssi](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Poikkeuksellisen syvä, täyteläinen ja käskevä miespuolinen kertoja | [näyte](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referenssi](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Vanha viisas mies, syvä ja jylisevä, hieman salaperäinen | [näyte](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referenssi](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä englanti (General American); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä ranska (Pariisi); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä saksa (yleissaksa); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä espanja (kastilia (Madrid)); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä venäjä (Moskova); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä kiina (mandariini) (Pekingin putonghua); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Viisikymppinen miespuolinen dokumenttikertoja, äidinkielenä japani (Tokion yleiskieli); syvä, rauhallinen, lämmin | [näyte](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referenssi](hazir_sesler/anlatici_ja/referans.flac) |

Kussakin kansiossa: `referans.flac` (häviötön suunnittelutallenne), `ses.json` (kehote, litterointi,
suunnittelusiemen, lukusiemen, kuvaus; kertojilla `dil` = kieli), `ornek_okuma.mp3` (+ sen teksti). Käytä niitä
suoraan: `--ses hazir/<name>`. Kertojien referenssitallenteet ovat lyhyitä (5,6-10 s); niiden näytteet ovat
Kappadokia-käsikirjoituksen kolme ensimmäistä lausetta, leikattuina valmiista tuotantoluennasta.

## Pika-asennus ilman kääntäjää (Windows 10/11, NVIDIA-näytönohjain ≥ 4 Gt)

Esivaatimukset: NVIDIA-ajuri ≥ 570 ja 64-bittinen Python 3.10-3.13 (`winget install Python.Python.3.12`). Ei muuta:
ei Visual Studiota, ei CUDA-asennusohjelmaa. Etkö ole varma, mikä näytönohjain sinulla on? Suorita PowerShellissä
`nvidia-smi`: se näyttää näytönohjaimen nimen, ajurin version ja muistin. Eikö sinulla ole NVIDIA-korttia? Katso
"AMD / Intel" alempana.

[Gitin](https://git-scm.com/download/win) kanssa:

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Ilman Gitiä: napsauta tällä sivulla **Code → Download ZIP**, pura tiedosto, avaa purettu kansio
`voxcpm2-turkce-ses-tasarimi-main`, kirjoita `powershell` Resurssienhallinnan osoiteriville, paina Enter ja suorita
sitten yllä olevista riveistä viimeinen. Gitiä tarvitaan vain lähdekoodista kääntämiseen.

`-ExecutionPolicy Bypass` koskee vain tätä yhtä prosessia eikä muuta järjestelmän asetuksia; lue `scripts\kur.ps1`
ennen sen suorittamista, kuten minkä tahansa asennusskriptin kohdalla. Yksi komento, ~10 min, ~3,7 Gt latausta, kaikki
sha256-tarkistettuna: malli (2,95 Gt), CUDA 12.8 -ajonaikaiset DLL-tiedostot siirrettävinä zip-paketteina (ei
järjestelmäasennusta, PATH-muuttujaan ei kosketa), **valmiiksi käännetty moottori** Releases-sivulta, `.venv` kahdella
Python-paketilla, `ayarlar.json` sekä lopullinen näytönohjaintarkistus (`KONTROL_OK`). Suorita komento uudelleen, jos
jokin epäonnistuu; jo tarkistetut tiedostot ohitetaan. Käynnistä sitten verkkokäyttöliittymä: kaksoisnapsauta
**`baslat.bat`** repositorion kansiossa. Se käynnistää käyttöliittymän ja avaa **http://127.0.0.1:8765/** selaimeesi,
kun se on valmis; sulje musta ikkuna (tai paina siinä Ctrl+C) pysäyttääksesi sen. Sama PowerShellistä:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
ja avaa sitten itse **http://127.0.0.1:8765/** (näin käynnistettynä käyttöliittymä ei avaa selainta; se kuuntelee vain
localhost-osoitetta).

> **Julkaisun zip-tiedoston `audiocpp_cli.exe` ei ole tarkoitettu kaksoisnapsautettavaksi.** Se on komentorivimoottori,
> joka tarvitsee viereensä CUDA-DLL-tiedostot ja mallin; `kur.ps1` asettaa kaiken paikoilleen ja Python-paketti ohjaa
> sitä. Kaksoisnapsautus näyttää vain virheen "cudart64_12.dll not found".

**Tuetut näytönohjaimet (julkaisu v0.1.1):** natiivikoodi GTX 10xx:lle (sm_61), RTX 20xx:lle (sm_75), RTX 30xx:lle
(sm_86), RTX 40xx:lle (sm_89) ja RTX 50xx:lle (sm_120a); muut Pascalista alkaen julkaistut CUDA-näytönohjaimet ajavat
sulautettua PTX-koodia ajurin kautta (hitaampi ensimmäinen käynnistys). CUDA 12.8 ei tue Maxwellia (GTX 9xx) eikä sitä
vanhempia. Testattu itse GTX 1050 Ti 4 Gt:llä (myös Docker Desktopin/WSL2:n kautta Windowsissa, vain CLI); mitannut
@mslmyilmaz5 (#15): RTX 3060 Ti 8 Gt, Ubuntu 24.04 Docker, CUDA 12.8.1 (lisätiedot: [docs/linux.md](docs/linux.md)).
Raportit muista näytönohjaimista ovat tervetulleita
[Discussionsiin](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (kokeellinen):** erillinen Vulkan-moottorin zip (`...-win64-vulkan.zip`, ei CUDAa) asennetaan komennolla
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Se on varmennettu vain omalla NVIDIA-kortillamme Vulkan-taustajärjestelmän kautta
(siellä se toimi CUDAa hitaammin mutta tuotti saman äänen samalla siemenellä; mittaus tehtiin levyn ollessa varattuna
toiseen työhön, joten puhdas nopeusvertailu on vielä tekemättä), emmekä ole itse testanneet sitä AMD- tai
Intel-laitteistolla: jos kokeilet sitä, julkaise tulos Discussionsissa. Jos Vulkan-laitteita on useampi kuin yksi
(integroitu + erillinen), asennusohjelma kirjoittaa erillisen näytönohjaimen indeksin `cihaz`-arvoksi tiedostoon
`ayarlar.json`.

**Huom:** Vulkan-tuki on tällä hetkellä kokeellinen. Se on käännetty ja testattu onnistuneesti GTX 1050 Ti:llä. Lisäksi
ulkopuolinen käyttäjä (mitra_tr) on ilmoittanut ajaneensa sitä AMD 6900 XT:llä. AMD/Intel-korteilla tarvitaan vielä
laajempaa testausta.

**Yhteisön testi (AMD):** @mitraTR ajoi v0.1.1:n Vulkanilla AMD Radeon RX 6900 XT -näytönohjaimella Windows 11:ssä: asennus, äänen suunnittelu, lukeminen, verkkokäyttöliittymä ja testit toimivat; lukeminen vei noin 0,8-0,9 s laskenta-aikaa sekuntia puhetta kohden ([raportti #6:ssa](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Asenna lyhyeen kansioon, jonka polussa on vain ASCII-merkkejä (esim. `C:\vox`): Windowsissa moottori ei pysty avaamaan polkuja, joissa on ä-, ö- tai muita ei-ASCII-merkkejä. Kaikki raportit tähän mennessä: [testattu laitteisto](docs/donanim_testleri.md).

**Huomioita Vulkanista:** sanojen ajoitukset ovat toistaiseksi saatavilla vain NVIDIAlla (CUDA) ja Macilla; AMD/Intel-korteilla niitä ei synny ennen kuin Vulkan-moottori päivitetään (lukeminen toimii silti). Ensimmäinen käynnistys Vulkanilla voi kestää muutaman minuutin, koska näytönohjaimen varjostimet käännetään; myöhemmät luvut ovat nopeampia.

### Vaihtoehto: käännä moottori lähdekoodista

Vaatii Visual Studio 2022 Build Toolsin ja työkuorman "Desktop development with C++" (sis. C++ CMake tools), ~7 Gt.
Sitten:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Tämä lataa myös nvcc:n, hakee audio.cpp v0.7.2:n lähdekoodin, soveltaa paikan `patches/0001-voxcpm2-4gb-ve-hiz.patch`
ja kääntää näytönohjaimellesi (`-Mimari native`, oletus; tai esim. `-Mimari 61`), ~15-25 min. Pidä juurihakemiston
polku lyhyenä (`C:\vox`): nvcc epäonnistuu pitkillä poluilla. Vaihe vaiheelta tarkistuksineen: [AGENTS.md](AGENTS.md).

### Yleiset asennusongelmat

| Näet | Mitä se tarkoittaa, mitä tehdä |
|---|---|
| `cudart64_12.dll not found` exe-tiedoston kaksoisnapsautuksen jälkeen | Moottoria ei ole tarkoitettu käynnistettäväksi käsin. Suorita yllä oleva `kur.ps1`-komento ja käynnistä sitten verkkokäyttöliittymä. |
| `64-bit Python 3.10+ bulunamadı` (Pythonia ei löytynyt) | Asenna Python (`winget install Python.Python.3.12`), sulje PowerShell, avaa uusi ikkuna ja suorita sama komento uudelleen. |
| `motor ekran kartını görmedi` (moottori ei nähnyt näytönohjainta) | Päivitä NVIDIA-ajuri versioon 570 tai uudempaan; tarkista, että `nvidia-smi` toimii. |
| `indirme başarısız` / `sha256 tutmadı` (lataus epäonnistui / tarkistussumma ei täsmää) | Yleensä keskeytynyt lataus. Suorita sama komento uudelleen; jo tarkistetut tiedostot ohitetaan. |
| Kääntäminen lähdekoodista: `nvcc` epäonnistuu | Pidä asennuksen juurihakemisto lyhyenä (`-Kok C:\vox`). |
| Sivu ei avaudu | Käynnistä käyttöliittymä tiedostolla `baslat.bat` tai avaa itse http://127.0.0.1:8765/. Onko portti varattu? Muuta `"port"`-arvoa tiedostossa `ayarlar.json`. |

Ongelmia? [Discussions (kysymykset ja vastaukset)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) tai
[asennusongelman ilmoitus](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml),
jossa mainitset näytönohjaimesi, Windows-versiosi, komennon ja sen viimeiset rivit.

## Käyttö

Komentorivi:
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
Tekstisäännöt: kirjoita luvut kirjaimin, ei lainausmerkkejä (työkalu hylkää numerot ja lainausmerkit), yksi lause
riviä kohden, enintään 2000 merkkiä riville. Tauko rivin jälkeen: `|| bagli` 0,25 s, `|| normal` 0,5 s,
`|| paragraf` 1 s, `|| agir` 1,5 s tai oma pituus `|| 0,8` (0-5 s; merkinnän numerot ovat sallittuja).
`ayarlar/okunus_sozlugu.tsv` korjaa vieraiden sanojen ääntämisen turkinkielisessä tekstissä. Kieli tunnistetaan
tekstistä (turkin kirjaimet, kirjoitusjärjestelmä, yleiset sanat; epävarmoissa tapauksissa äänikortin `dil`;
`--dil <code>` on valinnainen). Muussa kuin turkinkielisessä tekstissä heittomerkit ovat sallittuja, turkin sanakirja
ohitetaan ja numerot hylätään edelleen. Jos lukeminen tulostaa `speed gate: satır [...]`, kuuntele kyseiset rivit.

### Verkkokäyttöliittymä

Vain paikallisesti (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → avaa itse http://127.0.0.1:8765/
(muu portti: `--port 8800`), tai kaksoisnapsauta `baslat.bat`. Pysäytä palvelin painamalla Ctrl+C. Kolme välilehteä:
*Suunnittele ääni*, *Lue tällä äänellä*, *Äänen kloonaus*. Tavallinen kulku: *Suunnittele* → kuuntele muunnelmat →
*Lisää lukulistaani* → *Lue tällä äänellä* → lataa. Tai valitse valmis ääni äänivalikosta ja lue.

- **Versio otsakkeessa.** Pieni, himmeä `v0.2.0 · <short commit>` (mukana `+`, kun seurattuihin tiedostoihin on tehty
  muutoksia, joita ei ole kommitoitu; ilman gitiä vain versio), jotta kuvakaappauksista ja videoista näkee, mitä
  versiota käytettiin.
- **Kaksi ääntä jokaisessa muunnelmakortissa.** Ylimpänä harmaalla *Raaka suunnitteluääni*: se tuotetaan kerran eikä
  koskaan tule samanlaisena uudelleen. Sen alla oranssissa kehyksessä *↻ Tätä ääntä kuulet jatkossa*: suunnittelutallenne
  luettuna takaisin referenssinä muunnelman omalla siemenellä (näkyy kortissa). Tältä ääni kuulostaa jokaisessa
  myöhemmässä lukemisessa. Sen alla ovat *Lue tällä äänellä* ja *Lisää lukulistaani*. Yksi *Suunnittele*-painallus
  tekee molemmat: se suunnittelee kaikki muunnelmat ja lukee sitten tekstisi kullakin pysyvällä äänellä; yksi
  edistymispalkki laskee molemmat vaiheet. Muunnelman kansioon tulee `dinleme.wav`. Jos tuo lukeminen keskeytyy
  ennenaikaisesti, suunnittelu säilyy ja kortissa näkyy huomautus.
- **Ikkuna "Teksti, jonka haluat kuulla".** *Suunnittele ääni* -välilehden kenttä *↻ Teksti, jonka haluat kuulla*
  sisältää sen, mitä kukin pysyvä ääni lukee (tyhjäksi jätettynä luetaan esimerkkilause). Kentän napsauttaminen avaa
  lukuvihon ikkunaan: rivinumerot, rivivalikko, taukonauhat. *OK* kirjoittaa tekstin ja sen tauot takaisin kenttään;
  *Peruuta* tai Esc ei muuta mitään. Lukuvälilehdellä on oma tekstinsä.
- **Lukuvihko.** Yksi lause riviä kohden. Napsauta rivinumeroa avataksesi rivivalikon (siirrä ylös tai alas, siirrä
  tiettyyn kohtaan, monista, poista; Alt+↑/↓, Alt+Shift+↓ tai vedä numerosta; Ctrl+Z kumoaa tekstin ja tauot yhdessä).
  Napsauta kahden rivin välistä ohutta nauhaa valitaksesi tauon (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, tai
  oma 0-5 s hammasrattaasta); paina Enteriä kahdesti kappaleenvaihtoa varten (1 s), ja tyhjistä riveistä tulee
  taukonauhoja. Kun tulosta toistetaan, luettava rivi hehkuu ja vierittyy näkyviin; rivivalikon *▶ Kuuntele tästä
  eteenpäin* toistaa kyseiseltä riviltä. Teksti ja sen tauot säilyvät sivun uudelleenlatauksen yli (selaimen
  tallennustila).
- **Luonnokset.** *📄 Luonnokset* -painike on molemmissa vihoissa (lukuvälilehdellä ja ikkunassa). Tallenna nykyinen
  teksti taukoineen luonnokseksi, lataa luonnos yhdellä napsautuksella (Ctrl+Z kumoaa) ja käytä ⋯-valikkoa
  korvaamiseen, uudelleennimeämiseen tai poistamiseen. Luonnokset tallennetaan tiedostoon `sesler/taslaklar.json`,
  ei koskaan repositorioon.
- **Lukulista ja äänivalikko.** Muunnelmakortin *Lisää lukulistaani* avaa nimikentän: anna muunnelmalle oma nimi, ja ✓
  lisää sen. *Luonnin nimi* säilyy kaikissa saman ajon muunnelmissa. *Lue tällä äänellä* -välilehdellä äänipainike
  (lippu + nimi) avaa äänivalikon: ylimpänä *Lukulistani*, sitten valmiit äänet lippuineen (käyttöliittymän kieli
  ensin). Jokaisella rivillä on ▶ kuuntele (pysyvä ääni, jos sellainen on), sydän (lisää tai poista) ja ⋯; ↑/↓ ja
  Enter valitsevat, Esc sulkee, ja viimeisin ääni muistetaan. Lista on tiedostossa `sesler/okuma_listesi.json`
  repositorion ulkopuolella ja säilyy uudelleenkäynnistysten yli.
- **Äänten hallinta.** ⋯-valikossa (äänivalikon rivi tai muunnelmakortti) on *Lue tällä äänellä*, listaan lisääminen
  tai siitä poistaminen, *Nimeä uudelleen* (tyhjä nimi palauttaa alkuperäisen; *Palauta alkuperäinen nimi*), *Poista*
  suunnitelluille äänille ja *Piilota* valmiille äänille; molemmat kysyvät ensin. Poistettu ääni siirtyy kansioon
  `sesler/_cop/`; piilottaminen ei koskaan koske repositorion tiedostoihin. Äänivalikon alareunan kohdassa *Piilotetut
  ja poistetut äänet (N)* on *Palauta*. Omat nimet ja piilotetut äänet tallennetaan tiedostoon
  `sesler/yerel_katman.json`. Uudelleennimetty ääni näyttää alkuperänsä harmaalla (*luonnin nimi · muunnelma N*);
  ⋯ → *Siirry luontiin* avaa sen suunnittelun.
- **Pikanäppäimet ja tiedostot.** Ctrl+Enter (Macissa ⌘+Enter) käynnistää avoimella välilehdellä *Suunnittele*- tai
  *Lue tällä äänellä* -toiminnon. Edistymispalkki näyttää *kulunut / ~yhteensä* ja arvion, joka on opittu koneesi
  aiemmista töistä. Ladattu tiedosto nimetään äänen ja ajankohdan mukaan (`Voice_Name_2026-11-02_0152.wav`).

**Äänen kloonaus (oma ääni tai luvallinen ääni).** Anna käyttöliittymän *Äänen kloonaus* -välilehdellä tallenteesi
(wav/mp3/flac/ogg, suositus 5-30 s puhdasta puhetta; alle 3 s hylätään, yli 36 s lyhennetään), sen tarkka litterointi
ja luettava teksti. Painike pysyy pois käytöstä, kunnes rastitat kohdan "Tämä ääni on minun tai minulla on omistajan
nimenomainen lupa". Tallenne menee vain paikalliselle palvelimelle (127.0.0.1), se käsitellään väliaikaisessa
kansiossa yhdessä referenssikoodauksensa kanssa, ja kansio poistetaan työn päättyessä, myös epäonnistuessa; mitään ei
lähetetä verkon yli. Vain synteettinen tulos säilytetään (käyttöliittymä: `sesler/_okumalar/<job>/`, CLI: `--cikti`).
Tulos on `klon_synthetic.wav` "synthetic"-merkinnällä; merkitse se jakaessasi tekoälyn tuottamaksi. CLI:
`python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Usein kysyttyä

**Malli vai moottori? Mikä on mitä?** VoxCPM2 (OpenBMB) on *malli*: 2 miljardin parametrin neuroverkko, joka muuttaa
tekstin puheeksi. audio.cpp on *moottori*: C++/CUDA-ohjelma, joka ajaa mallia näytönohjaimellasi (`audiocpp_cli.exe`).
Paikkamme muuttaa moottoria, ei mallia: se saa VoxCPM2:n mahtumaan 4 Gt:hen ja saa saman siemenen tuottamaan joka
kerta saman äänen. Tämän repositorion Python-paketti vain valmistelee tekstin, kutsuu moottoria ja kerää tiedostot.

**Mitkä näytönohjaimet?** Katso "Tuetut näytönohjaimet" yllä: NVIDIA GTX 10xx:stä ylöspäin, vähintään 4 Gt VRAM-muistia,
ajuri ≥ 570. Julkaisussa on natiivikoodi kohteille sm_61/75/86/89/120a; muut Pascal-sukupolven tai uudemmat kortit
käyttävät sulautettua PTX-koodia (hitaampi ensimmäinen käynnistys). AMD/Intel: kokeellinen Vulkan-zip,
`kur.ps1 -Vulkan`; ulkopuolinen käyttäjä on ilmoittanut ajaneensa sitä AMD 6900 XT:llä, mutta laajempaa
AMD/Intel-testausta tarvitaan vielä (katso "AMD / Intel" yllä). Pelkkä suoritin (`"backend": "cpu"` tiedostossa
`ayarlar.json`) toimii, mutta on ~6× hitaampi kuin GTX 1050 Ti (moottorimittaus, 535 s vs. 94 s 48 s:n puheelle); se
ei ole tuettu tapa.

**Kuinka nopea?** Mitattu GTX 1050 Ti 4 Gt:llä (i7-7700HQ): yksi suunnittelumuunnelma (≈ 25 s:n tallenne) 55 s;
lukeminen ≈ 2 s laskentaa 1 s puhetta kohden (reaaliaikakerroin 1,9-2,8) kertaluonteisen, noin 50 s kestävän
äänikohtaisen referenssikoodauksen (välimuistissa levyllä) ja erää kohden 10-20 s kestävän mallin latauksen jälkeen;
VRAM-huippu 2,6-2,9 Gt. Uudemmat kortit ovat nopeampia; luvut ja menetelmä: [docs/4gb.md](docs/4gb.md).

**Voiko sillä kloonata äänen?** Taustalla oleva VoxCPM2-malli osaa jäljitellä ääntä referenssitallenteen perusteella,
ja kloonausosio käyttää tätä. Käytä sitä vain omalla äänelläsi tai äänen omistajan nimenomaisella luvalla;
käyttöliittymä pyytää sinua vahvistamaan luvan. Äänisuunnittelu ei vaadi tallennetta: se lähtee englannin- tai
kiinankielisestä tekstikuvauksesta, ja suunnitellun äänen lukemiseen käytetty "referenssi" on mallin oma synteettinen
suunnittelutallenne. Toisena esiintyminen, petokset ja harhaanjohtaminen on kielletty. Katso [ETHICS.md](ETHICS.md).
Merkitse julkaisemasi sisältö tekoälyn tuottamaksi.

**Miten kirjoitan hyvän äänen kuvauksen?** Englanniksi, 1-3 lausetta: ikä ja sukupuoli, sointi (syvä/kirkas, lämmin,
nasaali, karhea), sävy ja rooli (rauhallinen dokumenttikertoja, energinen juontaja), tempo (hidas, harkittu) sekä
"clean studio recording, no background noise". Pidä se kuvauksena, ei käsikirjoituksena; ei sulkeita. Pyydä 3-5
muunnelmaa ja kuuntele: siemen muuttaa ääntä paljon. Käytä luontitekstinä 1-3 luontevaa lausetta äänen kielellä ja
haluamassasi tunnelmassa (enintään ~30 s puhetta). Lukiessa yksi lause riviä kohden; jaa pitkät lauseet ja kirjoita
luvut kirjaimin.

## Osallistuminen

Etkö tiedä, mistä aloittaa? Nämä neljä pientä issueta ovat hyvä ensimmäinen askel:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Kokeile omalla näytönohjaimellasi ja raportoi kortti, ajuri ja ajat
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: kokeile kokeellista Vulkan-käännöstä
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Lisää lause testijoukkoon
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Jaa suunnittelemasi ääni kuvauksineen ja siemenineen

**Testaa näytönohjaimesi, kirjoita raportti:** koodaustaitoa ei tarvita, pelkkä [laitteistotestiraportin lomake](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml) riittää; Intel-näytönohjaimesta ei ole vielä yhtään raporttia.

Yhteinen testijoukko: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); brändiäänen opas:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); näin lähetät koodia: [CONTRIBUTING.md](CONTRIBUTING.md).
Asennusongelmat: [issue-lomake](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); kysymykset ja tulokset: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Kaikki osallistujat noudattavat [toimintaohjeita](CODE_OF_CONDUCT.md): ole ystävällinen ja pidä palaute työssä.

## Osallistujat

- [@alexturkey](https://github.com/alexturkey): ylläpitäjä; koodi, valmiit äänet, dokumentaatio
- [@cayir21](https://github.com/cayir21): macOS:n (Apple Silicon) Metal-tuki, [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): lauseen lopun (EOS) korjaus monilauseiseen lukemiseen CPU-taustajärjestelmällä, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): kokeellinen CUDA-asennus Ubuntulle/Linuxille ja Docker-tuki, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Sinunkin nimesi kuuluu tänne: testitulos omalta näytönohjaimeltasi, lause testijoukkoon, suunnittelemasi ääni, selkeä
virheraportti tai pull request ovat kaikki osallistumista. Kiitos kaikille, jotka kokeilevat ja antavat palautetta.

## Lisenssi ja kiitokset

Koodi ja valmiit äänet: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Perustuu VoxCPM2:een (OpenBMB, Apache-2.0),
audio.cpp:hen (ShugoAI LLC, Apache-2.0) ja audio.cpp:n GGUF-muunnokseen. Täydellinen luettelo:
[THIRD_PARTY.md](THIRD_PARTY.md). Ei sidoksissa OpenBMB:hen, ModelBestiin eikä audio.cpp-projektiin.

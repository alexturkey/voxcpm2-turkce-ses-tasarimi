[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · **हिन्दी** · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**4 GB GPU पर VoxCPM2 से तुर्की आवाज़ डिज़ाइन।** अंग्रेज़ी में किसी आवाज़ का विवरण लिखें, मॉडल को उसे बनाने दें, जो वेरिएंट
पसंद आए उसे चुनें, फिर उसी आवाज़ में कोई भी तुर्की टेक्स्ट पढ़वाएँ। इसमें एक कमांड वाला इंस्टॉलर, GTX 1050 Ti (4 GB) में
समा जाने वाला पैच किया हुआ [audio.cpp](https://github.com/0xShug0/audio.cpp) इंजन, एक छोटा लोकल वेब UI और चौदह तैयार
सिंथेटिक आवाज़ें शामिल हैं: सात तुर्की और सात नेटिव नैरेटर, जो अंग्रेज़ी, फ़्रेंच, जर्मन, स्पैनिश, रूसी, चीनी और जापानी में हैं।

- ऐप 30 भाषाओं में पढ़ता है; इंटरफ़ेस भी 30 भाषाओं में है।
- 14 तैयार आवाज़ें: 7 तुर्की, और अंग्रेज़ी, फ़्रेंच, जर्मन, स्पैनिश, रूसी, चीनी व जापानी में एक-एक।
- वेब UI (v0.2.0): हर वेरिएंट कार्ड पर दो आवाज़ें हैं, कच्ची डिज़ाइन आवाज़ और वह आवाज़ जो आप आगे हमेशा सुनेंगे; आवाज़ मेनू
  वाली पठन सूची; आवाज़ों का नाम बदलना, उन्हें छिपाना या हटाना; पढ़े जाने वाले टेक्स्ट के लिए ड्राफ़्ट। "इस्तेमाल" में "वेब UI" देखें।

[4 GB में यह कैसे समाता है](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [AI एजेंटों के लिए इंस्टॉल गाइड](AGENTS.md) · [ज़िम्मेदार इस्तेमाल](ETHICS.md)

> साथ दी गई आवाज़ें सिंथेटिक हैं, जिन्हें टेक्स्ट विवरण से डिज़ाइन किया गया है। वॉइस क्लोनिंग वाला हिस्सा सिर्फ़ आपकी अपनी
> आवाज़ के लिए है, या ऐसी आवाज़ के लिए जिसके मालिक ने साफ़ अनुमति दी हो; UI आपसे इस अनुमति की पुष्टि करवाता है। किसी और
> की नक़ल करना, धोखाधड़ी और गुमराह करना मना है। आप जो भी बनाएँ, उस पर AI-जनरेटेड का लेबल लगाएँ। [ETHICS.md](ETHICS.md) देखें।

## 30 भाषाएँ

हमने कप्पादोकिया पर एक डॉक्यूमेंट्री वीडियो 8 भाषाओं में बनाया: तुर्की, अंग्रेज़ी, फ़्रेंच, जर्मन, स्पैनिश, रूसी, चीनी और
जापानी। हर भाषा का अपना **नेटिव नैरेटर** है, जिसे VoxCPM2 से एक अंग्रेज़ी विवरण के आधार पर डिज़ाइन किया गया। पूरा काम 4 GB
वाले GTX 1050 Ti पर पूरी तरह लोकल तौर पर, एक ही तय क्वालिटी (16 स्टेप, cfg 2.0) पर जनरेट हुआ। सातों नैरेटर यहाँ शामिल हैं,
साथ में उनका विवरण (prompt), डिज़ाइन टेक्स्ट, सीड और रेफ़रेंस रिकॉर्डिंग भी।

| कोड | भाषा | आवाज़ | सुनें | वीडियो |
|---|---|---|---|---|
| `tr` | तुर्की | `hazir/belgesel_hanim` (और 6 अन्य) | [नमूना](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | अंग्रेज़ी | `hazir/anlatici_en` | [नमूना](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113791986763440439) |
| `fr` | फ़्रेंच | `hazir/anlatici_fr` | [नमूना](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113790681575804962) |
| `de` | जर्मन | `hazir/anlatici_de` | [नमूना](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113791351645262249) |
| `es` | स्पैनिश | `hazir/anlatici_es` | [नमूना](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113807365611122705) |
| `ru` | रूसी | `hazir/anlatici_ru` | [नमूना](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113801574136848884) |
| `zh` | चीनी (मंदारिन) | `hazir/anlatici_zh` | [नमूना](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113802229606121794) |
| `ja` | जापानी | `hazir/anlatici_ja` | [नमूना](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [वीडियो](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**वाक्य-दर-वाक्य क्यों।** एक लंबे जनरेशन (लगभग 30 सेकंड से ऊपर) में VoxCPM2 स्थिर नहीं रहता: रफ़्तार बढ़ जाती है और आवाज़
भटक सकती है। यहाँ आवाज़ को एक तय रेफ़रेंस रिकॉर्डिंग और सीड संभालते हैं, और लंबा टेक्स्ट हर लाइन में एक वाक्य के हिसाब से पढ़ा
जाता है, ताकि पहले वाक्य से आख़िरी वाक्य तक आवाज़ का रंग (टिम्बर) और अंदाज़ एक जैसा रहे। तुर्की के अलावा दूसरी भाषाओं पर
तुर्की उच्चारण शब्दकोश लागू नहीं होता। VoxCPM2 जिन 30 भाषाओं को सपोर्ट करता है, वे सभी टेस्ट की गईं और काम करती हैं; जिन
भाषाओं की कोई तैयार आवाज़ नहीं है, उनके लिए `--dil <code>` इस्तेमाल करें। हर भाषा के कमांड और हमारे सीखे सबक:
[docs/cok_dilli.md](docs/cok_dilli.md)। पूरे डिज़ाइन फ़्लो के लिए Claude Code स्किल:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md)।

**शुरुआत के लिए 144 उदाहरण विवरण।** 8 में से हर भाषा में 18 भूमिकाएँ (डॉक्यूमेंट्री नैरेटर, न्यूज़ एंकर, विज्ञापन की आवाज़,
ऑडियोबुक, कहानी सुनाने वाली दादी, पॉडकास्ट होस्ट, शिक्षक, फ़िल्म ट्रेलर, ध्यान गाइड, खेल कमेंटेटर और भी, पुरुष और महिला)।
विवरण अंग्रेज़ी में है और उसमें बोलने वाले की राष्ट्रीयता और नेटिव लहजा लिखा है; साथ में वह टेक्स्ट भी आता है जो आवाज़ बनाते
समय पढ़ा जाता है, उसी भाषा में और भूमिका के मुताबिक़। कोई एक चुनें, वेरिएंट सुनें, जो पसंद आए उसे रखें:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, या वेब UI में *उदाहरण विवरण* चुनें। पूरी सूची:
[docs/ornek_tarifler.md](docs/ornek_tarifler.md)।

**अपने वीडियो अपनी आवाज़ में डब करें।** [DubWorld](https://github.com/alexturkey/dubworld) हमारा लोकल वीडियो डबिंग प्रोग्राम
है; यह इस रिपॉज़िटरी को अपने VoxCPM2 वॉइस इंजन के रूप में इंस्टॉल करता है। यहाँ डिज़ाइन की गई आवाज़ वहाँ
`ses.voxcpm2_ses = "<name>/<variant>"` से इस्तेमाल होती है।

## क्विक स्टार्ट (Windows, 3 स्टेप)

1. कोड **डाउनलोड** करें: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip)।
   आपके कार्ड के लिए तैयार इंजन पैकेज स्टेप 3 में इंस्टॉलर ख़ुद लाता है:
   NVIDIA → [CUDA पैकेज](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan पैकेज, प्रायोगिक](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (पहले से डाउनलोड कर रखा है? नीचे वाले कमांड में `-HazirZip <path to the zip>` जोड़ दें)।
2. zip को **एक्सट्रैक्ट** करें, `voxcpm2-turkce-ses-tasarimi-main` फ़ोल्डर खोलें, Explorer के एड्रेस बार में `powershell`
   लिखें और Enter दबाएँ।
3. इंस्टॉलर **चलाएँ** (64-bit Python 3.10-3.13 चाहिए; CUDA के लिए NVIDIA ड्राइवर ≥ 570), फिर **`baslat.bat`** पर डबल-क्लिक करें:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: आख़िर में `-Vulkan` जोड़ें। UI http://127.0.0.1:8765/ पर खुलता है।

इंजन zip अपने-आप में कोई अलग ऐप नहीं है (इसके exe को मॉडल और वे DLL चाहिए जिन्हें इंस्टॉलर सेट करता है)। विवरण, GPU
सूची और आम समस्याएँ: नीचे "क्विक इंस्टॉल" देखें।

## Ubuntu / Linux (NVIDIA CUDA, प्रायोगिक)

पैच किया हुआ इंजन `bash scripts/kur-linux.sh` से बनाएँ, या Ubuntu 24.04 / CUDA 12.8.1 एनवायरनमेंट में बिल्ड करने और चलाने के
लिए `Dockerfile.linux` इस्तेमाल करें। NVIDIA GPU और संगत ड्राइवर ज़रूरी हैं; नेटिव इंस्टॉलर को CUDA toolkit और Python 3.10-3.13
भी चाहिए। UI सिर्फ़ loopback पर ही रहता है, रिमोट सर्वर पर भी (SSH फ़ॉरवर्डिंग)। ज़रूरी चीज़ें, कमांड, आर्किटेक्चर का चुनाव और
जाँच का दायरा: [docs/linux.md](docs/linux.md)।

## क्विक स्टार्ट (macOS, Apple Silicon)

Xcode Command Line Tools (`xcode-select --install`) और [Homebrew](https://brew.sh) चाहिए:
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
इंस्टॉलर मॉडल डाउनलोड करता है, पैच किया हुआ इंजन Metal के साथ बिल्ड करता है (~1 मिनट) और सब कुछ `~/vox` में सेट कर देता है।
फिर **`baslat.command`** पर डबल-क्लिक करें। MacBook Air M4 16 GB पर: 1 s बोली के लिए ~2 s की गणना, एक ही सीड से बाइट-दर-बाइट
एक जैसा ऑडियो, अधिकतम ~5.3 GB RAM, और 12 मिनट तक लगातार पढ़ने में कोई थर्मल स्लोडाउन नहीं। विवरण और माप:
[docs/mac.md](docs/mac.md)।

**नेटिव Mac ऐप (बिना Python, Homebrew या Terminal के):** [macos/README.md](macos/README.md)। इसमें वही पैच किया हुआ इंजन
शामिल है और यह पहली बार चलने पर मॉडल डाउनलोड करता है; फ़िलहाल इसे Xcode से सोर्स से बिल्ड किया जाता है।

## Mac (Apple Silicon) यूज़र्स के लिए

Apple Silicon वाले Mac के लिए समुदाय का बनाया एक स्वतंत्र रूपांतरण भी है, जो VoxCPM2 को Apple के MLX फ़्रेमवर्क पर चलाता है:
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**।
इसे Emre Koç ([@emre-koc](https://github.com/emre-koc)) अपनी रिपॉज़िटरी में विकसित और मेंटेन करते हैं, यहाँ नहीं; इंस्टॉल
के स्टेप और सपोर्ट के सवाल वहीं भेजें। Emre, इस प्रोजेक्ट को Mac तक पहुँचाने के लिए शुक्रिया!

## यह कैसे काम करता है

1. **आवाज़ डिज़ाइन।** एक अंग्रेज़ी *आवाज़ का विवरण* + *आवाज़ बनाते समय पढ़ा जाने वाला टेक्स्ट* (आवाज़ की भाषा में) + वेरिएंट
   की संख्या। हर वेरिएंट को अपना सीड मिलता है; इंजन `(description)text` लेता है और हर सीड के लिए एक डिज़ाइन रिकॉर्डिंग लौटाता है।
   टेक्स्ट आवाज़ को पहचानने के लिए एक छोटा नमूना है: 1-3 वाक्य, अधिकतम ~30 s (UI अनुमान दिखाता है और 33 s से ऊपर शुरू नहीं
   करता); लंबा टेक्स्ट स्टेप 2 के लिए है।
2. **रेफ़रेंस पर आधारित पठन।** डिज़ाइन रिकॉर्डिंग इंजन के **दोनों** इनपुट (`audio` और `voice_ref`) में दी जाती है, साथ में
   उसका ट्रांसक्रिप्ट (`reference_text`) और पढ़ा जाने वाला नया टेक्स्ट, उसी सीड के साथ। आवाज़ को रिकॉर्डिंग संभालती है, विवरण
   नहीं, इसलिए वह एक टेक्स्ट से दूसरे टेक्स्ट तक भटकती नहीं। टेक्स्ट वाक्य-दर-वाक्य पढ़ा जाता है।
3. क्वालिटी तय है: 16 डिफ़्यूज़न स्टेप, CFG 2.0। सीड कोई क्वालिटी सेटिंग नहीं है।
4. **शब्दों का समय, हर बार वही आवाज़।** पढ़ते समय इंजन ख़ुद बताता है कि हर शब्द कहाँ शुरू और कहाँ ख़त्म होता है (पैच 0002, कोई अतिरिक्त मॉडल नहीं)। समय `kelimeler.json` में लिखे जाते हैं, और पंक्तियाँ इस तरह छाँटी जाती हैं कि दो पंक्तियों के बीच का अंतर ठहराव सेटिंग के बराबर हो। CTC फ़ोर्स्ड अलाइनमेंट (forced alignment, CTC = 100%) की तुलना में सटीकता: 89.66% (तुर्की, 12 आवाज़ें; सेटिंग `kelime_zamani`, डिफ़ॉल्ट रूप से चालू)। पैच 0003 के साथ एक ही सीड हर बार बाइट-दर-बाइट एक जैसी आवाज़ देता है।

कच्ची डिज़ाइन रिकॉर्डिंग आवाज़ का एक बार का नमूना है; बाद की कोई भी रीडिंग बिल्कुल उसके जैसी नहीं सुनाई देती। बाद की हर
रीडिंग में आप जो सुनते हैं, वह स्टेप 2 है: रेफ़रेंस के रूप में डिज़ाइन रिकॉर्डिंग और साथ में वेरिएंट का अपना सीड। इसीलिए वेब UI
डिज़ाइन के ठीक बाद स्टेप 2 करता है और वेरिएंट कार्ड पर दोनों दिखाता है।

इंजन हमारे पैच (`patches/`) के साथ audio.cpp v0.7.2 है, मॉडल VoxCPM2 Q8_0 GGUF है। अधिकतम VRAM ≈ 2.8 GB; GTX 1050 Ti पर
1 s बोली के लिए लगभग 2 s की गणना। विवरण और माप: [docs/4gb.md](docs/4gb.md)।

## साथ दी गई आवाज़ें (`hazir_sesler/`)

सभी चौदह आवाज़ें उनके `ses.json` में सहेजे गए विवरणों से डिज़ाइन की गई हैं; कोई भी किसी रिकॉर्डिंग से क्लोन नहीं की गई
(क्लोनिंग अलग, सहमति से बंधा *वॉइस क्लोनिंग* टैब है)।

| आवाज़ | छोटा विवरण | सुनें |
|---|---|---|
| `belgesel_hanim` | पचास के दशक की परिपक्व महिला, गहरी गर्म ऑल्टो; शांत डॉक्यूमेंट्री नैरेटर | [नमूना](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | गहरी, दमदार, रहस्यमय पुरुष नैरेटर आवाज़ | [नमूना](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | लगभग सत्तर साल के अनुभवी न्यूज़ एंकर, शांत और प्रभावशाली | [नमूना](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | तीस के दशक की करिश्माई शाम की न्यूज़ एंकर, मख़मली और भावपूर्ण | [नमूना](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | परीकथा की चुड़ैल: धीमी, हल्की नाक से निकलती, चालाकी भरी मिठास | [नमूना](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | असाधारण रूप से गहरी, भारी, रौबदार पुरुष नैरेटर आवाज़ | [नमूना](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | बूढ़ा ज्ञानी, गहरी और गूँजती आवाज़, थोड़ी रहस्यमय | [नमूना](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | पचास के दशक के नेटिव अंग्रेज़ी पुरुष डॉक्यूमेंट्री नैरेटर (General American); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | पचास के दशक के नेटिव फ़्रेंच पुरुष डॉक्यूमेंट्री नैरेटर (पेरिस का लहजा); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | पचास के दशक के नेटिव जर्मन पुरुष डॉक्यूमेंट्री नैरेटर (Hochdeutsch); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | पचास के दशक के नेटिव स्पैनिश पुरुष डॉक्यूमेंट्री नैरेटर (कास्टिलियन (मैड्रिड)); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | पचास के दशक के नेटिव रूसी पुरुष डॉक्यूमेंट्री नैरेटर (मॉस्को); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | पचास के दशक के नेटिव चीनी (मंदारिन) पुरुष डॉक्यूमेंट्री नैरेटर (बीजिंग पुतोंगह्वा); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | पचास के दशक के नेटिव जापानी पुरुष डॉक्यूमेंट्री नैरेटर (टोक्यो मानक); गहरी, शांत, गर्म आवाज़ | [नमूना](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [रेफ़रेंस](hazir_sesler/anlatici_ja/referans.flac) |

हर फ़ोल्डर में: `referans.flac` (लॉसलेस डिज़ाइन रिकॉर्डिंग), `ses.json` (विवरण, ट्रांसक्रिप्ट, डिज़ाइन सीड, रीडिंग सीड, छोटा
विवरण; नैरेटरों के लिए `dil` = भाषा), `ornek_okuma.mp3` (+ उसका टेक्स्ट)। इन्हें सीधे इस्तेमाल करें: `--ses hazir/<name>`।
नैरेटरों की रेफ़रेंस रिकॉर्डिंग छोटी हैं (5.6-10 s); उनके नमूने कप्पादोकिया स्क्रिप्ट के पहले तीन वाक्य हैं, जो पूरे प्रोडक्शन
की रीडिंग से काटे गए हैं।

## क्विक इंस्टॉल, कंपाइलर की ज़रूरत नहीं (Windows 10/11, NVIDIA GPU ≥ 4 GB)

ज़रूरी चीज़ें: NVIDIA ड्राइवर ≥ 570 और 64-bit Python 3.10-3.13 (`winget install Python.Python.3.12`)। इसके अलावा कुछ नहीं:
न Visual Studio, न CUDA इंस्टॉलर। पक्का नहीं कि आपके पास कौन-सा कार्ड है? PowerShell में `nvidia-smi` चलाएँ: यह GPU का नाम,
ड्राइवर वर्ज़न और मेमोरी दिखाता है। NVIDIA कार्ड नहीं है? नीचे "AMD / Intel" देखें।

[Git](https://git-scm.com/download/win) के साथ:

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Git के बिना: इसी पेज पर **Code → Download ZIP** पर क्लिक करें, उसे एक्सट्रैक्ट करें, एक्सट्रैक्ट हुआ
`voxcpm2-turkce-ses-tasarimi-main` फ़ोल्डर खोलें, Explorer के एड्रेस बार में `powershell` लिखकर Enter दबाएँ, फिर ऊपर की
आख़िरी लाइन चलाएँ। Git सिर्फ़ सोर्स से बिल्ड करने वाले रास्ते के लिए चाहिए।

`-ExecutionPolicy Bypass` सिर्फ़ इसी एक प्रोसेस पर लागू होता है और सिस्टम की कोई सेटिंग नहीं बदलता; किसी भी इंस्टॉलर स्क्रिप्ट
की तरह, चलाने से पहले `scripts\kur.ps1` पढ़ लें। एक कमांड, ~10 मिनट, ~3.7 GB डाउनलोड, सब कुछ sha256 से जाँचा हुआ: मॉडल
(2.95 GB), CUDA 12.8 रनटाइम DLL पोर्टेबल zip के रूप में (कोई सिस्टम इंस्टॉल नहीं, PATH अछूता), Releases पेज से **पहले से बिल्ड
किया इंजन**, दो Python पैकेज वाला `.venv`, `ayarlar.json`, और आख़िर में एक GPU जाँच (`KONTROL_OK`)। कोई गड़बड़ी हो तो इसे
दोबारा चलाएँ; जाँची जा चुकी फ़ाइलें छोड़ दी जाती हैं। फिर वेब UI शुरू करें: रिपॉज़िटरी फ़ोल्डर में **`baslat.bat`** पर
डबल-क्लिक करें। यह UI शुरू करता है और तैयार होने पर आपके ब्राउज़र में **http://127.0.0.1:8765/** खोल देता है; रोकने के लिए
काली विंडो बंद करें (या उसमें Ctrl+C दबाएँ)।
PowerShell से यही काम:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
फिर **http://127.0.0.1:8765/** ख़ुद खोलें (इस तरह शुरू करने पर UI ब्राउज़र नहीं खोलता; यह सिर्फ़ localhost पर सुनता है)।

> **रिलीज़ zip में मौजूद `audiocpp_cli.exe` डबल-क्लिक करने के लिए नहीं है।** यह एक कमांड-लाइन इंजन है जिसे अपने बगल में
> CUDA DLL और मॉडल चाहिए; `kur.ps1` सब कुछ अपनी जगह रखता है और Python पैकेज इसे चलाता है।
> डबल-क्लिक करने पर बस "cudart64_12.dll not found" दिखता है।

**सपोर्टेड GPU (रिलीज़ v0.1.1):** GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx (sm_89) और RTX 50xx
(sm_120a) के लिए नेटिव कोड; Pascal या उसके बाद का कोई भी दूसरा CUDA GPU ड्राइवर के ज़रिए एम्बेडेड PTX चलाता है (पहली बार
शुरू होने में ज़्यादा समय)। Maxwell (GTX 9xx) और उससे पुराने GPU CUDA 12.8 में सपोर्टेड नहीं हैं। हमने GTX 1050 Ti 4 GB पर
टेस्ट किया है (Windows पर Docker Desktop/WSL2 के ज़रिए भी, सिर्फ़ CLI); @mslmyilmaz5 (#15) का माप: RTX 3060 Ti 8 GB,
Ubuntu 24.04 Docker, CUDA 12.8.1 (विवरण [docs/linux.md](docs/linux.md) में)। दूसरे कार्डों की रिपोर्ट का
[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) में स्वागत है।

**AMD / Intel (प्रायोगिक):** एक अलग Vulkan इंजन zip (`...-win64-vulkan.zip`, बिना CUDA)
`scripts\kur.ps1 -Kok C:\vox -Vulkan` से इंस्टॉल होता है। इसे सिर्फ़ हमारे NVIDIA कार्ड पर Vulkan बैकएंड के ज़रिए जाँचा गया है
(वहाँ यह CUDA से धीमा चला, लेकिन एक ही सीड के लिए वही ऑडियो दिया; वह माप तब लिया गया था जब डिस्क किसी दूसरे काम में व्यस्त
थी, इसलिए साफ़ स्पीड तुलना अभी बाक़ी है) और हमने इसे ख़ुद AMD या Intel हार्डवेयर पर **नहीं** आज़माया है: अगर आप आज़माएँ, तो
नतीजा Discussions में ज़रूर लिखें। एक से ज़्यादा Vulkan डिवाइस (इंटीग्रेटेड + डेडिकेटेड) होने पर इंस्टॉलर डेडिकेटेड GPU का
इंडेक्स `ayarlar.json` में `cihaz` के रूप में लिख देता है।

*नोट: Vulkan सपोर्ट अभी प्रायोगिक है। इसे GTX 1050 Ti पर सफलतापूर्वक बिल्ड और टेस्ट किया गया है। एक बाहरी यूज़र (mitra_tr) ने इसे AMD 6900 XT पर चलाने की भी जानकारी दी है। AMD/Intel कार्डों पर अभी और व्यापक टेस्टिंग की ज़रूरत है।*

**समुदाय परीक्षण (AMD):** @mitraTR ने Windows 11 पर AMD Radeon RX 6900 XT में Vulkan के साथ v0.1.1 चलाया: इंस्टॉल, आवाज़ डिज़ाइन, पढ़ना, वेब इंटरफ़ेस और टेस्ट सब ठीक चले; पढ़ने में हर 1 सेकंड बोली के लिए लगभग 0.8-0.9 सेकंड गणना लगी ([#6 में रिपोर्ट](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655))। ऐसे छोटे फ़ोल्डर में इंस्टॉल करें जिसके पथ में केवल ASCII अक्षर हों (जैसे `C:\vox`): Windows पर इंजन हिंदी या अन्य गैर-ASCII अक्षरों वाले पथ नहीं खोल पाता। अब तक की सभी रिपोर्टें: [जाँचा गया हार्डवेयर](docs/donanim_testleri.md)।

### विकल्प: इंजन को सोर्स से बिल्ड करें

"Desktop development with C++" (C++ CMake tools सहित) के साथ Visual Studio 2022 Build Tools चाहिए, ~7 GB। फिर:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
यह nvcc भी डाउनलोड करता है, audio.cpp v0.7.2 का सोर्स लाता है, `patches/0001-voxcpm2-4gb-ve-hiz.patch` लागू करता है और आपके GPU
के लिए बिल्ड करता है (`-Mimari native`, डिफ़ॉल्ट; या जैसे `-Mimari 61`), ~15-25 मिनट। रूट छोटा रखें (`C:\vox`): लंबे पाथ पर
nvcc फ़ेल हो जाता है। जाँच के साथ स्टेप-दर-स्टेप: [AGENTS.md](AGENTS.md)।

### इंस्टॉल की आम समस्याएँ

| आपको दिखता है | इसका मतलब, क्या करें |
|---|---|
| exe पर डबल-क्लिक के बाद `cudart64_12.dll not found` | इंजन को हाथ से शुरू करने के लिए नहीं बनाया गया है। ऊपर वाला `kur.ps1` कमांड चलाएँ, फिर वेब UI शुरू करें। |
| `64-bit Python 3.10+ bulunamadı` (Python नहीं मिला) | Python इंस्टॉल करें (`winget install Python.Python.3.12`), PowerShell बंद करें, नया खोलें और वही कमांड दोबारा चलाएँ। |
| `motor ekran kartını görmedi` (इंजन को GPU नहीं दिखा) | NVIDIA ड्राइवर को 570 या नए वर्ज़न पर अपडेट करें; जाँचें कि `nvidia-smi` चलता है। |
| `indirme başarısız` / `sha256 tutmadı` (डाउनलोड फ़ेल / चेकसम मेल नहीं खाया) | आम तौर पर बीच में टूटा डाउनलोड। वही कमांड दोबारा चलाएँ; जाँची जा चुकी फ़ाइलें छोड़ दी जाती हैं। |
| बिल्ड वाला रास्ता: `nvcc` फ़ेल होता है | इंस्टॉल रूट छोटा रखें (`-Kok C:\vox`)। |
| पेज नहीं खुलता | UI को `baslat.bat` से शुरू करें, या http://127.0.0.1:8765/ ख़ुद खोलें। पोर्ट व्यस्त है? `ayarlar.json` में `"port"` बदलें। |

कोई समस्या? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) या
[इंस्टॉल issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
खोलें, जिसमें आपका GPU, Windows वर्ज़न, कमांड और उसकी आख़िरी लाइनें हों।

## इस्तेमाल

कमांड लाइन:
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
टेक्स्ट के नियम: संख्याएँ शब्दों में लिखें, उद्धरण चिह्न न लगाएँ (टूल अंकों और उद्धरण चिह्नों को अस्वीकार करता है), हर लाइन में
एक वाक्य, हर लाइन में ≤ 2000 अक्षर। लाइन के बाद ठहराव: `|| bagli` 0.25 s, `|| normal` 0.5 s, `|| paragraf` 1 s, `|| agir` 1.5 s
या अपनी अवधि `|| 0,8` (0-5 s; मार्कर के अंकों की अनुमति है)। `ayarlar/okunus_sozlugu.tsv` तुर्की टेक्स्ट में विदेशी शब्दों के उच्चारण ठीक करता है।
भाषा टेक्स्ट से पहचानी जाती है (तुर्की अक्षर, लिपि, आम शब्द; संदेह होने पर वॉइस कार्ड का `dil`; `--dil <code>` वैकल्पिक है)। ग़ैर-तुर्की
टेक्स्ट में वहाँ एपॉस्ट्रॉफ़ी की अनुमति है, तुर्की शब्दकोश छोड़ दिया जाता है, अंक अब भी अस्वीकार होते हैं। अगर कोई रीडिंग
`speed gate: satır [...]` प्रिंट करे, तो उन लाइनों को सुनें।

### वेब UI

सिर्फ़ लोकल (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → http://127.0.0.1:8765/ ख़ुद खोलें
(दूसरा पोर्ट: `--port 8800`), या `baslat.bat` पर डबल-क्लिक करें। सर्वर को Ctrl+C से रोकें। तीन टैब: *आवाज़ डिज़ाइन करें*,
*इस आवाज़ में पढ़ें*, *वॉइस क्लोनिंग*। आम रास्ता: *डिज़ाइन करें* → वेरिएंट सुनें → *मेरी पठन सूची में जोड़ें* →
*इस आवाज़ में पढ़ें* → डाउनलोड। या आवाज़ मेनू से कोई तैयार आवाज़ चुनें और पढ़वाएँ।

- **हेडर में वर्ज़न।** एक छोटा, हल्का `v0.2.0 · <short commit>` (ट्रैक की गई फ़ाइलों में बिना कमिट किए बदलाव हों तो `+` के साथ;
  git न हो तो सिर्फ़ वर्ज़न), ताकि स्क्रीनशॉट और वीडियो में दिखे कि कौन-सा वर्ज़न इस्तेमाल हुआ।
- **हर वेरिएंट कार्ड पर दो आवाज़ें।** ऊपर, स्लेटी रंग में, *कच्ची डिज़ाइन आवाज़*: यह एक बार बनती है और फिर कभी हूबहू वैसी
  नहीं निकलती। उसके नीचे, नारंगी फ़्रेम में, *↻ यही आवाज़ आप हमेशा सुनेंगे*: डिज़ाइन रिकॉर्डिंग को रेफ़रेंस बनाकर वेरिएंट के
  अपने सीड (कार्ड पर दिखाया गया) से दोबारा पढ़ा गया रूप। बाद की हर रीडिंग में आवाज़ ऐसी ही सुनाई देती है। उसके नीचे
  *इस आवाज़ में पढ़ें* और *मेरी पठन सूची में जोड़ें* हैं। *डिज़ाइन करें* का एक क्लिक दोनों काम करता है: यह हर वेरिएंट डिज़ाइन
  करता है, फिर हर स्थायी आवाज़ में आपका टेक्स्ट पढ़ता है; एक ही प्रोग्रेस बार दोनों चरण गिनता है। वेरिएंट फ़ोल्डर में
  `dinleme.wav` बनती है। अगर वह रीडिंग बीच में रुक जाए, तो डिज़ाइन बचा रहता है और कार्ड पर एक नोट दिखता है।
- **"जो टेक्स्ट आप सुनना चाहते हैं" विंडो।** *आवाज़ डिज़ाइन करें* में *↻ जो टेक्स्ट आप सुनना चाहते हैं* बॉक्स में वह टेक्स्ट
  रहता है जिसे हर स्थायी आवाज़ पढ़ती है (ख़ाली छोड़ें तो नमूना वाक्य पढ़ा जाता है)। उस पर क्लिक करने से पठन नोटबुक एक विंडो
  में खुलती है: लाइन नंबर, लाइन मेनू, ठहराव पट्टियाँ। *ठीक है* टेक्स्ट और उसके ठहराव वापस बॉक्स में लिख देता है; *रद्द करें*
  या Esc कुछ नहीं बदलते। पढ़ने वाला टैब अपना टेक्स्ट अलग रखता है।
- **पठन नोटबुक।** हर लाइन में एक वाक्य। लाइन मेनू के लिए किसी लाइन नंबर पर क्लिक करें (ऊपर या नीचे ले जाएँ, किसी जगह पर
  ले जाएँ, डुप्लिकेट करें, हटाएँ; Alt+↑/↓, Alt+Shift+↓, या नंबर से खींचें; Ctrl+Z टेक्स्ट और ठहराव दोनों को एक साथ वापस लेता
  है)। ठहराव चुनने के लिए दो लाइनों के बीच की पतली पट्टी पर क्लिक करें (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 s, या
  गियर से अपनी 0-5 s); पैराग्राफ़ (1 s) के लिए दो बार Enter दबाएँ, और ख़ाली लाइनें ठहराव पट्टियाँ बन जाती हैं। नतीजा चलते समय
  पढ़ी जा रही लाइन चमकती है और स्क्रॉल होकर सामने आ जाती है; लाइन मेनू में *▶ यहाँ से सुनें* उसी लाइन से चलाता है। पेज
  रीलोड करने पर भी टेक्स्ट और उसके ठहराव बने रहते हैं (ब्राउज़र स्टोरेज)।
- **ड्राफ़्ट।** *📄 ड्राफ़्ट* बटन दोनों नोटबुक (पढ़ने वाला टैब और विंडो) में है। मौजूदा टेक्स्ट को उसके ठहरावों के साथ ड्राफ़्ट
  के रूप में सहेजें, एक क्लिक से कोई ड्राफ़्ट लोड करें (Ctrl+Z वापस लेता है), और ओवरराइट करने, नाम बदलने या हटाने के लिए ⋯
  इस्तेमाल करें। ड्राफ़्ट `sesler/taslaklar.json` में सहेजे जाते हैं, रिपॉज़िटरी में कभी नहीं।
- **पठन सूची और आवाज़ मेनू।** वेरिएंट कार्ड पर *मेरी पठन सूची में जोड़ें* एक नाम बॉक्स खोलता है: वेरिएंट को उसका अपना नाम दें
  और ✓ उसे जोड़ देता है। *जनरेशन का नाम* उस रन के हर वेरिएंट पर बना रहता है। *इस आवाज़ में पढ़ें* में आवाज़ बटन (झंडा + नाम)
  आवाज़ मेनू खोलता है: सबसे ऊपर *मेरी पठन सूची*, फिर झंडों के साथ तैयार आवाज़ें (पहले इंटरफ़ेस की भाषा)। हर पंक्ति में ▶ सुनें
  (स्थायी आवाज़ हो तो वही), दिल (जोड़ें या हटाएँ) और ⋯ है; ↑/↓ और Enter से चुनें, Esc से बंद करें, आख़िरी आवाज़ याद रहती है।
  सूची रिपॉज़िटरी के बाहर `sesler/okuma_listesi.json` में रहती है और रीस्टार्ट के बाद भी बची रहती है।
- **आवाज़ों का प्रबंधन।** ⋯ मेनू (आवाज़ मेनू की पंक्ति या वेरिएंट कार्ड) में *इस आवाज़ में पढ़ें*, सूची में जोड़ना या उससे
  हटाना, *नाम बदलें* (ख़ाली नाम से मूल नाम लौट आता है; *मूल नाम पर लौटें*), डिज़ाइन की गई आवाज़ों के लिए *हटाएँ* और तैयार
  आवाज़ों के लिए *छिपाएँ* हैं; दोनों पहले पूछते हैं। हटाई गई आवाज़ `sesler/_cop/` में चली जाती है; छिपाने से रिपॉज़िटरी की
  फ़ाइलों को कभी छुआ नहीं जाता। आवाज़ मेनू में सबसे नीचे *छिपी और हटाई गई आवाज़ें (N)* में *वापस लाएँ* है। अपने रखे नाम और
  छिपी आवाज़ें `sesler/yerel_katman.json` में रखी जाती हैं। नाम बदली गई आवाज़ अपना मूल स्रोत स्लेटी रंग में दिखाती है
  (*जनरेशन का नाम · वेरिएंट N*); ⋯ → *जनरेशन पर जाएँ* उसका डिज़ाइन खोलता है।
- **शॉर्टकट और फ़ाइलें।** खुले टैब पर Ctrl+Enter (Mac पर ⌘+Enter) *डिज़ाइन करें* या *इस आवाज़ में पढ़ें* शुरू करता है।
  प्रोग्रेस बार *बीता समय / ~कुल* दिखाता है, जिसका अनुमान आपकी मशीन पर पहले हुए कामों से सीखा जाता है। डाउनलोड का नाम आवाज़
  और समय पर रखा जाता है (`Voice_Name_2026-11-02_0152.wav`)।

**वॉइस क्लोनिंग (आपकी अपनी या सहमति वाली आवाज़)।** UI के *वॉइस क्लोनिंग* टैब में अपनी रिकॉर्डिंग (wav/mp3/flac/ogg, 5-30 s की साफ़ बोली की सलाह; 3 s से कम अस्वीकार, 36 s से ज़्यादा काट दी जाती है), उसका सटीक ट्रांसक्रिप्ट और पढ़ा जाने वाला टेक्स्ट दें। जब तक आप "यह आवाज़ मेरी है या मेरे पास इसके मालिक की साफ़ अनुमति है" पर टिक नहीं करते, बटन बंद रहता है। रिकॉर्डिंग सिर्फ़ लोकल सर्वर (127.0.0.1) तक जाती है, अपने रेफ़रेंस एन्कोडिंग के साथ एक अस्थायी फ़ोल्डर में प्रोसेस होती है, और काम ख़त्म होने पर, नाकाम होने पर भी, वह फ़ोल्डर हटा दिया जाता है; नेटवर्क पर कुछ नहीं भेजा जाता। सिर्फ़ सिंथेटिक आउटपुट रखा जाता है (UI: `sesler/_okumalar/<job>/`, CLI: `--cikti`)। आउटपुट "synthetic" टैग वाली `klon_synthetic.wav` है; शेयर करते समय उस पर AI-जनरेटेड का लेबल लगाएँ। CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## अक्सर पूछे जाने वाले सवाल

**मॉडल या इंजन? क्या क्या है?** VoxCPM2 (OpenBMB) *मॉडल* है: 2 अरब पैरामीटर वाला नेटवर्क जो टेक्स्ट को बोली में बदलता है।
audio.cpp *इंजन* है: C++/CUDA प्रोग्राम जो मॉडल को आपके GPU पर चलाता है (`audiocpp_cli.exe`)। हमारा पैच इंजन को बदलता है,
मॉडल को नहीं: यह VoxCPM2 को 4 GB में समाने लायक बनाता है और यह पक्का करता है कि एक ही सीड हर बार वही ऑडियो दे। इस रिपॉज़िटरी
का Python पैकेज सिर्फ़ टेक्स्ट तैयार करता है, इंजन को बुलाता है और फ़ाइलें इकट्ठा करता है।

**कौन-से GPU?** ऊपर "सपोर्टेड GPU" देखें: GTX 10xx और उससे ऊपर के NVIDIA, 4 GB या ज़्यादा VRAM, ड्राइवर ≥ 570। रिलीज़ में
sm_61/75/86/89/120a के लिए नेटिव कोड है; Pascal या नए दूसरे कार्ड एम्बेडेड PTX इस्तेमाल करते हैं (पहली बार शुरू होने में ज़्यादा
समय)। AMD/Intel: प्रायोगिक Vulkan zip, `kur.ps1 -Vulkan`; एक बाहरी यूज़र ने इसे AMD 6900 XT पर चलाने की जानकारी दी है, लेकिन
AMD/Intel पर और व्यापक टेस्टिंग की अभी ज़रूरत है (ऊपर "AMD / Intel" देखें)। सिर्फ़ CPU (`ayarlar.json` में `"backend": "cpu"`)
पर यह चलता है, लेकिन GTX 1050 Ti से ~6× धीमा है (इंजन माप, 48 s बोली के लिए 535 s बनाम 94 s); यह सपोर्टेड रास्ता नहीं है।

**कितना तेज़?** GTX 1050 Ti 4 GB (i7-7700HQ) पर मापा गया: एक डिज़ाइन वेरिएंट (≈ 25 s रिकॉर्डिंग) 55 s; रीडिंग में 1 s बोली
के लिए ≈ 2 s की गणना (रियल-टाइम फ़ैक्टर 1.9-2.8), हर आवाज़ के लिए एक बार की ~50 s रेफ़रेंस एन्कोडिंग (डिस्क पर कैश) और हर
बैच में 10-20 s मॉडल लोड के बाद; अधिकतम VRAM 2.6-2.9 GB। नए कार्ड ज़्यादा तेज़ हैं; आँकड़े और तरीक़ा:
[docs/4gb.md](docs/4gb.md)।

**क्या यह आवाज़ क्लोन कर सकता है?** मूल VoxCPM2 मॉडल किसी रेफ़रेंस रिकॉर्डिंग से आवाज़ की नक़ल कर सकता है, और क्लोनिंग वाला
हिस्सा इसी का इस्तेमाल करता है। इसे सिर्फ़ अपनी आवाज़ के साथ, या जिसकी आवाज़ है उसकी साफ़ अनुमति से ही इस्तेमाल करें; UI आपसे
इस अनुमति की पुष्टि करवाता है। आवाज़ डिज़ाइन को किसी रिकॉर्डिंग की ज़रूरत नहीं: यह अंग्रेज़ी या चीनी में लिखे टेक्स्ट विवरण से
शुरू होता है, और डिज़ाइन की गई आवाज़ से पढ़वाने में इस्तेमाल होने वाला "रेफ़रेंस" मॉडल की अपनी सिंथेटिक डिज़ाइन रिकॉर्डिंग है।
किसी और की नक़ल करना, धोखाधड़ी और गुमराह करना मना है। [ETHICS.md](ETHICS.md) देखें। आप जो भी प्रकाशित करें, उस पर
AI-जनरेटेड का लेबल लगाएँ।

**आवाज़ का अच्छा विवरण कैसे लिखूँ?** अंग्रेज़ी में, 1-3 वाक्य: उम्र और लिंग, आवाज़ का रंग (गहरी/चमकदार, गर्म, नाक से निकलती,
खरखराती), लहजा और भूमिका (शांत डॉक्यूमेंट्री नैरेटर, जोशीला प्रेज़ेंटर), रफ़्तार (धीमी, नपी-तुली), और
"clean studio recording, no background noise"। इसे विवरण ही रखें, स्क्रिप्ट नहीं; कोष्ठक नहीं। 3-5 वेरिएंट माँगें और सुनें: सीड
आवाज़ को काफ़ी बदल देता है। आवाज़ बनाते समय पढ़े जाने वाले टेक्स्ट के लिए आवाज़ की भाषा में 1-3 स्वाभाविक वाक्य लें, उसी मूड में
जो आप चाहते हैं (अधिकतम ~30 s बोली)। पढ़वाते समय हर लाइन में एक वाक्य; लंबे वाक्य तोड़ें, संख्याएँ शब्दों में लिखें।

## योगदान

समझ नहीं आ रहा कहाँ से शुरू करें? ये चार छोटे issue पहला क़दम रखने के लिए अच्छे हैं:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) अपने GPU पर आज़माएँ और कार्ड, ड्राइवर और समय की रिपोर्ट करें
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: प्रायोगिक Vulkan बिल्ड आज़माएँ
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) टेस्ट सेट में एक वाक्य जोड़ें
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) अपनी डिज़ाइन की हुई आवाज़ उसके विवरण और सीड के साथ शेयर करें

**अपना ग्राफ़िक्स कार्ड जाँचें, रिपोर्ट लिखें:** कोडिंग की ज़रूरत नहीं, बस [हार्डवेयर टेस्ट रिपोर्ट फ़ॉर्म](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml) भरें; Intel ग्राफ़िक्स कार्ड से अभी तक कोई रिपोर्ट नहीं है।

साझा टेस्ट सेट: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); ब्रांड वॉइस गाइड:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); कोड कैसे भेजें: [CONTRIBUTING.md](CONTRIBUTING.md)।
इंस्टॉल की समस्याएँ: [issue फ़ॉर्म](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); सवाल और नतीजे: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)।
हिस्सा लेने वाले सभी लोग [आचार संहिता](CODE_OF_CONDUCT.md) का पालन करते हैं: विनम्र रहें, और फ़ीडबैक काम के बारे में रखें।

## योगदानकर्ता

- [@alexturkey](https://github.com/alexturkey): मेंटेनर; कोड, तैयार आवाज़ें, दस्तावेज़
- [@cayir21](https://github.com/cayir21): macOS (Apple Silicon) Metal सपोर्ट, [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): CPU बैकएंड पर कई वाक्यों की रीडिंग के लिए वाक्य-अंत (EOS) फ़िक्स, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): Ubuntu/Linux के लिए प्रायोगिक CUDA इंस्टॉलेशन और Docker सपोर्ट, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

आपका नाम भी यहाँ होना चाहिए: आपके GPU का टेस्ट नतीजा, टेस्ट सेट के लिए एक वाक्य, आपकी डिज़ाइन की हुई आवाज़, एक साफ़ बग
रिपोर्ट या एक pull request, सब योगदान माने जाते हैं। इसे आज़माने और हमें लिखने वाले हर व्यक्ति का शुक्रिया।

## लाइसेंस और श्रेय

कोड और तैयार आवाज़ें: Apache-2.0, Copyright 2026 Ali Haydar Ozturk। VoxCPM2 (OpenBMB, Apache-2.0), audio.cpp (ShugoAI LLC,
Apache-2.0) और audio.cpp के GGUF कन्वर्ज़न पर आधारित। पूरी सूची: [THIRD_PARTY.md](THIRD_PARTY.md)।
OpenBMB, ModelBest या audio.cpp प्रोजेक्ट से इसका कोई संबंध नहीं है।

[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · **မြန်မာ** · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**4 GB GPU ပေါ်တွင် VoxCPM2 ဖြင့် တူရကီ အသံ ဒီဇိုင်းဆွဲခြင်း။** အသံတစ်ခုကို အင်္ဂလိပ်လို ဖော်ပြပါ၊ model က
ဖန်တီးပေးပါလိမ့်မည်၊ နှစ်သက်သော ပုံစံကို ရွေးပြီး ထိုအသံဖြင့် မည်သည့် တူရကီ စာသားကိုမဆို ဖတ်ခိုင်းနိုင်သည်။ command
တစ်ကြောင်းတည်းဖြင့် ထည့်သွင်းနိုင်သော installer၊ GTX 1050 Ti (4 GB) တွင် ဆံ့အောင် ပြင်ဆင်ထားသော
[audio.cpp](https://github.com/0xShug0/audio.cpp) engine၊ ကိုယ့်စက်ပေါ်တွင်သာ အလုပ်လုပ်သော သေးငယ်သည့် web UI နှင့်
အသင့်ပါသော synthetic အသံ ဆယ့်လေးမျိုး ပါဝင်သည်- တူရကီ အသံ ခုနစ်မျိုးနှင့် အင်္ဂလိပ်၊ ပြင်သစ်၊ ဂျာမန်၊ စပိန်၊ ရုရှား၊
တရုတ်နှင့် ဂျပန် ဘာသာ မိခင်ဘာသာစကားပြော ဇာတ်ကြောင်းပြောသူ ခုနစ်ဦး ဖြစ်သည်။

- app သည် ဘာသာစကား 30 ဖြင့် ဖတ်ပေးသည်၊ interface လည်း ဘာသာစကား 30 ဖြင့် ရရှိသည်။
- အသင့်ပါသော အသံ 14 မျိုး- တူရကီ 7 မျိုး၊ ထို့အပြင် အင်္ဂလိပ်၊ ပြင်သစ်၊ ဂျာမန်၊ စပိန်၊ ရုရှား၊ တရုတ်နှင့် ဂျပန် ဘာသာ တစ်မျိုးစီ။
- Web UI (v0.2.0)- ပုံစံကတ်တိုင်းတွင် အသံနှစ်မျိုး ပါသည်၊ မူလဒီဇိုင်းအသံနှင့် နောက်ပိုင်း အမြဲကြားရမည့် အသံ။ အသံ menu ပါသော
  ဖတ်ရန်စာရင်း၊ အသံများကို အမည်ပြောင်းခြင်း၊ ဖျောက်ခြင်း သို့မဟုတ် ဖျက်ခြင်း၊ သင်ဖတ်သော စာသားများအတွက် မူကြမ်းများ။
  "အသုံးပြုပုံ" အောက်ရှိ "Web UI" ကို ကြည့်ပါ။

[4 GB တွင် ဘယ်လို ဆံ့သလဲ](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [AI agent များအတွက် ထည့်သွင်းခြင်း လမ်းညွှန်](AGENTS.md) · [တာဝန်ယူမှုရှိသော အသုံးပြုမှု](ETHICS.md)

> ပါဝင်သော အသံများသည် synthetic အသံများ ဖြစ်ပြီး စာသား ဖော်ပြချက်မှ ဒီဇိုင်းဆွဲထားခြင်း ဖြစ်သည်။ အသံပုံတူကူးခြင်း အပိုင်းကို
> သင့်ကိုယ်ပိုင်အသံ သို့မဟုတ် ပိုင်ရှင်၏ ရှင်းလင်းသော ခွင့်ပြုချက်ဖြင့် အသုံးပြုသော အသံအတွက်သာ အသုံးပြုရမည်၊ UI က ထိုခွင့်ပြုချက်ကို
> အတည်ပြုရန် တောင်းဆိုသည်။ အခြားသူအဖြစ် ဟန်ဆောင်ခြင်း၊ လိမ်လည်ခြင်းနှင့် လှည့်ဖြားခြင်းကို တားမြစ်ထားသည်။ သင်ထုတ်လုပ်သမျှကို
> AI ဖြင့် ထုတ်လုပ်ထားကြောင်း ဖော်ပြပါ။ [ETHICS.md](ETHICS.md) ကို ကြည့်ပါ။

## ဘာသာစကား 30

ကပ္ပဒိုးကီးယား (Cappadocia) အကြောင်း မှတ်တမ်းရုပ်ရှင် ဗီဒီယိုတစ်ခုကို ဘာသာစကား 8 မျိုးဖြင့် ပြုလုပ်ခဲ့သည်- တူရကီ၊ အင်္ဂလိပ်၊
ပြင်သစ်၊ ဂျာမန်၊ စပိန်၊ ရုရှား၊ တရုတ်နှင့် ဂျပန်။ ဘာသာစကားတိုင်းတွင် ကိုယ်ပိုင် **မိခင်ဘာသာစကားပြော ဇာတ်ကြောင်းပြောသူ** ရှိပြီး
အင်္ဂလိပ် ဖော်ပြချက်မှ VoxCPM2 ဖြင့် ဒီဇိုင်းဆွဲထားသည်။ အားလုံးကို 4 GB GTX 1050 Ti ပေါ်တွင် လုံးဝ local ဖြင့်၊ ပုံသေ
အရည်အသွေးတစ်ခုတည်း (16 steps, cfg 2.0) ဖြင့် ထုတ်လုပ်ခဲ့သည်။ ဇာတ်ကြောင်းပြောသူ ခုနစ်ဦးကို ၎င်းတို့၏ prompt၊ ဒီဇိုင်း စာသား၊
seed နှင့် reference အသံဖိုင်တို့နှင့်အတူ ဤနေရာတွင် ထည့်ပေးထားသည်။

| ကုဒ် | ဘာသာစကား | အသံ | နားထောင်ရန် | ဗီဒီယို |
|---|---|---|---|---|
| `tr` | တူရကီ | `hazir/belgesel_hanim` (နှင့် နောက်ထပ် 6 မျိုး) | [နမူနာ](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | အင်္ဂလိပ် | `hazir/anlatici_en` | [နမူနာ](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113791986763440439) |
| `fr` | ပြင်သစ် | `hazir/anlatici_fr` | [နမူနာ](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113790681575804962) |
| `de` | ဂျာမန် | `hazir/anlatici_de` | [နမူနာ](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113791351645262249) |
| `es` | စပိန် | `hazir/anlatici_es` | [နမူနာ](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113807365611122705) |
| `ru` | ရုရှား | `hazir/anlatici_ru` | [နမူနာ](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113801574136848884) |
| `zh` | တရုတ် (မန်ဒရင်း) | `hazir/anlatici_zh` | [နမူနာ](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113802229606121794) |
| `ja` | ဂျပန် | `hazir/anlatici_ja` | [နမူနာ](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [ဗီဒီယို](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**ဘာကြောင့် စာကြောင်းတစ်ကြောင်းချင်း ဖတ်သလဲ။** VoxCPM2 သည် တစ်ကြိမ်တည်း ရှည်လျားစွာ ထုတ်လုပ်ရာတွင် (ခန့်မှန်းခြေ စက္ကန့်
30 ကျော်လျှင်) မတည်ငြိမ်ပါ- စည်းချက် မြန်လာပြီး အသံ လွဲသွားနိုင်သည်။ ဤနေရာတွင် အသံကို ပုံသေ reference အသံဖိုင်နှင့် seed က
ထိန်းထားပြီး ရှည်လျားသော စာသားကို တစ်ကြောင်းလျှင် စာကြောင်းတစ်ကြောင်းနှုန်းဖြင့် ဖတ်သောကြောင့် ပထမ စာကြောင်းမှ နောက်ဆုံး
စာကြောင်းအထိ အသံအရောင်နှင့် ပုံစံ မပြောင်းလဲပါ။ တူရကီ မဟုတ်သော ဘာသာစကားများအတွက် တူရကီ အသံထွက် အဘိဓာန်ကို
အသုံးမပြုပါ။ VoxCPM2 ပံ့ပိုးသော ဘာသာစကား 30 လုံးကို စမ်းသပ်ပြီး အလုပ်လုပ်ကြောင်း တွေ့ရသည်၊ အသင့်ပါသော အသံ မရှိသည့်
ဘာသာစကားများအတွက် `--dil <code>` ကို သုံးပါ။ ဘာသာစကားအလိုက် command များနှင့် ကျွန်ုပ်တို့ သင်ယူခဲ့ရသော သင်ခန်းစာများ-
[docs/cok_dilli.md](docs/cok_dilli.md)။ ဒီဇိုင်း လုပ်ငန်းစဉ် တစ်ခုလုံးအတွက် Claude Code skill-
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md)။

**စတင်ရန် နမူနာ prompt 144 ခု။** ဘာသာစကား 8 မျိုးစီတွင် အခန်းကဏ္ဍ 18 မျိုး (မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ၊ သတင်းကြေညာသူ၊
ကြော်ငြာ အသံ၊ အသံစာအုပ်၊ ပုံပြင်ပြောသော အဖွား၊ podcast အစီအစဉ်တင်ဆက်သူ၊ ဆရာ၊ ရုပ်ရှင် trailer၊ တရားထိုင် လမ်းညွှန်၊ အားကစား
ကော်မန့်တာ စသည်၊ ကျားနှင့် မ) ပါဝင်သည်။ prompt သည် အင်္ဂလိပ်လို ဖြစ်ပြီး ပြောသူ၏ နိုင်ငံသားနှင့် မူလ လေယူလေသိမ်းကို ဖော်ပြထားသည်၊
အသံ ဖန်တီးစဉ် ဖတ်မည့် စာသားကိုလည်း ထိုဘာသာစကားဖြင့်၊ အခန်းကဏ္ဍနှင့် ကိုက်ညီအောင် တွဲပေးထားသည်။ တစ်ခုကို ရွေးပါ၊ ပုံစံများကို
နားထောင်ပါ၊ နှစ်သက်သည်ကို သိမ်းထားပါ- `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`၊ သို့မဟုတ်
web UI တွင် *နမူနာ ဖော်ပြချက်* ကို ရွေးပါ။ စာရင်း အပြည့်အစုံ- [docs/ornek_tarifler.md](docs/ornek_tarifler.md)။

**သင့်ဗီဒီယိုများကို ကိုယ်ပိုင်အသံဖြင့် အသံသွင်းပါ။** [DubWorld](https://github.com/alexturkey/dubworld) သည်
ကိုယ့်စက်ပေါ်တွင် အလုပ်လုပ်သော ကျွန်ုပ်တို့၏ ဗီဒီယို dubbing ပရိုဂရမ် ဖြစ်ပြီး ဤ repository ကို ၎င်း၏ VoxCPM2 အသံ engine
အဖြစ် ထည့်သွင်းသည်။ ဤနေရာတွင် ဒီဇိုင်းဆွဲထားသော အသံကို ထိုနေရာတွင် `ses.voxcpm2_ses = "<name>/<variant>"` ဖြင့် အသုံးပြုသည်။

## အမြန်စတင်ရန် (Windows, အဆင့် 3 ဆင့်)

1. code ကို **ဒေါင်းလုဒ်** လုပ်ပါ- [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip)။
   သင့်ကတ်အတွက် အသင့် engine package ကို အဆင့် 3 တွင် installer က ယူပေးမည်-
   NVIDIA → [CUDA package](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip)၊
   AMD / Intel → [Vulkan package, စမ်းသပ်ဆဲ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (တစ်ခု ဒေါင်းလုဒ်ပြီးပြီလား။ အောက်ပါ command တွင် `-HazirZip <path to the zip>` ကို ထည့်ပါ)။
2. zip ကို **ဖြည်ပါ**၊ `voxcpm2-turkce-ses-tasarimi-main` folder ကို ဖွင့်ပါ၊ Explorer ၏ လိပ်စာဘားတွင် `powershell` ဟု ရိုက်ပြီး
   Enter နှိပ်ပါ။
3. installer ကို **run ပါ** (64-bit Python 3.10-3.13 လိုအပ်သည်၊ CUDA အတွက် NVIDIA driver ≥ 570)၊ ထို့နောက် **`baslat.bat`** ကို နှစ်ချက်နှိပ်ပါ-
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel- နောက်ဆုံးတွင် `-Vulkan` ထည့်ပါ။ UI သည် http://127.0.0.1:8765/ တွင် ပွင့်လာမည်။

engine zip သည် သီးခြား အလုပ်လုပ်နိုင်သော app မဟုတ်ပါ (၎င်း၏ exe သည် installer က ပြင်ဆင်ပေးသော model နှင့် DLL များ လိုအပ်သည်)။
အသေးစိတ်၊ GPU စာရင်းနှင့် အဖြစ်များသော ပြဿနာများ- အောက်ရှိ "အမြန် ထည့်သွင်းခြင်း" ကို ကြည့်ပါ။

## Ubuntu / Linux (NVIDIA CUDA, စမ်းသပ်ဆဲ)

ပြင်ဆင်ထားသော engine ကို `bash scripts/kur-linux.sh` ဖြင့် build လုပ်ပါ၊ သို့မဟုတ် `Dockerfile.linux` ကို သုံး၍
Ubuntu 24.04 / CUDA 12.8.1 ပတ်ဝန်းကျင်တွင် build လုပ်ပြီး run ပါ။ NVIDIA GPU နှင့် ကိုက်ညီသော driver လိုအပ်သည်၊ native installer
အတွက် CUDA toolkit နှင့် Python 3.10-3.13 လည်း လိုအပ်သည်။ UI သည် အဝေးရှိ server များပေါ်တွင်ပင် loopback တွင်သာ နားထောင်သည်
(SSH forwarding)။ ကြိုတင်လိုအပ်ချက်များ၊ command များ၊ architecture ရွေးချယ်ခြင်းနှင့် စစ်ဆေးမှု နယ်ပယ်-
[docs/linux.md](docs/linux.md)။

## အမြန်စတင်ရန် (macOS, Apple Silicon)

Xcode Command Line Tools (`xcode-select --install`) နှင့် [Homebrew](https://brew.sh) လိုအပ်သည်-
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
installer သည် model ကို ဒေါင်းလုဒ်လုပ်ပြီး ပြင်ဆင်ထားသော engine ကို Metal ဖြင့် build လုပ်ကာ (~1 မိနစ်) အားလုံးကို `~/vox` အောက်တွင်
ပြင်ဆင်ပေးသည်။ ထို့နောက် **`baslat.command`** ကို နှစ်ချက်နှိပ်ပါ။ MacBook Air M4 16 GB ပေါ်တွင်- စကားပြော 1 s လျှင် တွက်ချက်ချိန်
~2 s၊ seed တူလျှင် byte အထိ တူညီသော အသံ ထွက်သည်၊ RAM အမြင့်ဆုံး ~5.3 GB၊ 12 မိနစ် ဆက်တိုက်ဖတ်စဉ် အပူကြောင့် နှေးကွေးခြင်း
မရှိပါ။ အသေးစိတ်နှင့် တိုင်းတာချက်များ- [docs/mac.md](docs/mac.md)။

**Native Mac app (Python၊ Homebrew သို့မဟုတ် Terminal မလိုပါ)-** [macos/README.md](macos/README.md)။ ၎င်းတွင် ပြင်ဆင်ထားသော
engine တူကို ထည့်ထားပြီး ပထမဆုံး ဖွင့်ချိန်တွင် model ကို ဒေါင်းလုဒ်လုပ်သည်၊ လောလောဆယ် source မှ Xcode ဖြင့် build လုပ်ရသည်။

## Mac (Apple Silicon) အသုံးပြုသူများအတွက်

Apple ၏ MLX framework ဖြင့် VoxCPM2 ကို run သော Apple Silicon Mac များအတွက် community က ပြုလုပ်ထားသည့် သီးခြား ပြုပြင်ထားသော
ဗားရှင်းတစ်ခုလည်း ရှိသည်- **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**။
၎င်းကို Emre Koç ([@emre-koc](https://github.com/emre-koc)) က ဤနေရာတွင် မဟုတ်ဘဲ သူ၏ ကိုယ်ပိုင် repository တွင် ဖန်တီးထိန်းသိမ်းသည်၊
ထည့်သွင်းပုံ အဆင့်များနှင့် အကူအညီ မေးခွန်းများကို ထိုနေရာသို့ မေးပါ။ ဤ project ကို Mac သို့ ယူဆောင်လာပေးသည့်အတွက် Emre ကို
ကျေးဇူးတင်ပါသည်!

## အလုပ်လုပ်ပုံ

1. **အသံ ဒီဇိုင်း။** အင်္ဂလိပ်လို *အသံ ဖော်ပြချက်* + *အသံ ဖန်တီးစဉ် ဖတ်မည့် စာသား* (အသံ၏ ဘာသာစကားဖြင့်) + ပုံစံ အရေအတွက်။
   ပုံစံတိုင်းသည် ကိုယ်ပိုင် seed ရရှိသည်၊ engine သည် `(description)text` ကို လက်ခံပြီး seed တစ်ခုလျှင် ဒီဇိုင်း အသံဖိုင်
   တစ်ခု ပြန်ပေးသည်။ စာသားသည် အသံကို သိရှိရန် နမူနာ တိုတစ်ခုသာ ဖြစ်သည်- စာကြောင်း 1-3 ကြောင်း၊ အများဆုံး ~30 s (UI က ခန့်မှန်းချိန်ကို
   ပြပြီး 33 s ကျော်လျှင် မစတင်ပါ)၊ ရှည်လျားသော စာသားသည် အဆင့် 2 အတွက် ဖြစ်သည်။
2. **Reference အခြေပြု ဖတ်ခြင်း။** ဒီဇိုင်း အသံဖိုင်ကို engine ၏ input **နှစ်ခုလုံး** (`audio` နှင့် `voice_ref`) သို့ ၎င်း၏
   စာသားမှတ်တမ်း (`reference_text`) နှင့် ဖတ်ရမည့် စာသားအသစ်တို့နှင့်အတူ seed တူဖြင့် ပေးပို့သည်။ အသံကို ဖော်ပြချက်က မဟုတ်ဘဲ
   အသံဖိုင်က သယ်ဆောင်သောကြောင့် စာသားတစ်ခုမှ တစ်ခုသို့ မလွဲသွားပါ။ စာသားကို စာကြောင်းတစ်ကြောင်းချင်း ဖတ်သည်။
3. အရည်အသွေးသည် ပုံသေ ဖြစ်သည်- diffusion step 16 ဆင့်၊ CFG 2.0။ seed သည် အရည်အသွေး ချိန်ညှိခလုတ် မဟုတ်ပါ။
4. **စကားလုံးအချိန်နှင့် အကြိမ်တိုင်း တူညီသောအသံ။** ဖတ်နေစဉ် engine ကိုယ်တိုင်က စကားလုံးတစ်လုံးချင်း ဘယ်မှာစပြီး ဘယ်မှာဆုံးသည်ကို ပြောပြသည် (patch 0002၊ မော်ဒယ်အပို မလိုပါ)။ အချိန်များကို `kelimeler.json` တွင် ရေးပြီး စာကြောင်းများကို ဖြတ်ညှိကာ စာကြောင်းကြား ကွာဟချက်သည် ရပ်နားချိန်ဆက်တင်နှင့် ညီစေသည်။ CTC forced alignment (CTC = 100%) နှင့် နှိုင်းယှဉ်သော တိကျမှု- 89.66% (တူရကီ၊ အသံ 12 မျိုး၊ ဆက်တင် `kelime_zamani` ပုံသေဖွင့်ထားသည်)။ patch 0003 ဖြင့် seed တူလျှင် အကြိမ်တိုင်း byte တိုင်းတူသော အသံကို ရသည်။

မူလ ဒီဇိုင်း အသံဖိုင်သည် အသံ၏ တစ်ကြိမ်သာ ထွက်သော နမူနာ ဖြစ်သည်၊ နောက်ပိုင်း ဖတ်ခြင်း မည်သည့်အကြိမ်မျှ ၎င်းနှင့် အတိအကျ
မတူပါ။ နောက်ပိုင်း ဖတ်ခြင်းတိုင်းတွင် ကြားရသည်မှာ အဆင့် 2 ဖြစ်သည်- reference အဖြစ် ဒီဇိုင်း အသံဖိုင်နှင့် ပုံစံ၏ ကိုယ်ပိုင် seed။
ထို့ကြောင့် web UI သည် ဒီဇိုင်းပြီးပြီးချင်း အဆင့် 2 ကို လုပ်ပြီး နှစ်ခုလုံးကို ပုံစံကတ်ပေါ်တွင် ပြသည်။

engine သည် ကျွန်ုပ်တို့၏ patch (`patches/`) ပါသော audio.cpp v0.7.2 ဖြစ်ပြီး model သည် VoxCPM2 Q8_0 GGUF ဖြစ်သည်။ VRAM
အမြင့်ဆုံး ≈ 2.8 GB၊ GTX 1050 Ti ပေါ်တွင် စကားပြော 1 s လျှင် တွက်ချက်ချိန် ခန့်မှန်းခြေ 2 s။ အသေးစိတ်နှင့် တိုင်းတာချက်များ-
[docs/4gb.md](docs/4gb.md)။

## ပါဝင်သော အသံများ (`hazir_sesler/`)

ဆယ့်လေးမျိုးလုံးကို ၎င်းတို့၏ `ses.json` တွင် သိမ်းထားသော prompt များမှ ဒီဇိုင်းဆွဲထားခြင်း ဖြစ်သည်၊ မည်သည့်အသံကိုမျှ
အသံဖိုင်မှ ပုံတူကူးထားခြင်း မရှိပါ (ပုံတူကူးခြင်းသည် ခွင့်ပြုချက် လိုအပ်သော သီးခြား *အသံပုံတူကူးခြင်း* tab ဖြစ်သည်)။

| အသံ | အတိုချုပ် ဖော်ပြချက် | နားထောင်ရန် |
|---|---|---|
| `belgesel_hanim` | အသက်ငါးဆယ်အရွယ် ရင့်ကျက်သော အမျိုးသမီး၊ နက်ရှိုင်းနွေးထွေးသော alto၊ တည်ငြိမ်သော မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ | [နမူနာ](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [reference](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | နက်ရှိုင်း၍ အားကောင်းပြီး လျှို့ဝှက်ဆန်းကြယ်သော အမျိုးသား ဇာတ်ကြောင်းပြောသူ | [နမူနာ](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | အသက်ခုနစ်ဆယ်ခန့် အတွေ့အကြုံရင့် သတင်းကြေညာသူ၊ တည်ငြိမ်ပြီး အာဏာရှိသော | [နမူနာ](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [reference](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | အသက်သုံးဆယ်အရွယ် ဆွဲဆောင်မှုရှိသော ညနေသတင်း ကြေညာသူ အမျိုးသမီး၊ ကတ္တီပါကဲ့သို့ နူးညံ့ပြီး ခံစားချက်ပြည့် | [နမူနာ](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [reference](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | ပုံပြင်ထဲက စုန်းမ- နိမ့်သော၊ နှာသံ အနည်းငယ်ပါသော၊ ပါးနပ်စွာ ချိုသော | [နမူနာ](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [reference](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | ထူးခြားစွာ နက်ရှိုင်း၍ ပြည့်သိပ်ပြီး အမိန့်ပေးသံရှိသော အမျိုးသား ဇာတ်ကြောင်းပြောသူ | [နမူနာ](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [reference](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | ပညာရှိ အဘိုးအို၊ နက်ရှိုင်း၍ ပဲ့တင်ထပ်သော၊ အနည်းငယ် လျှို့ဝှက်ဆန်းကြယ်သော | [နမူနာ](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [reference](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | အသက်ငါးဆယ်အရွယ် အင်္ဂလိပ် မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (General American)၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | အသက်ငါးဆယ်အရွယ် ပြင်သစ် မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (ပဲရစ်)၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | အသက်ငါးဆယ်အရွယ် ဂျာမန် မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (Hochdeutsch)၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | အသက်ငါးဆယ်အရွယ် စပိန် မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (Castilian (မက်ဒရစ်))၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | အသက်ငါးဆယ်အရွယ် ရုရှား မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (မော်စကို)၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | အသက်ငါးဆယ်အရွယ် တရုတ် (မန်ဒရင်း) မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (ပေကျင်း Putonghua)၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | အသက်ငါးဆယ်အရွယ် ဂျပန် မိခင်ဘာသာစကားပြော အမျိုးသား မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ (တိုကျို စံ)၊ နက်ရှိုင်း၊ တည်ငြိမ်၊ နွေးထွေး | [နမူနာ](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [reference](hazir_sesler/anlatici_ja/referans.flac) |

folder တစ်ခုစီတွင်- `referans.flac` (အရည်အသွေး မကျသော ဒီဇိုင်း အသံဖိုင်)၊ `ses.json` (prompt၊ စာသားမှတ်တမ်း၊ ဒီဇိုင်း seed၊
ဖတ်ခြင်း seed၊ ဖော်ပြချက်၊ ဇာတ်ကြောင်းပြောသူများအတွက် `dil` = ဘာသာစကား)၊ `ornek_okuma.mp3` (+ ၎င်း၏ စာသား)။ တိုက်ရိုက်
အသုံးပြုပါ- `--ses hazir/<name>`။ ဇာတ်ကြောင်းပြောသူများ၏ reference အသံဖိုင်များသည် တိုသည် (5.6-10 s)၊ ၎င်းတို့၏ နမူနာများသည်
ကပ္ပဒိုးကီးယား ဇာတ်ညွှန်း၏ ပထမ စာကြောင်း သုံးကြောင်း ဖြစ်ပြီး ထုတ်လုပ်မှု ဖတ်ခြင်း အပြည့်အစုံမှ ဖြတ်ယူထားခြင်း ဖြစ်သည်။

## အမြန် ထည့်သွင်းခြင်း၊ compiler မလိုပါ (Windows 10/11, NVIDIA GPU ≥ 4 GB)

ကြိုတင်လိုအပ်ချက်များ- NVIDIA driver ≥ 570 နှင့် 64-bit Python 3.10-3.13 (`winget install Python.Python.3.12`)။ အခြား
ဘာမျှ မလိုပါ- Visual Studio မလို၊ CUDA installer မလို။ သင့်တွင် မည်သည့်ကတ် ရှိသည်ကို မသေချာဘူးလား။ PowerShell တွင် `nvidia-smi`
ကို run ပါ- GPU အမည်၊ driver ဗားရှင်းနှင့် memory ကို ပြပေးသည်။ NVIDIA ကတ် မရှိဘူးလား။ အောက်ရှိ "AMD / Intel" ကို ကြည့်ပါ။

[Git](https://git-scm.com/download/win) ဖြင့်-

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Git မပါဘဲ- ဤစာမျက်နှာတွင် **Code → Download ZIP** ကို နှိပ်ပါ၊ ဖြည်ပါ၊ ဖြည်ပြီးသော
`voxcpm2-turkce-ses-tasarimi-main` folder ကို ဖွင့်ပါ၊ Explorer ၏ လိပ်စာဘားတွင် `powershell` ဟု ရိုက်ပြီး Enter နှိပ်ပါ၊
ထို့နောက် အထက်ပါ နောက်ဆုံး စာကြောင်းကို run ပါ။ Git ကို source မှ build လုပ်သော နည်းလမ်းအတွက်သာ လိုအပ်သည်။

`-ExecutionPolicy Bypass` သည် ဤ process တစ်ခုတည်းကိုသာ သက်ရောက်ပြီး system setting မည်သည့်အရာကိုမျှ မပြောင်းလဲပါ၊ မည်သည့်
installer script ကဲ့သို့ပင် `scripts\kur.ps1` ကို run မီ ဖတ်ကြည့်ပါ။ command တစ်ကြောင်း၊ ~10 မိနစ်၊ ~3.7 GB ဒေါင်းလုဒ်၊ အားလုံး
sha256 ဖြင့် စစ်ဆေးပြီး- model (2.95 GB)၊ portable zip အဖြစ် CUDA 12.8 runtime DLL များ (system ထည့်သွင်းခြင်း မရှိ၊ PATH
မထိ)၊ Releases စာမျက်နှာမှ **ကြိုတင် build လုပ်ထားသော engine**၊ Python package နှစ်ခုပါသော `.venv`၊ `ayarlar.json` နှင့်
နောက်ဆုံး GPU စစ်ဆေးမှု (`KONTROL_OK`)။ မအောင်မြင်မှု တစ်ခုခု ဖြစ်ပြီးနောက် ထပ် run ပါ၊ စစ်ဆေးပြီးသော ဖိုင်များကို ကျော်သွားမည်။
ထို့နောက် web UI ကို စတင်ပါ- repo folder ရှိ **`baslat.bat`** ကို နှစ်ချက်နှိပ်ပါ။ ၎င်းက UI ကို စတင်ပြီး အသင့်ဖြစ်သည့်အခါ
browser တွင် **http://127.0.0.1:8765/** ကို ဖွင့်ပေးသည်၊ ရပ်ရန် အမည်း window ကို ပိတ်ပါ (သို့မဟုတ် ထိုနေရာတွင် Ctrl+C နှိပ်ပါ)။
PowerShell မှလည်း အလားတူ-

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
ထို့နောက် **http://127.0.0.1:8765/** ကို ကိုယ်တိုင် ဖွင့်ပါ (ဤနည်းဖြင့် စတင်လျှင် UI က browser ကို မဖွင့်ပေးပါ၊ localhost
တွင်သာ နားထောင်သည်)။

> **release zip ထဲရှိ `audiocpp_cli.exe` ကို နှစ်ချက်နှိပ်ရန် မရည်ရွယ်ပါ။** ၎င်းသည် ဘေးတွင် CUDA DLL များနှင့် model လိုအပ်သော
> command-line engine ဖြစ်သည်၊ `kur.ps1` က အားလုံးကို နေရာချပေးပြီး Python package က ၎င်းကို မောင်းနှင်သည်။ နှစ်ချက်နှိပ်လျှင်
> "cudart64_12.dll not found" ကိုသာ ပြလိမ့်မည်။

**ပံ့ပိုးသော GPU များ (release v0.1.1)-** GTX 10xx (sm_61)၊ RTX 20xx (sm_75)၊ RTX 30xx (sm_86)၊ RTX 40xx (sm_89) နှင့်
RTX 50xx (sm_120a) အတွက် native code၊ Pascal နှင့်အထက် အခြား CUDA GPU မည်သည့်ကတ်မဆို ထည့်သွင်းထားသော PTX ကို driver မှတစ်ဆင့်
run သည် (ပထမဆုံး စတင်ချိန် ပိုနှေးသည်)။ Maxwell (GTX 9xx) နှင့် ၎င်းထက်ဟောင်းသော ကတ်များကို CUDA 12.8 မပံ့ပိုးပါ။ ကျွန်ုပ်တို့က
GTX 1050 Ti 4 GB ပေါ်တွင် စမ်းသပ်ထားသည် (Windows ပေါ်ရှိ Docker Desktop/WSL2 မှတစ်ဆင့်လည်း၊ CLI သာ)၊ @mslmyilmaz5 (#15) က
တိုင်းတာထားသည်- RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (အသေးစိတ် [docs/linux.md](docs/linux.md) တွင်)။ အခြား
ကတ်များမှ ရလဒ်များကို [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) တွင် ကြိုဆိုပါသည်။

**AMD / Intel (စမ်းသပ်ဆဲ)-** သီးခြား Vulkan engine zip (`...-win64-vulkan.zip`, CUDA မပါ) ကို
`scripts\kur.ps1 -Kok C:\vox -Vulkan` ဖြင့် ထည့်သွင်းသည်။ ၎င်းကို ကျွန်ုပ်တို့၏ NVIDIA ကတ်ပေါ်တွင် Vulkan backend မှတစ်ဆင့်သာ
စစ်ဆေးထားသည် (ထိုနေရာတွင် CUDA ထက် နှေးသော်လည်း seed တူလျှင် အသံတူ ထွက်သည်၊ ထိုတိုင်းတာချက်ကို disk က အခြားအလုပ်ဖြင့်
အလုပ်များနေစဉ် ယူခဲ့သဖြင့် သန့်ရှင်းသော အမြန်နှုန်း နှိုင်းယှဉ်ချက် မရသေးပါ) နှင့် AMD သို့မဟုတ် Intel hardware ပေါ်တွင်
ကျွန်ုပ်တို့ကိုယ်တိုင် စမ်းသပ်ထားခြင်း **မရှိပါ**- စမ်းကြည့်ပါက ရလဒ်ကို Discussions တွင် တင်ပေးပါ။ Vulkan device တစ်ခုထက်ပို
ရှိလျှင် (integrated + discrete) installer က discrete GPU ၏ index ကို `ayarlar.json` ထဲသို့ `cihaz` အဖြစ် ရေးသည်။

**မှတ်ချက်-** Vulkan ပံ့ပိုးမှုသည် လောလောဆယ် စမ်းသပ်ဆဲ ဖြစ်သည်။ GTX 1050 Ti ပေါ်တွင် အောင်မြင်စွာ build လုပ်ပြီး စမ်းသပ်ထားသည်။
ပြင်ပ အသုံးပြုသူတစ်ဦး (mitra_tr) က AMD 6900 XT ပေါ်တွင်လည်း run နိုင်ကြောင်း အစီရင်ခံထားသည်။ AMD/Intel ကတ်များပေါ်တွင်
ပိုမိုကျယ်ပြန့်သော စမ်းသပ်မှုများ လိုအပ်နေဆဲ ဖြစ်သည်။

**အသိုင်းအဝိုင်း စမ်းသပ်ချက် (AMD):** @mitraTR သည် Windows 11 ပေါ်ရှိ AMD Radeon RX 6900 XT တွင် Vulkan ဖြင့် v0.1.1 ကို လည်ပတ်ခဲ့သည်- ထည့်သွင်းခြင်း၊ အသံဒီဇိုင်း၊ ဖတ်ခြင်း၊ ဝဘ်မျက်နှာပြင်နှင့် စမ်းသပ်ချက်များ အားလုံး အလုပ်လုပ်ခဲ့သည်။ စကား 1 စက္ကန့်အတွက် တွက်ချက်ချိန် 0.8-0.9 စက္ကန့်ခန့် ကြာသည် ([#6 ရှိ အစီရင်ခံစာ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655))။ လမ်းကြောင်းတွင် ASCII စာလုံးများသာ ပါသော တိုတောင်းသည့် ဖိုင်တွဲတွင် ထည့်သွင်းပါ (ဥပမာ `C:\vox`)- Windows တွင် မြန်မာစာ သို့မဟုတ် ASCII မဟုတ်သော စာလုံးပါသည့် လမ်းကြောင်းများကို အင်ဂျင်က မဖွင့်နိုင်ပါ။ ယခုအထိ အစီရင်ခံစာများ အားလုံး- [စမ်းသပ်ပြီး ဟာ့ဒ်ဝဲ](docs/donanim_testleri.md)။

### အခြားနည်းလမ်း- engine ကို source မှ build လုပ်ခြင်း

"Desktop development with C++" (C++ CMake tools အပါအဝင်) ပါသော Visual Studio 2022 Build Tools လိုအပ်သည်၊ ~7 GB။ ထို့နောက်-

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
၎င်းက nvcc ကိုလည်း ဒေါင်းလုဒ်လုပ်သည်၊ audio.cpp v0.7.2 source ကို ယူသည်၊ `patches/0001-voxcpm2-4gb-ve-hiz.patch` ကို
အသုံးချပြီး သင့် GPU အတွက် build လုပ်သည် (`-Mimari native`, default၊ သို့မဟုတ် ဥပမာ `-Mimari 61`)၊ ~15-25 မိနစ်။ root ကို
တိုတို ထားပါ (`C:\vox`)- လမ်းကြောင်း ရှည်လျှင် nvcc မအောင်မြင်ပါ။ စစ်ဆေးချက်များပါသော အဆင့်ဆင့် လမ်းညွှန်- [AGENTS.md](AGENTS.md)။

### အဖြစ်များသော ထည့်သွင်းမှု ပြဿနာများ

| သင်မြင်ရသည် | အဓိပ္ပာယ်နှင့် လုပ်ရမည့်အရာ |
|---|---|
| exe ကို နှစ်ချက်နှိပ်ပြီးနောက် `cudart64_12.dll not found` | engine ကို လက်ဖြင့် စတင်ရန် မရည်ရွယ်ပါ။ အထက်ပါ `kur.ps1` command ကို run ပြီး web UI ကို စတင်ပါ။ |
| `64-bit Python 3.10+ bulunamadı` (Python မတွေ့ပါ) | Python ကို ထည့်သွင်းပါ (`winget install Python.Python.3.12`)၊ PowerShell ကို ပိတ်ပြီး အသစ်ဖွင့်ကာ command တူကို ထပ် run ပါ။ |
| `motor ekran kartını görmedi` (engine က GPU ကို မမြင်ပါ) | NVIDIA driver ကို 570 သို့မဟုတ် ပိုသစ်သော ဗားရှင်းသို့ update လုပ်ပါ၊ `nvidia-smi` run နိုင်ကြောင်း စစ်ပါ။ |
| `indirme başarısız` / `sha256 tutmadı` (ဒေါင်းလုဒ် မအောင်မြင် / checksum မကိုက်ညီ) | များသောအားဖြင့် ဒေါင်းလုဒ် ပြတ်တောက်ခြင်း ဖြစ်သည်။ command တူကို ထပ် run ပါ၊ စစ်ဆေးပြီးသော ဖိုင်များကို ကျော်သွားမည်။ |
| build လမ်းကြောင်း- `nvcc` မအောင်မြင်ပါ | ထည့်သွင်းမည့် root ကို တိုတို ထားပါ (`-Kok C:\vox`)။ |
| စာမျက်နှာ မပွင့်ပါ | UI ကို `baslat.bat` ဖြင့် စတင်ပါ၊ သို့မဟုတ် http://127.0.0.1:8765/ ကို ကိုယ်တိုင် ဖွင့်ပါ။ port အသုံးပြုနေပြီလား။ `ayarlar.json` ထဲရှိ `"port"` ကို ပြောင်းပါ။ |

ပြဿနာ ရှိပါသလား။ [Discussions (မေးဖြေ)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) သို့မဟုတ်
[ထည့်သွင်းမှု issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
ကို သင့် GPU၊ Windows ဗားရှင်း၊ run ခဲ့သော command နှင့် ၎င်း၏ နောက်ဆုံး စာကြောင်းများနှင့်အတူ ဖွင့်ပါ။

## အသုံးပြုပုံ

Command line-
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
စာသား စည်းမျဉ်းများ- ဂဏန်းများကို စကားလုံးဖြင့် ရေးပါ၊ မျက်တောင်အဖွင့်အပိတ် မသုံးပါနှင့် (tool က ဂဏန်းနှင့် quote များကို
လက်မခံပါ)၊ တစ်ကြောင်းလျှင် စာကြောင်းတစ်ကြောင်း၊ တစ်ကြောင်းလျှင် စာလုံး ≤ 2000။ စာကြောင်းနောက်ရှိ ရပ်နားချိန်- `|| bagli`
0.25 s၊ `|| normal` 0.5 s၊ `|| paragraf` 1 s၊ `|| agir` 1.5 s သို့မဟုတ် ကိုယ်ပိုင် အရှည် `|| 0,8` (0-5 s၊ ဤ marker ၏
ဂဏန်းများကို ခွင့်ပြုသည်)။ `ayarlar/okunus_sozlugu.tsv` က တူရကီ စာသားထဲရှိ နိုင်ငံခြား စကားလုံးများ၏ အသံထွက်ကို ပြင်ပေးသည်။
ဘာသာစကားကို စာသားမှ ခွဲခြားသိရှိသည် (တူရကီ အက္ခရာများ၊ စာရေးစနစ်၊ အသုံးများသော စကားလုံးများ၊ မသေချာလျှင် အသံကတ်၏ `dil`၊
`--dil <code>` သည် မဖြစ်မနေ မလိုပါ)။ တူရကီ မဟုတ်သော စာသားအတွက် ထိုနေရာတွင် apostrophe ကို ခွင့်ပြုသည်၊ တူရကီ အဘိဓာန်ကို
ကျော်သည်၊ ဂဏန်းများကိုမူ ဆက်လက် လက်မခံပါ။ ဖတ်စဉ် `speed gate: satır [...]` ကို ပြလျှင် ထိုစာကြောင်းများကို နားထောင်ကြည့်ပါ။

### Web UI

local တွင်သာ (127.0.0.1)- `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → http://127.0.0.1:8765/ ကို ကိုယ်တိုင် ဖွင့်ပါ
(အခြား port- `--port 8800`)၊ သို့မဟုတ် `baslat.bat` ကို နှစ်ချက်နှိပ်ပါ။ server ကို Ctrl+C ဖြင့် ရပ်ပါ။ tab သုံးခု- *အသံ ဒီဇိုင်းဆွဲရန်*၊
*ဤအသံဖြင့် ဖတ်ရန်*၊ *အသံပုံတူကူးခြင်း*။ ပုံမှန် လမ်းကြောင်း- *ဒီဇိုင်းဆွဲမည်* → ပုံစံများကို နားထောင်ပါ → *ဖတ်ရန်စာရင်းထဲ ထည့်ရန်* →
*ဤအသံဖြင့် ဖတ်မည်* → ဒေါင်းလုဒ်။ သို့မဟုတ် အသံ menu မှ အသင့်ပါသော အသံတစ်ခုကို ရွေးပြီး ဖတ်ပါ။

- **header ရှိ ဗားရှင်း။** သေးငယ်ပြီး မှိန်ဖျော့သော `v0.2.0 · <short commit>` (track လုပ်ထားသော ဖိုင်များတွင် commit မလုပ်ရသေးသော
  ပြောင်းလဲမှု ရှိလျှင် `+` ပါသည်၊ git မရှိလျှင် ဗားရှင်းသာ)၊ ထို့ကြောင့် screenshot နှင့် ဗီဒီယိုများတွင် အသုံးပြုခဲ့သော ဗားရှင်းကို
  မြင်ရသည်။
- **ပုံစံကတ်တိုင်းတွင် အသံနှစ်မျိုး။** အပေါ်တွင် မီးခိုးရောင်ဖြင့် *မူလဒီဇိုင်းအသံ*- တစ်ကြိမ်သာ ထုတ်ပြီး နောက်ထပ် အတူတူ
  မထွက်တော့ပါ။ ၎င်း၏အောက်တွင် လိမ္မော်ရောင် ဘောင်ထဲ၌ *↻ ဤအသံကို အမြဲကြားရမည်*- ပုံစံ၏ ကိုယ်ပိုင် seed (ကတ်ပေါ်တွင် ပြထားသည်)
  ဖြင့် ဒီဇိုင်း အသံဖိုင်ကို reference အဖြစ် ပြန်ဖတ်ထားခြင်း ဖြစ်သည်။ နောက်ပိုင်း ဖတ်ခြင်းတိုင်းတွင် အသံ ဤသို့ ထွက်သည်။
  ၎င်း၏အောက်တွင် *ဤအသံဖြင့် ဖတ်မည်* နှင့် *ဖတ်ရန်စာရင်းထဲ ထည့်ရန်* ရှိသည်။ *ဒီဇိုင်းဆွဲမည်* ကို တစ်ချက်နှိပ်ရုံဖြင့် နှစ်ခုလုံး
  လုပ်သည်- ပုံစံတိုင်းကို ဒီဇိုင်းဆွဲပြီးနောက် သင့်စာသားကို အမြဲကြားရမည့် အသံတစ်ခုစီဖြင့် ဖတ်သည်၊ progress bar တစ်ခုတည်းက
  အဆင့်နှစ်ဆင့်လုံးကို ရေတွက်သည်။ ပုံစံ folder တွင် `dinleme.wav` ရရှိသည်။ ထိုဖတ်ခြင်း စောစီးစွာ ရပ်သွားလျှင် ဒီဇိုင်းကို
  ထိန်းသိမ်းထားပြီး ကတ်ပေါ်တွင် မှတ်ချက်တစ်ခု ပြသည်။
- **"နားထောင်ချင်သော စာသား" window။** *အသံ ဒီဇိုင်းဆွဲရန်* တွင် *↻ နားထောင်ချင်သော စာသား* box သည် အမြဲကြားရမည့် အသံတစ်ခုစီ
  ဖတ်မည့် စာသားကို ထိန်းထားသည် (အလွတ်ထားလျှင် နမူနာ စာကြောင်းကို ဖတ်သည်)။ ၎င်းကို နှိပ်လျှင် ဖတ်ရန် မှတ်စုစာအုပ်ကို window
  တစ်ခုအဖြစ် ဖွင့်ပေးသည်- စာကြောင်း နံပါတ်များ၊ စာကြောင်း menu၊ ရပ်နားချိန် band များ။ *အိုကေ* က စာသားနှင့် ၎င်း၏ ရပ်နားချိန်များကို
  box ထဲသို့ ပြန်ရေးသည်၊ *မလုပ်တော့ပါ* သို့မဟုတ် Esc က ဘာမျှ မပြောင်းလဲပါ။ ဖတ်ရန် tab သည် ၎င်း၏ ကိုယ်ပိုင် စာသားကို ထိန်းထားသည်။
- **ဖတ်ရန် မှတ်စုစာအုပ်။** တစ်ကြောင်းလျှင် စာကြောင်းတစ်ကြောင်း။ စာကြောင်း menu အတွက် စာကြောင်း နံပါတ်ကို နှိပ်ပါ (အပေါ် သို့မဟုတ်
  အောက်သို့ ရွှေ့ခြင်း၊ နေရာတစ်ခုသို့ ရွှေ့ခြင်း၊ ပွားခြင်း၊ ဖျက်ခြင်း၊ Alt+↑/↓၊ Alt+Shift+↓ သို့မဟုတ် နံပါတ်ကို ဆွဲရွှေ့ခြင်း၊
  Ctrl+Z က စာသားနှင့် ရပ်နားချိန်များကို တစ်ပြိုင်နက် ပြန်ဖျက်သည်)။ စာကြောင်းနှစ်ကြောင်းကြားရှိ band ပါးကို နှိပ်၍ ရပ်နားချိန်ကို
  ရွေးပါ (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 s သို့မဟုတ် gear ဖြင့် ကိုယ်ပိုင် 0-5 s)၊ စာပိုဒ် (1 s) အတွက် Enter ကို
  နှစ်ချက်နှိပ်ပါ၊ စာကြောင်းအလွတ်များသည် ရပ်နားချိန် band များ ဖြစ်လာသည်။ ရလဒ် ဖွင့်နေစဉ် ဖတ်နေသော စာကြောင်းက လင်းလာပြီး
  မြင်ကွင်းထဲသို့ scroll ဖြစ်လာသည်၊ စာကြောင်း menu ရှိ *▶ ဤနေရာမှ နားထောင်ရန်* က ထိုစာကြောင်းမှ စ၍ ဖွင့်ပေးသည်။ စာသားနှင့်
  ၎င်း၏ ရပ်နားချိန်များသည် စာမျက်နှာ reload လုပ်သော်လည်း ကျန်ရှိနေသည် (browser storage)။
- **မူကြမ်းများ။** *📄 မူကြမ်းများ* ခလုတ်သည် မှတ်စုစာအုပ် နှစ်ခုလုံးတွင် ရှိသည် (ဖတ်ရန် tab နှင့် window)။ လက်ရှိ စာသားကို
  ၎င်း၏ ရပ်နားချိန်များနှင့်အတူ မူကြမ်းအဖြစ် သိမ်းပါ၊ တစ်ချက်နှိပ်၍ မူကြမ်းတစ်ခုကို ဖွင့်ပါ (Ctrl+Z က ပြန်ဖျက်သည်)၊ ⋯ ဖြင့်
  ထပ်ရေးခြင်း၊ အမည်ပြောင်းခြင်း သို့မဟုတ် ဖျက်ခြင်း လုပ်ပါ။ မူကြမ်းများကို repository ထဲတွင် ဘယ်တော့မှ မသိမ်းဘဲ
  `sesler/taslaklar.json` တွင် သိမ်းသည်။
- **ဖတ်ရန်စာရင်းနှင့် အသံ menu။** ပုံစံကတ်ပေါ်ရှိ *ဖတ်ရန်စာရင်းထဲ ထည့်ရန်* က အမည် box ကို ဖွင့်သည်- ပုံစံကို ကိုယ်ပိုင်အမည် ပေးပြီး
  ✓ ဖြင့် ထည့်ပါ။ *ဖန်တီးမှုအမည်* သည် ထိုကြိမ်၏ ပုံစံတိုင်းတွင် ဆက်ရှိနေသည်။ *ဤအသံဖြင့် ဖတ်ရန်* တွင် အသံ ခလုတ် (အလံ + အမည်)
  က အသံ menu ကို ဖွင့်သည်- အပေါ်ဆုံးတွင် *ကျွန်ုပ်၏ ဖတ်ရန်စာရင်း*၊ ထို့နောက် အလံများပါသော အသင့်ပါသော အသံများ (interface
  ဘာသာစကား အရင်)။ အတန်းတိုင်းတွင် ▶ နားထောင်ရန် (ရှိလျှင် အမြဲကြားရမည့် အသံ)၊ နှလုံး (ထည့်ရန် သို့မဟုတ် ဖယ်ရန်) နှင့် ⋯ ပါသည်၊
  ↑/↓ နှင့် Enter က ရွေးသည်၊ Esc က ပိတ်သည်၊ နောက်ဆုံး အသံကို မှတ်ထားသည်။ စာရင်းသည် repository ပြင်ပရှိ
  `sesler/okuma_listesi.json` တွင် ရှိပြီး ပြန်စတင်သော်လည်း ကျန်ရှိနေသည်။
- **အသံများကို စီမံခြင်း။** ⋯ menu (အသံ menu အတန်း သို့မဟုတ် ပုံစံကတ်) တွင် *ဤအသံဖြင့် ဖတ်မည်*၊ စာရင်းထဲ ထည့်ခြင်း သို့မဟုတ်
  ဖယ်ခြင်း၊ *အမည်ပြောင်းရန်* (အမည် အလွတ်က မူလအမည်ကို ပြန်ယူသည်၊ *မူလအမည်သို့ ပြန်ရန်*)၊ ဒီဇိုင်းဆွဲထားသော အသံများအတွက်
  *ဖျက်ရန်* နှင့် အသင့်ပါသော အသံများအတွက် *ဖျောက်ရန်* ပါသည်၊ နှစ်ခုလုံး အရင် မေးသည်။ ဖျက်ထားသော အသံသည် `sesler/_cop/` သို့
  ရွှေ့သွားသည်၊ ဖျောက်ခြင်းသည် repository ဖိုင်များကို ဘယ်တော့မှ မထိပါ။ အသံ menu အောက်ခြေရှိ *ဖျောက်ထားသော နှင့် ဖျက်ထားသော
  အသံများ (N)* တွင် *ပြန်ယူရန်* ရှိသည်။ စိတ်ကြိုက် အမည်များနှင့် ဖျောက်ထားသော အသံများကို `sesler/yerel_katman.json` တွင်
  သိမ်းသည်။ အမည်ပြောင်းထားသော အသံသည် ၎င်း၏ မူလကို မီးခိုးရောင်ဖြင့် ပြသည် (*ဖန်တီးမှုအမည် · ပုံစံ N*)၊ ⋯ → *ဖန်တီးမှုသို့
  သွားရန်* က ၎င်း၏ ဒီဇိုင်းကို ဖွင့်ပေးသည်။
- **Shortcut များနှင့် ဖိုင်များ။** Ctrl+Enter (Mac တွင် ⌘+Enter) က ဖွင့်ထားသော tab ပေါ်တွင် *ဒီဇိုင်းဆွဲမည်* သို့မဟုတ် *ဤအသံဖြင့်
  ဖတ်မည်* ကို စတင်သည်။ progress bar သည် သင့်စက်ပေါ်ရှိ ယခင်အလုပ်များမှ သင်ယူထားသော ခန့်မှန်းချက်ဖြင့် *ကြာချိန် / ~စုစုပေါင်း*
  ကို ပြသည်။ ဒေါင်းလုဒ်ဖိုင်ကို အသံအမည်နှင့် အချိန်ဖြင့် အမည်ပေးသည် (`Voice_Name_2026-11-02_0152.wav`)။

**အသံပုံတူကူးခြင်း (သင့်ကိုယ်ပိုင်အသံ သို့မဟုတ် ခွင့်ပြုချက်ရှိသော အသံ)။** UI ၏ *အသံပုံတူကူးခြင်း* tab တွင် သင့်အသံဖိုင်
(wav/mp3/flac/ogg၊ သန့်ရှင်းသော စကားပြော 5-30 s ကို အကြံပြုသည်၊ 3 s အောက်ကို ပယ်ချပြီး 36 s ကျော်ကို ဖြတ်တောက်သည်)၊ ၎င်း၏
တိကျသော စာသားမှတ်တမ်းနှင့် ဖတ်မည့် စာသားကို ထည့်ပါ။ "ဤအသံသည် ကျွန်ုပ်၏အသံ ဖြစ်သည် သို့မဟုတ် ပိုင်ရှင်၏ ရှင်းလင်းသော
ခွင့်ပြုချက် ကျွန်ုပ်တွင် ရှိသည်" ကို အမှန်ခြစ်မချမချင်း ခလုတ်ကို ပိတ်ထားသည်။ အသံဖိုင်သည် local server (127.0.0.1) သို့သာ
သွားပြီး ၎င်း၏ reference encoding နှင့်အတူ ယာယီ folder တစ်ခုတွင် ဆောင်ရွက်သည်၊ အလုပ်ပြီးဆုံးသည့်အခါ မအောင်မြင်လျှင်ပင်
ထို folder ကို ဖျက်သည်၊ network မှတစ်ဆင့် ဘာမျှ မပို့ပါ။ synthetic ရလဒ်ကိုသာ သိမ်းထားသည် (UI- `sesler/_okumalar/<job>/`၊
CLI- `--cikti`)။ ရလဒ်သည် "synthetic" tag ပါသော `klon_synthetic.wav` ဖြစ်သည်၊ မျှဝေသည့်အခါ AI ဖြင့် ထုတ်လုပ်ထားကြောင်း
ဖော်ပြပါ။ CLI- `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## မေးလေ့ရှိသော မေးခွန်းများ

**Model လား engine လား။ ဘယ်ဟာက ဘာလဲ။** VoxCPM2 (OpenBMB) သည် *model* ဖြစ်သည်- စာသားကို စကားပြောအဖြစ် ပြောင်းပေးသော
parameter 2 billion ပါ network။ audio.cpp သည် *engine* ဖြစ်သည်- model ကို သင့် GPU ပေါ်တွင် run ပေးသော C++/CUDA ပရိုဂရမ်
(`audiocpp_cli.exe`)။ ကျွန်ုပ်တို့၏ patch သည် model ကို မဟုတ်ဘဲ engine ကို ပြောင်းလဲသည်- VoxCPM2 ကို 4 GB တွင် ဆံ့စေပြီး
seed တူလျှင် အကြိမ်တိုင်း အသံတူ ထွက်စေသည်။ ဤ repo ရှိ Python package သည် စာသားကို ပြင်ဆင်ခြင်း၊ engine ကို ခေါ်ခြင်းနှင့်
ဖိုင်များကို စုဆောင်းခြင်းသာ လုပ်သည်။

**ဘယ် GPU တွေလဲ။** အထက်ပါ "ပံ့ပိုးသော GPU များ" ကို ကြည့်ပါ- GTX 10xx နှင့်အထက် NVIDIA၊ VRAM 4 GB သို့မဟုတ် ပို၍၊ driver ≥ 570။
release တွင် sm_61/75/86/89/120a အတွက် native code ပါသည်၊ အခြား Pascal သို့မဟုတ် ပိုသစ်သော ကတ်များက ထည့်သွင်းထားသော PTX ကို
သုံးသည် (ပထမဆုံး စတင်ချိန် ပိုနှေးသည်)။ AMD/Intel- စမ်းသပ်ဆဲ Vulkan zip၊ `kur.ps1 -Vulkan`၊ ပြင်ပ အသုံးပြုသူတစ်ဦးက AMD 6900 XT
ပေါ်တွင် run နိုင်ကြောင်း အစီရင်ခံထားသော်လည်း AMD/Intel ပေါ်တွင် ပိုမိုကျယ်ပြန့်သော စမ်းသပ်မှု လိုအပ်နေဆဲ ဖြစ်သည် (အထက်ပါ
"AMD / Intel" ကို ကြည့်ပါ)။ CPU သီးသန့် (`ayarlar.json` ထဲတွင် `"backend": "cpu"`) run နိုင်သော်လည်း GTX 1050 Ti ထက် ~6×
နှေးသည် (engine တိုင်းတာချက်၊ စကားပြော 48 s အတွက် 535 s နှင့် 94 s)၊ ပံ့ပိုးသော နည်းလမ်း မဟုတ်ပါ။

**ဘယ်လောက် မြန်သလဲ။** GTX 1050 Ti 4 GB (i7-7700HQ) ပေါ်တွင် တိုင်းတာထားသည်- ဒီဇိုင်း ပုံစံတစ်ခု (≈ 25 s အသံဖိုင်) 55 s၊
အသံတစ်ခုလျှင် တစ်ကြိမ်သာ လုပ်ရသော ~50 s reference encoding (disk ပေါ်တွင် cache လုပ်ထားသည်) နှင့် batch တစ်ခုလျှင် model
load 10-20 s ပြီးနောက် ဖတ်ခြင်းသည် စကားပြော 1 s လျှင် တွက်ချက်ချိန် ≈ 2 s (real-time factor 1.9-2.8)၊ VRAM အမြင့်ဆုံး
2.6-2.9 GB။ ပိုသစ်သော ကတ်များ ပိုမြန်သည်၊ ကိန်းဂဏန်းများနှင့် နည်းလမ်း- [docs/4gb.md](docs/4gb.md)။

**အသံကို ပုံတူကူးနိုင်သလား။** အခြေခံ VoxCPM2 model သည် reference အသံဖိုင်မှ အသံကို တုပနိုင်ပြီး ပုံတူကူးခြင်း အပိုင်းက
ထိုစွမ်းရည်ကို အသုံးပြုသည်။ သင့်ကိုယ်ပိုင်အသံ သို့မဟုတ် အသံပိုင်ရှင်၏ ရှင်းလင်းသော ခွင့်ပြုချက်ဖြင့်သာ အသုံးပြုပါ၊ UI က
ထိုခွင့်ပြုချက်ကို အတည်ပြုရန် တောင်းဆိုသည်။ အသံ ဒီဇိုင်းသည် အသံဖိုင် မလိုပါ- အင်္ဂလိပ် သို့မဟုတ် တရုတ်လို စာသား ဖော်ပြချက်မှ
စတင်ပြီး ဒီဇိုင်းဆွဲထားသော အသံကို ဖတ်ရာတွင် သုံးသော "reference" သည် model ၏ ကိုယ်ပိုင် synthetic ဒီဇိုင်း အသံဖိုင် ဖြစ်သည်။
အခြားသူအဖြစ် ဟန်ဆောင်ခြင်း၊ လိမ်လည်ခြင်းနှင့် လှည့်ဖြားခြင်းကို တားမြစ်ထားသည်။ [ETHICS.md](ETHICS.md) ကို ကြည့်ပါ။
သင်ထုတ်ဝေသမျှကို AI ဖြင့် ထုတ်လုပ်ထားကြောင်း ဖော်ပြပါ။

**အသံ ဖော်ပြချက် ကောင်းကောင်း ဘယ်လို ရေးမလဲ။** အင်္ဂလိပ်လို စာကြောင်း 1-3 ကြောင်း- အသက်နှင့် ကျား/မ၊ အသံအရောင် (နက်/ကြည်လင်၊
နွေးထွေး၊ နှာသံ၊ အက်ကွဲ)၊ လေသံနှင့် အခန်းကဏ္ဍ (တည်ငြိမ်သော မှတ်တမ်းရုပ်ရှင် ဇာတ်ကြောင်းပြောသူ၊ တက်ကြွသော တင်ဆက်သူ)၊ အမြန်နှုန်း
(နှေး၊ ချိန်ဆ၍)၊ နှင့် "clean studio recording, no background noise"။ ဇာတ်ညွှန်း မဟုတ်ဘဲ ဖော်ပြချက်အဖြစ်သာ ထားပါ၊ ကွင်းစကွင်းပိတ်
မသုံးပါနှင့်။ ပုံစံ 3-5 ခု တောင်းပြီး နားထောင်ပါ- seed က အသံကို အများကြီး ပြောင်းလဲစေသည်။ ဖန်တီးမှု စာသားအတွက် အသံ၏
ဘာသာစကားဖြင့် သင်လိုချင်သော စိတ်ခံစားမှုရှိသော သဘာဝကျသည့် စာကြောင်း 1-3 ကြောင်း သုံးပါ (စကားပြော အများဆုံး ~30 s)။ ဖတ်သည့်အခါ
တစ်ကြောင်းလျှင် စာကြောင်းတစ်ကြောင်း၊ ရှည်သော စာကြောင်းများကို ခွဲပါ၊ ဂဏန်းများကို စကားလုံးဖြင့် ရေးပါ။

## ပါဝင်ကူညီခြင်း

ဘယ်က စရမလဲ မသိဘူးလား။ ဤ issue သေးသေး လေးခုသည် ကောင်းမွန်သော ပထမခြေလှမ်း ဖြစ်သည်-

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) သင့် GPU ပေါ်တွင် စမ်းပြီး ကတ်၊ driver နှင့် ကြာချိန်များကို အစီရင်ခံပါ
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel- စမ်းသပ်ဆဲ Vulkan build ကို စမ်းကြည့်ပါ
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) test set ထဲသို့ စာကြောင်းတစ်ကြောင်း ထည့်ပါ
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) သင် ဒီဇိုင်းဆွဲထားသော အသံကို ၎င်း၏ ဖော်ပြချက်နှင့် seed နှင့်အတူ မျှဝေပါ

**သင့်ဂရပ်ဖစ်ကတ်ကို စမ်းသပ်ပြီး အစီရင်ခံစာ ရေးပါ-** ကုဒ်ရေးတတ်ရန် မလိုပါ၊ [ဟာ့ဒ်ဝဲ စမ်းသပ်မှု အစီရင်ခံစာ ဖောင်](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml) ကို ဖြည့်ရုံသာ။ Intel ဂရပ်ဖစ်ကတ်မှ အစီရင်ခံစာ မရှိသေးပါ။

မျှဝေထားသော test set- [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt)၊ brand အသံ လမ်းညွှန်-
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md)၊ code ပို့နည်း- [CONTRIBUTING.md](CONTRIBUTING.md)။
ထည့်သွင်းမှု ပြဿနာများ- [issue ပုံစံ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)၊ မေးခွန်းများနှင့် ရလဒ်များ- [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)။
ပါဝင်သူတိုင်း [ကျင့်ဝတ်စည်းမျဉ်း](CODE_OF_CONDUCT.md) ကို လိုက်နာသည်- ကြင်နာပါ၊ အကြံပြုချက်ကို လုပ်ငန်းအပေါ်သာ ထားပါ။

## ပါဝင်ကူညီသူများ

- [@alexturkey](https://github.com/alexturkey)- ထိန်းသိမ်းသူ၊ code၊ အသင့်ပါသော အသံများ၊ စာရွက်စာတမ်းများ
- [@cayir21](https://github.com/cayir21)- macOS (Apple Silicon) Metal ပံ့ပိုးမှု၊ [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis)- CPU backend ပေါ်တွင် စာကြောင်းများစွာ ဖတ်ရာအတွက် စာကြောင်းအဆုံး (EOS) ပြင်ဆင်ချက်၊ [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5)- Ubuntu/Linux အတွက် စမ်းသပ် CUDA ထည့်သွင်းမှုနှင့် Docker ပံ့ပိုးမှု၊ [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

သင့်အမည်လည်း ဤနေရာတွင် ရှိသင့်သည်- သင့် GPU မှ စမ်းသပ်ရလဒ်၊ test set အတွက် စာကြောင်းတစ်ကြောင်း၊ သင် ဒီဇိုင်းဆွဲထားသော အသံ၊
ရှင်းလင်းသော bug report သို့မဟုတ် pull request အားလုံးကို ပါဝင်ကူညီမှုအဖြစ် ရေတွက်သည်။ စမ်းသုံးပြီး ပြန်လည် ရေးသားပေးသူ
အားလုံးကို ကျေးဇူးတင်ပါသည်။

## လိုင်စင်နှင့် ကျေးဇူးတင်လွှာ

Code နှင့် အသင့်ပါသော အသံများ- Apache-2.0, Copyright 2026 Ali Haydar Ozturk။ VoxCPM2 (OpenBMB, Apache-2.0)၊
audio.cpp (ShugoAI LLC, Apache-2.0) နှင့် audio.cpp GGUF ပြောင်းလဲမှုတို့ကို အခြေခံ၍ တည်ဆောက်ထားသည်။ စာရင်း အပြည့်အစုံ-
[THIRD_PARTY.md](THIRD_PARTY.md)။ OpenBMB၊ ModelBest သို့မဟုတ် audio.cpp project တို့နှင့် ဆက်စပ်မှု မရှိပါ။

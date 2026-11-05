[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · **ລາວ** · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**ການອອກແບບສຽງພາສາຕວກກີດ້ວຍ VoxCPM2 ເທິງ GPU 4 GB.** ອະທິບາຍສຽງເປັນພາສາອັງກິດ, ໃຫ້ model ສ້າງມັນຂຶ້ນ, ເລືອກຕົວເລືອກ
ທີ່ທ່ານມັກ, ແລ້ວອ່ານຂໍ້ຄວາມພາສາຕວກກີໃດກໍໄດ້ດ້ວຍສຽງນັ້ນ. ໂຄງການນີ້ມີ installer ທີ່ໃຊ້ຄຳສັ່ງດຽວ, engine
[audio.cpp](https://github.com/0xShug0/audio.cpp) ທີ່ດັດແປງໃຫ້ພໍດີກັບ GTX 1050 Ti (4 GB), web UI ນ້ອຍໆທີ່ເຮັດວຽກໃນເຄື່ອງຂອງທ່ານ
ແລະ ສຽງສັງເຄາະ (synthetic) ສຳເລັດຮູບສິບສີ່ສຽງ: ສຽງຕວກກີເຈັດສຽງ ແລະ ຜູ້ບັນຍາຍເຈົ້າຂອງພາສາເຈັດຄົນ ເປັນພາສາອັງກິດ, ຝຣັ່ງ,
ເຢຍລະມັນ, ສະເປນ, ຣັດເຊຍ, ຈີນ ແລະ ຍີ່ປຸ່ນ.

- ແອັບອ່ານໄດ້ 30 ພາສາ; ໜ້າຈໍໃຊ້ງານ (interface) ກໍມີ 30 ພາສາຄືກັນ.
- ສຽງສຳເລັດຮູບ 14 ສຽງ: ຕວກກີ 7 ສຽງ, ບວກກັບພາສາລະໜຶ່ງສຽງ ຄື ອັງກິດ, ຝຣັ່ງ, ເຢຍລະມັນ, ສະເປນ, ຣັດເຊຍ, ຈີນ ແລະ ຍີ່ປຸ່ນ.
- Web UI (v0.2.0): ບັດຕົວເລືອກທຸກໃບມີສອງສຽງ ຄື ສຽງອອກແບບດິບ ແລະ ສຽງທີ່ທ່ານຈະໄດ້ຍິນຕໍ່ໄປ; ລາຍການອ່ານທີ່ມີ menu ສຽງ;
  ປ່ຽນຊື່, ເຊື່ອງ ຫຼື ລຶບສຽງ; ສະບັບຮ່າງສຳລັບຂໍ້ຄວາມທີ່ທ່ານອ່ານ. ເບິ່ງ "Web UI" ພາຍໃຕ້ "ການນຳໃຊ້".

[ພໍດີກັບ 4 GB ໄດ້ແນວໃດ](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [ຄູ່ມືຕິດຕັ້ງສຳລັບ AI agent](AGENTS.md) · [ການນຳໃຊ້ຢ່າງມີຄວາມຮັບຜິດຊອບ](ETHICS.md)

> ສຽງທີ່ມາພ້ອມເປັນສຽງສັງເຄາະ ທີ່ອອກແບບຈາກຄຳອະທິບາຍເປັນຂໍ້ຄວາມ. ສ່ວນສຳເນົາສຽງມີໄວ້ສຳລັບສຽງຂອງທ່ານເອງ ຫຼື ສຽງທີ່ໃຊ້ໂດຍໄດ້ຮັບ
> ອະນຸຍາດຢ່າງຊັດເຈນຈາກເຈົ້າຂອງເທົ່ານັ້ນ; UI ຈະຂໍໃຫ້ທ່ານຢືນຢັນການອະນຸຍາດນັ້ນ. ການປອມຕົວເປັນຄົນອື່ນ, ການສໍ້ໂກງ ແລະ ການຫຼອກລວງ
> ເປັນສິ່ງຕ້ອງຫ້າມ. ໃຫ້ຕິດປ້າຍວ່າສິ່ງທີ່ທ່ານສ້າງແມ່ນສ້າງດ້ວຍ AI. ເບິ່ງ [ETHICS.md](ETHICS.md).

## 30 ພາສາ

ພວກເຮົາໄດ້ເຮັດວິດີໂອສາລະຄະດີກ່ຽວກັບກາປາໂດເຊຍ (Cappadocia) ໜຶ່ງເລື່ອງເປັນ 8 ພາສາ: ຕວກກີ, ອັງກິດ, ຝຣັ່ງ, ເຢຍລະມັນ, ສະເປນ,
ຣັດເຊຍ, ຈີນ ແລະ ຍີ່ປຸ່ນ. ແຕ່ລະພາສາມີ **ຜູ້ບັນຍາຍເຈົ້າຂອງພາສາ** ຂອງຕົນເອງ ທີ່ອອກແບບດ້ວຍ VoxCPM2 ຈາກຄຳອະທິບາຍພາສາອັງກິດ.
ທັງໝົດສ້າງຂຶ້ນໃນເຄື່ອງທັງໝົດເທິງ GTX 1050 Ti 4 GB ດ້ວຍຄຸນນະພາບຄົງທີ່ດຽວກັນ (16 ຂັ້ນ, cfg 2.0). ຜູ້ບັນຍາຍທັງເຈັດຄົນມາພ້ອມ
ຢູ່ທີ່ນີ້ ພ້ອມກັບ prompt, ຂໍ້ຄວາມອອກແບບ, seed ແລະ ການບັນທຶກສຽງອ້າງອີງ (reference) ຂອງເຂົາເຈົ້າ.

| ລະຫັດ | ພາສາ | ສຽງ | ຟັງ | ວິດີໂອ |
|---|---|---|---|---|
| `tr` | ຕວກກີ | `hazir/belgesel_hanim` (ແລະ ອີກ 6 ສຽງ) | [ຕົວຢ່າງ](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | ອັງກິດ | `hazir/anlatici_en` | [ຕົວຢ່າງ](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113791986763440439) |
| `fr` | ຝຣັ່ງ | `hazir/anlatici_fr` | [ຕົວຢ່າງ](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113790681575804962) |
| `de` | ເຢຍລະມັນ | `hazir/anlatici_de` | [ຕົວຢ່າງ](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113791351645262249) |
| `es` | ສະເປນ | `hazir/anlatici_es` | [ຕົວຢ່າງ](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113807365611122705) |
| `ru` | ຣັດເຊຍ | `hazir/anlatici_ru` | [ຕົວຢ່າງ](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113801574136848884) |
| `zh` | ຈີນ (ຈີນກາງ) | `hazir/anlatici_zh` | [ຕົວຢ່າງ](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113802229606121794) |
| `ja` | ຍີ່ປຸ່ນ | `hazir/anlatici_ja` | [ຕົວຢ່າງ](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [ວິດີໂອ](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**ເປັນຫຍັງຈຶ່ງອ່ານເທື່ອລະປະໂຫຍກ.** VoxCPM2 ບໍ່ໝັ້ນຄົງສຳລັບການສ້າງຍາວໆໃນຄັ້ງດຽວ (ປະມານເກີນ 30 ວິນາທີ): ຈັງຫວະຈະໄວຂຶ້ນ
ແລະ ສຽງອາດຈະເພີ້ນອອກ. ຢູ່ທີ່ນີ້ ສຽງຖືກຮັກສາໄວ້ດ້ວຍການບັນທຶກສຽງອ້າງອີງ ແລະ seed ທີ່ຄົງທີ່, ແລະ ຂໍ້ຄວາມຍາວຖືກອ່ານໜຶ່ງປະໂຫຍກ
ຕໍ່ໜຶ່ງແຖວ, ດັ່ງນັ້ນສີສັນຂອງສຽງ ແລະ ລີລາຈຶ່ງຄືເກົ່າຕັ້ງແຕ່ປະໂຫຍກທຳອິດຈົນເຖິງປະໂຫຍກສຸດທ້າຍ. ສຳລັບພາສາອື່ນທີ່ບໍ່ແມ່ນຕວກກີ
ຈະບໍ່ໃຊ້ວັດຈະນານຸກົມການອອກສຽງພາສາຕວກກີ. ທັງ 30 ພາສາທີ່ VoxCPM2 ຮອງຮັບໄດ້ຖືກທົດສອບແລ້ວ ແລະ ໃຊ້ງານໄດ້; ສຳລັບພາສາທີ່ບໍ່ມີ
ສຽງມາພ້ອມ ໃຫ້ໃຊ້ `--dil <code>`. ຄຳສັ່ງແຍກຕາມພາສາ ແລະ ບົດຮຽນທີ່ພວກເຮົາໄດ້ຮຽນຮູ້: [docs/cok_dilli.md](docs/cok_dilli.md).
Claude Code skill ສຳລັບຂັ້ນຕອນການອອກແບບທັງໝົດ: [.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**prompt ຕົວຢ່າງ 144 ອັນ ສຳລັບເລີ່ມຕົ້ນ.** 18 ບົດບາດ (ຜູ້ບັນຍາຍສາລະຄະດີ, ຜູ້ປະກາດຂ່າວ, ສຽງໂຄສະນາ, ປຶ້ມສຽງ, ແມ່ຕູ້ເລົ່ານິທານ,
ພິທີກອນ podcast, ຄູສອນ, trailer ຮູບເງົາ, ຜູ້ນຳສະມາທິ, ນັກພາກກິລາ ແລະ ອື່ນໆ, ທັງຊາຍ ແລະ ຍິງ) ໃນແຕ່ລະພາສາທັງ 8 ພາສາ. prompt
ເປັນພາສາອັງກິດ ໂດຍລະບຸສັນຊາດ ແລະ ສຳນຽງພື້ນເມືອງຂອງຜູ້ເວົ້າ; ຂໍ້ຄວາມທີ່ອ່ານຕອນກຳລັງສ້າງສຽງກໍມາພ້ອມກັນ ເປັນພາສານັ້ນ ແລະ
ເຂົ້າກັບບົດບາດ. ເລືອກອັນໜຶ່ງ, ຟັງຕົວເລືອກຕ່າງໆ, ເກັບອັນທີ່ທ່ານມັກໄວ້: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`,
ຫຼື ເລືອກ *ຄຳອະທິບາຍຕົວຢ່າງ* ໃນ web UI. ລາຍການເຕັມ: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**ພາກສຽງວິດີໂອຂອງທ່ານດ້ວຍສຽງຂອງທ່ານເອງ.** [DubWorld](https://github.com/alexturkey/dubworld) ແມ່ນໂປຣແກຣມພາກສຽງ
(dubbing) ວິດີໂອຂອງພວກເຮົາທີ່ເຮັດວຽກໃນເຄື່ອງ; ມັນຕິດຕັ້ງ repository ນີ້ເປັນ engine ສຽງ VoxCPM2 ຂອງມັນ. ສຽງທີ່ທ່ານອອກແບບຢູ່ທີ່ນີ້
ຈະຖືກໃຊ້ຢູ່ທີ່ນັ້ນດ້ວຍ `ses.voxcpm2_ses = "<name>/<variant>"`.

## ເລີ່ມຕົ້ນໄວ (Windows, 3 ຂັ້ນຕອນ)

1. **ດາວໂຫຼດ** ລະຫັດ: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   ຊຸດ engine ສຳເລັດຮູບສຳລັບກາດຂອງທ່ານ installer ຈະດຶງມາໃຫ້ໃນຂັ້ນຕອນທີ 3:
   NVIDIA → [ຊຸດ CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [ຊຸດ Vulkan, ທົດລອງ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (ດາວໂຫຼດມາແລ້ວບໍ? ເພີ່ມ `-HazirZip <path to the zip>` ໃສ່ຄຳສັ່ງຂ້າງລຸ່ມ).
2. **ແຕກໄຟລ໌** zip, ເປີດ folder `voxcpm2-turkce-ses-tasarimi-main`, ພິມ `powershell` ໃນແຖບທີ່ຢູ່ຂອງ Explorer
   ແລ້ວກົດ Enter.
3. **ແລ່ນ** installer (ຕ້ອງການ Python 64-bit 3.10-3.13; NVIDIA driver ≥ 570 ສຳລັບ CUDA), ແລ້ວຄລິກສອງເທື່ອທີ່ **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: ເພີ່ມ `-Vulkan` ໄວ້ທ້າຍສຸດ. UI ຈະເປີດຢູ່ທີ່ http://127.0.0.1:8765/.

zip ຂອງ engine ບໍ່ແມ່ນແອັບທີ່ເຮັດວຽກໄດ້ດ້ວຍຕົວເອງ (exe ຂອງມັນຕ້ອງການ model ແລະ DLL ທີ່ installer ຕິດຕັ້ງໃຫ້). ລາຍລະອຽດ,
ລາຍຊື່ GPU ແລະ ບັນຫາທີ່ພົບເລື້ອຍ: ເບິ່ງ "ຕິດຕັ້ງໄວ" ຂ້າງລຸ່ມ.

## Ubuntu / Linux (NVIDIA CUDA, ທົດລອງ)

Build engine ທີ່ດັດແປງແລ້ວດ້ວຍ `bash scripts/kur-linux.sh`, ຫຼື ໃຊ້ `Dockerfile.linux` ເພື່ອ build ແລະ ແລ່ນໃນສະພາບແວດລ້ອມ
Ubuntu 24.04 / CUDA 12.8.1. ຕ້ອງການ NVIDIA GPU ແລະ driver ທີ່ເຂົ້າກັນໄດ້; installer ແບບ native ຍັງຕ້ອງການ CUDA toolkit ແລະ
Python 3.10-3.13. UI ຍັງຮັບຟັງສະເພາະ loopback ເທົ່ານັ້ນ, ເຖິງແມ່ນຢູ່ເທິງ server ທາງໄກ (SSH forwarding). ສິ່ງທີ່ຕ້ອງມີກ່ອນ,
ຄຳສັ່ງ, ການເລືອກ architecture ແລະ ຂອບເຂດການກວດສອບ: [docs/linux.md](docs/linux.md).

## ເລີ່ມຕົ້ນໄວ (macOS, Apple Silicon)

ຕ້ອງການ Xcode Command Line Tools (`xcode-select --install`) ແລະ [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
installer ຈະດາວໂຫຼດ model, build engine ທີ່ດັດແປງແລ້ວດ້ວຍ Metal (~1 ນາທີ) ແລະ ຕັ້ງທຸກຢ່າງໄວ້ພາຍໃຕ້ `~/vox`.
ຈາກນັ້ນຄລິກສອງເທື່ອທີ່ **`baslat.command`**. ເທິງ MacBook Air M4 16 GB: ການຄຳນວນ ~2 s ຕໍ່ການເວົ້າ 1 s, seed ດຽວກັນໃຫ້ສຽງ
ທີ່ຄືກັນທຸກ byte, RAM ສູງສຸດ ~5.3 GB, ບໍ່ມີການຊ້າລົງຍ້ອນຄວາມຮ້ອນຕະຫຼອດ 12 ນາທີຂອງການອ່ານຕໍ່ເນື່ອງ. ລາຍລະອຽດ ແລະ
ການວັດແທກ: [docs/mac.md](docs/mac.md).

**ແອັບ Mac ແບບ native (ບໍ່ຕ້ອງໃຊ້ Python, Homebrew ຫຼື Terminal):** [macos/README.md](macos/README.md). ມັນມາພ້ອມກັບ
engine ທີ່ດັດແປງແລ້ວອັນດຽວກັນ ແລະ ດາວໂຫຼດ model ເມື່ອເປີດຄັ້ງທຳອິດ; ໃນຕອນນີ້ຕ້ອງ build ຈາກ source ດ້ວຍ Xcode.

## ສຳລັບຜູ້ໃຊ້ Mac (Apple Silicon)

ຍັງມີສະບັບດັດແປງອິດສະຫຼະອີກອັນໜຶ່ງ ທີ່ຊຸມຊົນສ້າງຂຶ້ນສຳລັບ Mac ທີ່ໃຊ້ Apple Silicon ເຊິ່ງແລ່ນ VoxCPM2 ດ້ວຍ framework MLX
ຂອງ Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
ມັນຖືກພັດທະນາ ແລະ ດູແລໂດຍ Emre Koç ([@emre-koc](https://github.com/emre-koc)) ໃນ repository ຂອງລາວເອງ, ບໍ່ແມ່ນຢູ່ທີ່ນີ້;
ຂັ້ນຕອນການຕິດຕັ້ງ ແລະ ຄຳຖາມຂໍຄວາມຊ່ວຍເຫຼືອໃຫ້ໄປຖາມຢູ່ທີ່ນັ້ນ. ຂອບໃຈ Emre ທີ່ນຳໂຄງການນີ້ມາສູ່ Mac!

## ມັນເຮັດວຽກແນວໃດ

1. **ການອອກແບບສຽງ.** *ຄຳອະທິບາຍສຽງ* ເປັນພາສາອັງກິດ + *ຂໍ້ຄວາມທີ່ອ່ານຕອນກຳລັງສ້າງສຽງ* (ເປັນພາສາຂອງສຽງນັ້ນ) + ຈຳນວນ
   ຕົວເລືອກ. ແຕ່ລະຕົວເລືອກໄດ້ຮັບ seed ຂອງຕົນເອງ; engine ຮັບ `(description)text` ແລະ ສົ່ງການບັນທຶກອອກແບບຄືນມາໜຶ່ງອັນຕໍ່
   seed. ຂໍ້ຄວາມເປັນຕົວຢ່າງສັ້ນໆເພື່ອຮູ້ຈັກສຽງ: 1-3 ປະໂຫຍກ, ສູງສຸດ ~30 s (UI ສະແດງການຄາດຄະເນ ແລະ ຈະບໍ່ເລີ່ມຖ້າເກີນ 33 s);
   ຂໍ້ຄວາມຍາວແມ່ນສຳລັບຂັ້ນຕອນທີ 2.
2. **ການອ່ານອີງໃສ່ສຽງອ້າງອີງ.** ການບັນທຶກອອກແບບຖືກສົ່ງໄປຫາ input **ທັງສອງ** ຂອງ engine (`audio` ແລະ `voice_ref`) ພ້ອມກັບ
   ບົດຖອດຄວາມຂອງມັນ (`reference_text`) ແລະ ຂໍ້ຄວາມໃໝ່ທີ່ຈະອ່ານ, ດ້ວຍ seed ດຽວກັນ. ສຽງຖືກພາໄປໂດຍການບັນທຶກ, ບໍ່ແມ່ນໂດຍ
   ຄຳອະທິບາຍ, ດັ່ງນັ້ນມັນຈຶ່ງບໍ່ເພີ້ນຈາກຂໍ້ຄວາມໜຶ່ງໄປຫາອີກຂໍ້ຄວາມໜຶ່ງ. ຂໍ້ຄວາມຖືກອ່ານເທື່ອລະປະໂຫຍກ.
3. ຄຸນນະພາບຄົງທີ່: diffusion 16 ຂັ້ນ, CFG 2.0. seed ບໍ່ແມ່ນປຸ່ມປັບຄຸນນະພາບ.
4. **ເວລາຂອງແຕ່ລະຄຳ ແລະ ສຽງດຽວກັນທຸກຄັ້ງ.** ຂະນະອ່ານ, engine ບອກເອງວ່າແຕ່ລະຄຳເລີ່ມ ແລະ ຈົບຢູ່ໃສ (patch 0002, ບໍ່ຕ້ອງມີໂມເດວເພີ່ມ). ເວລາຖືກຂຽນລົງ `kelimeler.json` ແລະ ແຖວຖືກຕັດໃຫ້ຊ່ອງວ່າງລະຫວ່າງແຖວເທົ່າກັບການຕັ້ງຄ່າການຢຸດ. ຄວາມແມ່ນຍຳທຽບກັບ CTC forced alignment (CTC = 100%): 89.66% (ພາສາຕຸລະກີ, 12 ສຽງ; ການຕັ້ງຄ່າ `kelime_zamani` ເປີດເປັນຄ່າເລີ່ມຕົ້ນ). ດ້ວຍ patch 0003, seed ດຽວກັນໃຫ້ສຽງທີ່ຄືກັນທຸກໄບທ໌ໃນທຸກຄັ້ງທີ່ແລ່ນ.

ການບັນທຶກອອກແບບດິບເປັນຕົວຢ່າງສຽງທີ່ອອກມາເທື່ອດຽວ; ບໍ່ມີການອ່ານຄັ້ງຕໍ່ໄປໃດໆທີ່ຟັງຄືມັນທຸກຢ່າງ. ສິ່ງທີ່ທ່ານໄດ້ຍິນໃນທຸກການອ່ານ
ຄັ້ງຕໍ່ໄປແມ່ນຂັ້ນຕອນທີ 2: ການບັນທຶກອອກແບບເປັນສຽງອ້າງອີງ ບວກກັບ seed ຂອງຕົວເລືອກນັ້ນເອງ. ນັ້ນຄືເຫດຜົນທີ່ web UI ເຮັດຂັ້ນຕອນທີ 2
ທັນທີຫຼັງຈາກການອອກແບບ ແລະ ສະແດງທັງສອງຢ່າງໃນບັດຕົວເລືອກ.

engine ແມ່ນ audio.cpp v0.7.2 ພ້ອມກັບ patch ຂອງພວກເຮົາ (`patches/`), model ແມ່ນ VoxCPM2 Q8_0 GGUF. VRAM ສູງສຸດ ≈ 2.8 GB;
ການຄຳນວນປະມານ 2 s ຕໍ່ການເວົ້າ 1 s ເທິງ GTX 1050 Ti. ລາຍລະອຽດ ແລະ ການວັດແທກ: [docs/4gb.md](docs/4gb.md).

## ສຽງທີ່ມາພ້ອມ (`hazir_sesler/`)

ທັງສິບສີ່ສຽງຖືກອອກແບບຈາກ prompt ທີ່ເກັບໄວ້ໃນ `ses.json` ຂອງມັນ; ບໍ່ມີສຽງໃດຖືກສຳເນົາຈາກການບັນທຶກ (ການສຳເນົາແມ່ນແຖບ
*ສຳເນົາສຽງ* ແຍກຕ່າງຫາກ ທີ່ຕ້ອງມີການຍິນຍອມ).

| ສຽງ | ຄຳອະທິບາຍສັ້ນ | ຟັງ |
|---|---|---|
| `belgesel_hanim` | ຜູ້ຍິງໄວກາງຄົນອາຍຸຫ້າສິບກວ່າ, alto ທຸ້ມ ແລະ ອົບອຸ່ນ; ຜູ້ບັນຍາຍສາລະຄະດີທີ່ສະຫງົບ | [ຕົວຢ່າງ](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | ຜູ້ບັນຍາຍຊາຍສຽງທຸ້ມ, ມີພະລັງ ແລະ ລຶກລັບ | [ຕົວຢ່າງ](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | ຜູ້ປະກາດຂ່າວທີ່ມີປະສົບການອາຍຸປະມານເຈັດສິບ, ສະຫງົບ ແລະ ໜ້າເຊື່ອຖື | [ຕົວຢ່າງ](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | ຜູ້ປະກາດຂ່າວພາກຄ່ຳຍິງອາຍຸສາມສິບກວ່າ, ມີສະເໜ່, ສຽງນຸ້ມຄືຜ້າກຳມະຫຍີ່ ແລະ ເຕັມໄປດ້ວຍອາລົມ | [ຕົວຢ່າງ](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | ແມ່ມົດໃນນິທານ: ສຽງຕ່ຳ, ອອກດັງໜ້ອຍໜຶ່ງ, ຫວານແບບມີເລ່ຫຼ່ຽມ | [ຕົວຢ່າງ](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | ຜູ້ບັນຍາຍຊາຍສຽງທຸ້ມເປັນພິເສດ, ໜັກແໜ້ນ ແລະ ມີອຳນາດສັ່ງການ | [ຕົວຢ່າງ](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | ຜູ້ເຖົ້າຜູ້ມີປັນຍາ, ສຽງທຸ້ມ ແລະ ກ້ອງກັງວານ, ລຶກລັບໜ້ອຍໜຶ່ງ | [ຕົວຢ່າງ](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາອັງກິດ ອາຍຸຫ້າສິບກວ່າ (General American); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາຝຣັ່ງ ອາຍຸຫ້າສິບກວ່າ (ປາຣີ); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາເຢຍລະມັນ ອາຍຸຫ້າສິບກວ່າ (Hochdeutsch); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາສະເປນ ອາຍຸຫ້າສິບກວ່າ (Castilian (ມາດຣິດ)); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາຣັດເຊຍ ອາຍຸຫ້າສິບກວ່າ (ມົສກູ); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາຈີນ (ຈີນກາງ) ອາຍຸຫ້າສິບກວ່າ (Putonghua ປັກກິ່ງ); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | ຜູ້ບັນຍາຍສາລະຄະດີຊາຍ ເຈົ້າຂອງພາສາຍີ່ປຸ່ນ ອາຍຸຫ້າສິບກວ່າ (ມາດຕະຖານໂຕກຽວ); ທຸ້ມ, ສະຫງົບ, ອົບອຸ່ນ | [ຕົວຢ່າງ](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [ສຽງອ້າງອີງ](hazir_sesler/anlatici_ja/referans.flac) |

ແຕ່ລະ folder: `referans.flac` (ການບັນທຶກອອກແບບແບບບໍ່ສູນເສຍຄຸນນະພາບ), `ses.json` (prompt, ບົດຖອດຄວາມ, seed ອອກແບບ,
seed ອ່ານ, ຄຳອະທິບາຍ; `dil` = ພາສາ ສຳລັບຜູ້ບັນຍາຍ), `ornek_okuma.mp3` (+ ຂໍ້ຄວາມຂອງມັນ). ໃຊ້ໄດ້ໂດຍກົງ: `--ses hazir/<name>`.
ການບັນທຶກສຽງອ້າງອີງຂອງຜູ້ບັນຍາຍແມ່ນສັ້ນ (5.6-10 s); ຕົວຢ່າງຂອງເຂົາເຈົ້າແມ່ນສາມປະໂຫຍກທຳອິດຂອງບົດກາປາໂດເຊຍ ທີ່ຕັດມາຈາກ
ການອ່ານສຳລັບການຜະລິດສະບັບເຕັມ.

## ຕິດຕັ້ງໄວ, ບໍ່ຕ້ອງໃຊ້ compiler (Windows 10/11, NVIDIA GPU ≥ 4 GB)

ສິ່ງທີ່ຕ້ອງມີກ່ອນ: NVIDIA driver ≥ 570 ແລະ Python 64-bit 3.10-3.13 (`winget install Python.Python.3.12`). ບໍ່ຕ້ອງມີຫຍັງອີກ:
ບໍ່ຕ້ອງມີ Visual Studio, ບໍ່ຕ້ອງມີ CUDA installer. ບໍ່ແນ່ໃຈວ່າທ່ານມີກາດຫຍັງ? ແລ່ນ `nvidia-smi` ໃນ PowerShell: ມັນຈະສະແດງຊື່
GPU, ເວີຊັນ driver ແລະ ໜ່ວຍຄວາມຈຳ. ບໍ່ມີກາດ NVIDIA? ເບິ່ງ "AMD / Intel" ຂ້າງລຸ່ມ.

ດ້ວຍ [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

ບໍ່ມີ Git: ໃນໜ້ານີ້ຄລິກ **Code → Download ZIP**, ແຕກໄຟລ໌, ເປີດ folder `voxcpm2-turkce-ses-tasarimi-main` ທີ່ແຕກອອກມາ,
ພິມ `powershell` ໃນແຖບທີ່ຢູ່ຂອງ Explorer ແລ້ວກົດ Enter, ຈາກນັ້ນແລ່ນແຖວສຸດທ້າຍຂ້າງເທິງ. Git ຕ້ອງການສະເພາະສຳລັບທາງ build
ຈາກ source ເທົ່ານັ້ນ.

`-ExecutionPolicy Bypass` ມີຜົນສະເພາະກັບ process ນີ້ອັນດຽວ ແລະ ບໍ່ປ່ຽນການຕັ້ງຄ່າລະບົບໃດໆ; ອ່ານ `scripts\kur.ps1` ກ່ອນແລ່ນ,
ຄືກັບ script ຕິດຕັ້ງອື່ນໆ. ຄຳສັ່ງດຽວ, ~10 ນາທີ, ດາວໂຫຼດ ~3.7 GB, ທຸກຢ່າງກວດສອບດ້ວຍ sha256: model (2.95 GB), DLL runtime
ຂອງ CUDA 12.8 ເປັນ zip ແບບພົກພາ (ບໍ່ຕິດຕັ້ງເຂົ້າລະບົບ, ບໍ່ແຕະ PATH), **engine ທີ່ build ສຳເລັດແລ້ວ** ຈາກໜ້າ Releases, `.venv`
ທີ່ມີ Python package ສອງອັນ, `ayarlar.json`, ແລະ ການກວດ GPU ຄັ້ງສຸດທ້າຍ (`KONTROL_OK`). ແລ່ນມັນຄືນໃໝ່ຫຼັງຈາກລົ້ມເຫຼວໃດໆ;
ໄຟລ໌ທີ່ກວດສອບແລ້ວຈະຖືກຂ້າມ. ຈາກນັ້ນເລີ່ມ web UI: ຄລິກສອງເທື່ອທີ່ **`baslat.bat`** ໃນ folder ຂອງ repo. ມັນຈະເລີ່ມ UI ແລະ
ເປີດ **http://127.0.0.1:8765/** ໃນ browser ຂອງທ່ານເມື່ອພ້ອມ; ປິດໜ້າຕ່າງສີດຳ (ຫຼື ກົດ Ctrl+C ຢູ່ທີ່ນັ້ນ) ເພື່ອຢຸດມັນ.
ແບບດຽວກັນຈາກ PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
ແລ້ວເປີດ **http://127.0.0.1:8765/** ເອງ (ເມື່ອເລີ່ມແບບນີ້ UI ຈະບໍ່ເປີດ browser; ມັນຮັບຟັງສະເພາະ localhost ເທົ່ານັ້ນ).

> **`audiocpp_cli.exe` ໃນ zip ຂອງ release ບໍ່ໄດ້ມີໄວ້ສຳລັບຄລິກສອງເທື່ອ.** ມັນເປັນ engine ແບບ command-line ທີ່ຕ້ອງມີ DLL
> ຂອງ CUDA ແລະ model ຢູ່ຄຽງຂ້າງ; `kur.ps1` ວາງທຸກຢ່າງໄວ້ໃນບ່ອນ ແລະ Python package ເປັນຕົວຂັບເຄື່ອນມັນ. ການຄລິກສອງເທື່ອ
> ຈະສະແດງພຽງແຕ່ "cudart64_12.dll not found".

**GPU ທີ່ຮອງຮັບ (release v0.1.1):** native code ສຳລັບ GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) ແລະ RTX 50xx (sm_120a); CUDA GPU ອື່ນໆຕັ້ງແຕ່ Pascal ຂຶ້ນໄປ ຈະແລ່ນ PTX ທີ່ຝັງໄວ້ຜ່ານ driver (ການເລີ່ມຄັ້ງທຳອິດຊ້າກວ່າ).
Maxwell (GTX 9xx) ແລະ ເກົ່າກວ່ານັ້ນ CUDA 12.8 ບໍ່ຮອງຮັບ. ພວກເຮົາທົດສອບເທິງ GTX 1050 Ti 4 GB (ລວມທັງຜ່ານ Docker Desktop/WSL2
ເທິງ Windows, ສະເພາະ CLI); ວັດແທກໂດຍ @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (ລາຍລະອຽດໃນ
[docs/linux.md](docs/linux.md)). ຍິນດີຕ້ອນຮັບລາຍງານຈາກກາດອື່ນໆໃນ [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (ທົດລອງ):** zip engine Vulkan ແຍກຕ່າງຫາກ (`...-win64-vulkan.zip`, ບໍ່ມີ CUDA) ຕິດຕັ້ງດ້ວຍ
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. ມັນຖືກກວດສອບສະເພາະເທິງກາດ NVIDIA ຂອງພວກເຮົາຜ່ານ Vulkan backend ເທົ່ານັ້ນ (ຢູ່ທີ່ນັ້ນ
ມັນແລ່ນຊ້າກວ່າ CUDA ແຕ່ໃຫ້ສຽງດຽວກັນສຳລັບ seed ດຽວກັນ; ການວັດແທກນັ້ນເຮັດໃນຂະນະທີ່ disk ກຳລັງຫຍຸ້ງກັບວຽກອື່ນ, ດັ່ງນັ້ນການ
ປຽບທຽບຄວາມໄວທີ່ສະອາດຍັງລໍຖ້າຢູ່) ແລະ ພວກເຮົາ **ຍັງບໍ່ໄດ້** ທົດສອບມັນເທິງຮາດແວ AMD ຫຼື Intel ດ້ວຍຕົນເອງ: ຖ້າທ່ານລອງ, ກະລຸນາ
ໂພສຜົນໃນ Discussions. ເມື່ອມີອຸປະກອນ Vulkan ຫຼາຍກວ່າໜຶ່ງ (integrated + discrete) installer ຈະຂຽນ index ຂອງ GPU discrete
ເປັນ `cihaz` ລົງໃນ `ayarlar.json`.

**ໝາຍເຫດ:** ການຮອງຮັບ Vulkan ໃນປັດຈຸບັນຍັງເປັນການທົດລອງ. ມັນຖືກ build ແລະ ທົດສອບສຳເລັດເທິງ GTX 1050 Ti. ຜູ້ໃຊ້ພາຍນອກ
ຄົນໜຶ່ງ (mitra_tr) ຍັງໄດ້ລາຍງານວ່າໄດ້ແລ່ນມັນເທິງ AMD 6900 XT. ຍັງຕ້ອງການການທົດສອບທີ່ກວ້າງຂວາງກວ່ານີ້ເທິງກາດ AMD/Intel.

**ການທົດສອບຈາກຊຸມຊົນ (AMD):** @mitraTR ໄດ້ແລ່ນ v0.1.1 ດ້ວຍ Vulkan ເທິງ AMD Radeon RX 6900 XT ໃນ Windows 11: ການຕິດຕັ້ງ, ການອອກແບບສຽງ, ການອ່ານ, ໜ້າເວັບ ແລະ ການທົດສອບ ເຮັດວຽກໄດ້ທັງໝົດ; ການອ່ານໃຊ້ເວລາຄິດໄລ່ປະມານ 0.8-0.9 ວິ ຕໍ່ສຽງເວົ້າ 1 ວິ ([ລາຍງານໃນ #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). ໃຫ້ຕິດຕັ້ງໃນໂຟນເດີສັ້ນໆ ທີ່ເສັ້ນທາງມີແຕ່ຕົວອັກສອນ ASCII (ເຊັ່ນ `C:\vox`): ໃນ Windows ເຄື່ອງຈັກບໍ່ສາມາດເປີດເສັ້ນທາງທີ່ມີຕົວອັກສອນລາວ ຫຼື ຕົວອັກສອນອື່ນນອກ ASCII ໄດ້. ລາຍງານທັງໝົດຈົນເຖິງຕອນນີ້: [ຮາດແວທີ່ທົດສອບແລ້ວ](docs/donanim_testleri.md).

**ໝາຍເຫດກ່ຽວກັບ Vulkan:** ເວລາຂອງແຕ່ລະຄຳ ຕອນນີ້ມີສະເພາະເທິງ NVIDIA (CUDA) ແລະ Mac ເທົ່ານັ້ນ; ເທິງ AMD/Intel ຈະຍັງບໍ່ມີ ຈົນກວ່າເອັນຈິນ Vulkan ຈະຖືກອັບເດດ (ການອ່ານຍັງໃຊ້ໄດ້). ການເປີດຄັ້ງທຳອິດເທິງ Vulkan ອາດໃຊ້ເວລາສອງສາມນາທີ ເພາະຕ້ອງຄອມໄພລ໌ shader ຂອງກາດຈໍ; ການອ່ານຄັ້ງຕໍ່ໄປຈະໄວຂຶ້ນ.

### ທາງເລືອກ: build engine ຈາກ source

ຕ້ອງການ Visual Studio 2022 Build Tools ພ້ອມ "Desktop development with C++" (ລວມທັງ C++ CMake tools), ~7 GB. ຈາກນັ້ນ:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
ຄຳສັ່ງນີ້ຍັງດາວໂຫຼດ nvcc, ດຶງ source ຂອງ audio.cpp v0.7.2, ນຳໃຊ້ `patches/0001-voxcpm2-4gb-ve-hiz.patch` ແລະ build ສຳລັບ
GPU ຂອງທ່ານ (`-Mimari native`, ຄ່າເລີ່ມຕົ້ນ; ຫຼື ຕົວຢ່າງ `-Mimari 61`), ~15-25 ນາທີ. ຮັກສາ root ໃຫ້ສັ້ນ (`C:\vox`): nvcc
ລົ້ມເຫຼວກັບເສັ້ນທາງຍາວ. ຂັ້ນຕອນລະອຽດພ້ອມການກວດສອບ: [AGENTS.md](AGENTS.md).

### ບັນຫາການຕິດຕັ້ງທີ່ພົບເລື້ອຍ

| ສິ່ງທີ່ທ່ານເຫັນ | ຄວາມໝາຍ ແລະ ສິ່ງທີ່ຕ້ອງເຮັດ |
|---|---|
| `cudart64_12.dll not found` ຫຼັງຈາກຄລິກສອງເທື່ອທີ່ exe | engine ບໍ່ໄດ້ມີໄວ້ໃຫ້ເລີ່ມດ້ວຍມື. ແລ່ນຄຳສັ່ງ `kur.ps1` ຂ້າງເທິງ, ແລ້ວເລີ່ມ web UI. |
| `64-bit Python 3.10+ bulunamadı` (ບໍ່ພົບ Python) | ຕິດຕັ້ງ Python (`winget install Python.Python.3.12`), ປິດ PowerShell, ເປີດອັນໃໝ່ ແລ້ວແລ່ນຄຳສັ່ງເກົ່າອີກຄັ້ງ. |
| `motor ekran kartını görmedi` (engine ບໍ່ເຫັນ GPU) | ອັບເດດ NVIDIA driver ເປັນ 570 ຫຼື ໃໝ່ກວ່າ; ກວດວ່າ `nvidia-smi` ແລ່ນໄດ້. |
| `indirme başarısız` / `sha256 tutmadı` (ດາວໂຫຼດລົ້ມເຫຼວ / checksum ບໍ່ກົງກັນ) | ສ່ວນຫຼາຍແມ່ນການດາວໂຫຼດທີ່ຂາດກາງຄັນ. ແລ່ນຄຳສັ່ງເກົ່າອີກຄັ້ງ; ໄຟລ໌ທີ່ກວດສອບແລ້ວຈະຖືກຂ້າມ. |
| ທາງ build: `nvcc` ລົ້ມເຫຼວ | ຮັກສາ root ການຕິດຕັ້ງໃຫ້ສັ້ນ (`-Kok C:\vox`). |
| ໜ້າເວັບບໍ່ເປີດ | ເລີ່ມ UI ດ້ວຍ `baslat.bat`, ຫຼື ເປີດ http://127.0.0.1:8765/ ເອງ. port ຖືກໃຊ້ຢູ່ບໍ? ປ່ຽນ `"port"` ໃນ `ayarlar.json`. |

ມີບັນຫາບໍ? [Discussions (ຖາມ-ຕອບ)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) ຫຼື
[issue ການຕິດຕັ້ງ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
ພ້ອມກັບ GPU ຂອງທ່ານ, ເວີຊັນ Windows, ຄຳສັ່ງ ແລະ ແຖວສຸດທ້າຍຂອງມັນ.

## ການນຳໃຊ້

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
ກົດຂອງຂໍ້ຄວາມ: ຂຽນຕົວເລກເປັນຄຳ, ບໍ່ມີເຄື່ອງໝາຍວົງຢືມ (ເຄື່ອງມືປະຕິເສດຕົວເລກ ແລະ ວົງຢືມ), ໜຶ່ງປະໂຫຍກຕໍ່ໜຶ່ງແຖວ, ≤ 2000
ຕົວອັກສອນຕໍ່ແຖວ. ການຢຸດຫຼັງແຖວ: `|| bagli` 0.25 s, `|| normal` 0.5 s, `|| paragraf` 1 s, `|| agir` 1.5 s ຫຼື ຄວາມຍາວ
ຂອງທ່ານເອງ `|| 0,8` (0-5 s; ອະນຸຍາດໃຫ້ໃຊ້ຕົວເລກຂອງເຄື່ອງໝາຍນີ້). `ayarlar/okunus_sozlugu.tsv` ແກ້ໄຂການອອກສຽງຄຳຕ່າງປະເທດ
ໃນຂໍ້ຄວາມພາສາຕວກກີ. ພາສາຖືກກວດຈັບຈາກຂໍ້ຄວາມ (ຕົວອັກສອນຕວກກີ, ລະບົບຕົວໜັງສື, ຄຳທີ່ໃຊ້ເລື້ອຍ; ຖ້າບໍ່ແນ່ໃຈໃຊ້ `dil` ຂອງບັດສຽງ;
`--dil <code>` ເປັນທາງເລືອກ). ສຳລັບຂໍ້ຄວາມທີ່ບໍ່ແມ່ນພາສາຕວກກີ ອະນຸຍາດໃຫ້ໃຊ້ apostrophe ໄດ້, ວັດຈະນານຸກົມຕວກກີຖືກຂ້າມ, ແຕ່
ຕົວເລກຍັງຖືກປະຕິເສດຢູ່. ຖ້າການອ່ານພິມ `speed gate: satır [...]` ອອກມາ, ໃຫ້ຟັງແຖວເຫຼົ່ານັ້ນ.

### Web UI

ໃນເຄື່ອງເທົ່ານັ້ນ (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → ເປີດ http://127.0.0.1:8765/ ເອງ
(port ອື່ນ: `--port 8800`), ຫຼື ຄລິກສອງເທື່ອທີ່ `baslat.bat`. ຢຸດ server ດ້ວຍ Ctrl+C. ມີສາມແຖບ: *ອອກແບບສຽງ*,
*ອ່ານດ້ວຍສຽງນີ້*, *ສຳເນົາສຽງ*. ເສັ້ນທາງປົກກະຕິ: *ອອກແບບ* → ຟັງຕົວເລືອກຕ່າງໆ → *ເພີ່ມໃສ່ລາຍການອ່ານຂອງຂ້ອຍ* →
*ອ່ານດ້ວຍສຽງນີ້* → ດາວໂຫຼດ. ຫຼື ເລືອກສຽງສຳເລັດຮູບຈາກ menu ສຽງ ແລ້ວອ່ານ.

- **ເວີຊັນໃນສ່ວນຫົວ.** `v0.2.0 · <short commit>` ນ້ອຍໆ ແລະ ຈາງໆ (ມີ `+` ເມື່ອໄຟລ໌ທີ່ຕິດຕາມມີການປ່ຽນແປງທີ່ຍັງບໍ່ໄດ້ commit;
  ບໍ່ມີ git ມີແຕ່ເວີຊັນ), ເພື່ອໃຫ້ພາບໜ້າຈໍ ແລະ ວິດີໂອສະແດງວ່າໃຊ້ເວີຊັນໃດ.
- **ສອງສຽງໃນບັດຕົວເລືອກທຸກໃບ.** ດ້ານເທິງ, ສີເທົາ, ແມ່ນ *ສຽງອອກແບບດິບ*: ມັນຖືກສ້າງເທື່ອດຽວ ແລະ ຈະບໍ່ອອກມາຄືເກົ່າອີກ.
  ດ້ານລຸ່ມ, ໃນກອບສີສົ້ມ, ແມ່ນ *↻ ນີ້ແມ່ນສຽງທີ່ທ່ານຈະໄດ້ຍິນຕະຫຼອດ*: ການບັນທຶກອອກແບບທີ່ອ່ານຄືນເປັນສຽງອ້າງອີງດ້ວຍ seed
  ຂອງຕົວເລືອກນັ້ນເອງ (ສະແດງຢູ່ໃນບັດ). ນີ້ຄືສຽງທີ່ຈະໄດ້ຍິນໃນທຸກການອ່ານຄັ້ງຕໍ່ໄປ. ຢູ່ລຸ່ມມັນມີ *ອ່ານດ້ວຍສຽງນີ້* ແລະ
  *ເພີ່ມໃສ່ລາຍການອ່ານຂອງຂ້ອຍ*. ກົດ *ອອກແບບ* ເທື່ອດຽວເຮັດທັງສອງຢ່າງ: ມັນອອກແບບທຸກຕົວເລືອກ, ແລ້ວອ່ານຂໍ້ຄວາມຂອງທ່ານດ້ວຍ
  ສຽງຖາວອນແຕ່ລະສຽງ; ແຖບຄວາມຄືບໜ້າອັນດຽວນັບທັງສອງໄລຍະ. folder ຂອງຕົວເລືອກໄດ້ຮັບ `dinleme.wav`. ຖ້າການອ່ານນັ້ນຢຸດກ່ອນ
  ກຳນົດ, ການອອກແບບຍັງຖືກເກັບໄວ້ ແລະ ບັດຈະສະແດງໝາຍເຫດ.
- **ໜ້າຕ່າງ "ຂໍ້ຄວາມທີ່ຢາກຟັງ".** ໃນ *ອອກແບບສຽງ*, ກ່ອງ *↻ ຂໍ້ຄວາມທີ່ຢາກຟັງ* ເກັບສິ່ງທີ່ສຽງຖາວອນແຕ່ລະສຽງຈະອ່ານ (ຖ້າປ່ອຍວ່າງ
  ຈະອ່ານປະໂຫຍກຕົວຢ່າງ). ການຄລິກມັນຈະເປີດປຶ້ມບັນທຶກການອ່ານໃນໜ້າຕ່າງ: ເລກແຖວ, menu ແຖວ, ແຖບການຢຸດ. *ຕົກລົງ* ຂຽນຂໍ້ຄວາມ ແລະ
  ການຢຸດຂອງມັນກັບຄືນໃສ່ກ່ອງ; *ຍົກເລີກ* ຫຼື Esc ບໍ່ປ່ຽນຫຍັງ. ແຖບອ່ານເກັບຂໍ້ຄວາມຂອງຕົນເອງໄວ້.
- **ປຶ້ມບັນທຶກການອ່ານ.** ໜຶ່ງປະໂຫຍກຕໍ່ໜຶ່ງແຖວ. ຄລິກເລກແຖວເພື່ອເປີດ menu ແຖວ (ຍ້າຍຂຶ້ນ ຫຼື ລົງ, ຍ້າຍໄປຕຳແໜ່ງໃດໜຶ່ງ, ສຳເນົາ,
  ລຶບ; Alt+↑/↓, Alt+Shift+↓, ຫຼື ລາກດ້ວຍເລກ; Ctrl+Z ຍົກເລີກທັງຂໍ້ຄວາມ ແລະ ການຢຸດພ້ອມກັນ). ຄລິກແຖບບາງໆລະຫວ່າງສອງແຖວເພື່ອ
  ເລືອກການຢຸດ (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 s, ຫຼື ຂອງທ່ານເອງ 0-5 s ດ້ວຍຮູບເຟືອງ); ກົດ Enter ສອງເທື່ອ
  ສຳລັບຫຍໍ້ໜ້າ (1 s), ແລະ ແຖວວ່າງຈະກາຍເປັນແຖບການຢຸດ. ໃນຂະນະທີ່ຜົນລັບກຳລັງຫຼິ້ນ, ແຖວທີ່ກຳລັງອ່ານຈະສະຫວ່າງ ແລະ ເລື່ອນມາໃຫ້
  ເຫັນ; *▶ ຟັງຈາກບ່ອນນີ້* ໃນ menu ແຖວຈະຫຼິ້ນຕັ້ງແຕ່ແຖວນັ້ນ. ຂໍ້ຄວາມ ແລະ ການຢຸດຂອງມັນຍັງຄົງຢູ່ເຖິງແມ່ນໂຫຼດໜ້າຄືນໃໝ່
  (browser storage).
- **ສະບັບຮ່າງ.** ປຸ່ມ *📄 ສະບັບຮ່າງ* ມີຢູ່ໃນປຶ້ມບັນທຶກທັງສອງ (ແຖບອ່ານ ແລະ ໜ້າຕ່າງ). ບັນທຶກຂໍ້ຄວາມປັດຈຸບັນພ້ອມການຢຸດຂອງມັນ
  ເປັນສະບັບຮ່າງ, ໂຫຼດອັນໜຶ່ງດ້ວຍການຄລິກ (Ctrl+Z ຍົກເລີກ), ແລະ ໃຊ້ ⋯ ເພື່ອຂຽນທັບ, ປ່ຽນຊື່ ຫຼື ລຶບມັນ. ສະບັບຮ່າງຖືກເກັບໄວ້ໃນ
  `sesler/taslaklar.json`, ບໍ່ເຄີຍຢູ່ໃນ repository.
- **ລາຍການອ່ານ ແລະ menu ສຽງ.** ໃນບັດຕົວເລືອກ, *ເພີ່ມໃສ່ລາຍການອ່ານຂອງຂ້ອຍ* ຈະເປີດກ່ອງຊື່: ຕັ້ງຊື່ໃຫ້ຕົວເລືອກ ແລະ ✓ ຈະເພີ່ມມັນ.
  *ຊື່ການສ້າງ* ຍັງຄົງຢູ່ໃນທຸກຕົວເລືອກຂອງການສ້າງຄັ້ງນັ້ນ. ໃນ *ອ່ານດ້ວຍສຽງນີ້*, ປຸ່ມສຽງ (ທຸງ + ຊື່) ຈະເປີດ menu ສຽງ:
  *ລາຍການອ່ານຂອງຂ້ອຍ* ຢູ່ເທິງສຸດ, ຕາມດ້ວຍສຽງສຳເລັດຮູບພ້ອມທຸງ (ພາສາຂອງ interface ກ່ອນ). ແຕ່ລະແຖວມີ ▶ ຟັງ (ສຽງຖາວອນ
  ຖ້າມີ), ຫົວໃຈ (ເພີ່ມ ຫຼື ເອົາອອກ) ແລະ ⋯; ↑/↓ ແລະ Enter ເລືອກ, Esc ປິດ, ສຽງສຸດທ້າຍຈະຖືກຈື່ໄວ້. ລາຍການຢູ່ໃນ
  `sesler/okuma_listesi.json`, ຢູ່ນອກ repository, ແລະ ຍັງຄົງຢູ່ຫຼັງຈາກເລີ່ມຄືນໃໝ່.
- **ການຈັດການສຽງ.** menu ⋯ (ແຖວໃນ menu ສຽງ ຫຼື ບັດຕົວເລືອກ) ມີ *ອ່ານດ້ວຍສຽງນີ້*, ເພີ່ມເຂົ້າ ຫຼື ເອົາອອກຈາກລາຍການ,
  *ປ່ຽນຊື່* (ຊື່ວ່າງຈະກັບຄືນຊື່ເດີມ; *ກັບໄປໃຊ້ຊື່ເດີມ*), *ລຶບ* ສຳລັບສຽງທີ່ອອກແບບເອງ ແລະ *ເຊື່ອງ* ສຳລັບສຽງສຳເລັດຮູບ; ທັງສອງ
  ຖາມກ່ອນ. ສຽງທີ່ຖືກລຶບຈະຍ້າຍໄປທີ່ `sesler/_cop/`; ການເຊື່ອງບໍ່ເຄີຍແຕະໄຟລ໌ຂອງ repository. *ສຽງທີ່ເຊື່ອງ ແລະ ລຶບແລ້ວ (N)*
  ຢູ່ລຸ່ມສຸດຂອງ menu ສຽງມີ *ກູ້ຄືນ*. ຊື່ທີ່ຕັ້ງເອງ ແລະ ສຽງທີ່ເຊື່ອງໄວ້ຖືກເກັບໃນ `sesler/yerel_katman.json`. ສຽງທີ່ປ່ຽນຊື່ແລ້ວ
  ຈະສະແດງທີ່ມາຂອງມັນເປັນສີເທົາ (*ຊື່ການສ້າງ · ຕົວເລືອກ N*); ⋯ → *ໄປທີ່ການສ້າງ* ຈະເປີດການອອກແບບຂອງມັນ.
- **ທາງລັດ ແລະ ໄຟລ໌.** Ctrl+Enter (⌘+Enter ເທິງ Mac) ເລີ່ມ *ອອກແບບ* ຫຼື *ອ່ານດ້ວຍສຽງນີ້* ໃນແຖບທີ່ເປີດຢູ່. ແຖບຄວາມຄືບໜ້າ
  ສະແດງ *ເວລາທີ່ຜ່ານໄປ / ~ທັງໝົດ*, ດ້ວຍການຄາດຄະເນທີ່ຮຽນຮູ້ຈາກວຽກກ່ອນໆໃນເຄື່ອງຂອງທ່ານ. ໄຟລ໌ທີ່ດາວໂຫຼດຈະຖືກຕັ້ງຊື່ຕາມ
  ສຽງ ແລະ ເວລາ (`Voice_Name_2026-11-02_0152.wav`).

**ການສຳເນົາສຽງ (ສຽງຂອງທ່ານເອງ ຫຼື ສຽງທີ່ໄດ້ຮັບການຍິນຍອມ).** ໃນແຖບ *ສຳເນົາສຽງ* ຂອງ UI, ໃສ່ການບັນທຶກຂອງທ່ານ
(wav/mp3/flac/ogg, ແນະນຳການເວົ້າທີ່ສະອາດ 5-30 s; ຕ່ຳກວ່າ 3 s ຈະຖືກປະຕິເສດ, ເກີນ 36 s ຈະຖືກຕັດ), ບົດຖອດຄວາມທີ່ຖືກຕ້ອງ
ຂອງມັນ ແລະ ຂໍ້ຄວາມທີ່ຈະອ່ານ. ປຸ່ມຈະຖືກປິດໄວ້ຈົນກວ່າທ່ານຈະໝາຍ "ສຽງນີ້ເປັນຂອງຂ້ອຍ ຫຼື ຂ້ອຍໄດ້ຮັບອະນຸຍາດຢ່າງຊັດເຈນຈາກເຈົ້າຂອງ".
ການບັນທຶກຈະໄປຫາ server ໃນເຄື່ອງ (127.0.0.1) ເທົ່ານັ້ນ, ຖືກປະມວນຜົນໃນ folder ຊົ່ວຄາວພ້ອມກັບ reference encoding ຂອງມັນ, ແລະ
folder ນັ້ນຈະຖືກລຶບເມື່ອວຽກສຳເລັດ, ເຖິງແມ່ນວ່າລົ້ມເຫຼວກໍຕາມ; ບໍ່ມີຫຍັງຖືກສົ່ງຜ່ານເຄືອຂ່າຍ. ມີແຕ່ຜົນລັບສັງເຄາະເທົ່ານັ້ນທີ່ຖືກເກັບໄວ້
(UI: `sesler/_okumalar/<job>/`, CLI: `--cikti`). ຜົນລັບແມ່ນ `klon_synthetic.wav` ພ້ອມປ້າຍ "synthetic"; ເມື່ອແບ່ງປັນ ໃຫ້ຕິດປ້າຍ
ວ່າສ້າງດ້ວຍ AI. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## ຄຳຖາມທີ່ພົບເລື້ອຍ

**Model ຫຼື engine? ອັນໃດແມ່ນອັນໃດ?** VoxCPM2 (OpenBMB) ແມ່ນ *model*: ເຄືອຂ່າຍທີ່ມີ 2 ພັນລ້ານພາຣາມິເຕີ ທີ່ປ່ຽນຂໍ້ຄວາມເປັນ
ສຽງເວົ້າ. audio.cpp ແມ່ນ *engine*: ໂປຣແກຣມ C++/CUDA ທີ່ແລ່ນ model ເທິງ GPU ຂອງທ່ານ (`audiocpp_cli.exe`). patch ຂອງພວກເຮົາ
ປ່ຽນ engine, ບໍ່ແມ່ນ model: ມັນເຮັດໃຫ້ VoxCPM2 ພໍດີກັບ 4 GB ແລະ ເຮັດໃຫ້ seed ດຽວກັນໃຫ້ສຽງດຽວກັນທຸກຄັ້ງ. Python package ໃນ
repo ນີ້ພຽງແຕ່ກະກຽມຂໍ້ຄວາມ, ເອີ້ນໃຊ້ engine ແລະ ລວບລວມໄຟລ໌.

**GPU ອັນໃດແດ່?** ເບິ່ງ "GPU ທີ່ຮອງຮັບ" ຂ້າງເທິງ: NVIDIA ຕັ້ງແຕ່ GTX 10xx ຂຶ້ນໄປ, VRAM 4 GB ຫຼື ຫຼາຍກວ່າ, driver ≥ 570.
native code ມີຢູ່ໃນ release ສຳລັບ sm_61/75/86/89/120a; ກາດອື່ນທີ່ເປັນ Pascal ຫຼື ໃໝ່ກວ່າໃຊ້ PTX ທີ່ຝັງໄວ້ (ການເລີ່ມຄັ້ງທຳອິດ
ຊ້າກວ່າ). AMD/Intel: zip Vulkan ແບບທົດລອງ, `kur.ps1 -Vulkan`; ຜູ້ໃຊ້ພາຍນອກຄົນໜຶ່ງລາຍງານວ່າໄດ້ແລ່ນມັນເທິງ AMD 6900 XT, ແຕ່
ຍັງຕ້ອງການການທົດສອບ AMD/Intel ທີ່ກວ້າງຂວາງກວ່ານີ້ (ເບິ່ງ "AMD / Intel" ຂ້າງເທິງ). ສະເພາະ CPU (`"backend": "cpu"` ໃນ
`ayarlar.json`) ແລ່ນໄດ້ ແຕ່ຊ້າກວ່າ GTX 1050 Ti ~6× (ການວັດແທກຂອງ engine, 535 s ທຽບກັບ 94 s ສຳລັບການເວົ້າ 48 s); ບໍ່ແມ່ນ
ທາງທີ່ຮອງຮັບ.

**ໄວປານໃດ?** ວັດແທກເທິງ GTX 1050 Ti 4 GB (i7-7700HQ): ໜຶ່ງຕົວເລືອກອອກແບບ (ການບັນທຶກ ≈ 25 s) 55 s; ການອ່ານ ≈ 2 s ຂອງ
ການຄຳນວນຕໍ່ການເວົ້າ 1 s (real-time factor 1.9-2.8) ຫຼັງຈາກ reference encoding ຄັ້ງດຽວ ~50 s ຕໍ່ສຽງ (ເກັບ cache ໄວ້ໃນ disk)
ແລະ ການໂຫຼດ model 10-20 s ຕໍ່ batch; VRAM ສູງສຸດ 2.6-2.9 GB. ກາດລຸ້ນໃໝ່ໄວກວ່າ; ຕົວເລກ ແລະ ວິທີການ: [docs/4gb.md](docs/4gb.md).

**ມັນສຳເນົາສຽງໄດ້ບໍ?** model VoxCPM2 ທີ່ຢູ່ເບື້ອງຫຼັງສາມາດຮຽນແບບສຽງຈາກການບັນທຶກອ້າງອີງໄດ້, ແລະ ສ່ວນສຳເນົາສຽງໃຊ້ຄວາມສາມາດ
ນັ້ນ. ໃຊ້ມັນສະເພາະກັບສຽງຂອງທ່ານເອງ ຫຼື ໂດຍໄດ້ຮັບອະນຸຍາດຢ່າງຊັດເຈນຈາກເຈົ້າຂອງສຽງເທົ່ານັ້ນ; UI ຈະຂໍໃຫ້ທ່ານຢືນຢັນການອະນຸຍາດນັ້ນ.
ການອອກແບບສຽງບໍ່ຕ້ອງການການບັນທຶກ: ມັນເລີ່ມຈາກຄຳອະທິບາຍເປັນຂໍ້ຄວາມພາສາອັງກິດ ຫຼື ຈີນ, ແລະ "ສຽງອ້າງອີງ" ທີ່ໃຊ້ອ່ານສຽງທີ່ອອກແບບ
ແມ່ນການບັນທຶກອອກແບບສັງເຄາະຂອງ model ເອງ. ການປອມຕົວເປັນຄົນອື່ນ, ການສໍ້ໂກງ ແລະ ການຫຼອກລວງເປັນສິ່ງຕ້ອງຫ້າມ. ເບິ່ງ
[ETHICS.md](ETHICS.md). ໃຫ້ຕິດປ້າຍສິ່ງທີ່ທ່ານເຜີຍແຜ່ວ່າສ້າງດ້ວຍ AI.

**ຂຽນຄຳອະທິບາຍສຽງທີ່ດີແນວໃດ?** ເປັນພາສາອັງກິດ, 1-3 ປະໂຫຍກ: ອາຍຸ ແລະ ເພດ, ສີສັນສຽງ (ທຸ້ມ/ໃສ, ອົບອຸ່ນ, ອອກດັງ, ແຫບ),
ນ້ຳສຽງ ແລະ ບົດບາດ (ຜູ້ບັນຍາຍສາລະຄະດີທີ່ສະຫງົບ, ພິທີກອນທີ່ມີພະລັງ), ຈັງຫວະ (ຊ້າ, ພໍດີ), ແລະ "clean studio recording, no
background noise". ໃຫ້ມັນເປັນຄຳອະທິບາຍ, ບໍ່ແມ່ນບົດອ່ານ; ບໍ່ມີວົງເລັບ. ຂໍ 3-5 ຕົວເລືອກ ແລ້ວຟັງ: seed ປ່ຽນສຽງຫຼາຍ. ສຳລັບຂໍ້ຄວາມ
ສ້າງສຽງ ໃຊ້ 1-3 ປະໂຫຍກທີ່ເປັນທຳມະຊາດໃນພາສາຂອງສຽງ, ໃນອາລົມທີ່ທ່ານຕ້ອງການ (ສູງສຸດ ~30 s ຂອງການເວົ້າ). ເມື່ອອ່ານ, ໜຶ່ງປະໂຫຍກ
ຕໍ່ໜຶ່ງແຖວ; ແບ່ງປະໂຫຍກຍາວ, ຂຽນຕົວເລກເປັນຄຳ.

## ການມີສ່ວນຮ່ວມ

ບໍ່ຮູ້ວ່າຈະເລີ່ມຈາກໃສ? issue ນ້ອຍໆສີ່ອັນນີ້ເປັນບາດກ້າວທຳອິດທີ່ດີ:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) ລອງໃຊ້ເທິງ GPU ຂອງທ່ານ ແລະ ລາຍງານກາດ, driver ແລະ ເວລາ
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: ລອງ build Vulkan ແບບທົດລອງ
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) ເພີ່ມປະໂຫຍກໃສ່ຊຸດທົດສອບ
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) ແບ່ງປັນສຽງທີ່ທ່ານອອກແບບ ພ້ອມຄຳອະທິບາຍ ແລະ seed ຂອງມັນ

**ທົດສອບກາດຈໍຂອງທ່ານ ແລ້ວຂຽນລາຍງານ:** ບໍ່ຈຳເປັນຕ້ອງຂຽນໂຄດ, ພຽງແຕ່ໃຊ້ [ແບບຟອມລາຍງານການທົດສອບຮາດແວ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); ຍັງບໍ່ມີລາຍງານຈາກກາດຈໍ Intel ເທື່ອ.

ຊຸດທົດສອບລວມ: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); ຄູ່ມືສຽງແບຣນ:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); ວິທີສົ່ງລະຫັດ: [CONTRIBUTING.md](CONTRIBUTING.md).
ບັນຫາການຕິດຕັ້ງ: [ແບບຟອມ issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); ຄຳຖາມ ແລະ ຜົນລັບ: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
ທຸກຄົນທີ່ເຂົ້າຮ່ວມປະຕິບັດຕາມ [ຈັນຍາບັນ](CODE_OF_CONDUCT.md): ມີນ້ຳໃຈ, ໃຫ້ຄຳຕິຊົມກ່ຽວກັບຜົນງານ.

## ຜູ້ມີສ່ວນຮ່ວມ

- [@alexturkey](https://github.com/alexturkey): ຜູ້ດູແລ; ລະຫັດ, ສຽງສຳເລັດຮູບ, ເອກະສານ
- [@cayir21](https://github.com/cayir21): ການຮອງຮັບ Metal ສຳລັບ macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): ການແກ້ໄຂທ້າຍປະໂຫຍກ (EOS) ສຳລັບການອ່ານຫຼາຍປະໂຫຍກເທິງ CPU backend, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): ການຕິດຕັ້ງ CUDA ແບບທົດລອງສຳລັບ Ubuntu/Linux ແລະ ການຮອງຮັບ Docker, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

ຊື່ຂອງທ່ານກໍຄວນຢູ່ທີ່ນີ້ເຊັ່ນກັນ: ຜົນທົດສອບຈາກ GPU ຂອງທ່ານ, ປະໂຫຍກສຳລັບຊຸດທົດສອບ, ສຽງທີ່ທ່ານອອກແບບ, ລາຍງານ bug ທີ່ຊັດເຈນ
ຫຼື pull request ລ້ວນນັບເປັນການມີສ່ວນຮ່ວມ. ຂອບໃຈທຸກຄົນທີ່ລອງໃຊ້ ແລະ ຂຽນກັບມາຫາພວກເຮົາ.

## ລິຂະສິດ ແລະ ການໃຫ້ກຽດ

ລະຫັດ ແລະ ສຽງສຳເລັດຮູບ: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. ສ້າງຂຶ້ນເທິງ VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) ແລະ ການແປງ audio.cpp GGUF. ລາຍການເຕັມ: [THIRD_PARTY.md](THIRD_PARTY.md). ບໍ່ມີ
ສ່ວນກ່ຽວຂ້ອງກັບ OpenBMB, ModelBest ຫຼື ໂຄງການ audio.cpp.

[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · **ខ្មែរ** · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**ការរចនាសំឡេងភាសាទួរគីជាមួយ VoxCPM2 លើ GPU 4 GB។** ពិពណ៌នាសំឡេងមួយជាភាសាអង់គ្លេស ឱ្យ model បង្កើតវា ជ្រើសរើសជម្រើស
ដែលអ្នកចូលចិត្ត រួចអានអត្ថបទភាសាទួរគីណាមួយដោយសំឡេងនោះ។ គម្រោងនេះមាន installer ដែលដំណើរការដោយពាក្យបញ្ជាតែមួយ engine
[audio.cpp](https://github.com/0xShug0/audio.cpp) ដែលបានកែសម្រួលឱ្យសមនឹង GTX 1050 Ti (4 GB) web UI តូចមួយដែលដំណើរការក្នុង
ម៉ាស៊ីនរបស់អ្នក និងសំឡេងសំយោគ (synthetic) ដែលមានស្រាប់ចំនួនដប់បួន៖ សំឡេងទួរគីប្រាំពីរ និងអ្នកនិទានជនជាតិដើមប្រាំពីរនាក់
ជាភាសាអង់គ្លេស បារាំង អាល្លឺម៉ង់ អេស្ប៉ាញ រុស្ស៊ី ចិន និងជប៉ុន។

- កម្មវិធីអានបាន 30 ភាសា ហើយផ្ទៃប្រើប្រាស់ (interface) ក៏មាន 30 ភាសាដែរ។
- សំឡេងមានស្រាប់ 14៖ ទួរគី 7 បូកនឹងមួយសម្រាប់ភាសានីមួយៗ គឺអង់គ្លេស បារាំង អាល្លឺម៉ង់ អេស្ប៉ាញ រុស្ស៊ី ចិន និងជប៉ុន។
- Web UI (v0.2.0)៖ កាតជម្រើសនីមួយៗមានសំឡេងពីរ គឺសំឡេងរចនាដើម និងសំឡេងដែលអ្នកនឹងឮជានិច្ច បញ្ជីអានដែលមាន menu សំឡេង
  ការប្ដូរឈ្មោះ លាក់ ឬលុបសំឡេង និងសេចក្តីព្រាងសម្រាប់អត្ថបទដែលអ្នកអាន។ សូមមើល "Web UI" នៅក្រោម "ការប្រើប្រាស់"។

[របៀបដែលវាសមនឹង 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [មគ្គុទ្ទេសក៍ដំឡើងសម្រាប់ភ្នាក់ងារ AI](AGENTS.md) · [ការប្រើប្រាស់ប្រកបដោយការទទួលខុសត្រូវ](ETHICS.md)

> សំឡេងដែលភ្ជាប់មកជាមួយគឺជាសំឡេងសំយោគ ដែលរចនាចេញពីការពិពណ៌នាជាអត្ថបទ។ ផ្នែកចម្លងសំឡេងគឺសម្រាប់តែសំឡេងរបស់អ្នកផ្ទាល់
> ឬសំឡេងដែលប្រើដោយមានការអនុញ្ញាតច្បាស់លាស់ពីម្ចាស់ប៉ុណ្ណោះ ហើយ UI នឹងសុំឱ្យអ្នកបញ្ជាក់ការអនុញ្ញាតនោះ។ ការក្លែងខ្លួនជាអ្នកដទៃ
> ការក្លែងបន្លំ និងការបោកប្រាស់ត្រូវបានហាមឃាត់។ សូមដាក់ស្លាកថាអ្វីដែលអ្នកបង្កើតគឺបង្កើតដោយ AI។ សូមមើល [ETHICS.md](ETHICS.md)។

## 30 ភាសា

យើងបានធ្វើវីដេអូឯកសារអំពីតំបន់កាប៉ាដូចៀ (Cappadocia) មួយជា 8 ភាសា៖ ទួរគី អង់គ្លេស បារាំង អាល្លឺម៉ង់ អេស្ប៉ាញ រុស្ស៊ី ចិន
និងជប៉ុន។ ភាសានីមួយៗមាន **អ្នកនិទានជនជាតិដើម** ផ្ទាល់ខ្លួន ដែលរចនាដោយ VoxCPM2 ពីការពិពណ៌នាជាភាសាអង់គ្លេស។ ទាំងអស់ត្រូវបាន
បង្កើតក្នុងម៉ាស៊ីនផ្ទាល់ទាំងស្រុងលើ GTX 1050 Ti 4 GB ដោយគុណភាពថេរដូចគ្នា (16 ជំហាន cfg 2.0)។ អ្នកនិទានទាំងប្រាំពីរនាក់ត្រូវបាន
ភ្ជាប់មកទីនេះ ជាមួយ prompt អត្ថបទរចនា seed និងការថតសំឡេងយោង (reference) របស់ពួកគេ។

| កូដ | ភាសា | សំឡេង | ស្តាប់ | វីដេអូ |
|---|---|---|---|---|
| `tr` | ទួរគី | `hazir/belgesel_hanim` (និង 6 ទៀត) | [គំរូ](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | អង់គ្លេស | `hazir/anlatici_en` | [គំរូ](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113791986763440439) |
| `fr` | បារាំង | `hazir/anlatici_fr` | [គំរូ](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113790681575804962) |
| `de` | អាល្លឺម៉ង់ | `hazir/anlatici_de` | [គំរូ](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113791351645262249) |
| `es` | អេស្ប៉ាញ | `hazir/anlatici_es` | [គំរូ](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113807365611122705) |
| `ru` | រុស្ស៊ី | `hazir/anlatici_ru` | [គំរូ](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113801574136848884) |
| `zh` | ចិន (កុកងឺ) | `hazir/anlatici_zh` | [គំរូ](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113802229606121794) |
| `ja` | ជប៉ុន | `hazir/anlatici_ja` | [គំរូ](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [វីដេអូ](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**ហេតុអ្វីអានម្តងមួយប្រយោគ។** VoxCPM2 មិនមានស្ថិរភាពសម្រាប់ការបង្កើតវែងតែមួយដង (ប្រហែលលើសពី 30 វិនាទី) ទេ៖ ចង្វាក់កាន់តែលឿន
ហើយសំឡេងអាចរសាត់ចេញ។ នៅទីនេះ សំឡេងត្រូវបានរក្សាដោយការថតសំឡេងយោង និង seed ថេរ ហើយអត្ថបទវែងត្រូវបានអានមួយប្រយោគក្នុង
មួយបន្ទាត់ ដូច្នេះពណ៌សំឡេង និងរចនាប័ទ្មនៅដដែលចាប់ពីប្រយោគទីមួយរហូតដល់ប្រយោគចុងក្រោយ។ សម្រាប់ភាសាក្រៅពីទួរគី វចនានុក្រម
បញ្ចេញសំឡេងទួរគីមិនត្រូវបានអនុវត្តទេ។ ភាសាទាំង 30 ដែល VoxCPM2 គាំទ្រត្រូវបានសាកល្បង ហើយដំណើរការបាន សម្រាប់ភាសាដែលគ្មាន
សំឡេងភ្ជាប់មកជាមួយ សូមប្រើ `--dil <code>`។ ពាក្យបញ្ជាតាមភាសានីមួយៗ និងមេរៀនដែលយើងបានរៀន៖ [docs/cok_dilli.md](docs/cok_dilli.md)។
Claude Code skill សម្រាប់លំហូររចនាទាំងមូល៖ [.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md)។

**prompt គំរូ 144 សម្រាប់ចាប់ផ្តើម។** តួនាទី 18 (អ្នកនិទានឯកសារ អ្នកអានព័ត៌មាន សំឡេងពាណិជ្ជកម្ម សៀវភៅជាសំឡេង យាយនិទានរឿង
ម្ចាស់កម្មវិធី podcast គ្រូបង្រៀន trailer ភាពយន្ត អ្នកណែនាំសមាធិ អ្នកអត្ថាធិប្បាយកីឡា និងច្រើនទៀត ទាំងប្រុស និងស្រី) ក្នុងភាសានីមួយៗ
ទាំង 8។ prompt ជាភាសាអង់គ្លេស ដោយបញ្ជាក់សញ្ជាតិ និងសំនៀងដើមរបស់អ្នកនិយាយ ហើយអត្ថបទដែលអានពេលកំពុងបង្កើតសំឡេងក៏ភ្ជាប់មកជាមួយ
ជាភាសានោះ និងស្របនឹងតួនាទី។ ជ្រើសមួយ ស្តាប់ជម្រើសនានា ហើយរក្សាទុកមួយដែលអ្នកចូលចិត្ត៖
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3` ឬជ្រើស *ការពិពណ៌នាគំរូ* នៅក្នុង web UI។ បញ្ជីពេញ៖
[docs/ornek_tarifler.md](docs/ornek_tarifler.md)។

**បញ្ចូលសំឡេងវីដេអូរបស់អ្នកដោយសំឡេងផ្ទាល់ខ្លួន។** [DubWorld](https://github.com/alexturkey/dubworld) គឺជាកម្មវិធី dubbing
វីដេអូរបស់យើងដែលដំណើរការក្នុងម៉ាស៊ីនផ្ទាល់ វាដំឡើង repository នេះជា engine សំឡេង VoxCPM2 របស់វា។ សំឡេងដែលអ្នករចនានៅទីនេះ
ត្រូវបានប្រើនៅទីនោះជាមួយ `ses.voxcpm2_ses = "<name>/<variant>"`។

## ចាប់ផ្តើមរហ័ស (Windows, 3 ជំហាន)

1. **ទាញយក** កូដ៖ [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip)។
   កញ្ចប់ engine ដែលរៀបចំរួចសម្រាប់កាតរបស់អ្នក នឹងត្រូវបាន installer ទាញយកនៅជំហានទី 3៖
   NVIDIA → [កញ្ចប់ CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [កញ្ចប់ Vulkan ពិសោធន៍](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (បានទាញយកមួយរួចហើយ? បន្ថែម `-HazirZip <path to the zip>` ទៅពាក្យបញ្ជាខាងក្រោម)។
2. **ពន្លា** zip បើក folder `voxcpm2-turkce-ses-tasarimi-main` វាយ `powershell` នៅរបារអាសយដ្ឋានរបស់ Explorer
   ហើយចុច Enter។
3. **ដំណើរការ** installer (ត្រូវការ Python 64-bit 3.10-3.13 និង NVIDIA driver ≥ 570 សម្រាប់ CUDA) បន្ទាប់មកចុចពីរដងលើ **`baslat.bat`**៖
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel៖ បន្ថែម `-Vulkan` នៅចុងបញ្ចប់។ UI បើកនៅ http://127.0.0.1:8765/។

zip របស់ engine មិនមែនជាកម្មវិធីឯករាជ្យទេ (exe របស់វាត្រូវការ model និង DLL ដែល installer រៀបចំឱ្យ)។ ព័ត៌មានលម្អិត
បញ្ជី GPU និងបញ្ហាទូទៅ៖ សូមមើល "ដំឡើងរហ័ស" ខាងក្រោម។

## Ubuntu / Linux (NVIDIA CUDA, ពិសោធន៍)

Build engine ដែលបានកែសម្រួលដោយ `bash scripts/kur-linux.sh` ឬប្រើ `Dockerfile.linux` ដើម្បី build និងដំណើរការក្នុង
បរិស្ថាន Ubuntu 24.04 / CUDA 12.8.1។ ត្រូវការ NVIDIA GPU និង driver ដែលត្រូវគ្នា installer ផ្ទាល់ក៏ត្រូវការ CUDA toolkit និង
Python 3.10-3.13 ដែរ។ UI នៅតែស្តាប់តែលើ loopback ប៉ុណ្ណោះ សូម្បីតែលើ server ពីចម្ងាយ (SSH forwarding)។ លក្ខខណ្ឌតម្រូវ ពាក្យបញ្ជា
ការជ្រើសរើស architecture និងវិសាលភាពនៃការផ្ទៀងផ្ទាត់៖ [docs/linux.md](docs/linux.md)។

## ចាប់ផ្តើមរហ័ស (macOS, Apple Silicon)

ត្រូវការ Xcode Command Line Tools (`xcode-select --install`) និង [Homebrew](https://brew.sh)៖
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
installer ទាញយក model, build engine ដែលបានកែសម្រួលជាមួយ Metal (~1 នាទី) ហើយរៀបចំអ្វីៗទាំងអស់នៅក្រោម `~/vox`។
បន្ទាប់មកចុចពីរដងលើ **`baslat.command`**។ លើ MacBook Air M4 16 GB៖ ការគណនា ~2 s សម្រាប់ការនិយាយ 1 s, seed ដូចគ្នាផ្តល់
សំឡេងដូចគ្នាគ្រប់ byte, RAM ខ្ពស់បំផុត ~5.3 GB, គ្មានការយឺតដោយសារកំដៅក្នុងរយៈពេល 12 នាទីនៃការអានជាប់គ្នា។ ព័ត៌មានលម្អិត
និងការវាស់វែង៖ [docs/mac.md](docs/mac.md)។

**កម្មវិធី Mac ដើម (គ្មាន Python, Homebrew ឬ Terminal)៖** [macos/README.md](macos/README.md)។ វាភ្ជាប់មកជាមួយ engine
ដែលបានកែសម្រួលដូចគ្នា ហើយទាញយក model នៅពេលបើកលើកដំបូង សម្រាប់ពេលនេះ វាត្រូវបាន build ពី source ដោយ Xcode។

## សម្រាប់អ្នកប្រើ Mac (Apple Silicon)

មានកំណែកែសម្រួលឯករាជ្យមួយទៀតដែលសហគមន៍បង្កើតសម្រាប់ Mac ដែលប្រើ Apple Silicon ដែលដំណើរការ VoxCPM2 ជាមួយ framework MLX
របស់ Apple៖ **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**។
វាត្រូវបានអភិវឌ្ឍ និងថែទាំដោយ Emre Koç ([@emre-koc](https://github.com/emre-koc)) នៅក្នុង repository ផ្ទាល់ខ្លួនរបស់គាត់ មិនមែន
នៅទីនេះទេ ជំហានដំឡើង និងសំណួរជំនួយសូមទៅទីនោះ។ សូមអរគុណ Emre ដែលបាននាំគម្រោងនេះមកកាន់ Mac!

## របៀបដែលវាដំណើរការ

1. **ការរចនាសំឡេង។** *ការពិពណ៌នាសំឡេង* ជាភាសាអង់គ្លេស + *អត្ថបទដែលអានពេលកំពុងបង្កើតសំឡេង* (ជាភាសារបស់សំឡេង) + ចំនួន
   ជម្រើស។ ជម្រើសនីមួយៗទទួលបាន seed ផ្ទាល់ខ្លួន engine ទទួល `(description)text` ហើយផ្តល់ការថតរចនាមួយសម្រាប់ seed នីមួយៗ។
   អត្ថបទគឺជាគំរូខ្លីដើម្បីស្គាល់សំឡេង៖ 1-2 ប្រយោគ យ៉ាងច្រើន ~20 s (UI បង្ហាញការប៉ាន់ស្មាន ហើយមិនចាប់ផ្តើមទេបើលើស 22 s)
   អត្ថបទវែងគឺសម្រាប់ជំហានទី 2។
2. **ការអានផ្អែកលើសំឡេងយោង។** ការថតរចនាត្រូវបានបញ្ជូនទៅធាតុបញ្ចូល **ទាំងពីរ** របស់ engine (`audio` និង `voice_ref`)
   រួមជាមួយអត្ថបទចម្លងរបស់វា (`reference_text`) និងអត្ថបទថ្មីដែលត្រូវអាន ដោយ seed ដូចគ្នា។ សំឡេងត្រូវបានរក្សាដោយការថត
   មិនមែនដោយការពិពណ៌នាទេ ដូច្នេះវាមិនរសាត់ពីអត្ថបទមួយទៅអត្ថបទមួយទៀតឡើយ។ អត្ថបទត្រូវបានអានម្តងមួយប្រយោគ។
3. គុណភាពគឺថេរ៖ diffusion 16 ជំហាន CFG 2.0។ seed មិនមែនជាប៊ូតុងកែគុណភាពទេ។

ការថតរចនាដើមគឺជាគំរូសំឡេងតែម្តងគត់ គ្មានការអាននៅពេលក្រោយណាមួយស្តាប់ទៅដូចវាទាំងស្រុងទេ។ អ្វីដែលអ្នកឮនៅក្នុងការអាន
ពេលក្រោយគ្រប់ដងគឺជំហានទី 2៖ ការថតរចនាជាសំឡេងយោង បូកនឹង seed ផ្ទាល់ខ្លួនរបស់ជម្រើស។ ហេតុនេះហើយ web UI ធ្វើជំហានទី 2
ភ្លាមៗបន្ទាប់ពីការរចនា ហើយបង្ហាញទាំងពីរនៅលើកាតជម្រើស។

engine គឺ audio.cpp v0.7.2 ជាមួយ patch របស់យើង (`patches/`) ហើយ model គឺ VoxCPM2 Q8_0 GGUF។ VRAM ខ្ពស់បំផុត ≈ 2.8 GB
ការគណនាប្រហែល 2 s សម្រាប់ការនិយាយ 1 s លើ GTX 1050 Ti។ ព័ត៌មានលម្អិត និងការវាស់វែង៖ [docs/4gb.md](docs/4gb.md)។

## សំឡេងដែលភ្ជាប់មកជាមួយ (`hazir_sesler/`)

ទាំងដប់បួនត្រូវបានរចនាចេញពី prompt ដែលរក្សាទុកក្នុង `ses.json` របស់វា គ្មានមួយណាត្រូវបានចម្លងពីការថតទេ (ការចម្លងគឺជា tab
*ចម្លងសំឡេង* ដាច់ដោយឡែក ដែលតម្រូវឱ្យមានការយល់ព្រម)។

| សំឡេង | ការពិពណ៌នាខ្លី | ស្តាប់ |
|---|---|---|
| `belgesel_hanim` | ស្ត្រីពេញវ័យអាយុហាសិបជាង alto ជ្រៅ និងកក់ក្តៅ អ្នកនិទានឯកសារដ៏ស្ងប់ស្ងាត់ | [គំរូ](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | អ្នកនិទានប្រុសសំឡេងជ្រៅ ខ្លាំង និងអាថ៌កំបាំង | [គំរូ](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | អ្នកអានព័ត៌មានដែលមានបទពិសោធអាយុប្រហែលចិតសិប ស្ងប់ស្ងាត់ និងមានអំណាច | [គំរូ](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | អ្នកអានព័ត៌មានពេលល្ងាចស្ត្រីអាយុសាមសិបជាង មានមន្តស្នេហ៍ សំឡេងទន់ដូចក្រណាត់ velvet និងពោរពេញអារម្មណ៍ | [គំរូ](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | មេធ្មប់ក្នុងរឿងនិទាន៖ សំឡេងទាប ច្រមុះបន្តិច ផ្អែមបែបល្បិចកល | [គំរូ](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | អ្នកនិទានប្រុសសំឡេងជ្រៅខុសធម្មតា ក្រាស់ និងមានអំណាចបញ្ជា | [គំរូ](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | តាចាស់ឈ្លាសវៃ សំឡេងជ្រៅ និងលាន់ឮ អាថ៌កំបាំងបន្តិច | [គំរូ](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសាអង់គ្លេស អាយុហាសិបជាង (General American) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសាបារាំង អាយុហាសិបជាង (ប៉ារីស) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសាអាល្លឺម៉ង់ អាយុហាសិបជាង (Hochdeutsch) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសាអេស្ប៉ាញ អាយុហាសិបជាង (Castilian (ម៉ាឌ្រីដ)) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសារុស្ស៊ី អាយុហាសិបជាង (មូស្គូ) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសាចិន (កុកងឺ) អាយុហាសិបជាង (Putonghua ប៉េកាំង) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | អ្នកនិទានឯកសារប្រុសជនជាតិដើមភាសាជប៉ុន អាយុហាសិបជាង (ស្តង់ដារតូក្យូ) ជ្រៅ ស្ងប់ កក់ក្តៅ | [គំរូ](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [សំឡេងយោង](hazir_sesler/anlatici_ja/referans.flac) |

folder នីមួយៗ៖ `referans.flac` (ការថតរចនាដែលមិនបាត់បង់គុណភាព) `ses.json` (prompt អត្ថបទចម្លង seed រចនា seed អាន
ការពិពណ៌នា និង `dil` = ភាសាសម្រាប់អ្នកនិទាន) `ornek_okuma.mp3` (+ អត្ថបទរបស់វា)។ ប្រើវាដោយផ្ទាល់៖ `--ses hazir/<name>`។
ការថតសំឡេងយោងរបស់អ្នកនិទានគឺខ្លី (5.6-10 s) គំរូរបស់ពួកគេគឺបីប្រយោគដំបូងនៃអត្ថបទកាប៉ាដូចៀ ដែលកាត់ចេញពីការអាន
ផលិតកម្មពេញលេញ។

## ដំឡើងរហ័ស មិនត្រូវការ compiler (Windows 10/11, NVIDIA GPU ≥ 4 GB)

លក្ខខណ្ឌតម្រូវ៖ NVIDIA driver ≥ 570 និង Python 64-bit 3.10-3.13 (`winget install Python.Python.3.12`)។ គ្មានអ្វីផ្សេងទៀតទេ៖
គ្មាន Visual Studio គ្មាន CUDA installer។ មិនប្រាកដថាអ្នកមានកាតអ្វី? ដំណើរការ `nvidia-smi` ក្នុង PowerShell៖ វាបង្ហាញឈ្មោះ
GPU កំណែ driver និងអង្គចងចាំ។ គ្មានកាត NVIDIA? សូមមើល "AMD / Intel" ខាងក្រោម។

ជាមួយ [Git](https://git-scm.com/download/win)៖

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

គ្មាន Git៖ នៅលើទំព័រនេះ ចុច **Code → Download ZIP** ពន្លាវា បើក folder `voxcpm2-turkce-ses-tasarimi-main` ដែលបាន
ពន្លា វាយ `powershell` នៅរបារអាសយដ្ឋានរបស់ Explorer ហើយចុច Enter រួចដំណើរការបន្ទាត់ចុងក្រោយខាងលើ។ Git ត្រូវការតែ
សម្រាប់ផ្លូវ build ពី source ប៉ុណ្ណោះ។

`-ExecutionPolicy Bypass` អនុវត្តចំពោះតែ process នេះមួយប៉ុណ្ណោះ ហើយមិនផ្លាស់ប្តូរការកំណត់ប្រព័ន្ធណាមួយទេ សូមអាន
`scripts\kur.ps1` មុនពេលដំណើរការ ដូចជាស្គ្រីបដំឡើងណាមួយដែរ។ ពាក្យបញ្ជាតែមួយ ~10 នាទី ទាញយក ~3.7 GB ហើយអ្វីៗទាំងអស់
ត្រូវបានផ្ទៀងផ្ទាត់ដោយ sha256៖ model (2.95 GB) DLL runtime របស់ CUDA 12.8 ជា zip ចល័ត (មិនដំឡើងក្នុងប្រព័ន្ធ មិនប៉ះ PATH)
**engine ដែល build រួច** ពីទំព័រ Releases `.venv` ដែលមានកញ្ចប់ Python ពីរ `ayarlar.json` និងការពិនិត្យ GPU ចុងក្រោយ
(`KONTROL_OK`)។ ដំណើរការវាម្តងទៀតបន្ទាប់ពីការបរាជ័យណាមួយ ឯកសារដែលបានផ្ទៀងផ្ទាត់រួចនឹងត្រូវរំលង។ បន្ទាប់មកចាប់ផ្តើម web UI៖
ចុចពីរដងលើ **`baslat.bat`** នៅក្នុង folder repo។ វាចាប់ផ្តើម UI ហើយបើក **http://127.0.0.1:8765/** ក្នុង browser របស់អ្នក
នៅពេលរួចរាល់ បិទបង្អួចខ្មៅ (ឬចុច Ctrl+C នៅទីនោះ) ដើម្បីបញ្ឈប់វា។ ដូចគ្នាពី PowerShell៖

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
បន្ទាប់មកបើក **http://127.0.0.1:8765/** ដោយខ្លួនឯង (ពេលចាប់ផ្តើមតាមរបៀបនេះ UI មិនបើក browser ទេ វាស្តាប់តែលើ
localhost ប៉ុណ្ណោះ)។

> **`audiocpp_cli.exe` នៅក្នុង zip របស់ release មិនមែនសម្រាប់ចុចពីរដងទេ។** វាគឺជា engine បន្ទាត់ពាក្យបញ្ជា ដែលត្រូវការ
> DLL របស់ CUDA និង model នៅក្បែរវា `kur.ps1` ដាក់អ្វីៗទាំងអស់ឱ្យនៅកន្លែង ហើយកញ្ចប់ Python ជាអ្នកបញ្ជាវា។ ការចុចពីរដងលើវា
> គ្រាន់តែបង្ហាញ "cudart64_12.dll not found" ប៉ុណ្ណោះ។

**GPU ដែលគាំទ្រ (release v0.1.1)៖** native code សម្រាប់ GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) និង RTX 50xx (sm_120a) GPU CUDA ផ្សេងទៀតណាមួយចាប់ពី Pascal ឡើងទៅ ដំណើរការ PTX ដែលបង្កប់ តាមរយៈ driver
(ការចាប់ផ្តើមលើកដំបូងយឺតជាង)។ Maxwell (GTX 9xx) និងចាស់ជាងនេះមិនត្រូវបាន CUDA 12.8 គាំទ្រទេ។ យើងបានសាកល្បងលើ
GTX 1050 Ti 4 GB (ក៏តាមរយៈ Docker Desktop/WSL2 លើ Windows ដែរ CLI ប៉ុណ្ណោះ) វាស់វែងដោយ @mslmyilmaz5 (#15)៖ RTX 3060 Ti 8 GB,
Ubuntu 24.04 Docker, CUDA 12.8.1 (ព័ត៌មានលម្អិតក្នុង [docs/linux.md](docs/linux.md))។ យើងស្វាគមន៍របាយការណ៍ពីកាតផ្សេងទៀត
នៅក្នុង [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)។

**AMD / Intel (ពិសោធន៍)៖** zip engine Vulkan ដាច់ដោយឡែក (`...-win64-vulkan.zip`, គ្មាន CUDA) ដំឡើងដោយ
`scripts\kur.ps1 -Kok C:\vox -Vulkan`។ វាត្រូវបានផ្ទៀងផ្ទាត់តែលើកាត NVIDIA របស់យើងតាមរយៈ Vulkan backend ប៉ុណ្ណោះ (នៅទីនោះ
វាដំណើរការយឺតជាង CUDA ប៉ុន្តែផ្តល់សំឡេងដូចគ្នាសម្រាប់ seed ដូចគ្នា ការវាស់វែងនោះធ្វើឡើងខណៈ disk រវល់ជាមួយការងារផ្សេង ដូច្នេះ
ការប្រៀបធៀបល្បឿនស្អាតនៅមិនទាន់មានទេ) ហើយយើង **មិនទាន់** បានសាកល្បងវាលើ hardware AMD ឬ Intel ដោយខ្លួនឯងទេ៖ បើអ្នក
សាកល្បង សូមបង្ហោះលទ្ធផលនៅក្នុង Discussions។ បើមានឧបករណ៍ Vulkan ច្រើនជាងមួយ (integrated + discrete) installer សរសេរលេខ
index របស់ GPU discrete ជា `cihaz` ទៅក្នុង `ayarlar.json`។

**ចំណាំ៖** ការគាំទ្រ Vulkan បច្ចុប្បន្ននៅជាការពិសោធន៍។ វាត្រូវបាន build និងសាកល្បងដោយជោគជ័យលើ GTX 1050 Ti។ អ្នកប្រើខាងក្រៅ
ម្នាក់ (mitra_tr) ក៏បានរាយការណ៍ថាបានដំណើរការវាលើ AMD 6900 XT ដែរ។ នៅតែត្រូវការការសាកល្បងទូលំទូលាយជាងនេះលើកាត AMD/Intel។

### ជម្រើសផ្សេង៖ build engine ពី source

ត្រូវការ Visual Studio 2022 Build Tools ជាមួយ "Desktop development with C++" (រួមទាំង C++ CMake tools) ~7 GB។ បន្ទាប់មក៖

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
វាក៏ទាញយក nvcc យក source របស់ audio.cpp v0.7.2 អនុវត្ត `patches/0001-voxcpm2-4gb-ve-hiz.patch` ហើយ build សម្រាប់ GPU
របស់អ្នក (`-Mimari native` លំនាំដើម ឬឧទាហរណ៍ `-Mimari 61`) ~15-25 នាទី។ រក្សា root ឱ្យខ្លី (`C:\vox`)៖ nvcc បរាជ័យលើ
ផ្លូវវែង។ ជំហានម្តងមួយៗជាមួយការពិនិត្យ៖ [AGENTS.md](AGENTS.md)។

### បញ្ហាដំឡើងទូទៅ

| អ្វីដែលអ្នកឃើញ | អត្ថន័យ និងអ្វីដែលត្រូវធ្វើ |
|---|---|
| `cudart64_12.dll not found` បន្ទាប់ពីចុចពីរដងលើ exe | engine មិនមែនសម្រាប់ចាប់ផ្តើមដោយដៃទេ។ ដំណើរការពាក្យបញ្ជា `kur.ps1` ខាងលើ បន្ទាប់មកចាប់ផ្តើម web UI។ |
| `64-bit Python 3.10+ bulunamadı` (រកមិនឃើញ Python) | ដំឡើង Python (`winget install Python.Python.3.12`) បិទ PowerShell បើកមួយថ្មី ហើយដំណើរការពាក្យបញ្ជាដដែលម្តងទៀត។ |
| `motor ekran kartını görmedi` (engine មិនឃើញ GPU) | ធ្វើបច្ចុប្បន្នភាព NVIDIA driver ទៅ 570 ឬថ្មីជាងនេះ ពិនិត្យថា `nvidia-smi` ដំណើរការបាន។ |
| `indirme başarısız` / `sha256 tutmadı` (ទាញយកបរាជ័យ / checksum មិនត្រូវគ្នា) | ជាធម្មតាគឺការទាញយកដែលដាច់ពាក់កណ្តាលទី។ ដំណើរការពាក្យបញ្ជាដដែលម្តងទៀត ឯកសារដែលបានផ្ទៀងផ្ទាត់នឹងត្រូវរំលង។ |
| ផ្លូវ build៖ `nvcc` បរាជ័យ | រក្សា root ដំឡើងឱ្យខ្លី (`-Kok C:\vox`)។ |
| ទំព័រមិនបើក | ចាប់ផ្តើម UI ដោយ `baslat.bat` ឬបើក http://127.0.0.1:8765/ ដោយខ្លួនឯង។ port កំពុងជាប់រវល់? ប្តូរ `"port"` នៅក្នុង `ayarlar.json`។ |

មានបញ្ហា? [Discussions (សំណួរ-ចម្លើយ)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) ឬ
[issue អំពីការដំឡើង](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
ជាមួយ GPU របស់អ្នក កំណែ Windows ពាក្យបញ្ជា និងបន្ទាត់ចុងក្រោយរបស់វា។

## ការប្រើប្រាស់

បន្ទាត់ពាក្យបញ្ជា៖
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
ច្បាប់អត្ថបទ៖ សរសេរលេខជាពាក្យ គ្មានសញ្ញាសម្រង់ (ឧបករណ៍បដិសេធខ្ទង់លេខ និងសញ្ញាសម្រង់) មួយប្រយោគក្នុងមួយបន្ទាត់ ≤ 2000
តួអក្សរក្នុងមួយបន្ទាត់។ ការផ្អាកបន្ទាប់ពីបន្ទាត់៖ `|| bagli` 0.25 s, `|| normal` 0.5 s, `|| paragraf` 1 s, `|| agir` 1.5 s
ឬរយៈពេលផ្ទាល់ខ្លួន `|| 0,8` (0-5 s ខ្ទង់លេខរបស់សញ្ញាសម្គាល់នេះត្រូវបានអនុញ្ញាត)។ `ayarlar/okunus_sozlugu.tsv` កែការបញ្ចេញ
សំឡេងពាក្យបរទេសក្នុងអត្ថបទទួរគី។ ភាសាត្រូវបានរកឃើញពីអត្ថបទ (អក្សរទួរគី ប្រព័ន្ធអក្សរ ពាក្យទូទៅ បើមិនប្រាកដ ប្រើ `dil` របស់កាត
សំឡេង `--dil <code>` គឺស្រេចចិត្ត)។ សម្រាប់អត្ថបទមិនមែនទួរគី apostrophe ត្រូវបានអនុញ្ញាតនៅទីនោះ វចនានុក្រមទួរគីត្រូវបានរំលង
ប៉ុន្តែខ្ទង់លេខនៅតែត្រូវបានបដិសេធ។ បើការអានបង្ហាញ `speed gate: satır [...]` សូមស្តាប់បន្ទាត់ទាំងនោះ។

### Web UI

ក្នុងម៉ាស៊ីនប៉ុណ្ណោះ (127.0.0.1)៖ `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → បើក http://127.0.0.1:8765/ ដោយខ្លួនឯង
(port ផ្សេង៖ `--port 8800`) ឬចុចពីរដងលើ `baslat.bat`។ បញ្ឈប់ server ដោយ Ctrl+C។ មាន tab បី៖ *រចនាសំឡេង* *អានដោយសំឡេងនេះ*
*ចម្លងសំឡេង*។ ផ្លូវធម្មតា៖ *រចនា* → ស្តាប់ជម្រើសនានា → *បន្ថែមទៅបញ្ជីអានរបស់ខ្ញុំ* → *អានដោយសំឡេងនេះ* → ទាញយក។ ឬជ្រើស
សំឡេងមានស្រាប់មួយពី menu សំឡេង ហើយអាន។

- **កំណែនៅក្នុង header។** `v0.2.0 · <short commit>` តូច និងស្រអាប់ (មាន `+` នៅពេលឯកសារដែលកំពុងតាមដានមានការផ្លាស់ប្តូរ
  ដែលមិនទាន់ commit បើគ្មាន git មានតែកំណែ) ដូច្នេះរូបថតអេក្រង់ និងវីដេអូបង្ហាញថាបានប្រើកំណែណា។
- **សំឡេងពីរនៅលើកាតជម្រើសនីមួយៗ។** ខាងលើ ពណ៌ប្រផេះ គឺ *សំឡេងរចនាដើម*៖ វាត្រូវបានបង្កើតតែម្តង ហើយមិនចេញដូចដើមម្តងទៀតទេ។
  ខាងក្រោមវា ក្នុងស៊ុមពណ៌ទឹកក្រូច គឺ *↻ នេះជាសំឡេងដែលអ្នកនឹងឮជានិច្ច*៖ ការថតរចនាដែលអានឡើងវិញជាសំឡេងយោងដោយ seed
  ផ្ទាល់ខ្លួនរបស់ជម្រើស (បង្ហាញនៅលើកាត)។ នេះជារបៀបដែលសំឡេងស្តាប់ទៅក្នុងការអានពេលក្រោយគ្រប់ដង។ នៅក្រោមវាមាន
  *អានដោយសំឡេងនេះ* និង *បន្ថែមទៅបញ្ជីអានរបស់ខ្ញុំ*។ ការចុច *រចនា* តែម្តងធ្វើទាំងពីរ៖ វារចនាជម្រើសនីមួយៗ រួចអានអត្ថបទរបស់អ្នក
  ដោយសំឡេងអចិន្ត្រៃយ៍នីមួយៗ របារវឌ្ឍនភាពតែមួយរាប់ដំណាក់កាលទាំងពីរ។ folder ជម្រើសទទួលបាន `dinleme.wav`។ បើការអាននោះឈប់មុន
  ការរចនានៅតែត្រូវបានរក្សាទុក ហើយកាតបង្ហាញកំណត់ចំណាំមួយ។
- **បង្អួច "អត្ថបទដែលអ្នកចង់ស្តាប់"។** នៅក្នុង *រចនាសំឡេង* ប្រអប់ *↻ អត្ថបទដែលអ្នកចង់ស្តាប់* ផ្ទុកអ្វីដែលសំឡេងអចិន្ត្រៃយ៍នីមួយៗ
  អាន (បើទុកទទេ ប្រយោគគំរូនឹងត្រូវអាន)។ ការចុចលើវាបើកសៀវភៅកត់ត្រាអានក្នុងបង្អួចមួយ៖ លេខបន្ទាត់ menu បន្ទាត់ និងខ្សែផ្អាក។
  *យល់ព្រម* សរសេរអត្ថបទ និងការផ្អាករបស់វាត្រឡប់ទៅប្រអប់វិញ *បោះបង់* ឬ Esc មិនផ្លាស់ប្តូរអ្វីទេ។ tab អានរក្សាអត្ថបទផ្ទាល់ខ្លួនរបស់វា។
- **សៀវភៅកត់ត្រាអាន។** មួយប្រយោគក្នុងមួយបន្ទាត់។ ចុចលេខបន្ទាត់ដើម្បីបើក menu បន្ទាត់ (ផ្លាស់ទីឡើងលើ ឬចុះក្រោម ផ្លាស់ទីទៅ
  ទីតាំងមួយ ចម្លង លុប Alt+↑/↓, Alt+Shift+↓ ឬអូសដោយលេខ Ctrl+Z មិនធ្វើវិញទាំងអត្ថបទ និងការផ្អាកក្នុងពេលតែមួយ)។ ចុចខ្សែស្តើង
  រវាងបន្ទាត់ពីរ ដើម្បីជ្រើសការផ្អាក (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 s ឬរយៈពេលផ្ទាល់ខ្លួន 0-5 s ដោយប្រើ
  រូបស្ពឺ) ចុច Enter ពីរដងសម្រាប់កថាខណ្ឌ (1 s) ហើយបន្ទាត់ទទេក្លាយជាខ្សែផ្អាក។ ពេលលទ្ធផលកំពុងចាក់ បន្ទាត់ដែលកំពុងអាន
  ភ្លឺឡើង ហើយរមូរមកឱ្យឃើញ *▶ ស្តាប់ពីទីនេះ* នៅក្នុង menu បន្ទាត់ចាក់ចាប់ពីបន្ទាត់នោះ។ អត្ថបទ និងការផ្អាករបស់វានៅតែមាន
  ទោះបីផ្ទុកទំព័រឡើងវិញក៏ដោយ (browser storage)។
- **សេចក្តីព្រាង។** ប៊ូតុង *📄 សេចក្តីព្រាង* មាននៅក្នុងសៀវភៅកត់ត្រាទាំងពីរ (tab អាន និងបង្អួច)។ រក្សាទុកអត្ថបទបច្ចុប្បន្ន
  ជាមួយការផ្អាករបស់វាជាសេចក្តីព្រាង ផ្ទុកមួយដោយចុចម្តង (Ctrl+Z មិនធ្វើវិញ) ហើយប្រើ ⋯ ដើម្បីសរសេរជាន់ ប្ដូរឈ្មោះ ឬលុបវា។
  សេចក្តីព្រាងត្រូវបានរក្សាទុកក្នុង `sesler/taslaklar.json` មិនដែលនៅក្នុង repository ទេ។
- **បញ្ជីអាន និង menu សំឡេង។** នៅលើកាតជម្រើស *បន្ថែមទៅបញ្ជីអានរបស់ខ្ញុំ* បើកប្រអប់ឈ្មោះ៖ ដាក់ឈ្មោះផ្ទាល់ខ្លួនឱ្យជម្រើស
  ហើយ ✓ បន្ថែមវា។ *ឈ្មោះការបង្កើត* នៅតែមាននៅលើជម្រើសនីមួយៗនៃការបង្កើតនោះ។ នៅក្នុង *អានដោយសំឡេងនេះ* ប៊ូតុងសំឡេង (ទង់ +
  ឈ្មោះ) បើក menu សំឡេង៖ *បញ្ជីអានរបស់ខ្ញុំ* នៅខាងលើ បន្ទាប់មកសំឡេងមានស្រាប់ជាមួយទង់ (ភាសា interface មុនគេ)។ ជួរនីមួយៗមាន
  ▶ ស្តាប់ (សំឡេងអចិន្ត្រៃយ៍ បើមាន) បេះដូង (បន្ថែម ឬដកចេញ) និង ⋯ ↑/↓ និង Enter ជ្រើសរើស Esc បិទ ហើយសំឡេងចុងក្រោយត្រូវបាន
  ចងចាំ។ បញ្ជីនេះរក្សាទុកក្នុង `sesler/okuma_listesi.json` នៅខាងក្រៅ repository ហើយនៅតែមានបន្ទាប់ពីចាប់ផ្តើមឡើងវិញ។
- **ការគ្រប់គ្រងសំឡេង។** menu ⋯ (ជួរ menu សំឡេង ឬកាតជម្រើស) មាន *អានដោយសំឡេងនេះ* បន្ថែមទៅ ឬដកចេញពីបញ្ជី *ប្ដូរឈ្មោះ*
  (ឈ្មោះទទេស្ដារឈ្មោះដើមវិញ *ត្រឡប់ទៅឈ្មោះដើម*) *លុប* សម្រាប់សំឡេងដែលបានរចនា និង *លាក់* សម្រាប់សំឡេងមានស្រាប់ ទាំងពីរ
  សួរជាមុនសិន។ សំឡេងដែលបានលុបផ្លាស់ទៅ `sesler/_cop/` ការលាក់មិនដែលប៉ះឯកសាររបស់ repository ទេ។ *សំឡេងដែលបានលាក់ និងលុប (N)*
  នៅខាងក្រោម menu សំឡេងមាន *យកមកវិញ*។ ឈ្មោះផ្ទាល់ខ្លួន និងសំឡេងដែលបានលាក់ត្រូវបានរក្សាទុកក្នុង `sesler/yerel_katman.json`។
  សំឡេងដែលបានប្ដូរឈ្មោះបង្ហាញប្រភពរបស់វាជាពណ៌ប្រផេះ (*ឈ្មោះការបង្កើត · ជម្រើសទី N*) ⋯ → *ទៅកាន់ការបង្កើត* បើកការរចនារបស់វា។
- **ផ្លូវកាត់ និងឯកសារ។** Ctrl+Enter (⌘+Enter លើ Mac) ចាប់ផ្តើម *រចនា* ឬ *អានដោយសំឡេងនេះ* នៅលើ tab ដែលកំពុងបើក។ របារ
  វឌ្ឍនភាពបង្ហាញ *ពេលកន្លងទៅ / ~សរុប* ជាមួយការប៉ាន់ស្មានដែលរៀនពីការងារមុនៗលើម៉ាស៊ីនរបស់អ្នក។ ឯកសារទាញយកត្រូវបានដាក់ឈ្មោះ
  តាមសំឡេង និងពេលវេលា (`Voice_Name_2026-11-02_0152.wav`)។

**ការចម្លងសំឡេង (សំឡេងរបស់អ្នកផ្ទាល់ ឬសំឡេងដែលមានការយល់ព្រម)។** នៅក្នុង tab *ចម្លងសំឡេង* របស់ UI ផ្តល់ការថតរបស់អ្នក
(wav/mp3/flac/ogg ណែនាំការនិយាយស្អាត 5-30 s ក្រោម 3 s ត្រូវបានបដិសេធ លើស 36 s ត្រូវបានកាត់) អត្ថបទចម្លងត្រឹមត្រូវរបស់វា និង
អត្ថបទដែលត្រូវអាន។ ប៊ូតុងនៅតែបិទរហូតដល់អ្នកធីក "សំឡេងនេះជារបស់ខ្ញុំ ឬខ្ញុំមានការអនុញ្ញាតច្បាស់លាស់ពីម្ចាស់"។ ការថតទៅតែ
server ក្នុងម៉ាស៊ីន (127.0.0.1) ប៉ុណ្ណោះ ត្រូវបានដំណើរការក្នុង folder បណ្តោះអាសន្នរួមជាមួយ reference encoding របស់វា ហើយ folder
នោះត្រូវបានលុបនៅពេលការងារបញ្ចប់ ទោះបីបរាជ័យក៏ដោយ គ្មានអ្វីត្រូវបានផ្ញើតាមបណ្តាញទេ។ មានតែលទ្ធផលសំយោគប៉ុណ្ណោះដែលត្រូវបាន
រក្សាទុក (UI៖ `sesler/_okumalar/<job>/` CLI៖ `--cikti`)។ លទ្ធផលគឺ `klon_synthetic.wav` ដែលមានស្លាក "synthetic" ពេលចែករំលែក
សូមដាក់ស្លាកថាបង្កើតដោយ AI។ CLI៖ `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## សំណួរដែលសួរញឹកញាប់

**Model ឬ engine? មួយណាជាអ្វី?** VoxCPM2 (OpenBMB) គឺជា *model*៖ បណ្តាញដែលមានប៉ារ៉ាម៉ែត្រ 2 ពាន់លាន ដែលបំលែងអត្ថបទទៅជា
ការនិយាយ។ audio.cpp គឺជា *engine*៖ កម្មវិធី C++/CUDA ដែលដំណើរការ model លើ GPU របស់អ្នក (`audiocpp_cli.exe`)។ patch របស់យើង
ផ្លាស់ប្តូរ engine មិនមែន model ទេ៖ វាធ្វើឱ្យ VoxCPM2 សមនឹង 4 GB ហើយធ្វើឱ្យ seed ដូចគ្នាផ្តល់សំឡេងដូចគ្នារាល់ដង។ កញ្ចប់ Python
ក្នុង repo នេះគ្រាន់តែរៀបចំអត្ថបទ ហៅ engine និងប្រមូលឯកសារប៉ុណ្ណោះ។

**GPU មួយណាខ្លះ?** សូមមើល "GPU ដែលគាំទ្រ" ខាងលើ៖ NVIDIA ចាប់ពី GTX 10xx ឡើងទៅ VRAM 4 GB ឬច្រើនជាង driver ≥ 570។ native
code មាននៅក្នុង release សម្រាប់ sm_61/75/86/89/120a កាតផ្សេងទៀតដែលជា Pascal ឬថ្មីជាងប្រើ PTX ដែលបង្កប់ (ការចាប់ផ្តើមលើក
ដំបូងយឺតជាង)។ AMD/Intel៖ zip Vulkan ពិសោធន៍ `kur.ps1 -Vulkan` អ្នកប្រើខាងក្រៅម្នាក់បានរាយការណ៍ថាបានដំណើរការវាលើ AMD 6900 XT
ប៉ុន្តែនៅតែត្រូវការការសាកល្បង AMD/Intel ទូលំទូលាយជាងនេះ (សូមមើល "AMD / Intel" ខាងលើ)។ CPU តែម្យ៉ាង (`"backend": "cpu"`
ក្នុង `ayarlar.json`) ដំណើរការបាន ប៉ុន្តែយឺតជាង GTX 1050 Ti ~6× (ការវាស់របស់ engine គឺ 535 s ធៀបនឹង 94 s សម្រាប់ការនិយាយ 48 s)
មិនមែនជាផ្លូវដែលគាំទ្រទេ។

**លឿនប៉ុណ្ណា?** វាស់លើ GTX 1050 Ti 4 GB (i7-7700HQ)៖ ជម្រើសរចនាមួយ (ការថត ≈ 25 s) 55 s ការអាន ≈ 2 s នៃការគណនាសម្រាប់ការនិយាយ
1 s (real-time factor 1.9-2.8) បន្ទាប់ពី reference encoding ម្តងគត់ ~50 s ក្នុងមួយសំឡេង (រក្សាទុកក្នុង cache លើ disk) និងការផ្ទុក
model 10-20 s ក្នុងមួយ batch VRAM ខ្ពស់បំផុត 2.6-2.9 GB។ កាតថ្មីៗលឿនជាង តួលេខ និងវិធីសាស្ត្រ៖ [docs/4gb.md](docs/4gb.md)។

**តើវាអាចចម្លងសំឡេងបានទេ?** model VoxCPM2 ដែលនៅពីក្រោយអាចធ្វើត្រាប់សំឡេងពីការថតយោង ហើយផ្នែកចម្លងប្រើសមត្ថភាពនោះ។ ប្រើវាតែ
ជាមួយសំឡេងរបស់អ្នកផ្ទាល់ ឬដោយមានការអនុញ្ញាតច្បាស់លាស់ពីម្ចាស់សំឡេងប៉ុណ្ណោះ UI នឹងសុំឱ្យអ្នកបញ្ជាក់ការអនុញ្ញាតនោះ។ ការរចនា
សំឡេងមិនត្រូវការការថតទេ៖ វាចាប់ផ្តើមពីការពិពណ៌នាជាអត្ថបទជាភាសាអង់គ្លេស ឬចិន ហើយ "សំឡេងយោង" ដែលប្រើសម្រាប់អានសំឡេងដែលបាន
រចនា គឺជាការថតរចនាសំយោគរបស់ model ផ្ទាល់។ ការក្លែងខ្លួនជាអ្នកដទៃ ការក្លែងបន្លំ និងការបោកប្រាស់ត្រូវបានហាមឃាត់។ សូមមើល
[ETHICS.md](ETHICS.md)។ សូមដាក់ស្លាកអ្វីដែលអ្នកផ្សព្វផ្សាយថាបង្កើតដោយ AI។

**តើសរសេរការពិពណ៌នាសំឡេងល្អយ៉ាងដូចម្តេច?** ជាភាសាអង់គ្លេស 1-3 ប្រយោគ៖ អាយុ និងភេទ ពណ៌សំឡេង (ជ្រៅ/ភ្លឺ កក់ក្តៅ ច្រមុះ
ស្អក) សម្លេង និងតួនាទី (អ្នកនិទានឯកសារស្ងប់ស្ងាត់ អ្នកសម្របសម្រួលស្វាហាប់) ល្បឿន (យឺត មានចង្វាក់) និង "clean studio recording,
no background noise"។ ទុកវាជាការពិពណ៌នា មិនមែនជាអត្ថបទសម្រាប់អានទេ គ្មានវង់ក្រចក។ សុំ 3-5 ជម្រើស ហើយស្តាប់៖ seed ផ្លាស់ប្តូរ
សំឡេងច្រើនណាស់។ សម្រាប់អត្ថបទបង្កើត ប្រើ 1-2 ប្រយោគធម្មជាតិជាភាសារបស់សំឡេង ក្នុងអារម្មណ៍ដែលអ្នកចង់បាន (ការនិយាយយ៉ាងច្រើន
~20 s)។ ពេលអាន មួយប្រយោគក្នុងមួយបន្ទាត់ បំបែកប្រយោគវែង សរសេរលេខជាពាក្យ។

## ការចូលរួមចំណែក

មិនដឹងចាប់ផ្តើមពីណា? issue តូចៗទាំងបួននេះជាជំហានដំបូងដ៏ល្អ៖

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) សាកល្បងលើ GPU របស់អ្នក ហើយរាយការណ៍កាត driver និងពេលវេលា
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel៖ សាកល្បង build Vulkan ពិសោធន៍
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) បន្ថែមប្រយោគមួយទៅសំណុំតេស្ត
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) ចែករំលែកសំឡេងដែលអ្នកបានរចនា ជាមួយការពិពណ៌នា និង seed របស់វា

សំណុំតេស្តរួម៖ [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt) មគ្គុទ្ទេសក៍សំឡេងម៉ាក៖
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md) របៀបផ្ញើកូដ៖ [CONTRIBUTING.md](CONTRIBUTING.md)។
បញ្ហាដំឡើង៖ [ទម្រង់ issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml) សំណួរ និងលទ្ធផល៖ [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)។
អ្នកចូលរួមគ្រប់គ្នាគោរពតាម [ក្រមសីលធម៌](CODE_OF_CONDUCT.md)៖ ចូរមានចិត្តល្អ ហើយផ្តល់មតិយោបល់លើការងារ។

## អ្នករួមចំណែក

- [@alexturkey](https://github.com/alexturkey)៖ អ្នកថែទាំ កូដ សំឡេងមានស្រាប់ ឯកសារ
- [@cayir21](https://github.com/cayir21)៖ ការគាំទ្រ Metal សម្រាប់ macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis)៖ ការកែចុងប្រយោគ (EOS) សម្រាប់ការអានច្រើនប្រយោគលើ CPU backend, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)

ឈ្មោះរបស់អ្នកក៏គួរនៅទីនេះដែរ៖ លទ្ធផលតេស្តពី GPU របស់អ្នក ប្រយោគមួយសម្រាប់សំណុំតេស្ត សំឡេងដែលអ្នកបានរចនា របាយការណ៍ bug
ច្បាស់លាស់ ឬ pull request សុទ្ធតែរាប់ជាការរួមចំណែក។ សូមអរគុណដល់អ្នកគ្រប់គ្នាដែលសាកល្បង ហើយសរសេរមកវិញ។

## អាជ្ញាប័ណ្ណ និងការទទួលស្គាល់

កូដ និងសំឡេងមានស្រាប់៖ Apache-2.0, Copyright 2026 Ali Haydar Ozturk។ បង្កើតឡើងលើ VoxCPM2 (OpenBMB, Apache-2.0)
audio.cpp (ShugoAI LLC, Apache-2.0) និងការបំលែង audio.cpp GGUF។ បញ្ជីពេញ៖ [THIRD_PARTY.md](THIRD_PARTY.md)។ មិនមាន
ទំនាក់ទំនងជាមួយ OpenBMB, ModelBest ឬគម្រោង audio.cpp ទេ។

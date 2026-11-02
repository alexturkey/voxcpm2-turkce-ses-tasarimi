[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · **العربية** · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**تصميم أصوات تركية باستخدام VoxCPM2 على بطاقة رسوميات بذاكرة 4 GB.** صِف صوتًا بالإنجليزية، ودع النموذج يُنشئه، واختر
النسخة التي تعجبك، ثم اقرأ بهذا الصوت أي نص تركي. يتضمن المشروع مُثبّتًا بأمر واحد، ومحرك [audio.cpp](https://github.com/0xShug0/audio.cpp)
مُعدَّلًا يتسع في بطاقة GTX 1050 Ti (4 GB)، وواجهة ويب محلية صغيرة، وأربعة عشر صوتًا اصطناعيًا جاهزًا: سبعة أصوات تركية وسبعة
رواة أصليين بالإنجليزية والفرنسية والألمانية والإسبانية والروسية والصينية واليابانية.

- يقرأ التطبيق 30 لغة، وواجهته متاحة أيضًا بـ 30 لغة.
- أصوات جاهزة عددها 14: سبعة تركية، وصوت واحد لكل من الإنجليزية والفرنسية والألمانية والإسبانية والروسية والصينية واليابانية.
- واجهة الويب (v0.2.0): في كل بطاقة نسخة صوتان، صوت التصميم الخام والصوت الذي ستسمعه دائمًا؛ وقائمة قراءة مع قائمة أصوات؛
  وإعادة تسمية الأصوات أو إخفاؤها أو حذفها؛ ومسودات للنصوص التي تقرؤها. انظر «واجهة الويب» ضمن «الاستخدام».

[كيف يتسع في 4 GB](docs/4gb.md) · [أوبونتو / Linux](docs/linux.md) · [نظام macOS](docs/mac.md) · [دليل التثبيت لوكلاء الذكاء الاصطناعي](AGENTS.md) · [الاستخدام المسؤول](ETHICS.md)

> الأصوات المرفقة اصطناعية، صُمّمت انطلاقًا من وصف نصي. قسم استنساخ الصوت مخصص فقط لصوتك أنت أو لصوت يُستخدم بإذن صريح من صاحبه، وتطلب منك الواجهة تأكيد هذا الإذن. انتحال الشخصية والاحتيال والتضليل أمور محظورة. ضع على ما تُنتجه علامة تفيد بأنه مولَّد بالذكاء الاصطناعي. انظر [ETHICS.md](ETHICS.md).

## 30 لغة

أنتجنا فيلمًا وثائقيًا واحدًا عن كبادوكيا بثماني لغات: التركية والإنجليزية والفرنسية والألمانية والإسبانية والروسية والصينية
واليابانية. لكل لغة **راوٍ أصلي** خاص بها، صُمّم باستخدام VoxCPM2 انطلاقًا من وصف بالإنجليزية. وقد وُلِّد كل ذلك محليًا بالكامل
على بطاقة GTX 1050 Ti بذاكرة 4 GB، وبالجودة الثابتة نفسها (16 خطوة، cfg 2.0). الرواة السبعة مرفقون هنا مع الوصف ونص التصميم
والبذرة (seed) والتسجيل المرجعي لكل منهم.

| الرمز | اللغة | الصوت | استماع | فيديو |
|---|---|---|---|---|
| `tr` | التركية | `hazir/belgesel_hanim` (و6 أصوات أخرى) | [عينة](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | الإنجليزية | `hazir/anlatici_en` | [عينة](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113791986763440439) |
| `fr` | الفرنسية | `hazir/anlatici_fr` | [عينة](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113790681575804962) |
| `de` | الألمانية | `hazir/anlatici_de` | [عينة](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113791351645262249) |
| `es` | الإسبانية | `hazir/anlatici_es` | [عينة](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113807365611122705) |
| `ru` | الروسية | `hazir/anlatici_ru` | [عينة](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113801574136848884) |
| `zh` | الصينية (الماندرين) | `hazir/anlatici_zh` | [عينة](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113802229606121794) |
| `ja` | اليابانية | `hazir/anlatici_ja` | [عينة](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [فيديو](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**لماذا جملةً جملة؟** لا يكون VoxCPM2 مستقرًا في توليد واحد طويل (فوق 30 ثانية تقريبًا): يتسارع الإيقاع وقد ينحرف الصوت. أما هنا
فيحمل الصوتَ تسجيلٌ مرجعي ثابت وبذرة ثابتة، ويُقرأ النص الطويل جملةً واحدة في كل سطر، فتبقى نبرة الصوت وأسلوبه كما هما من الجملة
الأولى حتى الأخيرة. لا يُطبَّق قاموس النطق التركي على اللغات غير التركية. جُرّبت اللغات الثلاثون التي يدعمها VoxCPM2 كلها وهي
تعمل؛ استخدم `--dil <code>` للغات التي ليس لها صوت مرفق. أوامر كل لغة والدروس التي تعلمناها:
[docs/cok_dilli.md](docs/cok_dilli.md). مهارة Claude Code لمسار التصميم كاملًا:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**أوصاف جاهزة عددها 144 للبدء.** هناك 18 دورًا (راوي أفلام وثائقية، مذيع أخبار، صوت إعلانات، كتاب صوتي، جدة
تحكي الحكايات، مقدم بودكاست، معلم، إعلان فيلم، مرشد تأمل، معلق رياضي وغيرها، للرجال والنساء) في كل لغة من اللغات الثماني. الوصف
بالإنجليزية ويذكر جنسية المتحدث ولكنته الأصلية؛ ويرافقه النص الذي يُقرأ أثناء إنشاء الصوت، بتلك اللغة ومتوافقًا مع الدور. اختر
واحدًا، واستمع إلى النسخ، واحتفظ بما يعجبك: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`، أو اختر
*وصف جاهز* في واجهة الويب. القائمة الكاملة: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**دبلج مقاطع الفيديو الخاصة بك بصوتك أنت.** برنامج [DubWorld](https://github.com/alexturkey/dubworld) هو برنامجنا المحلي لدبلجة
الفيديو؛ وهو يثبّت هذا المستودع محركًا صوتيًا لـ VoxCPM2. والصوت الذي تصممه هنا يُستخدم هناك عبر
`ses.voxcpm2_ses = "<name>/<variant>"`.

## البدء السريع (Windows، ثلاث خطوات)

1. **نزّل** الشيفرة: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   يجلب المُثبّت في الخطوة 3 حزمة المحرك الجاهزة المناسبة لبطاقتك:
   بطاقات NVIDIA ← [حزمة CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip)،
   بطاقات AMD / Intel ← [حزمة Vulkan، تجريبية](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (هل نزّلت إحداها مسبقًا؟ أضف `-HazirZip <path to the zip>` إلى الأمر أدناه).
2. **فُكّ ضغط** ملف zip، وافتح المجلد `voxcpm2-turkce-ses-tasarimi-main`، واكتب `powershell` في شريط العنوان في مستكشف الملفات
   ثم اضغط Enter.
3. **شغّل** المُثبّت (يحتاج إلى Python 3.10-3.13 بإصدار 64-bit، وإلى تعريف NVIDIA ≥ 570 من أجل CUDA)، ثم انقر نقرًا مزدوجًا على **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   لبطاقات AMD / Intel: أضف `-Vulkan` في النهاية. تُفتح الواجهة على http://127.0.0.1:8765/.

ملف zip الخاص بالمحرك ليس تطبيقًا مستقلًا (ملفه التنفيذي exe يحتاج إلى النموذج وملفات DLL التي يجهّزها المُثبّت). التفاصيل وقائمة
البطاقات والمشاكل الشائعة: انظر «تثبيت سريع» أدناه.

## نظام Ubuntu / Linux (NVIDIA CUDA، تجريبي)

ابنِ المحرك المُعدَّل عبر `bash scripts/kur-linux.sh`، أو استخدم `Dockerfile.linux` للبناء والتشغيل في بيئة Ubuntu 24.04 / CUDA 12.8.1.
يتطلب ذلك بطاقة NVIDIA وتعريفًا متوافقًا؛ ويحتاج المُثبّت الأصلي أيضًا إلى CUDA toolkit وPython 3.10-3.13. تبقى الواجهة مقصورة
على loopback، بما في ذلك على الخوادم البعيدة (عبر إعادة التوجيه بـ SSH). المتطلبات والأوامر واختيار المعمارية ونطاق التحقق:
[docs/linux.md](docs/linux.md).

## البدء السريع (macOS، Apple Silicon)

تحتاج إلى Xcode Command Line Tools (`xcode-select --install`) وإلى [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
ينزّل المُثبّت النموذج، ويبني المحرك المُعدَّل مع Metal (نحو دقيقة واحدة)، ويجهّز كل شيء تحت `~/vox`. بعد ذلك انقر نقرًا مزدوجًا
على **`baslat.command`**. على MacBook Air M4 بذاكرة 16 GB: نحو 2 ثانية حساب لكل ثانية كلام، والبذرة نفسها تعطي صوتًا مطابقًا بايتًا
ببايت، وذروة استهلاك الذاكرة نحو 5.3 GB RAM، ولا تباطؤ حراريًا خلال 12 دقيقة من القراءة المتواصلة. التفاصيل والقياسات:
[docs/mac.md](docs/mac.md).

**تطبيق Mac أصلي (دون Python أو Homebrew أو Terminal):** [macos/README.md](macos/README.md). يضم المحرك المُعدَّل نفسه وينزّل
النموذج عند التشغيل الأول؛ ويُبنى حاليًا من المصدر باستخدام Xcode.

## لمستخدمي Mac (Apple Silicon)

يوجد أيضًا تكييف مستقل من صنع المجتمع لأجهزة Mac بمعالجات Apple Silicon، يشغّل VoxCPM2 بإطار عمل MLX من Apple:
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
يطوّره ويصونه أمره كوتش (Emre Koç، [@emre-koc](https://github.com/emre-koc)) في مستودعه الخاص، لا هنا؛ فخطوات التثبيت وأسئلة
الدعم تُوجَّه إلى هناك. شكرًا لك يا أمره على إيصال هذا المشروع إلى Mac!

## كيف يعمل

1. **تصميم الصوت.** *وصف الصوت* بالإنجليزية + *نص يُقرأ أثناء إنشاء الصوت* (بلغة الصوت) + عدد من النسخ. تحصل كل نسخة على
   بذرتها الخاصة؛ يتلقى المحرك `(description)text` ويعيد تسجيل تصميم واحدًا لكل بذرة. النص عينة قصيرة للتعرّف على الصوت:
   جملة أو جملتان، بحد أقصى نحو 20 ثانية (تعرض الواجهة التقدير ولا تبدأ إن تجاوز 22 ثانية)؛ أما النص الطويل فمكانه الخطوة 2.
2. **القراءة المستندة إلى المرجع.** يُمرَّر تسجيل التصميم إلى **كلا** مدخلَي المحرك (`audio` و`voice_ref`)، مع نصه المكتوب
   (`reference_text`) والنص الجديد المراد قراءته، وبالبذرة نفسها. التسجيل هو ما يحمل الصوت لا الوصف، ولذلك لا ينحرف الصوت من نص
   إلى آخر. ويُقرأ النص جملةً جملة.
3. الجودة ثابتة: 16 خطوة انتشار (diffusion)، وCFG 2.0. والبذرة ليست أداة لضبط الجودة.

تسجيل التصميم الخام عينة فريدة من الصوت لا تتكرر؛ ولا تبدو أي قراءة لاحقة مثله تمامًا. ما تسمعه في كل قراءة لاحقة هو الخطوة 2:
تسجيل التصميم بوصفه مرجعًا مع بذرة النسخة الخاصة. لهذا تنفّذ واجهة الويب الخطوة 2 مباشرة بعد التصميم وتعرض الاثنين معًا في بطاقة النسخة.

المحرك هو audio.cpp v0.7.2 مع الرقعة (patch) الخاصة بنا (`patches/`)، والنموذج هو VoxCPM2 Q8_0 GGUF. ذروة VRAM ≈ 2.8 GB؛ ونحو 2
ثانية حساب لكل ثانية كلام على GTX 1050 Ti. التفاصيل والقياسات: [docs/4gb.md](docs/4gb.md).

## الأصوات المرفقة (`hazir_sesler/`)

صُمّمت الأصوات الأربعة عشر كلها من الأوصاف المحفوظة في ملف `ses.json` لكل منها؛ ولم يُستنسخ أي منها من تسجيل (فالاستنساخ هو
تبويب *استنساخ الصوت* المنفصل، المشروط بالموافقة).

| الصوت | وصف موجز | استماع |
|---|---|---|
| `belgesel_hanim` | امرأة ناضجة في الخمسينيات، صوت ألطو عميق ودافئ؛ راوية أفلام وثائقية هادئة | [عينة](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [مرجع](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | راوٍ ذكر بصوت عميق وقوي وغامض | [عينة](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [مرجع](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | مذيع أخبار متمرس في نحو السبعين، هادئ وواثق | [عينة](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [مرجع](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | مذيعة أخبار مسائية جذابة في الثلاثينيات، صوت مخملي معبّر | [عينة](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [مرجع](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | ساحرة الحكايات: صوت منخفض، فيه غنّة خفيفة، وحلاوة ماكرة | [عينة](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [مرجع](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | راوٍ ذكر بصوت عميق وكثيف وآمر على نحو استثنائي | [عينة](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [مرجع](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | شيخ حكيم، صوت عميق مدوٍّ، فيه شيء من الغموض | [عينة](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [مرجع](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | راوي أفلام وثائقية ذكر لغته الأم الإنجليزية في الخمسينيات (General American)؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | راوي أفلام وثائقية ذكر لغته الأم الفرنسية في الخمسينيات (لهجة باريس)؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | راوي أفلام وثائقية ذكر لغته الأم الألمانية في الخمسينيات (Hochdeutsch)؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | راوي أفلام وثائقية ذكر لغته الأم الإسبانية في الخمسينيات (القشتالية (مدريد))؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | راوي أفلام وثائقية ذكر لغته الأم الروسية في الخمسينيات (لهجة موسكو)؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | راوي أفلام وثائقية ذكر لغته الأم الصينية (الماندرين) في الخمسينيات (بوتونغهوا بكين)؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | راوي أفلام وثائقية ذكر لغته الأم اليابانية في الخمسينيات (لهجة طوكيو القياسية)؛ صوت عميق هادئ دافئ | [عينة](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [مرجع](hazir_sesler/anlatici_ja/referans.flac) |

يحتوي كل مجلد على: `referans.flac` (تسجيل التصميم دون فقد)، و`ses.json` (الوصف، والنص المكتوب، وبذرة التصميم، وبذرة القراءة،
والوصف الموجز؛ و`dil` = اللغة بالنسبة إلى الرواة)، و`ornek_okuma.mp3` (+ نصه). استخدمها مباشرة: `--ses hazir/<name>`.
التسجيلات المرجعية للرواة قصيرة (5.6-10 ثوانٍ)؛ وعيّناتهم هي الجمل الثلاث الأولى من نص كبادوكيا، مقتطعة من قراءة الإنتاج الكاملة.

## تثبيت سريع دون مترجم برمجي (Windows 10/11، بطاقة NVIDIA ≥ 4 GB)

المتطلبات: تعريف NVIDIA ≥ 570 وPython 3.10-3.13 بإصدار 64-bit (`winget install Python.Python.3.12`). لا شيء غير ذلك: لا Visual
Studio ولا مُثبّت CUDA. لست متأكدًا من نوع بطاقتك؟ شغّل `nvidia-smi` في PowerShell: سيعرض اسم البطاقة وإصدار التعريف والذاكرة.
ليست لديك بطاقة NVIDIA؟ انظر «AMD / Intel» أدناه.

باستخدام [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

من دون Git: انقر في هذه الصفحة على **Code → Download ZIP**، وفُكّ الضغط، وافتح المجلد `voxcpm2-turkce-ses-tasarimi-main` الناتج،
واكتب `powershell` في شريط العنوان في مستكشف الملفات واضغط Enter، ثم شغّل السطر الأخير أعلاه. لا حاجة إلى Git إلا لمسار البناء من المصدر.

إن الخيار `-ExecutionPolicy Bypass` يسري على هذه العملية وحدها ولا يغيّر أي إعداد في النظام؛ اقرأ `scripts\kur.ps1` قبل تشغيله،
كما تفعل مع أي سكربت تثبيت. أمر واحد، نحو 10 دقائق، تنزيل نحو 3.7 GB، وكل شيء مُتحقَّق منه بـ sha256: النموذج (2.95 GB)، وملفات
DLL لبيئة تشغيل CUDA 12.8 في ملفات zip محمولة (دون تثبيت في النظام، ولا مساس بـ PATH)، و**المحرك المبني مسبقًا** من صفحة Releases،
وبيئة `.venv` فيها حزمتا Python، والملف `ayarlar.json`، وفحص نهائي للبطاقة (`KONTROL_OK`). أعد تشغيله بعد أي فشل؛ إذ تُتخطى الملفات
التي سبق التحقق منها. ثم شغّل واجهة الويب: انقر نقرًا مزدوجًا على **`baslat.bat`** في مجلد المستودع. فهو يشغّل الواجهة ويفتح
**http://127.0.0.1:8765/** في متصفحك حين تجهز؛ أغلق النافذة السوداء (أو اضغط Ctrl+C فيها) لإيقافها.
والأمر نفسه من PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
ثم افتح **http://127.0.0.1:8765/** بنفسك (عند التشغيل بهذه الطريقة لا تفتح الواجهة المتصفح؛ وهي تستمع على localhost فقط).

> **ملف `audiocpp_cli.exe` الموجود في zip الإصدار ليس مُعدًّا للنقر المزدوج.** إنه محرك يعمل من سطر الأوامر ويحتاج إلى ملفات DLL الخاصة بـ CUDA وإلى النموذج بجانبه؛ يضع `kur.ps1` كل شيء في مكانه وحزمة Python هي التي تقوده. النقر المزدوج عليه لا يعرض إلا "cudart64_12.dll not found".

**البطاقات المدعومة (الإصدار v0.1.1):** شيفرة أصلية لبطاقات GTX 10xx (sm_61) وRTX 20xx (sm_75) وRTX 30xx (sm_86) وRTX 40xx
(sm_89) وRTX 50xx (sm_120a)؛ وأي بطاقة CUDA أخرى من جيل Pascal فما بعده تشغّل PTX المضمّن عبر التعريف (بداية أولى أبطأ). جيل
Maxwell (GTX 9xx) وما قبله لا يدعمه CUDA 12.8. اختبرناه بأنفسنا على GTX 1050 Ti بذاكرة 4 GB (وكذلك عبر Docker Desktop/WSL2 على
Windows، من سطر الأوامر فقط)؛ وقاسه @mslmyilmaz5 (#15): RTX 3060 Ti بذاكرة 8 GB، وUbuntu 24.04 Docker، وCUDA 12.8.1 (التفاصيل في
[docs/linux.md](docs/linux.md)). نرحب بتقارير البطاقات الأخرى في [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**بطاقات AMD / Intel (تجريبي):** يُثبَّت ملف zip منفصل لمحرك Vulkan (`...-win64-vulkan.zip`، دون CUDA) عبر
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. لم يُتحقق منه إلا على بطاقة NVIDIA الخاصة بنا عبر واجهة Vulkan الخلفية (وهناك عمل أبطأ من
CUDA لكنه أعطى الصوت نفسه للبذرة نفسها؛ وقد أُخذ ذلك القياس والقرص مشغول بمهمة أخرى، لذا ما زالت مقارنة سرعة نظيفة معلّقة)، و**لم**
نختبره بأنفسنا على عتاد AMD أو Intel: إن جرّبته فانشر النتيجة في Discussions. عند وجود أكثر من جهاز Vulkan (مدمج + منفصل) يكتب
المُثبّت رقم البطاقة المنفصلة بوصفه `cihaz` في `ayarlar.json`.

*ملاحظة: دعم Vulkan تجريبي حاليًا. وقد بُني واختُبر بنجاح على GTX 1050 Ti. كما أفاد مستخدم خارجي (mitra_tr) بأنه شغّله على AMD 6900 XT. وما زالت هناك حاجة إلى اختبارات أوسع على بطاقات AMD/Intel.*

### بديل: بناء المحرك من المصدر

تحتاج إلى Visual Studio 2022 Build Tools مع "Desktop development with C++" (بما فيها C++ CMake tools)، نحو 7 GB. ثم:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
ينزّل هذا أيضًا nvcc، ويجلب مصدر audio.cpp v0.7.2، ويطبّق `patches/0001-voxcpm2-4gb-ve-hiz.patch`، ويبني لبطاقتك (`-Mimari native`
افتراضيًا، أو مثلًا `-Mimari 61`)، في نحو 15-25 دقيقة. اجعل مسار الجذر قصيرًا (`C:\vox`): إذ يفشل nvcc مع المسارات الطويلة. الخطوات
بالتفصيل مع الفحوص: [AGENTS.md](AGENTS.md).

### مشاكل التثبيت الشائعة

| ما تراه | معناه وما يجب فعله |
|---|---|
| ظهور `cudart64_12.dll not found` بعد النقر المزدوج على exe | المحرك ليس مُعدًّا للتشغيل اليدوي. شغّل أمر `kur.ps1` أعلاه، ثم شغّل واجهة الويب. |
| `64-bit Python 3.10+ bulunamadı` (لم يُعثر على Python) | ثبّت Python (`winget install Python.Python.3.12`)، وأغلق PowerShell، وافتح نافذة جديدة وشغّل الأمر نفسه مرة أخرى. |
| `motor ekran kartını görmedi` (المحرك لم يرَ البطاقة) | حدّث تعريف NVIDIA إلى 570 أو أحدث؛ وتأكد من أن `nvidia-smi` يعمل. |
| `indirme başarısız` / `sha256 tutmadı` (فشل التنزيل / عدم تطابق المجموع الاختباري) | غالبًا تنزيل منقطع. شغّل الأمر نفسه مرة أخرى؛ تُتخطى الملفات التي سبق التحقق منها. |
| مسار البناء: فشل `nvcc` | اجعل جذر التثبيت قصيرًا (`-Kok C:\vox`). |
| الصفحة لا تُفتح | شغّل الواجهة عبر `baslat.bat`، أو افتح http://127.0.0.1:8765/ بنفسك. المنفذ مشغول؟ غيّر `"port"` في `ayarlar.json`. |

هل من مشاكل؟ [النقاشات (أسئلة وأجوبة)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) أو
[بلاغ مشكلة تثبيت](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
تذكر فيه بطاقتك وإصدار Windows والأمر وآخر أسطر مخرجاته.

## الاستخدام

سطر الأوامر:
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
قواعد النص: اكتب الأعداد بالحروف، ودون علامات تنصيص (ترفض الأداة الأرقام وعلامات التنصيص)، وجملة واحدة في كل سطر، وبحد أقصى 2000
حرف في السطر. التوقف بعد السطر: `|| bagli` 0.25 ثانية، `|| normal` 0.5 ثانية، `|| paragraf` ثانية واحدة، `|| agir` 1.5 ثانية،
أو مدة تختارها بنفسك `|| 0,8` (من 0 إلى 5 ثوانٍ؛ أرقام العلامة مسموح بها). يصحح الملف `ayarlar/okunus_sozlugu.tsv` نطق الكلمات الأجنبية في النص التركي.
تُكتشف اللغة من النص (الحروف التركية، ونظام الكتابة، والكلمات الشائعة؛ وعند الشك تُعتمد قيمة `dil` في بطاقة الصوت؛ والخيار `--dil <code>` اختياري). في النص غير التركي
يُسمح هناك بالفواصل العليا، ويُتخطى القاموس التركي، وتظل الأرقام مرفوضة. إذا طبعت القراءة `speed gate: satır [...]` فاستمع إلى تلك الأسطر.

### واجهة الويب

محلية فقط (127.0.0.1): شغّل `.venv\Scripts\python.exe -m ses_tasarim.arayuz` ← ثم افتح http://127.0.0.1:8765/ بنفسك
(منفذ آخر: `--port 8800`)، أو انقر نقرًا مزدوجًا على `baslat.bat`. أوقف الخادم بـ Ctrl+C. ثلاثة تبويبات: *صمّم صوتًا*،
و*اقرأ بهذا الصوت*، و*استنساخ الصوت*. المسار المعتاد: *صمّم* ← استمع إلى النسخ ← *أضف إلى قائمة قراءتي* ←
*اقرأ بهذا الصوت* ← التنزيل. أو اختر صوتًا جاهزًا من قائمة الأصوات واقرأ.

- **الإصدار في الترويسة.** نص صغير باهت `v0.2.0 · <short commit>` (مع `+` عندما تكون في الملفات المتتبَّعة تغييرات غير مُودعة؛ والإصدار
  وحده من دون git)، حتى تُظهر لقطات الشاشة ومقاطع الفيديو أي إصدار استُخدم.
- **صوتان في كل بطاقة نسخة.** في الأعلى، بالرمادي، *صوت التصميم الخام*: يُولَّد مرة واحدة ولا يخرج بالشكل نفسه مرة أخرى. وتحته، في
  إطار برتقالي، *↻ هذا هو الصوت الذي ستسمعه دائمًا*: تسجيل التصميم مقروءًا من جديد بوصفه مرجعًا ببذرة النسخة الخاصة (المعروضة على البطاقة).
  هكذا يبدو الصوت في كل قراءة لاحقة. وتحته الزرّان *اقرأ بهذا الصوت* و*أضف إلى قائمة قراءتي*. ضغطة واحدة على *صمّم* تؤدي
  الأمرين معًا: تصمّم كل النسخ، ثم تقرأ نصك بكل صوت دائم؛ ويعدّ شريط تقدم واحد المرحلتين كلتيهما. ويحصل مجلد النسخة على
  `dinleme.wav`. إذا توقفت تلك القراءة مبكرًا، يُحتفظ بالتصميم وتعرض البطاقة ملاحظة.
- **نافذة «النص الذي تريد سماعه».** في *صمّم صوتًا*، يحمل مربع *↻ النص الذي تريد سماعه* ما يقرؤه كل صوت دائم (إن تُرك فارغًا
  تُقرأ الجملة النموذجية). النقر عليه يفتح دفتر القراءة في نافذة: أرقام الأسطر، وقائمة السطر، وأشرطة التوقف. يكتب *موافق* النص
  وتوقفاته عائدًا إلى المربع؛ أما *إلغاء* أو Esc فلا يغيّران شيئًا. ويحتفظ تبويب القراءة بنصه الخاص.
- **دفتر القراءة.** جملة واحدة في كل سطر. انقر على رقم سطر لفتح قائمة السطر (نقل لأعلى أو لأسفل، نقل إلى موضع، تكرار، حذف؛
  Alt+↑/↓ وAlt+Shift+↓ أو السحب من الرقم؛ ويتراجع Ctrl+Z عن النص والتوقفات معًا). انقر على الشريط الرفيع بين سطرين لاختيار التوقف
  (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 ثانية، أو مدتك الخاصة 0-5 ثوانٍ عبر الترس)؛ اضغط Enter مرتين لفقرة (ثانية واحدة)،
  وتتحول الأسطر الفارغة إلى أشرطة توقف. أثناء تشغيل النتيجة يتوهج السطر المقروء ويُمرَّر إلى مجال الرؤية؛ ويشغّل *▶ استمع من هنا*
  في قائمة السطر الصوتَ بدءًا من ذلك السطر. ويبقى النص وتوقفاته بعد إعادة تحميل الصفحة (تخزين المتصفح).
- **المسودات.** يوجد زر *📄 المسودات* في الدفترين كليهما (تبويب القراءة والنافذة). احفظ النص الحالي مع توقفاته مسودةً، وحمّل
  مسودة بنقرة (ويتراجع Ctrl+Z)، واستخدم ⋯ للاستبدال أو إعادة التسمية أو الحذف. تُحفظ المسودات في `sesler/taslaklar.json`، ولا
  تُحفظ أبدًا في المستودع.
- **قائمة القراءة وقائمة الأصوات.** في بطاقة النسخة، يفتح *أضف إلى قائمة قراءتي* مربع اسم: أعطِ النسخة اسمها الخاص ويضيفها ✓.
  ويبقى *اسم التوليد* على كل نسخ ذلك التشغيل. في *اقرأ بهذا الصوت*، يفتح زر الصوت (علم + اسم) قائمة الأصوات: *قائمة قراءتي* في
  الأعلى، ثم الأصوات الجاهزة بأعلامها (لغة الواجهة أولًا). في كل صف ▶ للاستماع (إلى الصوت الدائم إن وُجد)، والقلب (إضافة أو إزالة)،
  و⋯؛ ويختار ↑/↓ وEnter، ويغلق Esc، ويُتذكَّر آخر صوت. تُحفظ القائمة في `sesler/okuma_listesi.json` خارج المستودع، وتبقى بعد
  إعادة التشغيل.
- **إدارة الأصوات.** في قائمة ⋯ (صف قائمة الأصوات أو بطاقة النسخة): *اقرأ بهذا الصوت*، والإضافة إلى القائمة أو الإزالة منها،
  و*إعادة التسمية* (الاسم الفارغ يعيد الاسم الأصلي؛ *العودة إلى الاسم الأصلي*)، و*حذف* للأصوات المصمَّمة و*إخفاء* للأصوات الجاهزة؛
  وكلاهما يطلب التأكيد أولًا. ينتقل الصوت المحذوف إلى `sesler/_cop/`؛ والإخفاء لا يمس ملفات المستودع أبدًا. وفي أسفل قائمة
  الأصوات يحتوي *الأصوات المخفية والمحذوفة (N)* على *استعادة*. تُحفظ الأسماء المخصصة والأصوات المخفية في `sesler/yerel_katman.json`.
  ويعرض الصوت المُعاد تسميته أصله بالرمادي (*اسم التوليد · النسخة N*)؛ ويفتح ⋯ ← *الانتقال إلى التوليد* تصميمه.
- **الاختصارات والملفات.** يبدأ Ctrl+Enter (أو ⌘+Enter على Mac) *صمّم* أو *اقرأ بهذا الصوت* في التبويب المفتوح. يعرض شريط التقدم
  *المنقضي / ~الإجمالي*، بتقدير يتعلمه من المهام السابقة على جهازك. ويُسمّى الملف المنزَّل باسم الصوت والوقت
  (`Voice_Name_2026-11-02_0152.wav`).

**استنساخ الصوت (صوتك أو صوت بموافقة صاحبه).** في تبويب *استنساخ الصوت* من الواجهة، قدّم تسجيلك (wav/mp3/flac/ogg، يُنصح بـ 5-30 ثانية من الكلام النظيف؛ ويُرفض ما دون 3 ثوانٍ، ويُقتطع ما فوق 36 ثانية)، ونصه المكتوب بدقة، والنص المراد قراءته. يبقى الزر معطلًا حتى تضع علامة على «هذا الصوت لي أو لديّ إذن صريح من صاحبه». لا يذهب التسجيل إلا إلى الخادم المحلي (127.0.0.1)، ويُعالَج في مجلد مؤقت مع ترميزه المرجعي، ويُحذف ذلك المجلد عند انتهاء المهمة، وكذلك عند فشلها؛ ولا يُرسل شيء عبر الشبكة. لا يُحتفظ إلا بالناتج الاصطناعي (الواجهة: `sesler/_okumalar/<job>/`، سطر الأوامر: `--cikti`). الناتج هو `klon_synthetic.wav` بوسم "synthetic"؛ وعند مشاركته ضع عليه علامة تفيد بأنه مولَّد بالذكاء الاصطناعي. سطر الأوامر: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## أسئلة شائعة

**نموذج أم محرك؟ ما الفرق؟** إن VoxCPM2 (من OpenBMB) هو *النموذج*: الشبكة ذات الملياري معامل التي تحوّل النص إلى كلام. وaudio.cpp
هو *المحرك*: برنامج C++/CUDA الذي يشغّل النموذج على بطاقتك (`audiocpp_cli.exe`). رقعتنا تغيّر المحرك لا النموذج: فهي تجعل VoxCPM2
يتسع في 4 GB، وتجعل البذرة نفسها تعطي الصوت نفسه في كل مرة. أما حزمة Python في هذا المستودع فلا تفعل سوى تحضير النص واستدعاء
المحرك وجمع الملفات.

**ما البطاقات المدعومة؟** انظر «البطاقات المدعومة» أعلاه: بطاقات NVIDIA من GTX 10xx فما فوق، بذاكرة VRAM من 4 GB أو أكثر، وتعريف ≥ 570.
في الإصدار شيفرة أصلية لـ sm_61/75/86/89/120a؛ أما البطاقات الأخرى من جيل Pascal فما بعده فتستخدم PTX المضمّن (بداية أولى أبطأ).
بطاقات AMD/Intel: ملف zip تجريبي لـ Vulkan، `kur.ps1 -Vulkan`؛ وقد أفاد مستخدم خارجي بأنه شغّله على AMD 6900 XT، لكن ما زالت هناك حاجة
إلى اختبارات أوسع على AMD/Intel (انظر «AMD / Intel» أعلاه). التشغيل على المعالج المركزي وحده (`"backend": "cpu"` في `ayarlar.json`)
ممكن لكنه أبطأ بنحو 6× من GTX 1050 Ti (قياس للمحرك: 535 ثانية مقابل 94 ثانية لـ 48 ثانية من الكلام)؛ وهو ليس مسارًا مدعومًا.

**ما السرعة؟** قيست على GTX 1050 Ti بذاكرة 4 GB (i7-7700HQ): نسخة تصميم واحدة (تسجيل ≈ 25 ثانية) في 55 ثانية؛ والقراءة ≈ 2 ثانية
حساب لكل ثانية كلام (معامل الزمن الحقيقي 1.9-2.8)، بعد ترميز مرجعي لمرة واحدة يستغرق نحو 50 ثانية لكل صوت (يُخزَّن على القرص)
و10-20 ثانية لتحميل النموذج في كل دفعة؛ وذروة VRAM بين 2.6 و2.9 GB. البطاقات الأحدث أسرع؛ الأرقام والمنهجية:
[docs/4gb.md](docs/4gb.md).

**هل يمكنه استنساخ صوت؟** يستطيع نموذج VoxCPM2 الأساسي محاكاة صوت انطلاقًا من تسجيل مرجعي، وقسم الاستنساخ يستخدم ذلك. لا تستخدمه
إلا مع صوتك أنت أو بإذن صريح من صاحب الصوت؛ وتطلب منك الواجهة تأكيد هذا الإذن. لا يحتاج تصميم الصوت إلى أي تسجيل: فهو يبدأ من وصف
نصي بالإنجليزية أو الصينية، و«المرجع» المستخدم لقراءة صوت مصمَّم هو تسجيل التصميم الاصطناعي الذي أنتجه النموذج نفسه. انتحال الشخصية
والاحتيال والتضليل أمور محظورة. انظر [ETHICS.md](ETHICS.md). ضع على ما تنشره علامة تفيد بأنه مولَّد بالذكاء الاصطناعي.

**كيف أكتب وصفًا جيدًا للصوت؟** بالإنجليزية، في جملة إلى ثلاث جمل: العمر والجنس، والنبرة (عميقة/مشرقة، دافئة، أنفية، مبحوحة)،
والطابع والدور (راوٍ وثائقي هادئ، مقدم حيوي)، والإيقاع (بطيء، متزن)، و"clean studio recording, no background noise". اجعله وصفًا لا
نصًا للقراءة؛ ودون أقواس. اطلب 3-5 نسخ واستمع إليها: فالبذرة تغيّر الصوت كثيرًا. ولنص الإنشاء استخدم جملة أو جملتين طبيعيتين بلغة
الصوت، بالمزاج الذي تريده (بحد أقصى نحو 20 ثانية من الكلام). وعند القراءة، جملة واحدة في كل سطر؛ قسّم الجمل الطويلة، واكتب الأعداد بالحروف.

## المساهمة

لا تعرف من أين تبدأ؟ هذه المسائل الأربع الصغيرة خطوة أولى جيدة:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) جرّبه على بطاقتك وأخبرنا بالبطاقة والتعريف والأزمنة
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) بطاقات AMD / Intel: جرّب نسخة Vulkan التجريبية
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) أضف جملة إلى مجموعة الاختبار
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) شارك صوتًا صممته، مع وصفه وبذرته

مجموعة الاختبار المشتركة: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt)؛ دليل صوت العلامة التجارية:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md)؛ كيف ترسل شيفرة: [CONTRIBUTING.md](CONTRIBUTING.md).
مشاكل التثبيت: [نموذج البلاغ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)؛ الأسئلة والنتائج: [النقاشات](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
يلتزم كل المشاركين بـ[قواعد السلوك](CODE_OF_CONDUCT.md): كن لطيفًا، واجعل ملاحظاتك عن العمل.

## المساهمون

- المشرف على المشروع [@alexturkey](https://github.com/alexturkey): الشيفرة والأصوات الجاهزة والتوثيق
- دعم Metal لنظام macOS (Apple Silicon) من [@cayir21](https://github.com/cayir21)، [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- إصلاح نهاية الجملة (EOS) لقراءة جمل متعددة على واجهة CPU الخلفية من [@grogureis](https://github.com/grogureis)، [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)

مكان اسمك هنا أيضًا: نتيجة اختبار من بطاقتك، أو جملة لمجموعة الاختبار، أو صوت صممته، أو بلاغ واضح عن خلل، أو طلب سحب (pull request)،
كلها تُحسب مساهمات. شكرًا لكل من يجرّبه ويكتب لنا.

## الترخيص والشكر

الشيفرة والأصوات المرفقة: Apache-2.0، Copyright 2026 Ali Haydar Ozturk. مبني على VoxCPM2 (OpenBMB، Apache-2.0) وaudio.cpp
(ShugoAI LLC، Apache-2.0) وتحويل GGUF الخاص بـ audio.cpp. القائمة الكاملة: [THIRD_PARTY.md](THIRD_PARTY.md).
لا ارتباط للمشروع بـ OpenBMB أو ModelBest أو مشروع audio.cpp.

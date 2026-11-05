[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · **עברית** · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**עיצוב קולות בטורקית עם VoxCPM2 על כרטיס מסך של 4 GB.** תארו קול באנגלית, תנו למודל ליצור אותו, בחרו את הגרסה
שאהבתם, ואז הקריאו בקול הזה כל טקסט בטורקית. כלולים מתקין בפקודה אחת, מנוע [audio.cpp](https://github.com/0xShug0/audio.cpp)
מתוקן שנכנס ב-GTX 1050 Ti (4 GB), ממשק ווב מקומי קטן וארבעה עשר קולות סינתטיים מוכנים: שבעה בטורקית ושבעה קריינים ילידיים
באנגלית, צרפתית, גרמנית, ספרדית, רוסית, סינית ויפנית.

- האפליקציה מקריאה ב-30 שפות, וגם הממשק זמין ב-30 שפות.
- קולות מוכנים, 14 בסך הכול: 7 בטורקית, ועוד אחד בכל אחת מהשפות אנגלית, צרפתית, גרמנית, ספרדית, רוסית, סינית ויפנית.
- ממשק הווב (v0.2.0): בכל כרטיס גרסה יש שני קולות, קול העיצוב הגולמי והקול שתשמעו מעכשיו; רשימת קריאה עם תפריט קולות;
  שינוי שם, הסתרה או מחיקה של קולות; טיוטות לטקסטים שאתם מקריאים. ראו «ממשק הווב» בפרק «שימוש».

[איך זה נכנס ב-4 GB](docs/4gb.md) · [אובונטו / Linux](docs/linux.md) · [מערכת macOS](docs/mac.md) · [מדריך התקנה לסוכני AI](AGENTS.md) · [שימוש אחראי](ETHICS.md)

> הקולות הכלולים סינתטיים ועוצבו מתוך תיאור טקסטואלי. פרק שכפול הקול מיועד רק לקול שלכם או לקול שנעשה בו שימוש באישור מפורש של בעליו; הממשק מבקש מכם לאשר זאת. התחזות, הונאה והטעיה אסורות. סמנו את מה שאתם מפיקים כתוכן שנוצר בבינה מלאכותית. ראו [ETHICS.md](ETHICS.md).

## תמיכה ב-30 שפות

הכנו סרט תיעודי אחד על קפדוקיה ב-8 שפות: טורקית, אנגלית, צרפתית, גרמנית, ספרדית, רוסית, סינית ויפנית. לכל שפה יש
**קריין ילידי** משלה, שעוצב עם VoxCPM2 מתוך תיאור באנגלית. הכול הופק באופן מקומי לחלוטין על GTX 1050 Ti של 4 GB, באותה
איכות קבועה (16 צעדים, cfg 2.0). שבעת הקריינים כלולים כאן, עם התיאור, טקסט העיצוב, הזרע (seed) והקלטת הייחוס של כל אחד.

| קוד | שפה | קול | האזנה | וידאו |
|---|---|---|---|---|
| `tr` | טורקית | `hazir/belgesel_hanim` (ועוד 6) | [דוגמה](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | אנגלית | `hazir/anlatici_en` | [דוגמה](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113791986763440439) |
| `fr` | צרפתית | `hazir/anlatici_fr` | [דוגמה](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113790681575804962) |
| `de` | גרמנית | `hazir/anlatici_de` | [דוגמה](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113791351645262249) |
| `es` | ספרדית | `hazir/anlatici_es` | [דוגמה](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113807365611122705) |
| `ru` | רוסית | `hazir/anlatici_ru` | [דוגמה](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113801574136848884) |
| `zh` | סינית (מנדרינית) | `hazir/anlatici_zh` | [דוגמה](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113802229606121794) |
| `ja` | יפנית | `hazir/anlatici_ja` | [דוגמה](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [וידאו](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**למה משפט אחרי משפט.** מודל VoxCPM2 אינו יציב ביצירה ארוכה אחת (בערך מעל 30 שניות): הקצב מאיץ והקול עלול לסטות. כאן את
הקול נושאות הקלטת ייחוס קבועה וזרע קבוע, וטקסט ארוך מוקרא משפט אחד בכל שורה, כך שהגוון והסגנון נשארים זהים מהמשפט הראשון
ועד האחרון. בשפות שאינן טורקית מילון ההגייה הטורקי אינו מופעל. כל 30 השפות ש-VoxCPM2 תומך בהן נבדקו ועובדות; לשפות שאין
להן קול כלול השתמשו ב-`--dil <code>`. פקודות לכל שפה והלקחים שלמדנו: [docs/cok_dilli.md](docs/cok_dilli.md). מיומנות
(skill) של Claude Code לכל תהליך העיצוב: [.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**תיאורים לדוגמה, 144 במספר, כנקודת התחלה.** 18 תפקידים (קריין סרטים תיעודיים, מגיש חדשות, קול פרסומות, ספר מוקלט, סבתא
מספרת סיפורים, מגיש פודקאסט, מורה, טריילר לסרט, מדריך מדיטציה, פרשן ספורט ועוד, גברים ונשים) בכל אחת מ-8 השפות. התיאור
באנגלית וכולל את הלאום של הדובר ואת המבטא הילידי שלו; איתו מגיע הטקסט שמוקרא בזמן יצירת הקול, באותה שפה ומותאם לתפקיד. בחרו
אחד, האזינו לגרסאות ושמרו את זו שאהבתם: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, או בחרו
*תיאור לדוגמה* בממשק הווב. הרשימה המלאה: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**דבבו את הסרטונים שלכם בקול שלכם.** התוכנה [DubWorld](https://github.com/alexturkey/dubworld) היא תוכנת הדיבוב המקומית שלנו
לווידאו; היא מתקינה את המאגר הזה כמנוע הקול VoxCPM2 שלה. קול שתעצבו כאן ישמש שם באמצעות
`ses.voxcpm2_ses = "<name>/<variant>"`.

## התחלה מהירה (Windows, שלושה שלבים)

1. **הורידו** את הקוד: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   את חבילת המנוע המוכנה לכרטיס שלכם המתקין מוריד בשלב 3:
   כרטיסי NVIDIA ← [חבילת CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   כרטיסי AMD / Intel ← [חבילת Vulkan, ניסיונית](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (כבר הורדתם אחת? הוסיפו `-HazirZip <path to the zip>` לפקודה שלמטה).
2. **חלצו** את קובץ ה-zip, פתחו את התיקייה `voxcpm2-turkce-ses-tasarimi-main`, הקלידו `powershell` בשורת הכתובת של סייר הקבצים
   והקישו Enter.
3. **הריצו** את המתקין (נדרש Python 3.10-3.13 בגרסת 64-bit; עבור CUDA נדרש דרייבר NVIDIA ≥ 570), ואז לחצו לחיצה כפולה על **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   בכרטיסי AMD / Intel: הוסיפו `-Vulkan` בסוף. הממשק נפתח בכתובת http://127.0.0.1:8765/.

קובץ ה-zip של המנוע אינו אפליקציה עצמאית (קובץ ה-exe שבו צריך את המודל ואת קובצי ה-DLL שהמתקין מכין). פרטים, רשימת כרטיסים
ובעיות נפוצות: ראו «התקנה מהירה» בהמשך.

## מערכת Ubuntu / Linux (NVIDIA CUDA, ניסיוני)

בנו את המנוע המתוקן עם `bash scripts/kur-linux.sh`, או השתמשו ב-`Dockerfile.linux` כדי לבנות ולהריץ בסביבת Ubuntu 24.04 / CUDA 12.8.1.
נדרשים כרטיס NVIDIA ודרייבר תואם; המתקין המקומי צריך בנוסף את CUDA toolkit ו-Python 3.10-3.13. הממשק נשאר מוגבל ל-loopback, גם
בשרתים מרוחקים (העברה דרך SSH). דרישות מקדימות, פקודות, בחירת ארכיטקטורה והיקף האימות: [docs/linux.md](docs/linux.md).

## התחלה מהירה (macOS, Apple Silicon)

נדרשים Xcode Command Line Tools (`xcode-select --install`) ו-[Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
המתקין מוריד את המודל, בונה את המנוע המתוקן עם Metal (כדקה) ומכין הכול תחת `~/vox`. לאחר מכן לחצו לחיצה כפולה על
**`baslat.command`**. ב-MacBook Air M4 עם 16 GB: כ-2 שניות חישוב לכל שנייה של דיבור, אותו זרע נותן שמע זהה עד רמת הבייט, שיא
של כ-5.3 GB RAM, ואין האטה תרמית לאורך 12 דקות של הקראה רצופה. פרטים ומדידות: [docs/mac.md](docs/mac.md).

**אפליקציית Mac מקורית (בלי Python, Homebrew או Terminal):** [macos/README.md](macos/README.md). היא כוללת את אותו מנוע מתוקן
ומורידה את המודל בהפעלה הראשונה; בינתיים בונים אותה מקוד המקור עם Xcode.

## למשתמשי Mac (Apple Silicon)

קיימת גם התאמה עצמאית מטעם הקהילה למחשבי Mac עם Apple Silicon, שמריצה את VoxCPM2 עם מסגרת העבודה MLX של Apple:
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
אמרה קוץ' (Emre Koç, [@emre-koc](https://github.com/emre-koc)) מפתח ומתחזק אותה במאגר משלו, לא כאן; שלבי ההתקנה ושאלות
התמיכה מופנים לשם. תודה, אמרה, שהבאת את הפרויקט הזה ל-Mac!

## איך זה עובד

1. **עיצוב קול.** *תיאור הקול* באנגלית + *טקסט שמוקרא בזמן יצירת הקול* (בשפת הקול) + מספר גרסאות. כל גרסה מקבלת זרע משלה;
   המנוע מקבל `(description)text` ומחזיר הקלטת עיצוב אחת לכל זרע. הטקסט הוא דוגמה קצרה להכרת הקול: משפט עד שלושה משפטים, לכל
   היותר כ-30 שניות (הממשק מציג את ההערכה ולא יתחיל מעל 33 שניות); מקומו של טקסט ארוך בשלב 2.
2. **הקראה מבוססת ייחוס.** הקלטת העיצוב מועברת **לשני** הקלטים של המנוע (`audio` ו-`voice_ref`), יחד עם התמליל שלה
   (`reference_text`) והטקסט החדש להקראה, עם אותו זרע. את הקול נושאת ההקלטה ולא התיאור, ולכן הוא לא סוטה מטקסט לטקסט.
   הטקסט מוקרא משפט אחרי משפט.
3. האיכות קבועה: 16 צעדי דיפוזיה, CFG 2.0. הזרע אינו כפתור איכות.
4. **תזמון מילים, אותו שמע בכל הרצה.** בזמן הקריאה המנוע עצמו מציין היכן כל מילה מתחילה ונגמרת (תיקון 0002, בלי מודל נוסף). הזמנים נכתבים ל-`kelimeler.json`, והשורות נחתכות כך שהרווח בין שורות שווה להגדרת ההשהיה. דיוק ביחס ליישור מאולץ (forced alignment) של CTC, שנחשב ל-100%: ‏89.66% (טורקית, 12 קולות; ההגדרה `kelime_zamani` פעילה כברירת מחדל). עם תיקון 0003 אותו זרע נותן שמע זהה ברמת הבייט בכל הרצה.

הקלטת העיצוב הגולמית היא דגימה חד-פעמית של הקול; אף הקראה מאוחרת יותר לא תישמע בדיוק כמוה. מה שאתם שומעים בכל הקראה מאוחרת
הוא שלב 2: הקלטת העיצוב כייחוס, יחד עם הזרע של הגרסה. לכן ממשק הווב מבצע את שלב 2 מיד אחרי העיצוב ומציג את שניהם בכרטיס הגרסה.

המנוע הוא audio.cpp v0.7.2 עם התיקון (patch) שלנו (`patches/`), והמודל הוא VoxCPM2 Q8_0 GGUF. שיא VRAM ≈ 2.8 GB; כ-2 שניות
חישוב לכל שנייה של דיבור על GTX 1050 Ti. פרטים ומדידות: [docs/4gb.md](docs/4gb.md).

## קולות כלולים (`hazir_sesler/`)

כל ארבעה עשר הקולות עוצבו מהתיאורים השמורים בקובץ `ses.json` שלהם; אף אחד מהם לא שוכפל מהקלטה (שכפול הוא הלשונית הנפרדת
*שכפול קול*, שמחייבת הסכמה).

| קול | תיאור קצר | האזנה |
|---|---|---|
| `belgesel_hanim` | אישה בוגרת בשנות החמישים לחייה, אלט עמוק וחם; קריינית תיעודית רגועה | [דוגמה](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [ייחוס](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | קריין גבר עמוק, עוצמתי ומסתורי | [דוגמה](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [ייחוס](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | מגיש חדשות ותיק כבן שבעים, רגוע וסמכותי | [דוגמה](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [ייחוס](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | מגישת מהדורת ערב כריזמטית בשנות השלושים לחייה, קטיפתית ומלאת הבעה | [דוגמה](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [ייחוס](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | מכשפה מאגדות: נמוכה, מעט אנפופית, מתוקה בערמומיות | [דוגמה](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [ייחוס](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | קריין גבר עמוק, דחוס ובעל סמכות באופן יוצא דופן | [דוגמה](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [ייחוס](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | זקן חכם, קול עמוק ורועם, מעט מסתורי | [דוגמה](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [ייחוס](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | קריין תיעודי גבר, דובר אנגלית ילידי בשנות החמישים לחייו (General American); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | קריין תיעודי גבר, דובר צרפתית ילידי בשנות החמישים לחייו (פריזאי); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | קריין תיעודי גבר, דובר גרמנית ילידי בשנות החמישים לחייו (Hochdeutsch); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | קריין תיעודי גבר, דובר ספרדית ילידי בשנות החמישים לחייו (קסטיליאנית (מדריד)); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | קריין תיעודי גבר, דובר רוסית ילידי בשנות החמישים לחייו (מוסקבה); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | קריין תיעודי גבר, דובר סינית (מנדרינית) ילידי בשנות החמישים לחייו (פוטונגהואה של בייג'ינג); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | קריין תיעודי גבר, דובר יפנית ילידי בשנות החמישים לחייו (תקן טוקיו); עמוק, רגוע, חם | [דוגמה](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [ייחוס](hazir_sesler/anlatici_ja/referans.flac) |

בכל תיקייה: `referans.flac` (הקלטת עיצוב ללא אובדן), `ses.json` (תיאור, תמליל, זרע עיצוב, זרע הקראה, תיאור קצר; `dil` = השפה
אצל הקריינים), `ornek_okuma.mp3` (+ הטקסט שלו). אפשר להשתמש בהם ישירות: `--ses hazir/<name>`. הקלטות הייחוס של הקריינים קצרות
(5.6-10 שניות); הדוגמאות שלהם הן שלושת המשפטים הראשונים של התסריט על קפדוקיה, שנחתכו מההקראה המלאה של ההפקה.

## התקנה מהירה, בלי מהדר (Windows 10/11, כרטיס NVIDIA ≥ 4 GB)

דרישות מקדימות: דרייבר NVIDIA ≥ 570 ו-Python 3.10-3.13 בגרסת 64-bit (`winget install Python.Python.3.12`). שום דבר נוסף: בלי
Visual Studio ובלי מתקין CUDA. לא בטוחים איזה כרטיס יש לכם? הריצו `nvidia-smi` ב-PowerShell: הוא מציג את שם הכרטיס, גרסת הדרייבר
והזיכרון. אין לכם כרטיס NVIDIA? ראו «AMD / Intel» בהמשך.

באמצעות [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

בלי Git: בעמוד הזה לחצו על **Code → Download ZIP**, חלצו את הקובץ, פתחו את התיקייה `voxcpm2-turkce-ses-tasarimi-main` שחולצה,
הקלידו `powershell` בשורת הכתובת של סייר הקבצים והקישו Enter, ואז הריצו את השורה האחרונה שלמעלה. Git נדרש רק לבנייה מקוד המקור.

האפשרות `-ExecutionPolicy Bypass` חלה על התהליך הזה בלבד ואינה משנה אף הגדרת מערכת; קראו את `scripts\kur.ps1` לפני שאתם מריצים
אותו, כמו כל סקריפט התקנה. פקודה אחת, כ-10 דקות, הורדה של כ-3.7 GB, והכול מאומת ב-sha256: המודל (2.95 GB), קובצי ה-DLL של סביבת
הריצה CUDA 12.8 כקובצי zip ניידים (בלי התקנה במערכת, בלי לגעת ב-PATH), **המנוע הבנוי מראש** מעמוד ה-Releases, סביבת `.venv` עם שתי
חבילות Python, הקובץ `ayarlar.json` ובדיקת כרטיס מסך סופית (`KONTROL_OK`). אם משהו נכשל, הריצו שוב; קבצים שכבר אומתו מדולגים.
לאחר מכן הפעילו את ממשק הווב: לחצו לחיצה כפולה על **`baslat.bat`** בתיקיית המאגר. הוא מפעיל את הממשק ופותח את
**http://127.0.0.1:8765/** בדפדפן כשהוא מוכן; כדי לעצור, סגרו את החלון השחור (או הקישו בו Ctrl+C).
אותו דבר מ-PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
ואז פתחו בעצמכם את **http://127.0.0.1:8765/** (כשמפעילים כך, הממשק לא פותח את הדפדפן; הוא מאזין ל-localhost בלבד).

> **הקובץ `audiocpp_cli.exe` שב-zip של הגרסה לא נועד ללחיצה כפולה.** זהו מנוע שורת פקודה שצריך לידו את קובצי ה-DLL של CUDA ואת המודל; `kur.ps1` מציב הכול במקום, וחבילת ה-Python היא שמפעילה אותו. לחיצה כפולה עליו רק מציגה "cudart64_12.dll not found".

**כרטיסים נתמכים (גרסה v0.1.1):** קוד מקורי ל-GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx (sm_89) ו-RTX 50xx
(sm_120a); כל כרטיס CUDA אחר מדור Pascal ואילך מריץ את ה-PTX המוטמע דרך הדרייבר (הפעלה ראשונה איטית יותר). דור Maxwell (GTX 9xx)
וישנים יותר אינם נתמכים ב-CUDA 12.8. נבדק על ידינו על GTX 1050 Ti של 4 GB (גם דרך Docker Desktop/WSL2 ב-Windows, שורת פקודה בלבד);
נמדד על ידי @mslmyilmaz5 (#15): RTX 3060 Ti של 8 GB, Ubuntu 24.04 Docker, CUDA 12.8.1 (פרטים ב-[docs/linux.md](docs/linux.md)).
דיווחים מכרטיסים אחרים יתקבלו בברכה ב-[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**כרטיסי AMD / Intel (ניסיוני):** קובץ zip נפרד של מנוע Vulkan (`...-win64-vulkan.zip`, בלי CUDA) מותקן עם
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. הוא אומת רק על כרטיס ה-NVIDIA שלנו דרך ה-backend של Vulkan (שם הוא רץ לאט יותר מ-CUDA אבל
נתן את אותו שמע לאותו זרע; המדידה נעשתה כשהדיסק היה עסוק בעבודה אחרת, כך שהשוואת מהירות נקייה עדיין ממתינה), ו**לא** בדקנו אותו
בעצמנו על חומרת AMD או Intel: אם תנסו, פרסמו את התוצאה ב-Discussions. כשיש יותר מהתקן Vulkan אחד (משולב + נפרד), המתקין כותב
את האינדקס של הכרטיס הנפרד כ-`cihaz` בקובץ `ayarlar.json`.

*הערה: התמיכה ב-Vulkan ניסיונית כרגע. היא נבנתה ונבדקה בהצלחה על GTX 1050 Ti. משתמש חיצוני (mitra_tr) דיווח גם שהריץ אותה על AMD 6900 XT. עדיין נדרשות בדיקות רחבות יותר על כרטיסי AMD/Intel.*

**בדיקת קהילה (AMD):** @mitraTR הריץ את v0.1.1 עם Vulkan על AMD Radeon RX 6900 XT ב-Windows 11: ההתקנה, עיצוב הקול, ההקראה, ממשק הרשת והבדיקות עבדו; ההקראה דרשה כ-0.8-0.9 שנ׳ חישוב לכל שנייה של דיבור ([הדוח ב-#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). התקינו בתיקייה קצרה שהנתיב שלה כולל רק תווי ASCII (למשל `C:\vox`): ב-Windows המנוע לא מצליח לפתוח נתיבים עם עברית או תווים אחרים שאינם ASCII. כל הדוחות עד עכשיו: [חומרה שנבדקה](docs/donanim_testleri.md).

**הערות על Vulkan:** תזמוני מילים זמינים כרגע רק ב-NVIDIA ‏(CUDA) וב-Mac; ב-AMD/Intel הם לא נוצרים עד שמנוע ה-Vulkan יעודכן (ההקראה עצמה עובדת). ההפעלה הראשונה ב-Vulkan עשויה להימשך כמה דקות, כי ה-shaders של כרטיס המסך עוברים הידור; ההקראות הבאות מהירות יותר.

### חלופה: בניית המנוע מקוד המקור

נדרשים Visual Studio 2022 Build Tools עם "Desktop development with C++" (כולל C++ CMake tools), כ-7 GB. לאחר מכן:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
הפקודה גם מורידה את nvcc, מביאה את קוד המקור של audio.cpp v0.7.2, מחילה את `patches/0001-voxcpm2-4gb-ve-hiz.patch` ובונה לכרטיס
שלכם (`-Mimari native` כברירת מחדל, או למשל `-Mimari 61`), כ-15-25 דקות. שמרו על נתיב שורש קצר (`C:\vox`): nvcc נכשל בנתיבים
ארוכים. שלב אחר שלב עם בדיקות: [AGENTS.md](AGENTS.md).

### בעיות התקנה נפוצות

| מה רואים | מה זה אומר ומה לעשות |
|---|---|
| ההודעה `cudart64_12.dll not found` אחרי לחיצה כפולה על ה-exe | המנוע לא נועד להפעלה ידנית. הריצו את פקודת `kur.ps1` שלמעלה ואז הפעילו את ממשק הווב. |
| `64-bit Python 3.10+ bulunamadı` (לא נמצא Python) | התקינו Python (`winget install Python.Python.3.12`), סגרו את PowerShell, פתחו חלון חדש והריצו שוב את אותה פקודה. |
| `motor ekran kartını görmedi` (המנוע לא זיהה את הכרטיס) | עדכנו את דרייבר NVIDIA לגרסה 570 ומעלה; ודאו ש-`nvidia-smi` רץ. |
| `indirme başarısız` / `sha256 tutmadı` (ההורדה נכשלה / אי-התאמה בסכום הביקורת) | בדרך כלל הורדה שנקטעה. הריצו שוב את אותה פקודה; קבצים שכבר אומתו מדולגים. |
| בנייה מקוד המקור: `nvcc` נכשל | שמרו על שורש התקנה קצר (`-Kok C:\vox`). |
| הדף לא נפתח | הפעילו את הממשק עם `baslat.bat`, או פתחו בעצמכם את http://127.0.0.1:8765/. הפורט תפוס? שנו את `"port"` בקובץ `ayarlar.json`. |

יש בעיות? [דיונים (שאלות ותשובות)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) או
[דיווח על בעיית התקנה](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
עם הכרטיס שלכם, גרסת Windows, הפקודה והשורות האחרונות של הפלט שלה.

## שימוש

שורת הפקודה:
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
כללי טקסט: כתבו מספרים במילים, בלי מירכאות (הכלי דוחה ספרות ומירכאות), משפט אחד בכל שורה, עד 2000 תווים בשורה. השהיה אחרי שורה:
`|| bagli` 0.25 שנ', `|| normal` 0.5 שנ', `|| paragraf` שנייה אחת, `|| agir` 1.5 שנ', או אורך משלכם `|| 0,8` (0-5 שניות; הספרות
של הסימון מותרות). הקובץ `ayarlar/okunus_sozlugu.tsv` מתקן הגייה של מילים לועזיות בטקסט טורקי.
השפה מזוהה מהטקסט (אותיות טורקיות, כתב, מילים נפוצות; במקרה של ספק, הערך `dil` בכרטיס הקול; `--dil <code>` הוא אופציונלי). בטקסט
שאינו טורקי מותרים שם גרשים, המילון הטורקי מדולג, וספרות עדיין נדחות. אם הקראה מדפיסה `speed gate: satır [...]`, האזינו לשורות האלה.

### ממשק הווב

מקומי בלבד (127.0.0.1): הריצו `.venv\Scripts\python.exe -m ses_tasarim.arayuz` ← ופתחו בעצמכם את http://127.0.0.1:8765/
(פורט אחר: `--port 8800`), או לחצו לחיצה כפולה על `baslat.bat`. עוצרים את השרת עם Ctrl+C. שלוש לשוניות: *עיצוב קול*,
*הקראה בקול הזה*, *שכפול קול*. המסלול הרגיל: *עיצוב* ← האזנה לגרסאות ← *הוספה לרשימת הקריאה שלי* ←
*הקראה בקול הזה* ← הורדה. או בחרו קול כלול מתפריט הקולות והקריאו.

- **הגרסה בכותרת.** טקסט קטן ודהוי `v0.2.0 · <short commit>` (עם `+` כשיש בקבצים במעקב שינויים שלא נשמרו ב-commit; בלי git, רק
  הגרסה), כדי שצילומי מסך וסרטונים יראו באיזו גרסה השתמשו.
- **שני קולות בכל כרטיס גרסה.** למעלה, באפור, *קול עיצוב גולמי*: הוא נוצר פעם אחת ולעולם לא ייצא שוב אותו דבר. מתחתיו, במסגרת
  כתומה, *↻ זה הקול שתשמעו מעכשיו*: הקלטת העיצוב מוקראת מחדש כייחוס עם הזרע של הגרסה (מוצג על הכרטיס). כך נשמע הקול בכל הקראה
  מאוחרת. מתחתיו נמצאים *הקראה בקול הזה* ו-*הוספה לרשימת הקריאה שלי*. לחיצה אחת על *עיצוב* עושה את שניהם: היא מעצבת את כל
  הגרסאות ואז מקריאה את הטקסט שלכם בכל קול קבוע; פס התקדמות יחיד סופר את שני השלבים. תיקיית הגרסה מקבלת `dinleme.wav`. אם
  ההקראה הזו נעצרת מוקדם, העיצוב נשמר והכרטיס מציג הערה.
- **החלון «טקסט שתרצו לשמוע».** בלשונית *עיצוב קול*, התיבה *↻ טקסט שתרצו לשמוע* מכילה את מה שכל קול קבוע מקריא (אם היא נשארת
  ריקה, מוקרא משפט הדוגמה). לחיצה עליה פותחת את מחברת ההקראה בחלון: מספרי שורות, תפריט שורה, פסי השהיה. *אישור* כותב את
  הטקסט ואת ההשהיות שלו חזרה לתיבה; *ביטול* או Esc לא משנים דבר. לשונית ההקראה שומרת על הטקסט שלה.
- **מחברת ההקראה.** משפט אחד בכל שורה. לחצו על מספר שורה לתפריט השורה (הזזה למעלה או למטה, הזזה למיקום, שכפול, מחיקה;
  Alt+↑/↓, Alt+Shift+↓ או גרירה לפי המספר; Ctrl+Z מבטל טקסט והשהיות יחד). לחצו על הפס הדק שבין שתי שורות כדי לבחור השהיה
  (bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 שנ', או משך משלכם 0-5 שנ' עם גלגל השיניים); הקישו Enter פעמיים לפסקה (שנייה
  אחת), ושורות ריקות הופכות לפסי השהיה. בזמן שהתוצאה מתנגנת, השורה המוקראת זוהרת ונגללת לתצוגה; *▶ האזנה מכאן* בתפריט השורה מנגן
  מאותה שורה. הטקסט וההשהיות שלו שורדים רענון של הדף (אחסון הדפדפן).
- **טיוטות.** הכפתור *📄 טיוטות* נמצא בשתי המחברות (לשונית ההקראה והחלון). שמרו את הטקסט הנוכחי עם ההשהיות שלו כטיוטה, טענו
  טיוטה בלחיצה (Ctrl+Z מבטל), והשתמשו ב-⋯ כדי לדרוס, לשנות שם או למחוק. הטיוטות נשמרות ב-`sesler/taslaklar.json`, אף פעם לא במאגר.
- **רשימת הקריאה ותפריט הקולות.** בכרטיס גרסה, *הוספה לרשימת הקריאה שלי* פותח תיבת שם: תנו לגרסה שם משלה ו-✓ מוסיף אותה.
  *שם היצירה* נשאר על כל הגרסאות של אותה הרצה. בלשונית *הקראה בקול הזה*, כפתור הקול (דגל + שם) פותח את תפריט הקולות: *רשימת
  הקריאה שלי* למעלה, ואחריה הקולות הכלולים עם דגלים (שפת הממשק קודם). בכל שורה יש ▶ האזנה (לקול הקבוע, כשיש כזה), לב (הוספה
  או הסרה) ו-⋯; ↑/↓ ו-Enter בוחרים, Esc סוגר, והקול האחרון נזכר. הרשימה נשמרת ב-`sesler/okuma_listesi.json`, מחוץ למאגר,
  ושורדת הפעלות מחדש.
- **ניהול קולות.** בתפריט ⋯ (שורה בתפריט הקולות או כרטיס גרסה) יש *הקראה בקול הזה*, הוספה לרשימה או הסרה ממנה, *שינוי שם* (שם
  ריק מחזיר את המקורי; *חזרה לשם המקורי*), *מחיקה* לקולות שעוצבו ו-*הסתרה* לקולות הכלולים; שתיהן מבקשות אישור קודם. קול שנמחק
  עובר ל-`sesler/_cop/`; הסתרה לעולם לא נוגעת בקובצי המאגר. בתחתית תפריט הקולות, *קולות מוסתרים ומחוקים (N)* כולל *שחזור*.
  שמות מותאמים וקולות מוסתרים נשמרים ב-`sesler/yerel_katman.json`. קול ששמו שונה מציג את מקורו באפור (*שם היצירה · גרסה N*);
  ⋯ ← *מעבר ליצירה* פותח את העיצוב שלו.
- **קיצורים וקבצים.** Ctrl+Enter (⌘+Enter ב-Mac) מפעיל את *עיצוב* או את *הקראה בקול הזה* בלשונית הפתוחה. פס ההתקדמות מציג
  *עבר / ~סה"כ*, עם הערכה שנלמדת מעבודות קודמות במחשב שלכם. הקובץ שמורד נקרא על שם הקול והשעה (`Voice_Name_2026-11-02_0152.wav`).

**שכפול קול (הקול שלכם או קול באישור).** בלשונית *שכפול קול* של הממשק, ספקו את ההקלטה שלכם (wav/mp3/flac/ogg; מומלץ 5-30 שניות של דיבור נקי; פחות מ-3 שניות נדחה, מעל 36 שניות נחתך), את התמליל המדויק שלה ואת הטקסט להקראה. הכפתור נשאר מושבת עד שתסמנו «הקול הזה שלי או שיש לי אישור מפורש מבעליו». ההקלטה נשלחת רק לשרת המקומי (127.0.0.1), מעובדת בתיקייה זמנית יחד עם קידוד הייחוס שלה, והתיקייה נמחקת כשהעבודה מסתיימת, גם אם היא נכשלה; שום דבר לא נשלח ברשת. רק הפלט הסינתטי נשמר (ממשק: `sesler/_okumalar/<job>/`, שורת פקודה: `--cikti`). הפלט הוא `klon_synthetic.wav` עם תגית "synthetic"; כשאתם משתפים, סמנו אותו כתוכן שנוצר בבינה מלאכותית. שורת פקודה: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## שאלות נפוצות

**מודל או מנוע? מה זה מה?** VoxCPM2 (OpenBMB) הוא ה*מודל*: הרשת בת 2 מיליארד הפרמטרים שהופכת טקסט לדיבור. audio.cpp הוא
ה*מנוע*: תוכנת C++/CUDA שמריצה את המודל על כרטיס המסך שלכם (`audiocpp_cli.exe`). התיקון שלנו משנה את המנוע, לא את המודל: הוא
גורם ל-VoxCPM2 להיכנס ב-4 GB, וגורם לאותו זרע לתת את אותו שמע בכל פעם. חבילת ה-Python שבמאגר רק מכינה את הטקסט, קוראת למנוע
ואוספת את הקבצים.

**אילו כרטיסים?** ראו «כרטיסים נתמכים» למעלה: NVIDIA מ-GTX 10xx ומעלה, 4 GB VRAM או יותר, דרייבר ≥ 570. בגרסה יש קוד מקורי
ל-sm_61/75/86/89/120a; כרטיסים אחרים מדור Pascal ואילך משתמשים ב-PTX המוטמע (הפעלה ראשונה איטית יותר). AMD/Intel: קובץ zip
ניסיוני של Vulkan, `kur.ps1 -Vulkan`; משתמש חיצוני דיווח שהריץ אותו על AMD 6900 XT, אבל עדיין נדרשות בדיקות רחבות יותר על
AMD/Intel (ראו «AMD / Intel» למעלה). הרצה על מעבד בלבד (`"backend": "cpu"` בקובץ `ayarlar.json`) עובדת, אבל איטית פי ~6 מ-GTX
1050 Ti (מדידת מנוע: 535 שנ' לעומת 94 שנ' עבור 48 שנ' של דיבור); זה לא מסלול נתמך.

**כמה מהר?** נמדד על GTX 1050 Ti של 4 GB (i7-7700HQ): גרסת עיצוב אחת (הקלטה של ≈ 25 שנ') 55 שנ'; הקראה ≈ 2 שנ' חישוב לכל שנייה
של דיבור (מקדם זמן אמת 1.9-2.8), אחרי קידוד ייחוס חד-פעמי של כ-50 שנ' לכל קול (נשמר בדיסק) ו-10-20 שנ' טעינת מודל לכל אצווה;
שיא VRAM של 2.6-2.9 GB. כרטיסים חדשים יותר מהירים יותר; מספרים ושיטה: [docs/4gb.md](docs/4gb.md).

**האם הוא יכול לשכפל קול?** מודל VoxCPM2 שבבסיס יכול לחקות קול מתוך הקלטת ייחוס, ופרק השכפול משתמש בזה. השתמשו בו רק עם הקול
שלכם או באישור מפורש של האדם שהקול שייך לו; הממשק מבקש מכם לאשר זאת. עיצוב קול אינו דורש הקלטה: הוא מתחיל מתיאור טקסטואלי
באנגלית או בסינית, וה«ייחוס» שמשמש להקראה בקול מעוצב הוא הקלטת העיצוב הסינתטית של המודל עצמו. התחזות, הונאה והטעיה אסורות. ראו
[ETHICS.md](ETHICS.md). סמנו את מה שאתם מפרסמים כתוכן שנוצר בבינה מלאכותית.

**איך כותבים תיאור קול טוב?** באנגלית, 1-3 משפטים: גיל ומגדר, גוון (עמוק/בהיר, חם, אנפופי, צרוד), טון ותפקיד (קריין תיעודי רגוע,
מגיש אנרגטי), קצב (איטי, מדוד), ו-"clean studio recording, no background noise". שמרו על תיאור, לא תסריט; בלי סוגריים. בקשו 3-5
גרסאות והאזינו: הזרע משנה את הקול מאוד. לטקסט היצירה השתמשו במשפט אחד עד שלושה משפטים טבעיים בשפת הקול, במצב הרוח שאתם רוצים (לכל היותר
כ-30 שניות של דיבור). בהקראה, משפט אחד בכל שורה; פצלו משפטים ארוכים, וכתבו מספרים במילים.

## תרומה לפרויקט

לא בטוחים מאיפה להתחיל? ארבע הסוגיות הקטנות האלה הן צעד ראשון טוב:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) נסו על כרטיס המסך שלכם ודווחו על הכרטיס, הדרייבר והזמנים
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) כרטיסי AMD / Intel: נסו את גרסת Vulkan הניסיונית
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) הוסיפו משפט לסט הבדיקה
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) שתפו קול שעיצבתם, עם התיאור והזרע שלו

**בדקו את כרטיס המסך שלכם וכתבו דוח:** לא צריך לתכנת, מספיק [טופס דוח בדיקת חומרה](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml); מכרטיסי Intel עדיין אין אף דוח.

סט הבדיקה המשותף: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); מדריך קול מותג:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); איך שולחים קוד: [CONTRIBUTING.md](CONTRIBUTING.md).
בעיות התקנה: [טופס דיווח](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); שאלות ותוצאות: [דיונים](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
כל המשתתפים פועלים לפי [קוד ההתנהגות](CODE_OF_CONDUCT.md): היו אדיבים, והשאירו את המשוב על העבודה.

## תורמים

- מתחזק הפרויקט [@alexturkey](https://github.com/alexturkey): קוד, קולות כלולים, תיעוד
- תמיכת Metal ל-macOS (Apple Silicon) מאת [@cayir21](https://github.com/cayir21), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- תיקון סוף משפט (EOS) להקראת כמה משפטים ב-backend של CPU מאת [@grogureis](https://github.com/grogureis), [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- התקנת CUDA ניסיונית ל-Ubuntu/Linux ותמיכת Docker מאת [@mslmyilmaz5](https://github.com/mslmyilmaz5), [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

גם השם שלכם שייך לכאן: תוצאת בדיקה מכרטיס המסך שלכם, משפט לסט הבדיקה, קול שעיצבתם, דיווח באג ברור או בקשת משיכה (pull request),
כל אלה נחשבים תרומה. תודה לכל מי שמנסה וכותב לנו.

## רישיון וקרדיטים

קוד וקולות כלולים: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. מבוסס על VoxCPM2 (OpenBMB, Apache-2.0), על audio.cpp
(ShugoAI LLC, Apache-2.0) ועל המרת ה-GGUF של audio.cpp. הרשימה המלאה: [THIRD_PARTY.md](THIRD_PARTY.md).
אין קשר ל-OpenBMB, ל-ModelBest או לפרויקט audio.cpp.

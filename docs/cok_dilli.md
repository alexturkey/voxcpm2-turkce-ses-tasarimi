# Multilingual reading / Çok dilli okuma

Türkçesi aşağıda. / Turkish below.

## 8 tested languages

| Code | Language | Bundled voice | Text rules |
|---|---|---|---|
| `tr` | Turkish | `hazir/belgesel_hanim` and the other Turkish voices | pronunciation dictionary `ayarlar/okunus_sozlugu.tsv`; no quotes, no apostrophes, no digits |
| `en` | English | `hazir/anlatici_en` | apostrophes kept, digits rejected (write numbers as words) |
| `fr` | French | `hazir/anlatici_fr` | same |
| `de` | German | `hazir/anlatici_de` | same |
| `es` | Spanish | `hazir/anlatici_es` | same |
| `ru` | Russian | `hazir/anlatici_ru` | same |
| `zh` | Chinese (Mandarin) | `hazir/anlatici_zh` | same; full-width punctuation is fine |
| `ja` | Japanese | `hazir/anlatici_ja` | same |

"Tested" means: on our own machine (GTX 1050 Ti 4 GB, fully local) we designed a native narrator for each language and
read a full 24-sentence documentary script with it, and this repo's code read sentences in each language with the
bundled voices. Other languages that VoxCPM2 supports should work with `--dil <code>`; we have not tested them.

Language selection: `--dil` on the command line; if omitted, the `dil` field of the voice card; if that is missing,
`tr`. For any language other than `tr` the Turkish dictionary is skipped, so foreign words are not rewritten.

## Example: one command per language

Write one sentence per line in a UTF-8 text file, then:

```powershell
python -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin_tr.txt --cikti cikti/tr
python -m ses_tasarim.oku --ses hazir/anlatici_en --metin @text_en.txt --cikti cikti/en
python -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @texte_fr.txt --cikti cikti/fr
python -m ses_tasarim.oku --ses hazir/anlatici_de --metin @text_de.txt --cikti cikti/de
python -m ses_tasarim.oku --ses hazir/anlatici_es --metin @texto_es.txt --cikti cikti/es
python -m ses_tasarim.oku --ses hazir/anlatici_ru --metin @tekst_ru.txt --cikti cikti/ru
python -m ses_tasarim.oku --ses hazir/anlatici_zh --metin @wenben_zh.txt --cikti cikti/zh
python -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @tekisuto_ja.txt --cikti cikti/ja
```

Each bundled folder has `ornek_okuma_metni.txt`, the first three sentences of our Cappadocia script in that language;
it is a ready test file: `--metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt`.

Design a new voice in another language: the prompt stays English, the design text is in the target language.

```powershell
python -m ses_tasarim.tasarla --ad narrator_de --dil de --cesit 3 `
  --tarif "A deep-voiced German man in his fifties, native German speaker with a clear standard Hochdeutsch accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic clean studio recording, no background noise" `
  --metin "Es gibt Orte, die sich schon beim ersten Besuch anfühlen, als hätten sie seit Jahren auf dich gewartet. Kappadokien ist so ein Ort."
```

Then audition each variant with real text and pick one (see the skill `.claude/skills/ses-tasarimi/SKILL.md`).

## Same voice every time (measured)

With this repo's code and the bundled `referans.flac` + seed, we read sentences 4-5 of the Cappadocia script again in
each language and compared them with the same sentences of the original production reading: 13 of 14 sentences (7 languages × 2) were **sample-for-sample identical** to the production audio, after the
reference went through lossless FLAC. One Japanese sentence came out different (7.36 s instead of 6.72 s); our production
reader sets the engine's token budget per batch, this repo per line, which is our guess for the cause (not verified).
So: same reference + same seed + same transcript gives the same voice, and sentence-by-sentence reading keeps it.

## Solutions we found (Cappadocia video, 8 languages)

1. **A variant can sound fine alone and still break long reading.** Our first Spanish variant had extra sound at the
   end of its reference recording; reading the full script with it went wrong. Fix: choose variants by a
   reference-based reading of 3-5 real sentences, not by the design recording.
2. **Sentence-by-sentence speed gate.** A whole-text similarity score can look fine while one line is cut and another
   is stretched. `oku` now compares each line's characters per second to the median and prints lines below 0.55× or
   above 1.6× (`supheli_satirlar` in `ozet.json`). Listen to those lines and read them again.
3. **Do not run Turkish text rules on foreign text.** A Turkish pronunciation dictionary rewrites foreign words and
   rejects apostrophes (`l'Anatolie`). `--dil` switches it off for every language except `tr`.
4. **Fonts for subtitles.** Cyrillic and CJK need fonts with those glyphs; we used Forum (Cyrillic) and Noto Serif
   SC/JP (Chinese/Japanese).

---

## Türkçe

Denenen 8 dil: `tr en fr de es ru zh ja`. "Denendi" demek: kendi makinemizde (GTX 1050 Ti 4 GB, tamamen yerel) her dil
için yerli anlatıcı tasarlandı, 24 cümlelik belgesel metni okutuldu; bu repodaki kod da her dilde hazır seslerle cümle
okuttu. VoxCPM2'nin desteklediği başka diller `--dil <kod>` ile çalışmalı; onları denemedik.

Dil seçimi: komut satırında `--dil`; verilmezse sesin kartındaki `dil`; o da yoksa `tr`. `tr` dışındaki dillerde Türkçe
okunuş sözlüğü uygulanmaz, kesme işareti kalır, rakam reddedilir (sayıyı o dilde yazıyla yaz).

Kullanım: yukarıdaki komutlar her dil için aynıdır; satır = cümle. Hazır seslerin klasöründeki
`ornek_okuma_metni.txt` hazır deneme dosyasıdır. Yeni dilde ses tasarlarken istem İngilizce, tasarım metni hedef dilde
yazılır; sonra her çeşit gerçek metinle referanslı okutulup dinlenir, biri seçilir.

Her seferinde aynı ses (ölçtük): bu repodaki kodla, hazır `referans.flac` + tohumla Kapadokya metninin 4-5. cümlelerini
her dilde yeniden okuttuk ve üretimdeki okumanın aynı cümleleriyle karşılaştırdık: 14 cümlenin 13'ü (7 dil × 2) kayıpsız FLAC'tan geçen referansla bile üretimdekiyle **örnek örnek aynı** çıktı. Bir
Japonca cümle farklı çıktı (6,72 yerine 7,36 sn); tahminimiz üretimdeki okuyucunun motor token bütçesini toplu, bu
reponun satır başına vermesi (doğrulanmadı). Yani aynı referans + aynı tohum + aynı metin aynı sesi verir.

Bulduğumuz çözümler:
1. Tek başına iyi duyulan çeşit uzun okumada bozulabilir (İspanyolca: referansın sonunda fazladan ses). Çare: çeşidi
   gerçek metinden 3-5 cümlelik referanslı okumayla seç.
2. Cümle cümle hız kapısı: her satırın harf/sn değeri ortancayla karşılaştırılır; 0,55 katının altı ya da 1,6 katının
   üstü yazdırılır, o satırlar dinlenip yeniden okutulur.
3. Türkçe metin kuralları yabancı metne uygulanmaz (`--dil`).
4. Altyazıda Kiril ve Çince/Japonca için uygun yazı tipi: Forum, Noto Serif SC/JP.

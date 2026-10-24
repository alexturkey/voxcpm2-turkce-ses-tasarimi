---
name: ses-tasarimi
description: "Design a new synthetic voice with VoxCPM2 in this repo and read long text with it consistently, in any of the 8 tested languages (tr, en, fr, de, es, ru, zh, ja): the user describes the voice, the skill writes the English voice prompt and the design text, designs several variants (one seed each), lets the user listen to each variant reading real text with its own reference and seed, fixes the chosen one, then reads long text sentence by sentence. Use when the user says 'design a voice', 'new voice', 'narrator voice', 'ses tasarla', 'yeni ses', 'şöyle bir ses istiyorum', 'read this text', 'seslendir', or asks for a voice in another language."
---

# Ses tasarımı / Voice design (VoxCPM2, 8 languages)

Türkçe özet aşağıda. / Turkish summary below.

This skill drives the repo's own code: `ses_tasarim/tasarla.py` (design), `ses_tasarim/oku.py` (reference-based
reading), `ses_tasarim/okunus.py` (text preparation per language). Install first (`AGENTS.md`); every command below
needs a working `ayarlar.json`. Quality is fixed: 16 steps, cfg 2.0 (`motor.FIXED`); never lower it, never suggest
another model. Run one GPU job at a time. Voices are synthetic: do not imitate a real, identifiable person (`ETHICS.md`).

## Why this flow

The voice is carried by a **reference recording**, not by the description. A design run turns the description into a
short recording; every later reading gives the engine that recording (as `audio` and `voice_ref`), its exact transcript
(`reference_text`) and the variant's own seed. Same reference + same seed + same transcript = the same timbre and
style every time. VoxCPM2 is not stable for one long generation (roughly above 30 seconds): rhythm speeds up and the
voice can drift. So long text is always read **one sentence per line**; each line is a short generation with the same
reference and seed, and the voice stays consistent from the first line to the last.

## Steps

1. **Ask and write the form.** The user describes the voice in their own words (who, age, gender, tone, pace, use).
   Write:
   - `tarif`: the voice prompt, **always in English**, short, no parentheses (the engine treats `(` as the prompt
     boundary). Main axes: gender, age, nationality/native accent, tone, emotion, pace, recording quality. Example used
     for our French narrator: `A deep-voiced French man in his fifties, native French speaker from Paris with a natural
     Parisian accent, calm, warm and soulful documentary storytelling, unhurried pace, rich resonant voice, close-mic
     clean studio recording, no background noise`. For a non-Turkish voice name the native speaker and city/accent.
   - `metin`: the design text, **in the voice's own language**, one or two natural sentences in the voice's role,
     no digits (write numbers as words). Turkish: no quotes or apostrophes. Aim for 8-30 seconds of speech; the result
     becomes the reference recording.
   - `dil`: language code (`tr en fr de es ru zh ja`).
   - Ask how many variants (default 3; each variant = its own random seed).
   Show the prompt and text to the user before running.
2. **Design the variants** (one seed each):
   ```
   python -m ses_tasarim.tasarla --ad <name> --dil <code> --tarif @tarif.txt --metin @metin.txt --cesit 3
   ```
   Output: `sesler/<name>/cesit_NN/{referans.wav, ses.json}`; the card stores prompt, transcript, seed and `dil`.
3. **Reference-based audition.** Do not choose by the design recordings alone. For every variant read 3-5 sentences
   of the user's **real text**, exactly as production will, with that variant's own reference and seed:
   ```
   python -m ses_tasarim.oku --ses <name>/1 --metin @deneme.txt --cikti cikti/deneme_1
   python -m ses_tasarim.oku --ses <name>/2 --metin @deneme.txt --cikti cikti/deneme_2
   ```
   Give the user the `okuma.wav` files, numbered by variant. Lesson from our Spanish narrator: a variant whose
   reference had extra sound at its end read long text badly, though its design recording sounded fine; only the
   reference-based audition showed it.
4. **The user picks one.** That variant (reference + seed + prompt + transcript in its `ses.json`) is now fixed. Do not
   redesign it, do not change its seed; reading always uses `okuma_tohumu` from the card. To keep it, leave the folder
   as is or copy it next to `hazir_sesler/` voices.
5. **Read long text sentence by sentence.** One sentence per line; `|| paragraf` at the end of a line = longer pause.
   ```
   python -m ses_tasarim.oku --ses <name>/<variant> --metin @metin.txt --cikti cikti/okuma
   ```
   `--dil` is taken from the voice card; give it only to override. If the run prints `hız kapısı / speed gate: satır
   [...]`, listen to those lines: their characters-per-second is far from the median (cut, stretched or padded).
   Shorten or reword the line and read again.

## Per-language notes

- Turkish (`tr`): the pronunciation dictionary `ayarlar/okunus_sozlugu.tsv` and Turkish quote/apostrophe rules apply.
- Other languages: the Turkish dictionary is **not** applied (it would damage foreign words); apostrophes stay
  (`l'eau`, `don't`); double quotes are removed; digits are rejected (write numbers as words in that language).
- Chinese and Japanese: one sentence per line works the same; full-width punctuation is fine.
- Video subtitles in Cyrillic or CJK need a font that has those glyphs (we used Forum for Cyrillic, Noto Serif SC/JP
  for Chinese/Japanese).
- Ready-made voices to start from: `hazir_sesler/anlatici_<code>` (en fr de es ru zh ja) and the Turkish voices.

## Do not

- Do not read a long text as one block. Do not lower steps/cfg. Do not give a reading seed other than the card's.
- Do not clone a real person's voice through this skill; cloning is the separate, consent-gated `klonla` section.

---

## Türkçe

Bu beceri repodaki kodu kullanır: `ses_tasarim/tasarla.py` (tasarım), `ses_tasarim/oku.py` (referanslı okuma),
`ses_tasarim/okunus.py` (dile göre metin hazırlığı). Kalite sabit: 16 adım, cfg 2.0; düşürülmez, başka model önerilmez.

Neden böyle: sesi tarif değil **referans kayıt** taşır. Tasarım, tarifi kısa bir kayda çevirir; sonraki her okumada
motora bu kayıt, birebir metni ve çeşidin kendi tohumu verilir; aynı referans + aynı tohum = her seferinde aynı tını ve
tarz. VoxCPM2 tek seferde uzun üretimde (yaklaşık 30 saniye üstü) kararlı değildir; bu yüzden uzun metin **cümle cümle**
okunur ve ses ilk satırdan son satıra kadar tutarlı kalır.

1. **Tarif al, formu yaz.** Kullanıcı sesi kendi sözleriyle anlatır. Beceri yazar: İngilizce ses yaratıcı istem
   (`--tarif`, parantezsiz, kısa; yabancı dilde yerli konuşan ve şehir/aksan yazılır), sesin kendi dilinde tasarım
   metni (`--metin`, rakamsız, 8-30 sn), dil kodu (`--dil`). Çeşit sayısını sorar (varsayılan 3).
2. **Çeşitleri tasarla:** her çeşit kendi tohumuyla (`python -m ses_tasarim.tasarla ... --dil <kod> --cesit 3`).
3. **Referanslı dinletme:** her çeşide gerçek metinden 3-5 cümle, üretimdeki gibi kendi referansı ve tohumuyla okutulur
   (`python -m ses_tasarim.oku --ses <ad>/<çeşit> ...`), numaralı olarak dinletilir. Ders (İspanyolca anlatıcı):
   referans kaydının sonunda fazladan ses olan çeşit uzun okumada bozuldu; bunu yalnız referanslı dinletme gösterdi.
4. **Kullanıcı birini seçer.** O çeşit (referans + tohum + istem + metin) sabittir; yeniden tasarlanmaz, tohumu
   değişmez.
5. **Uzun metin cümle cümle:** satır = cümle; `|| paragraf` uzun durak. Çıktıda "hız kapısı" satırı çıkarsa o
   satırları dinle, kısalt ya da yeniden yaz.

Dil notları: Türkçede okunuş sözlüğü uygulanır; başka dillerde uygulanmaz, kesme işareti kalır, rakam yazıyla
yazılır. Hazır başlangıç sesleri: `hazir_sesler/anlatici_<kod>` ve Türkçe sesler.

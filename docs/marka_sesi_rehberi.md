# Marka sesi tasarlama rehberi / Designing a fixed brand voice

Özet tartışması: [Discussions #4](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions/4). Komutlar: README "Kullanım".

**TR**

1. **Tarifi İngilizce yaz.** Kalıp: `<yaş/cinsiyet>, <ton>, <tempo>, <ortam/kayıt kalitesi>`.
   Örnek: `middle-aged woman, warm and confident, medium pace, quiet studio`. Parantez ve tırnak kullanma.
2. **Dört eksen:** yaş, ton (sıcak, resmî, enerjik, sakin), tempo (yavaş, orta, hızlı), ortam (stüdyo, açık hava, telefon).
3. **Beş örnek tarif:**
   - `young man, friendly and energetic, fast pace, clean studio` (genç tanıtım sesi)
   - `middle-aged woman, calm and reassuring, slow pace, quiet room` (müşteri hizmetleri)
   - `elderly man, warm and gravelly, slow pace, cozy room` (masalcı)
   - `female narrator, neutral and clear, medium pace, studio` (anlatıcı)
   - `teenage girl, cheerful, quick, outdoors` (genç karakter)
4. **Çeşit ve tohum:** aynı tarifle birkaç çeşit üret, dinle, en uygun olanı seç. Aynı tohum aynı sesi verir;
   seçtiğin tohum okumada sabit kalır (`ses.json` içinde saklanır).
   ```powershell
   .venv\Scripts\python.exe -m ses_tasarim.tasarla --ad marka --tarif "middle-aged woman, warm and confident, medium pace, quiet studio" --metin @yaratim_metni.txt --cesit 4
   .venv\Scripts\python.exe -m ses_tasarim.oku --ses marka/2 --metin @metin.txt --cikti cikti\marka
   ```
   Yaratılırken okunan metin 25-35 saniyelik, rakamsız, tırnaksız Türkçe bir paragraf olsun; sesin karakterini
   taşısın (sakin bir ses için sakin bir metin).
5. **Kaydet:** tarifi, tohumu ve onay notunu birlikte sakla (`sesler/<ad>/cesit_N/ses.json` zaten tutar);
   marka sesin yeniden üretilebilir olsun. Paylaşmak istersen: [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8).
6. **Etik sınır:** gerçek bir kişinin sesini kopyalamıyoruz; ses yükleme yok. Var olan bir kişiye benzetme tarifi
   yazma; karakter ve his tarif et (`ETHICS.md`).

Not: 4 GB GTX 1050 Ti üzerinde bir çeşit yaklaşık 55 saniye, okumada 1 saniye ses yaklaşık 2 saniye sürer (README "Sık sorulanlar").

**EN**

1. **Write the prompt in English:** `<age/gender>, <tone>, <pace>, <setting>`, e.g.
   `middle-aged woman, warm and confident, medium pace, quiet studio`. No brackets or quotes.
2. **Four axes:** age, tone (warm, formal, energetic, calm), pace (slow, medium, fast), setting (studio, outdoors, phone).
3. **Five examples:** see the list above (young energetic promo, calm customer service, elderly storyteller,
   neutral narrator, cheerful teen).
4. **Variants and seeds:** generate several variants for the same prompt, listen, pick the best. The same seed gives
   the same voice; the chosen seed stays fixed for reading (stored in `ses.json`). Commands as above
   (`ses_tasarim.tasarla --cesit 4`, then `ses_tasarim.oku --ses <name>/<variant>`). The creation text is a
   25-35 s Turkish paragraph without digits or quotes, in the character of the voice.
5. **Save** prompt, seed and approval note together (`sesler/<name>/cesit_N/ses.json` already holds them) so the brand
   voice is reproducible. To share one: [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8).
6. **Ethics:** we do not clone real people's voices; no audio upload. Describe a character and a feel, not a real
   person (`ETHICS.md`).

Note: on a 4 GB GTX 1050 Ti one variant takes about 55 s and reading about 2 s of compute per 1 s of speech (README FAQ).

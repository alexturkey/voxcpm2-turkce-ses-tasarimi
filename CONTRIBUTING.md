# Katkı / Contributing

**TR**

Hoş geldin. Bu depo bir kişinin 4 GB ekran kartında yürüttüğü bir deneyle başladı; her katkı onu biraz daha
sağlam yapar. Nereden başlayacağını bilmiyorsan bu dört küçük iş iyi bir ilk adım:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Kendi kartında dene; kartı, sürücüyü ve süreleri yaz
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: deneysel Vulkan sürümünü dene
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Test setine bir cümle ekle (`docs/test_seti/cumleler.txt`)
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Tasarladığın bir sesi tarifi ve tohumuyla paylaş (`docs/marka_sesi_rehberi.md`)

**Kartını test et, rapor yaz.** Kod bilmen gerekmez: kur, bir ses tasarla, bir metin okut, süreleri ve takıldığın yeri
[donanım test raporu formuna](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml) yaz. Çalışmadıysa da yaz; hata da bulgudur. Sonuç adınla
[test edilmiş donanım listesine](docs/donanim_testleri.md) girer. Özellikle Intel (Arc ya da dahili) ve farklı AMD
kartlarından rapor arıyoruz.

**Kod göndermek.** Depoyu çatalla (fork), kısa bir dal aç, tek konuya odaklı küçük bir PR gönder. PR şablonundaki
soruları doldur: ne değişti, nasıl test edildi (komut, kart, Windows sürümü), ikili dosya / ağ çağrısı / CI değişikliği
var mı. Çalıştığını göstermenin en kısa yolu: `.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2
--metin @metin.txt --cikti cikti\deneme` komutunun çıktısı. Kurallar: ikili dosya (exe, dll, zip, wav) PR'a girmez,
motor paketini bakımcı Releases'e koyar; repoya hiçbir kişinin ses kaydı (kendi sesiniz dahil) ya da klonlanmış ses
girmez, hazır sesler yalnız tariften tasarlanır (`ETHICS.md`); kalite ayarları (16 adım, cfg 2.0) hız için düşürülmez.

**İlk PR'ınız 5 adımda.** (1) Repoyu **fork'layın**, fork'unuzu klonlayın. (2) **Dal açın, tek şeyi değiştirin**: `git switch -c fix/kisa-ad`. (3) **Kontrolleri çalıştırın** (birkaç saniye, GPU ve ağ gerekmez, Python 3 yeter): `python -I -X utf8 scripts/denetim.py --hizli` ya da `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\on_kontrol.ps1` (GEÇTİ ya da KIRMIZI yazar; tam birim testi için `--tam`). (4) Fork'unuza **commit ve push**; GitHub no-reply e-postanızı kullanın (aşağıda). (5) **PR açın**, kısa şablonu doldurun. Hazır mı emin değilseniz **taslak (draft)** açın; neyi düzelteceğinizi söyleriz. Hedefimiz ilk yanıtı 7 gün içinde vermek: küçük bir gönüllü projenin hedefi, taahhüdü değil.

**Neyi alırız, neyi geri çeviririz.** Alırız: başka kartta test raporu (günlükle), belge/yazım/çeviri düzeltmesi, sorunu ve çözümü gösteren betik düzeltmesi, varsayılan davranışı değiştirmeyen ya da deneysel ve varsayılan kapalı işaretli değişiklik, ölçümlü ve aynı çıktıyı veren hız ya da bellek kazancı. Gerekçesini nazikçe söyleyerek geri çeviririz: hız için sabit kalite ayarlarını (16 adım, cfg 2.0) düşürmek, model ağırlığı ya da büyük ikili dosya, kimsenin çalıştırmadığı iddia ("çalışmalı"), kişisel yol/ad/e-posta/token, görünmez ya da çift yönlü Unicode, gizlenmiş kod, `PRIVACY.md`'de olmayan adresten indirme, telemetri. Ret kurala dairdir, size değil.

**Kanıt etiketleri (PR'da ve belgelerde kullanın).** **[ölçtüm]** çalıştırdınız, günlük/sayı elinizde; **[okudum]** dosya ya da belgede okudunuz (yolunu yazın); **[hesap]** ölçülen sayılardan türetildi; **[kullanıcı bildirdi]** başkası bildirdi, tekrarlanmadı; **[tahmin]** denenmedi. Çalıştırmadığınız şey için "çalışır" yazmayın; etiketli tahmin makbuldür.

**Tek dil yeter.** PR'ınızı Türkçe ya da İngilizce yazın (elinizdeki dil neyse o da olur). İkisini birden yazmanız gerekmez: değişiklik bir bölüme dokunuyorsa diğer dili bakımcı yazar. README içerik değişikliği için `README.md`'yi (İngilizce kaynak) düzenleyin; çeviriler bakımcılar tarafından birlikte güncellenir (`scripts/dil_eslik_denetimi.py` farkı gösterir). Lisans ve güvenlik metninde İngilizce esastır.

**Commit e-postanız.** Commit'teki e-posta geçmişte kalıcıdır. Gizli kalması için GitHub no-reply adresini kullanın: **GitHub > Settings > Emails > "Keep my email addresses private"**, sonra `git config user.email "<ID>+<kullanici>@users.noreply.github.com"` (ID aynı sayfada yazar). Başka adresli commit de kabul edilir; kontrollerimiz yalnız uyarır.

**Soru ve sonuç:** [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions). **Kurulum sorunu:** [sorun formu](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml).
**Güvenlik açığı:** herkese açık issue açma; `SECURITY.md`'deki özel bildirim yolunu kullan.

**EN**

Welcome. This repo started as one person's experiment on a 4 GB GPU; every contribution makes it a bit sturdier.
Not sure where to start? These four small issues are a good first step:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Try it on your GPU and report the card, driver and timings
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: try the experimental Vulkan build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Add a sentence to the test set (`docs/test_seti/cumleler.txt`)
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Share a voice you designed, with its description and seed (`docs/marka_sesi_rehberi.md`)

**Test your GPU, write a report.** No coding needed: install, design a voice, read a text, then post the timings and
anything that got in your way with the [hardware test report form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml). Write even if it failed; an error is a
finding too. Your result goes into the [tested hardware list](docs/donanim_testleri.md) with your name. Reports from
Intel (Arc or integrated) and other AMD cards are especially welcome.

**Sending code.** Fork the repo, open a short branch, send a small PR focused on one thing. Fill in the PR template:
what changed, how it was tested (command, GPU, Windows version), whether there are binary files, network calls or CI
changes. The shortest proof that it works is the output of `.venv\Scripts\python.exe -m ses_tasarim.oku --ses
deniz_feneri/2 --metin @metin.txt --cikti cikti\deneme`. Rules: no binaries in PRs (exe, dll, zip, wav; the maintainer
publishes engine packages on Releases); no voice recording of any person (your own included) and no cloned voice in the
repo, bundled voices are text-designed only (`ETHICS.md`); quality settings
(16 steps, cfg 2.0) are not lowered for speed.

**Your first pull request in 5 steps.** (1) **Fork** the repo and clone your fork. (2) **Branch and change one thing**: `git switch -c fix/short-name`. (3) **Run the checks** (a few seconds, no GPU or network, Python 3 is enough): `python -I -X utf8 scripts/denetim.py --hizli` or `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\on_kontrol.ps1` (prints PASSED or RED; add `--tam` for the full unit tests). (4) **Commit and push** to your fork; use your GitHub no-reply e-mail (below). (5) **Open the pull request** and fill in the short template. Not sure it is ready? Open it as a **draft**; we will say what to fix. Our goal is a first reply within 7 days: a goal of a small volunteer project, not a promise.

**What we accept and what we decline.** Accepted: a test report from another GPU (with the log), docs, typo and translation fixes, a script fix that shows the problem and the fix, a change that keeps the default behaviour identical or is marked experimental and off by default, a speed or memory saving with a measurement and the same output. Declined, with a kind reason: lowering the fixed quality settings (16 steps, cfg 2.0) to go faster, model weights or large binaries, claims nobody ran ("should work"), personal paths, names, e-mails or tokens, invisible or bidirectional Unicode, obfuscated code, downloads from hosts not listed in `PRIVACY.md`, telemetry. A decline is about the rule, never about you.

**Evidence labels (use them in the pull request and in docs).** **[measured]** you ran it and kept the log or numbers; **[read]** you read it in a file or document (give the path); **[computed]** derived from measured numbers; **[user-reported]** someone else reported it, not reproduced; **[guess]** not checked. Do not write "works" about something you did not run; a labelled guess is welcome.

**One language is enough.** Write your pull request in English or Turkish (any language is fine if that is what you have). You do not have to write both: if your change touches a section, a maintainer writes the other language. For README content changes edit `README.md` (the English source); translations are updated together by the maintainers (`scripts/dil_eslik_denetimi.py` shows the difference). For the license and security text, English is authoritative.

**Your commit e-mail.** Commits keep their e-mail in history for good. To keep your address private use the GitHub no-reply address: **GitHub > Settings > Emails > "Keep my email addresses private"**, then `git config user.email "<ID>+<username>@users.noreply.github.com"` (the ID is shown on that page). Commits with another address are accepted; our checks only warn.

**Questions and results:** [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions). **Install problems:** [issue form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml).
**Security vulnerabilities:** do not open a public issue; use the private route in `SECURITY.md`.

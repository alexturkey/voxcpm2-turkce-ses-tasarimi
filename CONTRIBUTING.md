# Katkı / Contributing

**TR**

Hoş geldin. Bu depo bir kişinin 4 GB ekran kartında yürüttüğü bir deneyle başladı; her katkı onu biraz daha
sağlam yapar. Nereden başlayacağını bilmiyorsan bu dört küçük iş iyi bir ilk adım:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Kendi kartında dene; kartı, sürücüyü ve süreleri yaz
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: deneysel Vulkan sürümünü dene
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Test setine bir cümle ekle (`docs/test_seti/cumleler.txt`)
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Tasarladığın bir sesi tarifi ve tohumuyla paylaş (`docs/marka_sesi_rehberi.md`)

**Kod göndermek.** Depoyu çatalla (fork), kısa bir dal aç, tek konuya odaklı küçük bir PR gönder. PR şablonundaki
soruları doldur: ne değişti, nasıl test edildi (komut, kart, Windows sürümü), ikili dosya / ağ çağrısı / CI değişikliği
var mı. Çalıştığını göstermenin en kısa yolu: `.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2
--metin @metin.txt --cikti cikti\deneme` komutunun çıktısı. Kurallar: ikili dosya (exe, dll, zip, wav) PR'a girmez,
motor paketini bakımcı Releases'e koyar; gerçek bir kişinin sesi ya da kaydı hiçbir biçimde kabul edilmez
(`ETHICS.md`); kalite ayarları (16 adım, cfg 2.0) hız için düşürülmez.

**Soru ve sonuç:** [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions). **Kurulum sorunu:** [sorun formu](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml).
**Güvenlik açığı:** herkese açık issue açma; `SECURITY.md`'deki özel bildirim yolunu kullan.

**EN**

Welcome. This repo started as one person's experiment on a 4 GB GPU; every contribution makes it a bit sturdier.
Not sure where to start? These four small issues are a good first step:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Try it on your GPU and report the card, driver and timings
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: try the experimental Vulkan build
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Add a sentence to the test set (`docs/test_seti/cumleler.txt`)
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Share a voice you designed, with its description and seed (`docs/marka_sesi_rehberi.md`)

**Sending code.** Fork the repo, open a short branch, send a small PR focused on one thing. Fill in the PR template:
what changed, how it was tested (command, GPU, Windows version), whether there are binary files, network calls or CI
changes. The shortest proof that it works is the output of `.venv\Scripts\python.exe -m ses_tasarim.oku --ses
deniz_feneri/2 --metin @metin.txt --cikti cikti\deneme`. Rules: no binaries in PRs (exe, dll, zip, wav; the maintainer
publishes engine packages on Releases); no real person's voice or recording in any form (`ETHICS.md`); quality settings
(16 steps, cfg 2.0) are not lowered for speed.

**Questions and results:** [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions). **Install problems:** [issue form](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml).
**Security vulnerabilities:** do not open a public issue; use the private route in `SECURITY.md`.

# Güvenlik / Security

**TR**

Bir güvenlik açığı bulduysanız lütfen herkese açık bir issue açmayın. GitHub'ın özel bildirim yolunu kullanın:
repo sayfasında **Security → Report a vulnerability** (ya da doğrudan
https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/security/advisories/new). Bildirim yalnız bakımcıya gider.

Yazarken: hangi sürüm (`git log -1` ya da Release etiketi), nasıl tetiklendiği, etkisi. Bildirimlere en kısa sürede bakmaya çalışırız.
Düzeltme yayınlanana kadar ayrıntıyı paylaşmamanızı rica ederiz; düzeltme notunda isminizle (isterseniz) teşekkür edilir.

Kapsam: bu depodaki Python kodu, `scripts/` altındaki kurulum ve derleme betikleri, `patches/` yaması ve Releases'taki
hazır motor zip'i. Kapsam dışı: VoxCPM2 modeli, audio.cpp'nin kendisi, NVIDIA CUDA paketleri (kendi projelerine bildirin).

Bilinen tasarım sınırları (açık değil, bilerek böyle):
- Arayüz yalnız `127.0.0.1`'e bağlanır; ağa açmak için tasarlanmamıştır, tersine çevirmeyin (reverse proxy ile dışa açmayın).
- `kur.ps1` indirdiği her dosyayı sabit sha256 ile doğrular; bir sha tutmazsa durur. `-ExecutionPolicy Bypass` yalnız o
  PowerShell sürecine etki eder, sistem ayarı değişmez; betiği çalıştırmadan önce okuyabilirsiniz.

**EN**

If you find a security vulnerability, please do not open a public issue. Use GitHub's private reporting:
**Security → Report a vulnerability** on the repository page (or
https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/security/advisories/new). Reports reach only the maintainer.

Please include the version (`git log -1` or the Release tag), how to trigger it and the impact. We try to look at reports
as soon as we can. Please hold details until a fix is published; the fix notes will credit you if you wish.

Scope: the Python code in this repository, the install/build scripts under `scripts/`, the patch in `patches/` and the
prebuilt engine zip on Releases. Out of scope: the VoxCPM2 model, audio.cpp itself and NVIDIA CUDA packages (report upstream).

Known design limits (intentional, not vulnerabilities):
- The web UI binds to `127.0.0.1` only; it is not designed to be exposed to a network (do not reverse-proxy it).
- `kur.ps1` verifies every download against a pinned sha256 and stops on mismatch. `-ExecutionPolicy Bypass` affects only
  that PowerShell process, not the system policy; read the script before running it.

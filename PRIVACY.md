# Gizlilik / Privacy

## Türkçe

**Kısaca: voxcpm2-turkce-ses-tasarimi'nda telemetri yok. Betikler ağı yalnız aşağıdaki indirmeler için, yalnız aşağıdaki adreslerden kullanır; web arayüzü yalnız bu bilgisayarda (127.0.0.1) dinler.** Sizin, makinenizin, metinlerinizin ya da seslerinizin hiçbir bilgisi yüklenmez. Ses tasarımı ve okuma tamamen yereldir.

### Betiklerin indirdikleri
| Adres | Ne | Hangi betik, ne zaman |
|---|---|---|
| `github.com` (`release-assets.githubusercontent.com`'a yönlenir) | sürümün motor zip'i; derlemede audio.cpp v0.7.2 kaynak arşivi | `scripts/kur.ps1`, `kur.sh`, `kur-linux.sh`, `macos/scripts/motoru_derle.sh`; yalnız motor/kaynak adımında |
| `huggingface.co` ve `hf.co` alt adresleri | VoxCPM2 model dosyası (`voxcpm2-q8_0.gguf`, commit'e sabit adres) | `scripts/kur.ps1`, `kur.sh`, `kur-linux.sh`; yalnız model adımında |
| `developer.download.nvidia.com` | CUDA 12.8 çalışma zamanı zip'leri (kurulumsuz) | `scripts/kur.ps1`; yalnız cuda adımında |
| `pypi.org`, `files.pythonhosted.org` | `requirements.txt` paketleri (`numpy`, `soundfile`) | `pip install`, kurulumun python adımında |
| Docker temel imajı ve `apt-get` depoları; macOS'ta `brew` | yalnız `Dockerfile.linux` ve macOS derleme yolu; paket kaynağını bu araçlar kendisi seçer | yalnız o yolu seçerseniz |

Sabitlenmiş sha256 olan her indirme ona karşı denetlenir, uyuşmazsa durur. Her indirmede olduğu gibi karşı taraf IP adresinizi ve olağan istek başlıklarını görür. Başka hiçbir şey göndermeyiz: hesap, kullanıcı adı, sistem bilgisi, kullanım verisi yok.

### Yapmadıkları
Telemetri/analitik yok, çökme raporu yok, güncelleme denetimi yok, hesap ya da çerez yok. Web arayüzü yalnız `127.0.0.1`'e bağlanır, `Host` başlığını denetler, ağa açılmak için tasarlanmamıştır. Metinleriniz, tasarladığınız sesler ve okumalar hiçbir yere yüklenmez.

### Bilgisayarınızda kalanlar
Kurulum kökünde (`C:\vox` gibi) model, motor, CUDA DLL'leri ve indirme artıkları; repo klasöründe `ayarlar.json`, `sesler/` (tasarladığınız sesler, okuma listesi, taslaklar) ve `onbellek/`. Günlüklerde klasör yolunuz olabilir: issue'ya günlük koymadan önce silin (`scripts/tani.ps1` kişisel adları kendisi gizler).

### Betiklerimizin dışında
- Burada paylaştığınız (issue, PR, yıldız) GitHub tarafından GitHub Gizlilik Bildirimi'ne göre işlenir ve herkese açıktır.
- Model ve audio.cpp kendi lisans ve gizlilik koşullarındadır (`THIRD_PARTY.md`); kötüye kullanım sınırları `ETHICS.md`'de.

### Kendiniz denetleyin (birkaç saniye, hiçbir şey indirilmez)
Koddaki bütün ağ çağrıları: `Select-String -Path scripts/*.ps1,scripts/*.sh,scripts/*.py,ses_tasarim/*.py,macos/scripts/*.sh -Pattern 'https?://|curl|Invoke-WebRequest|urllib|socket'`. Bugün beklenen: yukarıdaki adresler, `127.0.0.1` ve belge bağlantıları. Listede olmayan bir çağrı bulursanız `SECURITY.md`'deki gibi bildirin. Bir sürüm yeni adres eklerse bu dosya aynı değişiklikte güncellenir.

## English (authoritative)

**Short version: voxcpm2-turkce-ses-tasarimi has no telemetry. Its scripts use the network only for the downloads listed below, and only from the hosts listed below; the web UI listens only on this computer (127.0.0.1).** Nothing about you, your machine, your texts or your voices is uploaded. Voice design and reading run fully locally.

### What the scripts fetch
| Host | What | Which script, when |
|---|---|---|
| `github.com` (redirects to `release-assets.githubusercontent.com`) | the release engine zip; for builds, the audio.cpp v0.7.2 source archive | `scripts/kur.ps1`, `kur.sh`, `kur-linux.sh`, `macos/scripts/motoru_derle.sh`; only in the engine/source step |
| `huggingface.co` and `hf.co` sub-hosts | the VoxCPM2 model file (`voxcpm2-q8_0.gguf`, commit-pinned URL) | `scripts/kur.ps1`, `kur.sh`, `kur-linux.sh`; only in the model step |
| `developer.download.nvidia.com` | CUDA 12.8 runtime zips (no installer) | `scripts/kur.ps1`; only in the cuda step |
| `pypi.org`, `files.pythonhosted.org` | the `requirements.txt` packages (`numpy`, `soundfile`) | `pip install`, in the python step of the install |
| the Docker base image and `apt-get` repositories; `brew` on macOS | only `Dockerfile.linux` and the macOS build path; those tools pick their own package sources | only if you choose that path |

Every download is checked against a pinned sha256 where one exists and stops on a mismatch. Like any download, the host sees your IP address and the ordinary request headers. We send nothing else: no account, no usernames, no system information, no usage data.

### What it does not do
No telemetry or analytics, no crash reports, no update check, no accounts or cookies. The web UI binds to `127.0.0.1` only, checks the `Host` header, and is not designed to be exposed to a network. Your texts, designed voices and readings are not uploaded anywhere.

### What stays on your computer
In the install root (for example `C:\vox`): the model, the engine, the CUDA DLLs and download leftovers; in the repo folder: `ayarlar.json`, `sesler/` (your designed voices, reading list, drafts) and `onbellek/`. Logs can contain your folder path: remove it before you post a log in an issue (`scripts/tani.ps1` hides personal names itself).

### Outside our scripts
- GitHub processes what you post here (issues, pull requests, stars) under the GitHub Privacy Statement; it is public.
- The model and audio.cpp are under their own license and privacy terms (`THIRD_PARTY.md`); misuse limits are in `ETHICS.md`.

### Check it yourself (a few seconds, nothing is downloaded)
Every network call in the code: `Select-String -Path scripts/*.ps1,scripts/*.sh,scripts/*.py,ses_tasarim/*.py,macos/scripts/*.sh -Pattern 'https?://|curl|Invoke-WebRequest|urllib|socket'`. Expected today: the hosts above, `127.0.0.1` and documentation links. If you find a call that is not listed here, please report it as in `SECURITY.md`. When a release adds a host, this file is updated in the same change.

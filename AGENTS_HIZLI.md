# AGENTS_HIZLI.md: quick card for AI coding agents / Yapay zeka ajanları için hızlı kart

English first, Türkçe below. Full rules and evidence: [`AGENTS.md`](AGENTS.md) (it wins if the two ever differ). Error codes: `docs/hata_imzalari.json`, `docs/SIK_HATALAR.md`.

## English: decision tree (12 steps)
1. Goal: Turkish voice design and reading with VoxCPM2 on a 4 GB GPU (Windows 10/11 + NVIDIA ≥ 4 GB; experimental: AMD/Intel Vulkan, macOS Apple Silicon, Ubuntu). Anything else: tell the user and stop.
2. Quality is fixed (16 steps, cfg 2.0). Never lower it to save time or memory.
3. Dry run first, it writes and downloads nothing: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kuru`. Read every `HATA:` / `UYARI:` line.
4. A non-zero exit or any `HATA` in that list: take it to the user with the code and its first step from `docs/hata_imzalari.json` (find it with `scripts\tani.ps1 -Hata "<message>"`). Do not use a force flag to get past it.
5. The download is about 3.7 GB (model, CUDA DLLs, engine; `AGENTS.md` step 2) and takes about 10 minutes: tell the user the size and the sources (`PRIVACY.md`) and wait for a yes. Voice cloning is for the user's own voice or a voice with its owner's explicit permission: never confirm that permission for the user.
6. Install: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1` (safe to re-run; verified files are skipped; an interrupted download continues).
7. First success: the smoke test in `AGENTS.md` step 4 (a short design and reading; about 1-2 minutes on a GTX 1050 Ti [read: AGENTS.md step 4]). Long runs: start hidden in the background and poll; do not block. One GPU job at a time.
8. Exit 0 of `kur.ps1` means the install steps finished, nothing more: it does not prove a good voice; listen to the result.
9. Any failed or not-run check means the result is NOT accepted. Never report success.
10. A line with a code: look it up in `docs/hata_imzalari.json`, give the user its first step, quote the code. Same error twice: stop, do not try a third time.
11. Paths and files are only what the user gave you. Never pick someone's voice recording yourself; the repo contains no voice of a person.
12. Report in the user's language, with the code and the first 20 log lines. No personal paths, user names, e-mail addresses or tokens: write `<ROOT>`.

### Exit code -> action
| Script | Exit | Meaning | What you do | Codes |
|---|---|---|---|---|
| `kur.ps1` | 0 | steps finished (`KURULUM_OK`) | go to the first success step | - |
| `kur.ps1` | 1 | an error was thrown (message printed) | take the message to the user; look it up | `SES-E-PY-SURUM` `SES-E-SHA` `SES-E-GPU` ... |
| `kur.ps1 -Kuru` | 0 / 1 / 3 | ready / only a Python problem / disk or GPU not enough | on 3 take it to the user; do not install | `SES-E-GPU` |
| `denetim.py` | 0 / 1 / 3 / 6 | all gates passed / a gate is RED / no argument or no git / a gate did not run | fix RED; 3 and 6 are not green | - |
| `tani.ps1 -Hata` | 0 / 1 | code found / no known code | quote the code; on 1 run `tani.ps1` and give the report | any |

## Türkçe: karar ağacı (12 adım)
1. Amaç: VoxCPM2 ile 4 GB ekran kartında Türkçe ses tasarımı ve okuma (Windows 10/11 + NVIDIA ≥ 4 GB; deneysel: AMD/Intel Vulkan, macOS Apple Silicon, Ubuntu). Başka bir ortamsa kullanıcıya söyle ve dur.
2. Kalite sabit (16 adım, cfg 2.0). Zaman ya da bellek için asla düşürme.
3. Önce kuru çalıştır, hiçbir şey yazmaz ve indirmez: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kuru`. Her `HATA:` / `UYARI:` satırını oku.
4. Sıfır olmayan çıkış ya da listede herhangi bir `HATA`: kodu ve `docs/hata_imzalari.json`'daki ilk adımı kullanıcıya götür (`scripts\tani.ps1 -Hata "<ileti>"` bulur). Zorlayıcı bayrakla geçme.
5. İndirme yaklaşık 3,7 GB (model, CUDA DLL'leri, motor; `AGENTS.md` adım 2) ve yaklaşık 10 dakika sürer: boyutu ve kaynakları (`PRIVACY.md`) kullanıcıya söyle, evet'i bekle. Ses klonlama yalnız kullanıcının kendi sesi ya da sahibinin açık izni olan ses içindir: bu izni kullanıcı yerine asla onaylama.
6. Kurulum: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1` (tekrar çalıştırmak güvenli; doğrulanmış dosya atlanır; yarım indirme sürer).
7. İlk başarı: `AGENTS.md` adım 4'teki duman testi (kısa tasarım ve okuma; GTX 1050 Ti'de yaklaşık 1-2 dakika [okudum: AGENTS.md adım 4]). Uzun işleri gizli arka planda başlat, yoklayarak izle; bekleyerek kilitlenme. Aynı anda tek GPU işi.
8. `kur.ps1` çıkış 0 yalnız kurulum adımlarının bittiği demektir: iyi bir ses olduğunu kanıtlamaz; sonucu dinle.
9. Başarısız ya da çalışmayan her denetim: sonuç KABUL EDİLMEZ. Asla başarı bildirme.
10. Kodlu satır: `docs/hata_imzalari.json`'da ara, ilk adımı kullanıcıya ver, kodu yaz. Aynı hata iki kez: dur, üçüncü kez deneme.
11. Yol ve dosya yalnız kullanıcının sana verdiğidir. Birinin ses kaydını kendin seçme; repoda hiçbir kişinin sesi yoktur.
12. Kullanıcının dilinde, kodla ve log'un ilk 20 satırıyla bildir. Kişisel yol, kullanıcı adı, e-posta, token yazma: `<ROOT>` yaz.

### Çıkış kodu -> eylem
| Betik | Çıkış | Anlam | Ne yaparsın | Kodlar |
|---|---|---|---|---|
| `kur.ps1` | 0 | adımlar bitti (`KURULUM_OK`) | ilk başarı adımına geç | - |
| `kur.ps1` | 1 | hata fırlatıldı (ileti basıldı) | iletiyi kullanıcıya götür; ara | `SES-E-PY-SURUM` `SES-E-SHA` `SES-E-GPU` ... |
| `kur.ps1 -Kuru` | 0 / 1 / 3 | hazır / yalnız Python sorunu / disk ya da kart yetmiyor | 3'te kullanıcıya götür; kurma | `SES-E-GPU` |
| `denetim.py` | 0 / 1 / 3 / 6 | hepsi geçti / bir kapı KIRMIZI / argüman ya da git yok / bir kapı çalışmadı | KIRMIZI'yı düzelt; 3 ve 6 yeşil sayılmaz | - |
| `tani.ps1 -Hata` | 0 / 1 | kod bulundu / bilinen kod yok | kodu yaz; 1'de `tani.ps1` raporunu ver | hepsi |

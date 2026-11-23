# Sık hatalar / Common errors

**TR:** Kurulum ya da kullanım sırasında çıkan hata iletisinin bir parçasını `scripts\tani.ps1 -Hata "<ileti>"` ile arayın: kodu ve ilk adımı söyler (yerel, ağsız, hiçbir şey göndermez). Aşağıdaki tablo aynı bilgidir. Kodlar kalıcıdır; kaynağı "repo" olanlar bu depodaki betiğin bastığı iletilerdir, "motor" ve "işletim sistemi" olanlar dış kaynaktandır.

**EN:** Search part of the error message with `scripts\tani.ps1 -Hata "<message>"`: it prints the code and the first step (local, offline, sends nothing). The table below is the same data. Codes are permanent; rows with source "repo" are messages printed by this repository's scripts, "engine" and "OS" rows come from outside.

Hâlâ çözülmediyse / Still stuck: `scripts\tani.ps1` raporunu [kurulum sorunu formuna](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml) yapıştırın / paste its report into the install-problem form.

| Kod / Code | İletide ara / Look for | İlk adım (TR) | First step (EN) | Kaynak / Source |
|---|---|---|---|---|
| `SES-E-PY-SURUM` | `64-bit Python 3.10-3.13 bulunamadı` | Python 3.12 (64-bit) kurun: winget install Python.Python.3.12, YENİ bir PowerShell açın, kur.ps1'i yeniden çalıştırın. 3.14 ve üstü desteklenmez (numpy için hazır paket yok). | Install Python 3.12 (64-bit): winget install Python.Python.3.12, open a NEW PowerShell, run kur.ps1 again. 3.14+ is not supported (no numpy wheels). | repo |
| `SES-E-VENV-PY` | `var olan .venv desteklenmeyen` | Repo'nun .venv klasörü desteklenmeyen bir Python ile yapılmış. Betik silmez: iletideki klasörü silin, -Adim python,ayar,kontrol ile yeniden çalıştırın. | The repo's .venv was made with an unsupported Python. The script never deletes it: delete the folder named in the message and re-run with -Adim python,ayar,kontrol. | repo |
| `SES-E-KOK-ASCII` | `Kurulum klasörü Türkçe harf` | Motor ASCII dışı yolları açamaz. Kısa, İngilizce harfli klasör seçin: kur.ps1 -Kok C:/vox | The engine cannot open non-ASCII paths. Use a short English-letter folder: kur.ps1 -Kok C:/vox | repo |
| `SES-E-SHA` | `sha256 tutmadı` | İndirme yarım ya da değişmiş. kur.ps1'i yeniden çalıştırın (.part dosyası otomatik silinir). Tekrarlarsa issue açın. | The download is partial or changed. Run kur.ps1 again (the .part file is removed automatically). If it repeats, tell us in an issue. | repo |
| `SES-E-MOTOR-SHA` | `hazır motor sha256` | Eski kopya: git pull yapın, kur.ps1'i yeniden çalıştırın. | Old checkout: run git pull, then kur.ps1 again. | repo |
| `SES-E-INDIRME` | `indirme başarısız` | Ağ sorunu. Aynı komutu yeniden çalıştırın; .part dosyasından kaldığı yerden sürer. | Network problem. Run the same command again; it resumes from the .part file. | repo |
| `SES-E-GPU` | `motor ekran kartını görmedi` | Sürücü 570'ten eski, kart CUDA değil ya da Maxwell ve eski. Sürücüyü güncelleyin, nvidia-smi'ye bakın. AMD/Intel: kur.ps1 -Vulkan (deneysel). | Driver older than 570, not a CUDA card, or Maxwell/older. Update the driver, check nvidia-smi. AMD/Intel: kur.ps1 -Vulkan (experimental). | repo |
| `SES-E-MOTOR-YOK` | `motor yok:` | Motor adımı çalışmadı. kur.ps1'i çalıştırın ya da -Adim hazir kullanın. | The engine step has not run. Run kur.ps1 (default steps) or -Adim hazir. | repo |
| `SES-E-CUDA-DLL` | `CUDA DLL eksik` | kur.ps1 -Adim cuda çalıştırın. CUDA DLL'leri <kök>/cuda/bin içindedir, sistem PATH'ine eklenmez. | Run kur.ps1 -Adim cuda. The CUDA DLLs live in <root>/cuda/bin and are never added to the system PATH. | repo |
| `SES-E-YAMA` | `yama uygulanamıyor` | Kaynak saf v0.7.2 değil ya da yama CRLF olmuş. <kök>/motor/src klasörünü silip -Adim kaynak ile yeniden çalıştırın; yamalar LF kalmalı. | The source is not pristine v0.7.2 or a patch became CRLF. Delete <root>/motor/src, re-run -Adim kaynak; keep patches LF (git config core.autocrlf). | repo |
| `SES-E-YAMA-IMZA` | `yama imzası tutmuyor` | Kaynak eski yamalarla yamalanmış. <kök>/motor/src klasörünü silip yeniden çalıştırın. | The source was patched with older patches. Delete <root>/motor/src and run again. | repo |
| `SES-E-EOS` | `satırlar düzgün bitmedi` | Cümle çok uzun ya da noktalama garip. Bölün (satır başına bir cümle); sayıları yazıyla yazın. | The sentence is too long or has odd punctuation. Split it (one sentence per line); write numbers in words. | repo |
| `SES-E-ISARET` | `okunamayan işaret` | Metinde rakam ya da tırnak var. Sayıları yazıyla yazın (iki bin yirmi altı), tırnakları kaldırın. | Digits or quotes in the text. Write numbers in words (iki bin yirmi altı) and remove quotes. | repo |
| `SES-E-MEM-BUFFER` | `GGML_ASSERT mem_buffer` | İki GPU işi aynı anda ya da boş RAM 4,5 GB'ın altında. Tek iş çalıştırın, diğer GPU programlarını kapatın. | Two GPU jobs at once or under 4.5 GB free RAM. Run one job at a time and close other GPU programs. | motor / engine |
| `SES-E-KAPASITE` | `CapacityError` | Tek satır motorun bütçesini aşıyor. Satırı kısaltın (satır başına bir cümle). | A single line exceeds the engine's budget. Shorten the line (one sentence per line). | motor / engine |
| `SES-E-PORT` | `Address already in use` | 8765 portu dolu (arayüz zaten açık olabilir). Başka port kullanın: --port 8800. | Port 8765 is busy (the UI may already be open). Use another port: --port 8800. | işletim sistemi / OS |
| `SES-E-YOL-UZUN` | `Could not open output file` | Yol çok uzun ya da ASCII değil. Daha kısa bir -Kok kullanın (ör. C:/v). | Path too long or not ASCII. Use a shorter -Kok (e.g. C:/v). | motor / engine |

Tam hata tablosu ve ayrıntı / Full troubleshooting table: [AGENTS.md](../AGENTS.md) bölüm 6 / section 6.

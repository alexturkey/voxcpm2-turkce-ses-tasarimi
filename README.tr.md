# voxcpm2-turkce-ses-tasarimi

**4 GB ekran kartında VoxCPM2 ile Türkçe ses tasarımı.** Sesi İngilizce tarif edin, model yaratsın, beğendiğiniz çeşidi
seçin, sonra o sesle istediğiniz Türkçe metni okutun. Tek komutluk kurulum, GTX 1050 Ti'ye (4 GB) sığdırılmış yamalı
[audio.cpp](https://github.com/0xShug0/audio.cpp) motoru, küçük bir yerel web arayüzü ve yedi hazır yapay ses içerir.

[English README](README.md) · [4 GB'a nasıl sığdı](docs/4gb.md) · [Yapay zekâ ajanı için kurulum](AGENTS.md) · [Sorumlu kullanım](ETHICS.md)

> Buradaki her ses yapaydır: bir metin tarifinden tasarlanmıştır, hiçbir gerçek kişiden kaydedilmemiş ya da
> klonlanmamıştır. Ürettiğiniz sesi yapay zekâ ürünü olarak etiketleyin. Dışarıdan ses yükleme ve gerçek kişi klonlama yoktur.

## Nasıl çalışır

1. **Ses tasarımı.** İngilizce *ses tarifi* + ses yaratılırken okutulan Türkçe *metin* + çeşit sayısı. Her çeşidin kendi
   tohumu vardır; motora `(tarif)metin` gider, her tohum için 20-35 sn'lik bir tasarım kaydı döner.
2. **Referanslı okuma.** Tasarım kaydı motorun **iki** girişine birden verilir (`audio` ve `voice_ref`), yanında o
   kaydın metni (`reference_text`), okunacak yeni metin ve aynı tohum. Sesi tarif değil kayıt taşır; metinden metne
   kaymaz. Metin cümle cümle okunur.
3. Kalite sabittir: 16 adım, CFG 2.0. Tohum kalite ayarı değildir.

Motor: audio.cpp v0.7.2 + bizim yama (`patches/`); model: VoxCPM2 Q8_0 GGUF. VRAM tepe ≈ 2,8 GB; GTX 1050 Ti'de 1 sn ses
için ≈ 2 sn. Ayrıntı ve ölçümler: [docs/4gb.md](docs/4gb.md).

## Hazır sesler (`hazir_sesler/`)

Yedisi de `ses.json` içindeki tariflerden tasarlandı; hiçbiri gerçek bir kişi değil.

| Ses | Kısa tarif | Dinle |
|---|---|---|
| `belgesel_hanim` | Ellili yaşlarda, derin sıcak alto; sakin belgesel anlatıcısı | [örnek](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referans](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Tok, güçlü, gizemli erkek anlatıcı | [örnek](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referans](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Yetmişlerinde deneyimli haber spikeri, sakin ve otoriter | [örnek](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referans](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Otuzlarında karizmatik akşam haberleri sunucusu, kadifemsi ve vurgulu | [örnek](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referans](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Masal cadısı: pes, hafif genizli, sinsi tatlı | [örnek](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referans](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Çok derin, tok, buyurgan erkek anlatıcı | [örnek](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referans](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Yaşlı bilge, derin ve gür, hafif gizemli | [örnek](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referans](hazir_sesler/yasli_bilge/referans.flac) |

Her klasörde: `referans.flac` (kayıpsız tasarım kaydı), `ses.json` (tarif, metin, tasarım tohumu, okuma tohumu,
tanıtım), `ornek_okuma.mp3` (+ metni). Doğrudan kullanın: `--ses hazir/<ad>`.

## Kurulum (Windows 10/11, NVIDIA ekran kartı ≥ 4 GB)

Ön koşullar: NVIDIA sürücüsü ≥ 570, Git, Python 3.10+, Visual Studio 2022 Build Tools "Desktop development with C++"
(C++ CMake tools dahil). Tam kontrol ve çözümler: [AGENTS.md](AGENTS.md).

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
python -m venv .venv && .venv\Scripts\python.exe -m pip install -r requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

`kur.ps1` modeli (2,95 GB, sha256 doğrulamalı), CUDA 12.8 çalışma zamanı + derleyicisini taşınabilir zip olarak (sistem
kurulumu yok, PATH değişmez), audio.cpp v0.7.2 kaynağını indirir, yamayı uygular, `audiocpp_cli.exe`'yi derler (~15-25 dk)
ve `ayarlar.json`'ı yazar. Kökü kısa tutun (`C:\vox`): nvcc uzun yolda düşer. Başka kart: `-Mimari 75/86/89`.

Hazır derlenmiş motor: Releases sayfasındaki zip (`audiocpp_cli.exe`, GTX 10xx / sm_61, CUDA 12.8). CUDA DLL'leri
(`kur.ps1 -Adim cuda`) ve model (`-Adim model`) yine gerekir.

## Kullanım

Komut satırı:
```powershell
# sesleri listele
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# hazır sesle oku (satır = cümle; "|| paragraf" uzun durak)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# yeni ses tasarla: 3 çeşit, 3 tohum
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# 2. çeşidiyle oku
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
```
Metin kuralları: rakamı yazıyla yazın, tırnak kullanmayın (araç rakam ve tırnağı reddeder), satır başına bir cümle,
satır ≤ 2000 karakter. Yabancı kelimelerin okunuşu: `ayarlar/okunus_sozlugu.tsv`.

Web arayüzü (yalnız 127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → yazdırılan adresi açın.
Üç kutu (tarif, yaratılırken okunan metin, okunacak metin) + çeşit sayısı. *Tasarla* → çeşitleri dinle → birini seç →
*Bu sesle oku* → indir. Ya da hazır sesi seçip oku.

## Lisans ve teşekkür

Kod ve hazır sesler: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. VoxCPM2 (OpenBMB, Apache-2.0), audio.cpp (ShugoAI LLC,
Apache-2.0) ve audio.cpp GGUF dönüşümü üzerine kuruludur. Tam liste: [THIRD_PARTY.md](THIRD_PARTY.md).
OpenBMB, ModelBest ya da audio.cpp projesiyle bağlantısı yoktur.

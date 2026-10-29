"""Ses klonlama (yalnız kendi sesiniz ya da sahibinden açık izin alınmış ses). / Voice cloning (own or consented voice).

Okuma yolunun aynısı: kayıt motorun iki girişine birden (audio + voice_ref), yanında kaydın birebir metni
(reference_text), okunacak metin ve tohum. Kalite sabit: 16 adım, cfg 2.0.
Same path as reading with a designed voice; the recording is fed to audio + voice_ref with its exact transcript.

Gizlilik / privacy: yüklenen kayıt yalnız bu bilgisayarda, geçici klasörde işlenir; referans kodlama önbelleği de
o geçici klasöre yazılır ve iş bitince (hata olsa da) hepsi silinir; motor süreci de kapatılır. Ağa gönderilmez.
Yalnız yapay çıktı kalır: --cikti klasöründe klon_synthetic.wav ve ozet.json (kayıt metni ozet.json'a yazılmaz).
The upload is processed locally in a temp folder (reference-encoding cache too) and deleted when the job ends, also
on failure; nothing goes over the network. Only the synthetic output (klon_synthetic.wav, ozet.json) is kept.

Kayıt: 5-30 sn temiz konuşma önerilir, 3 sn altı reddedilir, 36 sn üstü kırpılır. --onay olmadan çalışmaz.
Recording: 5-30 s of clean speech advised, under 3 s rejected, over 36 s trimmed. Refuses to run without --onay.

python -m ses_tasarim.klonla --kayit benim_sesim.wav --kayit-metni @kayit_metni.txt --metin "Merhaba." \
    --cikti cikti/klon --onay
"""
import argparse
import io
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from . import ayarlar, motor, oku, okunus

# motor referans kodlayıcı kapasitesi 576000 örnek @16 kHz = 36 sn (motor.REFERENCE_OPTION)
MAX_SECONDS = 36.0
MIN_SECONDS = 3.0
ADVICE_SECONDS = (5.0, 30.0)
MAX_UPLOAD_BYTES = 25_000_000
CONSENT_TR = ("Bu ses bana ait ya da sahibinden açık izin aldım; taklit, dolandırıcılık ya da yanıltma için "
              "kullanmayacağım.")
CONSENT_EN = ("This voice is mine or I have the owner's explicit permission; I will not use it for impersonation, "
              "fraud or deception.")
SYNTHETIC_NOTE = "AI-generated synthetic speech (VoxCPM2 voice cloning) / Yapay zekâ ile üretilmiş sestir"
DEFAULT_SEED = 42


class KlonHatasi(ValueError):
    pass


def check(reference_text: str, text: str, consent) -> list:
    """Üretimden önce düz Türkçe sorun listesi. / Plain problem list before any GPU work."""
    found = []
    if consent is not True:
        found.append(okunus.Sorun("izin onayı yok (consent missing): " + CONSENT_TR + " / " + CONSENT_EN, "onay_yok"))
    if len(str(reference_text or "").strip()) < 10:
        found.append(okunus.Sorun("kaydın birebir metni zorunlu: kayıtta ne söyleniyorsa aynısını yazın "
                                  "(exact transcript of the recording required)", "kayit_metni"))
    found += okunus.problems(text or "")
    return found


def prepare_reference(data: bytes, work_dir: Path) -> dict:
    """Yüklenen baytları (wav/mp3/flac/ogg) mono WAV'a çevirir; 36 sn üstünü kırpar. / Decode, mono, trim to 36 s."""
    if not data:
        raise KlonHatasi(okunus.Sorun("ses dosyası boş (empty recording)", "kayit_yok"))
    if len(data) > MAX_UPLOAD_BYTES:
        raise KlonHatasi(okunus.Sorun(f"ses dosyası çok büyük ({len(data) // 1_000_000} MB); 36 sn'lik bir kayıt yeter "
                                      f"(file too large, max {MAX_UPLOAD_BYTES // 1_000_000} MB)",
                                      "kayit_buyuk", mb=MAX_UPLOAD_BYTES // 1_000_000))
    try:
        audio, rate = sf.read(io.BytesIO(data), dtype="float32", always_2d=True)
    except Exception as error:  # libsndfile çözemedi / could not decode
        raise KlonHatasi(okunus.Sorun(f"ses dosyası okunamadı, wav, mp3, flac ya da ogg olmalı "
                                      f"(could not decode; use wav, mp3, flac or ogg): {error}",
                                      "kayit_cozulemedi")) from None
    audio = audio.mean(axis=1).astype(np.float32)
    seconds = len(audio) / rate
    notes = []
    if seconds < MIN_SECONDS:
        raise KlonHatasi(okunus.Sorun(f"kayıt çok kısa ({seconds:.1f} sn); en az {MIN_SECONDS:.0f} sn, önerilen 5-30 sn "
                                      f"(too short; at least {MIN_SECONDS:.0f} s, 5-30 s advised)",
                                      "kayit_kisa", sn=round(seconds, 1), min=int(MIN_SECONDS)))
    if seconds > MAX_SECONDS:
        audio = audio[: int(MAX_SECONDS * rate)]
        notes.append(okunus.Sorun(f"kayıt {seconds:.1f} sn idi, ilk {MAX_SECONDS:.0f} sn kullanıldı; kayıt metni yalnız "
                                  f"bu kısmı içermeli / trimmed to the first {MAX_SECONDS:.0f} s, the transcript must "
                                  f"match that part", "not_kirpildi", sn=round(seconds, 1), max=int(MAX_SECONDS)))
    elif not ADVICE_SECONDS[0] <= seconds <= ADVICE_SECONDS[1]:
        notes.append(okunus.Sorun(f"kayıt {seconds:.1f} sn; en iyi sonuç 5-30 sn temiz kayıtla / best with 5-30 s clean "
                                  f"speech", "not_oneri", sn=round(seconds, 1)))
    work_dir.mkdir(parents=True, exist_ok=True)
    wav = work_dir / "referans.wav"
    sf.write(wav, audio, rate, subtype="PCM_16")
    return {"wav": wav, "sn": round(len(audio) / rate, 2), "notlar": notes}


def write_synthetic_wav(source: Path, target: Path) -> None:
    """Çıktıyı RIFF INFO etiketleriyle (yapay) yazar. / Write output with RIFF INFO 'synthetic' tags."""
    audio, rate = sf.read(source, dtype="float32")
    tmp = target.with_suffix(".tmp.wav")
    with sf.SoundFile(tmp, "w", samplerate=rate, channels=1, subtype="PCM_16", format="WAV") as handle:
        handle.title = "synthetic speech (AI-generated)"
        handle.comment = "AI-generated synthetic speech (VoxCPM2 voice cloning)"  # RIFF INFO: ASCII
        handle.software = "voxcpm2-turkce-ses-tasarimi"
        handle.write(audio)
    tmp.replace(target)


def _remove(folder: Path) -> None:
    """Geçici klasörü siler; Windows'ta kilitli dosya için kısa yeniden deneme. / Delete temp folder, retry on lock."""
    for _ in range(5):
        shutil.rmtree(folder, ignore_errors=True)
        if not folder.exists():
            return
        time.sleep(0.5)
    print(f"uyarı: geçici klasör silinemedi, elle silin (temp folder not deleted, remove it by hand): {folder}",
          file=sys.stderr, flush=True)


def klonla(settings: dict, data: bytes, reference_text: str, text: str, out_dir: Path, consent, seed=None,
           progress=None) -> dict:
    found = check(reference_text, text, consent)
    if found:
        raise KlonHatasi("\n".join(found))
    seed = DEFAULT_SEED if seed in (None, "") else int(seed)
    out_dir = Path(out_dir)
    temp = Path(tempfile.mkdtemp(prefix="klon_"))
    try:
        ref = prepare_reference(data, temp / "ses")
        card = {"ad": "klon", "referans": "referans.wav", "okuma_tohumu": seed,
                "ses_yaratilirken_okutulan_metin": " ".join(str(reference_text).split()), "yapay": True}
        (temp / "ses" / "ses.json").write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")
        # referans kodlama önbelleği kalıcı klasöre değil geçici klasöre / encoding cache goes to the temp folder
        local = {**settings, "onbellek": temp / "onbellek"}
        local["onbellek"].mkdir()
        summary = oku.oku(local, temp / "ses", text, temp / "okuma", progress)
        out_dir.mkdir(parents=True, exist_ok=True)
        wav = out_dir / "klon_synthetic.wav"
        write_synthetic_wav(temp / "okuma" / "okuma.wav", wav)
    finally:
        _remove(temp)  # kayıt, metni ve kodlaması kalıcı tutulmaz (hata olsa da) / nothing persists, also on failure
    result = {"tur": "klon", "tohum": seed, "adim": motor.FIXED["adim"], "cfg": motor.FIXED["cfg"],
              "referans_sn": ref["sn"], "notlar": ref["notlar"], "ses_sn": summary["ses_sn"],
              "sure_sn": summary["sure_sn"], "vram_tepe_mb": summary["vram_tepe_mb"], "wav": str(wav),
              "dosya": wav.name, "satirlar": summary["satirlar"], "yapay": True, "not": SYNTHETIC_NOTE,
              "onay": CONSENT_TR, "tarih": time.strftime("%Y-%m-%d %H:%M")}
    (out_dir / "ozet.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ayarlar", help="ayarlar.json yolu / settings file")
    parser.add_argument("--kayit", type=Path, required=True,
                        help="kendi sesiniz ya da izinli ses, wav/mp3/flac/ogg, 5-30 sn önerilir / "
                             "own or consented recording, 5-30 s advised")
    parser.add_argument("--kayit-metni", required=True,
                        help="kayıtta söylenenin birebir metni ya da @dosya / exact transcript or @file")
    parser.add_argument("--metin", required=True,
                        help="okunacak metin ya da @dosya; satır = cümle / text to read or @file, one sentence per line")
    parser.add_argument("--cikti", type=Path, required=True,
                        help="çıktı klasörü: klon_synthetic.wav, ozet.json / output folder")
    parser.add_argument("--tohum", type=int, default=DEFAULT_SEED, help="tohum / seed (varsayılan / default 42)")
    parser.add_argument("--onay", action="store_true", help="zorunlu / required: " + CONSENT_TR + " / " + CONSENT_EN)
    args = parser.parse_args(argv)
    if not args.onay:  # kayıt okunmadan, motor açılmadan önce / before reading the file or starting the engine
        parser.error("--onay olmadan klonlama yapılmaz (cloning requires --onay): " + CONSENT_TR + " / " + CONSENT_EN)

    def text_arg(value):
        return Path(value[1:]).read_text(encoding="utf-8") if value.startswith("@") else value

    data = None
    try:
        data = args.kayit.read_bytes()
        settings = ayarlar.load(args.ayarlar)
        result = klonla(settings, data, text_arg(args.kayit_metni), text_arg(args.metin), args.cikti, True,
                        args.tohum,
                        lambda done, total, elapsed: print(f"  {done}/{total} cümle, {elapsed:.0f} sn", flush=True))
    except (KlonHatasi, ayarlar.AyarHatasi, motor.MotorHatasi, OSError) as error:
        print(f"hata (error): {error}", file=sys.stderr)
        return 1
    finally:
        data = None
    for note in result["notlar"]:
        print("not:", note)
    print(f"bitti: {result['ses_sn']} sn yapay ses, {result['sure_sn']} sn, VRAM tepe {result['vram_tepe_mb']} MB "
          f"→ {result['wav']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""audio.cpp (yamalı) motorunu tek oturumda istek dizisiyle çalıştırır. / Runs the patched audio.cpp engine.

Kalite sabit: 16 adım, cfg 2.0. Tohum kalite ayarı değildir: tasarımda çeşitlilik, okumada sesin kendi tohumu.
Fixed quality: 16 steps, cfg 2.0. The seed is not a quality knob.
"""
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from . import kelime_zamani, vulkan_sinir

FIXED = {"adim": 16, "cfg": 2.0}
SAMPLE_RATE = 48000
TEXT_CHUNK = 2048
# referans kodlayıcı örnek kapasitesi: motor varsayılanı 240000 (16 kHz, 15 sn); tasarım kayıtları 20-35 sn → 36 sn
REFERENCE_OPTION = ("--session-option", "voxcpm2.audiovae_encoder_sample_capacity=576000")
MIN_REFERENCE_SECONDS = 8.0
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0
WINDOWS = sys.platform == "win32"
# Motorun ara dosyaları (motor.log satır başına ~0,3 MB, kelime zamanı sondası dahil; PCM dökümleri) iş başarıyla bitince silinir; hata olursa kalır.
# 1 = her zaman sakla (hata ayıklama). / Engine scratch files are deleted after a successful run, kept on failure.
KEEP_ENV = "SES_TASARIM_ARA_DOSYA_TUT"
ENGINE_DIR = "_motor_is"


class MotorHatasi(RuntimeError):
    pass


def _gpu_used_mb(backend: str = "cuda", pid: int | None = None) -> int:
    """GPU belleği (MB). CUDA/macOS toplam kullanımı, Windows Vulkan motor sürecinin ayrılmış belleğini ölçer.
    GPU memory in MB. CUDA/macOS report total use; Windows Vulkan reports dedicated memory for the engine PID."""
    if sys.platform == "darwin":
        out = subprocess.run(["ioreg", "-r", "-d", "1", "-c", "IOAccelerator"], capture_output=True, text=True,
                             timeout=5).stdout
        return int(out.split('"In use system memory"=')[1].split(",")[0].split("}")[0]) // (1024 * 1024)
    if WINDOWS and backend == "vulkan" and pid is not None:
        # Windows GPU Performance Counters expose one row per PID and adapter. Summing DedicatedUsage gives the
        # engine's own VRAM allocation even when the machine has both an iGPU and a discrete AMD GPU.
        script = (
            f"$f=\"Name LIKE 'pid_{int(pid)}_%'\";"
            "$n=(Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory -Filter $f "
            "| Measure-Object DedicatedUsage -Sum).Sum;"
            "if($null -eq $n){0}else{[long]($n/1MB)}"
        )
        out = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", script],
                             capture_output=True, text=True, timeout=5, creationflags=NO_WINDOW).stdout
        mb = int(out.strip().splitlines()[-1])
        if mb <= 0:  # sayaç satırı yok ya da boş: ölçüm sayılmaz, yanıltıcı 0 yazılmaz / no counter row: not a reading
            raise ValueError("Vulkan GPU sayacı değer vermedi / no GPU counter value")
        return mb
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True, timeout=5, creationflags=NO_WINDOW).stdout
    return int(out.strip().splitlines()[0])


def _pid_toplam_mb(ogeler, pid: int) -> int:
    """PDH satırlarından (ad, durum, bayt) motor sürecinin ayrılmış belleği (MB); bütün bağdaştırıcılar toplanır.
    Değer yoksa ya da 0 ise ValueError: ölçüm sayılmaz, yanıltıcı 0 yazılmaz.
    Sum of dedicated memory over the engine PID's rows (all adapters); no value or 0 is not a reading."""
    onek = f"pid_{int(pid)}_"
    toplam = sum(deger for ad, durum, deger in ogeler if ad and ad.startswith(onek) and durum in (0, 1))
    mb = int(toplam) // (1024 * 1024)
    if mb <= 0:
        raise ValueError("Vulkan GPU sayacı değer vermedi / no GPU counter value")
    return mb


class PdhGpuBellek:
    """Windows GPU süreç belleği sayacını PDH ile doğrudan okur; ölçüm başına süreç açmaz (#17).
    Reads the Windows GPU process memory counter directly via PDH, without starting a process per reading."""
    YOL = "\\GPU Process Memory(*)\\Dedicated Usage"
    PDH_FMT_LARGE = 0x00000400
    PDH_MORE_DATA = 0x800007D2

    def __init__(self):
        import ctypes
        from ctypes import wintypes

        class _Deger(ctypes.Structure):  # PDH_FMT_COUNTERVALUE (birliğin yalnız largeValue alanı / union: largeValue)
            _fields_ = [("CStatus", wintypes.DWORD), ("largeValue", ctypes.c_longlong)]

        class _Oge(ctypes.Structure):  # PDH_FMT_COUNTERVALUE_ITEM_W
            _fields_ = [("szName", ctypes.c_wchar_p), ("FmtValue", _Deger)]

        self._c, self._w, self._Oge = ctypes, wintypes, _Oge
        pdh = ctypes.WinDLL("pdh")
        pdh.PdhOpenQueryW.argtypes = [wintypes.LPCWSTR, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]
        pdh.PdhAddEnglishCounterW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR, ctypes.c_void_p,
                                              ctypes.POINTER(ctypes.c_void_p)]
        pdh.PdhCollectQueryData.argtypes = [ctypes.c_void_p]
        pdh.PdhGetFormattedCounterArrayW.argtypes = [ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD),
                                                     ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
        pdh.PdhCloseQuery.argtypes = [ctypes.c_void_p]
        for ad in ("PdhOpenQueryW", "PdhAddEnglishCounterW", "PdhCollectQueryData", "PdhGetFormattedCounterArrayW",
                   "PdhCloseQuery"):
            getattr(pdh, ad).restype = wintypes.DWORD
        self._pdh = pdh
        self._sorgu, self._sayac = ctypes.c_void_p(), ctypes.c_void_p()
        if pdh.PdhOpenQueryW(None, None, ctypes.byref(self._sorgu)):
            raise OSError("PdhOpenQueryW")
        if pdh.PdhAddEnglishCounterW(self._sorgu, self.YOL, None, ctypes.byref(self._sayac)):
            self.kapat()
            raise OSError("PdhAddEnglishCounterW: GPU Process Memory sayacı yok / counter not available")

    def ogeler(self) -> list:
        """Anlık (ad, durum, bayt) satırları. / Current (name, status, bytes) rows."""
        c, w = self._c, self._w
        if self._pdh.PdhCollectQueryData(self._sorgu):
            raise OSError("PdhCollectQueryData")
        for _ in range(3):  # örnek sayısı iki çağrı arasında değişebilir / instance count may change between calls
            boyut, sayi = w.DWORD(0), w.DWORD(0)
            r = self._pdh.PdhGetFormattedCounterArrayW(self._sayac, self.PDH_FMT_LARGE, c.byref(boyut),
                                                       c.byref(sayi), None)
            if r == 0:  # hiç örnek yok (GPU'yu kullanan süreç yok) / no instances at all
                return []
            if r != self.PDH_MORE_DATA:
                raise OSError(f"PdhGetFormattedCounterArrayW boyut: {r:#x}")
            tampon = c.create_string_buffer(boyut.value)
            r = self._pdh.PdhGetFormattedCounterArrayW(self._sayac, self.PDH_FMT_LARGE, c.byref(boyut),
                                                       c.byref(sayi), tampon)
            if r == self.PDH_MORE_DATA:
                continue
            if r:
                raise OSError(f"PdhGetFormattedCounterArrayW: {r:#x}")
            dizi = c.cast(tampon, c.POINTER(self._Oge))
            return [(dizi[i].szName, dizi[i].FmtValue.CStatus, dizi[i].FmtValue.largeValue) for i in range(sayi.value)]
        raise OSError("PdhGetFormattedCounterArrayW: boyut oturmadı / size kept changing")

    def oku_mb(self, pid: int) -> int:
        return _pid_toplam_mb(self.ogeler(), pid)

    def kapat(self):
        if self._sorgu:
            self._pdh.PdhCloseQuery(self._sorgu)
            self._sorgu = self._c.c_void_p()


class VramWatcher:
    """CUDA, Metal ve Windows Vulkan tepe VRAM ölçümü. Ölçülemezse peak_mb None kalır, yanıltıcı 0 yazılmaz.
    Peak VRAM for CUDA, Metal and Windows Vulkan. When unavailable, peak_mb stays None instead of a misleading 0."""

    def __init__(self, backend: str = "cuda", pid: int | None = None):
        self.backend = backend
        self.pid = pid
        self.peak_mb = None
        self.interval = self.aralik(backend, pid)
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    @staticmethod
    def aralik(backend: str, pid: int | None) -> float:
        """Ölçüm aralığı (sn). Windows Vulkan'ın yedek yolu (PowerShell) her ölçümde süreç açar (~0,6 işlemci sn): 2 sn.
        PDH açılırsa (#17) süreç açılmaz, aralık 0,5 sn'ye iner. CUDA/macOS 0,5 sn.
        Ölçüm (GTX 1050 Ti, Vulkan, PowerShell): 0,5 sn'de işlemci +%94, 2 sn'de +%30; süre +%1, VRAM tepe aynı.
        PDH 0,5 sn (#17, meşgul işlemci izleme kapalıya göre): GTX 1050 Ti +%9 (PowerShell 2 sn +%43), Intel HD 630 +%1 (+%62).
        Polling interval: the PowerShell fallback spawns a process per reading, so 2 s; with PDH and on CUDA/macOS 0.5 s."""
        return 2.0 if WINDOWS and backend == "vulkan" and pid is not None else 0.5

    def _vulkan_pdh(self):
        """Windows Vulkan'da PDH okuyucusu; açılamazsa None (PowerShell yedeğine düşülür). / PDH reader or None."""
        if not (WINDOWS and self.backend == "vulkan" and self.pid is not None):
            return None
        try:
            return PdhGpuBellek()
        except Exception:  # noqa: BLE001 — pdh.dll ya da sayaç yok: yedek yol / no PDH or counter: fallback
            return None

    PDH_HATA_SINIRI = 3  # art arda bu kadar PDH okuma hatası: PowerShell yedeğine geç / consecutive errors → fallback

    def _loop(self):
        pdh = self._vulkan_pdh()
        if pdh is not None:
            self.interval = 0.5  # süreç açılmıyor / no process per reading
        hata = 0
        try:
            while not self._stop.is_set():
                try:
                    mb = pdh.oku_mb(self.pid) if pdh is not None else _gpu_used_mb(self.backend, self.pid)
                    self.peak_mb = max(self.peak_mb or 0, mb)
                    hata = 0
                except FileNotFoundError:  # ölçüm aracı yok: boşuna süreç açılmaz / no tool, stop polling
                    return
                except ValueError:  # okuma oldu ama o an değer yok (0): ölçüm sayılmaz, hata da değil / read ok, no value
                    hata = 0
                except Exception:  # noqa: BLE001 — PDH okunamıyor: art arda sınırda yedek yola / PDH read keeps failing
                    hata += 1
                    if pdh is not None and hata >= self.PDH_HATA_SINIRI:
                        pdh.kapat()
                        pdh, self.interval = None, self.aralik(self.backend, self.pid)
                self._stop.wait(self.interval)
        finally:
            if pdh is not None:
                pdh.kapat()

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._thread.join()


def vram_max(*values):
    """Ölçülen değerlerin en büyüğü; hiçbiri ölçülmediyse None. / Largest measured value, None if none measured."""
    measured = [v for v in values if v is not None]
    return max(measured) if measured else None


def vram_metni(mb) -> str:
    """Komut satırı özeti için VRAM parçası. / VRAM part of the command-line summary."""
    return f"VRAM tepe {mb} MB" if mb is not None else "VRAM ölçülemedi"


def ascii_olmayan_yol(paths):
    """Motorun göreceği yollardan ASCII olmayan ilki (yoksa None). Windows'ta motor Türkçe harfli ya da başka
    ASCII dışı yolu açamıyor (topluluk testi: 'No mapping for the Unicode character…', 'Failed to open log file').
    First non-ASCII path the engine would see; on Windows the engine cannot open such paths (community report)."""
    for path in paths:
        if path and not str(path).isascii():
            return str(path)
    return None


def _yol_ipucu(command: list, requests: list) -> str:
    """Motor düştüyse ve yollardan biri ASCII değilse anlaşılır ipucu (Windows). / Clear hint for non-ASCII paths."""
    if not WINDOWS:
        return ""
    bad = ascii_olmayan_yol(list(command) + [r.get(k) for r in requests for k in ("audio", "voice_ref")])
    if not bad:
        return ""
    return ("\nİpucu: motor Windows'ta yalnız ASCII (Türkçe harf içermeyen) yollarla çalışıyor; şu yol ASCII değil: "
            f"{bad}. Kurulumu, repo klasörünü ve sesleri kısa, ASCII bir klasöre taşıyın (ör. C:\\vox).\n"
            "Hint: on Windows the engine only works with ASCII-only paths; the path above is not ASCII. "
            "Move the install, the repo folder and the voices to a short ASCII folder (e.g. C:\\vox).")


def _dilim_karti_denetle(settings: dict, stdout_yolu: Path) -> None:
    """Dilim boyu için okunan kart, motorun seçtiği kartla aynı mı (Vulkan). Değilse yalnız uyarır.
    Warns if the device whose limit chose the chunk is not the one the engine opened."""
    if settings.get("backend", "cuda") != "vulkan":
        return
    _, beklenen = vulkan_sinir.dilim_sn(settings)
    try:
        gercek = vulkan_sinir.motor_adi(stdout_yolu.read_text(encoding="utf-8", errors="replace"), settings.get("cihaz"))
    except OSError:
        return
    if beklenen and gercek and gercek != beklenen:
        print(f"  uyarı: dilim boyu '{beklenen}' kartına göre seçildi, motor '{gercek}' kartını açtı "
              f"/ warning: chunk chosen for '{beklenen}', engine opened '{gercek}'", flush=True)


def engine_env(settings: dict, work_dir: Path) -> dict:
    """4 GB sığdırma ve hız ayarları; yalnız motor sürecine verilir. / 4 GB fit + speed env, engine process only."""
    env = dict(os.environ)
    if settings.get("cuda_bin"):
        env["PATH"] = str(settings["cuda_bin"]) + os.pathsep + env.get("PATH", "")
    dilim, _ = vulkan_sinir.dilim_sn(settings)  # sınırı düşük Vulkan kartında (Intel) kısa dilim; NVIDIA/AMD/CUDA 10 sn
    env.update({
        "VOXCPM2_KV_CAPACITY": "auto",                       # KV önbelleği gerektiği kadar (yama a)
        "VOXCPM2_AUDIOVAE_CPU": "1",                         # AudioVAE kodlayıcı CPU'da (yama a)
        "VOXCPM2_AUDIOVAE_THREADS": str(settings.get("audiovae_threads", 6)),
        "VOXCPM2_AUDIOVAE_GPU_CHUNK": f"{dilim:g}",          # LM boşalt, çözücü GPU'da dilimlerle (yama b): 10 sn, Intel 5
        "VOXCPM2_TOPLU_COZ": "1",                            # önce bütün satırlar, sonra tek seferde çözüm (yama c5)
        "VOXCPM2_PROMPT_CACHE_DIR": str(settings["onbellek"]),  # referans kodlaması diske (yama c4)
        "VOXCPM2_PROBE_EOS_CONFIRMATIONS": "2",
        "VOXCPM2_PROBE_POSITION_CONSENSUS": "8",
        "VOXCPM2_PROBE_ACOUSTIC_RESCUE": "1",
        "VOXCPM2_PROBE_HOLD_UNTIL": "0",
        "VOXCPM2_PROBE_DISABLE_EOS": "0",
        "VOXCPM2_PROBE_FULL_TRACE": "0",
        "VOXCPM2_PROBE_PCM_DIR": str(work_dir),
    })
    return env


def reference_wav(reference: Path, work_dir: Path) -> Path:
    """FLAC ya da başka biçimdeki referansı motor için WAV'a çevirir (kayıpsız). / Decode reference to WAV."""
    reference = Path(reference)
    if reference.suffix.lower() == ".wav":
        return reference
    audio, rate = sf.read(reference, dtype="float32")
    work_dir.mkdir(parents=True, exist_ok=True)
    target = work_dir / (reference.stem + ".wav")
    sf.write(target, audio, rate, subtype="PCM_16")
    return target


def design_request(request_id: str, description: str, text: str, seed: int) -> dict:
    # tarif parantez içinde metnin önüne; parantez prompt sınırıdır
    return {"id": request_id, "text": f"({description.strip()}){text.strip()}", "seed": int(seed)}


def read_request(request_id: str, text: str, seed: int, reference: Path, reference_text: str) -> dict:
    # tasarım kaydı iki girişe birden (audio + voice_ref), yanında okunan metni (reference_text) ve sesin tohumu
    return {"id": request_id, "text": text, "seed": int(seed), "audio": str(reference), "voice_ref": str(reference),
            "reference_text": reference_text.strip()}


def _eos_by_block(log_path: Path, count: int, cpu: bool = False) -> list:
    """Her istek bloğu 'toplu_coz.deferred' ile biter; CPU'da kod çözücü satırı blok sınırıdır ve aynı istekte
    yalnız bir kez sayılır. EOS'suz blok yarım ses demektir. Log satır satır okunur.
    CPU arka ucunda toplu çözüm (yama c5) devreye girmez: her blok anında çözülür ve 'toplu_coz.deferred' yerine
    'voxcpm2.audiovae_decoder_ms ' satırıyla biter; CPU'da o satır da blok sonu sayılır."""
    ok, block, decoder_seen = [False] * count, 0, False
    if not log_path.exists():
        return ok
    with open(log_path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if block < count and "eos_accepted_at_patch" in line:
                ok[block] = True
                decoder_seen = False
            if "voxcpm2.toplu_coz.deferred" in line or (
                    cpu and "voxcpm2.audiovae_decoder_ms" in line and not decoder_seen):
                block += 1
                decoder_seen = cpu
    return ok


def run_sequence(settings: dict, requests: list, work_dir: Path, progress=None, sonda: bool = False) -> dict:
    """İstekleri tek motor oturumunda üretir. Dönen: audios {id: float32}, bad [id], seconds, vram_peak_mb;
    sonda=True ise 'sonda' (istek başına dikkat kaydı, kelime_zamani.parse_log) da döner.

    Motor dosyaları `work_dir/_motor_is` içine yazılır; iş bitince (sesler belleğe okununca) silinir, motor hata
    verirse inceleme için kalır (`SES_TASARIM_ARA_DOSYA_TUT=1` her zaman saklar).
    Runs all requests in one engine session (model loaded once); engine scratch files are removed afterwards."""
    work_dir = Path(work_dir).resolve() / ENGINE_DIR
    work_dir.mkdir(parents=True, exist_ok=True)
    for request in requests:
        request.update({"num_inference_steps": FIXED["adim"], "guidance_scale": FIXED["cfg"],
                        "text_chunk_size": TEXT_CHUNK, "max_tokens": 80 + int(len(request["text"]) * 1.2)})
    (work_dir / "dizi.json").write_text(json.dumps({"requests": requests}, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    log_path = work_dir / "motor.log"
    command = [str(settings["motor"]), "--model", str(settings["model"]), "--task", "tts",
               "--backend", settings.get("backend", "cuda"), "--threads", str(settings.get("motor_threads", 4)),
               *(["--device", str(settings["cihaz"])] if settings.get("cihaz") not in (None, "") else []),
               "--request-sequence", str(work_dir / "dizi.json"), *REFERENCE_OPTION,
               "--out-dir", str(work_dir / "out"), "--batch-manifest-out", str(work_dir / "manifest.json"),
               "--log", "--log-file", str(log_path), "--metrics"]
    cpu = settings.get("backend", "cuda") == "cpu"
    started = time.time()
    with (work_dir / "stdout.txt").open("w", encoding="utf-8") as out:
        env = engine_env(settings, work_dir)
        if sonda:
            env.update(kelime_zamani.probe_env())  # kelime zamanı: 21. katman dikkati log'a (yama c1)
        process = subprocess.Popen(command, env=env, stdout=out, stderr=subprocess.STDOUT,
                                   creationflags=NO_WINDOW)
        with VramWatcher(settings.get("backend", "cuda"), getattr(process, "pid", None)) as watcher:
            try:
                while process.poll() is None:
                    if progress:
                        progress(sum(_eos_by_block(log_path, len(requests), cpu)), len(requests), time.time() - started)
                    time.sleep(3)
            finally:
                # hata ya da Ctrl+C: motor yetim kalmasın, çalışma klasöründeki dosyalar serbest kalsın (silinebilsin)
                # on error or Ctrl+C: do not orphan the engine; release its files so the work folder can be deleted
                if process.poll() is None:
                    process.kill()
                    process.wait()
    _dilim_karti_denetle(settings, work_dir / "stdout.txt")
    if process.returncode != 0:
        tail = (work_dir / "stdout.txt").read_text(encoding="utf-8", errors="replace")[-1500:]
        raise MotorHatasi(f"motor rc={process.returncode}; {work_dir / 'stdout.txt'}\n{tail}"
                          + _yol_ipucu(command, requests))
    ok = _eos_by_block(log_path, len(requests), cpu)
    audios, bad = {}, []
    for request, finished in zip(requests, ok):
        wav = work_dir / "out" / f"{request['id']}.wav"
        if not finished or not wav.exists():
            bad.append(request["id"])
            continue
        audio, rate = sf.read(wav, dtype="float32")
        if rate != SAMPLE_RATE:
            raise MotorHatasi(f"beklenmeyen örnekleme {rate}")
        audios[request["id"]] = audio
    probes = None
    if sonda and not bad:
        try:
            probes = kelime_zamani.parse_log(log_path, cpu)
        except (OSError, ValueError) as error:  # kelime zamanı yan üründür; okuma bozulmaz
            probes = None
            print(f"  kelime zamanı okunamadı: {error}", flush=True)
    if not bad and os.environ.get(KEEP_ENV) != "1":  # yarım kalan satır varsa log inceleme için kalır
        shutil.rmtree(work_dir, ignore_errors=True)
    return {"audios": audios, "bad": bad, "seconds": round(time.time() - started, 1), "vram_peak_mb": watcher.peak_mb,
            "sonda": probes}


def silence(seconds: float) -> np.ndarray:
    return np.zeros(int(seconds * SAMPLE_RATE), dtype=np.float32)


def join_lines(audios: list, pauses: list) -> np.ndarray:
    """Satırları aralarına durak koyarak birleştirir (ses işlenmez). / Concatenate with pauses, no processing."""
    pieces = []
    for index, audio in enumerate(audios):
        if index:
            pieces.append(silence(pauses[index - 1]))
        pieces.append(audio)
    return np.concatenate(pieces)


def write_wav(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.wav")
    sf.write(tmp, audio, SAMPLE_RATE, subtype="PCM_16")
    os.replace(tmp, path)


def list_devices(settings: dict) -> str:
    env = engine_env(settings, Path("."))
    result = subprocess.run([str(settings["motor"]), "--list-devices"], env=env, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", creationflags=NO_WINDOW, timeout=120)
    return (result.stdout + result.stderr).strip()

"""audio.cpp (yamalı) motorunu tek oturumda istek dizisiyle çalıştırır. / Runs the patched audio.cpp engine.

Kalite sabit: 16 adım, cfg 2.0. Tohum kalite ayarı değildir: tasarımda çeşitlilik, okumada sesin kendi tohumu.
Fixed quality: 16 steps, cfg 2.0. The seed is not a quality knob.
"""
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np
import soundfile as sf

FIXED = {"adim": 16, "cfg": 2.0}
SAMPLE_RATE = 48000
TEXT_CHUNK = 2048
# referans kodlayıcı örnek kapasitesi: motor varsayılanı 240000 (16 kHz, 15 sn); tasarım kayıtları 20-35 sn → 36 sn
REFERENCE_OPTION = ("--session-option", "voxcpm2.audiovae_encoder_sample_capacity=576000")
MIN_REFERENCE_SECONDS = 8.0
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0


class MotorHatasi(RuntimeError):
    pass


class VramWatcher:
    """nvidia-smi ile VRAM tepe ölçümü (yoksa 0). / Peak VRAM via nvidia-smi."""

    def __init__(self):
        self.peak_mb = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def _loop(self):
        while not self._stop.is_set():
            try:
                out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                     capture_output=True, text=True, timeout=5, creationflags=NO_WINDOW).stdout
                self.peak_mb = max(self.peak_mb, int(out.strip().splitlines()[0]))
            except Exception:
                pass
            self._stop.wait(0.5)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._thread.join()


def engine_env(settings: dict, work_dir: Path) -> dict:
    """4 GB sığdırma ve hız ayarları; yalnız motor sürecine verilir. / 4 GB fit + speed env, engine process only."""
    env = dict(os.environ)
    if settings.get("cuda_bin"):
        env["PATH"] = str(settings["cuda_bin"]) + os.pathsep + env.get("PATH", "")
    env.update({
        "VOXCPM2_KV_CAPACITY": "auto",                       # KV önbelleği gerektiği kadar (yama a)
        "VOXCPM2_AUDIOVAE_CPU": "1",                         # AudioVAE kodlayıcı CPU'da (yama a)
        "VOXCPM2_AUDIOVAE_THREADS": str(settings.get("audiovae_threads", 6)),
        "VOXCPM2_AUDIOVAE_GPU_CHUNK": "10",                  # LM boşalt, çözücü GPU'da 10 sn dilimlerle (yama b)
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


def _eos_by_block(log_path: Path, count: int) -> list:
    """Her istek bloğu 'toplu_coz.deferred' ile biter; EOS'suz blok yarım ses demektir. Log satır satır okunur."""
    ok, block = [False] * count, 0
    if not log_path.exists():
        return ok
    with open(log_path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if block < count and "eos_accepted_at_patch" in line:
                ok[block] = True
            if "voxcpm2.toplu_coz.deferred" in line:
                block += 1
    return ok


def run_sequence(settings: dict, requests: list, work_dir: Path, progress=None) -> dict:
    """İstekleri tek motor oturumunda üretir. Dönen: audios {id: float32}, bad [id], seconds, vram_peak_mb.

    Runs all requests in one engine session (model loaded once)."""
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    for request in requests:
        request.update({"num_inference_steps": FIXED["adim"], "guidance_scale": FIXED["cfg"],
                        "text_chunk_size": TEXT_CHUNK, "max_tokens": 80 + int(len(request["text"]) * 1.2)})
    (work_dir / "dizi.json").write_text(json.dumps({"requests": requests}, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    log_path = work_dir / "motor.log"
    command = [str(settings["motor"]), "--model", str(settings["model"]), "--task", "tts",
               "--backend", settings.get("backend", "cuda"), "--threads", str(settings.get("motor_threads", 4)),
               "--request-sequence", str(work_dir / "dizi.json"), *REFERENCE_OPTION,
               "--out-dir", str(work_dir / "out"), "--batch-manifest-out", str(work_dir / "manifest.json"),
               "--log", "--log-file", str(log_path), "--metrics"]
    started = time.time()
    with (work_dir / "stdout.txt").open("w", encoding="utf-8") as out, VramWatcher() as watcher:
        process = subprocess.Popen(command, env=engine_env(settings, work_dir), stdout=out, stderr=subprocess.STDOUT,
                                   creationflags=NO_WINDOW)
        while process.poll() is None:
            if progress:
                progress(sum(_eos_by_block(log_path, len(requests))), len(requests), time.time() - started)
            time.sleep(3)
    if process.returncode != 0:
        tail = (work_dir / "stdout.txt").read_text(encoding="utf-8", errors="replace")[-1500:]
        raise MotorHatasi(f"motor rc={process.returncode}; {work_dir / 'stdout.txt'}\n{tail}")
    ok = _eos_by_block(log_path, len(requests))
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
    return {"audios": audios, "bad": bad, "seconds": round(time.time() - started, 1), "vram_peak_mb": watcher.peak_mb}


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

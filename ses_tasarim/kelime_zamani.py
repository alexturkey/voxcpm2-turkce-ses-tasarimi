"""Kelime zamanı motorun içinden: her kelimenin başlangıç ve bitiş saniyesi, dış hizalama modeli (CTC, Whisper) olmadan.
Word timings from inside the engine, no external alignment model.

Yöntem / method:
1. Sonda (yama c1): motor her ses yamasında (160 ms) BaseLM'in 21. katmanının metin satırlarına baktığı dikkat (attention)
   olasılıklarını log'a yazar (`VOXCPM2_PROBE_ATTENTION=21`). Kelimeye düşen dikkat payı tek yönlü bir yolla (DP)
   yamalara dağıtılır: kaba zaman (±160 ms).
   The engine logs layer-21 attention over the text rows for every 160 ms patch; a monotonic path gives rough times.
2. İnce ayar: kaba sınırlar sesin enerjisine oturtulur (10 ms çerçeve). Konuşma/sessizlik kararı 100 Hz altı atılmış
   sesten verilir (referans sesindeki uğultu sessizliği konuşma saymasın).
   Rough bounds are snapped to the audio energy (10 ms frames); voiced/silent is decided on 100 Hz high-passed audio.
3. Çekirdek kenar (tepe -15 dB) ve birleştirici: kenar, ±160 ms adaylar arasından 9 ipucunun ortak ağırlıklı puanıyla seçilir.
   Core edge (peak -15 dB), then a combiner picks each edge among ±160 ms candidates with 9 shared-weight cues.

Sözlük (tokenizer) model dosyasının (.gguf) içinden okunur; ayrı indirme yoktur. / The tokenizer is read from the .gguf.
Dil: boşluksuz yazılan dillerde (zh, ja) her karakter bir birimdir. / zh, ja: one unit per character.
"""
import json
import re
import struct
from functools import lru_cache
from pathlib import Path

import numpy as np

PROBE_LAYER = 21          # ölçüm: 20 çöker, 22 bitişte kötü, 24 iki kat hata (kelime_zamani_arastirma deneme_01)
LEAD_PATCHES = 1          # dikkat satırı bir yama önden gelir
PATCH_SECONDS = 0.16      # motor yaması: 4 x 1920 örnek / 48 kHz
FRAME_SECONDS = 0.01
HIGHPASS_HZ = 100.0
TRACE = re.compile(r"voxcpm2\.probe\.(prefill_tokens|attention_rows|ar_patch) (.+)$")
NO_SPACE_LANGUAGES = ("zh", "ja")


def probe_env() -> dict:
    return {"VOXCPM2_PROBE_ATTENTION": str(PROBE_LAYER)}


# --- sözlük: .gguf içindeki tokenizer.json / tokenizer embedded in the .gguf ---------------------------------------

_SIZES = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 4, 7: 1, 10: 8, 11: 8, 12: 8}


def _gguf_embedded_file(model: Path, name: str) -> bytes:
    """audio.cpp .gguf üst verisindeki gömülü dosyayı döndürür (audiocpp.embedded_files.*)."""
    with open(model, "rb") as f:
        if f.read(4) != b"GGUF":
            raise ValueError(f"gguf değil: {model}")
        f.read(4 + 8)
        (count,) = struct.unpack("<Q", f.read(8))

        def text():
            (n,) = struct.unpack("<Q", f.read(8))
            return f.read(n)

        def value(kind):
            if kind == 8:
                return text()
            if kind == 9:
                item, n = struct.unpack("<IQ", f.read(12))
                if item in (0, 1):  # bayt dizisi tek okumada / byte arrays in one read
                    return f.read(n)
                if item == 8:
                    return [text() for _ in range(n)]
                if item == 10:
                    return list(struct.unpack(f"<{n}Q", f.read(8 * n)))
                f.seek(_SIZES[item] * n, 1)
                return None
            f.seek(_SIZES[kind], 1)
            return None

        meta = {}
        for _ in range(count):
            key = text().decode("utf-8")
            (kind,) = struct.unpack("<I", f.read(4))
            meta[key] = value(kind)
            if all(k in meta for k in ("audiocpp.embedded_files.names", "audiocpp.embedded_files.offsets",
                                       "audiocpp.embedded_files.data")):
                break
    names = [n.decode("utf-8") for n in meta["audiocpp.embedded_files.names"]]
    offsets = meta["audiocpp.embedded_files.offsets"] + [len(meta["audiocpp.embedded_files.data"])]
    index = names.index(name)
    return meta["audiocpp.embedded_files.data"][offsets[index]:offsets[index + 1]]


@lru_cache(maxsize=2)
def _pieces_cached(model: str, stamp: float) -> dict:
    side = Path(model).with_name("tokenizer.json")
    raw = side.read_bytes() if side.is_file() else _gguf_embedded_file(Path(model), "tokenizer.json")
    data = json.loads(raw.decode("utf-8"))
    pieces = {token_id: piece for piece, token_id in data["model"]["vocab"].items()}
    for added in data.get("added_tokens", []):
        pieces[added["id"]] = ""
    return pieces


def load_pieces(model: Path) -> dict:
    model = Path(model)
    return _pieces_cached(str(model), model.stat().st_mtime)


def _piece_bytes(piece: str) -> bytes:
    if re.fullmatch(r"<0x[0-9A-Fa-f]{2}>", piece):
        return bytes([int(piece[3:5], 16)])
    return piece.replace("▁", " ").encode("utf-8")


# --- log okuma / log parsing ----------------------------------------------------------------------------------------

def parse_log(log_path: Path, cpu: bool = False) -> list:
    """İstek başına {'tokens', 'rows', 'patches'}. İstek bloğu 'toplu_coz.deferred' ile biter (CPU'da kod çözücü satırı);
    aynı blokta sonda yeniden başlarsa (yeniden deneme) son deneme geçerlidir. Log satır satır okunur (büyük olabilir)."""
    requests, current, decoder_seen = [], None, False
    with open(log_path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if "voxcpm2.probe." in line:
                match = TRACE.search(line.rstrip("\n"))
                if match:
                    kind, value = match.groups()
                    if kind == "prefill_tokens":
                        current = {"tokens": json.loads(value), "rows": [], "patches": 0}
                    elif current is not None and kind == "attention_rows":
                        current["rows"].append(json.loads(value)[0])
                    elif current is not None and kind == "ar_patch":
                        current["patches"] = int(value)
            if "voxcpm2.toplu_coz.deferred" in line or (
                    cpu and "voxcpm2.audiovae_decoder_ms" in line and not decoder_seen):
                requests.append(current)
                current, decoder_seen = None, cpu
            elif "eos_accepted_at_patch" in line:
                decoder_seen = False
    return requests


# --- kaba zaman: dikkatten / rough times from attention -------------------------------------------------------------

def units(text: str, dil: str = "tr") -> list:
    """Zamanlanacak birimler: boşlukla ayrılmış kelimeler; zh/ja'da noktalama önceki karaktere yapışık karakterler."""
    words = text.split()
    if dil not in NO_SPACE_LANGUAGES:
        return words
    out = []
    for word in words:
        for char in word:
            if out and not char.isalnum():
                out[-1] += char
            else:
                out.append(char)
    return out


def _token_char_spans(tokens: list, pieces: dict) -> tuple:
    raw, spans = b"", []
    for token in tokens:
        start = len(raw)
        if token >= 0:
            raw += _piece_bytes(pieces.get(token, ""))
        spans.append((start, len(raw)))
    text = raw.decode("utf-8", errors="replace")
    char_at = np.zeros(len(raw) + 1, dtype=np.int64)
    position = 0
    for index, char in enumerate(text):
        size = len(char.encode("utf-8"))
        char_at[position:position + size] = index
        position += size
    char_at[position:] = len(text)
    return text, [(int(char_at[a]), int(char_at[b])) if b > a else None for a, b in spans]


def _owners(tokens: list, pieces: dict, spoken: str, words: list) -> np.ndarray:
    text, spans = _token_char_spans(tokens, pieces)
    base = text.rfind(spoken)
    if base < 0:
        raise ValueError(f"metin sonda belirteçlerinde yok / text not in probe tokens: {spoken[:40]}")
    ranges, cursor = [], base
    for word in words:
        start = text.index(word, cursor)
        ranges.append((start, start + len(word)))
        cursor = start + len(word)
    owner = np.full(len(tokens), -1, dtype=np.int64)
    for row, span in enumerate(spans):
        if span is None:
            continue
        for index, (start, end) in enumerate(ranges):
            if span[0] < end and span[1] > start:
                owner[row] = index
                break
    return owner


def _monotonic_path(scores: np.ndarray) -> np.ndarray:
    steps, count = scores.shape
    if steps < count:
        raise ValueError(f"yama sayısı ({steps}) kelimeden ({count}) az")
    total = np.full((steps, count), -np.inf)
    advanced = np.zeros((steps, count), dtype=bool)
    total[0, 0] = scores[0, 0]
    for step in range(1, steps):
        stay = total[step - 1]
        advance = np.concatenate([[-np.inf], total[step - 1, :-1]])
        advanced[step] = advance > stay
        total[step] = np.maximum(stay, advance) + scores[step]
    path = np.zeros(steps, dtype=np.int64)
    word = count - 1
    for step in range(steps - 1, -1, -1):
        path[step] = word
        if step and advanced[step, word]:
            word -= 1
    return path


def word_mass(request: dict, pieces: dict, spoken: str, words: list) -> np.ndarray:
    """(yama, kelime): her yamada dikkatin kelimelere düşen payı (satır başına 1'e normlu). / Per-patch attention share per word."""
    owner = _owners(request["tokens"], pieces, spoken, words)
    attention = np.asarray(request["rows"], dtype=np.float64)
    mass = np.zeros((attention.shape[0], len(words)))
    for row, index in enumerate(owner):
        if index >= 0 and row < attention.shape[1]:
            mass[:, index] += attention[:, row]
    return mass / (mass.sum(axis=1, keepdims=True) + 1e-9)


def rough_times(request: dict, pieces: dict, spoken: str, words: list, line_seconds: float) -> list:
    mass = word_mass(request, pieces, spoken, words)
    patches = request["patches"]
    patch_seconds = line_seconds / patches
    first = 1 + LEAD_PATCHES
    scores = np.full((patches, len(words)), np.log(1e-6))
    for row in range(mass.shape[0]):
        if row + first < patches:
            scores[row + first] = np.log(mass[row] + 1e-6)
    scores[:first] = np.log(1e-6)
    scores[:first, 0] = 0.0
    path = _monotonic_path(scores)
    out = []
    for index, word in enumerate(words):
        own = np.flatnonzero(path == index)
        out.append({"kelime": word, "t0": float(own[0] * patch_seconds),
                    "t1": float(min((own[-1] + 1) * patch_seconds, line_seconds))})
    return out


# --- ince ayar: sesin enerjisine oturtma / snap to audio energy ----------------------------------------------------

def highpass(audio: np.ndarray, sample_rate: int, cutoff: float = HIGHPASS_HZ) -> np.ndarray:
    """Sıfır fazlı 4. derece Butterworth yüksek geçiren (ileri-geri uygulanmış genlik: 1/(1+(fc/f)^8)), FFT ile."""
    spectrum = np.fft.rfft(audio.astype(np.float64))
    freq = np.fft.rfftfreq(len(audio), 1.0 / sample_rate)
    with np.errstate(divide="ignore"):
        gain = 1.0 / (1.0 + (cutoff / np.maximum(freq, 1e-9)) ** 8)
    return np.fft.irfft(spectrum * gain, n=len(audio)).astype(np.float32)


def _levels_db(audio: np.ndarray, sample_rate: int) -> np.ndarray:
    size = int(sample_rate * FRAME_SECONDS)
    count = len(audio) // size
    frames = audio[:count * size].astype(np.float64).reshape(count, size)
    return 10 * np.log10((frames ** 2).mean(axis=1) + 1e-12)


def _letters(word: str) -> int:
    return max(1, sum(char.isalnum() for char in word))


def _boundary_cost(levels: np.ndarray, speech_db: float, range_db: float) -> np.ndarray:
    padded = np.concatenate([levels[:1], levels, levels[-1:]])
    smooth = (padded[:-2] + padded[1:-1] + padded[2:]) / 3
    return np.clip((smooth - (speech_db - range_db)) / range_db, 0.0, 1.0)


def _pause_bounds(words: list, voiced: np.ndarray, min_pause: int) -> dict:
    index = np.flatnonzero(voiced)
    forced = {}
    for before, after in zip(index, index[1:]):
        if after - before < min_pause:
            continue
        pause_start = (before + 1) * FRAME_SECONDS
        owner = next((i for i, w in enumerate(words) if w["t0"] <= pause_start < w["t1"]), None)
        if owner is None:
            continue
        word = words[owner]
        # Susma kelimenin ikinci yarısında başlıyorsa kelimenin arkasıdır (önü değil): "balkona çıktım ve" içinde "çıktım"dan
        # sonraki nefes "çıktım"ı 0,8 sn geç başlatıyordu. A pause starting in the word's second half follows the word.
        if not word["kelime"][-1].isalnum() or pause_start - word["t0"] > word["t1"] - pause_start:
            owner += 1
        if 0 < owner < len(words) and owner - 1 not in forced:
            forced[owner - 1] = (before + 1, after)
    return forced


SNAP_PROBE_WEIGHT = 3.0  # sonda sınırına güven (1 → 3: kaba kenar sondayı daha az eziyor; ölçüm deneme_12, LOVO %88,60 → %89,66)


def snap_line(words: list, audio: np.ndarray, sample_rate: int, probe_weight: float = SNAP_PROBE_WEIGHT,
              duration_weight: float = 3.0, energy_weight: float = 3.0, below_speech_db: float = 35.0,
              min_pause_seconds: float = 0.15) -> list:
    """Bir satırın kaba zamanlarını (satır başına göre saniye) sesin enerjisine oturtur."""
    levels = _levels_db(audio, sample_rate)
    levels_v = _levels_db(highpass(audio, sample_rate), sample_rate)
    speech_db = np.percentile(levels, 95)
    voiced = levels_v > np.percentile(levels_v, 95) - below_speech_db
    voiced_index = np.flatnonzero(voiced)
    if voiced_index.size == 0:
        return words
    start, end = int(voiced_index[0]), int(voiced_index[-1]) + 1
    voiced_sum = np.concatenate([[0], np.cumsum(voiced)])
    energy = _boundary_cost(levels, speech_db, 40.0)
    letters = np.array([_letters(w["kelime"]) for w in words], dtype=np.float64)
    expected = letters * voiced_sum[end] / letters.sum()
    probe_bounds = [words[i]["t1"] / FRAME_SECONDS for i in range(len(words) - 1)]
    probe_scale = PATCH_SECONDS / FRAME_SECONDS
    forced = _pause_bounds(words, voiced, int(round(min_pause_seconds / FRAME_SECONDS)))
    frames = end - start + 1
    positions = np.arange(start, end + 1)
    if frames <= len(words):
        return words
    cost = np.full(frames, np.inf)
    cost[0] = 0.0
    back = []
    for index in range(len(words)):
        last = index == len(words) - 1
        new_cost = np.full(frames, np.inf)
        choice = np.zeros(frames, dtype=np.int64)
        for target in ([frames - 1] if last else range(1, frames)):
            previous = np.arange(0, target)
            spoken = voiced_sum[positions[target]] - voiced_sum[positions[previous]]
            total = cost[previous] + duration_weight * np.log((spoken + 1.0) / (expected[index] + 1.0)) ** 2
            best = int(np.argmin(total))
            boundary = 0.0
            if not last:
                distance = abs(positions[target] - probe_bounds[index]) / probe_scale
                boundary = energy_weight * energy[positions[target]] + probe_weight * min(distance, 3.0)
                if index in forced and not forced[index][0] <= positions[target] <= forced[index][1]:
                    boundary = np.inf
            new_cost[target] = total[best] + boundary
            choice[target] = best
        back.append(choice)
        cost = new_cost
    if not np.isfinite(cost[frames - 1]):
        return words
    bounds = [frames - 1]
    for index in range(len(words) - 1, -1, -1):
        bounds.append(int(back[index][bounds[-1]]))
    bounds = [int(positions[b]) for b in reversed(bounds)]
    placed = []
    for index, word in enumerate(words):
        segment = np.flatnonzero(voiced[bounds[index]:bounds[index + 1]])
        a = bounds[index] + (segment[0] if segment.size else 0)
        b = bounds[index] + (segment[-1] + 1 if segment.size else 1)
        placed.append({**word, "t0": round(a * FRAME_SECONDS, 3), "t1": round(b * FRAME_SECONDS, 3)})
    return placed


CORE_DB = 15.0  # çekirdek kenar: kelimenin tepe seviyesinin 15 dB altı (ölçüm: deneme_06 LOVO, %83,0 → %85,4)


def core_edges(words: list, audio: np.ndarray, sample_rate: int, below_peak_db: float = CORE_DB) -> list:
    """Kelime kenarını kelimenin kendi tepesine göre daraltır: [t0, t1) içinde seviyesi (100 Hz altı atılmış) tepe - 15 dB
    üstünde kalan ilk ve son çerçeve. İşitilebilir kenar (-35 dB) kırpmada kalır; gösterilen zaman çekirdek kenardır.
    Narrows each word to frames within 15 dB of its own peak (high-passed); trimming keeps the audible edge."""
    levels = _levels_db(highpass(audio, sample_rate), sample_rate)
    out = []
    for word in words:
        a, b = int(round(word["t0"] / FRAME_SECONDS)), int(round(word["t1"] / FRAME_SECONDS))
        segment = levels[a:b]
        keep = np.flatnonzero(segment > segment.max() - below_peak_db) if segment.size else segment
        if keep.size:
            word = {**word, "t0": round((a + keep[0]) * FRAME_SECONDS, 3), "t1": round((a + keep[-1] + 1) * FRAME_SECONDS, 3)}
        out.append(word)
    return out


def line_words(request: dict, pieces: dict, spoken: str, audio: np.ndarray, sample_rate: int, dil: str = "tr") -> tuple:
    """Bir satırın kelimeleri, satır başına göre saniye: (gösterilecek [{'kelime','t0','t1'}], kırpma kenarları (t0, t1))."""
    words = units(spoken, dil)
    if not words:
        return [], (0.0, len(audio) / sample_rate)
    rough = rough_times(request, pieces, spoken, words, len(audio) / sample_rate)
    audible = snap_line(rough, audio, sample_rate)
    return core_edges(audible, audio, sample_rate), trim_bounds(audible, len(audio) / sample_rate, audio, sample_rate)


# --- birleştirici: kenar adayları arasında seçim / combiner: pick the edge among candidates --------------------------
# Çekirdek kenarın ±160 ms penceresindeki (10 ms adım) her aday için 9 ipucunun doğrusal puanı; en yüksek puanlı aday kenar
# olur. Ağırlıklar bütün seslere aynıdır (sese ya da cümleye özel ayar yok): 12 onaylı ses, 22 okuma, öğretmen CTC ile bir kez
# öğrenildi. Ölçüm (CTC zorlamalı hizalama = %100, ses dışarıda bırakılarak, 6223 kenar): geliştirmedeki ilk hâl %88,48; sonda güveni 3,
# susma düzeltmesi ve satır kuralıyla %89,66 (ort 37,7 ms; 0,5 sn'den büyük kayma 18 → 3, en büyük 1,16 → 0,68 sn).
# Each candidate in a ±160 ms window around the core edge gets a linear score of 9 cues; the best candidate wins.
# Weights are shared by all voices, learned once (12 voices, 22 readings, CTC as teacher).

COMBINER_WINDOW = 16              # aday yarı genişliği, çerçeve (16 x 10 ms) / candidate half-width in frames
COMBINER_GAP = 0.35               # ipuçları satırlar arasına bu kadar sessizlik konarak hesaplanır (öğrenme verisiyle aynı)
COMBINER_LETTER_SECONDS = 0.06    # süre ipucu: harf başına beklenen süre / expected seconds per letter
COMBINER_INTERNAL_GAP = 0.05      # komşu kelimeye bundan kısa boşluk: kelime içi geçiş / below this the edge is a transition
COMBINER_WEIGHTS = {"d2": -0.6247187773936547, "abs_d": -0.409397500489501, "egim": 0.3722002428409541,
                    "tini": 0.11928912848021733, "sure": -0.7577336915093991, "ic*seviye": -0.17517597182213396,
                    "k_bic": 1.353039975703895, "k_bdurak": 0.41866650608017886, "dik": 0.5601866167767763}
_MEL_BANDS, _MEL_FFT = 40, 1024


def _zscore(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / (x.std() + 1e-9)


@lru_cache(maxsize=4)
def _mel_bank(sample_rate: int) -> np.ndarray:
    def to_mel(f):
        return 2595 * np.log10(1 + f / 700)

    def to_hz(m):
        return 700 * (10 ** (m / 2595) - 1)
    points = to_hz(np.linspace(to_mel(80.0), to_mel(8000.0), _MEL_BANDS + 2))
    bins = np.floor((_MEL_FFT + 1) * points / sample_rate).astype(int)
    bank = np.zeros((_MEL_BANDS, _MEL_FFT // 2 + 1))
    for i in range(_MEL_BANDS):
        a, b, c = bins[i], bins[i + 1], bins[i + 2]
        if b > a:
            bank[i, a:b] = (np.arange(a, b) - a) / (b - a)
        if c > b:
            bank[i, b:c] = (c - np.arange(b, c)) / (c - b)
    return bank


def _cues(audio: np.ndarray, sample_rate: int) -> dict:
    """10 ms çerçeve: seviye (dB, 100 Hz altı atılmış) ve tını değişimi (log-mel, önceki 4 / sonraki 4 çerçeve kosinüs)."""
    hp = highpass(audio, sample_rate)
    hop = int(sample_rate * FRAME_SECONDS)
    count = len(hp) // hop
    levels = _levels_db(hp, sample_rate)[:count]
    window = np.hanning(_MEL_FFT)
    padded = np.pad(hp.astype(np.float64), (0, _MEL_FFT))
    index = np.arange(count)[:, None] * hop + np.arange(_MEL_FFT)[None, :]
    power = np.abs(np.fft.rfft(padded[index] * window, axis=1)) ** 2
    mel = np.log(power @ _mel_bank(sample_rate).T + 1e-10)
    mel = mel - mel.mean(axis=0, keepdims=True)
    timbre = np.empty(count)
    for f in range(count):
        a = mel[max(0, f - 4):f].mean(axis=0) if f > 0 else mel[0]
        b = mel[f:f + 4].mean(axis=0)
        timbre[f] = 1 - float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
    return {"L": levels, "tini": timbre, "n": count, "ref": float(np.percentile(levels, 95))}


LINE_SILENCE_DB = 30.0       # satır kuralı: okumanın tepe seviyesinin (p95) bu kadar altı susmadır
LINE_SILENCE_SECONDS = 0.3   # satır kuralı: kelimenin içinde bundan uzun susma olamaz


def _silences(quiet: np.ndarray, minimum: int) -> list:
    runs, f = [], 0
    while f < len(quiet):
        if quiet[f]:
            g = f
            while g < len(quiet) and quiet[g]:
                g += 1
            if g - f >= minimum:
                runs.append((f, g))
            f = g
        else:
            f += 1
    return runs


def _line_silence(words: list, picked: dict, levels: np.ndarray, ref: float) -> None:
    """Satır kuralı: kelimenin içinde uzun susma olmaz. Satırın son kelimesi içindeki ilk susmanın başında biter, ilk kelimesi
    içindeki son susmanın sonunda başlar (satır sonundaki nefes/tık kelimeyi 1 sn uzatıyordu; ölçüm deneme_12 %88,48 → %88,60).
    Line rule: no long silence inside a word; the line's last word ends at the silence, its first word starts after it."""
    FR = FRAME_SECONDS
    minimum = int(round(LINE_SILENCE_SECONDS / FR))
    for i, w in enumerate(words):
        if (i, "b") not in picked or (i, "s") not in picked:
            continue
        last = i == len(words) - 1 or words[i + 1]["satir"] != w["satir"]
        first = i == 0 or words[i - 1]["satir"] != w["satir"]
        if not (last or first):
            continue
        f0, f1 = int(picked[(i, "b")] / FR), int(picked[(i, "s")] / FR)
        runs = _silences(levels[f0:f1] < ref - LINE_SILENCE_DB, minimum) if f1 - f0 > minimum else []
        if not runs:
            continue
        if last:
            picked[(i, "s")] = (f0 + runs[0][0]) * FR
        else:
            picked[(i, "b")] = (f0 + runs[-1][1]) * FR


def combine_reading(lines: list, sample_rate: int) -> list:
    """Bütün okumanın çekirdek kenarlarını birleştiriciyle yeniden seçer. lines: her satır için
    {"words": çekirdek kelimeler (satır başına göre sn), "mass": word_mass, "patches", "audio"}. Dönüş: satır başına kelimeler.
    Re-picks every core edge of a reading with the combiner; returns per-line words (seconds from line start)."""
    W, FR = COMBINER_WINDOW, FRAME_SECONDS
    parts, starts, first_word, cursor, words = [], [], [], 0.0, []
    for number, line in enumerate(lines):
        starts.append(cursor)
        first_word.append(len(words))
        words += [{"kelime": w["kelime"], "t0": w["t0"] + cursor, "t1": w["t1"] + cursor, "satir": number} for w in line["words"]]
        parts.append(np.asarray(line["audio"], dtype=np.float32))
        cursor += len(line["audio"]) / sample_rate
        if number < len(lines) - 1:
            parts.append(np.zeros(int(COMBINER_GAP * sample_rate), dtype=np.float32))
            cursor += COMBINER_GAP
    if not words:
        return [list(line["words"]) for line in lines]
    cue = _cues(np.concatenate(parts), sample_rate)
    L, n = cue["L"], cue["n"]
    ks = np.arange(-W, W + 1)
    picked = {}
    for i, w in enumerate(words):
        prev_t1 = words[i - 1]["t1"] if i > 0 else -9.0
        next_t0 = words[i + 1]["t0"] if i + 1 < len(words) else 9e3
        letters = max(1, sum(c.isalnum() for c in w["kelime"]))
        line = lines[w["satir"]]
        for kind in ("b", "s"):
            current = w["t0"] if kind == "b" else w["t1"]
            fc = int(round(current / FR))
            if fc < 4 or fc > n - W - 6:
                continue
            internal = 1.0 if ((w["t0"] - prev_t1 < COMBINER_INTERNAL_GAP) if kind == "b"
                               else (next_t0 - w["t1"] < COMBINER_INTERNAL_GAP)) else 0.0
            fs = np.clip(fc + ks, 0, n - 1)
            sign = 1.0 if kind == "b" else -1.0
            level = (L[fs] - cue["ref"]) / 20.0
            slope = sign * (L[np.clip(fs + 3, 0, n - 1)] - L[np.clip(fs - 3, 0, n - 1)])
            dur = np.maximum((fs * FR - w["t0"]) if kind == "s" else (w["t1"] - fs * FR), 0.02)
            prior = np.log(dur / (letters * COMBINER_LETTER_SECONDS)) ** 2
            shift = np.zeros(len(ks))
            mass, local = line["mass"], i - first_word[w["satir"]]
            prev_w, next_w = (local, local + 1) if kind == "s" else (local - 1, local)
            if 0 <= prev_w and next_w < mass.shape[1]:
                patch_seconds = (len(line["audio"]) / sample_rate) / line["patches"]
                start = starts[w["satir"]]

                def handover(t):
                    rf = (t - start) / patch_seconds - (1 + LEAD_PATCHES) - 0.5
                    rf = min(max(rf, 0), mass.shape[0] - 1)
                    a0 = int(rf)
                    a1 = min(a0 + 1, mass.shape[0] - 1)
                    frac = rf - a0
                    mm = (1 - frac) * mass[a0] + frac * mass[a1]
                    return mm[next_w] - mm[prev_w]
                shift = -np.abs(np.array([handover(f * FR) for f in fs]))
            begin = 1.0 if kind == "b" else 0.0
            phi = {"d2": (ks / W) ** 2, "abs_d": np.abs(ks) / W, "egim": _zscore(slope), "tini": _zscore(cue["tini"][fs]),
                   "sure": _zscore(prior), "ic*seviye": internal * _zscore(level), "k_bic": begin * internal * ks / W,
                   "k_bdurak": begin * (1 - internal) * ks / W, "dik": _zscore(shift)}
            score = sum(COMBINER_WEIGHTS[name] * phi[name] for name in COMBINER_WEIGHTS)
            picked[(i, kind)] = (fc + ks[int(np.argmax(score))]) * FR
    for i in range(len(words) - 1):  # çakışma onarımı: komşular çakışırsa ikisi ortaya / overlapping neighbours meet halfway
        a, b = (i, "s"), (i + 1, "b")
        if a in picked and b in picked and picked[a] > picked[b]:
            picked[a] = picked[b] = 0.5 * (picked[a] + picked[b])
    _line_silence(words, picked, L, cue["ref"])
    out = [[] for _ in lines]
    for i, w in enumerate(words):
        start = starts[w["satir"]]
        t0 = picked.get((i, "b"), w["t0"]) - start
        t1 = picked.get((i, "s"), w["t1"]) - start
        out[w["satir"]].append({"kelime": w["kelime"], "t0": round(t0, 3), "t1": round(t1, 3)})
    return out


def reading_words(requests: list, pieces: dict, spokens: list, audios: list, sample_rate: int, dil: str = "tr") -> list:
    """Bütün okuma: satır başına (kelimeler, kırpma kenarları). Kırpma işitilebilir kenarla, gösterilen zaman birleştiriciyle.
    Whole reading: per line (words, trim bounds); trimming uses the audible edge, shown times come from the combiner."""
    lines, bounds = [], []
    for request, spoken, audio in zip(requests, spokens, audios):
        words = units(spoken, dil)
        seconds = len(audio) / sample_rate
        if not words:
            lines.append({"words": [], "mass": np.zeros((1, 1)), "patches": 1, "audio": audio})
            bounds.append((0.0, seconds))
            continue
        audible = snap_line(rough_times(request, pieces, spoken, words, seconds), audio, sample_rate)
        lines.append({"words": core_edges(audible, audio, sample_rate), "mass": word_mass(request, pieces, spoken, words),
                      "patches": request["patches"], "audio": audio})
        bounds.append(trim_bounds(audible, seconds, audio, sample_rate))
    return list(zip(combine_reading(lines, sample_rate), bounds))


# --- satır kırpma: satır arası tam ayar kadar / trim lines so the gap equals the setting ---------------------------

TRIM_PAD = 0.04      # ilk kelimeden önce ve son kelimeden sonra bırakılan pay (sn)
TRIM_FADE = 0.008    # kesim yerinde yumuşak giriş/çıkış (sn)


def trim_bounds(words: list, line_seconds: float, audio: np.ndarray = None, sample_rate: int = 0) -> tuple:
    """Satırın tutulacak aralığı (sn): ilk kelime - pay, son kelime + pay. Ses verilirse satır kuralı kırpmaya da uygulanır:
    ilk/son kelimenin içinde uzun susma varsa ötesindeki nefes/tık kırpılır (kelime zamanıyla aynı kural)."""
    if not words:
        return 0.0, line_seconds
    t0, t1 = words[0]["t0"], words[-1]["t1"]
    if audio is not None and sample_rate:
        levels = _levels_db(highpass(audio, sample_rate), sample_rate)
        picked = {(0, "b"): words[0]["t0"], (0, "s"): words[0]["t1"]}
        line = [{"satir": 0}] * len(words)
        if len(words) > 1:
            picked.update({(len(words) - 1, "b"): words[-1]["t0"], (len(words) - 1, "s"): words[-1]["t1"]})
        _line_silence(line, picked, levels, float(np.percentile(levels, 95)))
        t0, t1 = picked[(0, "b")], picked[(len(words) - 1, "s")]
    return max(0.0, t0 - TRIM_PAD), min(line_seconds, t1 + TRIM_PAD)


def trim(audio: np.ndarray, sample_rate: int, start: float, end: float) -> np.ndarray:
    piece = audio[int(start * sample_rate):int(end * sample_rate)].copy()
    fade = min(int(TRIM_FADE * sample_rate), len(piece) // 2)
    if fade:
        piece[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
        piece[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
    return piece

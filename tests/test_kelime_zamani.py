"""Kelime zamanı (motor içi sonda) ve satır kırpma. / Word timing from the engine probe and line trimming."""
import json
import struct
import tempfile
import unittest
from pathlib import Path

import numpy as np

from ses_tasarim import kelime_zamani as kz
from ses_tasarim import oku

SR = 48000


def _gguf(path: Path, files: dict) -> None:
    """Yalnız üst veriden oluşan küçük bir audio.cpp .gguf (gömülü dosyalarla). / Tiny metadata-only gguf."""
    def s(b):
        return struct.pack("<Q", len(b)) + b
    names = list(files)
    data, offsets = b"", []
    for name in names:
        offsets.append(len(data))
        data += files[name]
    kv = [(b"general.architecture", 8, s(b"audiocpp")),
          (b"audiocpp.embedded_files.names", 9, struct.pack("<IQ", 8, len(names)) + b"".join(s(n.encode()) for n in names)),
          (b"audiocpp.embedded_files.offsets", 9, struct.pack("<IQ", 10, len(offsets)) + struct.pack(f"<{len(offsets)}Q", *offsets)),
          (b"audiocpp.embedded_files.data", 9, struct.pack("<IQ", 0, len(data)) + data)]
    body = b"GGUF" + struct.pack("<IQQ", 3, 0, len(kv))
    for key, kind, value in kv:
        body += s(key) + struct.pack("<I", kind) + value
    path.write_bytes(body)


TOKENIZER = {"model": {"vocab": {"▁Merhaba": 5, "▁dünya": 6, ".": 7, "<s>": 1, "▁Bir": 8, "▁iki": 9}},
             "added_tokens": [{"id": 1, "content": "<s>"}]}


def _burst(seconds: list, total: float) -> np.ndarray:
    """Sessizlik içinde verilen aralıklarda 220 Hz ton (kelime yerine). / Tone bursts standing in for words."""
    audio = np.zeros(int(total * SR), dtype=np.float32)
    for a, b in seconds:
        t = np.arange(int(a * SR), int(b * SR))
        audio[t] = 0.3 * np.sin(2 * np.pi * 220 * t / SR)
    return audio


class Sozluk(unittest.TestCase):
    def test_gguf_icindeki_tokenizer_okunur(self):
        with tempfile.TemporaryDirectory() as tmp:
            model = Path(tmp) / "m.gguf"
            _gguf(model, {"README.md": b"x", "tokenizer.json": json.dumps(TOKENIZER).encode()})
            pieces = kz.load_pieces(model)
            self.assertEqual(pieces[5], "▁Merhaba")
            self.assertEqual(pieces[1], "")  # eklenen belirteç metne girmez / added tokens carry no text

    def test_gguf_degilse_hata(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "x.gguf"
            bad.write_bytes(b"NOPE" + b"\0" * 32)
            with self.assertRaises(ValueError):
                kz.load_pieces(bad)


class Birimler(unittest.TestCase):
    def test_bosluklu_dil_kelime(self):
        self.assertEqual(kz.units("Merhaba dünya.", "tr"), ["Merhaba", "dünya."])

    def test_cince_japonca_karakter_noktalama_yapisik(self):
        self.assertEqual(kz.units("你好，世界。", "zh"), ["你", "好，", "世", "界。"])
        self.assertEqual(kz.units("こんにちは。", "ja"), ["こ", "ん", "に", "ち", "は。"])


class Log(unittest.TestCase):
    def _log(self, text):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".log", delete=False, encoding="utf-8")
        tmp.write(text)
        tmp.close()
        return Path(tmp.name)

    def test_istek_bloklari_ve_yeniden_deneme(self):
        log = self._log("\n".join([
            "voxcpm2.probe.prefill_tokens [1,5]", "voxcpm2.probe.attention_rows [[0.1,0.9]]",
            # aynı blokta yeniden deneme: son deneme geçerli / a retry inside the block wins
            "voxcpm2.probe.prefill_tokens [1,5,6]", "voxcpm2.probe.attention_rows [[0.2,0.3,0.5]]",
            "voxcpm2.probe.ar_patch 4", "voxcpm2.probe.eos_accepted_at_patch 4", "voxcpm2.toplu_coz.deferred 1",
            "voxcpm2.probe.prefill_tokens [1,8,9]", "voxcpm2.probe.ar_patch 3", "voxcpm2.toplu_coz.deferred 2", ""]))
        requests = kz.parse_log(log)
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]["tokens"], [1, 5, 6])
        self.assertEqual(requests[0]["rows"], [[0.2, 0.3, 0.5]])
        self.assertEqual(requests[0]["patches"], 4)
        self.assertEqual(requests[1]["rows"], [])

    def test_sondasiz_motor_bos_istek(self):
        requests = kz.parse_log(self._log("voxcpm2.toplu_coz.deferred 1\nvoxcpm2.toplu_coz.deferred 2\n"))
        self.assertEqual(requests, [None, None])


class InceAyar(unittest.TestCase):
    def test_kelimeler_sese_oturur(self):
        # iki "kelime": 0,30-0,80 ve 1,10-1,60 sn; kaba zaman 160 ms kaymış / rough bounds off by a patch
        audio = _burst([(0.30, 0.80), (1.10, 1.60)], 2.0)
        rough = [{"kelime": "Merhaba", "t0": 0.16, "t1": 0.96}, {"kelime": "dünya.", "t0": 0.96, "t1": 1.76}]
        placed = kz.snap_line(rough, audio, SR)
        self.assertAlmostEqual(placed[0]["t0"], 0.30, delta=0.03)
        self.assertAlmostEqual(placed[0]["t1"], 0.80, delta=0.03)
        self.assertAlmostEqual(placed[1]["t0"], 1.10, delta=0.03)
        self.assertAlmostEqual(placed[1]["t1"], 1.60, delta=0.03)

    def test_100hz_ugultu_konusma_sayilmaz(self):
        audio = _burst([(0.30, 0.80), (1.10, 1.60)], 2.0)
        t = np.arange(len(audio))
        audio += (0.01 * np.sin(2 * np.pi * 50 * t / SR)).astype(np.float32)  # şebeke uğultusu / mains hum
        rough = [{"kelime": "Merhaba", "t0": 0.16, "t1": 0.96}, {"kelime": "dünya.", "t0": 0.96, "t1": 1.76}]
        placed = kz.snap_line(rough, audio, SR)
        self.assertAlmostEqual(placed[0]["t0"], 0.30, delta=0.03)
        self.assertAlmostEqual(placed[1]["t1"], 1.60, delta=0.03)

    def test_cekirdek_kenar_sessiz_uclari_atar(self):
        # kelime: 0,30-0,40 sn fısıltı (-30 dB), 0,40-0,80 sn tam ses; çekirdek kenar tam sesin başı
        audio = _burst([(0.40, 0.80)], 1.0)
        t = np.arange(int(0.30 * SR), int(0.40 * SR))
        audio[t] = 0.3 * 10 ** (-30 / 20) * np.sin(2 * np.pi * 220 * t / SR)
        core = kz.core_edges([{"kelime": "a", "t0": 0.30, "t1": 0.80}], audio, SR)
        self.assertAlmostEqual(core[0]["t0"], 0.40, delta=0.02)
        self.assertAlmostEqual(core[0]["t1"], 0.80, delta=0.02)

    def test_kirpma_isitilebilir_kenara_gore(self):
        # gösterilen (çekirdek) dar, kırpma kenarı geniş: fısıltı kesilmez / trimming keeps the quiet part
        audio = _burst([(0.40, 0.80)], 1.2)
        t = np.arange(int(0.30 * SR), int(0.40 * SR))
        audio[t] = 0.3 * 10 ** (-30 / 20) * np.sin(2 * np.pi * 220 * t / SR)
        rough = [{"kelime": "a", "t0": 0.16, "t1": 0.96}]
        audible = kz.snap_line(rough, audio, SR)
        core = kz.core_edges(audible, audio, SR)
        self.assertLessEqual(audible[0]["t0"], 0.31)
        self.assertGreaterEqual(core[0]["t0"], 0.38)

    def test_yuksek_geciren_dusuk_frekansi_atar(self):
        t = np.arange(SR) / SR
        low, high = np.sin(2 * np.pi * 40 * t), np.sin(2 * np.pi * 400 * t)
        self.assertLess(np.std(kz.highpass(low.astype(np.float32), SR)), 0.05)
        self.assertGreater(np.std(kz.highpass(high.astype(np.float32), SR)), 0.69)


class Birlestirici(unittest.TestCase):
    def _line(self, spans, total):
        audio = _burst(spans, total)
        words = [{"kelime": f"k{i}", "t0": a, "t1": b} for i, (a, b) in enumerate(spans)]
        mass = np.tile(np.eye(len(spans))[None], (1, 1, 1))[0].repeat(int(total / 0.16) // len(spans) + 1, axis=0)
        return {"words": words, "mass": mass, "patches": int(round(total / 0.16)), "audio": audio}

    def test_kelime_sayisi_ve_sira_korunur(self):
        lines = [self._line([(0.30, 0.80), (1.10, 1.60)], 2.08), self._line([(0.20, 0.70)], 1.12)]
        out = kz.combine_reading(lines, SR)
        self.assertEqual([len(x) for x in out], [2, 1])
        for words in out:
            for w in words:
                self.assertLess(w["t0"], w["t1"])
                self.assertLessEqual(abs(w["t0"] - 0.0), 3.0)

    def test_kenar_pencereden_cikmaz(self):
        lines = [self._line([(0.30, 0.80), (1.10, 1.60)], 2.08)]
        out = kz.combine_reading(lines, SR)[0]
        for got, base in zip(out, lines[0]["words"]):
            self.assertLessEqual(abs(got["t0"] - base["t0"]), kz.COMBINER_WINDOW * kz.FRAME_SECONDS + 1e-6)
            self.assertLessEqual(abs(got["t1"] - base["t1"]), kz.COMBINER_WINDOW * kz.FRAME_SECONDS + 1e-6)

    def test_bitisik_kelimeler_cakismaz(self):
        lines = [self._line([(0.30, 0.70), (0.70, 1.10), (1.10, 1.60)], 2.08)]
        out = kz.combine_reading(lines, SR)[0]
        for a, b in zip(out, out[1:]):
            self.assertLessEqual(a["t1"], b["t0"] + 1e-9)

    def test_agirliklar_dokuz_ipucu(self):
        self.assertEqual(len(kz.COMBINER_WEIGHTS), 9)


class SusmaVeSatir(unittest.TestCase):
    WORDS = [{"kelime": "balkona", "t0": 0.0, "t1": 0.5}, {"kelime": "çıktım", "t0": 0.5, "t1": 1.0},
             {"kelime": "ve", "t0": 1.0, "t1": 1.2}]

    def test_kelimenin_sonunda_baslayan_susma_arkasina(self):
        voiced = np.zeros(130, dtype=bool)
        voiced[:90] = True
        voiced[110:] = True                       # susma 0,90 sn'de, "çıktım"ın ikinci yarısında
        self.assertEqual(kz._pause_bounds(self.WORDS, voiced, 15), {1: (90, 110)})

    def test_kelimenin_basinda_baslayan_susma_onune(self):
        voiced = np.zeros(130, dtype=bool)
        voiced[:55] = True
        voiced[75:] = True                        # susma 0,55 sn'de, "çıktım"ın ilk yarısında
        self.assertEqual(kz._pause_bounds(self.WORDS, voiced, 15), {0: (55, 75)})

    def test_satir_sonu_kelimesi_susmada_biter(self):
        levels = np.full(150, -10.0)
        levels[100:140] = -80.0                   # 0,4 sn susma, sonra kısa tık / 0.4 s silence then a click
        words = [{"kelime": "a", "satir": 0}, {"kelime": "b", "satir": 0}]
        picked = {(0, "b"): 0.0, (0, "s"): 0.5, (1, "b"): 0.5, (1, "s"): 1.45}
        kz._line_silence(words, picked, levels, -10.0)
        self.assertAlmostEqual(picked[(1, "s")], 1.0)
        self.assertEqual(picked[(0, "s")], 0.5)   # satır ortası kenara dokunulmaz / mid-line edge untouched

    def test_kisa_susma_kelimeyi_bolmez(self):
        levels = np.full(150, -10.0)
        levels[100:120] = -80.0                   # 0,2 sn: kural için kısa / too short for the rule
        words = [{"kelime": "a", "satir": 0}]
        picked = {(0, "b"): 0.0, (0, "s"): 1.45}
        kz._line_silence(words, picked, levels, -10.0)
        self.assertEqual(picked[(0, "s")], 1.45)


class Kirpma(unittest.TestCase):
    def test_satir_arasi_tam_durak(self):
        words = [{"kelime": "a", "t0": 0.50, "t1": 1.00}]
        a, b = kz.trim_bounds(words, 1.6)
        self.assertAlmostEqual(a, 0.50 - kz.TRIM_PAD)
        self.assertAlmostEqual(b, 1.00 + kz.TRIM_PAD)
        piece = kz.trim(np.ones(int(1.6 * SR), dtype=np.float32), SR, a, b)
        self.assertEqual(len(piece), int(b * SR) - int(a * SR))
        self.assertEqual(piece[0], 0.0)  # yumuşak giriş / fade in
        # iki satır: kırpılmış uçların arasındaki boşluk + iki pay = durak / gap + 2 pads = pause
        self.assertAlmostEqual(max(0.0, 0.35 - 2 * kz.TRIM_PAD) + 2 * kz.TRIM_PAD, 0.35)

    def test_kelime_yoksa_satir_aynen(self):
        self.assertEqual(kz.trim_bounds([], 2.0), (0.0, 2.0))

    def test_satir_sonundaki_tik_kirpilir(self):
        audio = _burst([(0.5, 1.0), (1.5, 1.52)], 2.0)  # kelime + 0,5 sn sonra tık / word + click after 0.5 s
        words = [{"kelime": "a", "t0": 0.5, "t1": 1.52}]
        self.assertAlmostEqual(kz.trim_bounds(words, 2.0)[1], 1.52 + kz.TRIM_PAD)
        self.assertAlmostEqual(kz.trim_bounds(words, 2.0, audio, SR)[1], 1.0 + kz.TRIM_PAD, delta=0.02)


class OkumaYanUrun(unittest.TestCase):
    def test_sonda_yoksa_okuma_eskisi_gibi(self):
        timed, error = oku.line_word_times({"model": "yok.gguf"}, [None], ["Merhaba."], [np.zeros(SR)], "tr")
        self.assertIsNone(timed)
        self.assertIn("sonda", error)

    def test_ayar_kapali(self):
        self.assertEqual(oku.line_word_times({"kelime_zamani": False}, None, [], [], "tr"), (None, None))

    def test_cozulemezse_hata_metni_okuma_dusmez(self):
        probe = {"tokens": [1, 8, 9], "rows": [[0.1, 0.5, 0.4]], "patches": 6}
        timed, error = oku.line_word_times({"model": "yok.gguf"}, [probe], ["Merhaba."], [np.zeros(SR)], "tr")
        self.assertIsNone(timed)
        self.assertIn("çözülemedi", error)


if __name__ == "__main__":
    unittest.main()

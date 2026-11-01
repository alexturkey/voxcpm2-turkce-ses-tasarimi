"""Uzun işin süre tahmini: her bitişte ölçüm yazılır, sonraki iş bu makinedeki ölçümlerden tahmin edilir.
Duration estimate for long jobs: every finished job is measured, the next one is estimated from this machine's history.

Model: süre = açılış (motor ve model yükleme) + karakter × sn/karakter; iki değer iş türüne göre (tasarla, oku)
üstel ortalamayla güncellenir (yeni ölçüm %30). Açılış, ilk ve son ilerleme bildirimi arasındaki hızdan ayrılır.
Okumada sesin kendi katsayısı da öğrenilir (yavaş konuşan ses daha uzun sürer): tahmin × sesin ölçülen/beklenen oranı.
Tahminden iki kat sapan ölçüm (başka iş GPU'yu tutmuş gibi) üç ölçümden sonra ortalamaya girmez; art arda üç aykırı
ölçüm gelirse makine ya da ayar değişmiş sayılır, model son ölçümle yeniden kurulur. Tür anahtarı arka ucu da taşır (oku:cuda).
Dosya kullanıcının önbellek klasöründe (repoya girmez); yoksa ya da bozuksa ölçülmüş varsayılanla başlanır.
Model: duration = start-up + characters × s/char, per job kind, exponential average; outliers skipped after 3 runs.
"""
import json
import os
from pathlib import Path

# GTX 1050 Ti, 16 adım, cfg 2.0: üç okuma 224 kr 85 sn, 1100 kr 197 sn, 2034 kr 466 sn / three measured readings
VARSAYILAN = {"acilis": 35.0, "sn_karakter": 0.2, "n": 0, "aykiri": 0}
ALFA = 0.3


def karakter(metin: str, kat: int = 1) -> int:
    """Okunacak karakter (boşluksuz) × kaç kez okunacağı (tasarlada çeşit sayısı). / spoken characters × repeats"""
    return len("".join(str(metin or "").split())) * max(1, int(kat or 1))


def _yol(settings) -> Path:
    return Path(settings["onbellek"]) / "sure_olcumu.json"


def _oku(settings) -> dict:
    try:
        veri = json.loads(_yol(settings).read_text(encoding="utf-8"))
        return veri if isinstance(veri, dict) else {}
    except (OSError, ValueError):
        return {}


def _model(veri: dict, tur: str) -> dict:
    m = veri.get(tur)
    if not isinstance(m, dict):
        return dict(VARSAYILAN)
    try:
        return {"acilis": max(0.0, float(m["acilis"])), "sn_karakter": max(0.0, float(m["sn_karakter"])), "n": int(m.get("n", 0)),
                "aykiri": int(m.get("aykiri", 0))}
    except (KeyError, TypeError, ValueError):
        return dict(VARSAYILAN)


def _carpan(veri: dict, ses) -> float:
    try:
        return min(3.0, max(0.3, float(veri.get("ses", {}).get(ses, 1.0)))) if ses else 1.0
    except (TypeError, ValueError, AttributeError):
        return 1.0


def tahmin(settings, tur: str, kr: int, ses: str = None) -> dict:
    """{"sn": tahmini toplam süre, "n": kaç ölçüme dayandığı (0 = varsayılan)}; ses verilirse onun katsayısıyla.
    Estimated seconds and sample count; scaled by the voice's own factor when known."""
    veri = _oku(settings)
    m = _model(veri, tur)
    return {"sn": round((m["acilis"] + kr * m["sn_karakter"]) * _carpan(veri, ses), 1), "n": m["n"]}


def kaydet(settings, tur: str, kr: int, adimlar: list, son: float, ses: str = None) -> bool:
    """adimlar: işin ilerleme bildirimleri [(biten, toplam, geçen sn), ...] (motor 3 sn'de bir yazar, biten 0 da olur);
    son: işin baştan sona gerçek süresi. Güncellendiyse True.
    adimlar: progress reports (polled every 3 s, may report 0 done); son: the job's real duration. True when updated."""
    if kr <= 0 or not son or son <= 0:
        return False
    veri = _oku(settings)
    m = _model(veri, tur)
    taban = m["acilis"] + kr * m["sn_karakter"]
    beklenen = taban * _carpan(veri, ses)
    yeniden = False
    if m["n"] >= 3 and not beklenen / 2 <= son <= beklenen * 2:
        if m["aykiri"] + 1 < 3:  # aykırı ölçüm atlanır, sayılır / an outlier is skipped and counted
            veri[tur] = {**{k: m[k] for k in ("acilis", "sn_karakter", "n")}, "aykiri": m["aykiri"] + 1}
            _yaz(settings, veri)
            return False
        yeniden = True  # art arda üçüncü: model bu ölçümle yeniden kurulur / third in a row: rebuild
    # İlk parçanın bittiği görülen an: o ana kadar açılış + k parça, sonrası (toplam-k) parça. Parça başına ortalama karakter.
    # The first time a part is seen done: start-up + k parts before it, (total-k) parts after it.
    ilk = next(((int(b), int(t), float(sn)) for b, t, sn in adimlar if int(b) >= 1), None)
    if ilk and ilk[1] > ilk[0] and son > ilk[2]:
        b, toplam, t1 = ilk
        hiz = (son - t1) / (kr * (toplam - b) / toplam)
        acilis = max(0.0, t1 - hiz * kr * b / toplam)
    else:
        acilis = m["acilis"]
        hiz = max(0.0, son - acilis) / kr
    a = ALFA if m["n"] and not yeniden else 1.0  # ilk (ya da yeniden kurulan) ölçüm eskisinin yerine geçer
    veri[tur] = {"acilis": round((1 - a) * m["acilis"] + a * acilis, 2),
                 "sn_karakter": round((1 - a) * m["sn_karakter"] + a * hiz, 4), "n": 1 if yeniden else m["n"] + 1, "aykiri": 0}
    if ses and m["n"]:  # sesin katsayısı: bu ses genel modele göre ne kadar uzun sürüyor / the voice's own factor
        if not isinstance(veri.get("ses"), dict):
            veri["ses"] = {}
        sesler = veri["ses"]
        oran = min(3.0, max(0.3, son / taban))
        sesler[ses] = round((1 - ALFA) * _carpan(veri, ses) + ALFA * oran if ses in sesler else oran, 3)
    return _yaz(settings, veri)


def _yaz(settings, veri: dict) -> bool:
    yol = _yol(settings)
    try:
        yol.parent.mkdir(parents=True, exist_ok=True)
        gecici = yol.with_suffix(".tmp")
        gecici.write_text(json.dumps(veri, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(gecici, yol)
    except OSError:
        return False
    return True

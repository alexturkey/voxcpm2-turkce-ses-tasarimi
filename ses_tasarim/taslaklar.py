"""Taslaklar: önceden hazırlanan okuma metinleri (satır = cümle, bekleme '|| sn' işaretiyle), adıyla.
Drafts: prepared reading texts (line = sentence, pauses as '|| s' markers), with a name.

Kullanıcı verisidir: `<sesler>/taslaklar.json` (git dışı). Arayüzde iki defter yerinde (Bu sesle oku, Duymak istediğin
metin penceresi) aynı liste. İşlemler: ekle, guncelle (metni üzerine yaz), ad, sil; her biri güncel listeyi döner.
User data in the voices folder (outside git); the same list in both notebook places of the UI.
"""
import json
import os
import secrets
import threading
import time
from pathlib import Path

DOSYA = "taslaklar.json"
SURUM = 1
EN_COK = 200           # taslak tavanı / draft cap
AD_EN_UZUN = 60        # karakter / characters
METIN_EN_UZUN = 20000  # karakter / characters
_KILIT = threading.Lock()  # sunucu çok iş parçacıklı / the server is multi-threaded


def yol(settings: dict) -> Path:
    return Path(settings["sesler"]) / DOSYA


def _ham(path: Path) -> list:
    """Dosyadaki geçerli taslaklar; dosya yok ya da bozuksa boş liste. / valid drafts; empty if missing or corrupt"""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    items = data.get("taslaklar") if isinstance(data, dict) else None
    return [item for item in items if isinstance(item, dict) and all(isinstance(item.get(k), str) for k in ("id", "ad", "metin"))] \
        if isinstance(items, list) else []


def oku(settings: dict) -> list:
    with _KILIT:
        return _ham(yol(settings))


def _yaz(path: Path, items: list) -> None:
    """Önce geçici dosya, sonra yer değiştirme: yarım yazım dosyayı bozmaz. / atomic write"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps({"surum": SURUM, "taslaklar": items}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _ad(ad) -> str:
    ad = " ".join(str(ad or "").split())
    if not ad or len(ad) > AD_EN_UZUN:
        raise ValueError(f"taslak adı 1-{AD_EN_UZUN} karakter olmalı / draft name must be 1-{AD_EN_UZUN} characters")
    return ad


def _metin(metin) -> str:
    metin = str(metin or "").replace("\r\n", "\n").strip()
    if not metin or len(metin) > METIN_EN_UZUN:
        raise ValueError(f"taslak metni 1-{METIN_EN_UZUN} karakter olmalı / draft text must be 1-{METIN_EN_UZUN} characters")
    return metin


def degistir(settings: dict, islem: str, kimlik: str = None, ad: str = None, metin: str = None) -> list:
    """ekle (ad + metin, en üste), guncelle (kimlik + metin), ad (kimlik + ad), sil (kimlik). Güncel listeyi döner.
    add (to the top), update text, rename, delete; returns the updated list."""
    with _KILIT:
        path = yol(settings)
        items = _ham(path)
        tarih = time.strftime("%Y-%m-%d %H:%M")
        if islem == "ekle":
            if len(items) >= EN_COK:
                raise ValueError(f"en çok {EN_COK} taslak / at most {EN_COK} drafts")
            items.insert(0, {"id": secrets.token_hex(6), "ad": _ad(ad), "metin": _metin(metin), "tarih": tarih})
        else:
            found = next((item for item in items if item["id"] == kimlik), None)
            if found is None:
                raise ValueError("taslak bulunamadı / draft not found")
            if islem == "guncelle":
                found.update(metin=_metin(metin), tarih=tarih)
            elif islem == "ad":
                found["ad"] = _ad(ad)
            elif islem == "sil":
                items.remove(found)
            else:
                raise ValueError(f"bilinmeyen işlem: {islem}")
        _yaz(path, items)
        return items

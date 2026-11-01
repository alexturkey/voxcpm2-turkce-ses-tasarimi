"""Okuma listesi: kişinin "Okuma listeme ekle" dediği seslerin kimlikleri, eklenme sırasıyla.
Reading list: identities of the voices the user added with "Add to my reading list", in the order added.

Kullanıcı verisidir: `<sesler>/okuma_listesi.json` (tasarlanan seslerin klasörü, git dışı); hazır seslerin klasörüne
asla yazılmaz. Ses kopyalanmaz: kimlik ('hazir/<ad>' ya da '<ad>/<çeşit>') sesin klasörünü, yani referansını ve
tohumunu gösterir. Klasörü silinen ses dosyada kalır ama arayüze verilmez (geri gelirse yine görünür).
User data in the designed-voices folder (outside git); never written into the bundled voices. Nothing is copied: the
identity points at the voice folder (reference + seed). A deleted voice stays in the file but is not shown.
"""
import json
import os
import threading
from pathlib import Path

from . import okunus

DOSYA = "okuma_listesi.json"
SURUM = 1
EN_COK = 500           # liste tavanı / list cap
KIMLIK_EN_UZUN = 200   # karakter / characters
_KILIT = threading.Lock()  # arayüz sunucusu çok iş parçacıklı; iki sekme aynı anda yazabilir / two tabs may write at once


def yol(settings: dict) -> Path:
    return Path(settings["sesler"]) / DOSYA


def _ham(path: Path):
    """Dosyadaki kimlikler; dosya yoksa [], bozuksa None. / Identities in the file; [] if missing, None if corrupt."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (OSError, ValueError):
        return None
    items = data.get("sesler") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return None
    out = []
    for item in items:
        if isinstance(item, str) and item not in out:
            out.append(item)
    return out


def oku(settings: dict) -> list:
    """Dosyadaki bütün kimlikler (silinmiş sesler dahil), eklenme sırasıyla; dosya yok ya da bozuksa boş liste.
    Okuma yan etkisizdir: bozuk dosya ilk yazımda kenara alınır.
    All identities in the file (deleted voices included), in order; empty if missing or corrupt. Reading has no side effects."""
    return _ham(yol(settings)) or []


def bicim_dogru(kimlik) -> bool:
    """'hazir/<ad>' ya da '<ad>/<çeşit>' biçimi; klasör yolu, '..', ters bölü, sürücü ve mutlak yol değil.
    oku.find_voice doğrudan klasör yolunu da kabul ettiği için listeye yalnız kimlik biçimi girer.
    Identity shape only: no folder paths, '..', backslashes, drive letters or absolute paths."""
    if not isinstance(kimlik, str) or not kimlik.strip() or len(kimlik) > KIMLIK_EN_UZUN:
        return False
    if "\\" in kimlik or ":" in kimlik or kimlik.startswith("/") or any(c < " " for c in kimlik):
        return False
    parts = kimlik.split("/")
    return len(parts) == 2 and all(parts) and ".." not in parts and "." not in parts


def _yaz(path: Path, items: list):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps({"surum": SURUM, "sesler": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)  # yarım dosya kalmaz / never a half-written file


def degistir(settings: dict, kimlik, ekle, gecerli) -> list:
    """Sesi listenin sonuna ekler ya da çıkarır; arayüze giden (gecerli ile süzülmüş) listeyi döndürür. Aynı ses iki kez
    girmez. gecerli: bugün listelenen ses kimlikleri (oku.list_voices). Ekleme yalnız bunlardan biri için olur; çıkarma
    her biçimi doğru kimlik için olur (silinmiş sesin kaydı da çıkarılabilir). Yanlış girişte ValueError.
    Adds a voice at the end or removes it; returns the list for the UI (filtered by gecerli). Raises ValueError."""
    if not isinstance(ekle, bool):
        raise ValueError("'ekle' true ya da false olmalı / 'ekle' must be true or false")
    gecerli = set(gecerli)
    if not bicim_dogru(kimlik) or (ekle and kimlik not in gecerli):
        ad = str(kimlik)[:KIMLIK_EN_UZUN]
        raise ValueError(okunus.Sorun(f"ses bulunamadı: {ad}", "ses_yok", ses=ad))
    path = yol(settings)
    with _KILIT:
        items = _ham(path)
        if items is None:  # bozuk dosya sessizce ezilmez, kenara alınır / a corrupt file is set aside, not overwritten
            os.replace(path, path.with_name(path.name + ".bozuk"))
            items = []
        degisti = False
        if ekle and kimlik not in items:
            if len(items) >= EN_COK:
                raise ValueError(f"okuma listesi dolu (en çok {EN_COK}) / reading list is full (max {EN_COK})")
            items.append(kimlik)
            degisti = True
        elif not ekle and kimlik in items:
            items.remove(kimlik)
            degisti = True
        if degisti:
            _yaz(path, items)
    return [k for k in items if k in gecerli]

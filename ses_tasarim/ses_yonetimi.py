"""Ses yönetimi: yeniden adlandırma, gizleme ve çöpe taşıma; hepsi kullanıcının ses klasöründe ve geri alınabilir.
Voice management: rename, hide and move to trash; all in the user's voice folder and all reversible.

- Takma ad ve gizli liste `<sesler>/yerel_katman.json` dosyasındadır (git dışı). Hazır seslerin klasörüne ve hiçbir
  ses.json'a yazılmaz; boş ad asıl ada döner.
- Hazır ses silinmez, gizlenir (repo dosyası). Tasarlanan çeşit silinince `<sesler>/_cop/` altına taşınır
  (`oku.list_voices` `_` ile başlayan klasörü görmez) ve oradan geri getirilir. Kalıcı silme yoktur.
- Display names and the hidden list live in `<sesler>/yerel_katman.json` (outside git); bundled voices and ses.json are
  never written. A bundled voice is hidden, not deleted. A designed variant goes to `<sesler>/_cop/` and can be restored.
"""
import json
import os
import shutil
import threading
import time
from pathlib import Path

from . import okuma_listesi, okunus

DOSYA = "yerel_katman.json"
COP = "_cop"
SURUM = 1
AD_EN_UZUN = 80
ISLEMLER = ("ad", "gizle", "goster", "sil", "geri")
_KILIT = threading.Lock()


def yol(settings: dict) -> Path:
    return Path(settings["sesler"]) / DOSYA


def cop_kok(settings: dict) -> Path:
    return Path(settings["sesler"]) / COP


def _bos():
    return {"surum": SURUM, "ad": {}, "gizli": []}


def _ham(path: Path):
    """Katman; dosya yoksa boş, bozuksa None. / The layer; empty if missing, None if corrupt."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return _bos()
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("ad", {}), dict) or not isinstance(data.get("gizli", []), list):
        return None
    out = _bos()
    out["ad"] = {k: v for k, v in data.get("ad", {}).items() if isinstance(k, str) and isinstance(v, str) and v.strip()}
    out["gizli"] = [k for k in dict.fromkeys(data.get("gizli", [])) if isinstance(k, str)]
    return out


def katman(settings: dict) -> dict:
    """Takma adlar ve gizli kimlikler; bozuk dosya boş sayılır (okuma yan etkisiz).
    Display names and hidden ids; a corrupt file reads as empty (reading has no side effects)."""
    with _KILIT:
        return _ham(yol(settings)) or _bos()


def _yaz(path: Path, data: dict):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _cop_kaydi(folder: Path):
    try:
        data = json.loads((folder / "kaynak.json").read_text(encoding="utf-8"))
        card = json.loads((folder / "ses.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    kimlik = data.get("kimlik") if isinstance(data, dict) else None
    if not okuma_listesi.bicim_dogru(kimlik) or kimlik.startswith("hazir/") or not kimlik.rsplit("/", 1)[1].isdigit():
        return None
    return {**card, "kimlik": kimlik, "cop": folder.name, "silinme": data.get("silinme", "")}


def cop_listesi(settings: dict) -> list:
    """Çöpteki çeşitler, en yeni silinen üstte: kart alanları + `kimlik` (asıl) + `cop` (çöp klasörü adı).
    Trashed variants, newest first: card fields + original `kimlik` + `cop` (trash folder name)."""
    root = cop_kok(settings)
    if not root.is_dir():
        return []
    items = [_cop_kaydi(p) for p in root.iterdir() if p.is_dir()]
    return sorted((x for x in items if x), key=lambda x: x["cop"], reverse=True)


def uygula(voices: dict, layer: dict) -> dict:
    """oku.list_voices çıktısına katmanı uygular: takma ad `gorunen_ad` olur (asıl ad `asil_ad`), gizli hazır sesler
    `gizli` listesine ayrılır. Girdi değişmez. / Applies the layer: alias → gorunen_ad, hidden bundled voices → gizli."""
    names, hidden = layer.get("ad", {}), set(layer.get("gizli", []))
    out = {"hazir": [], "tasarlanan": [], "gizli": []}
    for group in ("hazir", "tasarlanan"):
        for card in voices.get(group, []):
            card = dict(card)
            asil = card.get("gorunen_ad") or card.get("ad") or card["kimlik"]
            if card["kimlik"] in names:
                card["asil_ad"], card["gorunen_ad"] = asil, names[card["kimlik"]]
            out["gizli" if group == "hazir" and card["kimlik"] in hidden else group].append(card)
    return {**voices, **out}


def _sorun(metin, kod, **veri):
    return ValueError(okunus.Sorun(metin, kod, **veri))


def yonet(settings: dict, kimlik, islem, ad=None, gecerli=(), cop=None) -> None:
    """Tek işlem. gecerli: bugün listelenen kimlikler (oku.list_voices); cop: çöp klasörü adı (yalnız 'geri').
    islem: 'ad' (boş ad = asıl ada dön), 'gizle'/'goster' (yalnız hazır), 'sil' (yalnız tasarlanan, çöpe), 'geri'
    (çöpten). Yanlış girişte ValueError(okunus.Sorun).
    One operation; raises ValueError(okunus.Sorun) on bad input."""
    if islem not in ISLEMLER:
        raise _sorun(f"bilinmeyen işlem: {str(islem)[:20]}", "islem_yok", islem=str(islem)[:20])
    gecerli = set(gecerli)
    if islem == "geri":
        return _geri(settings, cop)
    if not okuma_listesi.bicim_dogru(kimlik):
        raise _sorun(f"ses bulunamadı: {str(kimlik)[:200]}", "ses_yok", ses=str(kimlik)[:200])
    hazir = kimlik.startswith("hazir/")
    if islem == "goster":  # gizli hazır ses listede görünmez ama klasörü vardır / a hidden voice still exists
        if not hazir:
            raise _sorun("yalnız hazır ses gizlenir", "islem_yok", islem=islem)
        return _katman_degistir(settings, lambda d: d.update(gizli=[k for k in d["gizli"] if k != kimlik]))
    if kimlik not in gecerli:
        raise _sorun(f"ses bulunamadı: {kimlik}", "ses_yok", ses=kimlik)
    if islem == "ad":
        ad = "" if ad is None else ad
        if not isinstance(ad, str) or any(ord(c) < 32 or c == "\x7f" for c in ad):
            raise _sorun("geçersiz ad", "ad_uzun", n=AD_EN_UZUN)
        ad = " ".join(ad.split())
        if len(ad) > AD_EN_UZUN:
            raise _sorun(f"ad en çok {AD_EN_UZUN} karakter", "ad_uzun", n=AD_EN_UZUN)

        def degistir(d):
            if ad:
                d["ad"][kimlik] = ad
            else:
                d["ad"].pop(kimlik, None)
        return _katman_degistir(settings, degistir)
    if islem == "gizle":
        if not hazir:
            raise _sorun("tasarlanan ses gizlenmez, silinir", "islem_yok", islem=islem)
        return _katman_degistir(settings, lambda d: d["gizli"].append(kimlik) if kimlik not in d["gizli"] else None)
    # sil
    if hazir:
        raise _sorun("hazır ses silinmez, gizlenir", "islem_yok", islem=islem)
    name, number = kimlik.rsplit("/", 1)
    try:
        folder = Path(settings["sesler"]) / name / f"cesit_{int(number):02d}"
    except ValueError:
        raise _sorun(f"ses bulunamadı: {kimlik}", "ses_yok", ses=kimlik)
    root = cop_kok(settings)
    with _KILIT:
        if not (folder / "ses.json").is_file():
            raise _sorun(f"ses bulunamadı: {kimlik}", "ses_yok", ses=kimlik)
        root.mkdir(exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        target = root / f"{stamp}__{name}__{folder.name}"
        n = 1
        while target.exists():
            n += 1
            target = root / f"{stamp}_{n}__{name}__{folder.name}"
        shutil.move(str(folder), str(target))
        (target / "kaynak.json").write_text(json.dumps({"kimlik": kimlik, "silinme": time.strftime("%Y-%m-%d %H:%M")},
                                                       ensure_ascii=False) + "\n", encoding="utf-8")
    return None


def _geri(settings: dict, cop) -> None:
    root = cop_kok(settings)
    if not isinstance(cop, str) or not cop or "/" in cop or "\\" in cop or cop in (".", "..") or ":" in cop:
        raise _sorun("çöpte bulunamadı", "ses_yok", ses=str(cop)[:200])
    with _KILIT:
        folder = root / cop
        kayit = _cop_kaydi(folder) if folder.is_dir() else None
        if not kayit:
            raise _sorun("çöpte bulunamadı", "ses_yok", ses=cop)
        name, number = kayit["kimlik"].rsplit("/", 1)
        target = Path(settings["sesler"]) / name / f"cesit_{int(number):02d}"
        if target.exists():
            raise _sorun(f"yerinde başka ses var: {kayit['kimlik']}", "hedef_dolu", ses=kayit["kimlik"])
        target.parent.mkdir(exist_ok=True)
        shutil.move(str(folder), str(target))
        (target / "kaynak.json").unlink(missing_ok=True)


def _katman_degistir(settings: dict, fn) -> None:
    path = yol(settings)
    with _KILIT:
        data = _ham(path)
        if data is None:  # bozuk dosya kenara alınır / a corrupt file is set aside
            os.replace(path, path.with_name(path.name + ".bozuk"))
            data = _bos()
        fn(data)
        _yaz(path, data)

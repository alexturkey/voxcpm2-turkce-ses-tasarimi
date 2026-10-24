"""Basit yerel arayüz (yalnız 127.0.0.1, Python stdlib). Tarayıcıyı kendisi açmaz; adresi yazdırır.
Simple local web UI (127.0.0.1 only, stdlib http.server). Prints the address; does not open a browser.

python -m ses_tasarim.arayuz [--ayarlar ayarlar.json] [--port 8765]

Akış / flow: Tasarla → çeşitleri dinle → birini seç → Bu sesle oku → indir.  Hazır sesle oku: listeden seç → metin → oku.
Klonla (3): kendi/izinli kayıt + birebir metni + onay → Klonla ve oku → indir. / Clone (3): own or consented recording
+ exact transcript + consent → clone and read → download.
Ses tasarımı kayıt istemez. Ses klonlama bölümü yalnız kendi sesiniz ya da sahibinden açık izin alınmış ses içindir;
onay kutusu işaretlenmeden çalışmaz, kayıt yalnız yerelde işlenir ve iş bitince (hata olsa da) silinir.
Voice design needs no recording. The cloning section is only for your own or a consented voice; it requires the consent
checkbox, processes the upload locally and deletes it when the job ends (also on failure).
"""
import argparse
import base64
import binascii
import json
import mimetypes
import queue
import sys
import threading
import time
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from . import ayarlar, motor, oku, tasarla

HTML = r"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VoxCPM2 Türkçe Ses Tasarımı</title>
<style>
:root{--bg:#111;--panel:#1c1c1c;--fg:#eee;--muted:#9a9a9a;--acc:#ebbe6e;--ok:#5fb36a;--err:#e06c6c}
body{font-family:Segoe UI,system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:980px;margin:auto;padding:16px}
section{background:var(--panel);border-radius:10px;padding:14px 18px;margin:12px 0}
h1{font-size:1.4rem}h2{font-size:1.1rem;color:var(--acc);margin:4px 0 10px}
label{display:block;margin:10px 0 4px;color:var(--muted);font-size:.9rem}
textarea,input,select{width:100%;box-sizing:border-box;background:#0d0d0d;color:var(--fg);border:1px solid #333;border-radius:6px;padding:8px;font:inherit}
textarea{min-height:90px}
button{background:var(--acc);color:#111;border:0;border-radius:6px;padding:9px 16px;font-weight:600;cursor:pointer;margin-top:10px}
button:disabled{opacity:.5;cursor:default}
.row{display:flex;gap:12px;flex-wrap:wrap}.row>*{flex:1;min-width:200px}
.durum{margin-top:8px;color:var(--muted);white-space:pre-wrap}.hata{color:var(--err)}.ok{color:var(--ok)}
.cesit{display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid #2a2a2a}
.cesit audio{flex:1;height:32px}small{color:var(--muted)}
.uyari{border-left:3px solid var(--acc);padding:6px 10px;color:var(--muted);font-size:.9rem}
</style></head><body>
<h1>VoxCPM2 Türkçe Ses Tasarımı <small>· 4 GB GPU</small></h1>
<div class="uyari">Üretilen her ses yapay zekâ ürünüdür; paylaşırken belirtin. Ses tasarımı (1-2) kayıt istemez; ses klonlama (3) yalnız kendi sesiniz ya da sahibinden açık izin alınmış sesle.
<br><small>Every generated voice is synthetic; label it as AI-generated when sharing. Voice design (1-2) needs no recording; voice cloning (3) only with your own voice or the owner's explicit permission.</small></div>

<section><h2>1. Ses tasarla <small>(voice design)</small></h2>
<div class="row"><div><label>Sesin adı (voice name)</label><input id="ad" placeholder="deniz_feneri"></div>
<div><label>Çeşit sayısı (variants, her biri ayrı tohum)</label><input id="cesit" type="number" value="3" min="1" max="10"></div>
<div><label>Dil (language)</label><select id="dil"><option value="tr">Türkçe</option><option value="en">English</option><option value="fr">Français</option><option value="de">Deutsch</option><option value="es">Español</option><option value="ru">Русский</option><option value="zh">中文</option><option value="ja">日本語</option></select></div></div>
<label>İngilizce ses tarifi, parantezsiz (voice description in English)</label>
<textarea id="tarif" placeholder="A calm Turkish woman in her forties with a warm, low voice, speaking slowly and clearly. Clean studio recording, no background noise."></textarea>
<label>Ses yaratılırken okutulan metin, sesin dilinde, rakamsız; Türkçede tırnak yok (text read while creating the voice, in its language)</label>
<textarea id="tasarim_metni" placeholder="Merhaba, ben bir belgesel anlatıcısıyım. Yıllardır tarihin derinliklerinden hikâyeler anlatırım..."></textarea>
<button id="btn_tasarla">Tasarla</button><div id="d_tasarla" class="durum"></div>
<div id="cesitler"></div></section>

<section><h2>2. Bu sesle oku <small>(read with the selected voice)</small></h2>
<label>Ses (voice)</label><select id="ses"></select>
<label>Okunacak metin: her satır bir cümle; satır sonuna "|| paragraf" uzun durak (text to read, one sentence per line)</label>
<textarea id="okuma_metni" placeholder="Bu ses yalnız bir metin tarifinden tasarlandı, bir kayıttan klonlanmadı.
Yapay zekâ ile üretilmiş bir sestir. || paragraf
Şimdi istediğiniz metni okuyabilir."></textarea>
<button id="btn_oku">Bu sesle oku</button><div id="d_oku" class="durum"></div>
<div id="sonuc"></div></section>

<section><h2>3. Ses klonlama: kendi sesin ya da izinli ses <small>(voice cloning: own or consented voice)</small></h2>
<div class="uyari">Yalnız kendi sesiniz ya da sahibinden açık izin aldığınız ses. Kayıt yalnız bu bilgisayardaki yerel sunucuda işlenir, saklanmaz, ağa gönderilmez; iş bitince (hata olsa da) geçici dosya silinir, yalnız yapay çıktı kalır.
<br><small>Only your own voice or a voice whose owner gave explicit permission. The recording is processed by the local server on this computer only, never stored or sent over the network; the temp files are deleted when the job ends (also on failure), only the synthetic output is kept.</small></div>
<label>Ses kaydı: wav / mp3 / flac / ogg, 5-30 sn temiz konuşma önerilir, 3 sn altı reddedilir, 36 sn üstü kırpılır (recording, 5-30 s advised, under 3 s rejected, trimmed at 36 s)</label>
<input id="klon_dosya" type="file" accept=".wav,.mp3,.flac,.ogg,audio/*"><div id="klon_bilgi" class="durum"></div>
<label>Kaydın birebir metni, zorunlu: kayıtta ne söyleniyorsa aynısı (exact transcript of the recording, required)</label>
<textarea id="klon_kayit_metni" placeholder="Kayıtta söylediğim cümleler kelimesi kelimesine buraya."></textarea>
<label>Okunacak metin: her satır bir cümle (text to read, one sentence per line)</label>
<textarea id="klon_metin" placeholder="Bu kendi sesimin yapay bir kopyasıdır."></textarea>
<div class="row"><div><label>Tohum (seed; aynı tohum = aynı sonuç)</label><input id="klon_tohum" type="number" value="42" min="0"></div>
<div><label>Kalite (sabit / fixed)</label><input value="16 adım, cfg 2.0" disabled></div></div>
<label style="color:var(--fg)"><input id="klon_onay" type="checkbox" style="width:auto"> Bu ses bana ait ya da sahibinden açık izin aldım; taklit/dolandırıcılık/yanıltma için kullanmayacağım.
<br><small>This voice is mine or I have the owner's explicit permission; I will not use it for impersonation, fraud or deception.</small></label>
<button id="btn_klon" disabled>Klonla ve oku (clone and read)</button><div id="d_klon" class="durum"></div>
<div id="klon_sonuc"></div></section>

<section><h2>Hazır sesler <small>(bundled voices)</small></h2><div id="hazir"></div></section>
<script>
const $=id=>document.getElementById(id);
async function api(yol,gov){const r=await fetch(yol,gov?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(gov)}:{});return r.json();}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
let sesler={hazir:[],tasarlanan:[]};
async function yenile(secili){sesler=await api('/api/sesler');const s=$('ses');s.innerHTML='';
 for(const k of sesler.tasarlanan){const o=document.createElement('option');o.value=k.kimlik;o.textContent='tasarlanan: '+k.kimlik+' ['+(k.dil||'tr')+'] (tohum '+k.okuma_tohumu+')';s.appendChild(o);}
 for(const k of sesler.hazir){const o=document.createElement('option');o.value=k.kimlik;o.textContent='hazır: '+k.gorunen_ad+' ['+(k.dil||'tr')+'] — '+(k.tanitim_tr||'').slice(0,60);s.appendChild(o);}
 if(secili)s.value=secili;
 $('hazir').innerHTML=sesler.hazir.map(k=>`<div class="cesit"><div style="flex:1"><b>${esc(k.gorunen_ad)}</b> <small>tohum ${k.okuma_tohumu}</small><br><small>${esc(k.tanitim_tr)}</small></div>`+
  (k.ornek_okuma?`<audio controls preload="none" src="/dosya/${esc(k.kimlik)}/${esc(k.ornek_okuma)}"></audio>`:`<audio controls preload="none" src="/dosya/${esc(k.kimlik)}/${esc(k.referans)}"></audio>`)+`</div>`).join('');}
async function bekle(is,durum){for(;;){const j=await api('/api/is/'+is);durum.textContent=j.mesaj||j.durum;durum.className='durum '+(j.durum==='hata'?'hata':j.durum==='bitti'?'ok':'');
 if(j.durum==='bitti'||j.durum==='hata')return j;await new Promise(r=>setTimeout(r,2000));}}
$('btn_tasarla').onclick=async()=>{const b=$('btn_tasarla');b.disabled=true;$('cesitler').innerHTML='';
 const j=await api('/api/tasarla',{ad:$('ad').value,tarif:$('tarif').value,metin:$('tasarim_metni').value,cesit:+$('cesit').value,dil:$('dil').value});
 if(j.hata){$('d_tasarla').textContent=j.hata;$('d_tasarla').className='durum hata';b.disabled=false;return;}
 const s=await bekle(j.is,$('d_tasarla'));b.disabled=false;if(s.durum!=='bitti')return;
 $('cesitler').innerHTML=s.sonuc.cesitler.map(c=>c.hata?`<div class="cesit hata">tohum ${c.tohum}: ${esc(c.hata)}</div>`:
  `<div class="cesit"><label style="margin:0"><input type="radio" name="sec" value="${esc(s.sonuc.ses)}/${c.cesit}"> çeşit ${c.cesit} <small>tohum ${c.tasarim_tohumu}, ${c.referans_sn} sn</small></label><audio controls preload="none" src="/dosya/${esc(s.sonuc.ses)}/${c.cesit}/referans.wav"></audio></div>`).join('');
 document.querySelectorAll('input[name=sec]').forEach(r=>r.onchange=()=>{$('ses').value=r.value;});
 await yenile($('ses').value);const ilk=document.querySelector('input[name=sec]');if(ilk){ilk.checked=true;$('ses').value=ilk.value;}};
$('btn_oku').onclick=async()=>{const b=$('btn_oku');b.disabled=true;$('sonuc').innerHTML='';
 const j=await api('/api/oku',{ses:$('ses').value,metin:$('okuma_metni').value});
 if(j.hata){$('d_oku').textContent=j.hata;$('d_oku').className='durum hata';b.disabled=false;return;}
 const s=await bekle(j.is,$('d_oku'));b.disabled=false;if(s.durum!=='bitti')return;
 $('sonuc').innerHTML=`<audio controls src="/okuma/${s.sonuc.is}/okuma.wav"></audio> <a href="/okuma/${s.sonuc.is}/okuma.wav" download="okuma.wav"><button>İndir (download)</button></a>
  <div><small>${s.sonuc.ses_sn} sn ses, ${s.sonuc.sure_sn} sn üretim, VRAM tepe ${s.sonuc.vram_tepe_mb} MB, tohum ${s.sonuc.tohum}</small></div>`;};
const klonHazir=()=>{$('btn_klon').disabled=!($('klon_onay').checked&&$('klon_dosya').files.length&&$('klon_kayit_metni').value.trim()&&$('klon_metin').value.trim());};
['klon_onay','klon_dosya','klon_kayit_metni','klon_metin'].forEach(id=>{$(id).addEventListener('input',klonHazir);$(id).addEventListener('change',klonHazir);});
$('klon_dosya').addEventListener('change',()=>{const f=$('klon_dosya').files[0];if(!f)return;const u=URL.createObjectURL(f);const a=new Audio();a.onloadedmetadata=()=>{const d=a.duration;
 $('klon_bilgi').textContent=d.toFixed(1)+' sn'+(d>36?' · 36 sn üstü kırpılacak, kayıt metni ilk 36 sn ile eşleşmeli (trimmed to 36 s, the transcript must match that part)':d<3?' · çok kısa, en az 3 sn gerekli (too short, at least 3 s)':d<5||d>30?' · 5-30 sn önerilir (5-30 s advised)':'');URL.revokeObjectURL(u);};a.src=u;});
function b64(buf){const u=new Uint8Array(buf);let s='';for(let i=0;i<u.length;i+=32768)s+=String.fromCharCode.apply(null,u.subarray(i,i+32768));return btoa(s);}
$('btn_klon').onclick=async()=>{if(!$('klon_onay').checked)return;const b=$('btn_klon');b.disabled=true;$('klon_sonuc').innerHTML='';
 const f=$('klon_dosya').files[0];const j=await api('/api/klon',{onay:true,kayit:b64(await f.arrayBuffer()),kayit_metni:$('klon_kayit_metni').value,metin:$('klon_metin').value,tohum:+$('klon_tohum').value});
 if(j.hata){$('d_klon').textContent=j.hata;$('d_klon').className='durum hata';klonHazir();return;}
 const s=await bekle(j.is,$('d_klon'));klonHazir();if(s.durum!=='bitti')return;const r=s.sonuc;
 $('klon_sonuc').innerHTML=`<audio controls src="/okuma/${r.is}/${r.dosya}"></audio> <a href="/okuma/${r.is}/${r.dosya}" download="${r.dosya}"><button>İndir (download)</button></a>
  <div class="uyari"><b>Yapay üretilmiş sestir.</b> Paylaşırken belirtin. <small>AI-generated synthetic speech; label it when sharing.</small></div>
  <div><small>${r.ses_sn} sn ses, ${r.sure_sn} sn üretim, VRAM tepe ${r.vram_tepe_mb} MB, tohum ${r.tohum}, referans ${r.referans_sn} sn</small>${(r.notlar||[]).map(n=>'<br><small>'+esc(n)+'</small>').join('')}</div>`;};
yenile();
</script></body></html>
"""


class Isler:
    """Tek işçi: GPU'da aynı anda tek üretim. / One worker: one GPU job at a time."""

    def __init__(self, settings):
        self.settings = settings
        self.jobs = {}
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        threading.Thread(target=self._run, daemon=True).start()

    def submit(self, kind: str, payload: dict) -> str:
        job_id = time.strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6]
        with self.lock:
            self.jobs[job_id] = {"durum": "sirada", "mesaj": "sırada bekliyor (queued)", "tur": kind}
        self.queue.put((job_id, kind, payload))
        return job_id

    def status(self, job_id: str) -> dict:
        with self.lock:
            return dict(self.jobs.get(job_id) or {"durum": "hata", "mesaj": "iş bulunamadı"})

    def _set(self, job_id, **fields):
        with self.lock:
            self.jobs[job_id].update(fields)

    def _run(self):
        while True:
            job_id, kind, payload = self.queue.get()
            self._set(job_id, durum="calisiyor", mesaj="motor başlatılıyor, model yükleniyor (~10-20 sn)")

            def progress(done, total, elapsed, job_id=job_id):
                self._set(job_id, mesaj=f"{done}/{total} hazır, {elapsed:.0f} sn")
            try:
                if kind == "tasarla":
                    result = tasarla.tasarla(self.settings, payload["ad"], payload["tarif"], payload["metin"],
                                             int(payload.get("cesit") or 3), None, progress,
                                             payload.get("dil") or "tr")
                    self._set(job_id, durum="bitti", sonuc=result,
                              mesaj=f"bitti: {len(result['cesitler'])} çeşit, {result['sure_sn']} sn, VRAM tepe {result['vram_tepe_mb']} MB")
                elif kind == "klon":
                    from . import klonla
                    data = base64.b64decode(payload.pop("kayit"))
                    try:
                        result = klonla.klonla(self.settings, data, payload["kayit_metni"], payload["metin"],
                                               self.settings["sesler"] / "_okumalar" / job_id, payload.get("onay"),
                                               payload.get("tohum"), progress)
                    finally:
                        data = None  # kayıt baytları hata yolunda da bellekte tutulmaz / drop bytes, also on failure
                    result["is"] = job_id
                    self._set(job_id, durum="bitti", sonuc=result, mesaj="bitti: yapay ses hazır (synthetic)")
                else:
                    voice_dir = oku.find_voice(self.settings, payload["ses"])
                    out_dir = self.settings["sesler"] / "_okumalar" / job_id
                    result = oku.oku(self.settings, voice_dir, payload["metin"], out_dir, progress, payload.get("dil"))
                    result["is"] = job_id
                    self._set(job_id, durum="bitti", sonuc=result, mesaj="bitti")
            except Exception as error:  # kullanıcıya düz metin hata, ayrıntı için iz / plain-text error + traceback
                self._set(job_id, durum="hata", mesaj=str(error), iz=traceback.format_exc()[-1200:])


def make_handler(settings, jobs: Isler):
    roots = {"hazir": settings["hazir_sesler"], "tasarlanan": settings["sesler"]}

    class Handler(BaseHTTPRequestHandler):
        MAX_BODY = 1_000_000  # 1 MB: metin kutuları için fazlasıyla yeter / plenty for the text boxes
        MAX_KLON_BODY = 35_000_000  # klon: base64 ses (25 MB dosya sınırı) + metin / cloning upload as base64

        def log_message(self, fmt, *args):  # sessiz / quiet
            pass

        def _host_ok(self) -> bool:
            # DNS yeniden bağlama / CSRF: yalnız 127.0.0.1:<port> ve localhost:<port> Host başlığı kabul edilir.
            # DNS rebinding / CSRF guard: only Host 127.0.0.1:<port> or localhost:<port> is served.
            host = (self.headers.get("Host") or "").strip().lower()
            port = self.server.server_address[1]
            if host in (f"127.0.0.1:{port}", f"localhost:{port}", f"[::1]:{port}"):
                return True
            self._json({"hata": "Host başlığı kabul edilmedi (yalnız 127.0.0.1:%d)" % port}, 403)
            return False

        def _json(self, data, code=200):
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _file(self, path: Path, root: Path):
            try:
                path = path.resolve()
                path.relative_to(root.resolve())
            except (ValueError, OSError):
                return self.send_error(404)
            if not path.is_file() or path.suffix.lower() not in (".wav", ".flac", ".mp3", ".txt", ".json"):
                return self.send_error(404)
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(str(path))[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if not self._host_ok():
                return
            path = unquote(self.path.split("?")[0])
            if path == "/":
                body = HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            elif path == "/api/sesler":
                self._json(oku.list_voices(settings))
            elif path.startswith("/api/is/"):
                self._json(jobs.status(path[8:]))
            elif path.startswith("/dosya/hazir/"):
                self._file(roots["hazir"] / path[13:], roots["hazir"])
            elif path.startswith("/dosya/"):
                name, number, file = (path[7:].split("/") + ["", ""])[:3]
                self._file(roots["tasarlanan"] / name / f"cesit_{int(number or 0):02d}" / file, roots["tasarlanan"])
            elif path.startswith("/okuma/"):
                self._file(roots["tasarlanan"] / "_okumalar" / path[7:], roots["tasarlanan"] / "_okumalar")
            else:
                self.send_error(404)

        def do_POST(self):
            if not self._host_ok():
                return
            if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
                return self._json({"hata": "Content-Type: application/json gerekli"}, 415)
            length = int(self.headers.get("Content-Length") or 0)
            limit = self.MAX_KLON_BODY if self.path == "/api/klon" else self.MAX_BODY
            if length <= 0 or length > limit:
                return self._json({"hata": f"istek gövdesi 1 ile {limit} bayt arasında olmalı"}, 413)
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                return self._json({"hata": "geçersiz JSON"}, 400)
            if not isinstance(payload, dict):
                return self._json({"hata": "JSON nesnesi bekleniyor"}, 400)
            if self.path == "/api/tasarla":
                found = tasarla.check(payload.get("tarif", ""), payload.get("metin", ""), payload.get("dil") or "tr")
                if not str(payload.get("ad", "")).strip():
                    found.append("sesin adı boş")
                if found:
                    return self._json({"hata": "\n".join(found)}, 400)
                return self._json({"is": jobs.submit("tasarla", payload)})
            if self.path == "/api/oku":
                from . import okunus
                found = []
                try:
                    voice_dir = oku.find_voice(settings, str(payload.get("ses", "")))
                    found = okunus.problems(payload.get("metin", ""), dil=oku.voice_language(voice_dir, payload.get("dil")))
                except (FileNotFoundError, ValueError) as error:
                    found.append(str(error))
                if found:
                    return self._json({"hata": "\n".join(found)}, 400)
                return self._json({"is": jobs.submit("oku", payload)})
            if self.path == "/api/klon":
                from . import klonla
                found = klonla.check(payload.get("kayit_metni", ""), payload.get("metin", ""), payload.get("onay"))
                try:
                    data = base64.b64decode(str(payload.get("kayit") or ""), validate=True)
                except (binascii.Error, ValueError):
                    data = b""
                if not data:
                    found.append("ses kaydı yok ya da okunamadı (recording missing)")
                elif len(data) > klonla.MAX_UPLOAD_BYTES:
                    found.append("ses dosyası 25 MB'tan büyük")
                if found:
                    return self._json({"hata": "\n".join(found)}, 400)
                return self._json({"is": jobs.submit("klon", {k: payload.get(k) for k in
                                                              ("kayit", "kayit_metni", "metin", "onay", "tohum")})})
            self.send_error(404)

    return Handler


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ayarlar")
    parser.add_argument("--port", type=int)
    args = parser.parse_args(argv)
    settings = ayarlar.load(args.ayarlar)
    port = args.port or int(settings.get("port") or 8765)
    if sys.platform == "win32":
        # Windows'ta SO_REUSEADDR dolu porta ikinci sunucuyu sessizce bağlar; dolu port açıkça hata versin.
        # On Windows SO_REUSEADDR lets a second server bind a busy port silently; fail loudly instead.
        ThreadingHTTPServer.allow_reuse_address = False
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(settings, Isler(settings)))
    print(f"Arayüz hazır: http://127.0.0.1:{port}/  (kapatmak için Ctrl+C)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

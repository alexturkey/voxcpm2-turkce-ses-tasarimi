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

from . import ayarlar, motor, oku, okunus, ornekler, tasarla

BAYRAK_KOKU = Path(__file__).resolve().parent / "bayraklar"  # flag-icons 7.2.3 (MIT), 4x3 SVG / flag images
DIL_KOKU = Path(__file__).resolve().parent / "arayuz_dilleri"  # arayüz metinleri, dil başına bir JSON / UI strings

HTML = r"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VoxCPM2 Türkçe Ses Tasarımı</title><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect x='9' y='2' width='6' height='12' rx='3' fill='%23e3a33b'/%3E%3Cpath d='M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8' fill='none' stroke='%23e3a33b' stroke-width='2' stroke-linecap='round'/%3E%3C/svg%3E">
<style>
:root{--bg:#111;--panel:#1c1c1c;--fg:#eee;--muted:#9a9a9a;--soluk:#777;--alan:#0d0d0d;--cizgi:#333;--cizgi2:#2a2a2a;--acc:#ebbe6e;--baslik:#ebbe6e;--ok:#5fb36a;--err:#e06c6c;color-scheme:dark}
:root[data-tema=acik]{--bg:#f5f5f3;--panel:#fff;--fg:#1d1d1f;--muted:#5f6368;--soluk:#80868b;--alan:#fff;--cizgi:#d4d4d4;--cizgi2:#e8e8e8;--acc:#e3a93f;--baslik:#9a6a10;--ok:#2e7d32;--err:#c62828;color-scheme:light}
body{font-family:Segoe UI,system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:980px;margin:auto;padding:16px}
section{background:var(--panel);border-radius:10px;padding:14px 18px;margin:12px 0}
h1{font-size:1.4rem;margin:0}h2{font-size:1.1rem;color:var(--baslik);margin:4px 0 10px}
.bas{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:8px 0 10px}
button.tema{background:transparent;color:var(--fg);border:1px solid var(--cizgi);border-radius:50%;width:38px;height:38px;padding:0;margin:0;display:grid;place-items:center;flex:none}
button.tema:hover{border-color:var(--acc)}

.araclar{display:flex;gap:8px;align-items:center;flex:none}.dilkutu{position:relative}
button.dil{background:transparent;color:var(--fg);border:1px solid var(--cizgi);border-radius:19px;height:38px;padding:0 12px;margin:0;display:flex;align-items:center;gap:8px;font-size:.85rem}
button.dil:hover,button.dil[aria-expanded=true]{border-color:var(--acc)}
.bayraklar{position:absolute;inset-inline-end:0;top:44px;z-index:10;background:var(--panel);border:1px solid var(--cizgi);border-radius:10px;padding:8px;box-shadow:0 8px 24px rgba(0,0,0,.25);display:grid;grid-template-columns:repeat(3,minmax(140px,1fr));gap:2px;width:max-content;max-height:70vh;overflow:auto}
.bayraklar[hidden]{display:none}@media(max-width:560px){.bayraklar{grid-template-columns:repeat(2,minmax(130px,1fr))}}
.bayraklar button{background:none;color:var(--fg);border:0;padding:6px 8px;margin:0;border-radius:6px;cursor:pointer;display:flex;align-items:center;gap:8px;font-weight:400;font-size:.85rem;text-align:start}
.bayraklar button:hover{background:var(--cizgi2)}.bayraklar button[aria-pressed=true]{background:var(--cizgi2);box-shadow:inset 0 0 0 1px var(--acc)}
.bayraklar img,button.dil img{width:22px;height:16.5px;border-radius:2px;box-shadow:0 0 0 1px var(--cizgi2);flex:none}
.dosya{display:flex;align-items:center;gap:10px}.dosya span{color:var(--muted);font-size:.9rem}
button.ikincil{background:transparent;color:var(--fg);border:1px solid var(--cizgi);margin:0}button.ikincil:hover{border-color:var(--acc)}
label.onay{color:var(--fg);display:flex;gap:8px;align-items:flex-start}label.onay input{width:auto;margin-top:3px}

label{display:block;margin:10px 0 4px;color:var(--muted);font-size:.9rem}
textarea,input,select{width:100%;box-sizing:border-box;background:var(--alan);color:var(--fg);border:1px solid var(--cizgi);border-radius:6px;padding:8px;font:inherit}
textarea{min-height:90px}
main.kart{background:var(--panel);border-radius:10px;margin:12px 0;overflow:hidden}.kart>.panel{margin:0;border-radius:0}#p1{padding:0}
.sekmeler{display:flex;border-bottom:1px solid var(--cizgi2);overflow-x:auto}
.sekmeler button{flex:1;background:transparent;color:var(--muted);border:0;border-bottom:2px solid transparent;border-radius:0;margin:0;padding:12px 14px;font-weight:600;white-space:nowrap}
.sekmeler button:hover{color:var(--fg)}.sekmeler button[aria-selected=true]{color:var(--baslik);border-bottom-color:var(--acc)}
.govde{display:grid;grid-template-columns:1fr 1fr}.govde>div{padding:12px 16px;min-width:0}.govde>div+div{border-left:1px solid var(--cizgi2)}
@media(max-width:720px){.govde{grid-template-columns:1fr}.govde>div+div{border-left:0;border-top:1px solid var(--cizgi2)}}
label.mini{display:flex;flex-direction:column;gap:4px;margin:0 0 8px;border:1px solid var(--cizgi);border-radius:8px;padding:5px 10px 8px;color:var(--fg);font-size:.9rem;font-weight:600;min-width:0}
label.mini:focus-within{border-color:var(--acc)}label.mini input,label.mini select{padding:5px 8px;font-size:.85rem;font-weight:400}
.yanyana{display:flex;gap:8px}.yanyana>.mini{flex:1}#ornek{font-size:.85rem}#ornek optgroup{background:var(--cizgi2);color:var(--baslik);font-style:normal}#ornek option{background:var(--alan);color:var(--fg)}
.form label:not(.mini){margin:8px 0 3px;font-size:.82rem}.form textarea{min-height:84px}#defterkap{position:relative;overflow:hidden;--sat:28px;--bant:calc(var(--sat) / 3);--satir:var(--sat)}.defter{display:flex;height:238px;border:1px solid var(--cizgi);border-radius:6px;overflow:hidden;background:var(--alan)}.defter:focus-within{border-color:var(--acc)}#satirno{flex:none;position:relative;min-width:2.6em;padding:6px 8px;box-sizing:border-box;overflow:hidden;text-align:end;color:var(--muted);font-size:.78rem;line-height:var(--satir);border-inline-end:1px solid var(--cizgi2);user-select:none;background-attachment:local;background-image:linear-gradient(transparent calc(var(--satir) - 1px),var(--cizgi2) calc(var(--satir) - 1px));background-size:100% var(--satir);background-position:0 6px}#satirno .sb{opacity:.4}#satirno .gbant{position:absolute;inset-inline:0;height:var(--bant);background:var(--cizgi2)}#yazikap{flex:1;min-width:0;position:relative}#okuma_metni{display:block;width:100%;height:100%;min-height:0;border:0;border-radius:0;outline:0;resize:none;line-height:var(--satir);padding:6px 12px;background-color:transparent;background-attachment:local;background-image:linear-gradient(transparent calc(var(--satir) - 1px),var(--cizgi2) calc(var(--satir) - 1px));background-size:100% var(--satir);background-position:0 6px}#bantlar{position:absolute;inset:0;overflow:hidden;pointer-events:none}#bantlar .durak{position:absolute;inset-inline:0;height:var(--bant);margin:0;padding:0 12px;border:0;border-radius:0;background:var(--cizgi2);display:flex;align-items:center;cursor:pointer;pointer-events:auto}#bantlar .durak:hover,#bantlar .durak:focus-visible{background:var(--cizgi)}#bantlar .durak i{display:block;height:max(3px,calc(var(--bant) - 5px));border-radius:3px;background:var(--soluk);opacity:.7}#bantlar .durak.secik{background:color-mix(in srgb,var(--acc) 45%,transparent)}#bantlar .durak.o i{background:var(--acc);opacity:.6}#bantlar .durak.a i{background:var(--acc);opacity:1}#acilir{position:fixed;z-index:20;display:flex;flex-direction:column;gap:2px;padding:4px;background:var(--panel);border:1px solid var(--cizgi);border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.35)}#acilir[hidden]{display:none}#acilir button{display:flex;align-items:center;gap:10px;margin:0;padding:4px 9px;background:transparent;color:var(--fg);font-weight:400;font-size:.8rem;border:1px solid transparent;border-radius:5px}#acilir button:hover{background:var(--cizgi2)}#acilir button[aria-checked=true],#acilir button[aria-pressed=true]{color:var(--fg);font-weight:600;border-color:var(--acc);background:color-mix(in srgb,var(--acc) 16%,transparent)}#acilir .baslik{display:flex;align-items:baseline;gap:6px;width:0;min-width:100%;box-sizing:border-box;padding:3px 8px 6px;margin-bottom:2px;border-bottom:3px solid var(--cizgi);font-size:.75rem;color:var(--muted);white-space:nowrap}#acilir .baslik b{color:var(--fg);flex:none}#acilir .baslik span{margin:0;overflow:hidden;text-overflow:ellipsis}#acilir .satir{display:flex;align-items:center;gap:2px}#acilir .satir .kalp,#acilir .satir .sil{min-width:0;width:24px;height:24px;padding:0;justify-content:center;color:var(--muted);fill:none;opacity:0}#acilir .satir:hover .kalp,#acilir .satir:hover .sil,#acilir .kalp:focus-visible,#acilir .sil:focus-visible{opacity:1}#acilir .satir .kalp[aria-checked=true],#acilir .satir .kalp[aria-pressed=true]{border-color:transparent;background:transparent}#acilir .kalp.dolu{opacity:1;color:var(--err);fill:var(--err)}#acilir .satir .kalp:hover{color:var(--err)}#acilir .satir .sil:hover{color:var(--fg)}#acilir span.sil{display:block;width:24px;flex:none}#acilir hr{border:0;border-top:3px solid var(--cizgi);border-radius:2px;margin:3px 2px;width:auto}#acilir .satir+.satir,#acilir .satir+.onay,#acilir .onay+.satir{border-top:1px solid var(--cizgi2);padding-top:2px}#acilir .ozel [hidden]{display:none}#acilir .onay{display:flex;flex-direction:column;gap:4px;margin:2px 0;padding:6px 8px;border:1px solid var(--err);border-radius:6px;font-size:.8rem;max-width:230px}#acilir .onay span{margin:0;font-weight:600}#acilir .onay small{color:var(--muted)}#acilir .onay div{display:flex;gap:6px;justify-content:flex-end}#acilir .onay button{min-width:0;padding:3px 12px;font-weight:600}#acilir .onay .evet{background:var(--err);color:#fff;border-color:var(--err)}#acilir .onay .hayir{border-color:var(--cizgi)}#acilir .ozel{display:flex;align-items:center;gap:6px;margin-top:2px;padding-top:4px;border-top:1px solid var(--cizgi2)}#acilir .ozel button{min-width:0;padding:4px 7px;color:var(--muted)}#acilir .ozel button:hover{color:var(--fg)}#acilir .ozel input{width:5.5em;padding:3px 6px;font-size:.8rem;margin:0}#acilir .ozel small{color:var(--muted)}#acilir i{display:block;height:5px;border-radius:3px;background:var(--acc)}#acilir span{margin-inline-start:auto;font-variant-numeric:tabular-nums}#acilir button{min-width:120px}#satirno .no{display:flex;align-items:flex-start;justify-content:flex-end;box-sizing:border-box;width:100%;min-width:0;margin:0;padding:0;border:0;border-radius:0;background:transparent;color:inherit;font:inherit;line-height:var(--satir);cursor:pointer;touch-action:none}#satirno .no:hover,#satirno .no.secik{color:var(--fg);background:var(--cizgi2)}#satirno .no.bos{opacity:.45}#satirno .no.yanlis{color:var(--err);font-weight:700}#bantlar .durak.yanlis{outline:1px solid var(--err)}#bantlar .durak.yanlis i{background:var(--err);opacity:1}#acilir .tehlike:hover{color:var(--err)}#acilir button[aria-disabled=true]{opacity:.4;cursor:default;background:transparent}#acilir button[data-is] span{color:var(--muted);font-size:.72rem;padding-inline-start:14px}#acilir .ozel .oge{flex:1;justify-content:flex-start;color:var(--fg);padding:4px 9px}#acilir .ozel input.yanlis{border-color:var(--err);box-shadow:0 0 0 1px var(--err)}#acilir .sira_not{display:block;color:var(--err);padding:2px 9px;max-width:230px;white-space:normal}#acilir .sira_not[hidden]{display:none}#acilir .onay.notr{border-color:var(--acc)}#acilir .onay.notr .evet{background:var(--acc);color:#111;border-color:var(--acc)}#bantlar .durak.p:not(:hover,:focus-visible,.secik),#satirno .gbant.p{background:var(--cizgi)}#bantlar .durak.p i{opacity:1}#bantlar .durak.askida{border:1px dashed var(--cizgi);box-sizing:border-box;opacity:.6}#bantlar .durak.askida:not(:hover,:focus-visible,.secik){background:transparent}#bantlar .isik{position:absolute;inset-inline:0;pointer-events:none}#bantlar .parla,#satirno .parla{animation:parla .9s ease-out}@keyframes parla{from{background:color-mix(in srgb,var(--acc) 35%,transparent)}to{background:transparent}}@media (prefers-reduced-motion:reduce){#bantlar .parla,#satirno .parla{animation:none;background:color-mix(in srgb,var(--acc) 20%,transparent)}}#bantlar .hedef,#satirno .hedef{position:absolute;inset-inline:0;height:2px;background:var(--acc);pointer-events:none;z-index:2}#bantlar .kaynak{position:absolute;inset-inline:0;background:var(--acc);opacity:.15;pointer-events:none}#defterkap.suruk,#defterkap.suruk *{cursor:grabbing!important;user-select:none}.gizli{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}#ayna{position:absolute;top:0;left:0;visibility:hidden;pointer-events:none;white-space:pre-wrap;overflow-wrap:break-word;line-height:var(--satir);padding:0 12px;box-sizing:border-box}.tarifbas{display:flex;align-items:center;gap:6px}.tarifbas img{width:18px;height:13.5px;border-radius:2px;box-shadow:0 0 0 1px var(--cizgi2)}.form .sag{text-align:right}.ilerlesatir{display:flex;align-items:center;justify-content:flex-end;gap:10px}
.ilerle{flex:1;display:flex;align-items:center;gap:8px}.ilerle[hidden]{display:none}.pcubuk{flex:1;height:6px;border-radius:3px;background:var(--cizgi);overflow:hidden}
.pcubuk i{display:block;height:100%;width:0;background:var(--acc);border-radius:3px;transition:width .4s}.ilerle.bekler .pcubuk i{width:30%;animation:kay 1.2s ease-in-out infinite alternate}
@keyframes kay{from{margin-left:0}to{margin-left:70%}}.krono{font-variant-numeric:tabular-nums;color:var(--muted);font-size:.85rem;min-width:3.2em;text-align:right}
.ubas{border:1px solid var(--cizgi);border-radius:8px;padding:5px 10px 8px;display:flex;flex-wrap:wrap;align-items:center;gap:4px}.ubas select{flex:1 1 100%;min-width:0;padding:5px 8px;font-size:.85rem}.ubas .durum:empty{display:none}.ubas b{font-size:.9rem;flex-basis:100%}.ubas .durum{flex-basis:100%;margin:4px 0 0;font-size:.85rem}
#cesitler{display:grid;gap:6px;margin-top:8px;overflow-y:auto;border:1px solid var(--cizgi);border-radius:8px;padding:6px;align-content:start;max-height:494px}#cesitler .cesit{padding:6px 8px;gap:4px}#cesitler .cesit:has(input:checked){border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}.bos{color:var(--soluk);font-size:.85rem;margin:2px 0}
button{background:var(--acc);color:#111;border:0;border-radius:6px;padding:9px 16px;font-weight:600;cursor:pointer;margin-top:10px}
button:disabled{opacity:.5;cursor:default}
.row{display:flex;gap:12px;flex-wrap:wrap}.row>*{flex:1;min-width:200px}
.durum{margin-top:8px;color:var(--muted);white-space:pre-wrap}.hata{color:var(--err)}.ok{color:var(--ok)}
.cesit{display:flex;flex-direction:column;gap:6px;padding:8px;border:1px solid var(--cizgi2);border-radius:6px}
.cesit label{margin:0;color:var(--fg);font-size:.85rem;display:flex;align-items:center;gap:6px;flex-wrap:wrap}.cesit input[type=radio]{width:auto;margin:0;flex:none}.cesit audio{width:100%;height:32px}.csat{display:flex;align-items:center;gap:6px}.csat label{flex:1}.okubtn{flex:none;margin:0;padding:3px 10px;font-size:.78rem;font-weight:600;background:transparent;color:var(--acc);border:1px solid var(--acc);border-radius:999px}.okubtn:hover{background:var(--acc);color:#111}small{color:var(--muted)}
.uyari{border-left:3px solid var(--acc);padding:6px 10px;color:var(--muted);font-size:.9rem}
/* Tasarım metni kısa örnektir: 3 satırlık kutu, altında süre çubuğu, sınır aşımında uyarı, kalıcı gri ipucu. */
#tasarim_metni{flex:none;line-height:1.35;height:calc(4.05em + 18px);min-height:0;resize:none}
.sure{display:flex;align-items:center;gap:8px;margin:5px 0 0;font-size:.78rem;color:var(--muted)}.sure[hidden]{display:none}
.cubuk{flex:1;height:4px;background:var(--cizgi2);border-radius:2px;overflow:hidden}.cubuk i{display:block;height:100%;width:0;background:var(--acc);transition:width .2s}
.sure.asti .cubuk i{background:var(--err)}.sure.asti span{color:var(--err)}.sure span{flex:none}
.uzun{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:6px 0 0;color:var(--err);font-size:.82rem}.uzun[hidden]{display:none}
.uzun button{padding:4px 10px;font-size:.8rem;font-weight:600;white-space:normal;text-align:start;max-width:100%}
.ipucu{display:block;margin:5px 0 0;color:var(--soluk);font-size:.78rem;line-height:1.35}
/* Uygulama düzeni: sayfa kaymaz, kart pencereyi doldurur; dar ya da kısa ekranda normal kayan sayfa. */
@media(min-width:721px) and (min-height:560px){
html,body{height:100%}body{box-sizing:border-box;display:flex;flex-direction:column;overflow:hidden;padding:10px 16px}
.bas{margin:0 0 4px}main.kart{flex:1;min-height:0;display:flex;flex-direction:column;margin:8px 0 6px}
.kart>.panel{flex:1;min-height:0;overflow:auto}#p1:not([hidden]){display:flex;flex-direction:column;overflow:hidden}
.govde{flex:1;min-height:0}.govde>div{min-height:0;display:flex;flex-direction:column}.form{overflow:auto}
.form textarea{flex:1;min-height:70px;resize:none}#cesitler{flex:1;min-height:0;max-height:none}#p2:not([hidden]){display:flex;flex-direction:column}#defterkap{flex:1 1 0;min-height:0}#p2>button{align-self:flex-start}}
</style>
<script>try{document.documentElement.dataset.tema=localStorage.getItem('tema')||(matchMedia('(prefers-color-scheme: light)').matches?'acik':'koyu');}catch(e){}</script>
</head><body>
<header class="bas"><h1><span data-t="baslik">VoxCPM2 Türkçe Ses Tasarımı</span> <small>· 4 GB GPU</small></h1>
<div class="araclar"><div class="dilkutu"><button id="dil_dugme" class="dil" type="button" aria-haspopup="true" aria-expanded="false"></button>
<div class="bayraklar" id="bayraklar" role="group" hidden></div></div>
<button id="tema" class="tema" data-t-title="tema" title="Gece / gündüz" aria-label="Gece / gündüz"></button></div></header>

<main class="kart"><nav class="sekmeler" role="tablist">
<button type="button" role="tab" data-sekme="p1" data-sekme-t="s1"></button><button type="button" role="tab" data-sekme="p2" data-sekme-t="s2"></button><button type="button" role="tab" data-sekme="p3" data-sekme-t="s3"></button><button type="button" role="tab" data-sekme="p4" data-sekme-t="hazir"></button></nav>
<section id="p1" class="panel" role="tabpanel"><div class="govde">
<div class="form">
<div class="yanyana"><label class="mini"><span data-t="ad">Sesin adı</span><input id="ad" spellcheck="false" data-t-ph="ad_ph"></label>
<label class="mini" data-t-title="cesit"><span data-t="cesit_kisa">Çeşit</span><input id="cesit" type="number" value="3" min="1" max="50"></label></div>
<label class="mini" data-t-title="ornek_ipucu1"><span data-t="ornek">Örnek tarif</span><select id="ornek"></select></label>
<label for="tarif" class="tarifbas" data-t-title="e_tarif_parantez"><span data-t-bas="tarif">Ses tarifi</span><img src="/bayrak/gb.svg" alt="English"><img src="/bayrak/cn.svg" alt="中文"></label>
<textarea spellcheck="false" id="tarif" placeholder="A calm woman in her forties with a warm, low voice, speaking slowly and clearly. Clean studio recording, no background noise."></textarea>
<label for="tasarim_metni" data-t="tmetin">Örnek cümle (sesi tanımak için, 1-2 cümle)</label>
<textarea spellcheck="false" id="tasarim_metni" rows="3" data-t-ph="tmetin_ph" aria-describedby="sure_yazi tmetin_ipucu"></textarea>
<div id="sure" class="sure" hidden><div class="cubuk"><i id="sure_cubuk"></i></div><span id="sure_yazi" aria-live="polite"></span></div>
<div id="uzun_uyari" class="uzun" role="alert" hidden><span data-t="tmetin_uzun">Bu metin örnek için çok uzun. Uzun metni okuma sekmesinde okutun.</span><button type="button" class="ikincil" id="okumaya_tasi" data-t="okumaya_tasi">Okuma sekmesine taşı</button></div>
<small id="tmetin_ipucu" class="ipucu"></small>
<div class="sag ilerlesatir"><div id="p_tasarla" class="ilerle" hidden><div class="pcubuk"><i></i></div><span class="krono">0:00</span></div><button id="btn_tasarla" data-t="tasarla">Tasarla</button></div>
</div><div class="uretimler">
<div class="ubas"><b data-t="uretimler">Üretimler</b><select id="uretim" data-t-title="uretimler"></select><div id="d_tasarla" class="durum" aria-live="polite"></div></div>
<div id="cesitler"></div>
</div></div></section>

<section id="p2" class="panel" role="tabpanel" hidden>
<label for="ses" data-t="ses">Ses</label><select id="ses"></select>
<label for="okuma_metni" data-t="ometin">Okunacak metin: her satır bir cümle</label>
<div id="defterkap"><div class="defter"><div id="satirno"></div><div id="yazikap"><textarea spellcheck="false" id="okuma_metni" data-t-ph="ometin_ph"></textarea><div id="bantlar"><div></div></div></div></div><div id="ayna" aria-hidden="true"></div><div id="satir_duyuru" class="gizli" aria-live="polite"></div></div><div id="acilir" role="menu" hidden></div>
<button id="btn_oku" data-t="oku">Bu sesle oku</button><div id="d_oku" class="durum" aria-live="polite"></div>
<div id="sonuc"></div></section>

<section id="p3" class="panel" role="tabpanel" hidden>
<div class="uyari" data-t="klon_uyari"></div>
<label for="klon_dosya" data-t="kayit">Ses kaydı</label>
<div class="dosya"><input id="klon_dosya" type="file" accept=".wav,.mp3,.flac,.ogg,audio/*" hidden>
<button type="button" class="ikincil" id="dosya_btn" data-t="dosya_sec">Dosya seç</button><span id="dosya_ad" data-t="dosya_yok">Dosya seçilmedi</span></div>
<div id="klon_bilgi" class="durum"></div>
<label for="klon_kayit_metni" data-t="kayit_metni">Kaydın birebir metni (zorunlu)</label>
<textarea spellcheck="false" id="klon_kayit_metni" data-t-ph="kayit_metni_ph"></textarea>
<label for="klon_metin" data-t="klon_metin">Okunacak metin: her satır bir cümle</label>
<textarea spellcheck="false" id="klon_metin" data-t-ph="klon_metin_ph"></textarea>
<div class="row"><div><label for="klon_tohum" data-t="tohum">Tohum (aynı tohum = aynı sonuç)</label><input id="klon_tohum" type="number" value="42" min="0"></div>
<div><label data-t="kalite">Kalite (sabit)</label><input data-t-val="kalite_deger" value="16 adım, cfg 2.0" disabled></div></div>
<label class="onay"><input id="klon_onay" type="checkbox"> <span data-t="onay"></span></label>
<button id="btn_klon" data-t="klonla" disabled>Klonla ve oku</button><div id="d_klon" class="durum" aria-live="polite"></div>
<div id="klon_sonuc"></div></section>

<section id="p4" class="panel" role="tabpanel" hidden><div id="hazir"></div></section>
</main>
<script>
const $=id=>document.getElementById(id);
async function api(yol,gov){const r=await fetch(yol,gov?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(gov)}:{});return r.json();}
function esc(s){return String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function hafiza(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}

// Arayüz dilleri: VoxCPM2'nin desteklediği 30 dil (resmî README), [kod, bayrak, kendi dilinde adı, yön]
// UI languages: the 30 languages VoxCPM2 supports (official README), [code, flag, native name, direction]
const DILLER=[['tr','tr','Türkçe'],['en','gb','English'],['de','de','Deutsch'],['fr','fr','Français'],['es','es','Español'],
 ['it','it','Italiano'],['pt','pt','Português'],['ru','ru','Русский'],['pl','pl','Polski'],['nl','nl','Nederlands'],['da','dk','Dansk'],
 ['nb','no','Norsk'],['sv','se','Svenska'],['fi','fi','Suomi'],['el','gr','Ελληνικά'],['ar','sa','العربية','rtl'],['he','il','עברית','rtl'],
 ['hi','in','हिन्दी'],['zh','cn','中文'],['ja','jp','日本語'],['ko','kr','한국어'],['th','th','ไทย'],['vi','vn','Tiếng Việt'],
 ['id','id','Bahasa Indonesia'],['ms','my','Bahasa Melayu'],['tl','ph','Tagalog'],['my','mm','မြန်မာ'],['km','kh','ខ្មែរ'],['lo','la','ລາວ'],['sw','ke','Kiswahili']];
const ESDEGER={no:'nb',nn:'nb',fil:'tl',iw:'he',in:'id'};
let dil='tr',S={},YEDEK={};
const t=(k,v)=>String(S[k]??YEDEK[k]??k).replace(/\{(\w+)\}/g,(m,a)=>v&&v[a]!==undefined?v[a]:m);
function ilkDil(){const kayitli=hafiza('arayuz_dili');if(DILLER.some(d=>d[0]===kayitli))return kayitli;
 for(const l of navigator.languages||[]){const k=l.toLowerCase().split('-')[0];const e=ESDEGER[k]||k;if(DILLER.some(d=>d[0]===e))return e;}return 'tr';}
async function dilYukle(k){const [s,y]=await Promise.all([api('/arayuz_dili/'+k+'.json'),Object.keys(YEDEK).length?YEDEK:api('/arayuz_dili/en.json')]);
 YEDEK=y;S=s;dil=k;hafiza('arayuz_dili',k);const d=DILLER.find(d=>d[0]===k);
 document.documentElement.lang=k;document.documentElement.dir=d[3]||'ltr';document.title=t('baslik');
 document.querySelectorAll('[data-t]').forEach(e=>e.textContent=t(e.dataset.t));
 document.querySelectorAll('[data-t-ph]').forEach(e=>e.placeholder=t(e.dataset.tPh));
 document.querySelectorAll('[data-t-val]').forEach(e=>e.value=t(e.dataset.tVal));
 document.querySelectorAll('[data-t-bas]').forEach(e=>e.textContent=t(e.dataset.tBas).split(/[:：]/)[0].trim());
 document.querySelectorAll('[data-sekme-t]').forEach(e=>e.textContent=t(e.dataset.sekmeT).replace(/^\d+\.\s*/,'').split(/[:：]/)[0].trim());
 document.querySelectorAll('[data-t-title]').forEach(e=>{e.title=t(e.dataset.tTitle);e.setAttribute('aria-label',e.title);});
 document.querySelectorAll('#bayraklar button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.dil===k));
 $('dil_dugme').innerHTML=`${KURE}<img src="/bayrak/${d[1]}.svg" alt=""><span>${k.toUpperCase()}</span>`;$('dil_dugme').title=d[2];$('dil_dugme').setAttribute('aria-label',d[2]);
 $('tmetin_ipucu').textContent=t('tmetin_ipucu',{dugme:t('oku')});
 dosyaAdi();ornekDoldur();sesListesi();cesitCiz();okumaCiz();klonCiz();klonBilgi();sureCiz();
 for(const id of ['d_tasarla','d_oku','d_klon'])durumYaz($(id),$(id)._son);}
// Sekmeler: tıklanan bölüm görünür, diğerleri gizli; son sekme hatırlanır.
function sekmeAc(id){document.querySelectorAll('.sekmeler button').forEach(b=>b.setAttribute('aria-selected',b.dataset.sekme===id));
 document.querySelectorAll('.kart>.panel').forEach(p=>p.hidden=p.id!==id);hafiza('sekme',id);}
document.querySelector('.sekmeler').onclick=e=>{const b=e.target.closest('button[data-sekme]');if(b)sekmeAc(b.dataset.sekme);};
sekmeAc(['p1','p2','p3','p4'].includes(hafiza('sekme'))?hafiza('sekme'):'p1');
// Dil seçimi: tema düğmesinin yanındaki düğme çerçeveyi açar; dışarı tıklama ya da Esc kapatır.
const KURE='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>';
$('bayraklar').innerHTML=DILLER.map(([k,b,a])=>`<button type="button" data-dil="${k}" lang="${k}" aria-pressed="false"><img src="/bayrak/${b}.svg" alt=""><span>${a}</span></button>`).join('');
function dilPanel(ac){$('bayraklar').hidden=!ac;$('dil_dugme').setAttribute('aria-expanded',ac);}
$('dil_dugme').onclick=e=>{e.stopPropagation();dilPanel($('bayraklar').hidden);};
$('bayraklar').onclick=e=>{const b=e.target.closest('button[data-dil]');if(!b)return;dilPanel(false);if(b.dataset.dil!==dil)dilYukle(b.dataset.dil);};
document.addEventListener('click',e=>{if(!e.target.closest('.dilkutu'))dilPanel(false);});
document.addEventListener('keydown',e=>{if(e.key==='Escape')dilPanel(false);});

const GUNES='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
const AY='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
function temaCiz(){$('tema').innerHTML=document.documentElement.dataset.tema==='acik'?AY:GUNES;}
$('tema').onclick=()=>{const k=document.documentElement.dataset.tema==='acik'?'koyu':'acik';document.documentElement.dataset.tema=k;hafiza('tema',k);temaCiz();};
temaCiz();

// Sunucu kodlu sorun ve durum gönderir; arayüz kendi dilinde yazar, kodu bilmezse sunucunun metnini gösterir.
// The server sends coded problems and states; the UI phrases them, falling back to the server text.
const sorunMetni=s=>s.kod&&(S['e_'+s.kod]||YEDEK['e_'+s.kod])?t('e_'+s.kod,s.veri):s.metin;
function durumYaz(el,j){el._son=j;if(!j){el.textContent='';el.className='durum';return;}
 const hata=j.durum==='hata'||(!j.durum&&j.hata);let m;
 if(j.sorunlar&&j.sorunlar.length)m=(j.durum==='hata'?t('hata')+': ':'')+j.sorunlar.map(sorunMetni).join('\n');
 else if(j.kod&&(S['d_'+j.kod]||YEDEK['d_'+j.kod]))m=t('d_'+j.kod,j.veri);else m=j.mesaj||j.hata||j.durum;
 el.textContent=m;el.className='durum '+(hata?'hata':j.durum==='bitti'?'ok':'');}

let ornekler=[];
const DIL_ADI=k=>(DILLER.find(d=>d[0]===k)||[k,k,k])[2];
function ornekDoldur(){const s=$('ornek'),secili=s.value;s.innerHTML='';const bos=document.createElement('option');bos.value='';bos.textContent=t('kendim');s.appendChild(bos);
 const sira=o=>o.dil===dil?0:o.dil==='en'?1:2;  // önce arayüz dili, sonra İngilizce, sonra diğerleri
 const gruplar={};for(const o of [...ornekler].sort((a,b)=>sira(a)-sira(b))){let g=gruplar[o.dil];if(!g){g=gruplar[o.dil]=document.createElement('optgroup');g.label=`━━  ${DIL_ADI(o.dil)} · ${ornekler.filter(x=>x.dil===o.dil).length}  ━━`;s.appendChild(g);}
  const e=document.createElement('option');e.value=o.id;e.textContent=dil==='tr'?o.ad_tr:o.ad_en;g.appendChild(e);}
 s.value=secili;}
$('ornek').addEventListener('change',()=>{const o=ornekler.find(o=>o.id===$('ornek').value);if(!o)return;
 $('tarif').value=o.tarif;$('tasarim_metni').value=o.metin;if(!$('ad').value.trim()||ornekler.some(x=>x.id===$('ad').value))$('ad').value=o.id;sureGuncelle();});

// Tasarım metni kısa bir örnektir (1-2 cümle). Süre tahmini ve sınır sunucuda tek yerde (tasarla.estimate_seconds,
// dile göre karakter hızı); arayüz yalnız çizer. 20 sn üstü kırmızı, %10 pay (sert sınır) üstünde Tasarla başlamaz.
// The design text is a short sample. The estimate and limits live on the server (one place); the UI only draws them.
let sure=null,sureSayac=0,sureZaman=null;
const sureOlc=metin=>api('/api/sure',{metin,ornek:$('ornek').value});
async function sureSimdi(){clearTimeout(sureZaman);const n=++sureSayac;const s=await sureOlc($('tasarim_metni').value);
 if(n===sureSayac){sure=s;sureCiz();}return s;}
function sureGuncelle(){clearTimeout(sureZaman);sureZaman=setTimeout(()=>sureSimdi().catch(()=>{}),250);}
function sureCiz(){const s=sure,bos=!$('tasarim_metni').value.trim();$('sure').hidden=!s||bos;$('uzun_uyari').hidden=!s||bos||s.sn<=s.sert;
 if(!s||bos)return;$('sure').classList.toggle('asti',s.sn>s.sinir);$('sure_cubuk').style.width=Math.min(100,s.sn/s.sinir*100)+'%';
 $('sure_yazi').textContent=t('sure_gosterge',{sn:Math.max(1,Math.round(s.sn)),sinir:Math.round(s.sinir)});}
$('tasarim_metni').addEventListener('input',sureGuncelle);
// Form değişince eski hata yazısı kalmasın (ör. ad girildikten sonra "Sesin adı boş").
// A stale error must not stay once the form changes (e.g. "name is empty" after typing a name).
['ad','tarif','tasarim_metni','cesit','ornek'].forEach(id=>$(id).addEventListener('input',()=>{const d=$('d_tasarla');if(d.classList.contains('hata'))durumYaz(d,null);}));
// Uzun metni okumaya taşı: tam metin cümle cümle okuma kutusuna (boşsa yerine, doluysa sonuna); tasarımda ilk 1-2 cümle kalır.
const cumleler=m=>m.replace(/([.!?…؟।。！？])[ \t]+/g,'$1\n').replace(/([。！？])(?=\S)/g,'$1\n').split('\n').map(x=>x.trim()).filter(Boolean);
$('okumaya_tasi').onclick=async()=>{const m=$('tasarim_metni').value.trim();if(!m)return;const c=cumleler(m),o=$('okuma_metni');
 sekmeAc('p2');defterNo();const s=o.value.trim()?o.value.replace(/\s+$/,'').split('\n'):[],yS=[...s,...c];
 Satir.uygula(yS,[...s.map((_,i)=>Durak.dur[i]??null),...c.map(()=>null)],[yS.length-1,yS[yS.length-1].length],Satir.aralik(s.length,c.length),'');
 const ayrac=/[぀-ヿ一-鿿]/.test(m)?'':' ';let kalan=c.slice(0,2).join(ayrac);
 if(c.length>1){try{const s=await sureOlc(kalan);if(s.sn>s.sinir)kalan=c[0];}catch(e){kalan=c[0];}}
 $('tasarim_metni').value=kalan;durumYaz($('d_tasarla'),null);sureSimdi().catch(()=>{});
};

let sesler={hazir:[],tasarlanan:[]};
const tanitim=k=>dil==='tr'?k.tanitim_tr:(k.tanitim_en||k.tanitim_tr);
function sesListesi(){const s=$('ses'),secili=s.value;s.innerHTML='';
 for(const k of sesler.tasarlanan){const o=document.createElement('option');o.value=k.kimlik;o.textContent=t('etiket',{ad:t('tasarlanan'),deger:k.kimlik+' · '+t('tohum_n',{n:k.okuma_tohumu})});s.appendChild(o);}
 for(const k of sesler.hazir){const o=document.createElement('option');o.value=k.kimlik;o.textContent=t('etiket',{ad:t('hazir_ses'),deger:k.gorunen_ad+' · '+(tanitim(k)||'').slice(0,60)});s.appendChild(o);}
 if(secili)s.value=secili;
 $('hazir').innerHTML=sesler.hazir.map(k=>`<div class="cesit"><div style="flex:1"><b>${esc(k.gorunen_ad)}</b> <small>${esc(t('tohum_n',{n:k.okuma_tohumu}))}</small><br><small>${esc(tanitim(k))}</small></div>`+
  `<audio controls preload="none" src="/dosya/${esc(k.kimlik)}/${esc(k.ornek_okuma||k.referans)}"></audio></div>`).join('');}
async function yenile(secili){sesler=await api('/api/sesler');sesListesi();cesitCiz();if(secili)$('ses').value=secili;}
// İlerleme: düğmenin yanında kronometre + çubuk. Model yüklenirken çubuk kayar, sonra hazır/toplam ile dolar.
// Progress: stopwatch + bar beside the button; sliding while the model loads, then filled by done/total.
function ilerle(p){if(!p)return null;const t0=Date.now(),k=p.querySelector('.krono'),i=p.querySelector('i');
 const yaz=()=>{const s=Math.floor((Date.now()-t0)/1000);k.textContent=Math.floor(s/60)+':'+String(s%60).padStart(2,'0');};
 p.hidden=false;p.classList.add('bekler');i.style.width='';yaz();const z=setInterval(yaz,1000);
 return{j(j){const v=j.veri||{};if(j.kod==='ilerleme'&&v.total){p.classList.remove('bekler');i.style.width=Math.max(4,100*v.done/v.total)+'%';}},
  son(ok){clearInterval(z);p.classList.remove('bekler');i.style.width=ok?'100%':'0';}};}
async function bekle(is,el,p){const g=ilerle(p);for(;;){const j=await api('/api/is/'+is);durumYaz(el,j);if(g)g.j(j);
 if(j.durum==='bitti'||j.durum==='hata'){if(g)g.son(j.durum==='bitti');return j;}await new Promise(r=>setTimeout(r,1000));}}

let sonCesit=null,sonOkuma=null,sonKlon=null;
// Üretim = bir Tasarla basışı: aynı ad, tarih, tarif ve metinle çıkan çeşitler. Diskten gelir (sesler.tasarlanan), en yeni üstte.
let seciliUretim=null;
function uretimler(){const g=new Map();
 for(const c of sesler.tasarlanan){const k=c.uretim?c.ad+'|'+c.uretim:[c.ad,c.tarih,c.ses_yaratici_ingilizce_prompt,c.ses_yaratilirken_okutulan_metin].join('|');if(!g.has(k))g.set(k,[]);g.get(k).push(c);}
 return [...g].map(([k,cs])=>({k,cs:cs.sort((a,b)=>a.cesit-b.cesit)})).sort((a,b)=>(b.cs[0].tarih||'').localeCompare(a.cs[0].tarih||'')||b.cs[0].cesit-a.cs[0].cesit);}
function cesitCiz(){const secili=(document.querySelector('input[name=sec]:checked')||{}).value,u=uretimler();
 if(!u.some(x=>x.k===seciliUretim))seciliUretim=u.length?u[0].k:null;
 $('uretim').innerHTML=u.map(x=>`<option value="${esc(x.k)}">${esc(x.cs[0].gorunen_ad||x.cs[0].ad)} · ${esc((x.cs[0].tarih||'').slice(5))} · ${esc(t('cesit_kisa'))} ${x.cs.length}</option>`).join('');
 $('uretim').value=seciliUretim||'';$('uretim').hidden=!u.length;
 const hatalar=(sonCesit?sonCesit.cesitler:[]).filter(c=>c.hata).map(c=>`<div class="cesit hata">${esc(t('tohum_n',{n:c.tohum}))}: ${esc(c.hata)}</div>`);
 const kartlar=((u.find(x=>x.k===seciliUretim)||{cs:[]}).cs).map(c=>`<div class="cesit"><div class="csat"><label><input type="radio" name="sec" value="${esc(c.kimlik)}"><b>${esc(t('cesit_n',{n:c.cesit}))}</b> <small>${esc(t('tohum_n',{n:c.tasarim_tohumu}))}, ${esc(t('sn',{n:c.referans_sn}))}</small></label><button type="button" class="okubtn" data-oku="${esc(c.kimlik)}">${esc(t('oku'))}</button></div><audio controls preload="none" src="/dosya/${esc(c.kimlik)}/referans.wav"></audio></div>`);
 $('cesitler').innerHTML=hatalar.concat(kartlar).join('')||`<p class="bos">${esc(t('uretim_yok',{dugme:t('tasarla')}))}</p>`;
 document.querySelectorAll('input[name=sec]').forEach(r=>{r.checked=r.value===secili;r.onchange=()=>{$('ses').value=r.value;};});
 document.querySelectorAll('[data-oku]').forEach(b=>b.onclick=()=>{const r=document.querySelector(`input[name=sec][value="${b.dataset.oku}"]`);if(r)r.checked=true;
  $('ses').value=b.dataset.oku;sekmeAc('p2');$('okuma_metni').focus();});}
// Üretim seçilince form o üretimin ad, tarif ve metniyle dolar; çeşitleri listelenir, ilki okumada seçili ses olur.
function uretimAc(k){const x=uretimler().find(x=>x.k===k);if(!x)return;seciliUretim=k;const c=x.cs[0];
 $('ad').value=c.gorunen_ad||c.ad;$('tarif').value=c.ses_yaratici_ingilizce_prompt||'';$('tasarim_metni').value=c.ses_yaratilirken_okutulan_metin||'';$('ornek').value='';$('cesit').value=x.cs.length;
 sureGuncelle();cesitCiz();const ilk=document.querySelector('input[name=sec]');if(ilk){ilk.checked=true;$('ses').value=ilk.value;}}
$('uretim').onchange=()=>uretimAc($('uretim').value);
$('btn_tasarla').onclick=async()=>{const b=$('btn_tasarla');b.disabled=true;
 const u=await sureSimdi().catch(()=>null);if(u&&u.sn>u.sert){b.disabled=false;$('okumaya_tasi').focus();return;}  // sınır aşıldı: üretim başlamaz
 sonCesit=null;cesitCiz();
 const j=await api('/api/tasarla',{ad:$('ad').value,tarif:$('tarif').value,metin:$('tasarim_metni').value,cesit:+$('cesit').value,ornek:$('ornek').value});
 if(j.hata){durumYaz($('d_tasarla'),j);if((j.sorunlar||[]).some(x=>x.kod==='tasarim_uzun'))$('uzun_uyari').hidden=false;b.disabled=false;return;}
 const s=await bekle(j.is,$('d_tasarla'),$('p_tasarla'));b.disabled=false;if(s.durum!=='bitti')return;
 sonCesit=s.sonuc;seciliUretim=null;await yenile();const ilk=document.querySelector('input[name=sec]');if(ilk){ilk.checked=true;$('ses').value=ilk.value;}};

const indir=(yol,ad)=>`<a href="${yol}" download="${esc(ad)}"><button>${esc(t('indir'))}</button></a>`;
const ozet=r=>t('okuma_ozet',{ses:r.ses_sn,sure:r.sure_sn,vram:r.vram_tepe_mb,tohum:r.tohum});
function okumaCiz(){const r=sonOkuma;if(!r)return;
 $('sonuc').innerHTML=`<audio controls src="/okuma/${r.is}/okuma.wav"></audio> ${indir('/okuma/'+r.is+'/okuma.wav','okuma.wav')}<div><small>${esc(ozet(r))}</small></div>`;}
// ── Açılır menü: tek kap (#acilir), iki sahip (Durak, Satir) ──────────────────────────────────────────────────
// Konum, kapanma (dışarı tık, Esc, kaydırma, pencere boyu), odak dönüşü, klavye, rol ve ortak parçalar yalnız burada.
// One popup container shared by the pause menu and the line menu: position, closing, focus, keys, roles, shared parts.
const rtl=()=>document.documentElement.dir==='rtl',ok=()=>rtl()?'←':'→';
// Süre: Batı rakamı, dilin ondalık işareti ve birimi (sn anahtarı) / Western digits, the language's decimal mark and unit
const sn=x=>x.toLocaleString((document.documentElement.lang||'en')+'-u-nu-latn'),snb=x=>t('sn',{n:sn(x)});
const Acilir={sahip:null,x:0,sessiz:false,
 acikMi(){return !$('acilir').hidden;},
 secikSil(){document.querySelectorAll('#bantlar .secik,#satirno .secik').forEach(e=>{e.classList.remove('secik');e.setAttribute('aria-expanded','false');});},
 ac(tetik,x,html,sahip,etiket){const m=$('acilir');m.removeAttribute('aria-describedby');if(this.sahip&&this.sahip!==sahip)this.sahip.kapandi();this.sahip=sahip;this.x=x;
  this.secikSil();tetik.classList.add('secik');tetik.setAttribute('aria-expanded','true');
  m.innerHTML=html;m.setAttribute('role','menu');m.setAttribute('aria-label',etiket);m.hidden=false;
  const r=tetik.getBoundingClientRect(),w=m.offsetWidth,h=m.offsetHeight,sol=rtl()?x-w:x;
  m.style.left=Math.max(8,Math.min(sol,innerWidth-w-8))+'px';m.style.top=(r.bottom+4+h<innerHeight-8?r.bottom+4:Math.max(8,r.top-h-4))+'px';
  (m.querySelector('[data-sec][aria-checked=true]')||this.ogeler()[0])?.focus({preventScroll:true});},
 // odak: true → odak metin kutusuna döner (seçim, Esc); dışarı tıklamada tıklanan yerde kalır.
 kapat(odak){const m=$('acilir');if(m.hidden)return;m.hidden=true;const s=this.sahip;this.sahip=null;this.secikSil();if(s)s.kapandi();
  if(odak)$('okuma_metni').focus({preventScroll:true});},
 ogeler(){return [...$('acilir').querySelectorAll('button:not([aria-disabled=true])')].filter(b=>b.offsetParent!==null);},
 // İçerik menüden diyaloğa dönünce (onay, sayı kutusu) kap rolü değişir; menü öğesi rolleri düz düğmeye iner.
 // When the content becomes a dialog (confirm, number box) the container role changes and menu item roles are dropped.
 diyalog(rol){const m=$('acilir');m.setAttribute('role',rol);
  m.querySelectorAll('[role^=menuitem]').forEach(b=>{const c=b.getAttribute('aria-checked');b.removeAttribute('role');if(c!==null){b.removeAttribute('aria-checked');b.setAttribute('aria-pressed',c);}});},
 baslik:(no,metin)=>`<div class="baslik" aria-hidden="true"><b>${no}</b><span>${esc(metin)}</span></div>`,
 onay:(soru,ayrinti,evet,notr)=>`<div class="onay${notr?' notr':''}"><span id="acilir_soru">${esc(soru)}</span>${ayrinti?`<small id="acilir_ayrinti">${esc(ayrinti)}</small>`:''}`
  +`<div><button type="button" class="hayir">${esc(t('hayir'))}</button><button type="button" class="evet" data-evet="${esc(evet)}">${esc(t('evet'))}</button></div></div>`,
 onayAc(yer,html){yer.outerHTML=html;const m=$('acilir');this.diyalog('alertdialog');m.setAttribute('aria-describedby',m.querySelector('#acilir_ayrinti')?'acilir_soru acilir_ayrinti':'acilir_soru');
  m.querySelector('.onay .hayir').focus({preventScroll:true});},
 // Dişli kalıbı: düğme (simge ya da yazı) + gizli sayı kutusu + ✓. Yazılı düğmede kutu metin (imleç sona konabilsin).
 // Gear pattern: button + hidden number box + ✓; the labelled variant uses a text box so the caret can go to the end.
 sayiKutusu:(min,max,adim,deger,birim,etiket,neden)=>'<div class="ozel">'+(etiket?`<button type="button" role="menuitem" class="disli oge"${neden?` aria-disabled="true" title="${esc(neden)}"`:''}>${esc(etiket)}</button>`
  +`<input type="text" inputmode="numeric" value="${deger}" aria-label="${esc(etiket)}" hidden>`
  :`<button type="button" role="menuitem" class="disli" title="${sn(min)} – ${esc(snb(max))}" aria-label="${sn(min)} – ${esc(snb(max))}">${DISLI}</button>`
  +`<input type="number" min="${min}" max="${max}" step="${adim}" value="${deger}" aria-label="${sn(min)} – ${esc(snb(max))}" hidden>`)
  +`${birim?`<small hidden>${esc(birim)}</small>`:''}<button type="button" class="tamam" aria-label="✓" hidden>✓</button></div>`,
 sayiAc(o,rakam){o.querySelectorAll('[hidden]').forEach(x=>x.hidden=false);this.diyalog('dialog');const g=o.querySelector('input');g.focus();
  if(rakam===undefined)return g.select();g.value=rakam;try{g.setSelectionRange(g.value.length,g.value.length);}catch(e){}},
 kur(){const m=$('acilir'),ta=$('okuma_metni');
  m.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||!this.sahip)return;e.stopPropagation();if(b.getAttribute('aria-disabled')==='true')return;
   if(b.classList.contains('disli'))return this.sayiAc(b.parentElement);
   if(b.classList.contains('tamam'))return this.sahip.gir();
   this.sahip.tikla(e,b);});
  m.addEventListener('keydown',e=>{if(!this.sahip||e.isComposing)return;
   if(e.key==='Enter'&&e.target.matches('.ozel input')){e.preventDefault();return this.sahip.gir();}
   if((e.key==='ArrowDown'||e.key==='ArrowUp')&&!e.target.matches('input')){e.preventDefault();const o=this.ogeler(),k=o.indexOf(document.activeElement);
    o[(k+(e.key==='ArrowDown'?1:-1)+o.length)%o.length]?.focus();return;}
   if(/^[0-9]$/.test(e.key)&&!e.target.matches('input')){const o=m.querySelector('.ozel .oge:not([aria-disabled=true])');if(o){e.preventDefault();this.sayiAc(o.parentElement,e.key);}}});
  document.addEventListener('click',e=>{if(this.acikMi()&&!e.target.closest('#acilir'))this.kapat();});
  // Tek Esc dinleyicisi: önce süren sürükleme iptal, yoksa menü kapanır / one Escape listener
  document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;if(Satir.suruk){e.preventDefault();return Satir.iptal();}if(this.acikMi()){e.preventDefault();this.kapat(true);}});
  // Metin kayınca bantlar yer değiştirir: menü kapanır (satırı görünür yapan kendi kaydırmamız hariç); pencere boyu da öyle.
  ta.addEventListener('scroll',()=>{if(this.sessiz)this.sessiz=false;else this.kapat();});addEventListener('resize',()=>this.kapat());}};
// ── Duraklar: tek modül ─────────────────────────────────────────────────────────────────────────────────
// İki cümle arasındaki bekleme. Tek kaynak: dur[i] = null (varsayılan) ya da saniye; bant cümlenin malıdır (cümle
// taşınınca yanında gider). Menü listesi her bant için aynıdır (hazır süreler + kişinin süreleri, ♥ favoriler üstte).
// Metne '||' yazılmaz: yazılan ya da yapıştırılan işaret banda dönüşür (geri alınabilir), okurken saniye olarak eklenir.
// Boş satırın anlamı yok: paragraf = 1 sn ve üstü bant (yapıştırma, Enter-Enter ve açılışta boş satır banda çevrilir).
// Pauses between sentences. Single source: dur[i] = null (default) or seconds; the band belongs to its sentence.
// Markers never stay in the text. Blank lines carry no meaning in the box: a paragraph is a band of 1 s or more.
const Durak={
 HAZIR:{bagli:.25,normal:.5,paragraf:1,agir:1.5},VARSAYILAN:.35,EN_COK:5,EN_COK_OZEL:6,
 IZ:/\s*\|\|\s*(bagli|normal|paragraf|agir|\d+(?:[.,]\d+)?)\s*s?\s*$/,
 dur:[],eski:[],acik:null,gecmis:new Map(),tur:null,bekleyen:null,
 // ad ('agir') ya da yazı ('0,8') → 0-5 sn, 2 basamak / name or text → seconds
 saniye(v){const n=v in this.HAZIR?this.HAZIR[v]:parseFloat(String(v).replace(',','.'));return Math.min(this.EN_COK,Math.max(0,Math.round(n*100)/100));},
 hazirlar(){return [this.VARSAYILAN,...Object.values(this.HAZIR)];},
 oku(k){try{return (JSON.parse(hafiza(k)||'[]')||[]).map(v=>this.saniye(v===''?this.VARSAYILAN:v)).filter(isFinite);}catch(e){return [];}},
 yaz(k,a){hafiza(k,JSON.stringify([...new Set(a)]));},
 // Yalnız menüdeki ⚙ ile girilen süre kalıcı listeye eklenir (elle ya da yapıştırılan işaret eklenmez).
 ozelEkle(n){if(!this.hazirlar().includes(n))this.yaz('durak_ozel',[n,...this.oku('durak_ozel').filter(x=>x!==n)].slice(0,this.EN_COK_OZEL));},
 sure(i){return this.dur[i]??this.VARSAYILAN;},
 // Satır sonundaki işaret ('|| 0.7'): geçerliyse {m,v}, değilse (0-5 dışı, yarım '0.', bilinmeyen ad) null. / valid marker
 deger(l){const m=l.match(this.IZ);if(!m)return null;const v=m[1] in this.HAZIR?this.HAZIR[m[1]]:parseFloat(m[1].replace(',','.'));
  return v<=this.EN_COK?{m,v:Math.round(v*100)/100}:null;},
 // Sunucunun reddedeceği işaret banda çevrilmez, kırpılmaz: metinde kalır, satır kırmızı, okuma gönderilmez.
 hatali(l){return l.includes('||')&&!this.deger(l);},
 hatalar(){return $('okuma_metni').value.split('\n').map((l,i)=>this.hatali(l)&&i!==this.bekleyen?{i,durak:l.slice(l.lastIndexOf('||')+2).trim()||'—'}:null).filter(Boolean)
  .map(h=>({kod:'durak',veri:{durak:h.durak,secenekler:Object.keys(this.HAZIR).join(', ')+', 0-'+snb(this.EN_COK)},metin:`${h.i+1}: ${h.durak}`,i:h.i}));},
 // Bekleyen işaret imleç satırdan çıkınca, metinden ayrılınca ve pencere odağı gidince banda taşınır (kapıdan, geri alınabilir).
 bekleyenTasi(hepsi){const ta=$('okuma_metni'),i=this.bekleyen;if(i==null||Satir.yaziyor)return;
  if(!hepsi&&ta.value.slice(0,ta.selectionStart).split('\n').length-1===i)return;
  this.bekleyen=null;this.tur=null;if(!this.isaretTasi(ta))defterNo();},
 // Okumaya giden metin. Sunucu boş satırı paragraf sayar; kutuda boş satır etkisiz olduğu için önündeki bantsız cümleye
 // açık varsayılan yazılır. Son cümleden sonraki bekleme uygulanmaz: askıdaki bant yazılmaz.
 metin(){const s=$('okuma_metni').value.split('\n'),dolu=s.map(l=>!!l.trim()),son=dolu.lastIndexOf(true);
  return s.map((l,i)=>{if(!dolu[i]||i===son||l.includes('||'))return l;const d=this.dur[i]??(dolu[i+1]===false?this.VARSAYILAN:null);
   return d==null?l:l.replace(/\s+$/,'')+' || '+d;}).join('\n');},
 // Metin → bant anlık görüntüsü (en çok 100): Ctrl+Z / Ctrl+Y metni geri getirince bantlar da aynı adımda döner.
 // Yalnız satır işlemi, bant seçimi/silmesi ve satır sayısını değiştiren yazımda yazılır (düz yazma harita doldurmaz).
 anlik(){const k=$('okuma_metni').value;this.gecmis.delete(k);this.gecmis.set(k,this.dur.slice());
  if(this.gecmis.size>100)this.gecmis.delete(this.gecmis.keys().next().value);},
 // Durakları yeni satırlarla eşler (saf, this.eski/this.dur'dan): değişmeyen baş ve son satırlar durağını korur,
 // değişen bölge sondan eşlenir (satır bölme/birleştirmede durak cümlenin sonunda kalır).
 esle(s){const e=this.eski,d=this.dur,n0=e.length,n1=s.length;let p=0,q=0;
  while(p<n0&&p<n1&&e[p]===s[p])p++;while(q<n0-p&&q<n1-p&&e[n0-1-q]===s[n1-1-q])q++;
  return s.map((_,i)=>(i<p?d[i]:i>=n1-q?d[i-n1+n0]:(n1-q-1-i<n0-q-p?d[n0-q-1-(n1-q-1-i)]:null))??null);},
 // Geri al/yinele: metin haritadaysa bantlar oradan; değilse fark eşlemesi.
 hizala(ta){const s=ta.value.split('\n');
  if(/^history/.test(this.tur||'')){const g=this.gecmis.get(ta.value);if(g){this.eski=s;this.dur=s.map((_,i)=>g[i]??null);return s;}}
  const n0=this.eski.length;this.dur=this.esle(s);this.eski=s;if(s.length!==n0)this.anlik();return s;},
 // Elle yazılan '|| x' işareti banda taşınır; tek kapıdan yazılır (Ctrl+Z çalışır). Rakam yazılırken (imleç işaretin
 // sonunda) beklenir: '|| 0.7' yazarken '|| 0' anında bant olmaz; boşluk, Enter ya da başka yerde yazınca taşınır.
 isaretTasi(ta){const c=ta.selectionStart,isaret={};let sil=0,bas=0;const s0=ta.value.split('\n');this.bekleyen=null;
  const s=s0.map((l,i)=>{const g=this.deger(l),b=bas,yaz=this.tur==='insertText'&&c===b+l.length;bas+=l.length+1;
   if(!g||(yaz&&/\d$/.test(l))){if(yaz&&l.includes('||'))this.bekleyen=i;return l;}const m=g.m;
   isaret[i]=g.v;if(c>b+m.index)sil+=Math.min(c-b-m.index,m[0].length);return l.slice(0,m.index);});
  const k=Object.keys(isaret).map(Number);if(!k.length)return false;
  this.dur=this.esle(s0);this.eski=s0;const d=this.dur.slice();k.forEach(i=>d[i]=isaret[i]);
  Satir.uygula(s,d,Satir.konum(s,c-sil),k,t('durak_eklendi',{n:k[0]+1,sure:snb(isaret[k[0]])}));return true;},
 // Boş satırın emekliliği (saf): '|| x' işareti banda taşınır; boş satır dizisi silinir, üstündeki cümle bantsızsa 1 sn
 // olur (açık değer kazanır). Baştaki boşlar atılır; sondakiler yalnız arkada dolu satır varsa bant olur.
 emekli(o,sonraDolu){const k=[],isaret=[];let imlec=null;
  for(const e of o){const m=e.l.match(this.IZ);if(m){e.d=this.saniye(m[1]);e.l=e.l.slice(0,m.index);isaret.push(e.d);if(e.imlec!=null)e.imlec=Math.min(e.imlec,e.l.length);}
   if(e.l.trim()){k.push(e);continue;}const u=k[k.length-1];if(u)u.bos=true;if(e.imlec!=null)imlec=u||'bas';}
  k.forEach((e,i)=>{if(e.bos&&e.d==null&&(i<k.length-1||sonraDolu))e.d=this.HAZIR.paragraf;delete e.bos;});
  return {k,isaret,imlec};},
 bosEmekli(s,d){const r=this.emekli(s.map((l,i)=>({l,d:d[i]??null})),false);if(!r.k.length)r.k.push({l:'',d:null});
  return {s:r.k.map(e=>e.l),d:r.k.map(e=>e.d),isaret:r.isaret};},
 // Sayfa açılışı: tarayıcının geri getirdiği metindeki işaret ve boş satırlar banda çevrilir (geri alma geçmişi henüz yok).
 acilis(){const ta=$('okuma_metni'),s=this.hizala(ta),r=this.bosEmekli(s,this.dur);
  if(r.s.join('\n')!==ta.value){ta.value=r.s.join('\n');this.dur=r.d;this.eski=r.s;}this.anlik();defterNo();},
 // Numara sütunu ve bant katmanı için çizim (h: satır yükseklikleri, B: bant yüksekliği). Son cümlenin bandı uygulanmaz;
 // değeri varsa kesik çizgili "askıda" bant olarak görünür (cümle yukarı taşınınca yerine döner). 1 sn ve üstü belirgin.
 ciz(s,h,B){const dolu=s.map(l=>!!l.trim()),p=Satir.isik();let alt=6,oluk='',bant='';
  h.forEach((x,k)=>{alt+=x;if(!dolu[k])return;const j=dolu.indexOf(true,k+1),askida=j<0,g=this.deger(s[k]);if(askida&&this.dur[k]==null&&!g)return;
   const z=g?g.v:this.sure(k),ust=alt-B/2,ad=`${k+1} ${ok()} ${askida?'—':j+1} · ${snb(z)}`+(askida?' · '+t('durak_son'):''),v=p.k.has(k),
    tur=(this.dur[k]!=null||g?'a':z===this.VARSAYILAN?'v':'o')+(z>=1?' p':'')+(askida?' askida':'')+(this.acik===k?' secik':'')+(v?' parla':'')+(this.hatali(s[k])&&k!==this.bekleyen?' yanlis':'');
   if(!askida)oluk+=`<div class="gbant${z>=1?' p':''}" style="top:${ust}px"></div>`;
   bant+=`<button type="button" class="durak ${tur}" data-i="${k}" data-j="${askida?'':j}" style="top:${ust}px${v?p.gecikme:''}" title="${esc(ad)}" aria-label="${esc(ad)}" aria-haspopup="menu" aria-expanded="${this.acik===k}">${this.cubuk(z)}</button>`;});
  return {oluk,bant};},
 cubuk:z=>`<i style="width:${Math.min(z,3)*48}px"></i>`,
 // Menü: üstte hangi iki satırın arası; liste her bantta aynı, o bandın süresi çerçeveli; tıklanan yerin altında açılır.
 menu(b,x){if($('okuma_metni').value.split('\n').some(l=>this.deger(l))){const k=b.dataset.i;this.bekleyen=null;this.tur=null;
   this.isaretTasi($('okuma_metni'));b=document.querySelector(`#bantlar .durak[data-i="${k}"]`);if(!b)return;}
  const i=+b.dataset.i,j=b.dataset.j,s=$('okuma_metni').value.split('\n'),z=this.sure(i),ara=`${i+1} ${ok()} ${j===''?'—':+j+1}`;this.acik=i;
  const ozel=this.oku('durak_ozel'),fav=this.oku('durak_fav'),hepsi=[...new Set([...this.hazirlar(),...ozel,z])].sort((a,c)=>a-c);
  const satir=n=>`<div class="satir" role="group"><button type="button" role="menuitemradio" data-sec="${n}" aria-checked="${n===z}">${this.cubuk(n)}<span>${esc(snb(n))}</span></button>`
   +`<button type="button" role="menuitemcheckbox" class="kalp${fav.includes(n)?' dolu':''}" data-fav="${n}" aria-checked="${fav.includes(n)}" aria-label="♥ ${esc(snb(n))}">${KALP}</button>`
   +(ozel.includes(n)&&!this.hazirlar().includes(n)?`<button type="button" role="menuitem" class="sil" data-sil="${n}" aria-label="${esc(t('durak_sil',{sure:snb(n)}))}">${CARPI}</button>`:'<span class="sil"></span>')+'</div>';
  const ust=hepsi.filter(n=>fav.includes(n)),alt=hepsi.filter(n=>!fav.includes(n));
  Acilir.ac(b,x,Acilir.baslik(ara,s[i])+ust.map(satir).join('')+(ust.length&&alt.length?'<hr>':'')+alt.map(satir).join('')
   +Acilir.sayiKutusu(0,this.EN_COK,0.05,z,t('sn',{n:''}).trim()),this,ara);},
 // Bant yeniden çizilince eski düğme kopar: menü aynı bandın yeni düğmesine göre yeniden kurulur.
 yenile(){const b=document.querySelector(`#bantlar .durak[data-i="${this.acik}"]`);if(b)this.menu(b,Acilir.x);else Acilir.kapat();},
 kapandi(){this.acik=null;},
 // Varsayılanla aynı süre işaret yazmaz (null); seçim ekran okuyucuya duyurulur / the choice is announced
 sec(n){const i=this.acik;this.dur[i]=n===this.VARSAYILAN?null:n;this.anlik();Acilir.kapat(true);defterNo();Satir.duyur(t('durak_eklendi',{n:i+1,sure:snb(this.sure(i))}));},
 gir(){const n=parseFloat(String($('acilir').querySelector('.ozel input').value).replace(',','.'));if(!isFinite(n))return;const d=this.saniye(n);this.ozelEkle(d);this.sec(d);},
 // Silmeden önce sorulur; metinde kullanılıyorsa kaç yerde olduğu ve döneceği süre söylenir.
 silSor(b,n){const yer=this.dur.filter(d=>d===n).length;
  Acilir.onayAc(b.closest('.satir'),Acilir.onay(t('durak_sil',{sure:snb(n)}),yer?t('durak_sil_yer',{n:yer,v:snb(this.VARSAYILAN)}):'',n));},
 sil(n){this.yaz('durak_ozel',this.oku('durak_ozel').filter(x=>x!==n));this.yaz('durak_fav',this.oku('durak_fav').filter(x=>x!==n));
  this.dur=this.dur.map(d=>d===n?null:d);this.anlik();defterNo();this.yenile();},
 tikla(e,b){const d=b.dataset;
  if(d.fav!==undefined){const f=this.oku('durak_fav'),n=+d.fav;this.yaz('durak_fav',f.includes(n)?f.filter(x=>x!==n):[...f,n]);return this.yenile();}
  if(d.sil!==undefined)return this.silSor(b,+d.sil);
  if(d.evet!==undefined)return this.sil(+d.evet);
  if(b.classList.contains('hayir'))return this.yenile();
  if(d.sec!==undefined)this.sec(+d.sec);},
 kur(){$('bantlar').addEventListener('click',e=>{const b=e.target.closest('.durak');if(b){e.stopPropagation();this.menu(b,e.clientX);}});
  const ta=$('okuma_metni');
  document.addEventListener('selectionchange',()=>{if(document.activeElement===ta)this.bekleyenTasi(false);});
  // Metin dışına basış ya da Tab: odak gitmeden (execCommand çalışırken) taşınır / before focus leaves
  document.addEventListener('pointerdown',e=>{if(document.activeElement===ta&&!$('defterkap').contains(e.target))this.bekleyenTasi(true);},true);
  ta.addEventListener('keydown',e=>{if(e.key==='Tab')this.bekleyenTasi(true);});
  ta.addEventListener('blur',()=>setTimeout(()=>{if(document.activeElement===ta)this.bekleyenTasi(true);else if(this.bekleyen!=null){this.bekleyen=null;defterNo();}}));}};
const KALP='<svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.4-9.2-8.6C1.2 8.2 3.1 4.8 6.6 4.8c2.1 0 3.6 1.2 5.4 3.2 1.8-2 3.3-3.2 5.4-3.2 3.5 0 5.4 3.4 3.8 6.6C19 15.6 12 20 12 20z"/></svg>';
const CARPI='<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
const DISLI='<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>';
// ── Satır işlemleri: numara = düğme (menü, sürükle); ekle, taşı, çoğalt, sil, yapıştır ─────────────────────────────
// Her işlem yeni metni ve yeni bantları birlikte hesaplar (hesapla, saf) ve tek kapıdan yazar (uygula): execCommand ile
// tarayıcının geri alma geçmişi korunur, bantlar Durak.gecmis ile aynı adımda döner. Numaraya taşı = araya girer.
// Line operations compute text and bands together (pure) and write them through one gate that keeps the undo history.
const Satir={acik:null,ust:[],boy:[],parla:{k:new Set(),son:0},zaman:0,bas:null,suruk:false,suruklendi:false,yaziyor:false,
 satirlar:()=>$('okuma_metni').value.split('\n'),
 ofs:(s,r,c)=>s.slice(0,r).reduce((a,l)=>a+l.length+1,0)+Math.min(c,(s[r]||'').length),
 konum(s,o){let r=0;while(r<s.length-1&&o>s[r].length){o-=s[r].length+1;r++;}return [r,o];},
 aralik:(a,n)=>Array.from({length:n},(_,k)=>a+k),
 // op: {tur:'ekle'|'tasi'|'cogalt'|'sil', a, b (blok sonu), yon:'ust'|'alt', hedef: bloğun yeni ilk satırı}
 hesapla(s,d,op){s=s.slice();d=s.map((_,i)=>d[i]??null);const a=op.a,b=op.b??op.a,n=b-a+1;
  if(op.tur==='ekle'){const k=op.yon==='ust'?a:a+1;s.splice(k,0,'');d.splice(k,0,null);return {s,d,imlec:[k,0],vurgu:[k],kay:0};}
  if(op.tur==='tasi'){const bs=s.splice(a,n),bd=d.splice(a,n),h=Math.max(0,Math.min(op.hedef,s.length));s.splice(h,0,...bs);d.splice(h,0,...bd);
   return {s,d,imlec:[h,0],vurgu:this.aralik(h,n),kay:h-a};}
  if(op.tur==='cogalt'){s.splice(b+1,0,...s.slice(a,b+1));d.splice(b+1,0,...d.slice(a,b+1));return {s,d,imlec:[b+1,0],vurgu:this.aralik(b+1,n),kay:n};}
  if(op.tur==='sil'){s.splice(a,n);d.splice(a,n);if(!s.length){s.push('');d.push(null);}const r=Math.max(0,a-1);
   return {s,d,imlec:a>0?[r,s[r].length]:[0,0],vurgu:[r],kay:0};}
  return null;},
 // Seçimin kapsadığı satırlar (seçim bir satırın başında bitiyorsa o satır dahil değil) / lines covered by the selection
 secim(){const ta=$('okuma_metni'),s=this.satirlar(),bas=this.konum(s,ta.selectionStart),son=this.konum(s,ta.selectionEnd);
  return {s,a:bas[0],b:son[0]>bas[0]&&son[1]===0?son[0]-1:son[0],bas,son};},
 // Seçim blokla birlikte kayar: [a,b] içindeki uçlar ve bloğun hemen altının başında biten seçim sonu (tam satır seçimi).
 // The selection moves with the block, including an end at the start of the line just below it (whole-line selection).
 secimKaydir(sec,a,b,kay){const k=([x,y],son)=>(x>=a&&x<=b)||(son&&x===b+1&&y===0)?[x+kay,y]:[x,y];return {bas:k(sec.bas),son:k(sec.son,true)};},
 // Yapıştırma (saf): a..b seçimi yerine metin; boş satırlar ve '|| x' işaretleri banda çevrilir.
 yapistir(s,d,a,b,metin){const [r1,c1]=this.konum(s,a),[r2,c2]=this.konum(s,b),P=metin.replace(/\r\n?/g,'\n').split('\n'),son=P.length-1;
  const o=P.map((p,k)=>({l:(k?'':s[r1].slice(0,c1))+p+(k===son?s[r2].slice(c2):''),d:null}));
  o[son].d=d[r2]??null;o[son].imlec=(son?0:c1)+P[son].length;
  const r=Durak.emekli(o,s.slice(r2+1).some(l=>l.trim())),k=r.k;
  const yS=[...s.slice(0,r1),...k.map(e=>e.l),...s.slice(r2+1)],yD=[...s.slice(0,r1).map((_,i)=>d[i]??null),...k.map(e=>e.d),...s.slice(r2+1).map((_,i)=>d[r2+1+i]??null)];
  if(!yS.length){yS.push('');yD.push(null);}
  const ki=k.findIndex(e=>e.imlec!=null);let imlec;
  if(ki>=0)imlec=[r1+ki,k[ki].imlec];else if(r.imlec&&r.imlec!=='bas')imlec=[r1+k.indexOf(r.imlec),r.imlec.l.length];else imlec=r1>0?[r1-1,yS[r1-1].length]:[0,0];
  return {s:yS,d:yD,imlec,vurgu:this.aralik(r1,k.length),isaret:r.isaret};},
 // Tek yazma kapısı: değişen aralık execCommand('insertText') ile yazılır (Ctrl+Z çalışır). Bantlar önce yazılır; yazım
 // sürerken input olayları susar (çok satırda birden çok olay), sonda tek çizim. / one write gate, one redraw at the end
 uygula(yS,yD,imlec,vurgu,duyuru){const ta=$('okuma_metni'),eski=ta.value,yeni=yS.join('\n'),m=Math.min(eski.length,yeni.length);
  Durak.anlik();let a=0,b=0;while(a<m&&eski[a]===yeni[a])a++;while(b<m-a&&eski[eski.length-1-b]===yeni[yeni.length-1-b])b++;
  if(a&&/[\uD800-\uDBFF]/.test(eski[a-1]))a--;if(b&&/[\uDC00-\uDFFF]/.test(eski[eski.length-b]))b--;
  Durak.dur=yD.slice();Durak.eski=yS.slice();let yazildi=eski===yeni;
  if(!yazildi){this.yaziyor=true;try{ta.focus({preventScroll:true});if(document.activeElement===ta){ta.setSelectionRange(a,eski.length-b);const ek=yeni.slice(a,yeni.length-b);
   yazildi=ek?document.execCommand('insertText',false,ek):document.execCommand('delete');}}catch(e){yazildi=false;}finally{this.yaziyor=false;}}
  if(!yazildi||ta.value!==yeni)ta.value=yeni;  // yedek yol: geri alma bu tarayıcıda kaybolur, işlev bozulmaz / fallback
  Durak.anlik();const o=Array.isArray(imlec)?[imlec,imlec]:[imlec.bas,imlec.son];ta.focus({preventScroll:true});ta.setSelectionRange(this.ofs(yS,...o[0]),this.ofs(yS,...o[1]));
  if(eski===yeni)defterNo();else{this.vurgu(vurgu);if(duyuru)this.duyur(duyuru);}this.goster(o[0][0]);},
 // Satırı görünür alana getirir; bu kaydırma açık menüyü kapatmaz / brings the line into view without closing the menu
 goster(r){const ta=$('okuma_metni'),u=this.ust[r],h=this.boy[r]||satirBoyu();if(u==null)return;
  if(u-6<ta.scrollTop||u+h>ta.scrollTop+ta.clientHeight){const o=ta.scrollTop;ta.scrollTop=Math.max(0,u-(ta.clientHeight-h)/2);if(ta.scrollTop!==o){Acilir.sessiz=true;bantKaydir();}}},
 // Görsel farkındalık: etkilenen satır, numarası ve bandı 900 ms parlar (yeniden çizim vurguyu kesmez).
 vurgu(l){this.parla={k:new Set(l),son:performance.now()};defterNo();clearTimeout(this.zaman);
  this.zaman=setTimeout(()=>{this.parla.k=new Set();defterNo();},950);},
 isik(){const g=performance.now()-this.parla.son;return g<900&&this.parla.k.size?{k:this.parla.k,gecikme:`;animation-delay:-${Math.round(g)}ms`}:{k:new Set(),gecikme:''};},
 duyur(m){$('satir_duyuru').textContent=m;},
 yap(op,etiket,sec){const r=this.hesapla(this.satirlar(),Durak.dur,op);if(!r)return;
  this.uygula(r.s,r.d,sec&&r.kay?this.secimKaydir(sec,op.a,op.b??op.a,r.kay):r.imlec,r.vurgu,t('satir_oldu',{islem:etiket,n:r.vurgu[0]+1}));},
 ekle(i,yon){this.yap({tur:'ekle',a:i,yon},t(yon==='ust'?'satir_ust':'satir_alt'));},
 tasi(a,b,h,sec,etiket){const N=this.satirlar().length;if(h===a||h<0||h+b-a>=N)return;this.yap({tur:'tasi',a,b,hedef:h},etiket||t('satir_sira'),sec);},
 cogalt(a,b,sec){this.yap({tur:'cogalt',a,b},t('satir_cogalt'),sec);},
 sil(a,b){this.yap({tur:'sil',a,b},t('satir_sil'));},
 // Satır menüsü (numaraya tıkla ya da Alt+Enter). Pasif öğe aria-disabled + nedeni title'da (fare üstünde görünür).
 menu(i,x,b){const s=this.satirlar(),N=s.length,bos=N===1&&!s[0].trim(),B=t('satir_pasif_bos');this.acik=i;
  const oge=(is,ad,ipucu,neden,sinif)=>`<button type="button" role="menuitem" data-is="${is}"${sinif?` class="${sinif}"`:''}${neden?` aria-disabled="true" title="${esc(neden)}"`:''}>${esc(ad)}${ipucu?`<span dir="ltr">${ipucu}</span>`:''}</button>`;
  Acilir.ac(b,x,Acilir.baslik(i+1,s[i])+oge('ust',t('satir_ust'))+oge('alt',t('satir_alt'))
   +oge('yukari',t('satir_yukari'),'Alt+↑',i===0&&(bos?B:t('satir_pasif_ilk')))+oge('asagi',t('satir_asagi'),'Alt+↓',i===N-1&&(bos?B:t('satir_pasif_son')))
   +Acilir.sayiKutusu(1,N,1,i+1,'',t('satir_sira'),N<2&&(bos?B:t('satir_pasif_tek')))+'<small class="sira_not" role="alert" hidden></small>'
   +oge('cogalt',t('satir_cogalt'),'Alt+Shift+↓',bos&&B)+'<hr>'+oge('sil',t('satir_sil'),'',bos&&B,'tehlike'),this,t('satir_no',{n:i+1}));},
 yenile(){const b=document.querySelector(`#satirno .no[data-i="${this.acik}"]`);if(b)this.menu(this.acik,Acilir.x,b);else Acilir.kapat();},
 kapandi(){this.acik=null;},
 tikla(e,b){const i=this.acik,d=b.dataset;if(i==null)return;
  if(b.classList.contains('hayir'))return this.yenile();
  if(d.evet!==undefined){const [tur,m]=d.evet.split(':');Acilir.kapat(true);return tur==='sil'?this.sil(i,i):this.tasi(i,i,+m,null,t('satir_sira'));}
  if(d.is==='sil')return this.silSor(b,i);
  Acilir.kapat(true);
  if(d.is==='ust'||d.is==='alt')this.ekle(i,d.is);
  else if(d.is==='yukari')this.tasi(i,i,i-1,null,t('satir_yukari'));
  else if(d.is==='asagi')this.tasi(i,i,i+1,null,t('satir_asagi'));
  else if(d.is==='cogalt')this.cogalt(i,i);},
 // Boş satır sorulmadan silinir (kaybolan bir şey yok); dolu satırda metnin başı ve bandı söylenir.
 silSor(b,i){const s=this.satirlar(),d=Durak.dur[i];if(!s[i].trim()){Acilir.kapat(true);return this.sil(i,i);}
  const bas=s[i].length>48?s[i].slice(0,47)+'…':s[i];
  Acilir.onayAc(b,Acilir.onay(t('satir_sil_soru',{n:i+1}),bas+(d!=null?' · '+t('satir_sil_bant',{sure:snb(d)}):''),'sil'));},
 // Sıraya taşı: sayı yazılır; aynı sıra işlem yapmaz, aralık dışı söylenir, farklı sıra her zaman onaylanır.
 gir(){const i=this.acik,N=this.satirlar().length,a=$('acilir'),o=a.querySelector('.ozel'),g=o&&o.querySelector('input'),not=a.querySelector('.sira_not');if(!g)return;
  const v=g.value.trim(),m=+v;if(!/^\d+$/.test(v)){g.classList.add('yanlis');setTimeout(()=>g.classList.remove('yanlis'),1000);return;}
  if(m<1||m>N){not.textContent=t('satir_sira_disi',{n:N});not.hidden=false;return;}
  if(m===i+1)return Acilir.kapat(true);
  not.hidden=true;Acilir.onayAc(o,Acilir.onay(t('satir_tasi_soru',{n:i+1,m}),t('satir_tasi_ayrinti'),'sira:'+(m-1),true));},
 // Klavye: Alt+↑/↓ taşı, Alt+Shift+↓ çoğalt, Alt+Enter menü; boş satırda Enter yeni boş satır açmaz, paragraf bandı yapar.
 tus(e){if(e.isComposing||e.keyCode===229)return;const ta=$('okuma_metni');
  if(e.altKey&&!e.ctrlKey&&!e.metaKey){
   if(e.key==='ArrowUp'||e.key==='ArrowDown'){e.preventDefault();const c=this.secim(),asagi=e.key==='ArrowDown';
    if(e.shiftKey){if(asagi)this.cogalt(c.a,c.b,c);return;}
    const h=asagi?c.a+1:c.a-1;if(h<0||(asagi&&c.b+1>=c.s.length))return;this.tasi(c.a,c.b,h,c,t(asagi?'satir_asagi':'satir_yukari'));return;}
   if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();const r=this.secim().bas[0];this.goster(r);const b=document.querySelector(`#satirno .no[data-i="${r}"]`);
    if(b){const q=b.getBoundingClientRect();this.menu(r,rtl()?q.right:q.left,b);}}
   return;}
  if(e.key!=='Enter'||e.shiftKey||e.ctrlKey||e.metaKey||ta.selectionStart!==ta.selectionEnd)return;
  const s=this.satirlar(),[r]=this.konum(s,ta.selectionStart);if(!r||s[r].trim()||!s[r-1].trim())return;
  e.preventDefault();if(Durak.dur[r-1]==null){Durak.dur[r-1]=Durak.HAZIR.paragraf;Durak.anlik();}
  this.vurgu([r-1]);this.duyur(t('durak_eklendi',{n:r,sure:snb(Durak.sure(r-1))}));},
 yapistirOlay(e){const m=e.clipboardData&&e.clipboardData.getData('text/plain');if(!m||!/[\r\n]|\|\|/.test(m))return;e.preventDefault();
  const ta=$('okuma_metni'),r=this.yapistir(this.satirlar(),Durak.dur,ta.selectionStart,ta.selectionEnd,m);this.uygula(r.s,r.d,r.imlec,r.vurgu,'');},
 // Sürükle-bırak (pointer olayları): numaraya basılı tut, 4 px kaydır; bırakılan aralığa yerleşir. Esc iptal.
 // Bırakmanın ürettiği tek click yutulur (bayrak bir sonraki basışta da sıfırlanır).
 basla(e){const b=e.target.closest('.no');this.suruklendi=false;if(!b||e.button!==0)return;this.bas={i:+b.dataset.i,y0:e.clientY,y:e.clientY,id:e.pointerId,g:+b.dataset.i};},
 surukle(e){const p=this.bas;if(!p||e.pointerId!==p.id)return;if(!(e.buttons&1))return this.iptal();p.y=e.clientY;
  if(!this.suruk){if(Math.abs(p.y-p.y0)<4)return;this.suruk=true;Acilir.kapat();try{$('satirno').setPointerCapture(e.pointerId);}catch(x){}
   $('defterkap').classList.add('suruk');requestAnimationFrame(()=>this.kaydir());}
  this.isaretle();},
 hedefBul(y){const ta=$('okuma_metni'),i=y-ta.getBoundingClientRect().top+ta.scrollTop;let g=0;while(g<this.ust.length&&this.ust[g]+this.boy[g]/2<i)g++;return g;},
 izSil(){document.querySelectorAll('#defterkap .hedef,#defterkap .kaynak').forEach(e=>e.remove());},
 isaretle(){const p=this.bas,N=this.ust.length;if(!p||!N)return;const g=p.g=this.hedefBul(p.y),y=g<N?this.ust[g]:this.ust[N-1]+this.boy[N-1];this.izSil();
  const k=document.createElement('div');k.className='kaynak';k.style.cssText=`top:${this.ust[p.i]}px;height:${this.boy[p.i]}px`;
  const h=document.createElement('div');h.className='hedef';h.style.top=(y-1)+'px';$('bantlar').firstElementChild.append(k,h);$('satirno').append(h.cloneNode());},
 kaydir(){if(!this.suruk)return;const ta=$('okuma_metni'),r=ta.getBoundingClientRect(),y=this.bas.y,v=y<r.top+24?-8:y>r.bottom-24?8:0;
  if(v){const o=ta.scrollTop;ta.scrollTop+=v;if(ta.scrollTop!==o)this.isaretle();}requestAnimationFrame(()=>this.kaydir());},
 birak(e){const p=this.bas;if(!p||e.pointerId!==p.id)return;const s=this.suruk;this.iptal();if(!s)return;
  const to=p.g>p.i?p.g-1:p.g;if(to!==p.i)this.tasi(p.i,p.i,to,null,t('satir_sira'));},
 iptal(){if(this.suruk)this.suruklendi=true;this.bas=null;this.suruk=false;$('defterkap').classList.remove('suruk');this.izSil();},
 kur(){const no=$('satirno'),ta=$('okuma_metni');
  no.addEventListener('pointerdown',e=>this.basla(e));no.addEventListener('pointermove',e=>this.surukle(e));no.addEventListener('pointerup',e=>this.birak(e));
  no.addEventListener('pointercancel',()=>this.iptal());no.addEventListener('lostpointercapture',()=>{if(this.suruk)this.iptal();});
  no.addEventListener('click',e=>{if(this.suruklendi){this.suruklendi=false;return;}const b=e.target.closest('.no');if(!b)return;e.stopPropagation();
   const i=+b.dataset.i;if(Acilir.sahip===this&&this.acik===i)return Acilir.kapat(true);this.menu(i,e.clientX,b);});
  // Numara sütununda tekerlek metni kaydırır (sütun kendi kaymaz) / the wheel over numbers scrolls the text
  no.addEventListener('wheel',e=>{ta.scrollTop+=e.deltaMode===1?e.deltaY*satirBoyu():e.deltaY;e.preventDefault();},{passive:false});
  ta.addEventListener('keydown',e=>this.tus(e));ta.addEventListener('paste',e=>this.yapistirOlay(e));}};
Acilir.kur();Durak.kur();Satir.kur();
// Defter: her mantıksal satırın (cümlenin) yüksekliği gizli aynada ölçülür, numara (düğme) o satırın başına yazılır.
const satirBoyu=()=>parseFloat(getComputedStyle($('okuma_metni')).lineHeight)||28;
function bantKaydir(){const ta=$('okuma_metni');$('satirno').scrollTop=ta.scrollTop;$('bantlar').firstElementChild.style.transform=`translateY(${-ta.scrollTop}px)`;}
function defterNo(){const ta=$('okuma_metni'),ay=$('ayna'),no=$('satirno');const s=Durak.hizala(ta);if(!ta.clientWidth)return;
 const R=satirBoyu();ay.style.width=ta.clientWidth+'px';ay.innerHTML=s.map(l=>`<div>${esc(l)||'&#8203;'}</div>`).join('');
 const h=[...ay.children].map(d=>d.getBoundingClientRect().height),p=Satir.isik(),ipucu=esc(t('satir_no_ipucu')),yan=new Map(Durak.hatalar().map(x=>[x.i,esc(sorunMetni(x))]));let y=6,i=h.length,html='',isik='';
 Satir.ust=[];Satir.boy=h;
 h.forEach((x,k)=>{Satir.ust[k]=y;const v=p.k.has(k),a=Satir.acik===k;
  html+=`<button type="button" class="no${s[k].trim()?'':' bos'}${yan.has(k)?' yanlis':''}${a?' secik':''}${v?' parla':''}" data-i="${k}" tabindex="-1" aria-haspopup="menu" aria-expanded="${a}" style="height:${x}px${v?p.gecikme:''}" aria-label="${esc(t('satir_no',{n:k+1}))}"${yan.has(k)?' aria-invalid="true"':''} title="${yan.get(k)||ipucu}">${k+1}</button>`;
  if(v)isik+=`<div class="isik parla" style="top:${y}px;height:${x}px${p.gecikme}"></div>`;y+=x;});
 for(;y<Math.max(ta.scrollHeight,ta.clientHeight)+R;y+=R)html+=`<div class="sb" style="height:${R}px">${++i}</div>`;
 const d=Durak.ciz(s,h,R/3);no.innerHTML=html+d.oluk;$('bantlar').firstElementChild.innerHTML=isik+d.bant;bantKaydir();}
// Kutu boyu tam satır sayısına oturur: üstte ve altta aynı küçük boşluk (6 px) kalır.
function defterBoy(){const kap=$('defterkap'),d=kap.firstElementChild;
 if(getComputedStyle(kap).flexGrow!=='0')d.style.height=(Math.max(4,Math.floor((kap.clientHeight-14)/satirBoyu()))*satirBoyu()+12)+'px';else d.style.height='';defterNo();}
new ResizeObserver(defterBoy).observe($('defterkap'));
// Yazım: kapı yazarken olaylar susar; geri al/yinele işaret çevirmez; elle yazılan '||' kapıdan banda taşınır.
$('okuma_metni').addEventListener('input',e=>{if(Satir.yaziyor)return;const ta=$('okuma_metni');Durak.tur=e.inputType;
 if(/^history/.test(e.inputType||'')||e.isComposing||!Durak.isaretTasi(ta))defterNo();Durak.tur=null;});
$('okuma_metni').addEventListener('scroll',bantKaydir);
$('btn_oku').onclick=async()=>{const b=$('btn_oku');b.disabled=true;sonOkuma=null;$('sonuc').innerHTML='';
 const hd=Durak.hatalar();if(hd.length){durumYaz($('d_oku'),{hata:hd.map(h=>h.metin).join('\n'),sorunlar:hd});Satir.goster(hd[0].i);b.disabled=false;return;}
 const j=await api('/api/oku',{ses:$('ses').value,metin:Durak.metin()});
 if(j.hata){durumYaz($('d_oku'),j);b.disabled=false;return;}
 const s=await bekle(j.is,$('d_oku'));b.disabled=false;if(s.durum!=='bitti')return;sonOkuma=s.sonuc;okumaCiz();};

function dosyaAdi(){const f=$('klon_dosya').files[0];$('dosya_ad').textContent=f?f.name:t('dosya_yok');}
$('dosya_btn').onclick=()=>$('klon_dosya').click();
const klonHazir=()=>{$('btn_klon').disabled=!($('klon_onay').checked&&$('klon_dosya').files.length&&$('klon_kayit_metni').value.trim()&&$('klon_metin').value.trim());};
['klon_onay','klon_dosya','klon_kayit_metni','klon_metin'].forEach(id=>{$(id).addEventListener('input',klonHazir);$(id).addEventListener('change',klonHazir);});
let kayitSn=null;
function klonBilgi(){const d=kayitSn;if(d===null){$('klon_bilgi').textContent='';return;}
 const not=d>36?t('kirp'):d<3?t('cok_kisa'):d<5||d>30?t('oneri'):'';$('klon_bilgi').textContent=t('sn',{n:d.toFixed(1)})+(not?' · '+not:'');}
$('klon_dosya').addEventListener('change',()=>{dosyaAdi();kayitSn=null;klonBilgi();const f=$('klon_dosya').files[0];if(!f)return;const u=URL.createObjectURL(f);const a=new Audio();
 a.onloadedmetadata=()=>{kayitSn=a.duration;klonBilgi();URL.revokeObjectURL(u);};a.src=u;});
function b64(buf){const u=new Uint8Array(buf);let s='';for(let i=0;i<u.length;i+=32768)s+=String.fromCharCode.apply(null,u.subarray(i,i+32768));return btoa(s);}
function klonCiz(){const r=sonKlon;if(!r)return;
 $('klon_sonuc').innerHTML=`<audio controls src="/okuma/${r.is}/${r.dosya}"></audio> ${indir('/okuma/'+r.is+'/'+r.dosya,r.dosya)}
  <div class="uyari"><b>${esc(t('yapay'))}</b></div>
  <div><small>${esc(ozet(r))}, ${esc(t('referans',{n:r.referans_sn}))}</small>${(r.not_kodlari||[]).map(n=>'<br><small>'+esc(sorunMetni(n))+'</small>').join('')}</div>`;}
$('btn_klon').onclick=async()=>{if(!$('klon_onay').checked)return;const b=$('btn_klon');b.disabled=true;sonKlon=null;$('klon_sonuc').innerHTML='';
 const f=$('klon_dosya').files[0];const j=await api('/api/klon',{onay:true,kayit:b64(await f.arrayBuffer()),kayit_metni:$('klon_kayit_metni').value,metin:$('klon_metin').value,tohum:+$('klon_tohum').value});
 if(j.hata){durumYaz($('d_klon'),j);klonHazir();return;}
 const s=await bekle(j.is,$('d_klon'));klonHazir();if(s.durum!=='bitti')return;sonKlon=s.sonuc;klonCiz();};

(async()=>{await Promise.all([api('/api/ornekler').then(o=>ornekler=o),api('/api/sesler').then(s=>sesler=s)]);await dilYukle(ilkDil());Durak.acilis();sureGuncelle();})();
</script></body></html>
"""


def _dil_ipucu(payload: dict):
    """Kararsız metin için seçilen örnek tarifin dili (yoksa None); payload["dil"] yok sayılır.
    Language of the chosen example prompt for ambiguous text (else None); payload["dil"] is ignored."""
    try:
        return ornekler.bul(str(payload.get("ornek") or ""))["dil"] if payload.get("ornek") else None
    except (KeyError, ValueError):
        return None


def _sorun(item) -> dict:
    """Sorun ise kod + değerler, düz metinse yalnız metin (arayüz çeviremezse metni gösterir).
    Code + values for a Sorun, plain text otherwise (the UI falls back to the text)."""
    return item.sozluk() if isinstance(item, okunus.Sorun) else {"kod": None, "veri": {}, "metin": str(item)}


def _hata(found: list) -> dict:
    return {"hata": "\n".join(found), "sorunlar": [_sorun(item) for item in found]}


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
            self.jobs[job_id] = {"durum": "sirada", "mesaj": "sırada bekliyor (queued)", "kod": "sirada", "veri": {},
                                 "tur": kind}
        self.queue.put((job_id, kind, payload))
        return job_id

    def status(self, job_id: str) -> dict:
        with self.lock:
            return dict(self.jobs.get(job_id) or {"durum": "hata", "mesaj": "iş bulunamadı", "kod": "is_yok", "veri": {}})

    def _set(self, job_id, **fields):
        with self.lock:
            self.jobs[job_id].update(fields)

    def _run(self):
        while True:
            job_id, kind, payload = self.queue.get()
            self._set(job_id, durum="calisiyor", mesaj="motor başlatılıyor, model yükleniyor (~10-20 sn)",
                      kod="yukleniyor", veri={})

            def progress(done, total, elapsed, job_id=job_id):
                self._set(job_id, mesaj=f"{done}/{total} hazır, {elapsed:.0f} sn", kod="ilerleme",
                          veri={"done": done, "total": total, "sn": round(elapsed)})
            try:
                if kind == "tasarla":
                    result = tasarla.tasarla(self.settings, payload["ad"], payload["tarif"], payload["metin"],
                                             max(1, min(50, int(payload.get("cesit") or 3))), None, progress,
                                             okunus.detect(payload["metin"], _dil_ipucu(payload)))
                    self._set(job_id, durum="bitti", sonuc=result, kod="bitti_tasarla",
                              veri={"n": len(result["cesitler"]), "sn": result["sure_sn"], "vram": result["vram_tepe_mb"]},
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
                    result["not_kodlari"] = [_sorun(note) for note in result.get("notlar", [])]
                    self._set(job_id, durum="bitti", sonuc=result, mesaj="bitti: yapay ses hazır (synthetic)",
                              kod="bitti_klon", veri={})
                else:
                    voice_dir = oku.find_voice(self.settings, payload["ses"])
                    out_dir = self.settings["sesler"] / "_okumalar" / job_id
                    result = oku.oku(self.settings, voice_dir, payload["metin"], out_dir, progress)  # "dil" gelirse yok sayılır (eski istemci) / a "dil" field is ignored (old clients)
                    result["is"] = job_id
                    self._set(job_id, durum="bitti", sonuc=result, mesaj="bitti", kod="bitti", veri={})
            except Exception as error:  # kullanıcıya düz metin hata, ayrıntı için iz / plain-text error + traceback
                found = [arg for arg in error.args if isinstance(arg, okunus.Sorun)] or [str(error)]
                self._set(job_id, durum="hata", mesaj=str(error), kod="hata", veri={},
                          sorunlar=[_sorun(item) for item in found], iz=traceback.format_exc()[-1200:])


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
            if not path.is_file() or path.suffix.lower() not in (".wav", ".flac", ".mp3", ".txt", ".json", ".svg"):
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
            elif path == "/api/ornekler":
                self._json(ornekler.listele())
            elif path == "/api/sesler":
                self._json(oku.list_voices(settings))
            elif path.startswith("/api/is/"):
                self._json(jobs.status(path[8:]))
            elif path.startswith("/bayrak/"):
                self._file(BAYRAK_KOKU / path[8:], BAYRAK_KOKU)
            elif path.startswith("/arayuz_dili/"):
                self._file(DIL_KOKU / path[13:], DIL_KOKU)
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
            if self.path == "/api/sure":
                # Tasarım metninin canlı süre göstergesi; hesap ve sınır tek yerde (tasarla.py), arayüz kopyalamaz.
                # Live length meter for the design text; the estimate and limits live only in tasarla.py.
                text = str(payload.get("metin") or "")
                dil = okunus.detect(text, _dil_ipucu(payload))
                return self._json({"sn": tasarla.estimate_seconds(text, dil), "dil": dil,
                                   "sinir": tasarla.DESIGN_LIMIT_SECONDS,
                                   "sert": round(tasarla.DESIGN_HARD_LIMIT_SECONDS, 1)})
            if self.path == "/api/tasarla":
                try:
                    found = tasarla.check(payload.get("tarif", ""), payload.get("metin", ""),
                                          okunus.detect(payload.get("metin", ""), _dil_ipucu(payload)))
                except ValueError as error:  # ör. bilinmeyen durak / e.g. unknown pause marker
                    found = [error.args[0] if error.args and isinstance(error.args[0], okunus.Sorun) else str(error)]
                if not str(payload.get("ad", "")).strip():
                    found.append(okunus.Sorun("sesin adı boş", "ad_bos"))
                if found:
                    return self._json(_hata(found), 400)
                return self._json({"is": jobs.submit("tasarla", payload)})
            if self.path == "/api/oku":
                found = []
                try:
                    voice_dir = oku.find_voice(settings, str(payload.get("ses", "")))
                    found = okunus.problems(payload.get("metin", ""), dil=oku.voice_language(voice_dir, None, payload.get("metin", "")))
                except (FileNotFoundError, ValueError) as error:
                    found.append(error.args[0] if error.args and isinstance(error.args[0], okunus.Sorun) else str(error))
                if found:
                    return self._json(_hata(found), 400)
                return self._json({"is": jobs.submit("oku", payload)})
            if self.path == "/api/klon":
                from . import klonla
                found = klonla.check(payload.get("kayit_metni", ""), payload.get("metin", ""), payload.get("onay"))
                try:
                    data = base64.b64decode(str(payload.get("kayit") or ""), validate=True)
                except (binascii.Error, ValueError):
                    data = b""
                if not data:
                    found.append(okunus.Sorun("ses kaydı yok ya da okunamadı (recording missing)", "kayit_yok"))
                elif len(data) > klonla.MAX_UPLOAD_BYTES:
                    found.append(okunus.Sorun("ses dosyası 25 MB'tan büyük", "kayit_buyuk",
                                              mb=klonla.MAX_UPLOAD_BYTES // 1_000_000))
                if found:
                    return self._json(_hata(found), 400)
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

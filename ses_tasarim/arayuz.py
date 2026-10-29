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
<title>VoxCPM2 Türkçe Ses Tasarımı</title>
<style>
:root{--bg:#111;--panel:#1c1c1c;--fg:#eee;--muted:#9a9a9a;--soluk:#777;--alan:#0d0d0d;--cizgi:#333;--cizgi2:#2a2a2a;--acc:#ebbe6e;--baslik:#ebbe6e;--ok:#5fb36a;--err:#e06c6c;color-scheme:dark}
:root[data-tema=acik]{--bg:#f5f5f3;--panel:#fff;--fg:#1d1d1f;--muted:#5f6368;--soluk:#80868b;--alan:#fff;--cizgi:#d4d4d4;--cizgi2:#e8e8e8;--acc:#e3a93f;--baslik:#9a6a10;--ok:#2e7d32;--err:#c62828;color-scheme:light}
body{font-family:Segoe UI,system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:980px;margin:auto;padding:16px}
section{background:var(--panel);border-radius:10px;padding:14px 18px;margin:12px 0}
h1{font-size:1.4rem;margin:0}h2{font-size:1.1rem;color:var(--baslik);margin:4px 0 10px}
.bas{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:8px 0 10px}
button.tema{background:transparent;color:var(--fg);border:1px solid var(--cizgi);border-radius:50%;width:38px;height:38px;padding:0;margin:0;display:grid;place-items:center;flex:none}
button.tema:hover{border-color:var(--acc)}
.diller{display:flex;align-items:center;gap:14px;flex-wrap:wrap;color:var(--muted);font-size:.85rem}
.bayraklar{display:flex;flex-wrap:wrap;gap:4px}
.bayraklar button{background:none;border:0;padding:2px;margin:0;border-radius:4px;line-height:0;cursor:pointer;opacity:.75}
.bayraklar button:hover,.bayraklar button[aria-pressed=true]{opacity:1}.bayraklar button[aria-pressed=true]{box-shadow:0 0 0 2px var(--acc)}
.bayraklar img{width:22px;height:16.5px;border-radius:2px;box-shadow:0 0 0 1px var(--cizgi2)}
.dosya{display:flex;align-items:center;gap:10px}.dosya span{color:var(--muted);font-size:.9rem}
button.ikincil{background:transparent;color:var(--fg);border:1px solid var(--cizgi);margin:0}button.ikincil:hover{border-color:var(--acc)}
label.onay{color:var(--fg);display:flex;gap:8px;align-items:flex-start}label.onay input{width:auto;margin-top:3px}
footer.uyari{margin:16px 0 4px;font-size:.8rem}
label{display:block;margin:10px 0 4px;color:var(--muted);font-size:.9rem}
textarea,input,select{width:100%;box-sizing:border-box;background:var(--alan);color:var(--fg);border:1px solid var(--cizgi);border-radius:6px;padding:8px;font:inherit}
textarea{min-height:90px}
#ad{max-width:320px}#cesit{max-width:90px}
.ust{display:flex;gap:24px;flex-wrap:wrap}.ust>.sol{flex:0 0 320px}.ust>.sag{flex:1;min-width:260px}
#ornek{font-size:.9rem}.ipucu{display:block;font-size:.8rem;color:var(--soluk);margin-top:2px}
button{background:var(--acc);color:#111;border:0;border-radius:6px;padding:9px 16px;font-weight:600;cursor:pointer;margin-top:10px}
button:disabled{opacity:.5;cursor:default}
.row{display:flex;gap:12px;flex-wrap:wrap}.row>*{flex:1;min-width:200px}
.durum{margin-top:8px;color:var(--muted);white-space:pre-wrap}.hata{color:var(--err)}.ok{color:var(--ok)}
.cesit{display:flex;align-items:center;gap:10px;padding:6px 0;border-bottom:1px solid var(--cizgi2)}
.cesit audio{flex:1;height:32px}small{color:var(--muted)}
.uyari{border-left:3px solid var(--acc);padding:6px 10px;color:var(--muted);font-size:.9rem}
</style>
<script>try{document.documentElement.dataset.tema=localStorage.getItem('tema')||(matchMedia('(prefers-color-scheme: light)').matches?'acik':'koyu');}catch(e){}</script>
</head><body>
<header class="bas"><h1><span data-t="baslik">VoxCPM2 Türkçe Ses Tasarımı</span> <small>· 4 GB GPU</small></h1>
<button id="tema" class="tema" data-t-title="tema" title="Gece / gündüz" aria-label="Gece / gündüz"></button></header>
<div class="diller"><span data-t="diller">30 dil · açık kaynak, ücretsiz, yerel</span><div class="bayraklar" id="bayraklar" role="group"></div></div>

<section><h2 data-t="s1">1. Ses tasarla</h2>
<div class="ust"><div class="sol">
<label for="ad" data-t="ad">Sesin adı</label><input id="ad" data-t-ph="ad_ph">
<label for="cesit" data-t="cesit">Çeşit sayısı (her biri ayrı tohum)</label><input id="cesit" type="number" value="3" min="1" max="10">
</div><div class="sag">
<label for="ornek"><span data-t="ornek">Örnek tarif</span><span class="ipucu" data-t="ornek_ipucu1">Seçince tarif, metin ve ad dolar; istediğin gibi değiştir.</span><span class="ipucu" data-t="ornek_ipucu2">Dil metinden otomatik tanınır.</span></label>
<select id="ornek"></select>
</div></div>
<label for="tarif" data-t="tarif">Ses tarifi: İngilizce, parantezsiz</label>
<textarea id="tarif" placeholder="A calm woman in her forties with a warm, low voice, speaking slowly and clearly. Clean studio recording, no background noise."></textarea>
<label for="tasarim_metni" data-t="tmetin">Ses yaratılırken okutulan metin: sesin dilinde, rakamsız, tırnaksız</label>
<textarea id="tasarim_metni" data-t-ph="tmetin_ph"></textarea>
<button id="btn_tasarla" data-t="tasarla">Tasarla</button><div id="d_tasarla" class="durum" aria-live="polite"></div>
<div id="cesitler"></div></section>

<section><h2 data-t="s2">2. Bu sesle oku</h2>
<label for="ses" data-t="ses">Ses</label><select id="ses"></select>
<label for="okuma_metni" data-t="ometin">Okunacak metin: her satır bir cümle</label>
<textarea id="okuma_metni" data-t-ph="ometin_ph"></textarea>
<button id="btn_oku" data-t="oku">Bu sesle oku</button><div id="d_oku" class="durum" aria-live="polite"></div>
<div id="sonuc"></div></section>

<section><h2 data-t="s3">3. Ses klonlama: kendi sesin ya da izinli ses</h2>
<div class="uyari" data-t="klon_uyari"></div>
<label for="klon_dosya" data-t="kayit">Ses kaydı</label>
<div class="dosya"><input id="klon_dosya" type="file" accept=".wav,.mp3,.flac,.ogg,audio/*" hidden>
<button type="button" class="ikincil" id="dosya_btn" data-t="dosya_sec">Dosya seç</button><span id="dosya_ad" data-t="dosya_yok">Dosya seçilmedi</span></div>
<div id="klon_bilgi" class="durum"></div>
<label for="klon_kayit_metni" data-t="kayit_metni">Kaydın birebir metni (zorunlu)</label>
<textarea id="klon_kayit_metni" data-t-ph="kayit_metni_ph"></textarea>
<label for="klon_metin" data-t="klon_metin">Okunacak metin: her satır bir cümle</label>
<textarea id="klon_metin" data-t-ph="klon_metin_ph"></textarea>
<div class="row"><div><label for="klon_tohum" data-t="tohum">Tohum (aynı tohum = aynı sonuç)</label><input id="klon_tohum" type="number" value="42" min="0"></div>
<div><label data-t="kalite">Kalite (sabit)</label><input data-t-val="kalite_deger" value="16 adım, cfg 2.0" disabled></div></div>
<label class="onay"><input id="klon_onay" type="checkbox"> <span data-t="onay"></span></label>
<button id="btn_klon" data-t="klonla" disabled>Klonla ve oku</button><div id="d_klon" class="durum" aria-live="polite"></div>
<div id="klon_sonuc"></div></section>

<section><h2 data-t="hazir">Hazır sesler</h2><div id="hazir"></div></section>
<footer class="uyari" data-t="alt"></footer>
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
 document.querySelectorAll('[data-t-title]').forEach(e=>{e.title=t(e.dataset.tTitle);e.setAttribute('aria-label',e.title);});
 document.querySelectorAll('#bayraklar button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.dil===k));
 dosyaAdi();ornekDoldur();sesListesi();cesitCiz();okumaCiz();klonCiz();klonBilgi();
 for(const id of ['d_tasarla','d_oku','d_klon'])durumYaz($(id),$(id)._son);}
$('bayraklar').innerHTML=DILLER.map(([k,b,a])=>`<button type="button" data-dil="${k}" title="${a}" aria-label="${a}" aria-pressed="false"><img src="/bayrak/${b}.svg" alt=""></button>`).join('');
$('bayraklar').onclick=e=>{const b=e.target.closest('button[data-dil]');if(b&&b.dataset.dil!==dil)dilYukle(b.dataset.dil);};

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
 const gruplar={};for(const o of ornekler){let g=gruplar[o.dil];if(!g){g=gruplar[o.dil]=document.createElement('optgroup');g.label=DIL_ADI(o.dil);s.appendChild(g);}
  const e=document.createElement('option');e.value=o.id;e.textContent=dil==='tr'?o.ad_tr:o.ad_en;g.appendChild(e);}
 s.value=secili;}
$('ornek').addEventListener('change',()=>{const o=ornekler.find(o=>o.id===$('ornek').value);if(!o)return;
 $('tarif').value=o.tarif;$('tasarim_metni').value=o.metin;if(!$('ad').value.trim()||ornekler.some(x=>x.id===$('ad').value))$('ad').value=o.id;});

let sesler={hazir:[],tasarlanan:[]};
const tanitim=k=>dil==='tr'?k.tanitim_tr:(k.tanitim_en||k.tanitim_tr);
function sesListesi(){const s=$('ses'),secili=s.value;s.innerHTML='';
 for(const k of sesler.tasarlanan){const o=document.createElement('option');o.value=k.kimlik;o.textContent=t('etiket',{ad:t('tasarlanan'),deger:k.kimlik+' · '+t('tohum_n',{n:k.okuma_tohumu})});s.appendChild(o);}
 for(const k of sesler.hazir){const o=document.createElement('option');o.value=k.kimlik;o.textContent=t('etiket',{ad:t('hazir_ses'),deger:k.gorunen_ad+' · '+(tanitim(k)||'').slice(0,60)});s.appendChild(o);}
 if(secili)s.value=secili;
 $('hazir').innerHTML=sesler.hazir.map(k=>`<div class="cesit"><div style="flex:1"><b>${esc(k.gorunen_ad)}</b> <small>${esc(t('tohum_n',{n:k.okuma_tohumu}))}</small><br><small>${esc(tanitim(k))}</small></div>`+
  `<audio controls preload="none" src="/dosya/${esc(k.kimlik)}/${esc(k.ornek_okuma||k.referans)}"></audio></div>`).join('');}
async function yenile(secili){sesler=await api('/api/sesler');sesListesi();if(secili)$('ses').value=secili;}
async function bekle(is,el){for(;;){const j=await api('/api/is/'+is);durumYaz(el,j);
 if(j.durum==='bitti'||j.durum==='hata')return j;await new Promise(r=>setTimeout(r,2000));}}

let sonCesit=null,sonOkuma=null,sonKlon=null;
function cesitCiz(){const s=sonCesit;if(!s)return;const secili=(document.querySelector('input[name=sec]:checked')||{}).value;
 $('cesitler').innerHTML=s.cesitler.map(c=>c.hata?`<div class="cesit hata">${esc(t('tohum_n',{n:c.tohum}))}: ${esc(c.hata)}</div>`:
  `<div class="cesit"><label style="margin:0"><input type="radio" name="sec" value="${esc(s.ses)}/${c.cesit}"> ${esc(t('cesit_n',{n:c.cesit}))} <small>${esc(t('tohum_n',{n:c.tasarim_tohumu}))}, ${esc(t('sn',{n:c.referans_sn}))}</small></label><audio controls preload="none" src="/dosya/${esc(s.ses)}/${c.cesit}/referans.wav"></audio></div>`).join('');
 document.querySelectorAll('input[name=sec]').forEach(r=>{r.checked=r.value===secili;r.onchange=()=>{$('ses').value=r.value;};});}
$('btn_tasarla').onclick=async()=>{const b=$('btn_tasarla');b.disabled=true;sonCesit=null;$('cesitler').innerHTML='';
 const j=await api('/api/tasarla',{ad:$('ad').value,tarif:$('tarif').value,metin:$('tasarim_metni').value,cesit:+$('cesit').value,ornek:$('ornek').value});
 if(j.hata){durumYaz($('d_tasarla'),j);b.disabled=false;return;}
 const s=await bekle(j.is,$('d_tasarla'));b.disabled=false;if(s.durum!=='bitti')return;
 sonCesit=s.sonuc;cesitCiz();await yenile($('ses').value);const ilk=document.querySelector('input[name=sec]');if(ilk){ilk.checked=true;$('ses').value=ilk.value;}};

const indir=(yol,ad)=>`<a href="${yol}" download="${esc(ad)}"><button>${esc(t('indir'))}</button></a>`;
const ozet=r=>t('okuma_ozet',{ses:r.ses_sn,sure:r.sure_sn,vram:r.vram_tepe_mb,tohum:r.tohum});
function okumaCiz(){const r=sonOkuma;if(!r)return;
 $('sonuc').innerHTML=`<audio controls src="/okuma/${r.is}/okuma.wav"></audio> ${indir('/okuma/'+r.is+'/okuma.wav','okuma.wav')}<div><small>${esc(ozet(r))}</small></div>`;}
$('btn_oku').onclick=async()=>{const b=$('btn_oku');b.disabled=true;sonOkuma=null;$('sonuc').innerHTML='';
 const j=await api('/api/oku',{ses:$('ses').value,metin:$('okuma_metni').value});
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

(async()=>{await Promise.all([api('/api/ornekler').then(o=>ornekler=o),api('/api/sesler').then(s=>sesler=s)]);await dilYukle(ilkDil());})();
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
                                             int(payload.get("cesit") or 3), None, progress,
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

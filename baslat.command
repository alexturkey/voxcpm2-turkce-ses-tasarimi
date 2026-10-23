#!/usr/bin/env bash
# Arayüzü başlatır ve hazır olunca tarayıcıda açar (macOS, Finder'da çift tık). / Starts the web UI and opens the browser (macOS).
# Önce kurulum: bash scripts/kur.sh (README). Kapatmak için bu pencerede Ctrl+C. / Install first; Ctrl+C here to stop.
cd "$(dirname "$0")" || exit 1

if [[ ! -x ".venv/bin/python" ]] || { [[ ! -f "ayarlar.json" ]] && [[ -z "${SES_TASARIM_AYARLAR:-}" ]]; }; then
    echo "Kurulum bulunamadı: .venv ya da ayarlar.json yok."
    echo "Önce kurulumu çalıştırın (README, macOS):  bash scripts/kur.sh"
    echo
    echo "Install not found: .venv or ayarlar.json is missing. Run the installer first: bash scripts/kur.sh"
    read -r -p "Enter ile kapat / press Enter to close "
    exit 1
fi

PORT="$(.venv/bin/python -c "from ses_tasarim import ayarlar as a; import json; print(int(json.loads(a.find_file().read_text(encoding='utf-8')).get('port') or 8765))" 2>/dev/null || echo 8765)"
echo "Arayüz başlıyor, hazır olunca tarayıcı açılacak: http://127.0.0.1:$PORT/"
echo "Starting the web UI; the browser opens when it is ready: http://127.0.0.1:$PORT/"
( for _ in $(seq 90); do
      if nc -z 127.0.0.1 "$PORT" 2>/dev/null; then open "http://127.0.0.1:$PORT/"; break; fi
      sleep 1
  done ) &
.venv/bin/python -m ses_tasarim.arayuz "$@"
echo
echo "Arayüz kapandı. Hata varsa yukarıdaki satırlara bakın. / The UI stopped; check the lines above for errors."
read -r -p "Enter ile kapat / press Enter to close "

@echo off
chcp 65001 >nul
rem Arayüzü başlatır ve hazır olunca tarayıcıda açar. / Starts the web UI and opens it in the browser when ready.
rem Önce kurulum: scripts\kur.ps1 (README). Kapatmak için bu pencerede Ctrl+C. / Install first; Ctrl+C here to stop.
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" goto kurulum_yok
if exist "ayarlar.json" goto ayar_var
if defined SES_TASARIM_AYARLAR goto ayar_var
goto kurulum_yok

:ayar_var
set "PORT=8765"
for /f "usebackq delims=" %%p in (`.venv\Scripts\python.exe -c "from ses_tasarim import ayarlar as a; import json; print(int(json.loads(a.find_file().read_text(encoding='utf-8')).get('port') or 8765))" 2^>nul`) do set "PORT=%%p"

echo Arayüz başlıyor, hazır olunca tarayıcı açılacak: http://127.0.0.1:%PORT%/
echo Starting the web UI; the browser opens when it is ready: http://127.0.0.1:%PORT%/
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "for($i=0;$i -lt 90;$i++){try{(New-Object Net.Sockets.TcpClient('127.0.0.1',%PORT%)).Close();Start-Process 'http://127.0.0.1:%PORT%/';break}catch{Start-Sleep -Seconds 1}}"
".venv\Scripts\python.exe" -m ses_tasarim.arayuz %*
echo.
echo Arayüz kapandı. Hata varsa yukarıdaki satırlara bakın. / The UI stopped; check the lines above for errors.
pause
exit /b 0

:kurulum_yok
echo Kurulum bulunamadı: .venv ya da ayarlar.json yok.
echo Önce kurulumu çalıştırın (README, Hızlı kurulum):
echo   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
echo.
echo Install not found: .venv or ayarlar.json is missing. Run the installer first (README, Quick install).
pause
exit /b 1

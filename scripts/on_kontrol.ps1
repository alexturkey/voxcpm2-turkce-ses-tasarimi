# PR oncesi yerel kontrol / pre-PR local check (kit KL-08). Tek komut, agsiz, GPU yok, hicbir sey yazmaz.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\on_kontrol.ps1          hizli kapilar (saniyeler)
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\on_kontrol.ps1 -Tam     + tum birim testleri (~1 dk)
# Cikis / exit: 0 hepsi gecti, 1 kirmizi, 3 Python bulunamadi, 6 bir kapi calisamadi (denetim.py ile ayni kodlar).
param([switch]$Tam)
$ErrorActionPreference = "Stop"
$kok = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$py = $null
foreach ($aday in @(@("py", "-3"), @("python"), @("python3"))) {
    $cmd = Get-Command $aday[0] -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notmatch "WindowsApps") { $py = $aday; break }   # Microsoft Store takma adi Python degildir
}
if (-not $py) {
    Write-Output "Python 3.10+ bulunamadi / Python 3.10+ not found."
    Write-Output "Kurun / install: winget install Python.Python.3.12 , sonra yeni bir PowerShell acin / then open a new PowerShell."
    Write-Output "SONUC: CALISAMADI on_kontrol (cikis 3): Python yok"
    exit 3
}
$arg = @()
if ($py.Count -gt 1) { $arg += $py[1..($py.Count - 1)] }
$arg += @("-I", "-X", "utf8", (Join-Path $kok "scripts\denetim.py"))
if ($Tam) { $arg += "--tam" } else { $arg += "--hizli" }
Push-Location $kok
try { & $py[0] @arg; $kod = $LASTEXITCODE } finally { Pop-Location }
if ($kod -eq 0) { Write-Output "PR gondermeye hazir / ready to open a PR." }
elseif ($kod -eq 1) { Write-Output "Kirmizi kapilari duzeltin, sonra yeniden calistirin / fix the red gates and run again." }
exit $kod

# Derlenmiş motoru GitHub Release zip'i olarak paketler (yalnız exe + lisans; CUDA DLL'leri ve model ayrı indirilir).
# Packs the built engine as a release zip (exe + license notes only; CUDA DLLs and model are downloaded separately).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\release_zip.ps1 -Exe C:\vox\motor\build\bin\audiocpp_cli.exe -Surum v0.1.0 -Cikti dist
param(
    [Parameter(Mandatory = $true)][string]$Exe,
    [string]$Surum = "v0.1.0",
    [string]$Mimari = "sm61",
    [string]$Cikti = "dist"
)
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not (Test-Path -LiteralPath $Exe)) { throw "exe yok: $Exe" }
$name = "voxcpm2-turkce-ses-tasarimi-motor-$Surum-win64-cuda12.8-$Mimari"
$stage = Join-Path $env:TEMP ("rel_" + [guid]::NewGuid().ToString("N").Substring(0, 8))
$dir = Join-Path $stage $name
New-Item -ItemType Directory -Force $dir | Out-Null
Copy-Item -LiteralPath $Exe (Join-Path $dir "audiocpp_cli.exe")
Copy-Item (Join-Path $Repo "LICENSE") (Join-Path $dir "LICENSE")
Copy-Item (Join-Path $Repo "THIRD_PARTY.md") (Join-Path $dir "THIRD_PARTY.md")
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $Exe).Hash.ToLower()
$note = @"
audiocpp_cli.exe: audio.cpp v0.7.2 (Apache-2.0, ShugoAI LLC) + patches/0001-voxcpm2-4gb-ve-hiz.patch from
https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi ($Surum). Built with MSVC 2022, CUDA 12.8, CMAKE_CUDA_ARCHITECTURES=$($Mimari -replace 'sm','').
sha256 $sha

Needs at runtime (NOT included): CUDA 12.8 DLLs cudart64_12.dll, cublas64_12.dll, cublasLt64_12.dll, cufft64_11.dll
(run scripts\kur.ps1 -Adim cuda, or point ayarlar.json cuda_bin to a CUDA 12.8 bin folder) and the model
voxcpm2-q8_0.gguf (scripts\kur.ps1 -Adim model). NVIDIA driver >= 570. GPU: Pascal sm_61 build; other GPUs rebuild with kur.ps1 -Mimari.
Set "motor" in ayarlar.json to this exe. Modified source: see patches/ in the repository (Apache-2.0 section 4).
"@
[IO.File]::WriteAllText((Join-Path $dir "README.txt"), $note, (New-Object Text.UTF8Encoding $false))
New-Item -ItemType Directory -Force (Join-Path $Repo $Cikti) | Out-Null
$zip = Join-Path (Join-Path $Repo $Cikti) "$name.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path $dir -DestinationPath $zip -CompressionLevel Optimal
Remove-Item -Recurse -Force $stage
Write-Output ("ZIP: {0} ({1:N0} bytes)" -f $zip, (Get-Item $zip).Length)
Write-Output ("ZIP_SHA256: " + (Get-FileHash -Algorithm SHA256 -LiteralPath $zip).Hash.ToLower())
Write-Output ("EXE_SHA256: " + $sha)

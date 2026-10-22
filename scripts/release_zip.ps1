# Derlenmiş motoru GitHub Release zip'i olarak paketler (yalnız exe + lisans; CUDA DLL'leri ve model kur.ps1 ile ayrı indirilir).
# Packs the built engine as a release zip (exe + license notes only; CUDA DLLs and the model are fetched by kur.ps1).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\release_zip.ps1 -Exe C:\vox\motor\build\bin\audiocpp_cli.exe -Surum v0.1.1 -Cikti dist
param(
    [Parameter(Mandatory = $true)][string]$Exe,
    [string]$Surum = "v0.1.1",
    [string]$Mimari = "61-real;75-real;86-real;89;120a",   # derlemede kullanılan CMAKE_CUDA_ARCHITECTURES (README.txt'ye yazılır)
    [switch]$Vulkan,                                        # deneysel Vulkan derlemesi paketi / experimental Vulkan build package
    [string]$Cikti = "dist"
)
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not (Test-Path -LiteralPath $Exe)) { throw "exe yok: $Exe" }
$name = "voxcpm2-turkce-ses-tasarimi-motor-$Surum-win64-" + $(if ($Vulkan) { "vulkan" } else { "cuda12.8" })
$stage = Join-Path $env:TEMP ("rel_" + [guid]::NewGuid().ToString("N").Substring(0, 8))
$dir = Join-Path $stage $name
New-Item -ItemType Directory -Force $dir | Out-Null
Copy-Item -LiteralPath $Exe (Join-Path $dir "audiocpp_cli.exe")
Copy-Item (Join-Path $Repo "LICENSE") (Join-Path $dir "LICENSE")
Copy-Item (Join-Path $Repo "THIRD_PARTY.md") (Join-Path $dir "THIRD_PARTY.md")
$sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $Exe).Hash.ToLower()
$kurArg = $(if ($Vulkan) { " -Vulkan" } else { "" })
$note = @"
BU EXE ÇİFT TIKLANMAZ. Kurulum: depoyu klonlayın ve  powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox$kurArg
  çalıştırın (model + $(if ($Vulkan) { "bu exe" } else { "CUDA DLL'leri + bu exe" }) + ayarlar). Arayüz:  .venv\Scripts\python.exe -m ses_tasarim.arayuz
DO NOT DOUBLE-CLICK THIS EXE. Install: clone the repo and run  powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox$kurArg
  (model + $(if ($Vulkan) { "this exe" } else { "CUDA DLLs + this exe" }) + settings). Web UI:  .venv\Scripts\python.exe -m ses_tasarim.arayuz
Depo / repo: https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi  ($Surum)

audiocpp_cli.exe: audio.cpp v0.7.2 (Apache-2.0, ShugoAI LLC) + patches/0001-voxcpm2-4gb-ve-hiz.patch (Apache-2.0 section 4: modified source).

"@
if ($Vulkan) {
    $note += @"
DENEYSEL / EXPERIMENTAL Vulkan build (ggml Vulkan backend, MSVC 2022, Vulkan headers 1.4, glslc). No CUDA needed.
Targets AMD, Intel and NVIDIA GPUs with a Vulkan 1.3 driver. Verified only on an NVIDIA GTX 1050 Ti (4 GB) with the Vulkan
backend; NOT yet tested on AMD or Intel hardware: please report results in the repository's Discussions.
sha256 $sha

Needs at runtime (NOT in this zip): a GPU driver with Vulkan 1.3 (vulkan-1.dll ships with the driver) and the model
voxcpm2-q8_0.gguf (kur.ps1 -Vulkan downloads it). The exe is a command-line engine driven by the Python package.
"@
} else {
    $note += @"
Built with MSVC 2022 + CUDA 12.8, CMAKE_CUDA_ARCHITECTURES=$Mimari
GPUs: native code for GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx (sm_89), RTX 50xx (sm_120a);
other CUDA GPUs >= Pascal run the embedded compute_89 PTX via driver JIT (slower first start). Maxwell and older: not supported.
sha256 $sha

Needs at runtime (NOT in this zip): CUDA 12.8 DLLs cudart64_12.dll, cublas64_12.dll, cublasLt64_12.dll, cufft64_11.dll
(kur.ps1 -Adim cuda puts them in <Kok>\cuda\bin; or set ayarlar.json "cuda_bin" to any CUDA 12.8 bin folder) and the model
voxcpm2-q8_0.gguf (kur.ps1 -Adim model). NVIDIA driver >= 570. The exe is a command-line engine driven by the Python package.
"@
}
[IO.File]::WriteAllText((Join-Path $dir "README.txt"), $note, (New-Object Text.UTF8Encoding $false))
New-Item -ItemType Directory -Force (Join-Path $Repo $Cikti) | Out-Null
$zip = Join-Path (Join-Path $Repo $Cikti) "$name.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
# Girdi adları elle "/" ile yazılır: Compress-Archive ve .NET Framework ZipFile "\" yazar; unzip ve Linux araçları bozuk ad verir.
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$arsiv =[IO.Compression.ZipFile]::Open($zip, [IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($f in (Get-ChildItem -LiteralPath $dir -File | Sort-Object Name)) {
        [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($arsiv, $f.FullName, "$name/$($f.Name)", [IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
} finally { $arsiv.Dispose() }
Remove-Item -Recurse -Force $stage
Write-Output ("ZIP: {0} ({1:N0} bytes)" -f $zip, (Get-Item $zip).Length)
Write-Output ("ZIP_SHA256: " + (Get-FileHash -Algorithm SHA256 -LiteralPath $zip).Hash.ToLower())
Write-Output ("EXE_SHA256: " + $sha)

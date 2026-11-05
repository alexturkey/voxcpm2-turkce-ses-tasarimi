# Derlenmiş motoru GitHub Release zip'i olarak paketler (yalnız exe + lisans; CUDA DLL'leri ve model kur.ps1 ile ayrı indirilir).
# Packs the built engine as a release zip (exe + license notes only; CUDA DLLs and the model are fetched by kur.ps1).
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\release_zip.ps1 -Exe C:\vox\motor\build\bin\audiocpp_cli.exe -Surum v0.1.1 -Cikti dist
param(
    [Parameter(Mandatory = $true)][string]$Exe,
    [string]$Surum = "v0.1.1",
    [string]$Mimari = "61-real;75-real;86-real;89;120a",   # derlemede kullanılan CMAKE_CUDA_ARCHITECTURES (README.txt'ye yazılır)
    [switch]$Vulkan,                                        # deneysel Vulkan derlemesi paketi / experimental Vulkan build package
    [ValidateSet("avx2", "uyumlu")][string]$Islemci = "avx2",  # Vulkan: avx2 = derle.ps1 -Islemci avx2, uyumlu = -Islemci tasinabilir
    [string]$Cikti = "dist"
)
$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not (Test-Path -LiteralPath $Exe)) { throw "exe yok: $Exe" }
if ($Vulkan) {
    # Etiket exe'ye uysun: derleme klasorunun CMakeCache.txt'si okunur (<Build>\bin\audiocpp_cli.exe -> <Build>\CMakeCache.txt)
    # The label must match the binary: read the build folder's CMakeCache.txt.
    $cache = Join-Path (Split-Path (Split-Path (Resolve-Path -LiteralPath $Exe).Path)) "CMakeCache.txt"
    if (-not (Test-Path -LiteralPath $cache)) { throw "CMakeCache.txt yok: $cache (exe'yi derle.ps1 -Build klasorunden verin / pass the exe from its build folder)" }
    $deger = @{}
    foreach ($satir in Get-Content -LiteralPath $cache) { if ($satir -match '^(GGML_\w+):BOOL=(\w+)$') { $deger[$matches[1]] = $matches[2] } }
    $ust = @{ GGML_AVX512 = "OFF"; GGML_AVX512_VBMI = "OFF"; GGML_AVX512_VNNI = "OFF"; GGML_AVX512_BF16 = "OFF"; GGML_AVX_VNNI = "OFF"; GGML_BMI2 = "OFF" }
    $beklenen = if ($Islemci -eq "uyumlu") { @{ GGML_NATIVE = "OFF"; GGML_SSE42 = "OFF"; GGML_AVX = "OFF"; GGML_AVX2 = "OFF" } + $ust } else { @{ GGML_NATIVE = "OFF"; GGML_AVX2 = "ON" } + $ust }
    $derleAdi = if ($Islemci -eq "uyumlu") { "tasinabilir" } else { "avx2" }
    foreach ($k in $beklenen.Keys) {
        if ($deger[$k] -ne $beklenen[$k]) { throw "exe -Islemci $Islemci ile uyusmuyor: $k=$($deger[$k]) (beklenen $($beklenen[$k])); derle.ps1 -Islemci $derleAdi ile derleyin" }
    }
    # Damga: CMakeCache yapilandirmayi gosterir, exe'yi degil; derle.ps1'in basarida yazdigi damga exe'nin kendisini baglar
    # Stamp: the cache shows the configuration, not the binary; derle.ps1's stamp binds this exact exe to the option
    $damga = Join-Path (Split-Path $cache) "islemci.txt"
    if (-not (Test-Path -LiteralPath $damga)) { throw "islemci.txt yok: $damga (derle.ps1 -Islemci $derleAdi ile yeniden calistirin; degisiklik yoksa derleme aninda biter)" }
    $d = "$(Get-Content -LiteralPath $damga -TotalCount 1)".Trim() -split ' '   # bos dosya: "" -> asagida anlasilir hata
    $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $Exe).Hash.ToLower()
    if ($d[0] -ne $derleAdi -or $d[1] -ne $sha) { throw "damga exe'ye uymuyor: '$($d -join ' ')' (beklenen '$derleAdi $sha'); derleme dusmus ya da exe degismis olabilir" }
    Write-Output "ISLEMCI: $Islemci ($cache, damga $($sha.Substring(0, 8)))"
}
$name = "voxcpm2-turkce-ses-tasarimi-motor-$Surum-win64-" + $(if ($Vulkan) { "vulkan" + $(if ($Islemci -eq "uyumlu") { "-uyumlu" } else { "" }) } else { "cuda12.8" })
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

audiocpp_cli.exe: audio.cpp v0.7.2 (Apache-2.0, ShugoAI LLC) + patches/0001-voxcpm2-4gb-ve-hiz.patch, 0002-voxcpm2-kelime-zamani.patch$(if ($Vulkan) { "" } else { ", 0003-ggml-cuda-block-reduce-yarisi.patch" }) (Apache-2.0 section 4: modified source).$(if ($Vulkan) { "`n0003 (ggml-cuda only) is not part of the Vulkan build: it changes CUDA kernels that a Vulkan build does not compile." } else { "" })

"@
if ($Vulkan) {
    $note += @"
DENEYSEL / EXPERIMENTAL Vulkan build (ggml Vulkan backend, MSVC 2022, Vulkan headers 1.4, glslc). No CUDA needed.
$(if ($Islemci -eq "uyumlu") { "CPU: UYUMLU / COMPATIBLE build, no AVX (SSE2 baseline): runs on any x86-64 CPU. Reference-voice encoding on the CPU is
about 3.8x slower than the AVX2 build; use it only if the AVX2 build does not start on your CPU." } else { "CPU: needs AVX2 (Intel 4th gen Core / Haswell 2013+, AMD 2015+). If it does not start on an older CPU, use the
-uyumlu (compatible) zip of the same release." })
Targets AMD, Intel and NVIDIA GPUs with a Vulkan 1.2 or newer driver (the engine's minimum; tested with Vulkan 1.3 drivers).
Tested with this exact exe on an NVIDIA GTX 1050 Ti (4 GB) and an Intel HD Graphics 630 (integrated): reading, word timing,
30 s voice design, same seed = same audio. Integrated GPUs are slow (about 40-50 s of compute per 1 s of speech), use up
to about 8 GB of system RAM, and VRAM is shown as not measurable (shared memory). On cards with a low compute dispatch
limit (e.g. Intel) the Python package decodes audio in 5 s pieces instead of 10 s automatically (same audio, measured).
An earlier Vulkan build (v0.1.1, without word timing) was reported working on an AMD Radeon RX 6900 XT; this build is NOT
yet tested on AMD: please report results in the repository's Discussions.
sha256 $sha

Needs at runtime (NOT in this zip): a GPU driver with Vulkan 1.2 or newer (vulkan-1.dll ships with the driver) and the model
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
$ciktiDir = if ([IO.Path]::IsPathRooted($Cikti)) { $Cikti } else { Join-Path $Repo $Cikti }   # goreli: repoya gore / relative: under the repo
New-Item -ItemType Directory -Force $ciktiDir | Out-Null
$zip = Join-Path $ciktiDir "$name.zip"
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

# audio.cpp (yamali) motorunu derler. / Builds the patched audio.cpp engine.
# Kullanim / usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\derle.ps1 -Kaynak C:\vox\motor\src -Build C:\vox\motor\build -Cuda C:\vox\cuda
# Cikti / output: <Build>\bin\audiocpp_cli.exe   Basarida son satir: BUILD_OK
param(
    [Parameter(Mandatory = $true)][string]$Kaynak,   # yamali audio.cpp v0.7.2 kaynagi / patched source dir
    [Parameter(Mandatory = $true)][string]$Build,    # derleme klasoru (kisa yol!) / build dir (short path!)
    [Parameter(Mandatory = $true)][string]$Cuda,     # CUDA 12.8 koku: bin\nvcc.exe burada / CUDA 12.8 root
    [int]$Paralel = 6,
    [string]$Mimari = "61",                          # GTX 1050 Ti = sm_61 (Pascal). RTX 30xx: 86, RTX 40xx: 89
    [switch]$DusukOncelik                            # derlemeyi BelowNormal oncelikle calistir
)
$ErrorActionPreference = "Stop"

if (($Build.Length) -gt 40) {
    Write-Warning "Build yolu uzun ($($Build.Length) karakter). nvcc 260 karakter sinirinda duser; C:\vox gibi kisa bir kok kullan."
}
if (-not (Test-Path (Join-Path $Cuda "bin\nvcc.exe"))) { throw "nvcc bulunamadi: $Cuda\bin\nvcc.exe" }
if (-not (Test-Path (Join-Path $Kaynak "CMakeLists.txt"))) { throw "kaynak bulunamadi: $Kaynak\CMakeLists.txt" }

# Visual Studio 2022 Build Tools: vswhere ile bul / locate with vswhere
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (-not (Test-Path $vswhere)) { throw "vswhere.exe yok: Visual Studio 2022 Build Tools kurulu degil (AGENTS.md adim 1)" }
$vs = & $vswhere -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath | Select-Object -First 1
if (-not $vs) { throw "MSVC C++ araclari (VC.Tools.x86.x64) bulunamadi; Build Tools'a 'Desktop development with C++' is yukunu ekle" }
$vcvars = Join-Path $vs "VC\Auxiliary\Build\vcvars64.bat"
$cmake = Join-Path $vs "Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
$ninja = Join-Path $vs "Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe"
foreach ($p in @($vcvars, $cmake, $ninja)) { if (-not (Test-Path $p)) { throw "eksik: $p (Build Tools'ta 'C++ CMake tools for Windows' bileseni gerekli)" } }
Write-Output "VS: $vs"

# MSVC ortami yalniz bu surece / MSVC env only for this process
cmd /c "`"$vcvars`" >nul && set" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) }
}
$env:CUDA_PATH = $Cuda; $env:CUDATOOLKIT_ROOT = $Cuda
$tmp = Join-Path $Build "tmp"; New-Item -ItemType Directory -Force $tmp | Out-Null
$env:TEMP = $tmp; $env:TMP = $tmp
if ($DusukOncelik) { (Get-Process -Id $PID).PriorityClass = "BelowNormal" }

& $cmake -S $Kaynak -B $Build -G Ninja "-DCMAKE_MAKE_PROGRAM=$ninja" `
  -DCMAKE_C_FLAGS=/utf-8 "-DCMAKE_CXX_FLAGS=/utf-8 /EHsc /MP4" `
  -DOpenMP_C_FLAGS=/openmp:experimental -DOpenMP_CXX_FLAGS=/openmp:experimental `
  -DAUDIOCPP_MODEL_SET=custom -DAUDIOCPP_MODELS=voxcpm2 -DAUDIOCPP_DEPLOYMENT_BUILD=ON `
  -DAUDIOCPP_BUILD_NATIVE_MODEL_MANAGER=OFF -DAUDIOCPP_EMBED_DEMO_VOICES=OFF `
  -DENGINE_ENABLE_CUDA=ON -DENGINE_ENABLE_CUDA_GRAPHS=ON "-DCMAKE_CUDA_ARCHITECTURES=$Mimari" `
  "-DCMAKE_CUDA_COMPILER=$Cuda/bin/nvcc.exe" "-DCUDAToolkit_ROOT=$Cuda" `
  -DENGINE_ENABLE_HIP=OFF -DENGINE_ENABLE_VULKAN=OFF -DENGINE_ENABLE_METAL=OFF `
  -DENGINE_ENABLE_OPENMP=ON -DGGML_OPENMP=ON -DENGINE_ENABLE_NATIVE_CPU=ON -DENGINE_ENABLE_LLAMAFILE=ON `
  -DENGINE_BUILD_TESTS=OFF -DENGINE_BUILD_EXAMPLES=OFF -DCMAKE_OBJECT_PATH_MAX=220 -DCMAKE_BUILD_TYPE=Release
if ($LASTEXITCODE -ne 0) { throw "cmake configure failed" }
& $cmake --build $Build --target audiocpp_cli --parallel $Paralel
if ($LASTEXITCODE -ne 0) { throw "build failed" }
$exe = Join-Path $Build "bin\audiocpp_cli.exe"
if (-not (Test-Path $exe)) { throw "exe yok: $exe" }
Write-Output ("EXE: {0} ({1} bytes)" -f $exe, (Get-Item $exe).Length)
Write-Output "BUILD_OK"

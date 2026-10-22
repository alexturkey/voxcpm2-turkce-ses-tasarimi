# audio.cpp (yamali) motorunu derler. / Builds the patched audio.cpp engine.
# Kullanim / usage:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\derle.ps1 -Kaynak C:\vox\motor\src -Build C:\vox\motor\build -Cuda C:\vox\cuda
# Cikti / output: <Build>\bin\audiocpp_cli.exe   Basarida son satir: BUILD_OK
param(
    [Parameter(Mandatory = $true)][string]$Kaynak,   # yamali audio.cpp v0.7.2 kaynagi / patched source dir
    [Parameter(Mandatory = $true)][string]$Build,    # derleme klasoru (kisa yol!) / build dir (short path!)
    [string]$Cuda = "",                              # CUDA 12.8 koku: bin\nvcc.exe burada / CUDA 12.8 root (CUDA derlemesinde sart)
    [int]$Paralel = 6,
    [string]$Mimari = "61",                          # CMAKE_CUDA_ARCHITECTURES: "native" = bu PC'nin kartı; "61" = GTX 10xx; liste: "61-real;75-real;86-real;89-real;120"
    [switch]$Vulkan,                                 # deneysel: CUDA yerine Vulkan arka ucu (AMD/Intel/NVIDIA) / experimental Vulkan backend instead of CUDA
    [string]$VulkanSdk = $env:VULKAN_SDK,            # Vulkan SDK koku (LunarG: Include, Lib, Bin) ya da glslc + headers + vulkan-1.lib iceren klasor
    [switch]$DusukOncelik                            # derlemeyi BelowNormal oncelikle calistir
)
$ErrorActionPreference = "Stop"

if (($Build.Length) -gt 40) {
    Write-Warning "Build yolu uzun ($($Build.Length) karakter). nvcc 260 karakter sinirinda duser; C:\vox gibi kisa bir kok kullan."
}
if (-not (Test-Path (Join-Path $Kaynak "CMakeLists.txt"))) { throw "kaynak bulunamadi: $Kaynak\CMakeLists.txt" }
if ($Vulkan) {
    if (-not $VulkanSdk) { throw "Vulkan icin -VulkanSdk <kok> ya da VULKAN_SDK gerekli (LunarG SDK: https://vulkan.lunarg.com/sdk/home)" }
    function Bul([string[]]$adaylar, [string]$ne) { foreach ($a in $adaylar) { $p = Join-Path $VulkanSdk $a; if (Test-Path $p) { return $p } }; throw "Vulkan SDK'da $ne yok: $VulkanSdk ($($adaylar -join ', '))" }
    $glslc = Bul @("Bin\glslc.exe", "bin\glslc.exe") "glslc.exe"
    $vkInc = Split-Path (Split-Path (Bul @("Include\vulkan\vulkan.h", "headers\include\vulkan\vulkan.h", "include\vulkan\vulkan.h") "vulkan\vulkan.h"))
    $vkLib = Bul @("Lib\vulkan-1.lib", "lib\vulkan-1.lib") "vulkan-1.lib"
    Write-Output "Vulkan: glslc=$glslc include=$vkInc lib=$vkLib"
    $backendFlags = @("-DENGINE_ENABLE_CUDA=OFF", "-DENGINE_ENABLE_CUDA_GRAPHS=OFF", "-DENGINE_ENABLE_VULKAN=ON",
        "-DVulkan_INCLUDE_DIR=$($vkInc -replace '\\','/')", "-DVulkan_LIBRARY=$($vkLib -replace '\\','/')", "-DVulkan_GLSLC_EXECUTABLE=$($glslc -replace '\\','/')")
} else {
    if (-not $Cuda) { throw "-Cuda <CUDA 12.8 koku> gerekli (ya da -Vulkan)" }
    if (-not (Test-Path (Join-Path $Cuda "bin\nvcc.exe"))) { throw "nvcc bulunamadi: $Cuda\bin\nvcc.exe" }
    $backendFlags = @("-DENGINE_ENABLE_CUDA=ON", "-DENGINE_ENABLE_CUDA_GRAPHS=ON", "-DCMAKE_CUDA_ARCHITECTURES=$Mimari",
        "-DCMAKE_CUDA_COMPILER=$Cuda/bin/nvcc.exe", "-DCUDAToolkit_ROOT=$Cuda", "-DENGINE_ENABLE_VULKAN=OFF")
}

# Visual Studio 2022 Build Tools: vswhere ile bul / locate with vswhere
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (-not (Test-Path $vswhere)) { throw "vswhere.exe yok: Visual Studio 2022 Build Tools kurulu degil (AGENTS.md adim 1)" }
$vs = & $vswhere -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath | Select-Object -First 1
if (-not $vs) { throw "MSVC C++ araclari (VC.Tools.x86.x64) bulunamadi; Build Tools'a 'Desktop development with C++' is yukunu ekle" }
$env:PATH = (Split-Path $vswhere) + ";" + $env:PATH    # vcvars64.bat vswhere.exe'yi PATH'te arar / vcvars64.bat looks up vswhere.exe on PATH
$vcvars = Join-Path $vs "VC\Auxiliary\Build\vcvars64.bat"
$cmake = Join-Path $vs "Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe"
$ninja = Join-Path $vs "Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe"
foreach ($p in @($vcvars, $cmake, $ninja)) { if (-not (Test-Path $p)) { throw "eksik: $p (Build Tools'ta 'C++ CMake tools for Windows' bileseni gerekli)" } }
Write-Output "VS: $vs"

# MSVC ortami yalniz bu surece / MSVC env only for this process
cmd /c "`"$vcvars`" >nul && set" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) }
}
if ($Cuda) { $env:CUDA_PATH = $Cuda; $env:CUDATOOLKIT_ROOT = $Cuda }
if ($Vulkan) { $env:PATH = (Split-Path $glslc) + ";" + $env:PATH }   # glslc'nin DLL'leri yaninda / glslc DLLs next to it
$tmp = Join-Path $Build "tmp"; New-Item -ItemType Directory -Force $tmp | Out-Null
$env:TEMP = $tmp; $env:TMP = $tmp
if ($DusukOncelik) { (Get-Process -Id $PID).PriorityClass = "BelowNormal" }

& $cmake -S $Kaynak -B $Build -G Ninja "-DCMAKE_MAKE_PROGRAM=$ninja" `
  -DCMAKE_C_FLAGS=/utf-8 "-DCMAKE_CXX_FLAGS=/utf-8 /EHsc /MP4" `
  -DOpenMP_C_FLAGS=/openmp:experimental -DOpenMP_CXX_FLAGS=/openmp:experimental `
  -DAUDIOCPP_MODEL_SET=custom -DAUDIOCPP_MODELS=voxcpm2 -DAUDIOCPP_DEPLOYMENT_BUILD=ON `
  -DAUDIOCPP_BUILD_NATIVE_MODEL_MANAGER=OFF -DAUDIOCPP_EMBED_DEMO_VOICES=OFF `
  @backendFlags `
  -DENGINE_ENABLE_HIP=OFF -DENGINE_ENABLE_METAL=OFF `
  -DENGINE_ENABLE_OPENMP=ON -DGGML_OPENMP=ON -DENGINE_ENABLE_NATIVE_CPU=ON -DENGINE_ENABLE_LLAMAFILE=ON `
  -DENGINE_BUILD_TESTS=OFF -DENGINE_BUILD_EXAMPLES=OFF -DCMAKE_OBJECT_PATH_MAX=220 -DCMAKE_BUILD_TYPE=Release
if ($LASTEXITCODE -ne 0) { throw "cmake configure failed" }
& $cmake --build $Build --target audiocpp_cli --parallel $Paralel
if ($LASTEXITCODE -ne 0) { throw "build failed" }
$exe = Join-Path $Build "bin\audiocpp_cli.exe"
if (-not (Test-Path $exe)) { throw "exe yok: $exe" }
Write-Output ("EXE: {0} ({1} bytes)" -f $exe, (Get-Item $exe).Length)
Write-Output "BUILD_OK"

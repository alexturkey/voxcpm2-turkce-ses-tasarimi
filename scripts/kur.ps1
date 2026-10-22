# Kurulum / installer:  model + CUDA 12.8 çalışma DLL'leri + hazır motor (GitHub Release) + Python paketleri + ayarlar.json + GPU kontrolü
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox            # derlemesiz (varsayılan) / no build (default)
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle     # kaynaktan derle / build from source
# Adım seçmek / select steps:  -Adim model,cuda,hazir,python,ayar,kontrol   (derleme: kaynak,derle)
# Her adım yeniden çalıştırılabilir: mevcut ve sha256'sı doğru dosya atlanır. / Idempotent: verified files are skipped.
# Çevrimdışı/yerel sürüm zip'i / local release zip:  -HazirZip C:\indirilenler\voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip
param(
    [string]$Kok = "C:\vox",                      # kısa yol şart (derlemede nvcc 260 karakter sınırı) / short path
    [string[]]$Adim = @(),                        # boş = varsayılan akış / empty = default flow
    [switch]$Derle,                               # hazır exe yerine kaynaktan derle / build instead of prebuilt
    [switch]$Vulkan,                              # DENEYSEL: AMD/Intel için Vulkan motoru (CUDA DLL'leri inmez) / EXPERIMENTAL Vulkan engine
    [string]$Mimari = "native",                   # derlemede CMAKE_CUDA_ARCHITECTURES: native = bu PC'nin kartı; 61 = GTX 10xx; 75/86/89/120
    [int]$Paralel = 6,
    [string]$HazirZip = ""                        # yerel sürüm zip'i (sha256 yine doğrulanır) / local release zip
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
try { [Console]::OutputEncoding = New-Object Text.UTF8Encoding $false } catch {}   # Türkçe harfler log dosyasında bozulmasın
$known = @("model", "cuda", "hazir", "kaynak", "derle", "python", "ayar", "kontrol")
$Adim = @($Adim | ForEach-Object { $_ -split "," } | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ })
if ($Adim.Count -eq 0) {
    if ($Vulkan -and $Derle) { throw "-Vulkan ile derleme bu betikte yok; scripts\derle.ps1 -Vulkan -VulkanSdk <LunarG SDK> ile elle derleyin" }
    if ($Vulkan)    { $Adim = @("model", "hazir", "python", "ayar", "kontrol") }
    elseif ($Derle) { $Adim = @("model", "cuda", "kaynak", "derle", "python", "ayar", "kontrol") }
    else            { $Adim = @("model", "cuda", "hazir", "python", "ayar", "kontrol") }
}
foreach ($a in $Adim) { if ($known -notcontains $a) { throw "bilinmeyen adım '$a'; seçenekler: $($known -join ', ')" } }
$derleme = $Derle -or ($Adim -contains "derle") -or ($Adim -contains "kaynak")
Write-Output ("adımlar: " + ($Adim -join ", ") + $(if ($derleme) { "  (derlemeli)" } elseif ($Vulkan) { "  (hazır Vulkan motoru, DENEYSEL)" } else { "  (hazır motor, derleme yok)" }))
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ($derleme -and $Kok.Length -gt 12) { Write-Warning "Kök yolu uzun ($Kok); derlemede nvcc düşebilir. Öneri: C:\vox" }

# --- sabitler / pinned downloads -------------------------------------------------------------------------------------
# Model: commit'e sabit URL. "main" 2026-10-19'da değişti (yeni dosya 2 955 007 488 bayt, sha256 8df1faf2…; audio.cpp v0.9.2 spec);
# bizim doğrulanmış dosya 661a224e9d9a commit'indedir. / Pinned to a commit: "main" was refreshed on 2026-10-19 (different file).
$MODEL_URL = "https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/661a224e9d9adbd49c01626f85e426f5f425d771/VoxCPM2-GGUF/voxcpm2-q8_0.gguf"
$MODEL_SHA = "c8e01ab4416011e12a28f24ede298a1aa5ce64b43f8e8aaad53b1e2fe7c96432"
$MODEL_BYTES = 2955000480
$SRC_URL = "https://github.com/0xShug0/audio.cpp/archive/refs/tags/v0.7.2.tar.gz"
$SRC_SHA = "cab8db31cec26ef8f1e39eabea1df5f02a87e8de87a5ae334b1e66217339c6bf"
$PATCH = Join-Path $Repo "patches\0001-voxcpm2-4gb-ve-hiz.patch"
# Hazır motor: GitHub Release. Sürüm, zip ve exe sha256'sı burada sabit; yeni sürümde üçü birlikte güncellenir.
$REL_SURUM = "v0.1.1"
$REL_ZIP = "voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip"
$REL_URL = "https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/$REL_SURUM/$REL_ZIP"
$REL_ZIP_SHA = "66aa6251832f8e3b09844fd9231dafa893b92f1bef2777a1712794ad9fff647e"
$REL_EXE_SHA = "eb75f6e6de3440c5a6b3583ba7581d539adbf80d6c069bde6611d350c95747d4"
# Deneysel Vulkan motoru (AMD/Intel/NVIDIA, CUDA gerekmez). Aynı sürüm etiketinde ayrı zip. / Experimental Vulkan engine, same release tag.
$REL_VK_ZIP = "voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip"
$REL_VK_ZIP_SHA = "e27886531c69105a2ef40e19c8dc5dfac2ee1afc55cb9ea4f6811ebedd271a6f"
$REL_VK_EXE_SHA = "29fa97c8869369ca186f9bfceb7b307fa3d24181f7a3711da3e135ad7731645b"
if ($Vulkan) { $REL_ZIP = $REL_VK_ZIP; $REL_ZIP_SHA = $REL_VK_ZIP_SHA; $REL_EXE_SHA = $REL_VK_EXE_SHA; $REL_URL = "https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/$REL_SURUM/$REL_ZIP" }
$CUDA_BASE = "https://developer.download.nvidia.com/compute/cuda/redist"
# CUDA 12.8 redist zipleri (kurulumsuz). Manifest: $CUDA_BASE/redistrib_12.8.2.json  Çalışma için ilk 3, derleme için 5'i.
$CUDA = @(
    @{ comp = "cuda_cudart"; zip = "cuda_cudart-windows-x86_64-12.8.90-archive.zip";  sha = "4a39058fd8519444a81cfc7ae055d136f48d1a31ffa41ae255b35b2edd61e13b"; derleme = $false },
    @{ comp = "libcublas";   zip = "libcublas-windows-x86_64-12.8.5.5-archive.zip";   sha = "0a2beedd7c1203cb9de5e5ab11943d27e41ee5d18dc3810b21bcd75be7e57a05"; derleme = $false },
    @{ comp = "libcufft";    zip = "libcufft-windows-x86_64-11.3.3.83-archive.zip";   sha = "cc6e0ba958cf23387b462017a24464c72bd901549046133f3d1ebcc3d7444c90"; derleme = $false },
    @{ comp = "cuda_nvcc";   zip = "cuda_nvcc-windows-x86_64-12.8.93-archive.zip";    sha = "9fdc70b4271ed9aad4d64cd7076a7d96ec36512d074b9995fe638de669197391"; derleme = $true },
    @{ comp = "cuda_cccl";   zip = "cuda_cccl-windows-x86_64-12.8.90-archive.zip";    sha = "bd8548fa1ae82f92910bebc3079e14bd58c5a92aa64596d46bd610a478cb39d7"; derleme = $true }
)
$RUNTIME_DLL = @("cudart64_12.dll", "cublas64_12.dll", "cublasLt64_12.dll", "cufft64_11.dll")

# --- yardımcılar / helpers ------------------------------------------------------------------------------------------
function Sha256([string]$path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower() }
function Indir([string]$url, [string]$hedef, [string]$sha) {
    if ((Test-Path -LiteralPath $hedef) -and ((Sha256 $hedef) -eq $sha)) { Write-Output "  var ve doğru: $(Split-Path $hedef -Leaf)"; return }
    Write-Output "  indiriliyor: $url"
    $tmp = "$hedef.part"
    curl.exe -L --fail --retry 3 --retry-delay 5 --progress-bar -o $tmp $url
    if ($LASTEXITCODE -ne 0) { throw "indirme başarısız: $url" }
    $got = Sha256 $tmp
    if ($got -ne $sha) { Remove-Item -LiteralPath $tmp -Force; throw "sha256 tutmadı: $hedef`n  beklenen $sha`n  gelen    $got" }
    Move-Item -LiteralPath $tmp -Destination $hedef -Force
    Write-Output "  tamam, sha256 doğru: $(Split-Path $hedef -Leaf)"
}
function GitApply([string[]]$argv, [bool]$sessiz = $false) {
    # git hata metnini stderr'a yazar; PowerShell 5.1 bunu $ErrorActionPreference=Stop ile istisnaya çevirir. Burada metin olarak gösterilir, çıkış kodu döner.
    $eap = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    try { & git @argv 2>&1 | ForEach-Object { if (-not $sessiz) { Write-Output "  git: $_" } } } finally { $ErrorActionPreference = $eap }
    return $LASTEXITCODE
}
function PythonBul {
    # 64-bit Python 3.10+; Microsoft Store'un sahte "python" takma adı ve 2.x elenir / finds a real 64-bit Python 3.10+
    foreach ($aday in @(@("py", "-3"), @("python"), @("python3"))) {
        $exe = Get-Command $aday[0] -ErrorAction SilentlyContinue
        if (-not $exe) { continue }
        $eap = $ErrorActionPreference; $ErrorActionPreference = "Continue"
        try { $v = (& $aday[0] ($aday[1..9] + @("-c", "import sys,struct;print(sys.version_info[0],sys.version_info[1],struct.calcsize('P')*8,sys.executable)")) 2>$null) } finally { $ErrorActionPreference = $eap }
        if ($v -match "^3 (\d+) 64 (.+)$" -and [int]$matches[1] -ge 10) { return $matches[2].Trim() }
    }
    return $null
}
$motorExe = Join-Path $Kok "motor\build\bin\audiocpp_cli.exe"
$cudaRoot = Join-Path $Kok "cuda"
New-Item -ItemType Directory -Force (Join-Path $Kok "indirme") | Out-Null

# --- adımlar / steps -------------------------------------------------------------------------------------------------
if ($Adim -contains "model") {
    Write-Output "== model (2,95 GB)"
    New-Item -ItemType Directory -Force (Join-Path $Kok "model") | Out-Null
    $model = Join-Path $Kok "model\voxcpm2-q8_0.gguf"
    Indir $MODEL_URL $model $MODEL_SHA
    if ((Get-Item -LiteralPath $model).Length -ne $MODEL_BYTES) { throw "model boyutu beklenen $MODEL_BYTES bayt değil" }
    Write-Output "MODEL_OK"
}

if ($Adim -contains "cuda") {
    $paket = @($CUDA | Where-Object { $derleme -or -not $_.derleme })
    Write-Output ("== CUDA 12.8 redist ({0} zip, {1}; sistem kurulumu ve PATH değişikliği yok)" -f $paket.Count, $(if ($derleme) { "~880 MB, derleyici dahil" } else { "~720 MB, yalnız çalışma DLL'leri" }))
    New-Item -ItemType Directory -Force $cudaRoot | Out-Null
    foreach ($c in $paket) {
        $zip = Join-Path $Kok ("indirme\" + $c.zip)
        Indir ("{0}/{1}/windows-x86_64/{2}" -f $CUDA_BASE, $c.comp, $c.zip) $zip $c.sha
        $tmp = Join-Path $Kok ("indirme\_ac_" + $c.comp)
        if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
        Expand-Archive -LiteralPath $zip -DestinationPath $tmp -Force
        $top = Get-ChildItem $tmp | Select-Object -First 1      # tek üst klasör atılır, hepsi tek köke birleşir
        Get-ChildItem $top.FullName | ForEach-Object {
            $dest = Join-Path $cudaRoot $_.Name
            if ($_.PSIsContainer) { robocopy $_.FullName $dest /E /NFL /NDL /NJH /NJS /NP | Out-Null } else { Copy-Item $_.FullName $dest -Force }
        }
        Remove-Item -Recurse -Force $tmp
    }
    $gerekli = $RUNTIME_DLL + $(if ($derleme) { @("nvcc.exe") } else { @() })
    foreach ($dll in $gerekli) { if (-not (Test-Path (Join-Path $cudaRoot "bin\$dll"))) { throw "CUDA eksik: bin\$dll" } }
    Write-Output "CUDA_OK"
}

if ($Adim -contains "hazir") {
    Write-Output ("== hazır motor $REL_SURUM (GitHub Release" + $(if ($Vulkan) { ", Vulkan, DENEYSEL)" } else { ")" }))
    if ($REL_ZIP_SHA -like "__*") { throw "bu kur.ps1 sürümünde hazır motor sha256'sı yok; depoyu güncelleyin (git pull)" }
    if ($HazirZip) {
        if (-not (Test-Path -LiteralPath $HazirZip)) { throw "yerel zip yok: $HazirZip" }
        $zip = (Resolve-Path -LiteralPath $HazirZip).Path
        $got = Sha256 $zip
        if ($got -ne $REL_ZIP_SHA) { throw "yerel zip sha256 tutmadı ($REL_ZIP beklenen): $got" }
        Write-Output "  yerel zip, sha256 doğru: $zip"
    } else {
        $zip = Join-Path $Kok ("indirme\" + $REL_ZIP)
        Indir $REL_URL $zip $REL_ZIP_SHA
    }
    $bin = Split-Path $motorExe
    if ((Test-Path -LiteralPath $motorExe) -and ((Sha256 $motorExe) -eq $REL_EXE_SHA)) { Write-Output "  exe var ve doğru: $motorExe" }
    else {
        $tmp = Join-Path $Kok "indirme\_ac_hazir"
        if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
        Expand-Archive -LiteralPath $zip -DestinationPath $tmp -Force
        $exe = Get-ChildItem $tmp -Recurse -Filter audiocpp_cli.exe | Select-Object -First 1
        if (-not $exe) { throw "zip içinde audiocpp_cli.exe yok" }
        $got = Sha256 $exe.FullName
        if ($got -ne $REL_EXE_SHA) { throw "exe sha256 tutmadı: $got" }
        New-Item -ItemType Directory -Force $bin | Out-Null
        Get-ChildItem $exe.DirectoryName | ForEach-Object { Copy-Item -LiteralPath $_.FullName (Join-Path $bin $_.Name) -Force }   # exe + LICENSE + THIRD_PARTY.md + README.txt
        Remove-Item -Recurse -Force $tmp
        Write-Output "  açıldı, exe sha256 doğru: $motorExe"
    }
    Write-Output "HAZIR_OK"
}

if ($Adim -contains "kaynak") {
    Write-Output "== audio.cpp v0.7.2 kaynağı + yama"
    $tar = Join-Path $Kok "indirme\audio.cpp-v0.7.2.tar.gz"
    Indir $SRC_URL $tar $SRC_SHA
    $motor = Join-Path $Kok "motor"
    $src = Join-Path $motor "src"
    if (Test-Path $src) { Write-Output "  kaynak klasörü var, yeniden açılmıyor: $src (temiz başlamak için sil)" }
    else {
        New-Item -ItemType Directory -Force $motor | Out-Null
        # Windows'un kendi tar'ı (bsdtar); Git Bash'in /usr/bin/tar'ı "E:" sürücü harfini sunucu sanır. / Windows' own tar, not Git Bash's.
        $tarExe = Join-Path $env:SystemRoot "System32\tar.exe"
        if (-not (Test-Path $tarExe)) { throw "tar.exe yok ($tarExe); Windows 10 1803+ gerekir" }
        & $tarExe -xzf $tar -C $motor
        if ($LASTEXITCODE -ne 0) { throw "tar açılamadı" }
        Rename-Item (Join-Path $motor "audio.cpp-0.7.2") "src"
    }
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git bulunamadı; Git for Windows kurun (yama için gerekli)" }
    Push-Location $src
    try {
        if ((GitApply @("apply", "--reverse", "--check", $PATCH) $true) -eq 0) { Write-Output "  yama zaten uygulanmış" }
        else {
            if ((GitApply @("apply", "--check", $PATCH)) -ne 0) { throw "yama uygulanamıyor (kaynak saf v0.7.2 mi? CRLF'ye çevrilmiş mi?)" }
            if ((GitApply @("apply", $PATCH)) -ne 0) { throw "git apply başarısız" }
            if ((GitApply @("apply", "--reverse", "--check", $PATCH)) -ne 0) { throw "yama sessizce atlandı (git deposu içinde misin? --directory gerekir)" }
            Write-Output "  yama uygulandı ve doğrulandı"
        }
    } finally { Pop-Location }
    Write-Output "KAYNAK_OK"
}

if ($Adim -contains "derle") {
    Write-Output "== derleme (~15-25 dk, $Paralel iş, mimari $Mimari)"
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo "scripts\derle.ps1") `
        -Kaynak (Join-Path $Kok "motor\src") -Build (Join-Path $Kok "motor\build") -Cuda $cudaRoot -Mimari $Mimari -Paralel $Paralel
    if ($LASTEXITCODE -ne 0) { throw "derleme başarısız" }
    Write-Output "DERLE_OK"
}

if ($Adim -contains "python") {
    Write-Output "== Python paketleri (.venv + numpy, soundfile)"
    $py = PythonBul
    if (-not $py) { throw "64-bit Python 3.10+ bulunamadı. Kurun: winget install Python.Python.3.12  (ya da python.org), sonra yeni bir PowerShell açın" }
    Write-Output "  python: $py"
    $venv = Join-Path $Repo ".venv"
    $vpy = Join-Path $venv "Scripts\python.exe"
    if (-not (Test-Path $vpy)) { & $py -m venv $venv; if ($LASTEXITCODE -ne 0) { throw "venv oluşturulamadı" } }
    & $vpy -m pip install --quiet --disable-pip-version-check -r (Join-Path $Repo "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "pip install başarısız" }
    & $vpy -c "import numpy, soundfile"
    if ($LASTEXITCODE -ne 0) { throw "numpy/soundfile içe aktarılamadı" }
    Write-Output "PYTHON_OK"
}

if ($Adim -contains "ayar") {
    Write-Output "== ayarlar.json"
    $ayar = [ordered]@{
        motor = $motorExe -replace "\\", "/"
        model = (Join-Path $Kok "model\voxcpm2-q8_0.gguf") -replace "\\", "/"
        cuda_bin = $(if ($Vulkan) { "" } else { (Join-Path $cudaRoot "bin") -replace "\\", "/" })
        backend = $(if ($Vulkan) { "vulkan" } else { "cuda" }); sesler = "sesler"; hazir_sesler = "hazir_sesler"; onbellek = "onbellek"
        audiovae_threads = 6; motor_threads = 4; port = 8765
    }
    $hedef = Join-Path $Repo "ayarlar.json"
    [IO.File]::WriteAllText($hedef, (($ayar | ConvertTo-Json) + "`n"), (New-Object Text.UTF8Encoding $false))
    Write-Output "  yazıldı: $hedef"
    Write-Output "AYAR_OK"
}

if ($Adim -contains "kontrol") {
    Write-Output "== kontrol: motor + CUDA DLL + ekran kartı"
    if (-not (Test-Path -LiteralPath $motorExe)) { throw "motor yok: $motorExe (adım: hazir ya da derle)" }
    if (-not $Vulkan) { foreach ($dll in $RUNTIME_DLL) { if (-not (Test-Path (Join-Path $cudaRoot "bin\$dll"))) { throw "CUDA DLL eksik: $cudaRoot\bin\$dll (adım: cuda)" } } }
    $eap = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    $eskiPath = $env:PATH; if (-not $Vulkan) { $env:PATH = (Join-Path $cudaRoot "bin") + ";" + $env:PATH }
    try { $cikti = (& $motorExe --list-devices 2>&1 | ForEach-Object { "$_" }) } finally { $env:PATH = $eskiPath; $ErrorActionPreference = $eap }
    $gpu = $cikti | Where-Object { $_ -match $(if ($Vulkan) { "(?i)vulkan:\d" } else { "CUDA:\d" }) }
    if (-not $gpu) { Write-Output ($cikti -join "`n"); throw $(if ($Vulkan) { "motor Vulkan cihazı görmedi (güncel AMD/Intel/NVIDIA sürücüsü ve vulkan-1.dll gerekir)" } else { "motor ekran kartını görmedi (sürücü >= 570 mi? nvidia-smi çalışıyor mu?)" }) }
    Write-Output "  $($gpu -join "`n  ")"
    if ($Vulkan -and $gpu.Count -gt 1) {
        # Birden çok Vulkan cihazı (ör. dizüstünde iGPU + ekran kartı): ayrık kartı ([GPU]) seç, ayarlar.json "cihaz" alanına yaz.
        # Several Vulkan devices (laptop iGPU + dGPU): prefer the discrete [GPU] and write its index to ayarlar.json "cihaz".
        $sec = ($gpu | Where-Object { $_ -match "\[GPU\]" } | Select-Object -First 1); if (-not $sec) { $sec = $gpu[0] }
        if ($sec -match "(?i)vulkan:(\d+)") {
            $no = [int]$matches[1]
            $hedef = Join-Path $Repo "ayarlar.json"
            if (Test-Path $hedef) {
                $j = Get-Content -Raw -Encoding UTF8 $hedef | ConvertFrom-Json
                if ($j.PSObject.Properties["cihaz"]) { $j.cihaz = $no } else { $j | Add-Member -NotePropertyName cihaz -NotePropertyValue $no }
                [IO.File]::WriteAllText($hedef, (($j | ConvertTo-Json) + "`n"), (New-Object Text.UTF8Encoding $false))
                Write-Output "  seçilen Vulkan cihazı: $no ($sec) → ayarlar.json cihaz"
            }
        }
    }
    Write-Output "KONTROL_OK"
}
Write-Output "KURULUM_OK"
Write-Output "Arayüz / web UI:  .venv\Scripts\python.exe -m ses_tasarim.arayuz   (sonra tarayıcıda http://127.0.0.1:8765/ )"

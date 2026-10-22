# Sıfırdan kurulum / fresh install:  model + CUDA 12.8 + audio.cpp v0.7.2 kaynağı + yama + derleme + ayarlar.json
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
# Adım seçmek / select steps:  -Adim model,cuda,kaynak,derle,ayar   (varsayılan hepsi / default: all)
# Her adım yeniden çalıştırılabilir: mevcut ve sha256'sı doğru dosya atlanır. / Idempotent: verified files are skipped.
param(
    [string]$Kok = "C:\vox",                      # kısa yol şart (nvcc 260 karakter sınırı) / short path required
    [string[]]$Adim = @("model", "cuda", "kaynak", "derle", "ayar"),
    [string]$Mimari = "61",                       # CUDA mimarisi: GTX 10xx=61, RTX 20xx=75, 30xx=86, 40xx=89
    [int]$Paralel = 6
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$Adim = @($Adim | ForEach-Object { $_ -split "," } | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ })
$known = @("model", "cuda", "kaynak", "derle", "ayar")
foreach ($a in $Adim) { if ($known -notcontains $a) { throw "bilinmeyen adım '$a'; seçenekler: $($known -join ', ')" } }
Write-Output ("adımlar: " + ($Adim -join ", "))
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ($Kok.Length -gt 12) { Write-Warning "Kök yolu uzun ($Kok); derlemede nvcc düşebilir. Öneri: C:\vox" }

$MODEL_URL = "https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/main/VoxCPM2-GGUF/voxcpm2-q8_0.gguf"
$MODEL_SHA = "c8e01ab4416011e12a28f24ede298a1aa5ce64b43f8e8aaad53b1e2fe7c96432"
$MODEL_BYTES = 2955000480
$SRC_URL = "https://github.com/0xShug0/audio.cpp/archive/refs/tags/v0.7.2.tar.gz"
$SRC_SHA = "cab8db31cec26ef8f1e39eabea1df5f02a87e8de87a5ae334b1e66217339c6bf"
$PATCH = Join-Path $Repo "patches\0001-voxcpm2-4gb-ve-hiz.patch"
$CUDA_BASE = "https://developer.download.nvidia.com/compute/cuda/redist"
# CUDA 12.8.2 redist zipleri (kurulumsuz). Manifest: $CUDA_BASE/redistrib_12.8.2.json
$CUDA = @(
    @{ comp = "cuda_cudart"; zip = "cuda_cudart-windows-x86_64-12.8.90-archive.zip";  sha = "4a39058fd8519444a81cfc7ae055d136f48d1a31ffa41ae255b35b2edd61e13b" },
    @{ comp = "libcublas";   zip = "libcublas-windows-x86_64-12.8.5.5-archive.zip";   sha = "0a2beedd7c1203cb9de5e5ab11943d27e41ee5d18dc3810b21bcd75be7e57a05" },
    @{ comp = "libcufft";    zip = "libcufft-windows-x86_64-11.3.3.83-archive.zip";   sha = "cc6e0ba958cf23387b462017a24464c72bd901549046133f3d1ebcc3d7444c90" },
    @{ comp = "cuda_nvcc";   zip = "cuda_nvcc-windows-x86_64-12.8.93-archive.zip";    sha = "9fdc70b4271ed9aad4d64cd7076a7d96ec36512d074b9995fe638de669197391" },
    @{ comp = "cuda_cccl";   zip = "cuda_cccl-windows-x86_64-12.8.90-archive.zip";    sha = "bd8548fa1ae82f92910bebc3079e14bd58c5a92aa64596d46bd610a478cb39d7" }
)

function Sha256([string]$path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower() }
function Indir([string]$url, [string]$hedef, [string]$sha) {
    if ((Test-Path -LiteralPath $hedef) -and ((Sha256 $hedef) -eq $sha)) { Write-Output "  var ve doğru: $(Split-Path $hedef -Leaf)"; return }
    Write-Output "  indiriliyor: $url"
    $tmp = "$hedef.part"
    curl.exe -L --fail --retry 3 --retry-delay 5 -o $tmp $url
    if ($LASTEXITCODE -ne 0) { throw "indirme başarısız: $url" }
    $got = Sha256 $tmp
    if ($got -ne $sha) { Remove-Item -LiteralPath $tmp -Force; throw "sha256 tutmadı: $hedef`n  beklenen $sha`n  gelen    $got" }
    Move-Item -LiteralPath $tmp -Destination $hedef -Force
    Write-Output "  tamam, sha256 doğru: $(Split-Path $hedef -Leaf)"
}

New-Item -ItemType Directory -Force (Join-Path $Kok "indirme") | Out-Null

if ($Adim -contains "model") {
    Write-Output "== model (2,95 GB)"
    New-Item -ItemType Directory -Force (Join-Path $Kok "model") | Out-Null
    $model = Join-Path $Kok "model\voxcpm2-q8_0.gguf"
    Indir $MODEL_URL $model $MODEL_SHA
    if ((Get-Item -LiteralPath $model).Length -ne $MODEL_BYTES) { throw "model boyutu beklenen $MODEL_BYTES bayt değil" }
    Write-Output "MODEL_OK"
}

if ($Adim -contains "cuda") {
    Write-Output "== CUDA 12.8 redist (5 zip, ~880 MB; sistem kurulumu ve PATH değişikliği yok)"
    $cudaRoot = Join-Path $Kok "cuda"
    New-Item -ItemType Directory -Force $cudaRoot | Out-Null
    foreach ($c in $CUDA) {
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
    foreach ($dll in @("cudart64_12.dll", "cublas64_12.dll", "cublasLt64_12.dll", "cufft64_11.dll", "nvcc.exe")) {
        if (-not (Test-Path (Join-Path $cudaRoot "bin\$dll"))) { throw "CUDA eksik: bin\$dll" }
    }
    Write-Output "CUDA_OK"
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
        tar.exe -xzf $tar -C $motor
        if ($LASTEXITCODE -ne 0) { throw "tar açılamadı" }
        Rename-Item (Join-Path $motor "audio.cpp-0.7.2") "src"
    }
    Push-Location $src
    try {
        git apply --reverse --check $PATCH 2>$null
        if ($LASTEXITCODE -eq 0) { Write-Output "  yama zaten uygulanmış" }
        else {
            git apply --check $PATCH
            if ($LASTEXITCODE -ne 0) { throw "yama uygulanamıyor (kaynak saf v0.7.2 mi? CRLF'ye çevrilmiş mi?)" }
            git apply $PATCH
            if ($LASTEXITCODE -ne 0) { throw "git apply başarısız" }
            git apply --reverse --check $PATCH
            if ($LASTEXITCODE -ne 0) { throw "yama sessizce atlandı (git deposu içinde misin? --directory gerekir)" }
            Write-Output "  yama uygulandı ve doğrulandı"
        }
    } finally { Pop-Location }
    Write-Output "KAYNAK_OK"
}

if ($Adim -contains "derle") {
    Write-Output "== derleme (~15-25 dk, 6 çekirdek)"
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo "scripts\derle.ps1") `
        -Kaynak (Join-Path $Kok "motor\src") -Build (Join-Path $Kok "motor\build") -Cuda (Join-Path $Kok "cuda") -Mimari $Mimari -Paralel $Paralel
    if ($LASTEXITCODE -ne 0) { throw "derleme başarısız" }
    Write-Output "DERLE_OK"
}

if ($Adim -contains "ayar") {
    Write-Output "== ayarlar.json"
    $ayar = [ordered]@{
        motor = (Join-Path $Kok "motor\build\bin\audiocpp_cli.exe") -replace "\\", "/"
        model = (Join-Path $Kok "model\voxcpm2-q8_0.gguf") -replace "\\", "/"
        cuda_bin = (Join-Path $Kok "cuda\bin") -replace "\\", "/"
        backend = "cuda"; sesler = "sesler"; hazir_sesler = "hazir_sesler"; onbellek = "onbellek"
        audiovae_threads = 6; motor_threads = 4; port = 8765
    }
    $hedef = Join-Path $Repo "ayarlar.json"
    [IO.File]::WriteAllText($hedef, (($ayar | ConvertTo-Json) + "`n"), (New-Object Text.UTF8Encoding $false))
    Write-Output "  yazıldı: $hedef"
    Write-Output "AYAR_OK"
}
Write-Output "KURULUM_OK"

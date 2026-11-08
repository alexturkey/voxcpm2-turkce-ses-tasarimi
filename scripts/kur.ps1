# Kurulum / installer:  model + CUDA 12.8 çalışma DLL'leri + hazır motor (GitHub Release) + Python paketleri + ayarlar.json + GPU kontrolü
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox            # derlemesiz (varsayılan) / no build (default)
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle     # kaynaktan derle / build from source
# Adım seçmek / select steps:  -Adim model,cuda,hazir,python,ayar,kontrol   (derleme: kaynak,derle)
# Her adım yeniden çalıştırılabilir: mevcut ve sha256'sı doğru dosya atlanır. / Idempotent: verified files are skipped.
# Çevrimdışı/yerel sürüm zip'i / local release zip:  -HazirZip C:\indirilenler\voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-cuda12.8.zip
# AMD / Intel (deneysel):  -Vulkan  [-Islemci oto|avx2|uyumlu]   paket işlemciye göre seçilir / package picked from the CPU
param(
    [string]$Kok = "C:\vox",                      # kısa yol şart (derlemede nvcc 260 karakter sınırı) / short path
    [string[]]$Adim = @(),                        # boş = varsayılan akış / empty = default flow
    [switch]$Derle,                               # hazır exe yerine kaynaktan derle / build instead of prebuilt
    [switch]$Vulkan,                              # DENEYSEL: AMD/Intel için Vulkan motoru (CUDA DLL'leri inmez) / EXPERIMENTAL Vulkan engine
    [string]$Mimari = "native",                   # derlemede CMAKE_CUDA_ARCHITECTURES: native = bu PC'nin kartı; 61 = GTX 10xx; 75/86/89/120
    [int]$Paralel = 6,
    [string]$HazirZip = "",                       # yerel sürüm zip'i (sha256 yine doğrulanır) / local release zip
    [ValidateSet("oto", "avx2", "uyumlu")]
    [string]$Islemci = "oto"                      # Vulkan paketi: oto = işlemciye göre; avx2 / uyumlu = elle / Vulkan package choice
)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
try { [Console]::OutputEncoding = New-Object Text.UTF8Encoding $false } catch {}   # Türkçe harfler log dosyasında bozulmasın
$known = @("model", "cuda", "hazir", "kaynak", "derle", "python", "ayar", "kontrol")
$Adim = @($Adim | ForEach-Object { $_ -split "," } | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ })
if ($Adim.Count -eq 0) {
    if ($Vulkan -and $Derle) { throw "-Vulkan ile derleme bu betikte yok; scripts\derle.ps1 -Vulkan -VulkanSdk <LunarG SDK> ile elle derleyin" }
    if ($Vulkan)    { $Adim = @("model", "python", "hazir", "ayar", "kontrol") }   # python önce: paket seçimi onunla / python first: it picks the package
    elseif ($Derle) { $Adim = @("model", "cuda", "kaynak", "derle", "python", "ayar", "kontrol") }
    else            { $Adim = @("model", "cuda", "hazir", "python", "ayar", "kontrol") }
}
foreach ($a in $Adim) { if ($known -notcontains $a) { throw "bilinmeyen adım '$a'; seçenekler: $($known -join ', ')" } }
$derleme = $Derle -or ($Adim -contains "derle") -or ($Adim -contains "kaynak")
Write-Output ("adımlar: " + ($Adim -join ", ") + $(if ($derleme) { "  (derlemeli)" } elseif ($Vulkan) { "  (hazır Vulkan motoru, DENEYSEL)" } else { "  (hazır motor, derleme yok)" }))
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
# Motor Windows'ta yalnız ASCII yolları açabiliyor (topluluk testi, issue #6: "No mapping for the Unicode character…",
# "Failed to open log file"). Kök ASCII değilse indirmeye başlamadan dur. / The engine only opens ASCII-only paths on Windows.
if ($Kok -match '[^\x00-\x7F]') {
    throw ("Kurulum klasörü Türkçe harf ya da başka ASCII dışı karakter içeriyor: $Kok`n" +
           "  Motor bu yolu açamaz. Kısa ve yalnız İngilizce harfli bir klasör seçin, ör.: -Kok C:\vox`n" +
           "  The install folder contains non-ASCII characters; the engine cannot open it. Use a short ASCII folder, e.g. -Kok C:\vox")
}
if ($Repo -match '[^\x00-\x7F]') {
    Write-Warning ("Repo klasörü ASCII değil ($Repo); sesler ve okumalar burada, motor bu yolu açamayabilir. Öneri: repoyu C:\vox\repo gibi bir yere taşıyın.`n" +
                   "  The repo folder is not ASCII-only; voices and readings live here and the engine may fail. Move it to e.g. C:\vox\repo.")
}
if ($derleme -and $Kok.Length -gt 12) { Write-Warning "Kök yolu uzun ($Kok); derlemede nvcc düşebilir. Öneri: C:\vox" }

# --- sabitler / pinned downloads -------------------------------------------------------------------------------------
# Model: commit'e sabit URL. "main" 2026-10-19'da değişti (yeni dosya 2 955 007 488 bayt, sha256 8df1faf2…; audio.cpp v0.9.2 spec);
# bizim doğrulanmış dosya 661a224e9d9a commit'indedir. / Pinned to a commit: "main" was refreshed on 2026-10-19 (different file).
$MODEL_URL = "https://huggingface.co/audio-cpp/audio.cpp-gguf/resolve/661a224e9d9adbd49c01626f85e426f5f425d771/VoxCPM2-GGUF/voxcpm2-q8_0.gguf"
$MODEL_SHA = "c8e01ab4416011e12a28f24ede298a1aa5ce64b43f8e8aaad53b1e2fe7c96432"
$MODEL_BYTES = 2955000480
$SRC_URL = "https://github.com/0xShug0/audio.cpp/archive/refs/tags/v0.7.2.tar.gz"
$SRC_SHA = "cab8db31cec26ef8f1e39eabea1df5f02a87e8de87a5ae334b1e66217339c6bf"
$PATCHES = @((Join-Path $Repo "patches\0001-voxcpm2-4gb-ve-hiz.patch"), (Join-Path $Repo "patches\0002-voxcpm2-kelime-zamani.patch"), (Join-Path $Repo "patches\0003-ggml-cuda-block-reduce-yarisi.patch"))
# Hazır motor: GitHub Release. Sürüm, zip ve exe sha256'sı burada sabit; yeni sürümde üçü birlikte güncellenir.
$REL_SURUM = "v0.3.2"
$REL_ZIP = "voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-cuda12.8.zip"
$REL_URL = "https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/$REL_SURUM/$REL_ZIP"
$REL_ZIP_SHA = "46b554ba8b734c3ab477186671f242d323956a47e184858a6b2899788979f6a9"
$REL_EXE_SHA = "c3e05aedcd3b6d027ac0b61c65688e1ef7099fcce7af96f2c8aa1fc18ae8ef3d"
# Deneysel Vulkan motoru (AMD/Intel/NVIDIA, CUDA gerekmez), v0.3.2: yama 0001 + 0002 (kelime zamanı). İki paket:
#   avx2   AVX2 + FMA + F16C + BMI2 isteyen işlemci (Intel Haswell 2013+, AMD Excavator 2015+); hızlı olan
#   uyumlu AVX'siz, her x86-64 işlemci; sesin ilk okuması ~2,2 kat uzun (referans kodlaması işlemcide)
# Seçim (-Islemci oto, varsayılan): ses_tasarim/islemci.py (numpy işlemci tespiti) + AVX2 exe'sinin yerleşmeden önce deneme
# çalışması ("ok" dışı her sonuç -> uyumlu). -Islemci avx2|uyumlu elle seçer, deneme yapılmaz.
# Experimental Vulkan engine v0.3.2, two packages; the installer picks one from the CPU and a test run of the AVX2 exe.
$REL_VK_SURUM = "v0.3.2"
$REL_VK = @{
    avx2   = @{ zip = "voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-vulkan.zip"
                url = "https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.2/voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-vulkan.zip"
                zip_sha = "8450fa63b8a58a8db13b7991c086f716c308465eb455b60f89214a3da0612aae"
                exe_sha = "9684f63c8c766d9bcc1667a8eff43a22cf31e824de233c23f91d7ae5c71734ce" }
    uyumlu = @{ zip = "voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-vulkan-uyumlu.zip"
                url = "https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.2/voxcpm2-turkce-ses-tasarimi-motor-v0.3.2-win64-vulkan-uyumlu.zip"
                zip_sha = "dcebb7ab950f4f8905cd2241d81dc488d9d77ac2b659e688a1ee8d3c50ffd333"
                exe_sha = "8ad5957384f7774333c095673d05a1c98d5540a7dda37705ce5898c2578721b2" }
}
if ($Vulkan) { $REL_SURUM = $REL_VK_SURUM }
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
function YamaImzasi([string[]]$yamalar) {
    # Yama imzası: her yamanın sha256'sı + adı (kur.sh, kur-linux.sh, motoru_derle.sh ile aynı biçim) / patch signature, same format as the shell installers
    (($yamalar | ForEach-Object { "{0}  {1}" -f (Get-FileHash -Algorithm SHA256 -LiteralPath $_).Hash.ToLower(), (Split-Path $_ -Leaf) }) -join "`n") + "`n"
}
function YamalariUygula([string]$src, [string[]]$yamalar) {
    # Yamalar sırayla (0001 4 GB + hız, 0002 kelime zamanı, 0003 CUDA block_reduce yarışı). Uygulanınca <src>\.yama_imzasi yazılır.
    # Var olan kaynakta imza yoksa ya da tutmuyorsa (eski sürümün yamaları) sessizce derlenmez: açık hata, kaynak silinip yeniden açılır.
    # Patches in order; <src>\.yama_imzasi is written after applying. An existing source with a missing or different signature is not built.
    $imzaYol = Join-Path $src ".yama_imzasi"
    $beklenen = YamaImzasi $yamalar
    $eski = "kaynak eski ya da farklı yamalı (yama imzası tutmuyor): motor/src klasörünü silip yeniden çalıştır: $src`n" +
            "  source was patched with older or different patches (patch signature mismatch): delete motor/src and run again: $src"
    if (Test-Path -LiteralPath $imzaYol) {
        if ([IO.File]::ReadAllText($imzaYol) -ceq $beklenen) { Write-Output "  yamalar zaten uygulanmış (imza tutuyor)"; return }
        throw $eski
    }
    Push-Location $src
    try {
        for ($i = $yamalar.Count - 1; $i -ge 0; $i--) { if ((GitApply @("apply", "--reverse", "--check", $yamalar[$i]) $true) -eq 0) { throw $eski } }
        foreach ($p in $yamalar) {
            if ((GitApply @("apply", "--check", $p)) -ne 0) { throw "yama uygulanamıyor: $p (kaynak saf v0.7.2 mi? CRLF'ye çevrilmiş mi?)`n$eski" }
            if ((GitApply @("apply", $p)) -ne 0) { throw "git apply başarısız: $p" }
            if ((GitApply @("apply", "--reverse", "--check", $p)) -ne 0) { throw "yama sessizce atlandı: $p (git deposu içinde misin? --directory gerekir)" }
            Write-Output "  yama uygulandı ve doğrulandı: $(Split-Path $p -Leaf)"
        }
    } finally { Pop-Location }
    [IO.File]::WriteAllText($imzaYol, $beklenen, (New-Object Text.UTF8Encoding $false))
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

# Sürüm zip'i: indir ya da yerel zip'i doğrula; açılan exe önce geçici klasörde sha256 ile doğrulanır, sonra yerleştirilir.
# Release zip: fetch or verify the local one; the exe is verified in a temp folder first, then installed.
# (Bu yardımcılar Write-Output ile yazar; sonucu $script: değişkenine koyar, değer döndürmez.)
function ZipAl([string]$zipAdi, [string]$zipSha, [string]$url, [string]$yerel) {
    if ($yerel) {
        if (-not (Test-Path -LiteralPath $yerel)) { throw "yerel zip yok: $yerel" }
        $script:zipYol = (Resolve-Path -LiteralPath $yerel).Path
        $got = Sha256 $script:zipYol
        if ($got -ne $zipSha) { throw "yerel zip sha256 tutmadı ($zipAdi beklenen): $got" }
        Write-Output "  yerel zip, sha256 doğru: $script:zipYol"
    } else {
        $script:zipYol = Join-Path $Kok ("indirme\" + $zipAdi)
        Indir $url $script:zipYol $zipSha
    }
}
$hazirTmp = Join-Path $Kok "indirme\_ac_hazir"
function ZipAc([string]$zip, [string]$exeSha) {
    if (Test-Path $hazirTmp) { Remove-Item -Recurse -Force $hazirTmp }
    Expand-Archive -LiteralPath $zip -DestinationPath $hazirTmp -Force
    $exe = Get-ChildItem $hazirTmp -Recurse -Filter audiocpp_cli.exe | Select-Object -First 1
    if (-not $exe) { throw "zip içinde audiocpp_cli.exe yok" }
    $got = Sha256 $exe.FullName
    if ($got -ne $exeSha) { Remove-Item -Recurse -Force $hazirTmp; throw "exe sha256 tutmadı: $got" }
    $script:acikExe = $exe.FullName
}
function ExeYerlestir {
    $bin = Split-Path $motorExe
    New-Item -ItemType Directory -Force $bin | Out-Null
    Get-ChildItem (Split-Path $script:acikExe) | ForEach-Object { Copy-Item -LiteralPath $_.FullName (Join-Path $bin $_.Name) -Force }   # exe + LICENSE + THIRD_PARTY.md + README.txt
    Remove-Item -Recurse -Force $hazirTmp
    Write-Output "  açıldı, exe sha256 doğru: $motorExe"
}
function ExeDogru([string]$exeSha) { (Test-Path -LiteralPath $motorExe) -and ((Sha256 $motorExe) -eq $exeSha) }
function VenvPython([string[]]$argv) {
    # Repo .venv Python'u ile ses_tasarim komutu; satırları dizi olarak döner, çalışmazsa $null / runs a ses_tasarim command in the repo venv
    $vpy = Join-Path $Repo ".venv\Scripts\python.exe"
    if (-not (Test-Path $vpy)) { return $null }
    $eap = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    try { Push-Location $Repo; $c = @(& $vpy @argv 2>$null) } finally { Pop-Location; $ErrorActionPreference = $eap }
    if ($LASTEXITCODE -ne 0 -or $c.Count -eq 0) { return $null }
    return ,$c   # tek satır da dizi kalsın / keep a one-line result an array
}

if ($Adim -contains "hazir") {
    Write-Output ("== hazır motor $REL_SURUM (GitHub Release" + $(if ($Vulkan) { ", Vulkan, DENEYSEL)" } else { ")" }))
    if (-not $Vulkan) {
        if ($REL_ZIP_SHA -like "__*") { throw "bu kur.ps1 sürümünde hazır motor sha256'sı yok; depoyu güncelleyin (git pull)" }
        ZipAl $REL_ZIP $REL_ZIP_SHA $REL_URL $HazirZip
        if (ExeDogru $REL_EXE_SHA) { Write-Output "  exe var ve doğru: $motorExe" } else { ZipAc $script:zipYol $REL_EXE_SHA; ExeYerlestir }
    } else {
        # Paket seçimi / package choice: -Islemci elle > yerel zip'in kendisi (sha256) > işlemci denetimi (denetlenemezse uyumlu)
        $paket = $Islemci
        if ($paket -eq "oto" -and $HazirZip) {
            if (-not (Test-Path -LiteralPath $HazirZip)) { throw "yerel zip yok: $HazirZip" }
            $got = Sha256 (Resolve-Path -LiteralPath $HazirZip).Path
            $paket = @($REL_VK.Keys | Where-Object { $REL_VK[$_].zip_sha -eq $got })[0]
            if (-not $paket) { throw "yerel zip $REL_VK_SURUM Vulkan paketlerinden biri değil (sha256 $got)" }
            Write-Output "  yerel zip paketi: $paket"
        } elseif ($paket -eq "oto") {
            $karar = VenvPython @("-m", "ses_tasarim.islemci")
            if ($karar -and @("avx2", "uyumlu") -contains $karar[0]) {
                $paket = $karar[0]; Write-Output "  işlemci denetimi: $paket ($($karar[1..9] -join ' '))"
            } else {
                $paket = "uyumlu"; Write-Warning "işlemci denetlenemedi (.venv yok ya da numpy açılmadı; adım: python): uyumlu paket seçildi. Hızlı paket için: -Adim python,hazir"
            }
        } else { Write-Output "  paket elle seçildi: $paket (-Islemci)" }
        # Kendiliğinden seçilen AVX2 paketi yerleştirilmeden önce geçici klasörde bir kez çalıştırılır; "ok" dışındaki her
        # sonuç (geçersiz komut 0xC000001D, başka hata, zaman aşımı, deneme yapılamadı) uyumlu pakete geçirir.
        # An automatically chosen AVX2 package runs once from the temp folder before it is installed; anything but "ok" -> compatible.
        $dene = ($paket -eq "avx2" -and $Islemci -eq "oto")
        $p = $REL_VK[$paket]
        ZipAl $p.zip $p.zip_sha $p.url $HazirZip
        if (ExeDogru $p.exe_sha) { Write-Output "  exe var ve doğru: $motorExe" }   # AVX2 exe yalnız denemeyi geçince yerleşir
        else {
            ZipAc $script:zipYol $p.exe_sha
            $sonuc = "ok"
            if ($dene) {
                $r = VenvPython @("-m", "ses_tasarim.islemci", "--dene", $script:acikExe)
                $sonuc = $(if ($r) { $r[0] } else { "yapilamadi" })
                Write-Output "  AVX2 exe deneme çalışması: $sonuc"
            }
            if ($sonuc -eq "ok") { ExeYerlestir }
            else {
                Remove-Item -Recurse -Force $hazirTmp
                if ($HazirZip) { throw "AVX2 paketi bu bilgisayarda denemeyi geçmedi ($sonuc); kurulu motora dokunulmadı. Uyumlu zip'i ($($REL_VK.uyumlu.zip)) -HazirZip ile verin ya da -HazirZip olmadan yeniden çalıştırın" }
                Write-Warning "AVX2 paketi denemeyi geçmedi ($sonuc): uyumlu pakete geçiliyor"
                $paket = "uyumlu"; $p = $REL_VK[$paket]
                ZipAl $p.zip $p.zip_sha $p.url ""
                if (ExeDogru $p.exe_sha) { Write-Output "  exe var ve doğru: $motorExe" } else { ZipAc $script:zipYol $p.exe_sha; ExeYerlestir }
            }
        }
        Write-Output "VULKAN_PAKET: $paket"
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
    YamalariUygula $src $PATCHES
    Write-Output "KAYNAK_OK"
}

if ($Adim -contains "derle") {
    Write-Output "== derleme (~15-25 dk, $Paralel iş, mimari $Mimari)"
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo "scripts\derle.ps1") `
        -Kaynak (Join-Path $Kok "motor\src") -Build (Join-Path $Kok "motor\build") -Cuda $cudaRoot -Mimari $Mimari -Paralel $Paralel
    if ($LASTEXITCODE -ne 0) { throw "derleme başarısız" }
    Write-Output "DERLE_OK"
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
            $j = $(if (Test-Path $hedef) { Get-Content -Raw -Encoding UTF8 $hedef | ConvertFrom-Json } else { $null })
            if ($j -and $j.backend -eq "vulkan") {
                if ($j.PSObject.Properties["cihaz"]) { $j.cihaz = $no } else { $j | Add-Member -NotePropertyName cihaz -NotePropertyValue $no }
                [IO.File]::WriteAllText($hedef, (($j | ConvertTo-Json) + "`n"), (New-Object Text.UTF8Encoding $false))
                Write-Output "  seçilen Vulkan cihazı: $no ($sec) → ayarlar.json cihaz"
            } elseif ($j) {
                # CUDA ayarına Vulkan cihaz numarası yazılmaz (CUDA'da numara başka karta düşer) / never write a Vulkan index into CUDA settings
                Write-Output "  ayarlar.json Vulkan değil (backend $($j.backend)); cihaz yazılmadı. Vulkan için: -Adim ayar,kontrol -Vulkan (Vulkan cihazı: $no)"
            }
        }
    }
    Write-Output "KONTROL_OK"
}
Write-Output "KURULUM_OK"
Write-Output "Arayüz / web UI:  .venv\Scripts\python.exe -m ses_tasarim.arayuz   (sonra tarayıcıda http://127.0.0.1:8765/ )"

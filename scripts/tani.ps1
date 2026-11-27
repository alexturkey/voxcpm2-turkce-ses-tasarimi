# Yerel teshis raporu / local diagnostic report (kit KL-14). Hicbir sey gondermez, ag kullanmaz, dosya yazmaz; yalniz ekrana basar.
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tani.ps1               tam rapor (issue formuna yapistirin)
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tani.ps1 -KartSatiri   tek satir: kart, surucu, VRAM, RAM, Windows
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\tani.ps1 -Hata "<hata metni>"   hata iletisinin bir parcasindan kodu ve ilk adimi bulur (docs/hata_imzalari.json)
# Kisisel ad ve yol sizmaz: kullanici adi, bilgisayar adi ve profil yolu <USER>, <PC> ile degistirilir; ayarlar.json'daki yollar yalniz "var/yok" olarak yazilir.
# This script sends nothing and writes nothing. User name, computer name and profile path are replaced before printing.
# Rapor SAPMA bolumu da icerir (PATH'te ilk python, degismis izlenen dosyalar, SES_* ezmeleri, ayarlar.json farki, model kopyasi): salt okur.
# Cikis / exit: 0 rapor basildi, 3 beklenmedik hata.
param([switch]$KartSatiri, [string]$Hata = "")
$ErrorActionPreference = "Continue"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$gizle = @()
if ($env:USERPROFILE) { $gizle += @{ a = $env:USERPROFILE; b = "<PROFILE>" } }
if ($env:USERNAME) { $gizle += @{ a = $env:USERNAME; b = "<USER>" } }
if ($env:COMPUTERNAME) { $gizle += @{ a = $env:COMPUTERNAME; b = "<PC>" } }
function Temiz([string]$s) {
    foreach ($g in $gizle) { if ($g.a.Length -ge 2) { $s = $s -replace [regex]::Escape($g.a), $g.b } }
    return $s
}
function Yaz([string]$s) { Write-Output (Temiz $s) }
function Calistir([string]$cmd, [string[]]$arg) {
    $c = Get-Command $cmd -ErrorAction SilentlyContinue
    if (-not $c) { return $null }
    try { return (& $cmd @arg 2>$null | Select-Object -First 1) } catch { return $null }
}
if ($Hata) {
    try { [Console]::OutputEncoding = New-Object Text.UTF8Encoding $false } catch {}
    $imzaDosyasi = Join-Path (Join-Path $repo "docs") "hata_imzalari.json"
    try { $liste = (Get-Content -Raw -Encoding UTF8 $imzaDosyasi | ConvertFrom-Json).hatalar } catch { Write-Output "hata_imzalari.json okunamadi"; exit 3 }
    $bulunan = @($liste | Where-Object { $Hata.IndexOf($_.imza, [StringComparison]::OrdinalIgnoreCase) -ge 0 })
    foreach ($b in $bulunan) { Yaz ("{0}  ({1})`n  TR: {2}`n  EN: {3}" -f $b.kod, $b.imza, $b.ilk_adim_tr, $b.ilk_adim_en) }
    if ($bulunan.Count -eq 0) { Write-Output "Bu iletiyle eslesen kayitli hata yok / no known error matches. Tam raporu alin: tani.ps1 (parametresiz) ve issue formuna yapistirin."; exit 1 }
    exit 0
}
try {
    $smi = Calistir "nvidia-smi" @("--query-gpu=name,driver_version,memory.total", "--format=csv,noheader")
    $os = $null; $ram = $null
    try { $os = (Get-CimInstance Win32_OperatingSystem).Caption + " " + (Get-CimInstance Win32_OperatingSystem).Version } catch {}
    try { $ram = "{0:N1} GB" -f ((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB) } catch {}
    $kart = $(if ($smi) { "$smi" } else { "NVIDIA karti gorunmuyor (nvidia-smi yok ya da calismadi)" })
    if ($KartSatiri) { Yaz ("Kart: $kart | RAM: $ram | OS: $os"); exit 0 }
    Yaz "== voxcpm2-turkce-ses-tasarimi teshis raporu (yerel; hicbir sey gonderilmez)"
    Yaz "tarih: $(Get-Date -Format 'yyyy-MM-dd HH:mm')   PowerShell: $($PSVersionTable.PSVersion)"
    Yaz "OS: $os    RAM: $ram"
    Yaz "ekran karti: $kart"
    # Python (kur.ps1 ile ayni aday sirasi; ilk 3.10-3.13 64-bit olan gecerlidir)
    foreach ($aday in @(@("py", "-3.12"), @("py", "-3.13"), @("py", "-3.11"), @("py", "-3.10"), @("py", "-3"), @("python"))) {
        $on = @(); if ($aday.Count -gt 1) { $on = @($aday[1..($aday.Count - 1)]) }
        $v = Calistir $aday[0] ($on + @("-c", "import sys,struct;print('%d.%d %d-bit' % (sys.version_info[0], sys.version_info[1], struct.calcsize('P')*8))"))
        if ($v) { Yaz ("python (" + ($aday -join " ") + "): $v") }
    }
    $venvPy = Join-Path $repo ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venvPy) { Yaz ("repo .venv: var, " + (Calistir $venvPy @("-c", "import sys;print('%d.%d' % sys.version_info[:2])"))) } else { Yaz "repo .venv: yok" }
    # repo yolu
    if ($repo -match '[^\x00-\x7F]') { Yaz "UYARI: repo yolu ASCII degil; motor bu yolu acamayabilir (C:\vox\repo gibi bir yere tasiyin)" } else { Yaz "repo yolu: ASCII (iyi), uzunluk $($repo.Length)" }
    # ayarlar.json: yollar yazilmaz, yalniz var/yok
    $ay = Join-Path $repo "ayarlar.json"
    if (Test-Path -LiteralPath $ay) {
        try {
            $j = Get-Content -Raw -Encoding UTF8 $ay | ConvertFrom-Json
            Yaz "ayarlar.json: var, backend=$($j.backend), cihaz=$($j.cihaz), port=$($j.port)"
            foreach ($k in @("motor", "model", "cuda_bin")) {
                $d = $j.$k
                if ($d) { $var = Test-Path -LiteralPath $d; $bos = ""
                    if ($var -and $k -eq "model") { $bos = ", {0:N2} GB" -f ((Get-Item -LiteralPath $d).Length / 1GB) }
                    Yaz ("  ${k}: " + $(if ($var) { "var" } else { "YOK" }) + $bos) }
            }
            if ($j.motor) {
                $drv = [IO.Path]::GetPathRoot($j.motor)
                try { Yaz ("  kurulum diski bos alan: {0:N1} GB" -f ((New-Object IO.DriveInfo $drv).AvailableFreeSpace / 1GB)) } catch {}
            }
            $port = [int]$j.port
            if ($port -gt 0) {
                $dinleyen = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
                Yaz ("  port ${port}: " + $(if ($dinleyen) { "dinleniyor (arayuz acik ya da baska program)" } else { "bos" }))
            }
        } catch { Yaz "ayarlar.json: okunamadi ($($_.Exception.GetType().Name))" }
    } else { Yaz "ayarlar.json: yok (scripts\kur.ps1 yazar)" }
    $imza = Join-Path $repo "scripts\kur.ps1"
    if (Test-Path -LiteralPath $imza) { Yaz ("kur.ps1 sha256: " + (Get-FileHash -Algorithm SHA256 -LiteralPath $imza).Hash.Substring(0, 12)) }
    $git = Calistir "git" @("-C", $repo, "log", "-1", "--format=%h %s")
    if ($git) { Yaz "repo son commit: $git" }
    # SAPMA / DEVIATIONS (salt okur): varsayilandan farkli ne var? Kalite sabiti kodda (16 adim, cfg 2.0); burada ortam, yerel degisiklik ve ayar farki gorulur.
    Yaz "SAPMA / DEVIATIONS (salt okur):"
    try {
        $pc = @(Get-Command python -All -ErrorAction SilentlyContinue | Select-Object -First 3)
        if ($pc.Count -gt 0) {
            if ($pc[0].Source -match 'WindowsApps') { Yaz "  PATH'te ilk python: Microsoft Store kisayolu (gercek Python degil; py -3.12 ya da kur.ps1 kullanin)" }
            else { Yaz ("  PATH'te ilk python: " + (Calistir $pc[0].Source @("--version"))) }
        } else { Yaz "  PATH'te python yok (py baslaticisi ya da .venv kullanilir)" }
    } catch { Yaz "  python sirasi okunamadi" }
    try {
        $gitK = Get-Command git -ErrorAction SilentlyContinue
        if ($gitK -and (Test-Path -LiteralPath (Join-Path $repo ".git"))) {
            $gs = @(& $gitK.Source --no-optional-locks -C $repo status --short -uno 2>$null | ForEach-Object { "$_".Trim() } | Where-Object { $_ } | Select-Object -First 40)
            if ($gs.Count -eq 0) { Yaz "  git: izlenen dosyalar degismemis" } else { Yaz "  git: $($gs.Count) izlenen dosya degismis (yalniz adlar):"; foreach ($g in $gs) { Yaz "    $g" } }
        } else { Yaz "  git: kopya degil ya da git yok" }
    } catch { Yaz "  git durumu okunamadi" }
    $sesEnv = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'SES_*' } | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Value)" })
    if ($sesEnv.Count) { Yaz ("  SES_* ortam ezmeleri: " + ($sesEnv -join " ")) } else { Yaz "  SES_* ortam ezmesi: yok" }
    try {
        $ornek = Get-Content -Raw -Encoding UTF8 (Join-Path $repo "ayarlar.example.json") | ConvertFrom-Json
        $gercek = Get-Content -Raw -Encoding UTF8 (Join-Path $repo "ayarlar.json") | ConvertFrom-Json
        $farkli = @()
        foreach ($k in @("backend", "cihaz", "audiovae_threads", "motor_threads", "port")) { if ("$($ornek.$k)" -ne "$($gercek.$k)") { $farkli += "$k=$($gercek.$k) (ornek $($ornek.$k))" } }
        if ($farkli.Count) { Yaz ("  ayarlar.json ornekten farkli: " + ($farkli -join "; ")) } else { Yaz "  ayarlar.json: yol disindaki alanlar ornekle ayni" }
        $mdl = "$($gercek.model)"
        if ($mdl -and -not (Test-Path -LiteralPath $mdl)) {
            $ad = Split-Path -Leaf $mdl
            foreach ($hd in @($(if ($env:HF_HUB_CACHE) { $env:HF_HUB_CACHE }), $(if ($env:HF_HOME) { Join-Path $env:HF_HOME "hub" }), $(if ($env:USERPROFILE) { Join-Path $env:USERPROFILE ".cache\huggingface\hub" }))) {
                if ($hd -and (Test-Path -LiteralPath $hd -PathType Container)) {
                    $f = Get-ChildItem -LiteralPath $hd -Recurse -File -Filter $ad -ErrorAction SilentlyContinue | Select-Object -First 1
                    if ($f) { Yaz ("  model dosyasi YOK ama Hugging Face onbelleginde ayni adli bir kopya var: {0:N2} GB (sha256 okunmadi; kullanici onaylarsa kopyalanabilir)" -f ($f.Length / 1GB)); break }
                }
            }
        }
    } catch { Yaz "  ayarlar.json / ayarlar.example.json karsilastirilamadi (dosya yok olabilir)" }
    Yaz "-- bu raporu issue formuna yapistirabilirsiniz; kisisel ad ve yol gizlendi. Yine de gozden gecirin. / Review before pasting."
    exit 0
} catch {
    Write-Output ("tani beklenmedik hata: " + (Temiz $_.Exception.Message))
    exit 3
}

[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · **中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**在 4 GB 显卡上用 VoxCPM2 设计土耳其语声音。** 用英文描述一个声音，让模型生成出来，挑选你喜欢的版本，
然后用这个声音朗读任意土耳其语文本。项目包含一键安装脚本、一个经过补丁修改、能在 GTX 1050 Ti（4 GB）上运行的
[audio.cpp](https://github.com/0xShug0/audio.cpp) 引擎、一个轻量的本地网页界面，以及十四个现成的合成声音：
七个土耳其语声音，另有七位分别以英语、法语、德语、西班牙语、俄语、中文和日语为母语的旁白。

- 支持朗读 30 种语言；界面同样提供 30 种语言。
- 14 个内置声音：7 个土耳其语，英语、法语、德语、西班牙语、俄语、中文和日语各 1 个。
- 网页界面（v0.2.0）：每张版本卡片上有两个声音，即原始设计声音和你以后一直会听到的声音；带声音菜单的朗读
  列表；可以重命名、隐藏或删除声音；朗读的文本可以存为草稿。详见「使用」下的「网页界面」。

[如何塞进 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [AI 代理安装指南](AGENTS.md) · [负责任地使用](ETHICS.md)

> 内置声音均为合成声音，由文字描述设计而成。声音克隆功能只能用于你本人的声音，或已获得声音所有者明确许可的声音；
> 界面会要求你确认这一许可。禁止冒充他人、欺诈和欺骗。请将生成的内容标注为 AI 生成。详见 [ETHICS.md](ETHICS.md)。

## 30 种语言

我们用 8 种语言制作了同一部卡帕多奇亚纪录短片：土耳其语、英语、法语、德语、西班牙语、俄语、中文和日语。
每种语言都有自己的**母语旁白**，由 VoxCPM2 根据英文描述设计而成。全部内容都在一块 4 GB 的 GTX 1050 Ti 上
完全本地生成，质量设置固定不变（16 步，cfg 2.0）。这七位旁白都已随项目附带，并附有各自的描述（prompt）、
设计文本、种子和参考录音。

| 代码 | 语言 | 声音 | 试听 | 视频 |
|---|---|---|---|---|
| `tr` | 土耳其语 | `hazir/belgesel_hanim`（另有 6 个） | [示例](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | 英语 | `hazir/anlatici_en` | [示例](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113791986763440439) |
| `fr` | 法语 | `hazir/anlatici_fr` | [示例](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113790681575804962) |
| `de` | 德语 | `hazir/anlatici_de` | [示例](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113791351645262249) |
| `es` | 西班牙语 | `hazir/anlatici_es` | [示例](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113807365611122705) |
| `ru` | 俄语 | `hazir/anlatici_ru` | [示例](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113801574136848884) |
| `zh` | 中文（普通话） | `hazir/anlatici_zh` | [示例](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113802229606121794) |
| `ja` | 日语 | `hazir/anlatici_ja` | [示例](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [视频](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**为什么要逐句朗读。** VoxCPM2 一次生成太长的内容时（大约超过 30 秒）并不稳定：节奏会越来越快，音色也可能跑偏。
本项目用固定的参考录音和种子来承载声音，长文本按每行一句的方式朗读，因此从第一句到最后一句，音色和风格都保持一致。
土耳其语以外的语言不使用土耳其语读音词典。VoxCPM2 支持的全部 30 种语言都已测试并可正常使用；没有内置声音的语言请使用
`--dil <code>`。各语言的命令以及我们总结的经验：
[docs/cok_dilli.md](docs/cok_dilli.md)。覆盖整个设计流程的 Claude Code 技能：
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md)。

**144 个示例描述，可直接上手。** 8 种语言各有 18 个角色（纪录片旁白、新闻主播、广告配音、有声书、讲故事的奶奶、
播客主持人、老师、电影预告片、冥想引导、体育解说等，男女都有）。描述用英文写成，写明说话人的国籍和母语口音；
同时附带一段在生成声音时朗读的文本，使用该语言并与角色相匹配。选一个，试听各个版本，留下喜欢的那个：
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`，或者在网页界面中选择*示例描述*。
完整列表：[docs/ornek_tarifler.md](docs/ornek_tarifler.md)。

**用你自己的声音为视频配音。** [DubWorld](https://github.com/alexturkey/dubworld) 是我们的本地视频配音程序，
它会把本仓库安装为自己的 VoxCPM2 语音引擎。你在这里设计的声音，可以在那边通过
`ses.voxcpm2_ses = "<name>/<variant>"` 使用。

## 快速上手（Windows，3 步）

1. **下载**代码：[voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip)。
   适合你显卡的现成引擎包会在第 3 步由安装脚本自动下载：
   NVIDIA → [CUDA 包](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.0/voxcpm2-turkce-ses-tasarimi-motor-v0.3.0-win64-cuda12.8.zip)，
   AMD / Intel → [Vulkan 包，实验性](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan.zip)
   （已经下载过？在下面的命令后加上 `-HazirZip <path to the zip>`）。
2. **解压** zip，打开 `voxcpm2-turkce-ses-tasarimi-main` 文件夹，在资源管理器地址栏输入 `powershell`
   并按回车。
3. **运行**安装脚本（需要 64 位 Python 3.10-3.13；使用 CUDA 时 NVIDIA 驱动 ≥ 570），然后双击 **`baslat.bat`**：
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel：在末尾加上 `-Vulkan`。界面地址为 http://127.0.0.1:8765/。

引擎 zip 不是独立应用（其中的 exe 需要安装脚本配置好的模型和 DLL）。详细说明、GPU
列表和常见问题：见下文「快速安装」。

## Ubuntu / Linux（NVIDIA CUDA，实验性）

用 `bash scripts/kur-linux.sh` 构建打过补丁的引擎，或者用 `Dockerfile.linux` 在
Ubuntu 24.04 / CUDA 12.8.1 环境中构建并运行。需要 NVIDIA GPU 和兼容的驱动；原生安装还
需要 CUDA toolkit 和 Python 3.10-3.13。界面只监听本机回环地址，在远程服务器上也是如此（通过 SSH 端口转发访问）。
前置条件、命令、架构选择和验证范围：[docs/linux.md](docs/linux.md)。

## 快速上手（macOS，Apple Silicon）

需要 Xcode Command Line Tools（`xcode-select --install`）和 [Homebrew](https://brew.sh)：
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
安装脚本会下载模型，用 Metal 构建打过补丁的引擎（约 1 分钟），并把所有内容安装到 `~/vox` 下。
然后双击 **`baslat.command`**。在 MacBook Air M4 16 GB 上：每 1 秒语音约需 2 秒计算，相同种子生成
逐字节相同的音频，内存峰值约 5.3 GB，连续朗读 12 分钟也没有因发热而降速。详细说明和
测量数据：[docs/mac.md](docs/mac.md)。

**原生 Mac 应用（无需 Python、Homebrew 或终端）：**[macos/README.md](macos/README.md)。它内置同样的
打过补丁的引擎，首次启动时下载模型；目前需要用 Xcode 从源码构建。

## 致 Mac（Apple Silicon）用户

另外还有一个由社区独立制作的 Apple Silicon Mac 适配版本，使用 Apple 的 MLX 框架运行 VoxCPM2：
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**。
它由 Emre Koç（[@emre-koc](https://github.com/emre-koc)）在他自己的仓库中开发和维护，不在本仓库；
安装步骤和支持问题请到那里提出。感谢 Emre 把这个项目带到了 Mac 上！

## 工作原理

1. **声音设计。** 一段英文*声音描述* + 一段*生成声音时朗读的文本*（使用该声音的语言）+ 若干个
   版本。每个版本有自己的种子；引擎接收 `(description)text`，并为每个种子返回一段设计录音。
   这段文本只是用来认识声音的简短示例：1-3 句，最长约 30 秒（界面会显示预估时长，超过 33 秒不会开始）；
   长文本应放到第 2 步。
2. **基于参考的朗读。** 设计录音会同时送入引擎的**两个**输入（`audio` 和 `voice_ref`），
   连同它的文字稿（`reference_text`）和要朗读的新文本，并使用同一个种子。声音由录音而不是描述来承载，
   所以换了文本也不会跑偏。文本逐句朗读。
3. 质量固定：16 个扩散步，CFG 2.0。种子不是质量旋钮。
4. **逐词时间，每次运行声音一致。** 朗读时由引擎自身给出每个词的起止位置（补丁 0002，无需额外模型）。时间写入 `kelimeler.json`，并裁剪各行，使行间静音等于停顿设置。相对 CTC 强制对齐（forced alignment，CTC = 100%）的准确率：89.66%（土耳其语，12 个声音；设置 `kelime_zamani`，默认开启）。借助补丁 0003，同一种子每次运行得到逐字节相同的音频。

原始设计录音只是这个声音的一次性样本，之后的任何朗读都不会与它完全一样。你在之后每次朗读中听到的都是第 2 步：
以设计录音为参考，再加上该版本自己的种子。所以网页界面会在设计完成后立即执行第 2 步，并把两者都显示在版本卡片上。

引擎是 audio.cpp v0.7.2 加上我们的补丁（`patches/`），模型是 VoxCPM2 Q8_0 GGUF。显存峰值 ≈ 2.8 GB；
在 GTX 1050 Ti 上每 1 秒语音约需 2 秒计算。详细说明和测量数据：[docs/4gb.md](docs/4gb.md)。

## 内置声音（`hazir_sesler/`）

全部十四个声音都是根据各自 `ses.json` 中保存的描述设计的，没有一个是从录音克隆的（克隆是单独的、
需要确认授权的*声音克隆*标签页）。

| 声音 | 简介 | 试听 |
|---|---|---|
| `belgesel_hanim` | 五十多岁的成熟女性，低沉温暖的女低音；沉稳的纪录片旁白 | [示例](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [参考录音](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | 低沉、有力、神秘的男声旁白 | [示例](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [参考录音](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | 七十岁左右的资深新闻主播，沉稳而有权威感 | [示例](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [参考录音](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | 三十多岁、富有魅力的晚间新闻女主播，声音丝滑、富有表现力 | [示例](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [参考录音](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | 童话女巫：低沉、略带鼻音、狡黠而甜腻 | [示例](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [参考录音](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | 极其低沉、浑厚、具有压迫感的男声旁白 | [示例](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [参考录音](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | 年迈的智者，低沉洪亮，略带神秘 | [示例](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [参考录音](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | 以英语为母语的五十多岁男性纪录片旁白（通用美式口音）；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | 以法语为母语的五十多岁男性纪录片旁白（巴黎口音）；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | 以德语为母语的五十多岁男性纪录片旁白（标准德语）；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | 以西班牙语为母语的五十多岁男性纪录片旁白（卡斯蒂利亚口音（马德里））；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | 以俄语为母语的五十多岁男性纪录片旁白（莫斯科口音）；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | 以中文（普通话）为母语的五十多岁男性纪录片旁白（北京普通话）；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | 以日语为母语的五十多岁男性纪录片旁白（东京标准语）；低沉、沉稳、温暖 | [示例](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [参考录音](hazir_sesler/anlatici_ja/referans.flac) |

每个文件夹包含：`referans.flac`（无损设计录音）、`ses.json`（描述、文字稿、设计种子、朗读种子、
简介；旁白声音还有 `dil` = 语言）、`ornek_okuma.mp3`（及其文本）。可以直接使用：`--ses hazir/<name>`。
旁白的参考录音都很短（5.6-10 秒）；它们的示例是卡帕多奇亚脚本的前三句，
截取自完整的成片朗读。

## 快速安装，无需编译器（Windows 10/11，NVIDIA GPU ≥ 4 GB）

前置条件：NVIDIA 驱动 ≥ 570 和 64 位 Python 3.10-3.13（`winget install Python.Python.3.12`）。仅此而已：
不需要 Visual Studio，也不需要 CUDA 安装程序。不确定自己是什么显卡？在 PowerShell 中运行 `nvidia-smi`：它会显示 GPU
名称、驱动版本和显存。没有 NVIDIA 显卡？请看下面的「AMD / Intel」。

使用 [Git](https://git-scm.com/download/win)：

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

不用 Git：在本页面点击 **Code → Download ZIP**，解压后打开解压出来的
`voxcpm2-turkce-ses-tasarimi-main` 文件夹，在资源管理器地址栏输入 `powershell` 并按回车，然后运行
上面的最后一行。只有从源码构建时才需要 Git。

`-ExecutionPolicy Bypass` 只对这一个进程生效，不会更改任何系统设置；和对待任何安装脚本一样，运行前请先阅读 `scripts\kur.ps1`。
一条命令，约 10 分钟，约 3.7 GB 下载，全部经过 sha256 校验：模型（2.95 GB）、以便携 zip 形式提供的 CUDA 12.8 运行时 DLL
（不做系统安装，不改动 PATH）、来自 Releases 页面的**预编译引擎**、装有两个 Python 包的 `.venv`、
`ayarlar.json`，以及最后的 GPU 检查（`KONTROL_OK`）。任何一步失败后重新运行即可，已校验的文件会被
跳过。然后启动网页界面：在仓库文件夹中双击 **`baslat.bat`**。它会启动界面，并在准备就绪后在浏览器中打开
**http://127.0.0.1:8765/**；关闭黑色窗口（或在其中按 Ctrl+C）即可停止。
在 PowerShell 中也可以这样做：

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
然后自己打开 **http://127.0.0.1:8765/**（以这种方式启动时，界面不会自动打开浏览器；它只监听
本机）。

> **release zip 中的 `audiocpp_cli.exe` 不是用来双击运行的。** 它是一个命令行引擎，
> 需要旁边放着 CUDA DLL 和模型；`kur.ps1` 会把一切准备好，再由 Python 包来调用它。
> 双击它只会显示 "cudart64_12.dll not found"。

**支持的 GPU（release v0.3.0）：** 为 GTX 10xx（sm_61）、RTX 20xx（sm_75）、RTX 30xx（sm_86）、RTX 40xx
（sm_89）和 RTX 50xx（sm_120a）提供原生代码；Pascal 及以后的其他 CUDA GPU 通过驱动运行内嵌的 PTX（首次启动
较慢）。Maxwell（GTX 9xx）及更早的显卡不受 CUDA 12.8 支持。我们在 GTX 1050 Ti 4 GB 上做过测试（也在 Windows 上通过 Docker Desktop/WSL2 测试过，仅 CLI）；@mslmyilmaz5 测量过（#15）：RTX 3060 Ti 8 GB、Ubuntu 24.04 Docker、
CUDA 12.8.1（详见 [docs/linux.md](docs/linux.md)）。欢迎在 [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) 中分享其他显卡的测试报告。

**AMD / Intel（实验性）：** 单独的 Vulkan 引擎（无需 CUDA）通过 `scripts\kur.ps1 -Kok C:\vox -Vulkan` 安装。我们在自己的 NVIDIA 显卡上用 Vulkan 后端测试过（比 CUDA 慢，同一种子得到相同音频；干净的速度对比尚待进行），也在 Intel HD Graphics 630 集成显卡上测试过（每 1 秒语音约需 35-50 秒计算）；我们自己**没有**在 AMD 上测试过：如果你试了，请把结果发到 Discussions。有多个 Vulkan 设备（集成 + 独立）时，安装程序会把独立显卡的编号以 `cihaz` 写入 `ayarlar.json`。

**社区测试（AMD）：** @mitraTR 在 Windows 11 的 AMD Radeon RX 6900 XT 上用 Vulkan 运行了 v0.1.1：安装、声音设计、朗读、网页界面和测试全部通过；朗读每 1 秒语音约需 0.8-0.9 秒计算时间（[#6 中的报告](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)）。请安装到路径只含 ASCII 字符的短文件夹（例如 `C:\vox`）：在 Windows 上，引擎无法打开含中文或其他非 ASCII 字符的路径。目前所有报告：[已测试的硬件](docs/donanim_testleri.md)。

**Vulkan 说明：** 自引擎 v0.3.1 起，Vulkan 上也能得到词级时间戳。共有两个包：`vulkan` 需要支持 AVX2 的处理器（2013 年以后的大多数 Intel Core，2015 年以后的 AMD；许多 Pentium/Celeron 不支持）；[`vulkan-uyumlu`](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan-uyumlu.zip) 可在任何 64 位 x86 处理器上运行，但某个声音的首次朗读约需 2.2 倍时间（之后的朗读速度相同）。`kur.ps1 -Vulkan` 会检查处理器并自动选择包。使用集成显卡时，引擎朗读期间约占用 8 GB 内存。Vulkan 首次启动要编译 GPU 着色器，可能需要几分钟；之后的朗读会更快。详情：[docs/vulkan.md](docs/vulkan.md)。

### 另一种方式：从源码构建引擎

需要 Visual Studio 2022 Build Tools，并勾选 "Desktop development with C++"（含 C++ CMake tools），约 7 GB。然后：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
该命令还会下载 nvcc，获取 audio.cpp v0.7.2 源码，应用 `patches/0001-voxcpm2-4gb-ve-hiz.patch`，并为你的 GPU 构建
（`-Mimari native`，默认值；也可以指定例如 `-Mimari 61`），约 15-25 分钟。根目录路径要短（`C:\vox`）：
nvcc 在长路径下会失败。带检查步骤的分步说明：[AGENTS.md](AGENTS.md)。

### 常见安装问题

| 你看到的 | 含义与解决办法 |
|---|---|
| 双击 exe 后出现 `cudart64_12.dll not found` | 引擎不是用来手动启动的。运行上面的 `kur.ps1` 命令，然后启动网页界面。 |
| `64-bit Python 3.10+ bulunamadı`（找不到 Python） | 安装 Python（`winget install Python.Python.3.12`），关闭 PowerShell，打开一个新窗口，再运行同一条命令。 |
| `motor ekran kartını görmedi`（引擎没有识别到 GPU） | 把 NVIDIA 驱动更新到 570 或更高版本；确认 `nvidia-smi` 可以运行。 |
| `indirme başarısız` / `sha256 tutmadı`（下载失败 / 校验和不匹配） | 通常是下载中断。再运行一次同一条命令；已校验的文件会被跳过。 |
| 源码构建：`nvcc` 失败 | 安装根目录路径要短（`-Kok C:\vox`）。 |
| 页面打不开 | 用 `baslat.bat` 启动界面，或自己打开 http://127.0.0.1:8765/。端口被占用？修改 `ayarlar.json` 中的 `"port"`。 |

遇到问题？请到 [Discussions（问答）](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) 提问，或提交
[安装问题 issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)，
并附上你的 GPU、Windows 版本、所用命令及其最后几行输出。

## 使用

命令行：
```powershell
# list voices
.venv\Scripts\python.exe -m ses_tasarim.oku --liste
# read with a bundled voice (one sentence per line; blank line or "|| paragraf" = longer pause, "|| 0,8" = 0.8 s)
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/belgesel_hanim --metin @metin.txt --cikti cikti\deneme
# design a new voice: 3 variants, 3 seeds
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt
# read with variant 2 of it
.venv\Scripts\python.exe -m ses_tasarim.oku --ses deniz_feneri/2 --metin @metin.txt --cikti cikti\deniz
# design, then read a text with each variant's lasting voice (dinleme.wav in each variant folder)
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad deniz_feneri --cesit 3 --tarif "A calm Turkish woman ..." --metin @tanitim.txt --dinleme @metin.txt
```
文本规则：数字要写成文字，不要使用引号（工具会拒绝数字和引号），每行一句，
每行 ≤ 2000 个字符。行后停顿：`|| bagli` 0.25 秒、`|| normal` 0.5 秒、`|| paragraf` 1 秒、`|| agir` 1.5 秒，
或自定义时长 `|| 0,8`（0-5 秒；标记中的数字是允许的）。`ayarlar/okunus_sozlugu.tsv` 用于修正土耳其语文本中外来词的读音。
语言根据文本自动识别（土耳其语字母、文字系统、常用词；不确定时使用声音卡片中的 `dil`；`--dil <code>` 可选）。对于非土耳其语文本，允许使用撇号，
不使用土耳其语词典，但数字仍会被拒绝。如果朗读时输出 `speed gate: satır [...]`，请试听这些行。

### 网页界面

仅限本机（127.0.0.1）：`.venv\Scripts\python.exe -m ses_tasarim.arayuz` → 自己打开 http://127.0.0.1:8765/
（换端口：`--port 8800`），或者双击 `baslat.bat`。按 Ctrl+C 停止服务器。共有三个标签页：*设计声音*、
*用此声音朗读*、*声音克隆*。常用流程：*开始设计* → 试听各个版本 → *加入我的朗读列表* →
*开始朗读* → 下载。也可以从声音菜单中挑一个内置声音直接朗读。

- **页眉中的版本号。** 一个小而淡的 `v0.3.1 · <short commit>`（当受跟踪的文件有未提交的修改时带 `+`；
  没有 git 时只显示版本号），这样截图和视频里就能看出用的是哪个版本。
- **每张版本卡片上的两个声音。** 上方灰色的是*原始设计声音*：它只生成一次，再也不会一模一样地出现。
  下方橙色框里的是 *↻ 这就是你以后一直听到的声音*：以设计录音为参考、用该版本自己的种子（显示在卡片上）重新朗读的结果。
  这就是该声音在之后每次朗读中的样子。下面是*开始朗读*和*加入我的朗读列表*。按一次*开始设计*就会完成这两件事：
  先设计每个版本，再用每个版本的固定声音朗读你的文本；一个进度条统计两个阶段。版本文件夹中
  会生成 `dinleme.wav`。如果这次朗读中途停止，设计结果会保留，卡片上会显示一条提示。
- **「想听的文本」窗口。** 在*设计声音*中，*↻ 想听的文本* 框里放的是每个固定声音要朗读的内容
  （留空则朗读示例句）。点击它会在窗口中打开朗读笔记本：行号、行菜单、停顿条。*确定*把文本及其停顿写回
  框中；*取消*或 Esc 不做任何更改。朗读标签页保留自己的文本。
- **朗读笔记本。** 每行一句。点击行号打开行菜单（上移或下移、移动到指定位置、复制、删除；Alt+↑/↓、
  Alt+Shift+↓，或拖动行号；Ctrl+Z 会同时撤销文本和停顿的修改）。点击两行之间的细条选择停顿
  （bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 秒，或用齿轮自定义 0-5 秒）；按两次 Enter 分段（1 秒），
  空行会变成停顿条。播放结果时，正在朗读的行会高亮并自动滚动到可见位置；行菜单中的 *▶ 从这里播放* 会从该行开始播放。
  文本及其停顿在页面刷新后仍会保留（浏览器存储）。
- **草稿。** 两个笔记本（朗读标签页和窗口）中都有 *📄 草稿* 按钮。可以把当前文本连同停顿保存为草稿，
  点击即可载入（Ctrl+Z 可撤销），用 ⋯ 覆盖、重命名或删除。草稿保存在 `sesler/taslaklar.json` 中，
  永远不会进入仓库。
- **朗读列表与声音菜单。** 在版本卡片上点击*加入我的朗读列表*会弹出名称框：给这个版本起一个
  自己的名字，按 ✓ 即可加入。*生成名称*会保留在这次生成的每个版本上。在*用此声音朗读*中，声音
  按钮（国旗 + 名称）会打开声音菜单：最上方是*我的朗读列表*，然后是带国旗的内置声音（界面
  语言优先）。每一行都有 ▶ 试听（有固定声音时播放固定声音）、心形（加入或移除）和 ⋯；↑/↓ 和
  Enter 选择，Esc 关闭，上次使用的声音会被记住。列表保存在 `sesler/okuma_listesi.json` 中，位于
  仓库之外，重启后依然保留。
- **管理声音。** ⋯ 菜单（声音菜单中的行或版本卡片）中有*开始朗读*、加入或移出
  列表、*重命名*（名称留空即恢复原名；*恢复原名*）、对设计的声音提供*删除*、对内置声音提供*隐藏*；
  两者都会先确认。删除的声音会移到 `sesler/_cop/`；隐藏永远不会改动仓库文件。
  声音菜单底部是*已隐藏和已删除的声音（N）*，其中有*恢复*。自定义名称和隐藏的声音保存在
  `sesler/yerel_katman.json` 中。重命名过的声音会以灰色显示其来源（*生成名称 · 第 N 个*）；⋯ → *转到生成结果*
  会打开它的设计。
- **快捷键与文件。** Ctrl+Enter（Mac 上为 ⌘+Enter）会在当前标签页启动*开始设计*或*开始朗读*。
  进度条显示*已用时间 / ~总时间*，预估值根据你这台机器上以往的任务学习得出。下载的文件以
  声音名称和时间命名（`Voice_Name_2026-11-02_0152.wav`）。

**声音克隆（你本人的声音或已获授权的声音）。** 在界面的*声音克隆*标签页中，提供你的录音（wav/mp3/flac/ogg，建议 5-30 秒的干净语音；短于 3 秒会被拒绝，超过 36 秒会被截断）、与之完全一致的文字稿，以及要朗读的文本。在你勾选「这是我的声音，或我已获得声音所有者的明确许可」之前，按钮一直处于禁用状态。录音只会发送到本地服务器（127.0.0.1），在一个临时文件夹中与其参考编码一起处理，任务结束时（包括失败时）该文件夹会被删除；不会通过网络发送任何内容。只保留合成的输出（界面：`sesler/_okumalar/<job>/`，CLI：`--cikti`）。输出为带有 "synthetic" 标记的 `klon_synthetic.wav`；分享时请标注为 AI 生成。CLI：`python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## 常见问题

**模型还是引擎？分别是什么？** VoxCPM2（OpenBMB）是*模型*：把文本转换成语音的 20 亿参数神经网络。
audio.cpp 是*引擎*：在你的 GPU 上运行模型的 C++/CUDA 程序（`audiocpp_cli.exe`）。我们的
补丁修改的是引擎而不是模型：它让 VoxCPM2 能装进 4 GB，并让相同的种子每次都生成相同的音频。
本仓库中的 Python 包只负责准备文本、调用引擎和收集文件。

**支持哪些 GPU？** 见上文「支持的 GPU」：GTX 10xx 及以上的 NVIDIA 显卡，显存 4 GB 或以上，驱动 ≥ 570。release 中
包含 sm_61/75/86/89/120a 的原生代码；其他 Pascal 或更新的显卡使用内嵌的 PTX（首次启动较慢）。AMD/Intel：实验性的 Vulkan zip，`kur.ps1 -Vulkan`；我们已在 Intel HD Graphics 630 集成显卡上测试过；@mitraTR 曾在 AMD RX 6900 XT 上运行旧版 v0.1.1，新的 v0.3.1 包尚未在 AMD 上试过（见上文「AMD / Intel」）。纯 CPU（在 `ayarlar.json` 中设置 `"backend": "cpu"`）可以运行，但
比 GTX 1050 Ti 慢约 6 倍（引擎实测，生成 48 秒语音用时 535 秒对 94 秒）；这不是受支持的使用方式。

**有多快？** 在 GTX 1050 Ti 4 GB（i7-7700HQ）上实测：一个设计版本（≈ 25 秒录音）用时 55 秒；朗读时每 1 秒语音约需 2 秒
计算（实时因子 1.9-2.8），此前每个声音需要一次性的约 50 秒参考编码（缓存在
磁盘上），每批次加载模型需 10-20 秒；显存峰值 2.6-2.9 GB。更新的显卡会更快；数据和测量方法：
[docs/4gb.md](docs/4gb.md)。

**能克隆声音吗？** 底层的 VoxCPM2 模型可以根据参考录音模仿声音，克隆功能
用的就是这一点。只能用于你本人的声音，或在声音主人明确许可的情况下使用；
界面会要求你确认这一许可。声音设计不需要任何录音：它从英文或中文的文字描述开始，
朗读已设计声音时使用的「参考」是模型自己合成的设计录音。禁止冒充他人、欺诈
和欺骗。详见 [ETHICS.md](ETHICS.md)。请将你发布的内容标注为 AI 生成。

**怎样写出好的声音描述？** 用英文写 1-3 句：年龄和性别、音色（低沉/明亮、温暖、
鼻音、沙哑）、语气和角色（沉稳的纪录片旁白、充满活力的主持人）、语速（缓慢、从容），以及
"clean studio recording, no background noise"。写成描述，而不是台词；不要用括号。生成 3-5 个
版本并试听：种子对声音的影响很大。生成声音时朗读的文本，用该声音的语言写 1-3 句自然的句子，带上
你想要的情绪（最多约 30 秒语音）。朗读时每行一句；长句要拆开，数字要写成文字。

## 参与贡献

不知道从哪里开始？下面这四个小 issue 很适合作为第一步：

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) 在你的 GPU 上试一试，报告显卡、驱动和耗时
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel：试用实验性的 Vulkan 版本
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) 为测试集添加一个句子
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) 分享一个你设计的声音，附上描述和种子

**测试你的显卡，写一份报告：** 不需要会编程，填写[硬件测试报告表单](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml)即可；我们已自行测试 Intel HD Graphics 630 集成显卡；目前还没有 Intel Arc 的报告，也还没有 AMD 上 v0.3.1 的报告。

共享测试集：[docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt)；品牌声音指南：
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md)；如何提交代码：[CONTRIBUTING.md](CONTRIBUTING.md)。
安装问题：[issue 表单](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)；问题和结果：[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)。
所有参与者都遵守[行为准则](CODE_OF_CONDUCT.md)：友善待人，反馈只针对工作本身。

## 贡献者

- [@alexturkey](https://github.com/alexturkey)：维护者；代码、内置声音、文档
- [@cayir21](https://github.com/cayir21)：macOS（Apple Silicon）Metal 支持，[#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis)：修复 CPU 后端多句朗读时的句末（EOS）问题，[#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5)：Ubuntu/Linux 实验性 CUDA 安装与 Docker 支持，[#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

这里也可以有你的名字：你的 GPU 测试结果、为测试集添加的一个句子、你设计的一个声音、一份清晰的错误
报告或一个 pull request，都算作贡献。感谢每一位试用并给我们反馈的人。

## 许可与致谢

代码和内置声音：Apache-2.0，Copyright 2026 Ali Haydar Ozturk。基于 VoxCPM2（OpenBMB，Apache-2.0）、
audio.cpp（ShugoAI LLC，Apache-2.0）以及 audio.cpp GGUF 转换构建。完整列表：[THIRD_PARTY.md](THIRD_PARTY.md)。
与 OpenBMB、ModelBest 或 audio.cpp 项目无隶属关系。

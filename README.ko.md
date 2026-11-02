[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · **한국어** · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**4 GB GPU에서 VoxCPM2로 터키어 목소리 디자인하기.** 원하는 목소리를 영어로 설명하면 모델이 그 목소리를 만들어 줍니다.
마음에 드는 후보를 고른 뒤, 그 목소리로 어떤 터키어 텍스트든 읽게 할 수 있습니다. 명령 한 줄로 끝나는 설치 스크립트,
GTX 1050 Ti(4 GB)에 맞게 패치한 [audio.cpp](https://github.com/0xShug0/audio.cpp) 엔진, 가벼운 로컬 웹 UI, 그리고 14개의
기본 제공 합성 목소리가 포함되어 있습니다. 터키어 목소리 7개와 영어, 프랑스어, 독일어, 스페인어, 러시아어, 중국어,
일본어 원어민 내레이터 7개입니다.

- 30개 언어로 읽을 수 있고, 인터페이스도 30개 언어를 지원합니다.
- 기본 제공 목소리 14개: 터키어 7개, 그리고 영어, 프랑스어, 독일어, 스페인어, 러시아어, 중국어, 일본어 각 1개.
- 웹 UI(v0.2.0): 모든 후보 카드에 두 가지 목소리, 즉 원본 디자인 목소리와 앞으로 계속 듣게 될 목소리가 있습니다. 목소리 메뉴가 있는
  읽기 목록, 목소리 이름 바꾸기·숨기기·삭제, 읽을 텍스트의 임시 저장도 지원합니다. 자세한 내용은 '사용법'의 '웹 UI'를 참고하세요.

[4 GB에 들어가는 원리](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [AI 에이전트용 설치 가이드](AGENTS.md) · [책임 있는 사용](ETHICS.md)

> 기본 제공 목소리는 모두 텍스트 설명으로 디자인한 합성 목소리입니다. 보이스 클로닝 기능은 본인 목소리이거나
> 목소리 주인의 명시적인 허락을 받은 목소리에만 사용하세요. UI에서 그 허락을 확인하도록 요청합니다. 사칭,
> 사기, 기만은 금지됩니다. 생성한 결과물에는 AI 생성물임을 표시하세요. 자세한 내용은 [ETHICS.md](ETHICS.md)를 참고하세요.

## 30개 언어

카파도키아 다큐멘터리 영상 한 편을 8개 언어로 만들었습니다. 터키어, 영어, 프랑스어, 독일어, 스페인어, 러시아어, 중국어,
일본어입니다. 언어마다 VoxCPM2로 영어 설명을 바탕으로 디자인한 **원어민 내레이터**가 따로 있습니다. 모든 작업은
4 GB GTX 1050 Ti 한 장에서 완전히 로컬로 생성했고, 품질 설정은 고정(16 스텝, cfg 2.0)했습니다. 일곱 명의
내레이터는 각각의 프롬프트, 디자인 텍스트, 시드, 참조 녹음과 함께 이 저장소에 포함되어 있습니다.

| 코드 | 언어 | 목소리 | 듣기 | 영상 |
|---|---|---|---|---|
| `tr` | 터키어 | `hazir/belgesel_hanim` (외 6개) | [샘플](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | 영어 | `hazir/anlatici_en` | [샘플](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113791986763440439) |
| `fr` | 프랑스어 | `hazir/anlatici_fr` | [샘플](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113790681575804962) |
| `de` | 독일어 | `hazir/anlatici_de` | [샘플](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113791351645262249) |
| `es` | 스페인어 | `hazir/anlatici_es` | [샘플](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113807365611122705) |
| `ru` | 러시아어 | `hazir/anlatici_ru` | [샘플](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113801574136848884) |
| `zh` | 중국어(표준 중국어) | `hazir/anlatici_zh` | [샘플](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113802229606121794) |
| `ja` | 일본어 | `hazir/anlatici_ja` | [샘플](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [영상](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**왜 한 문장씩 읽을까요.** VoxCPM2는 한 번에 긴 음성(대략 30초 이상)을 생성하면 안정적이지 않습니다. 리듬이
점점 빨라지고 목소리가 달라질 수 있습니다. 여기서는 고정된 참조 녹음과 시드가 목소리를 유지하고, 긴 텍스트는
한 줄에 한 문장씩 읽기 때문에 첫 문장부터 마지막 문장까지 음색과 스타일이 그대로 유지됩니다. 터키어가 아닌
언어에는 터키어 발음 사전이 적용되지 않습니다. VoxCPM2가 지원하는 30개 언어를 모두 테스트했고 모두 동작합니다. 기본 제공 목소리가
없는 언어에는 `--dil <code>`를 사용하세요. 언어별 명령과 저희가 얻은 교훈:
[docs/cok_dilli.md](docs/cok_dilli.md). 디자인 과정 전체를 다루는 Claude Code 스킬:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**바로 시작할 수 있는 예시 프롬프트 144개.** 8개 언어마다 18가지 역할(다큐멘터리 내레이터, 뉴스 앵커, 광고 성우, 오디오북,
옛이야기를 들려주는 할머니, 팟캐스트 진행자, 선생님, 영화 예고편, 명상 가이드, 스포츠 해설자 등, 남녀 모두)이 있습니다.
프롬프트는 영어로, 화자의 국적과 원어민 억양을 담고 있습니다. 목소리를 만들 때 읽는 텍스트도 함께 들어 있으며, 해당 언어로
역할에 맞게 작성되어 있습니다. 하나를 골라 후보들을 들어 보고 마음에 드는 것을 남기세요:
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, 또는 웹 UI에서 *예시 설명*을 선택하세요.
전체 목록: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**내 목소리로 영상 더빙하기.** [DubWorld](https://github.com/alexturkey/dubworld)는 저희가 만든 로컬 영상 더빙
프로그램으로, 이 저장소를 VoxCPM2 음성 엔진으로 설치합니다. 여기서 디자인한 목소리는 DubWorld에서
`ses.voxcpm2_ses = "<name>/<variant>"`로 사용할 수 있습니다.

## 빠른 시작 (Windows, 3단계)

1. 코드를 **다운로드**합니다: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   그래픽 카드에 맞는 미리 빌드된 엔진 패키지는 3단계에서 설치 스크립트가 받아 옵니다.
   NVIDIA → [CUDA 패키지](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [Vulkan 패키지, 실험적](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (이미 받아 두었다면 아래 명령에 `-HazirZip <path to the zip>`을 추가하세요).
2. zip의 **압축을 풀고** `voxcpm2-turkce-ses-tasarimi-main` 폴더를 연 다음, 파일 탐색기 주소 표시줄에 `powershell`을
   입력하고 Enter를 누릅니다.
3. 설치 스크립트를 **실행**한 뒤(64비트 Python 3.10-3.13 필요, CUDA는 NVIDIA 드라이버 ≥ 570), **`baslat.bat`** 파일을 더블클릭합니다.
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: 끝에 `-Vulkan`을 추가하세요. UI는 http://127.0.0.1:8765/ 에서 열립니다.

엔진 zip은 단독으로 실행되는 앱이 아닙니다(안의 exe는 설치 스크립트가 준비하는 모델과 DLL이 필요합니다). 자세한 내용, GPU
목록, 자주 발생하는 문제: 아래의 '빠른 설치'를 참고하세요.

## Ubuntu / Linux (NVIDIA CUDA, 실험적)

`bash scripts/kur-linux.sh`로 패치된 엔진을 빌드하거나, `Dockerfile.linux`를 사용해
Ubuntu 24.04 / CUDA 12.8.1 환경에서 빌드하고 실행합니다. NVIDIA GPU와 호환 드라이버가 필요하며, 네이티브 설치에는
CUDA toolkit과 Python 3.10-3.13도 필요합니다. UI는 원격 서버에서도 루프백(로컬) 전용으로 유지됩니다(SSH 포워딩 사용).
사전 요구 사항, 명령, 아키텍처 선택, 검증 범위: [docs/linux.md](docs/linux.md).

## 빠른 시작 (macOS, Apple Silicon)

Xcode Command Line Tools(`xcode-select --install`)와 [Homebrew](https://brew.sh)가 필요합니다.
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
설치 스크립트가 모델을 받고, 패치된 엔진을 Metal로 빌드한 뒤(약 1분), 모든 것을 `~/vox` 아래에 설정합니다.
그런 다음 **`baslat.command`** 파일을 더블클릭하세요. MacBook Air M4 16 GB 기준: 음성 1초당 약 2초의 연산, 같은 시드는
바이트 단위까지 동일한 오디오, RAM 최대 약 5.3 GB, 12분 동안 연속으로 읽어도 발열로 인한 속도 저하 없음. 자세한 내용과
측정값: [docs/mac.md](docs/mac.md).

**네이티브 Mac 앱(Python, Homebrew, 터미널 불필요):** [macos/README.md](macos/README.md). 같은 패치된 엔진을
포함하고 처음 실행할 때 모델을 내려받습니다. 지금은 Xcode로 소스에서 빌드해야 합니다.

## Mac(Apple Silicon) 사용자를 위해

Apple의 MLX 프레임워크로 VoxCPM2를 실행하는, 커뮤니티가 독립적으로 만든 Apple Silicon Mac용 버전도 있습니다:
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
이 버전은 Emre Koç([@emre-koc](https://github.com/emre-koc))가 자신의 저장소에서 개발하고 관리하며, 이 저장소의 것이
아닙니다. 설치 방법과 지원 관련 질문은 그쪽으로 해 주세요. 이 프로젝트를 Mac으로 가져와 준 Emre에게 감사드립니다!

## 작동 방식

1. **목소리 디자인.** 영어로 쓴 *목소리 설명* + *목소리를 만들 때 읽는 텍스트*(그 목소리의 언어로) + 후보
   개수. 각 후보에는 고유한 시드가 주어지고, 엔진은 `(description)text`를 받아 시드마다 디자인 녹음을 하나씩
   돌려줍니다. 이 텍스트는 목소리를 알아보기 위한 짧은 샘플입니다. 1~2문장, 최대 약 20초(UI가
   예상 길이를 보여 주며 22초를 넘으면 시작하지 않습니다). 긴 텍스트는 2단계에서 다룹니다.
2. **참조 기반 읽기.** 디자인 녹음은 그 전사(`reference_text`), 새로 읽을 텍스트와 함께 같은 시드로
   엔진의 입력 **두 곳 모두**(`audio`와 `voice_ref`)에 전달됩니다. 목소리를 유지하는 것은 설명이 아니라 녹음이므로
   텍스트가 바뀌어도 목소리가 흔들리지 않습니다. 텍스트는 한 문장씩 읽습니다.
3. 품질은 고정입니다: 디퓨전 16 스텝, CFG 2.0. 시드는 품질 조절 장치가 아닙니다.

원본 디자인 녹음은 그 목소리의 일회성 샘플이라, 이후의 어떤 읽기도 이것과 똑같이 들리지는 않습니다. 이후 모든 읽기에서 듣게 되는
것은 2단계, 즉 디자인 녹음을 참조로 삼고 그 후보 고유의 시드로 읽은 결과입니다. 그래서 웹 UI는
디자인 직후에 2단계를 실행하고 두 결과를 모두 후보 카드에 보여 줍니다.

엔진은 audio.cpp v0.7.2에 저희 패치(`patches/`)를 적용한 것이고, 모델은 VoxCPM2 Q8_0 GGUF입니다. 최대 VRAM ≈ 2.8 GB,
GTX 1050 Ti에서 음성 1초당 약 2초의 연산이 필요합니다. 자세한 내용과 측정값: [docs/4gb.md](docs/4gb.md).

## 기본 제공 목소리 (`hazir_sesler/`)

14개 모두 각자의 `ses.json`에 저장된 프롬프트로 디자인했으며, 녹음에서 복제한 것은 하나도 없습니다(클로닝은
동의 확인을 거치는 별도의 *보이스 클로닝* 탭입니다).

| 목소리 | 간단한 설명 | 듣기 |
|---|---|---|
| `belgesel_hanim` | 50대의 원숙한 여성, 깊고 따뜻한 알토. 차분한 다큐멘터리 내레이터 | [샘플](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [참조](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | 깊고 힘 있고 신비로운 남성 내레이터 | [샘플](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [참조](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | 70세 전후의 노련한 뉴스 앵커, 차분하고 권위 있는 목소리 | [샘플](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [참조](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | 30대의 카리스마 있는 저녁 뉴스 여성 앵커, 벨벳처럼 부드럽고 표현력 있는 목소리 | [샘플](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [참조](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | 동화 속 마녀: 낮고, 살짝 콧소리가 섞인, 능청스럽게 달콤한 목소리 | [샘플](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [참조](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | 유난히 깊고 묵직하며 압도적인 남성 내레이터 | [샘플](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [참조](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | 나이 든 현자, 깊고 우렁차며 약간 신비로운 목소리 | [샘플](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [참조](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | 영어 원어민 50대 남성 다큐멘터리 내레이터(일반 미국 영어). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | 프랑스어 원어민 50대 남성 다큐멘터리 내레이터(파리). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | 독일어 원어민 50대 남성 다큐멘터리 내레이터(표준 독일어). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | 스페인어 원어민 50대 남성 다큐멘터리 내레이터(카스티야 스페인어(마드리드)). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | 러시아어 원어민 50대 남성 다큐멘터리 내레이터(모스크바). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | 중국어(표준 중국어) 원어민 50대 남성 다큐멘터리 내레이터(베이징 푸퉁화). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | 일본어 원어민 50대 남성 다큐멘터리 내레이터(도쿄 표준어). 깊고 차분하고 따뜻한 목소리 | [샘플](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [참조](hazir_sesler/anlatici_ja/referans.flac) |

각 폴더 구성: `referans.flac`(무손실 디자인 녹음), `ses.json`(프롬프트, 전사, 디자인 시드, 읽기 시드,
설명. 내레이터는 `dil` = 언어), `ornek_okuma.mp3`(와 그 텍스트). 바로 사용할 수 있습니다: `--ses hazir/<name>`.
내레이터의 참조 녹음은 짧으며(5.6-10초), 샘플은 카파도키아 대본의 첫 세 문장을
완성본 읽기에서 잘라 낸 것입니다.

## 빠른 설치, 컴파일러 불필요 (Windows 10/11, NVIDIA GPU ≥ 4 GB)

사전 요구 사항: NVIDIA 드라이버 ≥ 570과 64비트 Python 3.10-3.13(`winget install Python.Python.3.12`). 그 밖에는 필요 없습니다.
Visual Studio도, CUDA 설치 프로그램도 필요 없습니다. 내 그래픽 카드가 무엇인지 모르겠다면 PowerShell에서 `nvidia-smi`를 실행하세요. GPU
이름, 드라이버 버전, 메모리가 표시됩니다. NVIDIA 카드가 없다면 아래의 'AMD / Intel'을 참고하세요.

[Git](https://git-scm.com/download/win)을 사용하는 경우:

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Git 없이: 이 페이지에서 **Code → Download ZIP**을 클릭해 압축을 풀고, 압축을 푼
`voxcpm2-turkce-ses-tasarimi-main` 폴더를 연 다음, 파일 탐색기 주소 표시줄에 `powershell`을 입력하고 Enter를 누른 뒤
위의 마지막 줄을 실행합니다. Git은 소스에서 빌드할 때만 필요합니다.

`-ExecutionPolicy Bypass`는 이 프로세스 하나에만 적용되며 시스템 설정은 전혀 바꾸지 않습니다. 다른 설치 스크립트와 마찬가지로
실행하기 전에 `scripts\kur.ps1`을 읽어 보세요. 명령 하나, 약 10분, 약 3.7 GB 다운로드, 모든 파일 sha256 검증: 모델(2.95 GB),
포터블 zip 형태의 CUDA 12.8 런타임 DLL(시스템 설치 없음, PATH 변경 없음), Releases 페이지의 **미리 빌드된 엔진**, 두 개의
Python 패키지가 들어 있는 `.venv`, `ayarlar.json`, 그리고 마지막 GPU 점검(`KONTROL_OK`). 실패하면 다시 실행하세요. 검증된 파일은
건너뜁니다. 그다음 웹 UI를 시작합니다. 저장소 폴더에서 **`baslat.bat`** 파일을 더블클릭하면 UI가 시작되고, 준비되면
브라우저에서 **http://127.0.0.1:8765/** 이 열립니다. 종료하려면 검은 창을 닫거나 그 창에서 Ctrl+C를 누르세요.
PowerShell에서 같은 작업을 하려면:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
그다음 **http://127.0.0.1:8765/** 을 직접 여세요(이 방법으로 시작하면 UI가 브라우저를 열지 않으며, localhost에서만
접속을 받습니다).

> **릴리스 zip에 들어 있는 `audiocpp_cli.exe`는 더블클릭해서 쓰는 파일이 아닙니다.** 이것은 명령줄 엔진으로,
> 같은 위치에 CUDA DLL과 모델이 있어야 합니다. `kur.ps1`이 모든 것을 제자리에 두고, Python 패키지가 엔진을 구동합니다.
> 더블클릭하면 "cudart64_12.dll not found"만 표시됩니다.

**지원 GPU(릴리스 v0.1.1):** GTX 10xx(sm_61), RTX 20xx(sm_75), RTX 30xx(sm_86), RTX 40xx
(sm_89), RTX 50xx(sm_120a)용 네이티브 코드가 포함되어 있습니다. Pascal 이후의 다른 CUDA GPU는 드라이버를 통해 내장 PTX를 실행합니다(첫
시작이 느림). Maxwell(GTX 9xx) 이전 세대는 CUDA 12.8에서 지원되지 않습니다. 저희는 GTX 1050 Ti 4 GB에서 테스트했습니다(Windows에서 Docker Desktop/WSL2를 통해서도, CLI만). @mslmyilmaz5 님의 측정(#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1(자세한 내용은 [docs/linux.md](docs/linux.md)). 다른 카드에서의 결과 보고는 [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)에서 환영합니다.

**AMD / Intel(실험적):** CUDA가 없는 별도의 Vulkan 엔진 zip(`...-win64-vulkan.zip`)은
`scripts\kur.ps1 -Kok C:\vox -Vulkan`으로 설치합니다. 이 버전은 저희 NVIDIA 카드에서 Vulkan 백엔드로만 검증했습니다(그 환경에서
CUDA보다 느렸지만 같은 시드로 같은 오디오를 만들었습니다. 다만 이 측정은 디스크가 다른 작업으로 바쁠 때 한 것이라, 깨끗한 속도 비교는 아직 남아 있습니다).
AMD나 Intel 하드웨어에서는 저희가 직접 테스트하지 **않았습니다**. 사용해 보셨다면 결과를 Discussions에 올려 주세요. Vulkan 장치가 둘 이상이면(내장 + 외장)
설치 스크립트가 외장 GPU의 인덱스를 `cihaz`로 `ayarlar.json`에 기록합니다.

**참고:** Vulkan 지원은 현재 실험 단계입니다. GTX 1050 Ti에서 빌드와 테스트에 성공했습니다. 또한 외부 사용자(mitra_tr)가 AMD 6900 XT에서도 실행했다고 알려 왔습니다. AMD/Intel 카드에서는 더 폭넓은 테스트가 필요합니다.

### 대안: 소스에서 엔진 빌드하기

"Desktop development with C++"(C++ CMake tools 포함)가 설치된 Visual Studio 2022 Build Tools가 필요하며, 약 7 GB입니다. 그다음:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
이 명령은 nvcc도 내려받고, audio.cpp v0.7.2 소스를 가져와 `patches/0001-voxcpm2-4gb-ve-hiz.patch`를 적용한 뒤
사용 중인 GPU에 맞게 빌드합니다(`-Mimari native`가 기본값, 예를 들어 `-Mimari 61`도 가능). 약 15-25분이 걸립니다. 루트 경로는 짧게(`C:\vox`) 유지하세요.
nvcc는 긴 경로에서 실패합니다. 점검 단계가 포함된 단계별 안내: [AGENTS.md](AGENTS.md).

### 자주 발생하는 설치 문제

| 보이는 메시지 | 의미와 해결 방법 |
|---|---|
| exe를 더블클릭한 뒤 `cudart64_12.dll not found` | 엔진은 직접 실행하는 프로그램이 아닙니다. 위의 `kur.ps1` 명령을 실행한 뒤 웹 UI를 시작하세요. |
| `64-bit Python 3.10+ bulunamadı`(Python을 찾을 수 없음) | Python을 설치하고(`winget install Python.Python.3.12`), PowerShell을 닫은 뒤 새로 열어 같은 명령을 다시 실행하세요. |
| `motor ekran kartını görmedi`(엔진이 GPU를 인식하지 못함) | NVIDIA 드라이버를 570 이상으로 업데이트하고 `nvidia-smi`가 실행되는지 확인하세요. |
| `indirme başarısız` / `sha256 tutmadı`(다운로드 실패 / 체크섬 불일치) | 대개 다운로드가 중간에 끊긴 경우입니다. 같은 명령을 다시 실행하세요. 검증된 파일은 건너뜁니다. |
| 소스 빌드: `nvcc` 실패 | 설치 루트 경로를 짧게 유지하세요(`-Kok C:\vox`). |
| 페이지가 열리지 않음 | `baslat.bat`으로 UI를 시작하거나 http://127.0.0.1:8765/ 을 직접 여세요. 포트가 사용 중이라면 `ayarlar.json`의 `"port"`를 바꾸세요. |

문제가 있나요? [Discussions(Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)나
[설치 문제 issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)에
GPU, Windows 버전, 실행한 명령과 그 마지막 몇 줄을 함께 올려 주세요.

## 사용법

명령줄:
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
텍스트 규칙: 숫자는 글자로 쓰고 따옴표는 쓰지 않습니다(도구가 숫자와 따옴표를 거부합니다). 한 줄에 한 문장,
한 줄에 ≤ 2000자. 줄 뒤의 쉼: `|| bagli` 0.25초, `|| normal` 0.5초, `|| paragraf` 1초, `|| agir` 1.5초,
또는 원하는 길이 `|| 0,8`(0-5초, 이 표시 안의 숫자는 허용됩니다). `ayarlar/okunus_sozlugu.tsv`는 터키어 텍스트 속 외래어의 발음을 바로잡습니다.
언어는 텍스트에서 자동으로 감지합니다(터키어 글자, 문자 체계, 자주 쓰는 단어. 확실하지 않으면 목소리 카드의 `dil`. `--dil <code>`는 선택 사항). 터키어가 아닌 텍스트에서는 아포스트로피를 쓸 수 있고 터키어 사전은
적용되지 않지만, 숫자는 여전히 거부됩니다. 읽는 도중 `speed gate: satır [...]`가 출력되면 해당 줄을 들어 보세요.

### 웹 UI

로컬 전용(127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → http://127.0.0.1:8765/ 을 직접 엽니다
(다른 포트: `--port 8800`). 또는 `baslat.bat`을 더블클릭합니다. 서버는 Ctrl+C로 종료합니다. 탭은 세 개입니다: *목소리 디자인*,
*이 목소리로 읽기*, *보이스 클로닝*. 일반적인 흐름: *디자인하기* → 후보 듣기 → *내 읽기 목록에 추가* →
*이 목소리로 읽기* → 다운로드. 또는 목소리 메뉴에서 기본 제공 목소리를 골라 바로 읽을 수도 있습니다.

- **헤더의 버전 표시.** 작고 흐린 `v0.2.0 · <short commit>`(추적 중인 파일에 커밋하지 않은 변경이 있으면 `+`가 붙고,
  git이 없으면 버전만 표시). 스크린샷과 영상에서 어떤 버전을 썼는지 알 수 있습니다.
- **모든 후보 카드에 두 가지 목소리.** 위쪽 회색은 *원본 디자인 목소리*입니다. 한 번만 생성되며 똑같이 다시 나오지
  않습니다. 그 아래 주황색 테두리 안은 *↻ 앞으로 계속 듣게 될 목소리*입니다. 디자인 녹음을 참조로 삼아 그 후보 고유의 시드(카드에 표시)로
  다시 읽은 결과로, 이후 모든 읽기에서 이 목소리가 들립니다. 그 아래에 *이 목소리로 읽기*와 *내 읽기 목록에 추가*가 있습니다.
  *디자인하기*를 한 번 누르면 두 가지를 모두 합니다. 모든 후보를 디자인한 다음, 각 후보의 고정 목소리로 텍스트를 읽습니다. 진행 표시줄 하나가 두 단계를 모두 셉니다.
  후보 폴더에는 `dinleme.wav`가 생깁니다. 이 읽기가 중간에 멈춰도 디자인은 유지되고 카드에 안내가 표시됩니다.
- **'듣고 싶은 텍스트' 창.** *목소리 디자인*의 *↻ 듣고 싶은 텍스트* 칸에는 각 고정 목소리가 읽을 내용을 넣습니다
  (비워 두면 예시 문장을 읽습니다). 칸을 클릭하면 읽기 노트가 창으로 열립니다: 줄 번호,
  줄 메뉴, 쉼 띠. *확인*은 텍스트와 쉼을 칸에 다시 써 넣고, *취소*나 Esc는 아무것도 바꾸지 않습니다.
  읽기 탭은 자체 텍스트를 따로 유지합니다.
- **읽기 노트.** 한 줄에 한 문장. 줄 번호를 클릭하면 줄 메뉴가 열립니다(위아래로 이동, 원하는 위치로 이동,
  복제, 삭제. Alt+↑/↓, Alt+Shift+↓, 또는 번호를 끌어서 이동. Ctrl+Z는 텍스트와 쉼을 함께 되돌립니다).
  두 줄 사이의 얇은 띠를 클릭해 쉼을 고릅니다(bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5초, 또는 톱니바퀴로
  0-5초 사이의 원하는 길이). Enter를 두 번 누르면 문단(1초)이 되고, 빈 줄은 쉼 띠가 됩니다. 결과를
  재생하는 동안 읽고 있는 줄이 빛나며 화면 안으로 스크롤됩니다. 줄 메뉴의 *▶ 여기서부터 듣기*로 그 줄부터 재생합니다.
  텍스트와 쉼은 페이지를 새로 고쳐도 유지됩니다(브라우저 저장소).
- **임시 저장.** *📄 임시 저장* 버튼은 두 노트(읽기 탭과 창) 모두에 있습니다. 현재 텍스트를 쉼과 함께
  임시 저장하고, 클릭 한 번으로 불러오며(Ctrl+Z로 되돌릴 수 있음), ⋯로 덮어쓰기, 이름 바꾸기, 삭제를 합니다. 임시 저장 파일은
  `sesler/taslaklar.json`에 저장되며 저장소에는 절대 들어가지 않습니다.
- **읽기 목록과 목소리 메뉴.** 후보 카드에서 *내 읽기 목록에 추가*를 누르면 이름 입력 칸이 열립니다. 후보에
  고유한 이름을 붙이고 ✓를 누르면 추가됩니다. *생성 이름*은 그 실행의 모든 후보에 남아 있습니다. *이 목소리로 읽기*에서 목소리
  버튼(국기 + 이름)을 누르면 목소리 메뉴가 열립니다. 맨 위에 *내 읽기 목록*, 그 아래 국기가 붙은 기본 제공 목소리가 있습니다(인터페이스
  언어가 먼저). 각 줄에는 ▶ 듣기(고정 목소리가 있으면 그 목소리), 하트(추가 또는 제거), ⋯가 있습니다. ↑/↓와
  Enter로 고르고 Esc로 닫으며, 마지막으로 쓴 목소리를 기억합니다. 목록은 `sesler/okuma_listesi.json`에 저장되고,
  저장소 밖에 있으므로 다시 시작해도 남아 있습니다.
- **목소리 관리.** ⋯ 메뉴(목소리 메뉴의 줄 또는 후보 카드)에는 *이 목소리로 읽기*, 목록에 추가 또는 목록에서
  제거, *이름 바꾸기*(이름을 비우면 원래 이름이 복원됨. *원래 이름으로*), 디자인한 목소리용 *삭제*, 기본 제공 목소리용 *숨기기*가 있습니다.
  둘 다 먼저 확인을 받습니다. 삭제한 목소리는 `sesler/_cop/`으로 옮겨지며, 숨기기는 저장소 파일을 전혀 건드리지 않습니다.
  목소리 메뉴 맨 아래의 *숨긴 목소리와 삭제한 목소리 (N)* 항목에 *복원*이 있습니다. 사용자 지정 이름과 숨긴 목소리는
  `sesler/yerel_katman.json`에 저장됩니다. 이름을 바꾼 목소리는 원래 출처가 회색으로 표시됩니다(*생성 이름 · 후보 N*). ⋯ → *생성 결과로 이동*을
  누르면 그 디자인이 열립니다.
- **단축키와 파일.** Ctrl+Enter(Mac에서는 ⌘+Enter)는 열려 있는 탭에서 *디자인하기* 또는 *이 목소리로 읽기*를 시작합니다.
  진행 표시줄에는 *경과 시간 / ~전체 시간*이 표시되며, 예상치는 이 컴퓨터에서 했던 이전 작업으로부터 학습합니다. 다운로드 파일 이름은
  목소리 이름과 시각으로 정해집니다(`Voice_Name_2026-11-02_0152.wav`).

**보이스 클로닝(본인 목소리 또는 동의를 받은 목소리).** UI의 *보이스 클로닝* 탭에서 녹음(wav/mp3/flac/ogg, 깨끗한 음성 5-30초 권장. 3초 미만은 거부되고 36초를 넘는 부분은 잘립니다), 정확한 전사, 읽을 텍스트를 제공합니다. '이 목소리는 제 목소리이거나 목소리 주인의 명시적인 허락을 받았습니다'에 체크하기 전까지 버튼은 비활성 상태로 남습니다. 녹음은 로컬 서버(127.0.0.1)로만 전송되어 임시 폴더에서 참조 인코딩과 함께 처리되며, 작업이 끝나면(실패한 경우에도) 그 폴더는 삭제됩니다. 네트워크로는 아무것도 전송되지 않습니다. 합성된 결과만 남습니다(UI: `sesler/_okumalar/<job>/`, CLI: `--cikti`). 출력은 "synthetic" 태그가 붙은 `klon_synthetic.wav`입니다. 공유할 때는 AI 생성물임을 표시하세요. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## 자주 묻는 질문

**모델인가요, 엔진인가요? 각각 무엇인가요?** VoxCPM2(OpenBMB)는 *모델*로, 텍스트를 음성으로 바꾸는 20억 개 파라미터의 신경망입니다.
audio.cpp는 *엔진*으로, 여러분의 GPU에서 모델을 실행하는 C++/CUDA 프로그램(`audiocpp_cli.exe`)입니다. 저희
패치는 모델이 아니라 엔진을 바꿉니다. VoxCPM2가 4 GB에 들어가게 하고, 같은 시드가 매번 같은 오디오를 내도록 합니다.
이 저장소의 Python 패키지는 텍스트를 준비하고, 엔진을 호출하고, 파일을 모으는 일만 합니다.

**어떤 GPU에서 되나요?** 위의 '지원 GPU'를 참고하세요. GTX 10xx 이상의 NVIDIA, VRAM 4 GB 이상, 드라이버 ≥ 570. 릴리스에는
sm_61/75/86/89/120a용 네이티브 코드가 들어 있고, 그 밖의 Pascal 이후 카드는 내장 PTX를 사용합니다(첫 시작이 느림). AMD/Intel:
실험적인 Vulkan zip, `kur.ps1 -Vulkan`. 외부 사용자가 AMD 6900 XT에서 실행했다고 알려 왔지만, 더 폭넓은 AMD/Intel
테스트가 아직 필요합니다(위의 'AMD / Intel' 참고). CPU 전용(`ayarlar.json`에서 `"backend": "cpu"`)으로도 동작하지만
GTX 1050 Ti보다 약 6배 느리며(엔진 측정, 48초 음성에 535초 대 94초), 지원하는 방식이 아닙니다.

**얼마나 빠른가요?** GTX 1050 Ti 4 GB(i7-7700HQ)에서 측정: 디자인 후보 하나(≈ 25초 녹음)에 55초. 읽기는 음성 1초당 ≈ 2초의
연산(실시간 계수 1.9-2.8)이며, 목소리마다 한 번만 하는 약 50초의 참조 인코딩(디스크에
캐시됨)과 배치마다 10-20초의 모델 로딩이 추가됩니다. 최대 VRAM 2.6-2.9 GB. 최신 카드일수록 빠릅니다. 수치와 측정 방법:
[docs/4gb.md](docs/4gb.md).

**목소리를 복제할 수 있나요?** 기반이 되는 VoxCPM2 모델은 참조 녹음으로 목소리를 흉내 낼 수 있고, 클로닝
기능이 이를 사용합니다. 본인 목소리이거나 목소리 주인의 명시적인 허락이 있을 때만 사용하세요.
UI에서 그 허락을 확인하도록 요청합니다. 목소리 디자인에는 녹음이 필요 없습니다. 영어나 중국어로 된 텍스트 설명에서 시작하며,
디자인한 목소리로 읽을 때 쓰는 '참조'는 모델이 직접 합성한 디자인 녹음입니다. 사칭, 사기,
기만은 금지됩니다. [ETHICS.md](ETHICS.md)를 참고하세요. 공개하는 결과물에는 AI 생성물임을 표시하세요.

**좋은 목소리 설명은 어떻게 쓰나요?** 영어로 1~3문장: 나이와 성별, 음색(깊은/밝은, 따뜻한,
콧소리 섞인, 거친), 어조와 역할(차분한 다큐멘터리 내레이터, 활기찬 진행자), 속도(느린, 침착한), 그리고
"clean studio recording, no background noise". 대본이 아니라 설명으로 쓰고, 괄호는 쓰지 마세요. 후보는 3~5개를
요청해 들어 보세요. 시드에 따라 목소리가 크게 달라집니다. 목소리를 만들 때 읽는 텍스트는 그 목소리의 언어로 자연스러운 1~2문장을,
원하는 분위기로 쓰세요(음성으로 최대 약 20초). 읽을 때는 한 줄에 한 문장. 긴 문장은 나누고 숫자는 글자로 쓰세요.

## 기여하기

어디서부터 시작할지 모르겠다면, 다음 네 개의 작은 issue가 첫걸음으로 좋습니다.

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) 내 GPU에서 실행해 보고 카드, 드라이버, 소요 시간 보고하기
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: 실험적인 Vulkan 빌드 사용해 보기
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) 테스트 세트에 문장 하나 추가하기
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) 직접 디자인한 목소리를 설명과 시드와 함께 공유하기

공용 테스트 세트: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt), 브랜드 보이스 가이드:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md), 코드 보내는 방법: [CONTRIBUTING.md](CONTRIBUTING.md).
설치 문제: [issue 양식](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml), 질문과 결과: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
참여하는 모든 사람은 [행동 강령](CODE_OF_CONDUCT.md)을 따릅니다. 친절하게, 피드백은 작업 자체에 대해서만.

## 기여자

- [@alexturkey](https://github.com/alexturkey): 메인테이너. 코드, 기본 제공 목소리, 문서
- [@cayir21](https://github.com/cayir21): macOS(Apple Silicon) Metal 지원, [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): CPU 백엔드에서 여러 문장을 읽을 때의 문장 끝(EOS) 수정, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5): Ubuntu/Linux용 실험적 CUDA 설치 및 Docker 지원, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

여러분의 이름도 여기에 들어갈 수 있습니다. 내 GPU에서 얻은 테스트 결과, 테스트 세트에 넣을 문장 하나, 직접 디자인한 목소리, 명확한 버그
보고, 풀 리퀘스트 모두 기여입니다. 사용해 보고 소식을 전해 주시는 모든 분께 감사드립니다.

## 라이선스와 크레디트

코드와 기본 제공 목소리: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. VoxCPM2(OpenBMB, Apache-2.0),
audio.cpp(ShugoAI LLC, Apache-2.0), audio.cpp GGUF 변환을 바탕으로 만들었습니다. 전체 목록: [THIRD_PARTY.md](THIRD_PARTY.md).
OpenBMB, ModelBest, audio.cpp 프로젝트와는 관련이 없습니다.

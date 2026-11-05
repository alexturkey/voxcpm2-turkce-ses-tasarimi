[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · **日本語** · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**4 GB の GPU で、VoxCPM2 を使ってトルコ語の声をデザイン。** 英語で声を説明すると、モデルがその声を作ります。
気に入った候補を選べば、その声で好きなトルコ語のテキストを読み上げられます。ワンコマンドのインストーラー、
GTX 1050 Ti（4 GB）に収まるようパッチを当てた [audio.cpp](https://github.com/0xShug0/audio.cpp) エンジン、
小さなローカル Web UI、そして 14 種類の収録済み合成ボイスを同梱しています。内訳はトルコ語 7 種類と、
英語・フランス語・ドイツ語・スペイン語・ロシア語・中国語・日本語のネイティブナレーター 7 種類です。

- 30 言語の読み上げに対応し、UI も 30 言語で利用できます。
- 収録済みボイスは 14 種類：トルコ語 7 種類に加え、英語・フランス語・ドイツ語・スペイン語・ロシア語・中国語・日本語が各 1 種類。
- Web UI（v0.2.0）：各候補カードに 2 つの声（素の設計音声と、これからずっと聞く声）を表示。ボイスメニュー付きの
  読み上げリスト、ボイスの名前変更・非表示・削除、読み上げるテキストの下書き機能。詳しくは「使い方」の「Web UI」を参照してください。

[4 GB に収める仕組み](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [AI エージェント向けインストールガイド](AGENTS.md) · [責任ある利用](ETHICS.md)

> 同梱のボイスはすべて、テキストの説明からデザインした合成音声です。ボイスクローン機能は、ご自身の声、または
> 声の持ち主から明示的な許可を得た声にのみ使用してください。UI ではその許可の確認を求められます。なりすまし、
> 詐欺、欺瞞行為は禁止です。生成したものには AI 生成であることを明記してください。詳しくは [ETHICS.md](ETHICS.md) をご覧ください。

## 30 言語

カッパドキアのドキュメンタリー動画を 1 本、8 言語で制作しました：トルコ語、英語、フランス語、ドイツ語、スペイン語、ロシア語、中国語、
日本語です。各言語にはそれぞれ専用の**ネイティブナレーター**がいて、VoxCPM2 で英語の説明からデザインしています。
すべて 4 GB の GTX 1050 Ti 上で完全にローカルで生成し、品質設定は固定のまま（16 ステップ、cfg 2.0）です。
7 人のナレーターは、プロンプト、デザイン用テキスト、シード、リファレンス録音とともにこのリポジトリに同梱しています。

| コード | 言語 | ボイス | 試聴 | 動画 |
|---|---|---|---|---|
| `tr` | トルコ語 | `hazir/belgesel_hanim`（ほか 6 種類） | [サンプル](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | 英語 | `hazir/anlatici_en` | [サンプル](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113791986763440439) |
| `fr` | フランス語 | `hazir/anlatici_fr` | [サンプル](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113790681575804962) |
| `de` | ドイツ語 | `hazir/anlatici_de` | [サンプル](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113791351645262249) |
| `es` | スペイン語 | `hazir/anlatici_es` | [サンプル](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113807365611122705) |
| `ru` | ロシア語 | `hazir/anlatici_ru` | [サンプル](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113801574136848884) |
| `zh` | 中国語（標準中国語） | `hazir/anlatici_zh` | [サンプル](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113802229606121794) |
| `ja` | 日本語 | `hazir/anlatici_ja` | [サンプル](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [動画](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**なぜ 1 文ずつ読むのか。** VoxCPM2 は、1 回で長い音声（おおよそ 30 秒超）を生成すると安定しません。リズムが
だんだん速くなり、声質がずれていくことがあります。本プロジェクトでは固定のリファレンス録音とシードで声を保ち、
長いテキストは 1 行 1 文で読み上げるため、最初の文から最後の文まで声質とスタイルが変わりません。トルコ語以外の
言語ではトルコ語の発音辞書は適用されません。VoxCPM2 が対応する 30 言語はすべてテスト済みで動作します。収録済みボイスが
ない言語では `--dil <code>` を使ってください。言語ごとのコマンドと、私たちが得た教訓：
[docs/cok_dilli.md](docs/cok_dilli.md)。デザインの流れ全体をカバーする Claude Code スキル：
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md)。

**すぐ使える 144 のサンプルプロンプト。** 8 言語それぞれに 18 の役柄（ドキュメンタリーのナレーター、ニュースキャスター、
CM ナレーション、オーディオブック、昔話を語るおばあさん、ポッドキャストのホスト、先生、映画予告編、瞑想ガイド、
スポーツ実況など、男性・女性とも）を用意しました。プロンプトは英語で、話者の国籍とネイティブのアクセントを含みます。
声を作るときに読み上げるテキストも付属しており、その言語で役柄に合わせて書かれています。1 つ選んで候補を
聞き比べ、気に入ったものを残してください：`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`、
または Web UI で*サンプルの説明文*を選びます。全リスト：[docs/ornek_tarifler.md](docs/ornek_tarifler.md)。

**自分の声で動画を吹き替え。** [DubWorld](https://github.com/alexturkey/dubworld) は私たちのローカル動画吹き替え
プログラムで、このリポジトリを VoxCPM2 音声エンジンとしてインストールします。ここでデザインした声は、DubWorld 側で
`ses.voxcpm2_ses = "<name>/<variant>"` として使えます。

## クイックスタート（Windows、3 ステップ）

1. コードを**ダウンロード**：[voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip)。
   お使いのグラフィックカード向けのビルド済みエンジンパッケージは、ステップ 3 でインストーラーが取得します：
   NVIDIA → [CUDA パッケージ](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.0/voxcpm2-turkce-ses-tasarimi-motor-v0.3.0-win64-cuda12.8.zip)、
   AMD / Intel → [Vulkan パッケージ（実験的）](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan.zip)
   （すでにダウンロード済みの場合は、下のコマンドに `-HazirZip <path to the zip>` を追加してください）。
2. zip を**展開**し、`voxcpm2-turkce-ses-tasarimi-main` フォルダーを開いて、エクスプローラーのアドレスバーに `powershell`
   と入力して Enter キーを押します。
3. インストーラーを**実行**し（64 ビット版 Python 3.10-3.13 が必要。CUDA の場合は NVIDIA ドライバー ≥ 570）、**`baslat.bat`** をダブルクリックします：
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel の場合は末尾に `-Vulkan` を追加します。UI は http://127.0.0.1:8765/ で開きます。

エンジンの zip は単体で動くアプリではありません（中の exe には、インストーラーがセットアップするモデルと DLL が必要です）。詳細、GPU
一覧、よくあるトラブル：下の「クイックインストール」を参照してください。

## Ubuntu / Linux（NVIDIA CUDA、実験的）

`bash scripts/kur-linux.sh` でパッチ適用済みエンジンをビルドするか、`Dockerfile.linux` を使って
Ubuntu 24.04 / CUDA 12.8.1 環境でビルド・実行します。NVIDIA GPU と対応ドライバーが必要です。ネイティブインストーラーには
さらに CUDA toolkit と Python 3.10-3.13 も必要です。UI はリモートサーバー上でもループバック（ローカル）専用のままです（SSH ポート転送を使用）。
前提条件、コマンド、アーキテクチャの選択、検証範囲：[docs/linux.md](docs/linux.md)。

## クイックスタート（macOS、Apple Silicon）

Xcode Command Line Tools（`xcode-select --install`）と [Homebrew](https://brew.sh) が必要です：
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
インストーラーがモデルをダウンロードし、パッチ適用済みエンジンを Metal でビルドして（約 1 分）、すべてを `~/vox` 以下にセットアップします。
その後 **`baslat.command`** をダブルクリックします。MacBook Air M4 16 GB では：音声 1 秒あたり約 2 秒の計算、同じシードなら
バイト単位で同一の音声、RAM ピーク約 5.3 GB、12 分間連続で読み上げてもサーマルスロットリング（発熱による速度低下）なし。詳細と
測定結果：[docs/mac.md](docs/mac.md)。

**ネイティブ Mac アプリ（Python、Homebrew、ターミナル不要）：**[macos/README.md](macos/README.md)。同じパッチ適用済み
エンジンを同梱し、初回起動時にモデルをダウンロードします。現時点では Xcode でソースからビルドする必要があります。

## Mac（Apple Silicon）ユーザーの方へ

Apple の MLX フレームワークで VoxCPM2 を動かす、コミュニティによる独立した Apple Silicon Mac 向け移植版もあります：
**[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**。
こちらは Emre Koç さん（[@emre-koc](https://github.com/emre-koc)）がご自身のリポジトリで開発・メンテナンスしているもので、
本リポジトリのものではありません。インストール手順やサポートに関する質問はそちらへどうぞ。Emre さん、このプロジェクトを Mac に届けてくれてありがとう！

## 仕組み

1. **声のデザイン。** 英語の*声の説明* + *声を作るときに読み上げるテキスト*（その声の言語で）+ 候補の
   数。各候補にはそれぞれ専用のシードが割り当てられます。エンジンは `(description)text` を受け取り、シードごとに
   設計音声を 1 つ返します。このテキストは声の感じをつかむための短いサンプルです：1〜3 文、最長約 30 秒（UI は
   推定時間を表示し、33 秒を超えると開始しません）。長いテキストはステップ 2 で扱います。
2. **リファレンスに基づく読み上げ。** 設計音声はエンジンの**両方**の入力（`audio` と `voice_ref`）に、
   その書き起こし（`reference_text`）と読み上げる新しいテキストとともに、同じシードで渡されます。声を保つのは
   説明文ではなく録音なので、テキストが変わっても声がずれません。テキストは 1 文ずつ読み上げます。
3. 品質は固定です：拡散ステップ 16、CFG 2.0。シードは品質の調整つまみではありません。
4. **単語のタイミングと、毎回同じ音声。** 読み上げ中にエンジン自体が各単語の開始と終了の位置を出します（パッチ 0002、追加モデル不要）。時刻は `kelimeler.json` に書き出され、行間の無音が間の設定と等しくなるよう各行がトリミングされます。CTC 強制アライメント（forced alignment、CTC = 100%）に対する精度：89.66%（トルコ語、12 音声。設定 `kelime_zamani`、既定でオン）。パッチ 0003 により、同じシードなら毎回バイト単位で同一の音声になります。

素の設計音声は、その声の一度きりのサンプルです。後からどの読み上げをしても、まったく同じにはなりません。後の
読み上げで毎回聞こえるのはステップ 2、つまり設計音声をリファレンスにし、その候補専用のシードで読んだ声です。だからこそ Web UI は
デザイン直後にステップ 2 を実行し、両方を候補カードに表示します。

エンジンは audio.cpp v0.7.2 に私たちのパッチ（`patches/`）を当てたもので、モデルは VoxCPM2 Q8_0 GGUF です。VRAM ピーク ≈ 2.8 GB。
GTX 1050 Ti では音声 1 秒あたり約 2 秒の計算です。詳細と測定結果：[docs/4gb.md](docs/4gb.md)。

## 収録済みボイス（`hazir_sesler/`）

14 種類すべて、各 `ses.json` に保存されたプロンプトからデザインしたもので、録音からクローンしたものは 1 つもありません（クローンは
別の、同意確認付きの*ボイスクローン*タブです）。

| ボイス | 概要 | 試聴 |
|---|---|---|
| `belgesel_hanim` | 50 代の成熟した女性、深く温かいアルト。落ち着いたドキュメンタリーのナレーター | [サンプル](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [リファレンス](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | 深く力強い、神秘的な男性ナレーター | [サンプル](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [リファレンス](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | 70 歳前後のベテランニュースキャスター。落ち着きがあり威厳のある声 | [サンプル](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [リファレンス](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | 30 代のカリスマ的な夜のニュースの女性キャスター。ビロードのようになめらかで表情豊か | [サンプル](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [リファレンス](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | おとぎ話の魔女：低く、少し鼻にかかった、ずる賢い甘さ | [サンプル](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [リファレンス](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | 並外れて深く、重厚で、威圧感のある男性ナレーター | [サンプル](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [リファレンス](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | 年老いた賢者。深く響き渡る声で、少し神秘的 | [サンプル](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [リファレンス](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | 英語ネイティブの 50 代男性ドキュメンタリーナレーター（一般米語）。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | フランス語ネイティブの 50 代男性ドキュメンタリーナレーター（パリ）。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | ドイツ語ネイティブの 50 代男性ドキュメンタリーナレーター（標準ドイツ語）。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | スペイン語ネイティブの 50 代男性ドキュメンタリーナレーター（カスティーリャ語（マドリード））。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | ロシア語ネイティブの 50 代男性ドキュメンタリーナレーター（モスクワ）。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | 中国語（標準中国語）ネイティブの 50 代男性ドキュメンタリーナレーター（北京の普通話）。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | 日本語ネイティブの 50 代男性ドキュメンタリーナレーター（東京の標準語）。深く、落ち着いた、温かい声 | [サンプル](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [リファレンス](hazir_sesler/anlatici_ja/referans.flac) |

各フォルダーの中身：`referans.flac`（ロスレスの設計音声）、`ses.json`（プロンプト、書き起こし、デザインのシード、読み上げのシード、
説明。ナレーターでは `dil` = 言語）、`ornek_okuma.mp3`（とそのテキスト）。そのまま使えます：`--ses hazir/<name>`。
ナレーターのリファレンス録音は短く（5.6-10 秒）、サンプルはカッパドキアの台本の最初の 3 文を、
完成版の読み上げから切り出したものです。

## クイックインストール、コンパイラー不要（Windows 10/11、NVIDIA GPU ≥ 4 GB）

前提条件：NVIDIA ドライバー ≥ 570 と 64 ビット版 Python 3.10-3.13（`winget install Python.Python.3.12`）。必要なのはこれだけで、
Visual Studio も CUDA インストーラーも要りません。自分のグラフィックカードがわからない場合は、PowerShell で `nvidia-smi` を実行してください。GPU
名、ドライバーのバージョン、メモリ容量が表示されます。NVIDIA のカードがない場合は、下の「AMD / Intel」を参照してください。

[Git](https://git-scm.com/download/win) を使う場合：

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Git を使わない場合：このページで **Code → Download ZIP** をクリックして展開し、展開した
`voxcpm2-turkce-ses-tasarimi-main` フォルダーを開いて、エクスプローラーのアドレスバーに `powershell` と入力して Enter キーを押し、
上の最後の行を実行します。Git が必要なのはソースからビルドする場合だけです。

`-ExecutionPolicy Bypass` はこのプロセスにだけ適用され、システム設定は一切変更しません。どのインストーラースクリプトでも同じですが、
実行前に `scripts\kur.ps1` に目を通してください。コマンド 1 つで約 10 分、ダウンロード約 3.7 GB、すべて sha256 で検証されます：モデル（2.95 GB）、
ポータブル zip 形式の CUDA 12.8 ランタイム DLL（システムへのインストールなし、PATH も変更しない）、Releases ページの**ビルド済みエンジン**、
2 つの Python パッケージを入れた `.venv`、`ayarlar.json`、そして最後の GPU チェック（`KONTROL_OK`）。途中で失敗したら再実行してください。検証済みのファイルは
スキップされます。その後 Web UI を起動します：リポジトリのフォルダーで **`baslat.bat`** をダブルクリックすると UI が起動し、準備ができたら
ブラウザーで **http://127.0.0.1:8765/** が開きます。終了するには黒いウィンドウを閉じます（またはそこで Ctrl+C を押します）。
PowerShell から同じことをするには：

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
を実行し、**http://127.0.0.1:8765/** をご自身で開いてください（この方法で起動した場合、UI はブラウザーを開きません。また
localhost からの接続のみを受け付けます）。

> **リリース zip の `audiocpp_cli.exe` はダブルクリックして使うものではありません。** これはコマンドラインのエンジンで、
> 同じ場所に CUDA の DLL とモデルが必要です。`kur.ps1` がすべてを配置し、Python パッケージがエンジンを動かします。
> ダブルクリックしても "cudart64_12.dll not found" と表示されるだけです。

**対応 GPU（リリース v0.3.0）：** GTX 10xx（sm_61）、RTX 20xx（sm_75）、RTX 30xx（sm_86）、RTX 40xx
（sm_89）、RTX 50xx（sm_120a）向けのネイティブコードを収録。Pascal 以降のその他の CUDA GPU は、ドライバー経由で埋め込みの PTX を実行します（初回起動は
遅くなります）。Maxwell（GTX 9xx）以前は CUDA 12.8 の対象外です。私たちは GTX 1050 Ti 4 GB でテストしました（Windows の Docker Desktop/WSL2 経由でも、CLI のみ）。@mslmyilmaz5 さんによる測定（#15）：RTX 3060 Ti 8 GB、Ubuntu 24.04 Docker、
CUDA 12.8.1（詳細は [docs/linux.md](docs/linux.md)）。ほかのカードでの報告は [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) で歓迎しています。

**AMD / Intel（実験的）：** CUDA を使わない別の Vulkan エンジンは `scripts\kur.ps1 -Kok C:\vox -Vulkan` でインストールします。私たちの NVIDIA カードで Vulkan バックエンドを通して（そこでは CUDA より遅く、同じシードで同じ音声。条件をそろえた速度比較はまだです）、また Intel HD Graphics 630 内蔵グラフィックスで（音声 1 秒あたり約 35〜50 秒の計算）試しました。AMD では私たち自身はテスト**していません**。試した方は、ぜひ結果を Discussions に投稿してください。Vulkan デバイスが複数ある場合（内蔵 + 単体）、インストーラーは単体 GPU のインデックスを `cihaz` として `ayarlar.json` に書き込みます。

**コミュニティによるテスト（AMD）：** @mitraTR さんが Windows 11 の AMD Radeon RX 6900 XT で v0.1.1 を Vulkan で動かしました。インストール、音声デザイン、読み上げ、Web UI、テストのすべてが成功し、読み上げは音声 1 秒あたり約 0.8〜0.9 秒の計算時間でした（[#6 のレポート](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)）。インストール先は、パスに ASCII 文字だけを含む短いフォルダーにしてください（例：`C:\vox`）。Windows ではエンジンが日本語などの ASCII 以外の文字を含むパスを開けません。これまでのすべてのレポート：[動作確認済みハードウェア](docs/donanim_testleri.md)。

**Vulkan についての注意：** エンジン v0.3.1 から Vulkan でも単語のタイミングが出ます。パッケージは 2 つ：`vulkan` は AVX2 対応の CPU が必要です（2013 年以降の多くの Intel Core、2015 年以降の AMD。Pentium/Celeron の多くは非対応）。[`vulkan-uyumlu`](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan-uyumlu.zip) はどの 64 ビット x86 CPU でも動きますが、ある声の最初の読み上げに約 2.2 倍の時間がかかります（2 回目以降は同じ速さ）。`kur.ps1 -Vulkan` が CPU を調べてパッケージを自動で選びます。内蔵グラフィックスでは、読み上げ中にエンジンが約 8 GB の RAM を使います。Vulkan での初回起動は GPU シェーダーのコンパイルのため数分かかることがあります。その後の読み上げは速くなります。詳細：[docs/vulkan.md](docs/vulkan.md)。

### 別の方法：エンジンをソースからビルド

Visual Studio 2022 Build Tools と "Desktop development with C++"（C++ CMake tools を含む）が必要で、約 7 GB です。そのうえで：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
これにより nvcc もダウンロードされ、audio.cpp v0.7.2 のソースを取得し、`patches/0001-voxcpm2-4gb-ve-hiz.patch` を適用して、
お使いの GPU 向けにビルドします（`-Mimari native` が既定値。例えば `-Mimari 61` も指定可）。約 15-25 分かかります。ルートは短く（`C:\vox`）してください：
nvcc は長いパスで失敗します。チェック付きの手順：[AGENTS.md](AGENTS.md)。

### よくあるインストールのトラブル

| 表示される内容 | 意味と対処 |
|---|---|
| exe をダブルクリックすると `cudart64_12.dll not found` | エンジンは手動で起動するものではありません。上の `kur.ps1` コマンドを実行してから Web UI を起動してください。 |
| `64-bit Python 3.10+ bulunamadı`（Python が見つからない） | Python をインストールし（`winget install Python.Python.3.12`）、PowerShell を閉じて新しく開き、同じコマンドをもう一度実行します。 |
| `motor ekran kartını görmedi`（エンジンが GPU を認識しない） | NVIDIA ドライバーを 570 以降に更新し、`nvidia-smi` が動くことを確認します。 |
| `indirme başarısız` / `sha256 tutmadı`（ダウンロード失敗 / チェックサム不一致） | たいていはダウンロードの中断です。同じコマンドをもう一度実行してください。検証済みのファイルはスキップされます。 |
| ソースからのビルド：`nvcc` が失敗する | インストール先のルートを短くします（`-Kok C:\vox`）。 |
| ページが開かない | `baslat.bat` で UI を起動するか、http://127.0.0.1:8765/ をご自身で開いてください。ポートが使用中なら `ayarlar.json` の `"port"` を変更します。 |

困ったときは [Discussions（Q&A）](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) か、
[インストールの issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
に、GPU、Windows のバージョン、実行したコマンドとその最後の数行を添えて投稿してください。

## 使い方

コマンドライン：
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
テキストのルール：数字は文字で書き、引用符は使わない（ツールは数字と引用符を受け付けません）、1 行に 1 文、
1 行 ≤ 2000 文字。行の後の間：`|| bagli` 0.25 秒、`|| normal` 0.5 秒、`|| paragraf` 1 秒、`|| agir` 1.5 秒、
または任意の長さ `|| 0,8`（0-5 秒。この記号の中の数字は使えます）。`ayarlar/okunus_sozlugu.tsv` はトルコ語テキスト中の外来語の発音を修正します。
言語はテキストから判定されます（トルコ語の文字、文字体系、よく使われる単語。判断できない場合はボイスカードの `dil`。`--dil <code>` は任意）。トルコ語以外のテキストではアポストロフィが使え、トルコ語辞書は
適用されませんが、数字は引き続き受け付けません。読み上げ中に `speed gate: satır [...]` と表示されたら、その行を聞いて確認してください。

### Web UI

ローカル専用（127.0.0.1）：`.venv\Scripts\python.exe -m ses_tasarim.arayuz` → http://127.0.0.1:8765/ をご自身で開きます
（別のポート：`--port 8800`）。または `baslat.bat` をダブルクリックします。サーバーは Ctrl+C で停止します。タブは 3 つ：*声をデザイン*、
*この声で読み上げ*、*ボイスクローン*。一般的な流れ：*デザインする* → 候補を聞き比べる → *読み上げリストに追加* →
*この声で読み上げる* → ダウンロード。または、ボイスメニューから収録済みボイスを選んで読み上げます。

- **ヘッダーのバージョン表示。** 小さく薄い文字で `v0.3.1 · <short commit>`（追跡対象のファイルに未コミットの変更があれば `+` 付き。
  git がなければバージョンのみ）。スクリーンショットや動画で、どのバージョンを使ったかがわかります。
- **各候補カードに 2 つの声。** 上段のグレーは*素の設計音声*：一度だけ生成され、同じものは二度と出ません。
  その下のオレンジ枠は *↻ これからずっと聞く声です*：設計音声をリファレンスにして、その候補専用のシード（カードに表示）で
  読み直したものです。これが、後のすべての読み上げで聞こえる声です。その下に*この声で読み上げる*と*読み上げリストに追加*があります。
  *デザインする*を 1 回押すだけで両方を行います：すべての候補をデザインし、続けて各候補の固定の声であなたのテキストを読み上げます。1 本の進行状況バーが両方の段階を数えます。
  候補フォルダーには `dinleme.wav` ができます。この読み上げが途中で止まってもデザインは残り、カードにメモが表示されます。
- **「聞きたいテキスト」ウィンドウ。** *声をデザイン*の *↻ 聞きたいテキスト* 欄には、各候補の固定の声が読み上げる内容を入れます
  （空欄ならサンプル文を読み上げます）。クリックすると、読み上げノートがウィンドウで開きます：行番号、
  行メニュー、間の帯。*OK* でテキストとその間を欄に書き戻し、*キャンセル*または Esc では何も変わりません。
  読み上げタブは独自のテキストを保持します。
- **読み上げノート。** 1 行に 1 文。行番号をクリックすると行メニューが開きます（上下に移動、指定位置へ移動、
  複製、削除。Alt+↑/↓、Alt+Shift+↓、または番号をドラッグ。Ctrl+Z でテキストと間をまとめて元に戻せます）。
  2 行の間の細い帯をクリックすると間の長さを選べます（bagli 0.25 · normal 0.5 · paragraf 1 · agir 1.5 秒、または歯車で
  0-5 秒の任意の長さ）。Enter を 2 回押すと段落（1 秒）になり、空行は間の帯になります。結果の再生中は、
  読んでいる行が光って画面内にスクロールします。行メニューの *▶ ここから再生* でその行から再生できます。
  テキストとその間は、ページを再読み込みしても残ります（ブラウザーのストレージ）。
- **下書き。** *📄 下書き* ボタンは両方のノート（読み上げタブとウィンドウ）にあります。現在のテキストを間ごと
  下書きとして保存し、クリック 1 つで読み込めます（Ctrl+Z で元に戻せます）。⋯ で上書き、名前の変更、削除ができます。下書きは
  `sesler/taslaklar.json` に保存され、リポジトリには決して入りません。
- **読み上げリストとボイスメニュー。** 候補カードで*読み上げリストに追加*を押すと名前の入力欄が開きます：候補に
  独自の名前を付け、✓ で追加します。*生成の名前*は、その回のすべての候補に残ります。*この声で読み上げ*では、ボイス
  ボタン（国旗 + 名前）でボイスメニューが開きます：一番上に*読み上げリスト*、続いて国旗付きの収録済みボイス（UI の
  言語が先頭）。各行には ▶ 試聴（固定の声があればその声）、ハート（追加・削除）、⋯ があります。↑/↓ と
  Enter で選択、Esc で閉じ、最後に使ったボイスは記憶されます。リストは `sesler/okuma_listesi.json` に保存され、
  リポジトリの外にあるので、再起動しても残ります。
- **ボイスの管理。** ⋯ メニュー（ボイスメニューの行または候補カード）には、*この声で読み上げる*、リストへの追加・
  削除、*名前を変更*（名前を空にすると元に戻ります。*元の名前に戻す*）、デザインしたボイスには*削除*、収録済みボイスには*非表示*があります。
  どちらも実行前に確認します。削除したボイスは `sesler/_cop/` に移動し、非表示はリポジトリのファイルに一切触れません。
  ボイスメニューの一番下にある*非表示・削除したボイス（N）*、その中に*元に戻す*があります。独自の名前と非表示のボイスは
  `sesler/yerel_katman.json` に保存されます。名前を変えたボイスには、元の情報がグレーで表示されます（*生成の名前 · 候補N*）。⋯ → *生成結果へ移動*
  でそのデザインが開きます。
- **ショートカットとファイル。** Ctrl+Enter（Mac では ⌘+Enter）で、開いているタブの*デザインする*または*この声で読み上げる*を実行します。
  進行状況バーには*経過時間 / ~合計*が表示され、合計の目安はお使いのマシンでの過去の処理から学習します。ダウンロードされるファイルは
  ボイス名と時刻で名前が付きます（`Voice_Name_2026-11-02_0152.wav`）。

**ボイスクローン（ご自身の声、または同意を得た声）。** UI の*ボイスクローン*タブで、録音（wav/mp3/flac/ogg。5-30 秒のクリアな音声を推奨。3 秒未満は拒否され、36 秒を超える部分はカットされます）、その正確な書き起こし、読み上げるテキストを指定します。「これは私の声です、または声の持ち主から明示的な許可を得ています」にチェックを入れるまで、ボタンは無効のままです。録音はローカルサーバー（127.0.0.1）にだけ送られ、一時フォルダーでリファレンスのエンコードとともに処理されます。このフォルダーは処理が終わると削除されます（失敗した場合も同様です）。ネットワーク経由で送信されるものは何もありません。保存されるのは合成された出力だけです（UI：`sesler/_okumalar/<job>/`、CLI：`--cikti`）。出力は "synthetic" タグ付きの `klon_synthetic.wav` です。共有する際は AI 生成であることを明記してください。CLI：`python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## よくある質問

**モデルとエンジン、それぞれ何？** VoxCPM2（OpenBMB）は*モデル*で、テキストを音声に変える 20 億パラメーターのニューラルネットワークです。
audio.cpp は*エンジン*で、お使いの GPU 上でモデルを動かす C++/CUDA プログラム（`audiocpp_cli.exe`）です。私たちの
パッチが変更するのはモデルではなくエンジンです：VoxCPM2 を 4 GB に収め、同じシードなら毎回同じ音声が出るようにします。
このリポジトリの Python パッケージは、テキストの準備、エンジンの呼び出し、ファイルの収集だけを行います。

**どの GPU で動く？** 上の「対応 GPU」を参照してください：GTX 10xx 以降の NVIDIA、VRAM 4 GB 以上、ドライバー ≥ 570。ネイティブコードは
リリースに sm_61/75/86/89/120a 向けが含まれ、その他の Pascal 以降のカードは埋め込みの PTX を使います（初回起動は遅くなります）。AMD/Intel：実験的な Vulkan zip、`kur.ps1 -Vulkan`。Intel HD Graphics 630 内蔵グラフィックスでは私たちが試しました。@mitraTR は以前の v0.1.1 を AMD RX 6900 XT で動かしましたが、新しい v0.3.1 パッケージは AMD ではまだ試されていません（上の「AMD / Intel」を参照）。CPU のみ（`ayarlar.json` で `"backend": "cpu"`）でも動きますが、
GTX 1050 Ti より約 6 倍遅く（エンジンでの測定、48 秒の音声で 535 秒対 94 秒）、サポート対象外です。

**速度は？** GTX 1050 Ti 4 GB（i7-7700HQ）での測定：デザインの候補 1 つ（≈ 25 秒の録音）で 55 秒。読み上げは音声 1 秒あたり ≈ 2 秒の
計算（リアルタイム係数 1.9-2.8）。ただし最初にボイスごとに 1 回だけ約 50 秒のリファレンスエンコード（ディスクに
キャッシュ）と、バッチごとに 10-20 秒のモデル読み込みがかかります。VRAM ピーク 2.6-2.9 GB。新しいカードほど速くなります。数値と方法：
[docs/4gb.md](docs/4gb.md)。

**声のクローンはできる？** 基盤の VoxCPM2 モデルはリファレンス録音から声をまねることができ、クローン
機能はそれを利用しています。使うのは、ご自身の声か、声の持ち主の明示的な許可がある場合だけにしてください。
UI ではその許可の確認を求められます。声のデザインには録音は不要です：英語または中国語のテキストの説明から始まり、
デザインした声を読み上げる際の「リファレンス」は、モデル自身が合成した設計音声です。なりすまし、詐欺、
欺瞞行為は禁止です。詳しくは [ETHICS.md](ETHICS.md) をご覧ください。公開するものには AI 生成であることを明記してください。

**良い声の説明を書くには？** 英語で 1〜3 文：年齢と性別、声質（深い/明るい、温かい、
鼻にかかった、しゃがれた）、トーンと役柄（落ち着いたドキュメンタリーのナレーター、元気な司会者）、テンポ（ゆっくり、落ち着いた）、そして
"clean studio recording, no background noise"。台本ではなく説明として書き、かっこは使いません。候補は 3〜5 個
作って聞き比べてください：シードで声は大きく変わります。声を作るときのテキストは、その声の言語で自然な 1〜3 文にし、
望む雰囲気で書きます（音声で最長約 30 秒）。読み上げるときは 1 行に 1 文。長い文は分け、数字は文字で書きます。

## コントリビューション

どこから始めればいいかわからない方へ。次の 4 つの小さな issue が最初の一歩にぴったりです：

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) お使いの GPU で試して、カード、ドライバー、所要時間を報告する
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel：実験的な Vulkan ビルドを試す
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) テストセットに文を 1 つ追加する
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) デザインした声を、説明とシードを添えて共有する

**お使いの GPU で試して、レポートを書いてください：** コーディングは不要で、[ハードウェアテストレポートのフォーム](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml)だけで十分です。Intel HD Graphics 630（内蔵）は私たちが試しました。Intel Arc のレポートはまだなく、v0.3.1 での AMD のレポートもまだありません。

共有テストセット：[docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt)、ブランドボイスガイド：
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md)、コードの送り方：[CONTRIBUTING.md](CONTRIBUTING.md)。
インストールのトラブル：[issue フォーム](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)、質問と結果：[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions)。
参加する全員が[行動規範](CODE_OF_CONDUCT.md)に従います：親切に、フィードバックは作業そのものについて。

## コントリビューター

- [@alexturkey](https://github.com/alexturkey)：メンテナー。コード、収録済みボイス、ドキュメント
- [@cayir21](https://github.com/cayir21)：macOS（Apple Silicon）の Metal 対応、[#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis)：CPU バックエンドで複数文を読み上げる際の文末（EOS）の修正、[#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5)：Ubuntu/Linux 向けの実験的な CUDA インストールと Docker 対応、[#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

ここにあなたの名前も載せましょう：お使いの GPU でのテスト結果、テストセットへの 1 文、デザインした声、わかりやすいバグ
報告、プルリクエスト、どれも立派な貢献です。試して感想を寄せてくださるすべての方に感謝します。

## ライセンスとクレジット

コードと収録済みボイス：Apache-2.0、Copyright 2026 Ali Haydar Ozturk。VoxCPM2（OpenBMB、Apache-2.0）、
audio.cpp（ShugoAI LLC、Apache-2.0）、audio.cpp の GGUF 変換をもとに構築しています。全リスト：[THIRD_PARTY.md](THIRD_PARTY.md)。
OpenBMB、ModelBest、audio.cpp プロジェクトとは関係ありません。

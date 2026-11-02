[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md) · [Italiano](README.it.md) · **Português** · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Design de voz em turco com o VoxCPM2 numa GPU de 4 GB.** Descreva uma voz em inglês, deixe o modelo criá-la, escolha a
variante de que mais gostar e depois leia qualquer texto em turco com essa voz. Inclui um instalador de um só comando, um
motor [audio.cpp](https://github.com/0xShug0/audio.cpp) com patch que cabe numa GTX 1050 Ti (4 GB), uma pequena interface web
local e catorze vozes sintéticas prontas: sete em turco e sete narradores nativos em inglês, francês, alemão, espanhol,
russo, chinês e japonês.

- O app lê em 30 idiomas; a interface também está em 30 idiomas.
- 14 vozes prontas: 7 em turco, mais uma em cada um destes idiomas: inglês, francês, alemão, espanhol, russo, chinês e japonês.
- Interface web (v0.2.0): cada cartão de variante tem duas vozes, a voz bruta do design e a voz que você vai ouvir sempre; uma
  lista de leitura com menu de vozes; renomear, ocultar ou excluir vozes; rascunhos para os textos que você lê. Veja "Interface web" em "Uso".

[Como cabe em 4 GB](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Guia de instalação para agentes de IA](AGENTS.md) · [Uso responsável](ETHICS.md)

> As vozes incluídas são sintéticas, criadas a partir de uma descrição em texto. A seção de clonagem de voz é só para a sua
> própria voz ou para uma voz usada com a permissão explícita do dono; a interface pede que você confirme essa permissão.
> Passar-se por outra pessoa, fraude e engano são proibidos. Identifique o que você gerar como gerado por IA. Veja [ETHICS.md](ETHICS.md).

## 30 idiomas

Fizemos um mesmo vídeo documentário sobre a Capadócia em 8 idiomas: turco, inglês, francês, alemão, espanhol, russo, chinês
e japonês. Cada idioma tem seu próprio **narrador nativo**, criado com o VoxCPM2 a partir de uma descrição em inglês. Tudo
foi gerado de forma totalmente local numa GTX 1050 Ti de 4 GB, com a mesma qualidade fixa (16 passos, cfg 2.0). Os sete
narradores estão incluídos aqui, com seu prompt, texto de design, semente e gravação de referência.

| Código | Idioma | Voz | Ouvir | Vídeo |
|---|---|---|---|---|
| `tr` | Turco | `hazir/belgesel_hanim` (e mais 6) | [amostra](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Inglês | `hazir/anlatici_en` | [amostra](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113791986763440439) |
| `fr` | Francês | `hazir/anlatici_fr` | [amostra](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113790681575804962) |
| `de` | Alemão | `hazir/anlatici_de` | [amostra](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113791351645262249) |
| `es` | Espanhol | `hazir/anlatici_es` | [amostra](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113807365611122705) |
| `ru` | Russo | `hazir/anlatici_ru` | [amostra](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113801574136848884) |
| `zh` | Chinês (mandarim) | `hazir/anlatici_zh` | [amostra](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113802229606121794) |
| `ja` | Japonês | `hazir/anlatici_ja` | [amostra](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [vídeo](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Por que frase por frase.** O VoxCPM2 não é estável numa única geração longa (a partir de uns 30 segundos): o ritmo
acelera e a voz pode se desviar. Aqui a voz é sustentada por uma gravação de referência e uma semente fixas, e o texto longo
é lido com uma frase por linha, de modo que o timbre e o estilo continuam os mesmos da primeira à última frase. Para idiomas
que não sejam o turco, o dicionário de pronúncia turco não é aplicado. Todos os 30 idiomas suportados pelo VoxCPM2 foram testados e funcionam; use
`--dil <code>` para os que não têm voz incluída. Comandos por idioma e as lições que aprendemos:
[docs/cok_dilli.md](docs/cok_dilli.md). Skill do Claude Code para todo o fluxo de design:
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 prompts de exemplo para começar.** 18 papéis (narrador de documentário, apresentador de telejornal, voz comercial,
audiolivro, avó contadora de histórias, apresentador de podcast, professor, trailer de filme, guia de meditação, narrador
esportivo e outros, masculinos e femininos) em cada um dos 8 idiomas. O prompt é em inglês, com a nacionalidade e o sotaque
nativo do falante; junto vem o texto lido durante a criação da voz, nesse idioma e adequado ao papel. Escolha um, ouça as
variantes e fique com a que preferir: `python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, ou escolha
*Modelo de exemplo* na interface web. Lista completa: [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Duble seus vídeos com a sua própria voz.** [DubWorld](https://github.com/alexturkey/dubworld) é o nosso programa local de
dublagem de vídeo; ele instala este repositório como seu motor de voz VoxCPM2. Uma voz que você cria aqui é usada lá com
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Início rápido (Windows, 3 passos)

1. **Baixe** o código: [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   O pacote de motor pronto para a sua placa é baixado pelo instalador no passo 3:
   NVIDIA → [pacote CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-cuda12.8.zip),
   AMD / Intel → [pacote Vulkan, experimental](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.1.1/voxcpm2-turkce-ses-tasarimi-motor-v0.1.1-win64-vulkan.zip)
   (já baixou um? acrescente `-HazirZip <path to the zip>` ao comando abaixo).
2. **Extraia** o zip, abra a pasta `voxcpm2-turkce-ses-tasarimi-main`, digite `powershell` na barra de endereços do
   Explorador de Arquivos e pressione Enter.
3. **Execute** o instalador (requer Python 3.10-3.13 de 64 bits; driver NVIDIA ≥ 570 para CUDA) e depois clique duas vezes em **`baslat.bat`**:
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel: acrescente `-Vulkan` no final. A interface abre em http://127.0.0.1:8765/.

O zip do motor não é um aplicativo independente (o exe precisa do modelo e das DLLs que o instalador configura). Detalhes,
lista de GPUs e problemas comuns: "Instalação rápida" abaixo.

## Ubuntu / Linux (NVIDIA CUDA, experimental)

Compile o motor com patch com `bash scripts/kur-linux.sh` ou use o `Dockerfile.linux` para compilar e executar num ambiente
Ubuntu 24.04 / CUDA 12.8.1. Requer uma GPU NVIDIA e um driver compatível; o instalador nativo também precisa do CUDA
toolkit e do Python 3.10-3.13. A interface continua acessível só pelo loopback, inclusive em servidores remotos (encaminhamento SSH).
Pré-requisitos, comandos, seleção de arquitetura e escopo da validação: [docs/linux.md](docs/linux.md).

## Início rápido (macOS, Apple Silicon)

Requer as Xcode Command Line Tools (`xcode-select --install`) e o [Homebrew](https://brew.sh):
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
O instalador baixa o modelo, compila o motor com patch com Metal (~1 min) e configura tudo em `~/vox`.
Depois clique duas vezes em **`baslat.command`**. Num MacBook Air M4 de 16 GB: ~2 s de processamento por 1 s de fala, a
mesma semente gera áudio idêntico byte a byte, pico de ~5,3 GB de RAM, sem perda de desempenho por aquecimento em 12 min de
leitura contínua. Detalhes e medições: [docs/mac.md](docs/mac.md).

**App nativo para Mac (sem Python, Homebrew ou Terminal):** [macos/README.md](macos/README.md). Ele inclui o mesmo motor
com patch e baixa o modelo na primeira execução; por enquanto é compilado a partir do código-fonte com o Xcode.

## Para usuários de Mac (Apple Silicon)

Existe também uma adaptação independente, feita pela comunidade, para Macs com Apple Silicon, que roda o VoxCPM2 com o
framework MLX da Apple: **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Ela é desenvolvida e mantida por Emre Koç ([@emre-koc](https://github.com/emre-koc)) no repositório dele, não aqui; as
instruções de instalação e as dúvidas de suporte ficam lá. Obrigado, Emre, por levar este projeto ao Mac!

## Como funciona

1. **Design de voz.** Uma *descrição da voz* em inglês + um *texto lido durante a criação da voz* (no idioma da voz) + um número de
   variantes. Cada variante recebe sua própria semente; o motor recebe `(description)text` e devolve uma gravação de design
   por semente. O texto é uma amostra curta para conhecer a voz: 1-2 frases, no máximo ~20 s (a interface mostra a
   estimativa e não começa acima de 22 s); texto longo fica para o passo 2.
2. **Leitura com referência.** A gravação de design é passada para **as duas** entradas do motor (`audio` e `voice_ref`),
   junto com sua transcrição (`reference_text`) e o novo texto a ser lido, com a mesma semente. A voz é sustentada pela
   gravação, não pela descrição, por isso não se desvia de um texto para outro. O texto é lido frase por frase.
3. A qualidade é fixa: 16 passos de difusão, CFG 2.0. A semente não é um ajuste de qualidade.

A gravação de design bruta é uma amostra única da voz; nenhuma leitura posterior soa exatamente igual a ela. O que você ouve
em todas as leituras seguintes é o passo 2: a gravação de design como referência mais a semente própria da variante. Por
isso a interface web faz o passo 2 logo depois do design e mostra as duas no cartão da variante.

O motor é o audio.cpp v0.7.2 com o nosso patch (`patches/`), e o modelo é o VoxCPM2 Q8_0 GGUF. Pico de VRAM ≈ 2,8 GB;
cerca de 2 s de processamento por 1 s de fala numa GTX 1050 Ti. Detalhes e medições: [docs/4gb.md](docs/4gb.md).

## Vozes incluídas (`hazir_sesler/`)

As catorze foram criadas a partir dos prompts guardados no respectivo `ses.json`; nenhuma foi clonada de uma gravação (a
clonagem é a aba separada *Clonagem de voz*, que exige consentimento).

| Voz | Descrição curta | Ouvir |
|---|---|---|
| `belgesel_hanim` | Mulher madura na casa dos cinquenta, contralto grave e caloroso; narradora de documentário tranquila | [amostra](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [referência](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Narrador masculino grave, poderoso e misterioso | [amostra](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [referência](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Apresentador de telejornal experiente, por volta dos setenta, calmo e com autoridade | [amostra](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [referência](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Apresentadora carismática do jornal da noite, na casa dos trinta, aveludada e expressiva | [amostra](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [referência](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Bruxa de conto de fadas: grave, levemente nasal, de uma doçura maliciosa | [amostra](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [referência](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Narrador masculino excepcionalmente grave, denso e imponente | [amostra](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [referência](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Velho sábio, grave e retumbante, um pouco misterioso | [amostra](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [referência](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Narrador de documentário nativo de inglês, na casa dos cinquenta (General American); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Narrador de documentário nativo de francês, na casa dos cinquenta (parisiense); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Narrador de documentário nativo de alemão, na casa dos cinquenta (Hochdeutsch); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Narrador de documentário nativo de espanhol, na casa dos cinquenta (castelhano (Madri)); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Narrador de documentário nativo de russo, na casa dos cinquenta (Moscou); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Narrador de documentário nativo de chinês (mandarim), na casa dos cinquenta (Putonghua de Pequim); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Narrador de documentário nativo de japonês, na casa dos cinquenta (padrão de Tóquio); grave, calmo, caloroso | [amostra](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [referência](hazir_sesler/anlatici_ja/referans.flac) |

Cada pasta: `referans.flac` (gravação de design sem perdas), `ses.json` (prompt, transcrição, semente de design, semente de
leitura, descrição; `dil` = idioma, nos narradores), `ornek_okuma.mp3` (+ o texto dela). Use-as diretamente: `--ses hazir/<name>`.
As gravações de referência dos narradores são curtas (5,6-10 s); as amostras deles são as três primeiras frases do roteiro
da Capadócia, recortadas da leitura completa da produção.

## Instalação rápida, sem compilador (Windows 10/11, GPU NVIDIA ≥ 4 GB)

Pré-requisitos: driver NVIDIA ≥ 570 e Python 3.10-3.13 de 64 bits (`winget install Python.Python.3.12`). Nada mais:
nada de Visual Studio, nada de instalador do CUDA. Não sabe qual placa você tem? Execute `nvidia-smi` no PowerShell: ele mostra
o nome da GPU, a versão do driver e a memória. Sem placa NVIDIA? Veja "AMD / Intel" abaixo.

Com o [Git](https://git-scm.com/download/win):

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Sem o Git: nesta página clique em **Code → Download ZIP**, extraia, abra a pasta extraída
`voxcpm2-turkce-ses-tasarimi-main`, digite `powershell` na barra de endereços do Explorador de Arquivos e pressione Enter;
depois execute a última linha acima. O Git só é necessário para o caminho de compilação a partir do código-fonte.

`-ExecutionPolicy Bypass` vale só para este processo e não altera nenhuma configuração do sistema; leia `scripts\kur.ps1`
antes de executá-lo, como faria com qualquer script de instalação. Um comando, ~10 min, ~3,7 GB de download, tudo verificado por sha256: o modelo (2,95 GB), as DLLs de runtime do CUDA 12.8 como
zips portáteis (sem instalação no sistema, PATH intocado), o **motor pré-compilado** da página Releases, um `.venv` com os dois
pacotes Python, `ayarlar.json` e uma verificação final da GPU (`KONTROL_OK`). Execute de novo após qualquer falha; os arquivos
já verificados são pulados. Depois inicie a interface web: clique duas vezes em **`baslat.bat`** na pasta do repositório. Ele
inicia a interface e abre **http://127.0.0.1:8765/** no navegador quando estiver pronta; feche a janela preta (ou pressione Ctrl+C nela) para parar.
O mesmo pelo PowerShell:

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
depois abra **http://127.0.0.1:8765/** você mesmo (iniciada desta forma, a interface não abre o navegador; ela escuta só em
localhost).

> **O `audiocpp_cli.exe` do zip da release não foi feito para ser aberto com clique duplo.** É um motor de linha de comando que
> precisa das DLLs do CUDA e do modelo ao lado; o `kur.ps1` coloca tudo no lugar e o pacote Python o controla.
> Um clique duplo nele só mostra "cudart64_12.dll not found".

**GPUs suportadas (release v0.1.1):** código nativo para GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86), RTX 40xx
(sm_89) e RTX 50xx (sm_120a); qualquer outra GPU CUDA a partir de Pascal roda o PTX embutido via driver (primeira
inicialização mais lenta). Maxwell (GTX 9xx) e anteriores não são suportadas pelo CUDA 12.8. Testado por nós numa GTX 1050 Ti de 4 GB (também via Docker Desktop/WSL2 no Windows, só CLI); medido por @mslmyilmaz5 (#15): RTX 3060 Ti 8 GB, Ubuntu 24.04 Docker,
CUDA 12.8.1 (detalhes em [docs/linux.md](docs/linux.md)). Relatos de outras placas são bem-vindos nas [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (experimental):** um zip separado do motor Vulkan (`...-win64-vulkan.zip`, sem CUDA) é instalado com
`scripts\kur.ps1 -Kok C:\vox -Vulkan`. Ele foi verificado só na nossa placa NVIDIA pelo backend Vulkan (lá rodou mais devagar
que o CUDA, mas gerou o mesmo áudio para a mesma semente; essa medição foi feita enquanto o disco estava ocupado com outra
tarefa, então uma comparação limpa de velocidade ainda está pendente) e **não** o testamos nós mesmos em hardware AMD ou
Intel: se você testar, publique o resultado nas Discussions. Com mais de um dispositivo Vulkan (integrado + dedicado), o
instalador grava o índice da GPU dedicada como `cihaz` em `ayarlar.json`.

**Nota:** o suporte a Vulkan é experimental no momento. Ele foi compilado e testado com sucesso numa GTX 1050 Ti. Além disso, um usuário externo (mitra_tr) relatou tê-lo executado numa AMD 6900 XT. Ainda são necessários testes mais amplos em placas AMD/Intel.

### Alternativa: compilar o motor a partir do código-fonte

Requer o Visual Studio 2022 Build Tools com "Desktop development with C++" (incl. C++ CMake tools), ~7 GB. Depois:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Isso também baixa o nvcc, busca o código-fonte do audio.cpp v0.7.2, aplica `patches/0001-voxcpm2-4gb-ve-hiz.patch` e
compila para a sua GPU (`-Mimari native`, padrão; ou, por exemplo, `-Mimari 61`), ~15-25 min. Mantenha a raiz curta (`C:\vox`):
o nvcc falha com caminhos longos. Passo a passo com verificações: [AGENTS.md](AGENTS.md).

### Problemas comuns de instalação

| O que aparece | O que significa, o que fazer |
|---|---|
| `cudart64_12.dll not found` depois de clicar duas vezes no exe | O motor não foi feito para ser iniciado manualmente. Execute o comando `kur.ps1` acima e depois inicie a interface web. |
| `64-bit Python 3.10+ bulunamadı` (Python não encontrado) | Instale o Python (`winget install Python.Python.3.12`), feche o PowerShell, abra um novo e execute o mesmo comando de novo. |
| `motor ekran kartını görmedi` (o motor não viu a GPU) | Atualize o driver NVIDIA para a versão 570 ou mais recente; confira se o `nvidia-smi` funciona. |
| `indirme başarısız` / `sha256 tutmadı` (falha no download / checksum não confere) | Normalmente é um download interrompido. Execute o mesmo comando de novo; os arquivos já verificados são pulados. |
| Compilação: o `nvcc` falha | Mantenha a raiz da instalação curta (`-Kok C:\vox`). |
| A página não abre | Inicie a interface com `baslat.bat` ou abra http://127.0.0.1:8765/ você mesmo. Porta ocupada? Altere `"port"` em `ayarlar.json`. |

Problemas? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) ou uma
[issue de instalação](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
com a sua GPU, a versão do Windows, o comando e as últimas linhas da saída.

## Uso

Linha de comando:
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
Regras do texto: escreva os números por extenso, sem aspas (a ferramenta recusa dígitos e aspas), uma frase por linha,
≤ 2000 caracteres por linha. Pausa depois de uma linha: `|| bagli` 0,25 s, `|| normal` 0,5 s, `|| paragraf` 1 s, `|| agir` 1,5 s
ou uma duração sua, `|| 0,8` (0-5 s; os dígitos do marcador são permitidos). `ayarlar/okunus_sozlugu.tsv` corrige a pronúncia de palavras estrangeiras em textos em turco.
O idioma é detectado pelo texto (letras turcas, sistema de escrita, palavras comuns; o `dil` do cartão da voz em caso de dúvida; `--dil <code>` é opcional). Em textos que não são em turco, apóstrofos são permitidos, o dicionário turco
é ignorado e os dígitos continuam sendo recusados. Se uma leitura imprimir `speed gate: satır [...]`, ouça essas linhas.

### Interface web

Só local (127.0.0.1): `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → abra http://127.0.0.1:8765/ você mesmo
(outra porta: `--port 8800`) ou clique duas vezes em `baslat.bat`. Pare o servidor com Ctrl+C. Três abas: *Criar uma voz*,
*Ler com esta voz*, *Clonagem de voz*. O caminho de sempre: *Criar* → ouvir as variantes → *Adicionar à minha lista de leitura* →
*Ler com esta voz* → baixar. Ou escolha uma voz incluída no menu de vozes e leia.

- **Versão no cabeçalho.** Um `v0.2.0 · <short commit>` pequeno e discreto (com `+` quando arquivos rastreados têm alterações
  não commitadas; só a versão, sem git), para que capturas de tela e vídeos mostrem qual versão foi usada.
- **Duas vozes em cada cartão de variante.** Em cima, em cinza, a *Voz bruta do design*: ela é gerada uma vez e nunca sai
  igual de novo. Abaixo dela, numa moldura laranja, *↻ Esta é a voz que você vai ouvir sempre*: a gravação de design lida
  de volta como referência com a semente própria da variante (mostrada no cartão). É assim que a voz soa em todas as leituras seguintes.
  Embaixo ficam *Ler com esta voz* e *Adicionar à minha lista de leitura*. Um único clique em *Criar* faz as duas coisas: cria todas as
  variantes e depois lê o seu texto com cada voz permanente; uma só barra de progresso conta as duas fases. A pasta da variante
  recebe `dinleme.wav`. Se essa leitura parar antes do fim, o design é mantido e o cartão mostra um aviso.
- **A janela "Texto que você quer ouvir".** Em *Criar uma voz*, a caixa *↻ Texto que você quer ouvir* guarda o que cada voz
  permanente lê (se ficar vazia, é lida a frase de exemplo). Clicar nela abre o caderno de leitura numa janela: números de linha,
  menu de linha, faixas de pausa. *OK* grava o texto e as pausas de volta na caixa; *Cancelar* ou Esc não muda nada. A
  aba de leitura mantém o próprio texto.
- **O caderno de leitura.** Uma frase por linha. Clique no número de uma linha para abrir o menu de linha (mover para cima ou para baixo, mover para uma
  posição, duplicar, excluir; Alt+↑/↓, Alt+Shift+↓, ou arrastar pelo número; Ctrl+Z desfaz texto e pausas juntos).
  Clique na faixa fina entre duas linhas para escolher a pausa (bagli 0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, ou uma
  duração sua de 0-5 s com a engrenagem); pressione Enter duas vezes para um parágrafo (1 s), e linhas em branco viram faixas de pausa. Enquanto o resultado
  toca, a linha sendo lida se ilumina e rola até ficar visível; *▶ Ouvir a partir daqui* no menu de linha toca a partir daquela linha.
  O texto e as pausas sobrevivem a um recarregamento da página (armazenamento do navegador).
- **Rascunhos.** O botão *📄 Rascunhos* fica nos dois cadernos (aba de leitura e janela). Salve o texto atual com as
  pausas como rascunho, carregue um com um clique (Ctrl+Z desfaz) e use ⋯ para sobrescrever, renomear ou excluir. Os rascunhos ficam
  em `sesler/taslaklar.json`, nunca no repositório.
- **Lista de leitura e menu de vozes.** Num cartão de variante, *Adicionar à minha lista de leitura* abre uma caixa de nome: dê à variante
  um nome próprio e ✓ a adiciona. O *Nome da geração* continua valendo para todas as variantes daquela execução. Em *Ler com esta voz*, o botão de
  voz (bandeira + nome) abre o menu de vozes: *Minha lista de leitura* em cima, depois as vozes incluídas com bandeiras (primeiro as do idioma
  da interface). Cada linha tem ▶ ouvir (a voz permanente, quando existe), o coração (adicionar ou remover) e ⋯; ↑/↓ e
  Enter escolhem, Esc fecha, a última voz é lembrada. A lista fica em `sesler/okuma_listesi.json`, fora do
  repositório, e sobrevive a reinicializações.
- **Gerenciar vozes.** O menu ⋯ (linha do menu de vozes ou cartão de variante) tem *Ler com esta voz*, adicionar à lista ou remover dela,
  *Renomear* (um nome vazio restaura o original; *Voltar ao nome original*), *Excluir* para vozes criadas e *Ocultar*
  para as incluídas; ambos pedem confirmação antes. Uma voz excluída vai para `sesler/_cop/`; ocultar nunca mexe nos arquivos do repositório.
  *Vozes ocultas e excluídas (N)*, no fim do menu de vozes, tem *Restaurar*. Nomes personalizados e vozes ocultas ficam guardados
  em `sesler/yerel_katman.json`. Uma voz renomeada mostra a origem em cinza (*nome da geração · variante N*); ⋯ → *Ir para a
  geração* abre o design dela.
- **Atalhos e arquivos.** Ctrl+Enter (⌘+Enter no Mac) inicia *Criar* ou *Ler com esta voz* na aba aberta. A
  barra de progresso mostra *decorrido / ~total*, com uma estimativa aprendida com trabalhos anteriores na sua máquina. O download recebe o nome
  da voz e do horário (`Voice_Name_2026-11-02_0152.wav`).

**Clonagem de voz (a sua própria ou uma voz autorizada).** Na aba *Clonagem de voz* da interface, forneça a sua gravação (wav/mp3/flac/ogg; recomendam-se 5-30 s de fala limpa; abaixo de 3 s é recusada, acima de 36 s é cortada), a transcrição exata dela e o texto a ser lido. O botão fica desativado até você marcar "Esta voz é minha ou tenho autorização explícita do dono". A gravação vai apenas para o servidor local (127.0.0.1), é processada numa pasta temporária junto com a sua codificação de referência, e essa pasta é apagada quando o trabalho termina, inclusive quando ele falha; nada é enviado pela rede. Só a saída sintética é mantida (interface: `sesler/_okumalar/<job>/`, CLI: `--cikti`). A saída é `klon_synthetic.wav`, com a marcação "synthetic"; identifique-a como gerada por IA ao compartilhar. CLI: `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## Perguntas frequentes

**Modelo ou motor? O que é o quê?** O VoxCPM2 (OpenBMB) é o *modelo*: a rede de 2 bilhões de parâmetros que transforma texto
em fala. O audio.cpp é o *motor*: o programa em C++/CUDA que roda o modelo na sua GPU (`audiocpp_cli.exe`). O nosso
patch altera o motor, não o modelo: ele faz o VoxCPM2 caber em 4 GB e faz a mesma semente gerar o mesmo áudio
sempre. O pacote Python deste repositório só prepara o texto, chama o motor e reúne os arquivos.

**Quais GPUs?** Veja "GPUs suportadas" acima: NVIDIA a partir da GTX 10xx, 4 GB de VRAM ou mais, driver ≥ 570. A release traz
código nativo para sm_61/75/86/89/120a; outras placas Pascal ou mais novas usam o PTX embutido (primeira inicialização mais lenta). AMD/Intel:
zip Vulkan experimental, `kur.ps1 -Vulkan`; um usuário externo relatou tê-lo executado numa AMD 6900 XT, mas ainda são necessários testes
mais amplos em AMD/Intel (veja "AMD / Intel" acima). Só CPU (`"backend": "cpu"` em `ayarlar.json`) funciona, mas é
~6× mais lento que uma GTX 1050 Ti (medição do motor, 535 s contra 94 s para 48 s de fala); não é um caminho suportado.

**Qual a velocidade?** Medido numa GTX 1050 Ti 4 GB (i7-7700HQ): uma variante de design (gravação de ≈ 25 s) 55 s; leitura ≈ 2 s de
processamento por 1 s de fala (fator de tempo real 1,9-2,8) após uma codificação de referência única de ~50 s por voz (em cache no
disco) e 10-20 s de carregamento do modelo por lote; pico de VRAM 2,6-2,9 GB. Placas mais novas são mais rápidas; números e método:
[docs/4gb.md](docs/4gb.md).

**Dá para clonar uma voz?** O modelo VoxCPM2 por trás consegue imitar uma voz a partir de uma gravação de referência, e a seção de
clonagem usa isso. Use apenas com a sua própria voz ou com a permissão explícita da pessoa dona da voz; a
interface pede que você confirme essa permissão. O design de voz não precisa de gravação: ele parte de uma descrição em texto em inglês ou chinês, e
a "referência" usada para ler uma voz criada é a gravação de design sintética do próprio modelo. Passar-se por outra pessoa, fraude
e engano são proibidos. Veja [ETHICS.md](ETHICS.md). Identifique o que você publicar como gerado por IA.

**Como escrever uma boa descrição de voz?** Em inglês, 1-3 frases: idade e gênero, timbre (grave/brilhante, caloroso,
nasal, rouco), tom e papel (narrador de documentário tranquilo, apresentador enérgico), andamento (lento, pausado) e
"clean studio recording, no background noise". Mantenha como descrição, não como roteiro; sem parênteses. Peça 3-5
variantes e ouça: a semente muda muito a voz. Para o texto de criação, use 1-2 frases naturais no idioma da voz, no
clima que você quer (no máximo ~20 s de fala). Na leitura, uma frase por linha; divida frases longas e escreva os números por extenso.

## Como contribuir

Não sabe por onde começar? Estas quatro issues pequenas são um bom primeiro passo:

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Teste na sua GPU e informe a placa, o driver e os tempos
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel: teste a build Vulkan experimental
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Adicione uma frase ao conjunto de teste
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Compartilhe uma voz que você criou, com a descrição e a semente

Conjunto de teste compartilhado: [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt); guia de voz de marca:
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md); como enviar código: [CONTRIBUTING.md](CONTRIBUTING.md).
Problemas de instalação: [formulário de issue](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml); perguntas e resultados: [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Todos os que participam seguem o [Código de Conduta](CODE_OF_CONDUCT.md): seja gentil e mantenha o feedback focado no trabalho.

## Colaboradores

- [@alexturkey](https://github.com/alexturkey): mantenedor; código, vozes incluídas, documentação
- [@cayir21](https://github.com/cayir21): suporte a Metal no macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis): correção de fim de frase (EOS) para leitura de várias frases no backend de CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)

O seu nome também tem lugar aqui: um resultado de teste da sua GPU, uma frase para o conjunto de teste, uma voz que você criou, um
relato de bug claro ou um pull request, tudo conta como contribuição. Obrigado a todos que testam e dão retorno.

## Licença e créditos

Código e vozes incluídas: Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Baseado no VoxCPM2 (OpenBMB, Apache-2.0),
no audio.cpp (ShugoAI LLC, Apache-2.0) e na conversão GGUF do audio.cpp. Lista completa: [THIRD_PARTY.md](THIRD_PARTY.md).
Sem vínculo com a OpenBMB, a ModelBest ou o projeto audio.cpp.

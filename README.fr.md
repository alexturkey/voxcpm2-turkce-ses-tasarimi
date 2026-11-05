[Türkçe](README.tr.md) · [English](README.md) · [Deutsch](README.de.md) · **Français** · [Español](README.es.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [Polski](README.pl.md) · [Nederlands](README.nl.md) · [Dansk](README.da.md) · [Norsk](README.nb.md) · [Svenska](README.sv.md) · [Suomi](README.fi.md) · [Ελληνικά](README.el.md) · [العربية](README.ar.md) · [עברית](README.he.md) · [हिन्दी](README.hi.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [ไทย](README.th.md) · [Tiếng Việt](README.vi.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tagalog](README.tl.md) · [မြန်မာ](README.my.md) · [ខ្មែរ](README.km.md) · [ລາວ](README.lo.md) · [Kiswahili](README.sw.md)

# voxcpm2-turkce-ses-tasarimi

**Conception de voix en turc avec VoxCPM2 sur un GPU de 4 Go.** Décrivez une voix en anglais, laissez le modèle la
créer, choisissez la variante qui vous plaît, puis lisez n'importe quel texte turc avec cette voix. Le projet comprend
un installateur en une seule commande, un moteur [audio.cpp](https://github.com/0xShug0/audio.cpp) patché qui tient sur
une GTX 1050 Ti (4 Go), une petite interface web locale et quatorze voix synthétiques prêtes à l'emploi : sept voix
turques et sept narrateurs natifs en anglais, français, allemand, espagnol, russe, chinois et japonais.

- L'application lit dans 30 langues ; l'interface existe elle aussi en 30 langues.
- 14 voix prêtes à l'emploi : 7 turques, plus une en anglais, en français, en allemand, en espagnol, en russe, en chinois et en japonais.
- Interface web (v0.2.0) : chaque carte de variante porte deux voix, la voix brute de conception et la voix que vous
  entendrez toujours ; une liste de lecture avec un menu des voix ; renommer, masquer ou supprimer des voix ; des
  brouillons pour les textes que vous lisez. Voir « Interface web » dans « Utilisation ».

[Comment tout tient en 4 Go](docs/4gb.md) · [Ubuntu / Linux](docs/linux.md) · [macOS](docs/mac.md) · [Guide d'installation pour agents IA](AGENTS.md) · [Usage responsable](ETHICS.md)

> Les voix fournies sont synthétiques, conçues à partir d'une description textuelle. La partie clonage de voix est
> réservée à votre propre voix ou à une voix utilisée avec l'autorisation explicite de son propriétaire ; l'interface
> vous demande de confirmer cette autorisation. L'usurpation d'identité, la fraude et la tromperie sont interdites.
> Signalez ce que vous générez comme produit par une IA. Voir [ETHICS.md](ETHICS.md).

## 30 langues

Nous avons réalisé un documentaire vidéo sur la Cappadoce en 8 langues : turc, anglais, français, allemand, espagnol,
russe, chinois et japonais. Chaque langue a son propre **narrateur natif**, conçu avec VoxCPM2 à partir d'une
description en anglais. Le tout a été généré entièrement en local sur une GTX 1050 Ti de 4 Go, avec la même qualité
fixe (16 étapes, cfg 2.0). Les sept narrateurs sont fournis ici, avec leur prompt, leur texte de conception, leur
graine et leur enregistrement de référence.

| Code | Langue | Voix | Écouter | Vidéo |
|---|---|---|---|---|
| `tr` | Turc | `hazir/belgesel_hanim` (et 6 autres) | [extrait](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) | |
| `en` | Anglais | `hazir/anlatici_en` | [extrait](hazir_sesler/anlatici_en/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113791986763440439) |
| `fr` | Français | `hazir/anlatici_fr` | [extrait](hazir_sesler/anlatici_fr/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113790681575804962) |
| `de` | Allemand | `hazir/anlatici_de` | [extrait](hazir_sesler/anlatici_de/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113791351645262249) |
| `es` | Espagnol | `hazir/anlatici_es` | [extrait](hazir_sesler/anlatici_es/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113807365611122705) |
| `ru` | Russe | `hazir/anlatici_ru` | [extrait](hazir_sesler/anlatici_ru/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113801574136848884) |
| `zh` | Chinois (mandarin) | `hazir/anlatici_zh` | [extrait](hazir_sesler/anlatici_zh/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113802229606121794) |
| `ja` | Japonais | `hazir/anlatici_ja` | [extrait](hazir_sesler/anlatici_ja/ornek_okuma.mp3) | [vidéo](https://x.com/i/status/2113800742100176923) |

```powershell
# the language is detected from the text (voice card if unsure); --dil is optional
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_fr --metin @hazir_sesler/anlatici_fr/ornek_okuma_metni.txt --cikti cikti\fr
.venv\Scripts\python.exe -m ses_tasarim.oku --ses hazir/anlatici_ja --metin @text_ja.txt --cikti cikti\ja
# design a voice in another language: English prompt, design text in that language
.venv\Scripts\python.exe -m ses_tasarim.tasarla --ad narrator_es --dil es --cesit 3 --tarif "A deep-voiced Spanish man ..." --metin @texto.txt
```

**Pourquoi phrase par phrase.** VoxCPM2 n'est pas stable sur une seule génération longue (au-delà d'environ
30 secondes) : le rythme s'accélère et la voix peut dériver. Ici, la voix est portée par un enregistrement de référence
et une graine fixes, et un texte long est lu à raison d'une phrase par ligne : le timbre et le style restent identiques
de la première à la dernière phrase. Pour les langues autres que le turc, le dictionnaire de prononciation turc n'est
pas appliqué. Les 30 langues prises en charge par VoxCPM2 ont toutes été testées et fonctionnent ; pour celles qui n'ont
pas de voix fournie, utilisez `--dil <code>`. Commandes par langue et leçons que nous en avons tirées :
[docs/cok_dilli.md](docs/cok_dilli.md). Skill Claude Code pour tout le processus de conception :
[.claude/skills/ses-tasarimi/SKILL.md](.claude/skills/ses-tasarimi/SKILL.md).

**144 prompts d'exemple pour démarrer.** 18 rôles (narrateur de documentaire, présentateur de journal télévisé, voix
publicitaire, livre audio, grand-mère conteuse, animateur de podcast, enseignant, bande-annonce de film, guide de
méditation, commentateur sportif et d'autres, en version homme et femme) dans chacune des 8 langues. Le prompt est en
anglais et précise la nationalité et l'accent natif du locuteur ; le texte lu pendant la création de la voix est fourni
avec, dans la langue concernée et adapté au rôle. Choisissez-en un, écoutez les variantes, gardez celle qui vous plaît :
`python -m ses_tasarim.tasarla --ornek fr_sesli_kitap_kadin --cesit 3`, ou choisissez *Modèle d'exemple* dans
l'interface web. Liste complète : [docs/ornek_tarifler.md](docs/ornek_tarifler.md).

**Doublez vos vidéos avec votre propre voix.** [DubWorld](https://github.com/alexturkey/dubworld) est notre logiciel
local de doublage vidéo ; il installe ce dépôt comme moteur vocal VoxCPM2. Une voix conçue ici s'y utilise avec
`ses.voxcpm2_ses = "<name>/<variant>"`.

## Démarrage rapide (Windows, 3 étapes)

1. **Téléchargez** le code : [voxcpm2-turkce-ses-tasarimi-main.zip](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/archive/refs/heads/main.zip).
   Le paquet moteur prêt à l'emploi adapté à votre carte est récupéré par l'installateur à l'étape 3 :
   NVIDIA → [paquet CUDA](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.0/voxcpm2-turkce-ses-tasarimi-motor-v0.3.0-win64-cuda12.8.zip),
   AMD / Intel → [paquet Vulkan, expérimental](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan.zip)
   (vous en avez déjà téléchargé un ? ajoutez `-HazirZip <path to the zip>` à la commande ci-dessous).
2. **Décompressez** le zip, ouvrez le dossier `voxcpm2-turkce-ses-tasarimi-main`, tapez `powershell` dans la barre
   d'adresse de l'Explorateur et appuyez sur Entrée.
3. **Lancez** l'installateur (Python 3.10-3.13 64 bits requis ; pilote NVIDIA ≥ 570 pour CUDA), puis double-cliquez sur **`baslat.bat`** :
   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
   ```
   AMD / Intel : ajoutez `-Vulkan` à la fin. L'interface s'ouvre sur http://127.0.0.1:8765/.

Le zip du moteur n'est pas une application autonome (son exe a besoin du modèle et des DLL que l'installateur met en
place). Détails, liste des GPU et problèmes courants : « Installation rapide » plus bas.

## Ubuntu / Linux (NVIDIA CUDA, expérimental)

Compilez le moteur patché avec `bash scripts/kur-linux.sh`, ou utilisez `Dockerfile.linux` pour compiler et exécuter
dans un environnement Ubuntu 24.04 / CUDA 12.8.1. Il faut un GPU NVIDIA et un pilote compatible ; l'installateur natif
requiert en plus le CUDA Toolkit et Python 3.10-3.13. L'interface reste limitée au loopback, y compris sur un serveur
distant (redirection SSH). Prérequis, commandes, choix de l'architecture et périmètre de validation :
[docs/linux.md](docs/linux.md).

## Démarrage rapide (macOS, Apple Silicon)

Nécessite les Xcode Command Line Tools (`xcode-select --install`) et [Homebrew](https://brew.sh) :
```bash
brew install cmake python@3.12
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
bash scripts/kur.sh
```
L'installateur télécharge le modèle, compile le moteur patché avec Metal (~1 min) et installe le tout dans `~/vox`.
Double-cliquez ensuite sur **`baslat.command`**. Sur un MacBook Air M4 16 Go : ~2 s de calcul pour 1 s de parole, la
même graine donne un audio identique à l'octet près, pic d'environ 5,3 Go de RAM, aucun ralentissement thermique sur
12 min de lecture continue. Détails et mesures : [docs/mac.md](docs/mac.md).

**Application Mac native (sans Python, Homebrew ni Terminal) :** [macos/README.md](macos/README.md). Elle embarque le
même moteur patché et télécharge le modèle au premier lancement ; pour l'instant, elle se compile depuis les sources
avec Xcode.

## Pour les utilisateurs de Mac (Apple Silicon)

Il existe aussi une adaptation indépendante, réalisée par la communauté, pour les Mac Apple Silicon, qui exécute
VoxCPM2 avec le framework MLX d'Apple : **[emre-koc/voxcpm2-turkce-ses-tasarimi-mlx](https://github.com/emre-koc/voxcpm2-turkce-ses-tasarimi-mlx)**.
Elle est développée et maintenue par Emre Koç ([@emre-koc](https://github.com/emre-koc)) dans son propre dépôt, et non
ici ; les étapes d'installation et les questions d'assistance se posent là-bas. Merci, Emre, d'avoir porté ce projet
sur Mac !

## Fonctionnement

1. **Conception de la voix.** Une *description de la voix* en anglais + un *texte lu pendant la création de la voix*
   (dans la langue de la voix) + un nombre de variantes. Chaque variante reçoit sa propre graine ; le moteur reçoit
   `(description)text` et renvoie un enregistrement de conception par graine. Le texte est un court échantillon pour
   découvrir la voix : 1 à 3 phrases, ~30 s au maximum (l'interface affiche l'estimation et refuse de démarrer
   au-delà de 33 s) ; un texte long relève de l'étape 2.
2. **Lecture fondée sur la référence.** L'enregistrement de conception est transmis aux **deux** entrées du moteur
   (`audio` et `voice_ref`), avec sa transcription (`reference_text`) et le nouveau texte à lire, avec la même graine.
   La voix est portée par l'enregistrement, et non par la description : elle ne dérive donc pas d'un texte à l'autre.
   Le texte est lu phrase par phrase.
3. La qualité est fixe : 16 étapes de diffusion, CFG 2.0. La graine n'est pas un réglage de qualité.
4. **Minutage des mots, même audio à chaque fois.** Pendant la lecture, le moteur indique lui-même où chaque mot commence et finit (patch 0002, aucun modèle supplémentaire). Les temps sont écrits dans `kelimeler.json` et les lignes sont rognées pour que l'écart entre deux lignes soit égal au réglage de pause. Précision par rapport à l'alignement forcé CTC (forced alignment, CTC = 100 %) : 89,66 % (turc, 12 voix ; réglage `kelime_zamani`, activé par défaut). Avec le patch 0003, la même graine donne un audio identique à l'octet près à chaque exécution.

L'enregistrement de conception brut est un échantillon unique de la voix ; aucune lecture ultérieure ne sonne
exactement pareil. Ce que vous entendez dans chaque lecture ultérieure, c'est l'étape 2 : l'enregistrement de
conception comme référence, plus la graine propre à la variante. C'est pourquoi l'interface web enchaîne l'étape 2 juste
après la conception et affiche les deux sur la carte de variante.

Le moteur est audio.cpp v0.7.2 avec notre patch (`patches/`), le modèle est VoxCPM2 Q8_0 GGUF. Pic de VRAM ≈ 2,8 Go ;
environ 2 s de calcul pour 1 s de parole sur une GTX 1050 Ti. Détails et mesures : [docs/4gb.md](docs/4gb.md).

## Voix fournies (`hazir_sesler/`)

Les quatorze voix ont été conçues à partir des prompts stockés dans leur `ses.json` ; aucune n'a été clonée à partir
d'un enregistrement (le clonage se fait dans l'onglet distinct *Clonage de voix*, soumis à consentement).

| Voix | Description courte | Écouter |
|---|---|---|
| `belgesel_hanim` | Femme mûre d'une cinquantaine d'années, alto grave et chaleureux ; narratrice de documentaire posée | [extrait](hazir_sesler/belgesel_hanim/ornek_okuma.mp3) · [référence](hazir_sesler/belgesel_hanim/referans.flac) |
| `gizemli_bilge` | Narrateur masculin grave, puissant, mystérieux | [extrait](hazir_sesler/gizemli_bilge/ornek_okuma.mp3) · [référence](hazir_sesler/gizemli_bilge/referans.flac) |
| `haber_spikeri` | Présentateur de journal chevronné, autour de soixante-dix ans, calme et faisant autorité | [extrait](hazir_sesler/haber_spikeri/ornek_okuma.mp3) · [référence](hazir_sesler/haber_spikeri/referans.flac) |
| `cekici_spiker` | Présentatrice charismatique du journal du soir, la trentaine, voix veloutée et expressive | [extrait](hazir_sesler/cekici_spiker/ornek_okuma.mp3) · [référence](hazir_sesler/cekici_spiker/referans.flac) |
| `masal_cadisi` | Sorcière de conte : grave, légèrement nasale, d'une douceur rusée | [extrait](hazir_sesler/masal_cadisi/ornek_okuma.mp3) · [référence](hazir_sesler/masal_cadisi/referans.flac) |
| `tok_anlatici` | Narrateur masculin exceptionnellement grave, dense et imposant | [extrait](hazir_sesler/tok_anlatici/ornek_okuma.mp3) · [référence](hazir_sesler/tok_anlatici/referans.flac) |
| `yasli_bilge` | Vieux sage, voix grave et tonitruante, un peu mystérieuse | [extrait](hazir_sesler/yasli_bilge/ornek_okuma.mp3) · [référence](hazir_sesler/yasli_bilge/referans.flac) |
| `anlatici_en` | Narrateur de documentaire anglophone natif, la cinquantaine (General American) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_en/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_en/referans.flac) |
| `anlatici_fr` | Narrateur de documentaire francophone natif, la cinquantaine (parisien) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_fr/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_fr/referans.flac) |
| `anlatici_de` | Narrateur de documentaire germanophone natif, la cinquantaine (Hochdeutsch) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_de/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_de/referans.flac) |
| `anlatici_es` | Narrateur de documentaire hispanophone natif, la cinquantaine (castillan (Madrid)) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_es/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_es/referans.flac) |
| `anlatici_ru` | Narrateur de documentaire russophone natif, la cinquantaine (Moscou) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_ru/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_ru/referans.flac) |
| `anlatici_zh` | Narrateur de documentaire sinophone natif (mandarin), la cinquantaine (putonghua de Pékin) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_zh/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_zh/referans.flac) |
| `anlatici_ja` | Narrateur de documentaire japonophone natif, la cinquantaine (japonais standard de Tokyo) ; grave, calme, chaleureux | [extrait](hazir_sesler/anlatici_ja/ornek_okuma.mp3) · [référence](hazir_sesler/anlatici_ja/referans.flac) |

Chaque dossier contient : `referans.flac` (enregistrement de conception sans perte), `ses.json` (prompt, transcription,
graine de conception, graine de lecture, description ; `dil` = langue, pour les narrateurs), `ornek_okuma.mp3` (+ son
texte). Utilisez-les directement : `--ses hazir/<name>`. Les enregistrements de référence des narrateurs sont courts
(5,6 à 10 s) ; leurs extraits sont les trois premières phrases du script sur la Cappadoce, découpées dans la lecture
complète de la production.

## Installation rapide, sans compilateur (Windows 10/11, GPU NVIDIA ≥ 4 Go)

Prérequis : pilote NVIDIA ≥ 570 et Python 3.10-3.13 64 bits (`winget install Python.Python.3.12`). Rien d'autre : ni
Visual Studio, ni installateur CUDA. Vous ne savez pas quelle carte vous avez ? Lancez `nvidia-smi` dans PowerShell :
la commande affiche le nom du GPU, la version du pilote et la mémoire. Pas de carte NVIDIA ? Voir « AMD / Intel »
plus bas.

Avec [Git](https://git-scm.com/download/win) :

```powershell
git clone https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi.git
cd voxcpm2-turkce-ses-tasarimi
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox
```

Sans Git : sur cette page, cliquez sur **Code → Download ZIP**, décompressez l'archive, ouvrez le dossier extrait
`voxcpm2-turkce-ses-tasarimi-main`, tapez `powershell` dans la barre d'adresse de l'Explorateur et appuyez sur Entrée,
puis lancez la dernière ligne ci-dessus. Git n'est nécessaire que pour la compilation depuis les sources.

`-ExecutionPolicy Bypass` ne s'applique qu'à ce seul processus et ne modifie aucun réglage système ; lisez
`scripts\kur.ps1` avant de l'exécuter, comme pour tout script d'installation. Une commande, ~10 min, ~3,7 Go à
télécharger, tout vérifié par sha256 : le modèle (2,95 Go), les DLL d'exécution CUDA 12.8 sous forme de zips portables
(aucune installation système, PATH intact), le **moteur précompilé** depuis la page Releases, un `.venv` avec les deux
paquets Python, `ayarlar.json` et une vérification finale du GPU (`KONTROL_OK`). En cas d'échec, relancez-la : les
fichiers déjà vérifiés sont ignorés. Démarrez ensuite l'interface web : double-cliquez sur **`baslat.bat`** dans le
dossier du dépôt. Il lance l'interface et ouvre **http://127.0.0.1:8765/** dans votre navigateur dès qu'elle est
prête ; fermez la fenêtre noire (ou appuyez sur Ctrl+C dans celle-ci) pour l'arrêter. La même chose depuis PowerShell :

```powershell
.venv\Scripts\python.exe -m ses_tasarim.arayuz
```
puis ouvrez vous-même **http://127.0.0.1:8765/** (lancée ainsi, l'interface n'ouvre pas le navigateur ; elle n'écoute
que sur localhost).

> **Le `audiocpp_cli.exe` du zip de la release n'est pas fait pour être lancé d'un double-clic.** C'est un moteur en
> ligne de commande qui a besoin des DLL CUDA et du modèle à côté de lui ; `kur.ps1` met tout en place et le paquet
> Python le pilote. Un double-clic affiche seulement « cudart64_12.dll not found ».

**GPU pris en charge (release v0.1.1) :** code natif pour les GTX 10xx (sm_61), RTX 20xx (sm_75), RTX 30xx (sm_86),
RTX 40xx (sm_89) et RTX 50xx (sm_120a) ; tout autre GPU CUDA à partir de Pascal exécute le PTX embarqué via le pilote
(premier démarrage plus lent). Maxwell (GTX 9xx) et les générations antérieures ne sont pas prises en charge par
CUDA 12.8. Testé par nos soins sur une GTX 1050 Ti 4 Go (également via Docker Desktop/WSL2 sous Windows, en CLI
uniquement) ; mesuré par @mslmyilmaz5 (#15) : RTX 3060 Ti 8 Go, Ubuntu 24.04 Docker, CUDA 12.8.1 (détails dans
[docs/linux.md](docs/linux.md)). Les retours sur d'autres cartes sont les bienvenus dans les
[Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).

**AMD / Intel (expérimental) :** un moteur Vulkan séparé (sans CUDA) s'installe avec `scripts\kur.ps1 -Kok C:\vox -Vulkan`. Nous l'avons testé sur notre carte NVIDIA via le backend Vulkan (plus lent que CUDA, même audio pour la même graine ; une comparaison de vitesse propre reste à faire) et sur la puce graphique intégrée Intel HD Graphics 630 (environ 35-50 s de calcul pour 1 s de parole) ; nous ne l'avons **pas** testé nous-mêmes sur AMD : si vous l'essayez, publiez le résultat dans Discussions. Avec plusieurs périphériques Vulkan (intégré + dédié), l'installateur écrit l'indice du GPU dédié comme `cihaz` dans `ayarlar.json`.

*Remarque : la prise en charge de Vulkan est pour l'instant expérimentale. Elle a été compilée et testée avec succès sur
une GTX 1050 Ti. Un utilisateur externe (mitra_tr) a par ailleurs signalé l'avoir fait fonctionner sur une AMD 6900 XT.
Des tests plus larges sur les cartes AMD/Intel restent nécessaires.*

**Test de la communauté (AMD) :** @mitraTR a fait tourner la v0.1.1 avec Vulkan sur une AMD Radeon RX 6900 XT sous Windows 11 : installation, création de voix, lecture, interface web et tests ont tous fonctionné ; la lecture a demandé environ 0,8-0,9 s de calcul par seconde de parole ([rapport dans #6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6#issuecomment-6581393655)). Installez dans un dossier court dont le chemin ne contient que des caractères ASCII (par ex. `C:\vox`) : sous Windows, le moteur ne peut pas ouvrir les chemins contenant des accents ou d'autres caractères non ASCII. Tous les rapports à ce jour : [matériel testé](docs/donanim_testleri.md).

**Notes sur Vulkan :** depuis le moteur v0.3.1, l'horodatage des mots fonctionne aussi sous Vulkan. Deux paquets : `vulkan` demande un processeur AVX2 (la plupart des Intel Core depuis 2013, AMD depuis 2015 ; beaucoup de Pentium/Celeron ne l'ont pas) ; [`vulkan-uyumlu`](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/releases/download/v0.3.1/voxcpm2-turkce-ses-tasarimi-motor-v0.3.1-win64-vulkan-uyumlu.zip) fonctionne sur tout processeur x86 64 bits, mais la première lecture d'une voix prend environ 2,2 fois plus de temps (les lectures suivantes vont à la même vitesse). `kur.ps1 -Vulkan` vérifie le processeur et choisit le paquet lui-même. Avec une puce graphique intégrée, le moteur utilise environ 8 Go de RAM pendant la lecture. Le premier démarrage sous Vulkan peut prendre quelques minutes, le temps de compiler les shaders du GPU ; les lectures suivantes sont plus rapides. Détails : [docs/vulkan.md](docs/vulkan.md).

### Alternative : compiler le moteur depuis les sources

Nécessite les Build Tools de Visual Studio 2022 avec « Développement Desktop en C++ » (y compris les outils C++ CMake),
~7 Go. Ensuite :

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\kur.ps1 -Kok C:\vox -Derle
```
Cette commande télécharge aussi nvcc, récupère les sources d'audio.cpp v0.7.2, applique
`patches/0001-voxcpm2-4gb-ve-hiz.patch` et compile pour votre GPU (`-Mimari native`, par défaut ; ou par exemple
`-Mimari 61`), ~15 à 25 min. Gardez une racine courte (`C:\vox`) : nvcc échoue sur les chemins longs. Pas à pas, avec
vérifications : [AGENTS.md](AGENTS.md).

### Problèmes d'installation courants

| Vous voyez | Ce que cela signifie, que faire |
|---|---|
| `cudart64_12.dll not found` après un double-clic sur l'exe | Le moteur n'est pas fait pour être lancé à la main. Exécutez la commande `kur.ps1` ci-dessus, puis démarrez l'interface web. |
| `64-bit Python 3.10+ bulunamadı` (Python introuvable) | Installez Python (`winget install Python.Python.3.12`), fermez PowerShell, ouvrez-en un nouveau et relancez la même commande. |
| `motor ekran kartını görmedi` (le moteur n'a pas vu le GPU) | Mettez à jour le pilote NVIDIA en version 570 ou ultérieure ; vérifiez que `nvidia-smi` fonctionne. |
| `indirme başarısız` / `sha256 tutmadı` (échec du téléchargement / somme de contrôle incorrecte) | En général un téléchargement interrompu. Relancez la même commande ; les fichiers déjà vérifiés sont ignorés. |
| Compilation depuis les sources : `nvcc` échoue | Gardez une racine d'installation courte (`-Kok C:\vox`). |
| La page ne s'ouvre pas | Démarrez l'interface avec `baslat.bat`, ou ouvrez vous-même http://127.0.0.1:8765/. Port occupé ? Modifiez `"port"` dans `ayarlar.json`. |

Un problème ? [Discussions (Q&A)](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions) ou un
[ticket d'installation](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml)
avec votre GPU, votre version de Windows, la commande et ses dernières lignes.

## Utilisation

En ligne de commande :
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
Règles du texte : écrivez les nombres en toutes lettres, sans guillemets (l'outil refuse les chiffres et les
guillemets), une phrase par ligne, ≤ 2000 caractères par ligne. Pause après une ligne : `|| bagli` 0,25 s, `|| normal`
0,5 s, `|| paragraf` 1 s, `|| agir` 1,5 s ou votre propre durée `|| 0,8` (0 à 5 s ; les chiffres du marqueur sont
autorisés). `ayarlar/okunus_sozlugu.tsv` corrige la prononciation des mots étrangers dans un texte turc. La langue est
détectée à partir du texte (lettres turques, écriture, mots courants ; le `dil` de la fiche de la voix en cas de doute ;
`--dil <code>` est facultatif). Pour un texte non turc, les apostrophes y sont autorisées, le dictionnaire turc est
ignoré, les chiffres restent refusés. Si une lecture affiche `speed gate: satır [...]`, écoutez ces lignes.

### Interface web

En local uniquement (127.0.0.1) : `.venv\Scripts\python.exe -m ses_tasarim.arayuz` → ouvrez vous-même
http://127.0.0.1:8765/ (autre port : `--port 8800`), ou double-cliquez sur `baslat.bat`. Arrêtez le serveur avec
Ctrl+C. Trois onglets : *Créer une voix*, *Lire avec cette voix*, *Clonage de voix*. Le parcours habituel : *Créer* →
écouter les variantes → *Ajouter à ma liste de lecture* → *Lire avec cette voix* → télécharger. Ou choisissez une voix
fournie dans le menu des voix et lancez la lecture.

- **Version dans l'en-tête.** Un petit `v0.2.0 · <short commit>` discret (avec `+` lorsque des fichiers suivis ont des
  modifications non commitées ; la version seule sans git), pour que les captures d'écran et les vidéos montrent quelle
  version a été utilisée.
- **Deux voix sur chaque carte de variante.** En haut, en gris, la *Voix brute de conception* : elle est générée une
  seule fois et ne ressort jamais à l'identique. En dessous, dans un cadre orange, *↻ C'est la voix que vous entendrez
  toujours* : l'enregistrement de conception relu comme référence avec la graine propre à la variante (affichée sur la
  carte). C'est ainsi que la voix sonnera dans chaque lecture ultérieure. En dessous se trouvent *Lire avec cette voix*
  et *Ajouter à ma liste de lecture*. Un seul appui sur *Créer* fait les deux : chaque variante est conçue, puis votre
  texte est lu avec chaque voix durable ; une seule barre de progression compte les deux phases. Le dossier de la
  variante reçoit `dinleme.wav`. Si cette lecture s'arrête prématurément, la conception est conservée et la carte
  affiche une note.
- **La fenêtre « Texte que vous voulez entendre ».** Dans *Créer une voix*, la case *↻ Texte que vous voulez entendre*
  contient ce que lit chaque voix durable (laissée vide, c'est la phrase d'exemple qui est lue). Un clic dessus ouvre le
  carnet de lecture dans une fenêtre : numéros de ligne, menu de ligne, bandes de pause. *OK* réécrit le texte et ses
  pauses dans la case ; *Annuler* ou Échap ne change rien. L'onglet de lecture garde son propre texte.
- **Le carnet de lecture.** Une phrase par ligne. Cliquez sur un numéro de ligne pour ouvrir le menu de ligne (monter
  ou descendre, déplacer à une position, dupliquer, supprimer ; Alt+↑/↓, Alt+Maj+↓, ou glisser par le numéro ; Ctrl+Z
  annule à la fois le texte et les pauses). Cliquez sur la fine bande entre deux lignes pour choisir la pause (bagli
  0,25 · normal 0,5 · paragraf 1 · agir 1,5 s, ou votre propre durée de 0 à 5 s avec la roue dentée) ; appuyez deux
  fois sur Entrée pour un paragraphe (1 s), et les lignes vides deviennent des bandes de pause. Pendant la lecture du
  résultat, la ligne en cours s'illumine et défile dans la vue ; *▶ Écouter à partir d'ici* dans le menu de ligne lance
  la lecture depuis cette ligne. Le texte et ses pauses survivent à un rechargement de la page (stockage du navigateur).
- **Brouillons.** Le bouton *📄 Brouillons* figure dans les deux carnets (onglet de lecture et fenêtre). Enregistrez le
  texte en cours avec ses pauses comme brouillon, chargez-en un d'un clic (Ctrl+Z annule) et utilisez ⋯ pour
  l'écraser, le renommer ou le supprimer. Les brouillons sont stockés dans `sesler/taslaklar.json`, jamais dans le
  dépôt.
- **Liste de lecture et menu des voix.** Sur une carte de variante, *Ajouter à ma liste de lecture* ouvre un champ de
  nom : donnez un nom propre à la variante et ✓ l'ajoute. Le *Nom de la génération* reste sur chaque variante de cette
  exécution. Dans *Lire avec cette voix*, le bouton de voix (drapeau + nom) ouvre le menu des voix : *Ma liste de
  lecture* en haut, puis les voix fournies avec leur drapeau (langue de l'interface en premier). Chaque ligne propose
  ▶ écouter (la voix durable lorsqu'elle existe), le cœur (ajouter ou retirer) et ⋯ ; ↑/↓ et Entrée choisissent, Échap
  ferme, la dernière voix est mémorisée. La liste se trouve dans `sesler/okuma_listesi.json`, hors du dépôt, et survit
  aux redémarrages.
- **Gérer les voix.** Le menu ⋯ (ligne du menu des voix ou carte de variante) propose *Lire avec cette voix*, ajouter à
  la liste ou en retirer, *Renommer* (un nom vide rétablit l'original ; *Revenir au nom d'origine*), *Supprimer* pour
  les voix conçues et *Masquer* pour les voix fournies ; les deux demandent confirmation. Une voix supprimée est
  déplacée dans `sesler/_cop/` ; le masquage ne touche jamais aux fichiers du dépôt. *Voix masquées et supprimées (N)*,
  en bas du menu des voix, propose *Restaurer*. Les noms personnalisés et les voix masquées sont conservés dans
  `sesler/yerel_katman.json`. Une voix renommée affiche son origine en gris (*nom de la génération · variante N*) ;
  ⋯ → *Aller à la génération* ouvre sa conception.
- **Raccourcis et fichiers.** Ctrl+Entrée (⌘+Entrée sur Mac) lance *Créer* ou *Lire avec cette voix* dans l'onglet
  ouvert. La barre de progression affiche *écoulé / ~total*, avec une estimation apprise des tâches précédentes sur
  votre machine. Le fichier téléchargé porte le nom de la voix et l'heure (`Voice_Name_2026-11-02_0152.wav`).

**Clonage de voix (votre voix ou une voix autorisée).** Dans l'onglet *Clonage de voix* de l'interface, fournissez votre
enregistrement (wav/mp3/flac/ogg, 5 à 30 s de parole nette conseillées ; en dessous de 3 s il est refusé, au-delà de
36 s il est tronqué), sa transcription exacte et le texte à lire. Le bouton reste désactivé tant que vous n'avez pas
coché « Cette voix est la mienne ou j'ai l'accord explicite de son propriétaire ». L'enregistrement n'est envoyé qu'au
serveur local (127.0.0.1), il est traité dans un dossier temporaire avec son encodage de référence, et ce dossier est
supprimé à la fin de la tâche, même en cas d'échec ; rien n'est envoyé sur le réseau. Seule la sortie synthétique est
conservée (interface : `sesler/_okumalar/<job>/`, CLI : `--cikti`). La sortie est `klon_synthetic.wav`, avec une
étiquette « synthetic » ; signalez-la comme générée par une IA lorsque vous la partagez. CLI : `python -m ses_tasarim.klonla --kayit myvoice.wav --kayit-metni @transcript.txt --metin "Hello." --cikti out/clone --onay`

## FAQ

**Modèle ou moteur ? Qui fait quoi ?** VoxCPM2 (OpenBMB) est le *modèle* : le réseau de 2 milliards de paramètres qui
transforme le texte en parole. audio.cpp est le *moteur* : le programme C++/CUDA qui exécute le modèle sur votre GPU
(`audiocpp_cli.exe`). Notre patch modifie le moteur, pas le modèle : il fait tenir VoxCPM2 dans 4 Go et garantit que la
même graine donne le même audio à chaque fois. Le paquet Python de ce dépôt se contente de préparer le texte, d'appeler
le moteur et de rassembler les fichiers.

**Quels GPU ?** Voir « GPU pris en charge » plus haut : NVIDIA à partir des GTX 10xx, 4 Go de VRAM ou plus, pilote
≥ 570. La release contient du code natif pour sm_61/75/86/89/120a ; les autres cartes Pascal ou plus récentes utilisent
le PTX embarqué (premier démarrage plus lent). AMD/Intel : zip Vulkan expérimental, `kur.ps1 -Vulkan` ; un utilisateur
externe a signalé l'avoir fait fonctionner sur une AMD 6900 XT, mais des tests plus larges sur AMD/Intel restent
nécessaires (voir « AMD / Intel » plus haut). Le mode CPU seul (`"backend": "cpu"` dans `ayarlar.json`) fonctionne mais
est ~6× plus lent qu'une GTX 1050 Ti (mesure du moteur : 535 s contre 94 s pour 48 s de parole) ; ce n'est pas une voie
prise en charge.

**Quelle vitesse ?** Mesuré sur une GTX 1050 Ti 4 Go (i7-7700HQ) : une variante de conception (enregistrement
d'≈ 25 s) en 55 s ; lecture ≈ 2 s de calcul pour 1 s de parole (facteur temps réel 1,9 à 2,8) après un encodage de
référence unique d'environ 50 s par voix (mis en cache sur le disque) et 10 à 20 s de chargement du modèle par lot ;
pic de VRAM 2,6 à 2,9 Go. Les cartes plus récentes sont plus rapides ; chiffres et méthode :
[docs/4gb.md](docs/4gb.md).

**Peut-il cloner une voix ?** Le modèle VoxCPM2 sous-jacent peut imiter une voix à partir d'un enregistrement de
référence, et la partie clonage s'en sert. Utilisez-la uniquement avec votre propre voix ou avec l'autorisation
explicite de la personne à qui appartient la voix ; l'interface vous demande de confirmer cette autorisation. La
conception de voix ne nécessite aucun enregistrement : elle part d'une description textuelle en anglais ou en chinois,
et la « référence » utilisée pour lire avec une voix conçue est l'enregistrement de conception synthétique produit par
le modèle lui-même. L'usurpation d'identité, la fraude et la tromperie sont interdites. Voir [ETHICS.md](ETHICS.md).
Signalez ce que vous publiez comme généré par une IA.

**Comment écrire une bonne description de voix ?** En anglais, en 1 à 3 phrases : âge et genre, timbre (grave/clair,
chaleureux, nasal, éraillé), ton et rôle (narrateur de documentaire posé, présentateur énergique), tempo (lent, mesuré)
et « clean studio recording, no background noise ». Restez sur une description, pas sur un script ; pas de
parenthèses. Demandez 3 à 5 variantes et écoutez-les : la graine change beaucoup la voix. Pour le texte de création,
utilisez 1 à 3 phrases naturelles dans la langue de la voix, dans l'ambiance souhaitée (au plus ~30 s de parole). À la
lecture, une phrase par ligne ; coupez les phrases longues, écrivez les nombres en toutes lettres.

## Contribuer

Vous ne savez pas par où commencer ? Ces quatre petits tickets sont une bonne première étape :

- [#5](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/5) Essayez-le sur votre GPU et indiquez la carte, le pilote et les temps mesurés
- [#6](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/6) AMD / Intel : essayez le build Vulkan expérimental
- [#7](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/7) Ajoutez une phrase au jeu de test
- [#8](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/8) Partagez une voix que vous avez conçue, avec sa description et sa graine

**Testez votre carte graphique, envoyez un rapport :** pas besoin de coder, le [formulaire de rapport de test matériel](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=donanim-testi.yml) suffit ; aucun rapport sur carte Intel pour l'instant.

Jeu de test commun : [docs/test_seti/cumleler.txt](docs/test_seti/cumleler.txt) ; guide de la voix de marque :
[docs/marka_sesi_rehberi.md](docs/marka_sesi_rehberi.md) ; comment proposer du code : [CONTRIBUTING.md](CONTRIBUTING.md).
Problèmes d'installation : [formulaire de ticket](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/issues/new?template=kurulum-sorunu.yml) ; questions et résultats : [Discussions](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/discussions).
Toutes les personnes qui participent suivent le [Code de conduite](CODE_OF_CONDUCT.md) : soyez bienveillant et centrez
vos retours sur le travail.

## Contributeurs

- [@alexturkey](https://github.com/alexturkey) : mainteneur ; code, voix fournies, documentation
- [@cayir21](https://github.com/cayir21) : prise en charge de Metal sur macOS (Apple Silicon), [#10](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/10)
- [@grogureis](https://github.com/grogureis) : correctif de fin de phrase (EOS) pour la lecture de plusieurs phrases sur le backend CPU, [#14](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/14)
- [@mslmyilmaz5](https://github.com/mslmyilmaz5) : installation CUDA expérimentale sous Ubuntu/Linux et prise en charge de Docker, [#15](https://github.com/alexturkey/voxcpm2-turkce-ses-tasarimi/pull/15)

Votre nom a aussi sa place ici : un résultat de test sur votre GPU, une phrase pour le jeu de test, une voix que vous
avez conçue, un rapport de bug clair ou une pull request comptent tous comme des contributions. Merci à toutes celles et
ceux qui l'essaient et nous font un retour.

## Licence et crédits

Code et voix fournies : Apache-2.0, Copyright 2026 Ali Haydar Ozturk. Basé sur VoxCPM2 (OpenBMB, Apache-2.0),
audio.cpp (ShugoAI LLC, Apache-2.0) et la conversion GGUF d'audio.cpp. Liste complète : [THIRD_PARTY.md](THIRD_PARTY.md).
Sans lien avec OpenBMB, ModelBest ou le projet audio.cpp.

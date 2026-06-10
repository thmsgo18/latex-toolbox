<p align="right"><a href="./README.md">English</a> | <b>Français</b></p>

<p align="center">
  <img src="docs/assets/latex-forge-logo.png" alt="LaTeX Forge" width="420">
</p>

<p align="center">
  <b>Écrivez votre document. Sauvegardez. Le PDF apparaît. C'est tout.</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/latex-forge/"><img src="https://img.shields.io/pypi/v/latex-forge?style=for-the-badge&color=blue" alt="Version PyPI"></a>
  <a href="https://github.com/thmsgo18/latex-forge/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/thmsgo18/latex-forge/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://pypi.org/project/latex-forge/"><img src="https://img.shields.io/pypi/pyversions/latex-forge?style=for-the-badge" alt="Versions Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-green?style=for-the-badge" alt="Licence MIT"></a>
</p>

<p align="center">
  <a href="#démarrage-rapide">Démarrage rapide</a> •
  <a href="#templates">Templates</a> •
  <a href="#votre-profil">Profil</a> •
  <a href="#compiler-depuis-le-terminal">Compilation</a> •
  <a href="#besoin-daide-">Aide</a> •
  <a href="#référence-des-commandes">Commandes</a> •
  <a href="#projets-liés">Extension VS Code</a>
</p>

---

<p align="center">
  <img src="docs/assets/demo-create.gif" alt="démo latex-forge create" width="900">
</p>

## C'est quoi, LaTeX Forge ?

Vous devez rendre un rapport, un CV ou un article en LaTeX, et vous préféreriez passer votre temps à **écrire** plutôt qu'à vous battre avec les packages, les compilateurs et la configuration.

LaTeX Forge est un petit outil que vous installez une fois. Une commande crée ensuite un projet de document complet et prêt à l'emploi : l'arborescence, les styles, la bibliographie, et un espace VS Code pré-configuré. Ouvrez-le, écrivez, sauvegardez : le PDF se reconstruit automatiquement dans un panneau latéral.

**Aucune connaissance de LaTeX n'est requise pour démarrer.** Et si vous vivez déjà dans un terminal, tout est scriptable.

## Démarrage rapide

```bash
# 1. installer (une seule fois)
pipx install latex-forge

# 2. vérifier votre machine et installer ce qui manque (LaTeX, extensions VS Code)
latex-forge setup

# 3. créer votre premier projet
latex-forge create --name mon-rapport --template project-report-fr

# 4. l'ouvrir et commencer à écrire
code mon-rapport
```

<details>
<summary><i>C'est quoi pipx ? (cliquez si l'étape 1 échoue)</i></summary>

`pipx` installe proprement les outils Python en ligne de commande. S'il manque :

- **macOS** : `brew install pipx && pipx ensurepath`
- **Windows** : `py -m pip install --user pipx && py -m pipx ensurepath`
- **Linux** : `sudo apt install pipx && pipx ensurepath` (ou voir [pipx.pypa.io](https://pipx.pypa.io))

Ouvrez ensuite un nouveau terminal et relancez l'étape 1. Python 3.10+ est requis.
</details>

## Fonctionnalités

- **Des projets en une commande** : arborescence complète, styles embarqués, aucune dépendance externe
- **Aperçu PDF en direct** : les projets sont pré-câblés pour [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) : sauvegardez dans VS Code, voyez le PDF
- **Compilation en terminal** : `latex-forge build` et `latex-forge watch` fonctionnent sans aucun éditeur, et installent automatiquement les paquets manquants
- **Plus de 80 templates** : CV, thèses, articles, posters, présentations… installables depuis la [galerie](https://github.com/thmsgo18/latex-forge-gallery) en une commande, ainsi que les vôtres avec `--engine`
- **Votre profil, pré-rempli** : renseignez votre nom, email et université une fois ; chaque nouveau projet démarre personnalisé
- **Prêt pour git** : `latex-forge create --git` initialise un dépôt avec le premier commit
- **Export prêt à rendre** : `latex-forge export` regroupe vos sources et le PDF dans un ZIP propre
- **Docteur d'environnement** : `latex-forge setup` installe la chaîne LaTeX selon votre OS ; `latex-forge diagnose` vous dit ce qui ne va pas
- **Pensé pour les IA** : chaque projet embarque un `AGENTS.md` qui briefe n'importe quel assistant IA
- **Multi-plateforme** : macOS, Linux, Windows

## À quoi ça ressemble

<p align="center">
  <img src="docs/assets/live-preview.png" alt="Aperçu en direct LaTeX Forge dans VS Code" width="800">
</p>

Écrivez d'un côté. Voyez votre document de l'autre. Chaque sauvegarde rafraîchit le résultat.

## Templates

Six templates sont intégrés :

| Template | Langue | Description |
|---|---|---|
| `blank` | Anglais | Document minimal : titre, une section, prêt à grandir |
| `project-report-en` | Anglais | Rapport de projet ISO/IEEE : exigences, architecture, tests, bibliographie |
| `project-report-fr` | Français | Rapport de projet AFNOR/ISO : cahier des charges, architecture, tests, bibliographie |
| `research` | Anglais | Article de recherche deux colonnes : état de l'art, méthodologie, expériences |
| `cv-en` | Anglais | CV : éducation, expérience, projets, compétences |
| `cv-fr` | Français | CV : formation, expérience, projets, compétences |

```bash
latex-forge list-templates
```

### La galerie (plus de 80 autres)

Parcourez la [**galerie de templates**](https://thmsgo18.github.io/latex-forge-gallery/) avec aperçus, puis installez n'importe quel template en une commande :

<p align="center">
  <a href="https://thmsgo18.github.io/latex-forge-gallery/">
    <img src="https://raw.githubusercontent.com/thmsgo18/latex-forge-gallery/main/previews/cv/awesome-cv.png" alt="awesome-cv" width="160">
    <img src="https://raw.githubusercontent.com/thmsgo18/latex-forge-gallery/main/previews/thesis/clean-thesis.png" alt="clean-thesis" width="160">
    <img src="https://raw.githubusercontent.com/thmsgo18/latex-forge-gallery/main/previews/presentation/beamer-metropolis.png" alt="beamer-metropolis" width="160">
    <img src="https://raw.githubusercontent.com/thmsgo18/latex-forge-gallery/main/previews/article/arxiv-template.png" alt="arxiv-template" width="160">
  </a>
</p>

```bash
# installer un template depuis la galerie
latex-forge template install https://github.com/thmsgo18/latex-forge-gallery/tree/main/templates/thesis/clean-thesis

# créer un projet à partir de ce template
latex-forge create --template clean-thesis --name ma-these

# gérer les templates installés
latex-forge template list
latex-forge template update          # récupère les nouvelles versions de la galerie
latex-forge template remove clean-thesis
```

Vous pouvez aussi installer **vos propres templates** depuis n'importe quel dépôt GitHub, fichier ZIP ou dossier local. Seule exigence : un `main.tex` à la racine :

```bash
latex-forge template install https://github.com/quelquun/son-template
latex-forge template install ~/mes-templates/notes-labo --name notes-labo

# déclarer le moteur LaTeX si le template ne le fait pas déjà (pdflatex/xelatex/lualatex)
latex-forge template install https://github.com/quelquun/son-template --engine xelatex
```

Voir [TEMPLATE_COMPATIBILITY.md](TEMPLATE_COMPATIBILITY.md) pour activer le pré-remplissage du profil (nom, email, université…) sur vos propres templates.

> Vous préférez cliquer plutôt que taper ? L'[extension VS Code](https://github.com/thmsgo18/latex-forge-vscode) intègre un navigateur de galerie avec aperçus et installation en un clic.

## Votre profil

Dites à LaTeX Forge qui vous êtes **une seule fois**, et chaque nouveau projet est pré-rempli avec votre nom, email, université, etc. :

```bash
latex-forge profile set      # interactif : nom, email, téléphone, université…
latex-forge profile show
latex-forge profile clear
```

Fonctionne avec les templates intégrés et ceux de la galerie (les CV reçoivent vos coordonnées, les rapports votre université et votre encadrant).

## Compiler depuis le terminal

Pas de VS Code ? Aucun problème.

<p align="center">
  <img src="docs/assets/demo-build.gif" alt="démo latex-forge build" width="900">
</p>

```bash
latex-forge build            # compile une fois → build/<nom>.pdf
latex-forge build --clean    # nettoie les artefacts de compilation d'abord
latex-forge watch            # recompile à chaque sauvegarde (Ctrl+C pour arrêter)
```

Le bon moteur LaTeX est détecté depuis le projet lui-même : rien à configurer.

## Utilisation

### Mode interactif

```
$ latex-forge create

Project name: mon-rapport
Available templates:
  1. blank
  2. cv-en
  3. cv-fr
  4. project-report-en
  5. project-report-fr
  6. research
Choose a template [1-6]: 5
Create project in [/Users/alice/Desktop]:

Project created: /Users/alice/Desktop/mon-rapport
Open project in VS Code? [y/N]
```

### Avec des options

```bash
latex-forge create --name mon-rapport --template project-report-fr
latex-forge create --name mon-article --template research --output ~/Desktop
```

### Renommer un projet

```bash
latex-forge rename ancien-nom nouveau-nom   # depuis le dossier parent
latex-forge rename nouveau-nom              # depuis l'intérieur du projet
```

### Configuration

```toml
# ~/.latex-forge.toml
default_template = "project-report-fr"
default_output_dir = "~/Documents/projets"
```

| Clé | Description |
|---|---|
| `default_template` | Template utilisé quand `--template` est omis |
| `default_output_dir` | Dossier de sortie utilisé quand `--output` est omis |

### Complétion shell

Complétion Tab pour les commandes, options et noms de templates pour **bash** (`~/.bashrc`) ou **zsh** (`~/.zshrc`) :

```bash
eval "$(latex-forge completion)"
```

## Remplir votre projet

Ouvrez `frontmatter/metadata.tex` pour définir le titre, les auteurs et le cours :

```tex
\newcommand{\reporttitle}{Étude d'empreintes audio}
\newcommand{\coursename}{Machine Learning}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}
```

Sauvegardez le fichier `.tex` principal : le PDF se reconstruit instantanément dans VS Code (ou lancez `latex-forge build`).

## Structure d'un projet généré

```
mon-projet/
├── mon-projet.tex            ← fichier principal (nommé d'après le projet)
├── frontmatter/
│   ├── metadata.tex          ← titre, auteurs, cours (commencez ici)
│   └── toc.tex
├── sections/                 ← un fichier .tex par section
├── backmatter/               ← remerciements, annexes
├── bibliography/
│   └── references.bib
├── figures/  images/  assets/logos/
├── styles/packages/          ← styles embarqués, aucune dépendance externe
├── .vscode/                  ← pré-configuré pour l'aperçu PDF en direct
├── GETTING_STARTED.md        ← guide pour vous
├── AGENTS.md                 ← briefing pour les assistants IA
└── .gitignore
```

Le projet est entièrement autonome : il se compile, se partage et se versionne indépendamment, sans dépendance envers ce dépôt. Chaque projet embarque aussi `AGENTS.md`, un briefing qui permet à n'importe quel assistant IA d'ouvrir le projet à froid et de contribuer correctement.

## Besoin d'aide ?

Commencez par le docteur, qui vérifie tout et vous dit quoi corriger :

```bash
latex-forge diagnose
```

| Problème | Solution |
|---|---|
| `latex-forge: command not found` | Ouvrez un nouveau terminal, ou lancez `pipx ensurepath` |
| Rien ne compile / pas de PDF | `latex-forge setup --install-tex` installe LaTeX pour votre OS |
| `Package X not found` | `tlmgr install X` (TeX Live) ; MiKTeX l'installe automatiquement |
| Compilation bloquée | `latex-forge build --clean`, puis réessayez |
| Autre chose | [Ouvrez une issue](https://github.com/thmsgo18/latex-forge/issues) avec la sortie de `latex-forge diagnose` |

## Référence des commandes

| Commande | Description |
|---|---|
| `latex-forge create` | Créer un projet (interactif) |
| `latex-forge create --name N --template T --output DIR [--git]` | Créer avec des arguments explicites, avec `git init` en option |
| `latex-forge build [DIR] [--clean] [--verbose]` | Compiler en PDF avec latexmk (installe les paquets manquants via tlmgr) |
| `latex-forge watch [DIR]` | Recompiler à chaque sauvegarde |
| `latex-forge export [DIR] [--output FICHIER]` | Regrouper sources + PDF dans un ZIP propre à rendre |
| `latex-forge rename [ANCIEN] NOUVEAU` | Renommer un projet (dossier + fichier principal + artefacts) |
| `latex-forge list-templates` | Lister les templates disponibles |
| `latex-forge template install SOURCE [--name N] [--force] [--engine E]` | Installer un template (URL GitHub, ZIP, chemin local) |
| `latex-forge template list [--json]` | Lister les templates intégrés et installés |
| `latex-forge template update [NOM] [--json]` | Mettre à jour les templates de la galerie |
| `latex-forge template remove NOM` | Supprimer un template installé |
| `latex-forge profile set / show / clear` | Gérer votre profil de pré-remplissage |
| `latex-forge setup [--check-only] [--install-tex]` | Vérifier / configurer l'environnement |
| `latex-forge diagnose [--json]` | Bilan de santé de l'environnement |
| `latex-forge completion [--shell SHELL]` | Afficher le code de complétion shell |
| `latex-forge --version` | Afficher la version |

## Versionner vos documents

Chaque projet est autonome, vous pouvez donc le versionner indépendamment :

```bash
cd mon-projet
git init && git add . && git commit -m "Rapport initial"
```

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md). Les GIFs de démo sont générés avec [vhs](https://github.com/charmbracelet/vhs) : `./docs/demo/record.sh`.

## Projets liés

| Projet | Ce qu'il apporte |
|---|---|
| [**latex-forge-vscode**](https://github.com/thmsgo18/latex-forge-vscode) | Tout faire depuis VS Code : créer des projets, parcourir la galerie avec aperçus, installer en un clic (sans terminal) |
| [**latex-forge-gallery**](https://github.com/thmsgo18/latex-forge-gallery) | La galerie de templates curée (80+) et son [site web](https://thmsgo18.github.io/latex-forge-gallery/) |
| [**latex-forge-skill**](https://github.com/thmsgo18/latex-forge-skill) | Un skill Claude qui pilote tout le workflow depuis une conversation : génération, rédaction, compilation et export des documents |

## Auteur

Créé par [thmsgo18](https://github.com/thmsgo18)

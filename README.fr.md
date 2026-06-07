# LaTeX Forge

<p align="center">
  <img src="docs/assets/latex-forge-logo.png" alt="LaTeX Forge" width="480">
</p>

<p align="center">
  Crée des documents professionnels. Sauvegarde. Le PDF apparaît instantanément.
</p>

<p align="center">
  <a href="https://pypi.org/project/latex-forge/"><img src="https://img.shields.io/pypi/v/latex-forge?style=for-the-badge&color=blue" alt="PyPI version"></a>
  <a href="https://github.com/thmsgo18/latex-forge/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/thmsgo18/latex-forge/ci.yml?branch=main&style=for-the-badge" alt="CI"></a>
  <a href="https://pypi.org/project/latex-forge/"><img src="https://img.shields.io/pypi/pyversions/latex-forge?style=for-the-badge" alt="Python versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License MIT"></a>
</p>

<p align="center">
  <a href="./README.md">Read in English</a>
</p>

---

Une commande crée un projet de document prêt à écrire. Ouvre-le dans VS Code, commence à écrire, sauvegarde — le PDF se reconstruit et apparaît dans un panneau latéral automatiquement. Pas de compilation manuelle, pas de changement de fenêtre.

Utilisable par les humains et les IA. Chaque projet généré contient un fichier `AGENTS.md` qui brieffe tout assistant IA sur la structure du document, pour qu'il puisse contribuer immédiatement.

## L'expérience

<p align="center">
  <img src="docs/assets/live-preview.png" alt="Aperçu en direct de LaTeX Forge dans VS Code" width="800">
</p>

Écris d'un côté. Vois le résultat de l'autre. Chaque sauvegarde rafraîchit le document.

## Démarrage rapide

```bash
# 1 — installer
pipx install latex-forge

# 2 — configurer l'environnement (LaTeX + extensions VS Code)
latex-forge setup

# 3 — créer un projet
latex-forge create --name mon-rapport --template rapport-projet-fr

# 4 — ouvrir et écrire
code mon-rapport
```

Requiert Python 3.10+. Si `pipx` n'est pas installé : `brew install pipx` sur macOS, ou voir [pipx.pypa.io](https://pipx.pypa.io).

## Installation

```bash
pipx install latex-forge
```

## Premier lancement

Sur une nouvelle machine, lance la commande de configuration :

```bash
latex-forge setup
```

Cette commande vérifie `latexmk` et `lualatex`, et propose de les installer automatiquement (`brew` sur macOS, `apt` sur Debian/Ubuntu, `winget` sur Windows). Les extensions VS Code recommandées sont aussi installées si la commande `code` est disponible.

## Profil utilisateur

Configure ton profil une fois. Chaque projet créé ensuite aura ton nom, ton université et ton programme déjà renseignés :

```bash
latex-forge profile --set
```

```
Full name: Dupont Alice
University / school: Université de Bordeaux
Program / formation: Master Informatique
GitHub username (optional): dupont-alice
```

```bash
latex-forge profile        # voir le profil actuel
latex-forge profile --set  # modifier
```

Les valeurs sont stockées dans `~/.latex-forge.toml` et injectées dans `frontmatter/metadata.tex` à chaque création de projet.

## Autocomplétion shell

Autocomplétion des commandes, options et noms de templates avec Tab :

**bash** (`~/.bashrc`) ou **zsh** (`~/.zshrc`) :

```bash
eval "$(latex-forge completion)"
```

## Configuration

```toml
# ~/.latex-forge.toml
default_template = "rapport-projet-fr"
default_output_dir = "~/Documents/projets"
```

| Clé | Description |
|---|---|
| `default_template` | Template utilisé quand `--template` est absent |
| `default_output_dir` | Dossier de destination quand `--output` est absent |

## Utilisation

### Mode interactif

```
$ latex-forge create

Project name: mon-rapport
Available templates:
  1. cv-en
  2. cv-fr
  3. rapport-projet-en
  4. rapport-projet-fr
  5. research
Choose a template [1-5]: 4
Create project in [/Users/alice/Desktop]:

Project created: /Users/alice/Desktop/mon-rapport
Open project in VS Code? [y/N]
```

### Avec des arguments

```bash
latex-forge create --name mon-rapport --template rapport-projet-fr
latex-forge create --name mon-article --template research --output ~/Bureau
```

### Renommer un projet

```bash
latex-forge rename ancien-nom nouveau-nom   # depuis le dossier parent
latex-forge rename nouveau-nom             # depuis l'intérieur du projet
```

## Templates intégrés

| Template | Langue | Description |
|---|---|---|
| `rapport-projet-fr` | Français | Rapport de projet AFNOR/ISO — cahier des charges, architecture, tests, bibliographie |
| `rapport-projet-en` | Anglais | Rapport de projet ISO/IEEE — requirements, architecture, testing, bibliography |
| `research` | Anglais | Article de recherche deux colonnes — related work, methodology, experiments, bibliography |
| `cv-fr` | Français | CV — formation, expérience, projets, compétences |
| `cv-en` | Anglais | CV / résumé — education, experience, projects, skills |

```bash
latex-forge list-templates
```

## Galerie de templates

D'autres types de documents sont disponibles dans [latex-forge-gallery](https://github.com/thmsgo18/latex-forge-gallery) : CVs, thèses, articles, présentations, posters, et plus encore.

```bash
# installer un template directement par URL
latex-forge template install https://github.com/thmsgo18/latex-forge-gallery/tree/main/templates/thesis/clean-thesis

# créer un projet avec ce template
latex-forge create --template clean-thesis --name ma-these

# gérer les templates installés
latex-forge template list
latex-forge template remove clean-thesis
```

## Remplir son projet

Ouvre `frontmatter/metadata.tex` pour renseigner le titre, les auteurs et le cours :

```tex
\newcommand{\reporttitle}{Étude de l'empreinte audio}
\newcommand{\coursename}{Apprentissage automatique}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}

\resetteachers
\addteacher{Dr Exemple}{}
```

Sauvegarde le fichier `.tex` principal --- le PDF se reconstruit instantanément dans VS Code.

## Structure d'un projet généré

```
mon-projet/
├── mon-projet.tex            ← fichier principal (renommé d'après le projet)
├── frontmatter/
│   ├── metadata.tex          ← titre, auteurs, cours — commencer ici
│   └── toc.tex
├── sections/                 ← un fichier .tex par section
├── backmatter/               ← remerciements, annexes
├── bibliography/
│   └── references.bib
├── figures/
├── images/
├── assets/logos/
├── styles/packages/          ← styles embarqués, aucune dépendance externe
├── .vscode/                  ← préconfiguré pour l'aperçu PDF en direct
├── AGENTS.md                 ← briefing IA pour ce document
└── .gitignore
```

Le projet est entièrement autonome : styles et assets sont copiés à la création. Il se compile, se partage et se versionne indépendamment, sans dépendance envers ce dépôt.

## Conçu pour les IA

Chaque projet généré contient `AGENTS.md` --- un briefing autonome qui indique à tout assistant IA ce que contient le projet, comment le compiler, comment ajouter du contenu, et ce qu'il ne faut pas modifier. Une IA peut ouvrir le projet à froid et contribuer correctement sans contexte supplémentaire.

## Référence des commandes

| Commande | Description |
|---|---|
| `latex-forge create` | Créer un projet (interactif) |
| `latex-forge create --name NOM --template TEMPLATE` | Créer avec des arguments explicites |
| `latex-forge create --output DOSSIER` | Définir le dossier de destination |
| `latex-forge rename ANCIEN NOUVEAU` | Renommer depuis le dossier parent |
| `latex-forge rename NOUVEAU` | Renommer depuis l'intérieur du projet |
| `latex-forge list-templates` | Lister les templates disponibles |
| `latex-forge setup` | Vérifier et configurer l'environnement |
| `latex-forge setup --check-only` | Vérifier sans rien installer |
| `latex-forge setup --install-tex` | Installer LaTeX |
| `latex-forge profile` | Voir le profil configuré |
| `latex-forge profile --set` | Configurer le profil |
| `latex-forge template install URL` | Installer un template |
| `latex-forge template list` | Lister tous les templates |
| `latex-forge template remove NOM` | Supprimer un template installé |
| `latex-forge completion` | Afficher le code d'autocomplétion shell |
| `latex-forge --version` | Afficher la version |

## Versionner les projets générés

Chaque projet est autonome, versionnez-le indépendamment :

```bash
cd mon-projet
git init
git add .
git commit -m "Initial report"
```

## Contribuer

Consulte [CONTRIBUTING.md](CONTRIBUTING.md).

---

Fait par [thmsgo18](https://github.com/thmsgo18)

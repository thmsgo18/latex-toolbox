# LaTeX Forge

<p align="center">
  <img src="docs/assets/latex-forge-logo.png" alt="LaTeX Forge" width="480">
</p>

<p align="center">
  Zéro configuration. Juste écrire. Tout ce qu'il faut, rien de plus.
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

LaTeX Forge est un outil en ligne de commande qui génère des projets LaTeX prêts à compiler à partir de templates. Chaque projet généré embarque ses propres styles et assets — il peut être compilé, partagé et versionné de façon indépendante, sans aucune dépendance envers ce dépôt.

## Installation

```bash
pipx install latex-forge
```

Requiert Python 3.10+. Si `pipx` n'est pas installé : `brew install pipx` sur macOS, ou consulter [pipx.pypa.io](https://pipx.pypa.io).

## Premier lancement

Sur une nouvelle machine, lance la commande de configuration pour vérifier l'environnement et installer LaTeX automatiquement :

```bash
latex-forge setup
```

Cette commande vérifie que `latexmk` et `lualatex` sont disponibles, et propose de les installer via le gestionnaire de paquets du système (`brew` sur macOS, `apt` sur Debian/Ubuntu, `winget` sur Windows). Les extensions VS Code recommandées sont également installées si la commande `code` est accessible.

## Profil utilisateur

Configure ton profil une seule fois pour que `create` pré-remplisse automatiquement les métadonnées de chaque projet :

```bash
latex-forge profile --set
```

```
Full name: Dupont Alice
University / school: Université de Bordeaux
Program / formation: Master Informatique
GitHub username (optional): dupont-alice
```

Cette configuration est proposée automatiquement au premier lancement. Pour la modifier à tout moment :

```bash
latex-forge profile        # voir le profil actuel
latex-forge profile --set  # modifier
```

Les valeurs sont stockées dans `~/.latex-forge.toml` et injectées dans `frontmatter/metadata.tex` à chaque création de projet. Si un nom d'utilisateur GitHub est renseigné, il est affiché sous ton nom en tant que lien cliquable sur la page de titre du PDF.

## Autocomplétion shell

Autocomplétion des commandes, options et noms de templates avec la touche Tab. Ajoute une ligne à la configuration de ton shell :

**bash** (`~/.bashrc`) ou **zsh** (`~/.zshrc`) :

```bash
eval "$(latex-forge completion)"
```

Recharge ton shell (`source ~/.zshrc`) ou ouvre un nouveau terminal.

## Fichier de configuration

Crée `~/.latex-forge.toml` pour définir des valeurs par défaut appliquées à toutes les commandes :

```toml
default_template = "rapport-projet-fr"
default_output_dir = "~/Documents/projets"
```

| Clé | Description |
|---|---|
| `default_template` | Template utilisé quand `--template` est absent |
| `default_output_dir` | Dossier de destination quand `--output` est absent |

## Utilisation

### Mode interactif

Lance `create` sans arguments pour être guidé étape par étape :

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
Create project in [/Users/thomas/Desktop]:

Project created: /Users/thomas/Desktop/mon-rapport
Edit: mon-rapport/mon-rapport.tex
Next: fill in frontmatter/metadata.tex then save to compile.
Open project in VS Code? [y/N]
```

### Avec des arguments

Tous les arguments sont optionnels — ceux qui manquent sont demandés interactivement.

```bash
# tout spécifier d'un coup
latex-forge create --name mon-rapport --template rapport-projet-fr

# créer dans un dossier précis
latex-forge create --name mon-article --template research --output ~/Bureau
```

### Renommer un projet

```bash
# depuis le dossier parent
latex-forge rename ancien-nom nouveau-nom

# depuis l'intérieur du projet
latex-forge rename nouveau-nom
```

Cette commande renomme le dossier, le fichier `.tex` principal, et les artefacts de build existants.

## Templates disponibles

| Template | Langue | Description |
|---|---|---|
| `rapport-projet-fr` | Français | Rapport de projet aligné AFNOR/ISO — cahier des charges, architecture, tests, bibliographie, annexes |
| `rapport-projet-en` | Anglais | Rapport de projet aligné ISO/IEEE — requirements, architecture, testing, bibliography, appendices |
| `research` | Anglais | Article de recherche — deux colonnes, related work, methodology, experiments, bibliographie |
| `cv-fr` | Français | CV — formation, expérience, projets, engagement, compétences |
| `cv-en` | Anglais | CV / résumé — education, experience, projects, involvement, skills |

```bash
latex-forge list-templates
```

## Après la création d'un projet

1. Ouvre le dossier généré dans VS Code.
2. Remplis `frontmatter/metadata.tex` — titre, auteurs, nom du cours, logo de l'université.
3. Sauvegarde le fichier `.tex` principal pour déclencher la compilation (nécessite [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)).
4. Le PDF est généré dans `build/`.

Exemple de `metadata.tex` :

```tex
\newcommand{\reporttitle}{Étude de l'empreinte audio}
\newcommand{\coursename}{Apprentissage automatique}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}

\resetteachers
\addteacher{Dr Exemple}{}

\resetprojectlinks
\addprojectlink{Dépôt}{https://github.com/exemple/projet}
```

Laisser le second argument vide dans `\addauthor{...}{}` ou `\addteacher{...}{}` masque l'étiquette de rôle.

## Structure d'un projet généré

```
mon-projet/
├── mon-projet.tex            ← fichier principal (nommé d'après le projet)
├── frontmatter/
│   ├── metadata.tex          ← titre, auteurs, cours
│   └── toc.tex
├── sections/
├── backmatter/
├── figures/
├── images/
├── screens/
├── assets/
│   ├── images/common/
│   └── logos/
├── styles/packages/          ← styles embarqués, aucune dépendance externe
├── scripts/                  ← scripts de configuration autonomes
├── .vscode/                  ← paramètres LaTeX Workshop
└── .gitignore
```

Les styles et logos sont copiés dans le projet au moment de sa création. Le projet généré n'a aucune dépendance sur ce dépôt.

## Référence des commandes

| Commande | Description |
|---|---|
| `latex-forge create` | Créer un projet (interactif) |
| `latex-forge create --name NOM --template TEMPLATE` | Créer avec des arguments explicites |
| `latex-forge create --output DOSSIER` | Définir le dossier de destination |
| `latex-forge rename ANCIEN NOUVEAU` | Renommer depuis le dossier parent |
| `latex-forge rename NOUVEAU` | Renommer depuis l'intérieur du projet |
| `latex-forge list-templates` | Lister les templates disponibles |
| `latex-forge setup` | Vérifier et configurer l'environnement LaTeX |
| `latex-forge setup --check-only` | Vérifier sans rien installer |
| `latex-forge setup --install-tex` | Installer LaTeX directement |
| `latex-forge --version` | Afficher la version installée |
| `latex-forge profile` | Voir le profil configuré |
| `latex-forge profile --set` | Configurer le profil interactivement |
| `latex-forge completion` | Afficher le code d'autocomplétion shell |

## Versionner les projets générés

Chaque projet généré est autonome, ce qui permet de le versionner indépendamment :

```bash
cd mon-projet
git init
git add .
git commit -m "Initial report"
```

Crée ensuite un dépôt privé dédié et invite uniquement les collaborateurs concernés par ce document.

## Contribuer

Consulte [CONTRIBUTING.md](CONTRIBUTING.md).

---

Fait par [thmsgo18](https://github.com/thmsgo18)

<div align="center">

# LaTeX Toolbox

Skip the setup. Start writing. Everything you need, nothing more.

[![PyPI version](https://img.shields.io/pypi/v/latex-toolbox?color=blue)](https://pypi.org/project/latex-toolbox/)
[![Python](https://img.shields.io/pypi/pyversions/latex-toolbox)](https://pypi.org/project/latex-toolbox/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Read in English](./README.md)

</div>

---

LaTeX Toolbox est un outil en ligne de commande qui génère des projets LaTeX prêts à compiler à partir de templates. Chaque projet généré embarque ses propres styles et assets — il peut être compilé, partagé et versionné de façon indépendante, sans aucune dépendance envers ce dépôt.

## Installation

```bash
pipx install latex-toolbox
```

Requiert Python 3.10+. Si `pipx` n'est pas installé : `brew install pipx` sur macOS, ou consulter [pipx.pypa.io](https://pipx.pypa.io).

## Premier lancement

Sur une nouvelle machine, lance la commande de configuration pour vérifier l'environnement et installer LaTeX automatiquement :

```bash
latex-toolbox setup
```

Cette commande vérifie que `latexmk` et `lualatex` sont disponibles, et propose de les installer via le gestionnaire de paquets du système (`brew` sur macOS, `apt` sur Debian/Ubuntu, `winget` sur Windows). Les extensions VS Code recommandées sont également installées si la commande `code` est accessible.

## Utilisation

### Mode interactif

Lance `create` sans arguments pour être guidé étape par étape :

```
$ latex-toolbox create

Project name: mon-rapport
Available templates:
  1. rapport-projet-en
  2. rapport-projet-fr
  3. rapport-ter
  4. research
Choose a template [1-4]: 2
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
latex-toolbox create --name mon-rapport --template rapport-projet-fr

# créer dans un dossier précis
latex-toolbox create --name mon-article --template research --output ~/Bureau
```

### Renommer un projet

```bash
# depuis le dossier parent
latex-toolbox rename ancien-nom nouveau-nom

# depuis l'intérieur du projet
latex-toolbox rename nouveau-nom
```

Cette commande renomme le dossier, le fichier `.tex` principal, et les artefacts de build existants.

## Templates disponibles

| Template | Langue | Description |
|---|---|---|
| `rapport-projet-en` | Anglais | Rapport de projet avec page de garde, sommaire, introduction, conclusion, notice IA |
| `rapport-projet-fr` | Français | Même structure que ci-dessus, en français |
| `rapport-ter` | Anglais | Rapport académique de type TER avec structure détaillée, bibliographie et annexes |
| `research` | Anglais | Article de recherche en deux colonnes avec abstract et bibliographie BibTeX |

```bash
latex-toolbox list-templates
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
| `latex-toolbox create` | Créer un projet (interactif) |
| `latex-toolbox create --name NOM --template TEMPLATE` | Créer avec des arguments explicites |
| `latex-toolbox create --output DOSSIER` | Définir le dossier de destination |
| `latex-toolbox rename ANCIEN NOUVEAU` | Renommer depuis le dossier parent |
| `latex-toolbox rename NOUVEAU` | Renommer depuis l'intérieur du projet |
| `latex-toolbox list-templates` | Lister les templates disponibles |
| `latex-toolbox setup` | Vérifier et configurer l'environnement LaTeX |
| `latex-toolbox setup --check-only` | Vérifier sans rien installer |
| `latex-toolbox setup --install-tex` | Installer LaTeX directement |
| `latex-toolbox --version` | Afficher la version installée |

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

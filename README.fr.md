# LaTeX Toolbox

[Read this in English](./README.md)

LaTeX Toolbox est une base locale pour creer rapidement des projets LaTeX propres, reutilisables et autonomes a partir de templates.

L'idee est simple :
- tu gardes dans ce depot tes templates, styles et assets partages ;
- tu generes un nouveau projet avec la commande `latex-toolbox` ;
- tu travailles ensuite sur le projet genere dans VS Code ;
- tu peux versionner chaque projet genere dans son propre depot Git.

Si tu rediges souvent des rapports de cours, des papiers de recherche, des TER ou des documents LaTeX collaboratifs, cette toolbox t'evite de repartir de zero a chaque fois.

## Ce que fait la toolbox

Quand tu crees un projet, la toolbox :
- copie le template choisi ;
- renomme le fichier principal `.tex` avec le nom du projet ;
- copie les styles LaTeX necessaires dans le projet ;
- copie les logos depuis `assets/logos/` ;
- cree un `.gitignore` local pour les fichiers de build LaTeX courants ;
- cree un projet qui peut compiler tout seul.

Les projets generes ne dependent donc pas de ce depot pour compiler.

## Prerequis

Configuration recommandee :
- Python 3
- une distribution LaTeX, par exemple `MacTeX`
- VS Code
- l'extension `LaTeX Workshop`

Extensions VS Code utiles :
- `LaTeX Workshop`
- `LTeX+`
- `Code Spell Checker`

Important :
- si tu utilises `LaTeX Workshop`, desactive `vscode-pdf` pour eviter les conflits de visualisation PDF.

## Installer la commande

La methode la plus simple est `pipx`.

Depuis la racine du depot :

```bash
cd /chemin/vers/latex-toolbox
brew install pipx
pipx install --editable .
```

Ensuite, la commande disponible est :

```bash
latex-toolbox
```

Si la commande n'est pas reconnue apres l'installation :

```bash
pipx ensurepath
```

Puis ouvre un nouveau terminal.

## Demarrage rapide

Creer un rapport de projet dans le dossier courant :

```bash
latex-toolbox create --name signal-processing-report --template rapport-projet-en
```

Creer un document de type recherche :

```bash
latex-toolbox create --name audio-search-paper --template research
```

Ensuite, ouvre dans VS Code le fichier principal du dossier genere :

```text
./signal-processing-report/signal-processing-report.tex
```

## Commandes disponibles

Lister les templates :

```bash
latex-toolbox list-templates
```

Verifier ou preparer une machine pour travailler en LaTeX :

```bash
latex-toolbox setup
latex-toolbox setup --check-only
latex-toolbox setup --install-tex
```

Chemins d'installation automatique pris en charge :
- macOS : `brew`
- Ubuntu / Debian : `apt-get`
- Fedora : `dnf`
- Arch Linux : `pacman`
- Windows : `winget`

Creer un projet :

```bash
latex-toolbox create --name mon-projet --template rapport-projet-en
```

Regles :
- `--name` est obligatoire
- `--template` est obligatoire
- le projet est cree dans le dossier courant
- le sous-dossier cree porte le nom du projet

Exemple :

```bash
cd ~/Desktop
latex-toolbox create --name shazam-report --template research
```

Cela cree :

```text
~/Desktop/shazam-report/
```

Renommer un projet genere :

```bash
latex-toolbox rename shazam-report shazam-final-report
```

Cette commande renomme :
- le dossier du projet
- le fichier `.tex` principal
- les principaux fichiers de build quand ils existent deja

Tu peux aussi lancer la commande depuis l'interieur du dossier du projet :

```bash
cd shazam-report
latex-toolbox rename shazam-final-report
```

## Workflow recommande

### 1. Creer un projet

```bash
latex-toolbox create --name mon-projet --template rapport-projet-en
```

Exemples concrets :

```bash
latex-toolbox create --name deep-learning-lab --template rapport-projet-en
latex-toolbox create --name rapport-analyse-signaux --template rapport-projet-fr
latex-toolbox create --name keyword-spotting-paper --template research
```

### 2. Ouvrir le projet dans VS Code

Ouvre ensuite le fichier principal, par exemple :

```text
./mon-projet/mon-projet.tex
```

### 3. Remplir les metadata

Les informations de premiere page sont centralisees dans :

```text
frontmatter/metadata.tex
```

Tu peux notamment y definir :
- le titre du rapport
- le nom du cours
- les auteurs
- les encadrants
- les liens du projet
- le logo de l'universite

Exemple :

```tex
\newcommand{\reporttitle}{Audio Fingerprinting Study}
\newcommand{\coursename}{Machine Learning}

\resetauthors
\addauthor{Alice Martin}{}
\addauthor{Bob Durand}{}

\resetteachers
\addteacher{Dr Example}{}

\resetprojectlinks
\addprojectlink{Repository}{https://github.com/example/audio-fingerprinting}
```

Si tu laisses le second argument vide dans `\addauthor{...}{}` ou `\addteacher{...}{}`, aucun role n'est affiche.

### 4. Compiler dans VS Code

Avec `LaTeX Workshop` :
- ouvre le fichier principal `.tex` ;
- lance `LaTeX Workshop: View LaTeX PDF` ;
- sauvegarde pour recompiler ;
- le PDF se met a jour apres chaque compilation reussie.

### 5. Versionner le projet genere

Chaque projet genere est autonome, donc tu peux le versionner separement :

```bash
cd mon-projet
git init
git add .
git commit -m "Initial report"
```

Puis creer un depot GitHub uniquement pour ce projet.

Workflow de collaboration typique :
- creer le projet avec `latex-toolbox` ;
- initialiser Git dans le dossier genere ;
- creer un depot GitHub prive pour ce projet ;
- inviter uniquement les personnes concernees par ce document.

## Templates disponibles

### `rapport-projet-en`

Template de rapport de projet en anglais avec :
- page de garde
- sommaire
- introduction
- conclusion
- notice IA

### `rapport-projet-fr`

Meme structure que `rapport-projet-en`, mais en francais.

### `rapport-ter`

Template academique en anglais pour un rapport de type TER, avec une structure plus riche.

### `research`

Template de type recherche en anglais avec :
- page de garde
- abstract
- sommaire
- corps principal en deux colonnes
- introduction
- conclusion
- appendix
- note sur l'usage de l'IA
- bibliographie BibTeX

## Structure d'un projet genere

Structure typique :

```text
mon-projet/
├── mon-projet.tex
├── frontmatter/
├── sections/
├── backmatter/ ou appendix/
├── references/ ou bibliography/
├── figures/
├── images/
├── screens/
├── assets/
│   ├── images/common/
│   └── logos/
└── styles/packages/
```

Points importants :
- le fichier principal porte le nom du projet ;
- les styles LaTeX sont copies dans le projet ;
- les logos sont copies dans le projet ;
- le projet peut etre partage sans embarquer toute la toolbox.

## Styles modulaires

Les styles sources sont dans :

```text
styles/packages/
```

Principaux fichiers :
- `university-project-report.sty`
- `university-ter-report.sty`
- `research-article.sty`
- `report-metadata.sty`
- `report-tables.sty`
- `report-code-python.sty`
- `report-code-bash.sty`
- `report-colors.sty`
- `report-ter-titlepage.sty`
- `report-theorems-fr.sty`

Quand tu crees un projet, ces styles sont copies localement dans :

```text
styles/packages/
```

du projet genere.

## Assets et logos

Le dossier racine :

```text
assets/logos/
```

sert de source pour les logos copies dans les nouveaux projets.

Dans un projet genere :
- mets les logos dans `assets/logos/`
- mets les images reutilisables dans `assets/images/common/`

## Bibliographie

Le template `research` utilise un fichier BibTeX separe.

Chemin typique :

```text
references/references.bib
```

Tu ajoutes tes references dans ce fichier, puis tu compiles normalement le document.

## Snippets VS Code

Des snippets sont fournis dans :

```text
.vscode/latex.code-snippets
```

Prefixes utiles :
- `ltx-code-py`
- `ltx-code-sh`
- `ltx-fig`
- `ltx-screen`
- `ltx-ai`
- `ltx-toc`

## Faire evoluer la toolbox

Si tu modifies :
- les templates dans `templates/`
- les styles dans `styles/packages/`
- les logos dans `assets/logos/`

alors les futurs projets generes incluront ces changements.

Les projets deja generes ne sont pas modifies automatiquement, car ils embarquent leur propre copie locale.

## Structure du depot

```text
LaTeX/
├── assets/
├── latex_toolbox/
├── projects/
├── scripts/
├── styles/
├── templates/
└── .vscode/
```

Role de chaque dossier :
- `latex_toolbox/` : code Python de la commande
- `templates/` : templates sources
- `styles/` : styles partages de la toolbox
- `assets/` : logos et ressources communes
- `projects/` : endroit pratique si tu veux stocker ici de vrais projets
- `scripts/` : petits wrappers de compatibilite

## Raccourci de commandes

Lister les templates :

```bash
latex-toolbox list-templates
```

Renommer un projet :

```bash
latex-toolbox rename ancien-projet nouveau-projet
```

Verifier la configuration locale :

```bash
latex-toolbox setup --check-only
```

Creer un rapport en anglais :

```bash
latex-toolbox create --name mon-projet --template rapport-projet-en
```

Creer un rapport en francais :

```bash
latex-toolbox create --name mon-projet --template rapport-projet-fr
```

Creer un projet research :

```bash
latex-toolbox create --name paper-audio-search --template research
```

## Resume

LaTeX Toolbox t'aide a :
- creer vite des projets LaTeX bien structures ;
- reutiliser tes styles et tes logos ;
- travailler confortablement dans VS Code ;
- partager chaque projet genere comme depot Git autonome.

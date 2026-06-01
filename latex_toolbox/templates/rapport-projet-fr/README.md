# Template de rapport de projet

Ce projet a ete genere a partir du template `rapport-projet-fr` de LaTeX Toolbox.

Il est pense pour les rapports de cours, comptes-rendus de TP, projets collaboratifs, et plus generalement les documents academiques structures en francais.

## Ce qui est deja inclus

Ce projet contient deja :
- une page de garde
- un sommaire
- une introduction
- une conclusion
- une notice sur l'usage de l'IA
- les styles LaTeX locaux dans `styles/packages/`
- les logos locaux dans `assets/logos/`
- la configuration VS Code dans `.vscode/settings.json`
- un `.gitignore` adapte a LaTeX

Le projet est autonome : tu peux partager uniquement ce dossier et le compiler sans avoir besoin de tout le depot de la toolbox.

## Demarrage rapide

1. Lance le script local de configuration.

macOS / Linux :

```bash
./scripts/setup.sh
```

Windows :

```bat
scripts\setup.bat
```

N'importe quelle plateforme avec Python :

```bash
python3 scripts/setup.py
```

Si tu veux que le script tente aussi d'installer la distribution TeX :

```bash
python3 scripts/setup.py --install-tex
```

Le script :
- installe les extensions VS Code recommandees quand c'est possible
- verifie si les outils LaTeX sont deja presents
- indique quoi installer selon le systeme d'exploitation

2. Ouvre ce dossier dans VS Code.
3. Ouvre le fichier principal :

```text
./NOM_DU_PROJET.tex
```

4. Modifie :
- `frontmatter/metadata.tex`
- `sections/introduction.tex`
- `sections/conclusion.tex`
- `backmatter/ai-statement.tex`

5. Compile avec `LaTeX Workshop`.

## Ce qu'il faut installer

Pour travailler confortablement sur ce projet, chaque collaborateur a besoin de :
- VS Code
- l'extension `LaTeX Workshop`
- une distribution LaTeX installee sur sa machine

Conseil :
- commence par lancer `scripts/setup.py` ou `scripts/setup.sh`

Extensions VS Code recommandees :
- `LaTeX Workshop`
- `LTeX+`
- `Code Spell Checker`

Important :
- si tu utilises `LaTeX Workshop`, desactive `vscode-pdf` pour eviter les conflits de visualisation PDF

## Installation selon le systeme d'exploitation

### macOS

Recommande :
- installer `MacTeX`

Pourquoi :
- il inclut les outils LaTeX standard utilises dans les projets academiques
- il fonctionne tres bien avec `LaTeX Workshop`

Apres installation :
- redemarre VS Code
- verifie dans un terminal :

```bash
latexmk --version
lualatex --version
```

### Windows

Options recommandees :
- `TeX Live`
- ou `MiKTeX`

Si tu veux la solution la plus previsible entre plusieurs collaborateurs, privilegie `TeX Live`.

Si tu veux une installation plus legere avec installation automatique des packages manquants, `MiKTeX` est aussi une bonne option.

Apres installation :
- redemarre VS Code
- verifie dans PowerShell ou l'invite de commandes :

```powershell
latexmk --version
lualatex --version
```

### Linux

Recommande :
- `TeX Live`

Moyens courants de l'installer :
- via le gestionnaire de paquets de ta distribution
- ou via l'installateur officiel TeX Live

Apres installation :
- redemarre VS Code
- verifie dans un terminal :

```bash
latexmk --version
lualatex --version
```

## Premiere compilation dans VS Code

1. Ouvre le fichier principal `.tex`.
2. Lance :

```text
LaTeX Workshop: View LaTeX PDF
```

3. Sauvegarde le fichier pour declencher une recompilation.

Ce projet est configure pour :
- compiler a chaque sauvegarde
- envoyer les fichiers de build dans `build/`
- ouvrir le PDF dans un onglet VS Code

## Si la compilation echoue

Causes frequentes :

1. `latexmk` ou `lualatex` n'est pas installe
- il faut verifier l'installation de la distribution LaTeX

2. Un package manque
- avec `TeX Live`, installe-le avec `tlmgr`
- avec `MiKTeX`, autorise l'installation automatique ou installe-le manuellement

3. VS Code ne voit pas encore les outils LaTeX
- redemarre VS Code
- parfois redemarrer le terminal ou la machine aide aussi

## Structure du projet

```text
.
├── NOM_DU_PROJET.tex
├── frontmatter/
├── sections/
├── backmatter/
├── figures/
├── images/
├── screens/
├── assets/
│   ├── images/common/
│   └── logos/
├── styles/packages/
├── .vscode/settings.json
└── .gitignore
```

## Ou modifier les choses

Modifie les metadata ici :

```text
frontmatter/metadata.tex
```

Modifie le contenu principal ici :

```text
sections/
```

Mets les images reutilisables ici :

```text
assets/images/common/
```

Mets les logos ici :

```text
assets/logos/
```

## Collaboration

Ce projet est prevu pour etre partage comme depot Git autonome.

Workflow typique :

```bash
git init
git add .
git commit -m "Initial report"
```

Ensuite, pousse-le sur GitHub et invite uniquement les personnes qui doivent avoir acces a ce rapport.

Si tu veux creer un depot GitHub prive a partir de ce projet avec la CLI GitHub :

```bash
gh auth login
git init
git add .
git commit -m "Initial report"
git branch -M main
gh repo create nom-du-projet --private --source=. --remote=origin --push
```

Remplace `nom-du-projet` par le nom que tu veux donner au depot sur GitHub.

## References utiles

- extension VS Code LaTeX : LaTeX Workshop
- distributions TeX :
  - macOS : MacTeX
  - multi-plateforme : TeX Live
  - Windows/macOS/Linux : MiKTeX

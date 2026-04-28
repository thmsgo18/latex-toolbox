Template francais pour un TER, inspire du rendu du template `Template_TER_IAD-VMI`
mais recompose pour s'integrer proprement a ce workspace modulaire.

Structure creee par defaut :

- page de garde au style IAD/VMI
- sommaire avec numerotation romaine
- introduction
- etat de l'art
- contribution
- conclusion
- note IA
- bibliographie
- annexes

Points repris du template source :

- page de garde avec logo centre et bloc titre encadre
- structure en chapitres
- style academique sobre
- bibliographie avec `biblatex` et `biber`
- support des theoremes, algorithmes et listings

Adaptations :

- le style principal est isole dans `../../styles/packages/university-ter-report.sty`
- la page de garde est factorisee dans `../../styles/packages/report-ter-titlepage.sty`
- les environnements de theoremes sont centralises dans `../../styles/packages/report-theorems-fr.sty`
- les informations de premiere page sont centralisees dans `frontmatter/metadata.tex`
- les auteurs et encadrants se declarent avec `\addauthor` et `\addteacher`
- la bibliographie vit dans `bibliography/references.bib`
- le contenu est decoupe dans `sections/`, `backmatter/` et `appendices/`
- les dossiers `images/`, `screens/` et `figures/` sont prets

Conseil :

- laisse `main.tex` tres simple
- personnalise d'abord `frontmatter/metadata.tex`
- ajoute ensuite tes chapitres dans `sections/`

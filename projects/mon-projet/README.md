Template anglais base sur ton fichier `main-4.tex`.

Default structure:

- title page
- table of contents
- introduction
- conclusion
- AI notice

Points gardes du template original :

- page de garde
- entetes/pieds de page
- styles de code
- gestion des captures d'ecran
- structure de rapport universitaire
- note sur l'usage de l'IA

Adaptations :

- le style principal est isole dans `../../styles/packages/university-project-report.sty`
- les informations de premiere page sont centralisees dans `frontmatter/metadata.tex`
- les auteurs, enseignants et liens se declarent avec `\addauthor`, `\addteacher` et `\addprojectlink`
- les technologies sont centralisees dans `data/technologies.tex`
- le contenu est decoupe dans `sections/`
- le sommaire est isole dans `frontmatter/toc.tex`
- la notice IA est isolee dans `backmatter/ai-statement.tex`
- les dossiers `images/`, `screens/` et `figures/` sont prets
- les assets communs du workspace restent accessibles

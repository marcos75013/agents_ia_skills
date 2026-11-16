# Versionnement et mises à jour

## Stratégie

Le toolkit utilisera des tags Semantic Versioning lorsque ses premiers artefacts installables seront stables :

- `MAJOR` : changement incompatible de structure, contrat d'installation ou comportement obligatoire ;
- `MINOR` : nouveau standard, skill, agent, modèle ou capacité compatible ;
- `PATCH` : clarification, correction ou amélioration compatible.

Avant ce jalon, les changements restent traçables par commits et pull requests. Un `CHANGELOG.md` sera ajouté lors de la première release, pas avant.

Le manifeste porte dès maintenant une version de toolkit et une version par ressource. Elles servent à comparer source et installation ; elles ne constituent pas encore une release publiée. Les ressources installables commencent en `0.1.0`, le toolkit est en `0.5.1`, `project-audit` en `0.1.1`, et le manifeste reste en schéma `1`. L'installateur enregistre les versions et empreintes réellement installées dans un état local afin de distinguer une mise à jour sûre d'une personnalisation.

## Mise à jour

- Vérifier périodiquement la documentation Codex et les catalogues officiels, car les emplacements et capacités évoluent.
- Modifier une seule source de vérité et mettre à jour ses liens.
- Tester les scripts sur les plateformes ciblées.
- Documenter toute migration et fournir un chemin sans écrasement silencieux.
- Épingler une version du toolkit dans les futurs manifestes de projets ; mettre à jour explicitement après revue du diff.

# Catalogue des skills

Ce dossier contient le **catalogue source**. Un skill n'est créé que lorsqu'un workflow répété, stable et testable le justifie. Chaque skill a son propre dossier et un `SKILL.md` concis, complété par des scripts ou références uniquement si utiles.

## Disponible

- [`project-audit`](project-audit/SKILL.md) : audit factuel et strictement non destructif d'un projet existant ou de plusieurs dépôts coordonnés. Il charge seulement les profils technologiques détectés et sépare faits, constats, recommandations et éléments non vérifiés. Voir le [guide d'utilisation](../docs/project-audit.md).

## Vérification préalable

Avant une implémentation personnalisée :

1. vérifier les skills système et curatés disponibles dans l'environnement Codex ;
2. évaluer leur provenance, leur portée, leurs permissions et leur maintenance ;
3. installer ou adapter une solution fiable si elle couvre le besoin ;
4. créer un skill local seulement si un écart concret subsiste.

L'environnement inspecté fournit notamment les skills système `skill-creator`, `skill-installer` et `openai-docs`, ainsi que des skills officiels pour documents, PDF, présentations et feuilles de calcul. Aucun skill métier disponible dans la session ne couvre directement les standards Flutter, Angular, Spring Boot, Node.js, sécurité, accessibilité ou écoconception listés ci-dessous. Cette observation doit être réévaluée avant chaque développement, car les catalogues évoluent.

## Feuille de route

| Domaine | Skills prévus | Priorité indicative |
| --- | --- | --- |
| Transversal | `new-project`, `feature-delivery`, `security-review`, `accessibility-audit`, `eco-design-review`, `code-review`, `cost-optimizer`, `release-readiness`, `token-optimization` | Revues ciblées après retour sur `project-audit` |
| Flutter | `flutter-clean-architecture`, `flutter-cubit`, `flutter-testing`, `flutter-performance` | Haute pour les nouveaux projets Flutter |
| Angular | `angular-architecture`, `angular-testing`, `angular-performance` | Selon projet pilote |
| Spring Boot | `spring-api-design`, `spring-security-review`, `spring-testing` | Selon projet pilote |
| Node.js | `node-api-design`, `node-security`, `node-testing` | Selon projet pilote |
| Déploiement | `vercel-deploy`, `render-deploy`, `supabase-operations`, `cloudflare-deploy`, `coolify-deploy`, `github-ci-cd` | Après définition des garde-fous CI/CD |

## Critères de création

- Déclencheur et résultat attendus non ambigus.
- Portée étroite, permissions minimales et mode lecture seule quand possible.
- Références versionnées ou vérifiées au moment de l'usage.
- Contrôles déterministes confiés à un script plutôt qu'au modèle.
- Compte rendu court, preuves de vérification et cas d'arrêt explicites.
- Aucun déploiement de production ou achat autonome.

Voir [Installation](../docs/installation.md) pour les cibles compatibles Codex.

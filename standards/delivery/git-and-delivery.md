# Git et qualité de livraison

- Utiliser une branche dédiée par changement cohérent et des commits compréhensibles.
- Livrer par pull request avec contexte, risques, preuves de test et plan de retour arrière si nécessaire.
- Exiger les contrôles automatisés pertinents et une revue humaine selon la criticité.
- Protéger `main` et les environnements de production ; limiter les permissions des tokens et workflows.
- Déclencher les déploiements via des workflows autorisés et auditables.
- Interdire à un agent IA de contourner tests, validations, revues ou protections de branche.
- Conserver un historique traçable des versions, décisions et déploiements.

Les workflows de production ne sont pas fournis dans cette fondation. Ils seront conçus par plateforme avec environnements protégés et approbations explicites.

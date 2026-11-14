# Projets multi-repositories

Chaque dépôt reste autonome : `AGENTS.md`, versions, commandes, skills installés, CI et règles de protection lui sont propres.

## Coordination

Créer dans le projet coordinateur une courte cartographie contenant :

- dépôts et responsables ;
- contrats partagés (API, événements, authentification, schémas) ;
- environnements compatibles ;
- ordre de livraison et stratégie de retour arrière ;
- versions minimales/maximales compatibles ;
- liens vers décisions et pull requests associées.

Pour un changement transversal : analyser les impacts dans chaque dépôt, versionner d'abord les contrats compatibles, livrer par pull requests séparées, vérifier l'intégration puis déployer uniquement via les workflows autorisés. Aucun agent ne doit pousser ou fusionner plusieurs dépôts sans autorisation explicite.

Éviter un `AGENTS.md` central massif : chaque dépôt charge son contexte local ; les standards communs sont référencés ou installés sélectivement.

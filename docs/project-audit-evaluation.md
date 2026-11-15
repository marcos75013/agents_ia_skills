# Évaluer `project-audit`

L'évaluation sépare les invariants déterministes du comportement réel de l'agent. Un test de script ne prouve pas que le modèle interprétera correctement une architecture ou priorisera un risque.

## Contrôles déterministes

Les tests automatisés peuvent vérifier :

- la détection des manifestes Flutter, Angular, Spring Boot, Node.js et multi-technologies ;
- l'élagage des dépendances et sorties générées ;
- la tolérance aux repositories incomplets et manifestes invalides ;
- l'absence d'écriture du détecteur et des prévisualisations d'installation ;
- les destinations, conflits, frontmatter, métadonnées et liens ;
- la présence dans le skill des catégories Fact, Finding, Recommendation et Unverified.

Ces tests valident des mécanismes et des contrats d'instructions, pas l'obéissance complète d'un modèle.

## Évaluation réelle de l'agent

Utiliser un dépôt propre et autorisé, puis conserver son commit de départ. Demander un audit en lecture seule, relire chaque preuve et vérifier :

1. que les versions proviennent de fichiers ou sorties identifiables ;
2. que l'architecture décrite correspond aux dépendances observées ;
3. qu'une architecture sans Cubit n'entraîne pas automatiquement une recommandation de migration ;
4. que les incertitudes et contrôles non exécutés sont explicites ;
5. que priorité, impact, effort et risque du changement sont proportionnés ;
6. que le statut Git et l'empreinte des fichiers sont inchangés après l'audit.

Un deuxième évaluateur humain ou agent peut noter exactitude des preuves, pertinence, couverture des risques et concision sans recevoir les conclusions attendues à l'avance.

## Mesures comparables

Lorsque l'environnement les expose, relever : fichiers inventoriés, fichiers ouverts en détail, commandes, durée et lectures répétées. Mesurer les tokens uniquement avec une métrique fournie par la plateforme. Pour comparer deux versions, garder dépôt, commit, demande et périmètre constants ; ne pas réduire les lectures si cela supprime une preuve nécessaire.

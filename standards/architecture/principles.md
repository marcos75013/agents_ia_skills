# Architecture et qualité

## Principes

- Séparer clairement responsabilités, règles métier, orchestration et infrastructure.
- Appliquer SOLID, DRY et KISS comme guides de décision, pas comme objectifs abstraits.
- Préférer la solution la plus simple qui reste testable, observable et évolutive.
- Introduire une abstraction ou une injection de dépendances seulement lorsqu'elle clarifie une frontière, facilite un test ou permet plusieurs implémentations plausibles.
- Rendre les erreurs explicites : contexte utile, traitement au bon niveau et aucune exception silencieusement ignorée.
- Éviter les dépendances cycliques et orienter les dépendances vers les règles métier lorsqu'une architecture en couches est justifiée.

## Choix proportionnés

Avant de choisir une architecture, documenter : taille et durée de vie prévues, criticité, équipe, fréquence d'évolution, intégrations, contraintes de performance et stratégie de tests. Un prototype réversible ne nécessite pas la même structure qu'un produit critique.

Pour un projet existant, cartographier d'abord les modules, flux, dépendances et tests. Toute migration doit être incrémentale, motivée par un problème observable et couverte par des contrôles de non-régression.

## Définition de terminé

Une modification est lisible, testée au niveau pertinent, documentée si son usage ou une décision change, vérifiée par les outils du projet et accompagnée d'une gestion d'erreur adaptée. Les compromis connus sont tracés.

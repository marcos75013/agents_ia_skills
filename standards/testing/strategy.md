# Stratégie de tests

Construire une pyramide adaptée au risque : beaucoup de tests rapides sur la logique, des tests d'intégration sur les frontières et quelques parcours fonctionnels critiques.

- Tester le comportement observable, les erreurs et les cas limites plutôt que les détails d'implémentation.
- Garder les tests déterministes, indépendants et lisibles.
- Utiliser de vraies intégrations contrôlées lorsque les mocks masqueraient un contrat important.
- Ajouter un test de non-régression pour chaque défaut corrigé lorsque raisonnable.
- Séparer les suites rapides obligatoires des suites longues, sans permettre de contourner les validations requises avant production.
- Mesurer la couverture comme signal, jamais comme objectif suffisant.

Chaque projet documente ses commandes de test, prérequis, données de test, seuils et responsabilités en cas d'échec intermittent.

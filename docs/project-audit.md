# Utiliser `project-audit`

Le skill analyse un projet existant sans le modifier. Il établit d'abord les faits, approfondit les zones à risque, puis propose des améliorations et les ressources IA pertinentes. Son rapport n'est ni une certification de conformité ni une autorisation de modifier le projet.

## Déclenchement

Après [installation](installation.md), ouvrir Codex à la racine du projet et demander :

```text
Utilise $project-audit pour auditer ce projet en lecture seule. Priorise sécurité, accessibilité, coûts et actions à faible effort.
```

L'invocation explicite est recommandée pour cadrer clairement une mission complète, même si la description permet aussi une sélection automatique du skill.

Pour plusieurs dépôts, fournir leurs chemins ou accès autorisés et préciser le dépôt coordinateur. Chaque dépôt conserve ses propres faits ; le rapport système ajoute seulement les contrats et dépendances de livraison observés.

## Déroulement

1. **Découverte** : instructions, manifests, versions, applications, composants et CI/CD.
2. **Analyse** : architecture, qualité, tests, sécurité, accessibilité, écoconception, performance, livraison et coûts.
3. **Diagnostic** : faits, constats, recommandations et éléments non vérifiés sont séparés. Les actions reçoivent priorité, effort et risque de changement.
4. **Intégration IA** : propositions d'`AGENTS.md`, de skills, d'agents spécialisés, de CI et de routage économe en tokens. Aucun de ces fichiers n'est créé pendant l'audit.

Le détecteur optionnel `scripts/detect_project.py` du skill inventorie uniquement les manifests. Il ne lance aucun outil du projet et son résultat doit être vérifié par l'auditeur.

## État opérationnel

Sont opérationnels : les instructions d'audit, le routage progressif vers les quatre profils, l'inventaire statique des manifests, le format de rapport, les contrôles du toolkit ainsi que l'installation et la mise à jour sécurisées avec prévisualisation, état, sauvegardes et détection des conflits.

Restent volontairement manuels ou non implémentés : l'exécution des tests propres au projet audité, la consultation des prix/quota externes, la génération d'`AGENTS.md`, les agents Architect et Security Auditor, et toute modification ou livraison du projet. Le sous-agent Code Reviewer est disponible séparément. `project-audit` guide Codex ; ce n'est pas un scanner autonome garantissant une couverture exhaustive.

## Lecture du rapport

- **Fact** : preuve directe dans un fichier, une configuration ou une sortie de version.
- **Finding** : interprétation des faits et de leur impact.
- **Recommendation** : prochaine action proportionnée et contrôle de réussite.
- **Unverified** : point pertinent qui n'a pas pu être observé ou vérifié sans risque.

`P0` est réservé à une menace ou panne immédiate et crédible ; `P1` désigne un risque élevé à court terme, `P2` une amélioration planifiée et `P3` une optimisation optionnelle. Les coûts ou quotas évolutifs doivent être sourcés et datés, sinon ils restent non vérifiés.

## Exemple Flutter

Demande :

```text
Utilise $project-audit sur cette application Flutter. Compare objectivement l'architecture observée à notre cible feature-first Clean Architecture avec Cubit, sans modifier le code ni proposer une migration automatique. Vérifie aussi les tests, l'accessibilité, les performances et le pipeline de release.
```

Le profil Flutter vérifie notamment les contraintes Flutter/Dart, plateformes, entry points, state management, navigation, injection, persistance, réseau et génération de code. Il compare ensuite les dépendances observées avec la cible `presentation` / `domain` / `data`, use cases et repositories, mais ne transforme pas un simple écart de structure en problème sans impact démontré.

Les profils Angular, Spring Boot et Node.js suivent la même logique : versions réelles d'abord, règles propres à la technologie ensuite. Un workspace mixte charge chaque profil correspondant.

## Réutiliser le résultat

Après validation humaine du rapport, lancer une tâche distincte pour créer ou modifier les instructions du projet. Fournir seulement les constats retenus, les commandes vérifiées et les contraintes durables. Garder `AGENTS.md` court ; confier les workflows détaillés à des skills et les contrôles déterministes au lint, aux tests ou à la CI.

Le sous-agent Code Reviewer est disponible. Architect et Security Auditor restent sur la [feuille de route](../agents/README.md) et ne seront créés qu'après des audits réels montrant un besoin de spécialisation.

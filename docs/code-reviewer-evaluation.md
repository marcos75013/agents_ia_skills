# Évaluer Code Reviewer

Les cas versionnés dans [`tests/fixtures/code-review/cases.json`](../tests/fixtures/code-review/cases.json) séparent les contrôles déterministes de l'évaluation comportementale par un modèle.

## Contrôles déterministes automatisés

La CI vérifie :

- la syntaxe TOML et les trois champs Codex requis ;
- l'absence de réglages de sandbox trompeurs dans le fichier agent ;
- la désactivation des demandes de permissions ;
- le contrat de lecture seule, de sélection du diff et de rapport ;
- les destinations projet et utilisateur du manifeste ;
- les conflits et l'absence d'écriture du mode de prévisualisation ;
- la présence de cas Flutter, Angular, Spring Boot, Node.js, de bugs connus et de diffs propres.

Ces tests ne prouvent pas qu'un modèle trouvera le bug, évitera tous les faux positifs ou respectera toujours les instructions.

## Évaluation comportementale manuelle

Pour chaque cas, lancer une nouvelle session avec le même modèle et le même niveau de raisonnement, installer l'agent dans un projet temporaire, puis demander une revue du seul diff. Relever sans corriger le cas :

1. constat attendu détecté ou manqué ;
2. gravité, ligne et certitude correctement étayées ;
3. faux positifs sur les cas `clean` ;
4. fichiers ouverts au-delà du diff et justification ;
5. commandes exécutées et toute tentative d'écriture ;
6. tokens uniquement si la plateforme fournit cette mesure.

Un résultat est acceptable quand tous les défauts majeurs attendus sont détectés, qu'aucun constat injustifié n'est produit sur les cas propres et qu'aucune écriture ou commande projet inconnue n'a lieu. Ce seuil est une cible d'évaluation, pas un résultat observé dans cette mission.

## Cas représentatifs et limites

Les fixtures comprennent un calcul erroné dans un Cubit Flutter, un identifiant de suppression incorrect dans un service Angular, une autorisation inversée dans Spring Boot et une double réponse possible dans une route Node.js. Deux diffs propres vérifient la capacité à rendre « aucune anomalie justifiée ».

Les cas sont synthétiques et courts. Ils ne couvrent pas les interactions distribuées, les migrations de données, les problèmes de concurrence complexes, les dépendances vulnérables ou les comportements visibles uniquement à l'exécution. Aucun appel réel à un modèle n'a été automatisé ici : les tests CI valident le contrat et les fixtures, pas la qualité sémantique du reviewer.

## Vérifier une conclusion

Revenir à la ligne citée, confirmer qu'elle appartient au diff, lire le contrat ou l'appelant utilisé comme preuve, puis tenter de réfuter l'impact. Une conclusion qui dépend d'une hypothèse non observable doit être abaissée en certitude ou déplacée vers les vérifications résiduelles.

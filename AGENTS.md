# Instructions de maintenance

## Portée

Ce dépôt contient les sources d'un toolkit réutilisable. Ne confonds pas `skills/` et `agents/` avec leurs cibles d'installation Codex documentées dans `docs/codex-compatibility.md`.

## Règles

- Inspecter l'état Git et les fichiers concernés avant toute modification.
- Préserver les personnalisations locales ; ne jamais écraser silencieusement un fichier cible.
- Garder les règles transversales indépendantes des frameworks et placer les exceptions dans les profils technologiques.
- Vérifier les versions réelles d'un projet avant de recommander une API ou un pattern.
- Pour Flutter neuf : Clean Architecture feature-first, couches `presentation`, `domain`, `data`, Cubit avec `flutter_bloc`, use cases et repositories du Domain. Ne pas proposer Riverpod par défaut.
- Pour un projet existant : auditer avant toute proposition de migration.
- Ne jamais déployer en production, pousser, fusionner, activer une ressource payante ou manipuler des secrets sans autorisation explicite.
- Utiliser un agent spécialisé seulement si sa portée apporte une valeur nette ; les audits doivent pouvoir rester en lecture seule.
- Éviter les dépendances et fichiers vides sans utilité vérifiable.

## Validation

Avant livraison, exécuter :

```bash
python3 scripts/check_toolkit.py
git diff --check
```

Relire les liens, les éventuels secrets, la cohérence avec `README.md` et l'état Git final.

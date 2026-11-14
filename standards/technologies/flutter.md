# Profil Flutter / Dart

## Nouveau projet

Standard par défaut : Clean Architecture, organisation feature-first et gestion d'état par Cubit avec `flutter_bloc`.

```text
lib/features/<feature>/
├── presentation/
├── domain/
└── data/
```

- `presentation` contient UI, Cubits et états sans logique d'infrastructure.
- `domain` contient entités, use cases et interfaces de repositories ; il ne dépend pas de Flutter ni de `data`.
- `data` contient modèles, sources de données, mappings et implémentations de repositories.
- L'injection de dépendances assemble les implémentations aux frontières de l'application.
- Tester Cubits, use cases, mappings et repositories ; ajouter widgets et intégrations selon les risques.

Riverpod n'est pas proposé par défaut. Pour un projet existant, analyser d'abord son architecture, ses conventions et sa dette ; ne pas lancer de migration automatique.

Vérifier les versions de Flutter, Dart, `flutter_bloc`, les plateformes cibles et contraintes d'accessibilité/performance avant toute recommandation détaillée.

# Scripts

Les scripts automatisent les contrôles déterministes afin de réduire erreurs et consommation de tokens.

```bash
python3 scripts/check_toolkit.py
```

Le contrôle utilise uniquement la bibliothèque standard Python. Il vérifie les fichiers requis, fichiers vides, liens Markdown locaux, marqueurs de conflit, formes courantes de secrets, manifeste, skills et configuration TOML de Code Reviewer. Il ne remplace pas une revue humaine ni un scanner de secrets spécialisé.

Les autres scripts sans dépendance externe sont :

- `install_toolkit.py` prévisualise, installe et met à jour les ressources globales ou locales avec état, empreintes, sauvegardes, rollback et refus des personnalisations conflictuelles ;
- `skills/project-audit/scripts/detect_project.py` inventorie les manifests représentatifs d'un projet audité sans exécuter son code.

Les scénarios synthétiques sont documentés dans [`tests/`](../tests/README.md).

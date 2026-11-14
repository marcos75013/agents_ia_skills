# Scripts

Les scripts automatisent les contrôles déterministes afin de réduire erreurs et consommation de tokens.

```bash
python3 scripts/check_toolkit.py
```

Le contrôle utilise uniquement la bibliothèque standard Python. Il vérifie les fichiers requis, fichiers vides, liens Markdown locaux, marqueurs de conflit et formes courantes de secrets. Il ne remplace pas une revue humaine ni un scanner de secrets spécialisé.

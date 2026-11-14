# Socle de sécurité

Appliquer les recommandations OWASP pertinentes à la technologie et au modèle de menace réel.

## Exigences minimales

- Valider et normaliser les entrées aux frontières de confiance ; encoder les sorties selon leur contexte.
- Appliquer authentification robuste, autorisation côté serveur et moindre privilège.
- Stocker les secrets dans un gestionnaire ou les variables protégées de la plateforme, jamais dans Git, les builds clients ou les logs.
- Chiffrer les données sensibles en transit et, lorsque nécessaire, au repos.
- Minimiser les données personnelles, définir leur durée de conservation et permettre leur suppression.
- Journaliser les événements utiles sans mots de passe, jetons, clés, données personnelles excessives ou corps sensibles.
- Épingler et analyser les dépendances ; traiter les vulnérabilités selon exploitabilité et impact.
- Protéger les workflows CI/CD : permissions minimales, environnements protégés, validation des entrées et dépendances d'actions figées.

## Revue

Identifier les actifs, acteurs, frontières de confiance, scénarios d'abus et mesures compensatoires. Toute exception doit avoir un propriétaire, une justification et une date de réévaluation. Une analyse automatisée complète la revue humaine sans la remplacer.

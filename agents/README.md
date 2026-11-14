# Agents spécialisés

Codex reste l'agent principal. Un agent spécialisé n'est introduit que si une mission étroite, des instructions propres ou une exécution parallèle apportent un bénéfice mesurable.

## Feuille de route limitée

| Agent | Rôle | Mode par défaut |
| --- | --- | --- |
| Architect | Cartographier l'architecture, les dépendances et les impacts ; proposer des options. | Lecture seule pendant l'analyse |
| Reviewer | Rechercher défauts, régressions, manque de tests et incohérences du diff. | Lecture seule |
| Security Auditor | Évaluer menaces, entrées, autorisations, secrets et dépendances. | Lecture seule |

Les audits produisent des constats sourcés et ne modifient pas le code sauf demande distincte. Les instructions seules ne créent pas un sandbox en lecture seule : les permissions de la session doivent aussi être configurées en conséquence.

## Source et installation

Les futures définitions source seront maintenues ici, relues et versionnées. L'installation copiera explicitement un fichier TOML validé vers :

- `.codex/agents/<nom>.toml` pour un projet ;
- `$HOME/.codex/agents/<nom>.toml` pour l'environnement personnel.

Aucun agent personnalisé n'est créé dans cette mission : son modèle, ses outils et ses permissions doivent être décidés avec un cas d'usage réel.

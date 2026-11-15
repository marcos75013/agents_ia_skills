# Agents spécialisés

Codex reste l'agent principal. Un agent spécialisé n'est introduit que si une mission étroite, des instructions propres ou une exécution parallèle apportent un bénéfice mesurable.

## Feuille de route limitée

| Agent | Responsabilité et déclencheur | Ressources possibles | Permissions | Rapport | Coût de contexte attendu |
| --- | --- | --- | --- | --- | --- |
| Architect | Cartographier les frontières et options avant une évolution transversale ou une décision difficile à inverser. | `project-audit`, standards d'architecture et profil technologique. | Lecture seule ; aucun shell d'écriture. | Options, preuves, compromis, impacts et décision à valider. | Élevé : plusieurs modules et contrats doivent être comparés. |
| [Code Reviewer](code-reviewer.toml) | Examiner un diff significatif pour bugs, régressions, tests manquants et incohérences. | Le diff, ses tests et seulement le contexte adjacent nécessaire. | Lecture seule sur code et diff ; tests seulement sur demande distincte. | Gravité, fichier/ligne, problème, impact, recommandation et certitude. | Faible à moyen si le diff borne le périmètre. |
| Security Auditor | Examiner une surface d'authentification, de données sensibles, d'entrées externes ou une préparation de release. | `project-audit`, baseline sécurité et profil technologique. | Lecture seule renforcée ; ne pas lire les valeurs de secrets ni accéder à la production. | Menaces, preuves, exploitabilité, sévérité, remédiation et vérification. | Moyen à élevé selon les frontières de confiance. |

Les audits produisent des constats sourcés et ne modifient pas le code sauf demande distincte. Les instructions seules ne créent pas un sandbox en lecture seule : les permissions de la session doivent aussi être configurées en conséquence.

## Source et installation

Les définitions source sont maintenues ici, relues et versionnées. L'installation de Code Reviewer copie explicitement un fichier TOML validé vers :

- `.codex/agents/<nom>.toml` pour un projet ;
- `$HOME/.codex/agents/<nom>.toml` pour l'environnement personnel.

Code Reviewer est le seul agent implémenté. Architect et Security Auditor restent au stade de la feuille de route. Voir son [guide d'utilisation](../docs/code-reviewer.md) et son [protocole d'évaluation](../docs/code-reviewer-evaluation.md).

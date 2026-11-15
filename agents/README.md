# Agents spécialisés

Codex reste l'agent principal. Un agent spécialisé n'est introduit que si une mission étroite, des instructions propres ou une exécution parallèle apportent un bénéfice mesurable.

## Feuille de route limitée

| Agent | Responsabilité et déclencheur | Ressources possibles | Permissions | Rapport | Coût de contexte attendu |
| --- | --- | --- | --- | --- | --- |
| Architect | Cartographier les frontières et options avant une évolution transversale ou une décision difficile à inverser. | `project-audit`, standards d'architecture et profil technologique. | Lecture seule ; aucun shell d'écriture. | Options, preuves, compromis, impacts et décision à valider. | Élevé : plusieurs modules et contrats doivent être comparés. |
| Code Reviewer | Examiner un diff significatif pour bugs, régressions, tests manquants et incohérences. | Standards qualité/tests et, seulement si nécessaire, profil technologique. | Lecture seule sur code et diff ; tests sûrs uniquement si autorisés. | Constats priorisés par fichier/ligne, puis risques résiduels. | Faible à moyen si le diff et les appels concernés bornent le périmètre. |
| Security Auditor | Examiner une surface d'authentification, de données sensibles, d'entrées externes ou une préparation de release. | `project-audit`, baseline sécurité et profil technologique. | Lecture seule renforcée ; ne pas lire les valeurs de secrets ni accéder à la production. | Menaces, preuves, exploitabilité, sévérité, remédiation et vérification. | Moyen à élevé selon les frontières de confiance. |

Les audits produisent des constats sourcés et ne modifient pas le code sauf demande distincte. Les instructions seules ne créent pas un sandbox en lecture seule : les permissions de la session doivent aussi être configurées en conséquence.

## Source et installation

Les futures définitions source seront maintenues ici, relues et versionnées. L'installation copiera explicitement un fichier TOML validé vers :

- `.codex/agents/<nom>.toml` pour un projet ;
- `$HOME/.codex/agents/<nom>.toml` pour l'environnement personnel.

Aucun agent personnalisé n'est créé dans cette mission. Le pilote confirme qu'un **Code Reviewer** minimal serait le premier candidat utile : son entrée peut être limitée à un diff, aux tests associés et à quelques fichiers appelés, ce qui réduit le contexte. Sa création doit rester une PR séparée avec des essais sur de vrais diffs avant d'ajouter Architect ou Security Auditor.

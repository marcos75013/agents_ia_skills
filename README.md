# AI Dev Toolkit

Bibliothèque personnelle et évolutive de standards de développement, de ressources Codex, de modèles et d'automatisations GitHub.

Le toolkit vise des projets Flutter/Dart, Angular/TypeScript, Java/Spring Boot, Node.js et, à terme, Swift/SwiftUI. Il privilégie la qualité, la sécurité, l'accessibilité, l'écoconception et un coût d'infrastructure nul ou minimal.

## Principes

- Adapter l'architecture à la complexité réelle du produit.
- Mutualiser les règles transversales sans imposer les mêmes patterns à toutes les technologies.
- Inspecter un projet existant avant de proposer une évolution structurelle.
- Garder les instructions Codex courtes et charger les workflows spécialisés à la demande.
- Automatiser les contrôles déterministes et conserver une validation humaine pour les décisions sensibles.
- Ne jamais déployer en production, activer une ressource payante ou exposer un secret sans autorisation explicite.

## Organisation

| Dossier | Rôle |
| --- | --- |
| [`standards/`](standards/README.md) | Référentiel commun et profils technologiques. |
| [`skills/`](skills/README.md) | Catalogue et futures sources des skills réutilisables. |
| [`agents/`](agents/README.md) | Politique et feuille de route des agents spécialisés. |
| [`templates/`](templates/README.md) | Modèles de cadrage, d'audit et d'instructions projet. |
| [`docs/`](docs/codex-compatibility.md) | Compatibilité Codex, installation, synchronisation et versionnement. |
| [`workflows/`](workflows/README.md) | Conception des futurs workflows GitHub réutilisables. |
| [`scripts/`](scripts/README.md) | Contrôles locaux déterministes et sans dépendance externe. |
| [`toolkit-manifest.json`](toolkit-manifest.json) | Ressources installables, versions, technologies et cibles. |

Cette arborescence est la **source** du toolkit. Elle est distincte des emplacements découverts par Codex :

- instructions projet : `AGENTS.md` ;
- skills partagés par un projet : `.agents/skills/<nom>/SKILL.md` ;
- skills personnels : `$HOME/.agents/skills/<nom>/SKILL.md` ;
- agents projet : `.codex/agents/<nom>.toml` ;
- agents personnels : `$HOME/.codex/agents/<nom>.toml`.

Voir [Compatibilité avec Codex](docs/codex-compatibility.md) pour les nuances liées à l'installateur local.

## Utilisation

1. Lire les [standards transversaux](standards/README.md).
2. Choisir uniquement les profils technologiques et ressources nécessaires.
3. Pour un nouveau projet, compléter le [modèle de cadrage](templates/new-project/PROJECT_BRIEF.md).
4. Pour un projet existant, utiliser [`project-audit`](docs/project-audit.md) ; le modèle d'audit reste utile pour préparer le contexte métier.
5. Installer les ressources selon le [guide d'installation](docs/installation.md).
6. Exécuter `python3 scripts/check_toolkit.py` avant une pull request.

Les projets multi-repositories suivent le guide de [coordination inter-repositories](docs/multi-repository.md). La politique de versions et de mises à jour est décrite dans [Versionnement](docs/versioning.md).

## État actuel

Le premier skill métier, [`project-audit`](skills/project-audit/SKILL.md), audite un projet en lecture seule avec des profils Flutter, Angular, Spring Boot et Node.js chargés à la demande. Un manifeste versionné et un installateur limité à la prévisualisation préparent sa distribution sans écrasement. Aucun agent spécialisé actif, workflow de déploiement ou service payant n'est ajouté.

## Références Codex

- [Instructions avec `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Skills Codex](https://learn.chatgpt.com/docs/build-skills)
- [Sous-agents et agents personnalisés](https://learn.chatgpt.com/docs/agent-configuration/subagents)

# Compatibilité avec Codex

Vérification actualisée le 14 novembre 2026 à partir de la documentation officielle Codex.

## Surfaces reconnues

| Besoin | Source dans ce toolkit | Cible reconnue par Codex |
| --- | --- | --- |
| Instructions durables du dépôt | `AGENTS.md` et modèle sous `templates/` | `AGENTS.md`, avec fichiers plus spécifiques dans les sous-dossiers si nécessaire |
| Skill partagé | futur dossier sous `skills/` | `.agents/skills/<nom>/SKILL.md` |
| Skill personnel | futur dossier sous `skills/` | `$HOME/.agents/skills/<nom>/SKILL.md` |
| Agent projet | future définition sous `agents/` | `.codex/agents/<nom>.toml` |
| Agent personnel | future définition sous `agents/` | `$HOME/.codex/agents/<nom>.toml` |
| Configuration projet | non fournie par défaut | `.codex/config.toml` dans un dépôt approuvé |
| Workflow GitHub actif | source validée au cas par cas | `.github/workflows/<nom>.yml` |

`AGENTS.md` est chargé automatiquement ; une instruction plus proche du dossier de travail est plus spécifique. Il doit rester court et opérationnel.

## Nuance d'installation des skills

La documentation actuelle reconnaît `.agents/skills` dans le dépôt et `$HOME/.agents/skills` pour l'utilisateur. Des versions antérieures ou certains helpers peuvent encore utiliser `$CODEX_HOME/skills` (souvent `$HOME/.codex/skills`). Le script du toolkit suit les emplacements actuels, annonce sa cible et reste limité à une prévisualisation ; une future écriture devra détecter explicitement tout environnement historique au lieu d'écrire dans les deux emplacements.

## Agents et lecture seule

Une définition d'agent peut limiter ses capacités et préciser une mission d'audit, mais ses instructions ne suffisent pas à garantir un sandbox en lecture seule. La session parente et sa politique de permissions restent déterminantes. Les agents héritent notamment des permissions et intégrations de leur parent.

## Références officielles

- [Instructions `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Création et emplacements des skills](https://learn.chatgpt.com/docs/build-skills)
- [Sous-agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

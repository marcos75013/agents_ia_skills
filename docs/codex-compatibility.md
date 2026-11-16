# Compatibilité avec Codex

Vérification actualisée le 15 novembre 2026 à partir de la documentation officielle Codex.

## Surfaces reconnues

| Besoin | Source dans ce toolkit | Cible reconnue par Codex |
| --- | --- | --- |
| Instructions durables du dépôt | `AGENTS.md` et modèle sous `templates/` | `AGENTS.md`, avec fichiers plus spécifiques dans les sous-dossiers si nécessaire |
| Skill partagé | futur dossier sous `skills/` | `.agents/skills/<nom>/SKILL.md` |
| Skill personnel | futur dossier sous `skills/` | `$HOME/.agents/skills/<nom>/SKILL.md` |
| Agent projet | `agents/code-reviewer.toml` | `.codex/agents/code-reviewer.toml` |
| Agent personnel | `agents/code-reviewer.toml` | `$HOME/.codex/agents/code-reviewer.toml` |
| Configuration projet | non fournie par défaut | `.codex/config.toml` dans un dépôt approuvé |
| Workflow GitHub actif | source validée au cas par cas | `.github/workflows/<nom>.yml` |

`AGENTS.md` est chargé automatiquement ; une instruction plus proche du dossier de travail est plus spécifique. Il doit rester court et opérationnel.

## Nuance d'installation des skills

La documentation actuelle reconnaît `.agents/skills` dans le dépôt et `$HOME/.agents/skills` pour l'utilisateur. Des versions antérieures ou certains helpers peuvent encore utiliser `$CODEX_HOME/skills` (souvent `$HOME/.codex/skills`). Le script du toolkit suit les emplacements actuels, annonce sa cible et permet la prévisualisation, l'installation et la mise à jour contrôlée. Il n'écrit pas simultanément dans les emplacements actuels et historiques ; toute cible existante différente est traitée comme un conflit.

## Agents et lecture seule

Une définition d'agent doit fournir `name`, `description` et `developer_instructions`. Elle peut limiter certaines capacités, mais ses instructions ne suffisent pas à garantir un sandbox en lecture seule. La session parente et sa politique de permissions restent déterminantes. Les agents héritent notamment des permissions et intégrations de leur parent ; `sandbox_mode` ou `approval_policy` dans le fichier agent ne les remplacent pas.

## Références officielles

- [Instructions `AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Création et emplacements des skills](https://learn.chatgpt.com/docs/build-skills)
- [Sous-agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

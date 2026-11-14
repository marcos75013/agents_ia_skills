# Installation et réutilisation

Cette fondation documente l'installation ; elle ne copie encore aucune ressource automatiquement.

## Installation globale

Utiliser pour des workflows personnels stables et indépendants d'un projet :

1. sélectionner un skill ou agent source validé ;
2. contrôler son contenu, ses scripts, permissions et dépendances ;
3. comparer la cible avec la version de Codex installée ;
4. copier dans `$HOME/.agents/skills/<nom>/` ou `$HOME/.codex/agents/<nom>.toml` ;
5. démarrer une nouvelle session si la découverte n'est pas dynamique ;
6. conserver la version source installée dans un manifeste futur.

Le helper officiel `skill-installer` peut cibler `$CODEX_HOME/skills` selon l'installation. Voir [Compatibilité Codex](codex-compatibility.md).

## Installation par projet

Sélectionner le socle commun, puis uniquement les ressources utiles :

| Projet | Sélection type |
| --- | --- |
| Flutter | standards communs + profil Flutter + futurs skills Clean Architecture/Cubit/tests |
| Angular | standards communs + profil Angular |
| Spring Boot | standards communs + profil Spring Boot |
| Angular + Node.js | standards communs + profils Angular et Node.js |

Les skills validés sont copiés vers `.agents/skills/<nom>/`, les agents vers `.codex/agents/` et le modèle d'instructions devient un `AGENTS.md` adapté au dépôt. Ne pas copier tout le catalogue.

## Synchronisation sans écrasement

Une future commande d'installation devra :

1. générer un plan et un diff avant écriture ;
2. comparer version source, version installée et modifications locales ;
3. refuser par défaut l'écrasement d'un fichier modifié ;
4. proposer mise à jour, conservation ou fusion manuelle ;
5. sauvegarder un manifeste des ressources et versions installées ;
6. rester idempotente et offrir un mode `--check` sans écriture.

En attendant cet outil, les mises à jour sont manuelles et passent par une pull request dans chaque projet cible.

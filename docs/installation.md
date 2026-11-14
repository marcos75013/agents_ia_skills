# Installation et réutilisation

Le manifeste [`toolkit-manifest.json`](../toolkit-manifest.json) décrit les ressources installables, leur version, leurs technologies et leurs cibles. Le premier script d'installation est volontairement limité à la prévisualisation : il ne copie ni ne remplace aucun fichier.

## Installation globale

Utiliser pour des workflows personnels stables et indépendants d'un projet :

1. sélectionner un skill ou agent source validé ;
2. contrôler son contenu, ses scripts, permissions et dépendances ;
3. comparer la cible avec la version de Codex installée ;
4. copier dans `$HOME/.agents/skills/<nom>/` ou `$HOME/.codex/agents/<nom>.toml` ;
5. démarrer une nouvelle session si la découverte n'est pas dynamique ;
6. conserver la version source installée dans un manifeste futur.

Le helper officiel `skill-installer` peut cibler `$CODEX_HOME/skills` selon l'installation. Voir [Compatibilité Codex](codex-compatibility.md).

Pour prévisualiser `project-audit` dans l'environnement personnel :

```bash
python3 scripts/install_toolkit.py --dry-run --scope user --resource project-audit
```

## Installation par projet

Sélectionner le socle commun, puis uniquement les ressources utiles :

| Projet | Sélection type |
| --- | --- |
| Flutter | standards communs + profil Flutter + futurs skills Clean Architecture/Cubit/tests |
| Angular | standards communs + profil Angular |
| Spring Boot | standards communs + profil Spring Boot |
| Angular + Node.js | standards communs + profils Angular et Node.js |

Après une prévisualisation sans conflit, une installation **manuelle** peut copier le dossier source complet `skills/project-audit/` vers `.agents/skills/project-audit/`. Arrêter si la cible existe ; ne pas fusionner ou remplacer son contenu. Les futurs agents iront sous `.codex/agents/` et le modèle d'instructions pourra devenir un `AGENTS.md` adapté au dépôt. Ne pas copier tout le catalogue.

Depuis le toolkit, prévisualiser une installation locale sans écrire :

```bash
python3 scripts/install_toolkit.py --check --scope project --target /chemin/du/projet --resource project-audit
```

Ajouter `--technology flutter`, `angular`, `spring-boot`, `nodejs` ou `multi-technology` pour filtrer les ressources compatibles. Le mode `--check` retourne un code non nul si une cible existe avec un contenu différent ; `--dry-run` affiche le même plan mais reste informatif. Les deux modes sont sans écriture dans cette première version.

## Synchronisation sans écrasement

Une future version avec écriture devra :

1. générer un plan et un diff avant écriture ;
2. comparer version source, version installée et modifications locales ;
3. refuser par défaut l'écrasement d'un fichier modifié ;
4. proposer mise à jour, conservation ou fusion manuelle ;
5. sauvegarder un manifeste des ressources et versions installées ;
6. rester idempotente et offrir un mode `--check` sans écriture.

En attendant cette version, effectuer la copie manuellement après revue du plan. Une cible différente est signalée `CONFLICT` et ne doit jamais être remplacée silencieusement. Les mises à jour passent par une pull request dans chaque projet cible.

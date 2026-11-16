# Installation et mise à jour

Le manifeste [`toolkit-manifest.json`](../toolkit-manifest.json) décrit les ressources, leurs versions, technologies et destinations. L'installateur utilise uniquement la bibliothèque standard Python et sépare toujours le plan de l'écriture.

## Règles de sécurité

- `--check` et `--dry-run` ne modifient aucun fichier.
- `--install` crée les ressources absentes et peut enregistrer une cible déjà strictement identique.
- `--install` refuse une mise à jour ; celle-ci nécessite `--update` explicitement.
- `--update` remplace uniquement une cible gérée dont l'empreinte correspond encore à la dernière installation.
- Une cible inconnue, personnalisée, symbolique ou située hors du dossier cible est refusée.
- Tout le plan est contrôlé avant la première écriture ; un conflit annule l'ensemble.
- Une mise à jour conserve l'ancienne ressource sous `.codex/toolkit-backups/`.
- L'état géré est enregistré dans `.codex/agents-ia-toolkit-state.json` par écriture atomique.

L'installateur ne fusionne pas des personnalisations. Si un conflit est signalé, comparer les versions et effectuer la fusion dans une branche séparée.

## Installation dans un projet

Depuis la racine du toolkit, prévisualiser les deux ressources :

```bash
python3 scripts/install_toolkit.py \
  --check \
  --scope project \
  --target /chemin/du/projet \
  --resource project-audit \
  --resource code-reviewer
```

Après lecture du plan, appliquer la première installation :

```bash
python3 scripts/install_toolkit.py \
  --install \
  --scope project \
  --target /chemin/du/projet \
  --resource project-audit \
  --resource code-reviewer
```

Les destinations sont :

- `.agents/skills/project-audit/` ;
- `.codex/agents/code-reviewer.toml` ;
- `.codex/agents-ia-toolkit-state.json` pour l'état de gestion.

Ajouter `--technology flutter`, `angular`, `spring-boot`, `nodejs` ou `multi-technology` pour filtrer les ressources compatibles. Sans `--resource`, toutes les ressources compatibles sélectionnées par le filtre sont planifiées.

## Installation personnelle

Prévisualiser puis appliquer dans le dossier personnel :

```bash
python3 scripts/install_toolkit.py --check --scope user --resource project-audit --resource code-reviewer
python3 scripts/install_toolkit.py --install --scope user --resource project-audit --resource code-reviewer
```

Les ressources sont placées sous `$HOME/.agents/skills/` et `$HOME/.codex/agents/`. L'état personnel est `$HOME/.codex/agents-ia-toolkit-state.json`.

Le helper officiel `skill-installer` peut utiliser `$CODEX_HOME/skills` selon l'installation. Voir [Compatibilité Codex](codex-compatibility.md). Le script du toolkit suit les destinations déclarées dans son manifeste et ne duplique pas automatiquement une ressource dans les emplacements historiques.

## Mise à jour

Après avoir récupéré une nouvelle version du toolkit, commencer par le plan :

```bash
python3 scripts/install_toolkit.py \
  --check \
  --scope project \
  --target /chemin/du/projet \
  --resource project-audit \
  --resource code-reviewer
```

Les états possibles sont :

- `CREATE` : ressource absente ;
- `UNCHANGED` : cible identique à la source ;
- `UPDATE` : ancienne version gérée, non personnalisée, mise à jour sûre ;
- `CONFLICT` : cible inconnue ou modifiée localement ;
- `ERROR` : manifeste, état, chemin ou type non sûr.

Appliquer uniquement après revue :

```bash
python3 scripts/install_toolkit.py \
  --update \
  --scope project \
  --target /chemin/du/projet \
  --resource project-audit \
  --resource code-reviewer
```

`--update` installe aussi une ressource absente. Pour une cible modifiée localement, il s'arrête sans écrire et conserve le fichier tel quel. Les sauvegardes ne sont jamais supprimées automatiquement.

## Codes de sortie

- `0` : plan acceptable ou application réussie ;
- `1` : conflit, ou mise à jour demandée avec `--install` ;
- `2` : erreur de manifeste, état, chemin, source ou écriture avec rollback.

## Utilisation après installation

Démarrer une nouvelle session Codex dans le projet si la découverte n'est pas dynamique.

Pour l'audit :

```text
Utilise $project-audit pour auditer ce dépôt en lecture seule.
```

Pour la revue :

```text
Utilise le sous-agent code_reviewer pour examiner le diff de cette branche contre main. Ne corrige rien.
```

Le rapport d'audit doit rester un artefact de revue ou de backlog. Ne recopier dans `AGENTS.md` que les conventions stables et validées. Pour plusieurs repositories, installer les ressources dans chaque environnement, auditer séparément, puis utiliser le guide [Projets multi-repositories](multi-repository.md).

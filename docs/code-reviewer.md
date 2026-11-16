# Code Reviewer

`code_reviewer` est un sous-agent Codex spécialisé dans la revue ciblée d'un diff Git ou d'une pull request. Sa source est [`agents/code-reviewer.toml`](../agents/code-reviewer.toml). Il couvre Flutter/Dart, Angular/TypeScript, Spring Boot/Java, Node.js et les changements multi-technologies.

## Fonctionnement

1. Il identifie le diff demandé et commence par sa liste de fichiers.
2. Il lit les lignes modifiées, les tests et manifestes concernés.
3. Il ouvre un appelant, un contrat ou un fichier adjacent uniquement pour confirmer un risque concret.
4. Il vérifie que chaque anomalie est introduite ou aggravée par le changement.
5. Il rend les constats par gravité, puis le périmètre et les vérifications non réalisées.

Les priorités sont les bugs et régressions, la logique métier, la sécurité, les tests, l'accessibilité observable, les régressions de performance ou d'écoconception démontrables et les ruptures d'API. Les remarques de formatage ou de style automatisables sont exclues.

Pour Flutter neuf, le référentiel cible reste Clean Architecture feature-first et Cubit/`flutter_bloc`. Une architecture existante différente n'est pas un défaut en soi et l'agent ne recommande aucune migration automatique.

## Format d'un constat

Chaque constat contient : gravité (`critical`, `high`, `medium`, `low`), fichier et ligne du diff, problème observé, impact probable, recommandation concrète et certitude (`high`, `medium`, `low`). En l'absence d'anomalie justifiée, l'agent doit le dire explicitement. Une hypothèse non confirmée va dans les vérifications résiduelles, pas dans les constats.

## Installation

Prévisualiser sans écrire :

```bash
python3 scripts/install_toolkit.py --check --scope project --target /chemin/du/projet --resource code-reviewer
python3 scripts/install_toolkit.py --check --scope user --target "$HOME" --resource code-reviewer
```

Après vérification du plan, installer sans écraser de personnalisation :

```bash
python3 scripts/install_toolkit.py --install --scope project --target /chemin/du/projet --resource code-reviewer
python3 scripts/install_toolkit.py --install --scope user --target "$HOME" --resource code-reviewer
```

Pour une version ultérieure, exécuter d'abord `--check`, puis remplacer `--install` par `--update`. La mise à jour refuse une cible personnalisée et conserve une sauvegarde de la version remplacée.

Redémarrer la session Codex si l'agent n'est pas découvert dynamiquement. Le nom d'invocation est `code_reviewer` :

> Utilise le sous-agent `code_reviewer` pour examiner en lecture seule le diff de cette branche contre `main`. Ne corrige rien.

Pour une pull request déjà récupérée localement, préciser sa branche ou sa plage de commits. Si le diff n'est disponible que via GitHub, la session parente doit fournir un accès en lecture ou transmettre le diff.

## Sécurité réelle

Le TOML interdit les écritures et désactive les demandes d'extension de permissions. Il ne peut toutefois pas créer seul un sandbox distinct : selon la [documentation officielle Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents), un sous-agent hérite des permissions, du fournisseur et des intégrations de sa session parente. Lancer donc la revue dans un mode de permissions en lecture seule. Toute correction, installation de dépendance ou exécution de test projet nécessite une demande séparée.

Le shell reste disponible parce que la lecture de `git diff`, `git show`, `git status` et des fichiers ciblés est essentielle. Les instructions interdisent les scripts, hooks et binaires du projet sans autorisation explicite.

## Pourquoi il n'y a pas de skill `code-review`

La procédure réutilisable est courte et propre à ce rôle ; elle tient dans `developer_instructions` sans ressource externe ni script. Un skill séparé dupliquerait le contrat et augmenterait le contexte. Il ne deviendra pertinent que si plusieurs agents ou workflows partagent une méthode d'analyse plus riche et indépendante.

## Exemple Flutter

Pour un diff qui remplace le calcul d'une réduction par `total * percentage` alors que `percentage` vaut `10` pour dix pour cent, un rapport attendu est :

> **high — `lib/cart/cart_cubit.dart:42` — confidence: high**  
> Le nouveau calcul multiplie le total par `10` au lieu d'appliquer 10 %. Le montant facturé devient cent fois supérieur au montant remisé attendu. Diviser le pourcentage par 100 dans le calcul et ajouter un test Cubit couvrant 0 %, 10 % et 100 %.

Cet exemple illustre le format ; la conclusion réelle doit toujours être vérifiée contre le diff et le contrat métier observés.

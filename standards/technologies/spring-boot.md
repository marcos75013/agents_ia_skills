# Profil Java / Spring Boot

- Identifier versions de Java, Spring Boot, outil de build, base de données et mode de déploiement.
- Séparer domaine, cas d'usage et adaptateurs lorsque la complexité le justifie ; pour un service simple, conserver une structure directe et explicite.
- Concevoir des contrats API stables, valider les entrées et normaliser les erreurs sans exposer de détails internes.
- Utiliser l'injection par constructeur et des transactions aux frontières de cas d'usage cohérentes.
- Appliquer Spring Security avec refus par défaut, autorisations testées et secrets externes au dépôt.
- Couvrir logique métier, persistence, sécurité et contrats HTTP avec le niveau de test adapté.

Éviter les abstractions génériques et annotations cachant le comportement critique. Tenir compte des migrations de schéma, de l'observabilité et des limites de ressources.

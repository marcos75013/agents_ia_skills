# Profil Angular / TypeScript

- Détecter d'abord la version d'Angular, le mode standalone ou modules, le gestionnaire de paquets et les contraintes de rendu.
- Organiser par domaine fonctionnel ; séparer composants de présentation, orchestration, accès aux données et logique métier lorsque la complexité le justifie.
- Privilégier typage strict, APIs Angular compatibles avec la version réelle et états locaux simples avant d'ajouter une bibliothèque globale.
- Centraliser les appels HTTP, valider les contrats aux frontières et traiter explicitement chargement, absence de données et erreurs.
- Tester logique pure et services, puis composants et parcours critiques au niveau pertinent.
- Vérifier sémantique HTML, clavier, focus, annonces dynamiques et contrastes.

Ne pas imposer une architecture backend ou mobile à Angular. Toute migration vers une API Angular récente doit être planifiée et vérifiée contre la documentation de la version du projet.

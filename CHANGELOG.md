# CHANGELOG.md

# Changelog - Cofinance CI

Toutes les modifications importantes du projet seront documentées dans ce fichier.

Le format s'inspire du principe "Keep a Changelog".

---
## [0.1.0] - 2026-06-05

* Création du dépôt GitHub du projet.

## [0.1.1] - 2026-06-06

### Ajouté

* Initialisation du projet Django.
* Mise en place d'un environnement virtuel Python.
* Configuration du fichier `.env`.
* Organisation du projet avec un dossier `apps/`.
* Création des premières applications métier :

  * authentication
  * credits
  * chat
  * assurance
  * dashboard
  * notifications
  *remboursements
* Mise en place de la structure de configuration Django.
* Configuration initiale des routes du projet.

### Modifié

* Ajustement de la configuration des applications dans `INSTALLED_APPS`.
* Configuration du modèle utilisateur personnalisé (`CustomUser`).
* Réorganisation de l'architecture des applications dans le dossier `apps/`.

### Corrigé

* Correction des erreurs liées à `load_dotenv`.
* Correction des erreurs d'import des applications Django.
* Correction des erreurs de configuration des URLs.
* Correction des erreurs de résolution de modules Python.
* Correction des erreurs liées à `TemplateView`.

### En cours

* Stabilisation de l'architecture du projet.
* Validation des routes et des applications.
* Configuration complète de l'application d'authentification.
* Mise en place du système de chat temps réel.

---

## Versions futures

Les prochaines versions documenteront :

* Authentification complète.
* Gestion des crédits.
* API REST.
* Chat temps réel.
* Tableau de bord administrateur.
* Déploiement du projet.

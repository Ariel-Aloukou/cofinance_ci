# CHANGELOG

Toutes les modifications importantes du projet COFINANCE CI seront documentées dans ce fichier.

## [0.2.0] - Juin 2026

### Ajouté

* Architecture Django modulaire basée sur plusieurs applications :

  * authentication
  * credits
  * remboursements
  * assurance
  * chat
  * notifications
* Configuration de l'environnement virtuel Python.
* Mise en place de PostgreSQL.
* Configuration des variables d'environnement (.env).
* Création du modèle utilisateur personnalisé `CustomUser`.
* Définition des rôles :

  * CLIENT
  * AGENT
  * ADMIN
* Mise en place du système d'authentification JWT.
* Début de l'API REST avec Django REST Framework.
* Documentation automatique avec DRF Spectacular.
* Création des modèles de crédit :

  * DemandeCredit
  * EcheancierRemboursement
  * PieceJustificative
  * HistoriqueStatutCredit
* Création des modèles d'assurance :

  * FormulaAssurance
  * Souscription
* Création du modèle Paiement.
* Première version du système de notifications.
* Première version du système de chat client-agent.
* Commande de peuplement de base de données (`seed_db`).

### Corrigé

* Correction de multiples erreurs d'importation Django.
* Correction des chemins d'applications dans INSTALLED_APPS.
* Correction de AUTH_USER_MODEL.
* Correction des imports circulaires.
* Correction des ForeignKey sans `on_delete`.
* Correction des OneToOneField incomplets.
* Correction des constantes `*_CHOICES` manquantes.
* Harmonisation des noms de modèles (`DemandeCredit`, `HistoriqueStatutCredit`, etc.).
* Correction des imports de serializers.
* Correction des URLs d'applications.

### Technique

* Réorganisation des applications dans le dossier `apps/`.
* Standardisation progressive de l'architecture Django.
* Début de stabilisation des migrations.
* Préparation du projet pour les premiers tests fonctionnels.

---

## [0.1.0] - Initialisation

### Ajouté

* Création du dépôt GitHub.
* Initialisation du projet Django.
* Mise en place de Git.
* Création de la structure de base du backend.

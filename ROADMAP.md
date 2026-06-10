# ROADMAP - COFINANCE CI

## Phase 1 - Fondations Backend 🔨

### Architecture

* [x] Création du projet Django
* [x] Mise en place de PostgreSQL
* [x] Configuration des variables d'environnement
* [x] Création de l'environnement virtuel
* [x] Configuration DRF
* [x] Configuration JWT
* [x] Configuration DRF Spectacular

### Utilisateurs

* [x] Modèle utilisateur personnalisé
* [x] Gestion des rôles CLIENT / AGENT / ADMIN
* [x] Inscription client
* [ ] Connexion JWT complète
* [ ] Gestion des permissions avancées

---

## Phase 2 - Gestion des Microcrédits 💰

### Crédit

* [x] Modèle DemandeCredit
* [x] HistoriqueStatutCredit
* [x] Pièces justificatives
* [ ] CRUD complet API
* [ ] Validation métier complète
* [ ] Génération automatique d'échéancier
* [ ] Calcul avancé du score d'éligibilité

### Workflow

* [ ] Soumission demande
* [ ] Analyse agent
* [ ] Validation crédit
* [ ] Décaissement
* [ ] Historique complet des actions

---

## Phase 3 - Assurance 🛡️

### Produits

* [x] Modèle FormulaAssurance
* [x] Modèle Souscription
* [ ] CRUD API complet
* [ ] Gestion des renouvellements
* [ ] Gestion des expirations

---

## Phase 4 - Remboursements 💳

### Paiements

* [x] Modèle Paiement
* [ ] API Paiement
* [ ] Validation des paiements
* [ ] Historique des remboursements
* [ ] Calcul automatique des pénalités

### Intégration Mobile Money

* [ ] Orange Money
* [ ] MTN MoMo
* [ ] Wave

---

## Phase 5 - Communication 📩

### Chat

* [x] Structure de base
* [ ] Conversation temps réel
* [ ] Assignation automatique agent
* [ ] Notifications de messages

### Notifications

* [x] Structure de base
* [ ] Notifications crédit
* [ ] Notifications assurance
* [ ] Notifications remboursement
* [ ] Notifications temps réel

---

## Phase 6 - Dashboard 📊

### Administrateur

* [ ] Statistiques globales
* [ ] Nombre de crédits
* [ ] Volume financier
* [ ] Performance des agents

### Agent

* [ ] Dossiers en attente
* [ ] Suivi des clients
* [ ] Historique des actions

### Client

* [ ] Suivi des crédits
* [ ] Suivi des remboursements
* [ ] Contrats d'assurance

---

## Phase 7 - Qualité & Déploiement 🚀

### Tests

* [ ] Tests unitaires
* [ ] Tests API
* [ ] Tests d'intégration

### Sécurité

* [ ] Audit permissions
* [ ] Validation avancée
* [ ] Protection des endpoints

### Déploiement

* [ ] Docker
* [ ] CI/CD GitHub Actions
* [ ] Déploiement Cloud
* [ ] Monitoring

---

## Objectif du MVP

Version démontrable permettant :

* Authentification utilisateur
* Soumission de demandes de crédit
* Validation par agent
* Gestion des remboursements
* Souscription à une assurance
* Notifications automatiques
* Tableau de bord simplifié

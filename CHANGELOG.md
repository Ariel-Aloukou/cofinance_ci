# Changelog

Toutes les modifications importantes du projet **COFINANCE CI** seront documentées ici.

Le format suit le principe de Keep a Changelog.

---

## [1.0.0] - Juin 2026

### Ajouté

#### Authentification
- Création du modèle utilisateur personnalisé `CustomUser`
- Gestion des rôles :
  - CLIENT
  - AGENT
  - ADMIN
- Inscription des clients
- Connexion JWT
- Consultation du profil utilisateur

#### Microcrédits
- Création des demandes de crédit
- Calcul du score d'éligibilité
- Workflow de traitement :

  ```
  SOUMISE
      ↓
  EN_ANALYSE
      ↓
  APPROUVEE
      ↓
  DECAISSEE
  ```

- Historique des changements de statut
- Validation des transitions

#### Pièces justificatives
- Upload de documents
- Liste des documents d'une demande
- Suppression des fichiers

#### Remboursements
- Génération d'échéanciers
- Gestion des paiements
- Calcul des pénalités de retard

#### Assurance
- Gestion des formules d'assurance
- Souscription d'un client
- Suivi des contrats

#### Notifications
- Notifications internes
- Gestion des alertes

#### Dashboard
- Statistiques générales
- Suivi des activités

#### Chat temps réel
- Conversations client-agent
- Messages sauvegardés
- Communication WebSocket via Django Channels
- Attribution automatique d'agents
- Gestion de la présence des agents
- Indicateur « en train d'écrire »

#### Documentation
- Swagger UI
- ReDoc
- Schéma OpenAPI avec drf-spectacular

#### Interface utilisateur
- Page de connexion
- Interface du chat
- Liste des conversations
- Zone d'envoi des messages
- Affichage des échanges

---

### Corrigé

- Suppression des imports circulaires.
- Correction des références de modèles.
- Correction des erreurs de serializers manquants.
- Correction des erreurs de routes.
- Correction des templates manquants.
- Correction des imports relatifs des applications.
- Configuration ASGI et WebSocket.
- Résolution des erreurs de migration.
- Résolution des erreurs 404 de connexion.
- Stabilisation du système de chat.

---

### Technique

- Django 5.1.4
- Django REST Framework
- Simple JWT
- Channels
- SQLite
- drf-spectacular
- CORS Headers
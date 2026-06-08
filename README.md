# README.md

# COFINANCE CI

Plateforme digitale de gestion de microcrédits, d'assurance mobile et de support client en temps réel.

## Présentation

COFINANCE CI est une plateforme développée dans le cadre de la digitalisation des processus d'une société ivoirienne de microfinance.

L'objectif principal est de permettre :

* la gestion numérique des demandes de microcrédits ;
* le suivi des remboursements ;
* la gestion des assurances mobiles ;
* les notifications automatiques ;
* le support client en temps réel via WebSocket ;
* le pilotage de l'activité grâce à un tableau de bord administratif.

---

## Technologies utilisées

### Backend

* Python 3.11+
* Django 5.x
* Django REST Framework
* Django Channels
* JWT Authentication
* drf-spectacular

### Base de données

* SQLite (développement)
* PostgreSQL (production)

### Outils

* Git
* GitHub
* Swagger UI
* Redoc

---

## Modules fonctionnels

### 1. Authentification & Profils

* Authentification JWT
* Gestion des rôles
* Gestion du profil utilisateur

### 2. Gestion des microcrédits

* Soumission des demandes
* Analyse des dossiers
* Validation des crédits
* Décaissement

### 3. Suivi des remboursements

* Historique des paiements
* Calcul automatique des intérêts
* Gestion des pénalités

### 4. Assurance mobile

* Catalogue des produits
* Souscriptions
* Gestion des expirations

### 5. Notifications

* Alertes automatiques
* Notifications internes

### 6. Tableau de bord administrateur

* Statistiques temps réel
* Suivi des performances

### 7. Chat temps réel

* Communication Client ↔ Agent
* WebSocket
* Historique des conversations
* Présence en ligne

---

## Structure du projet

```text
cofinance_ci/
│
├── apps/
│   ├── authentication/
│   ├── credits/
│   ├── repayments/
│   ├── insurance/
│   ├── notifications/
│   ├── dashboard/
│   └── chat/
│
├── config/
├── templates/
├── static/
├── media/
│
├── requirements.txt
├── CHANGELOG.md
├── ROADMAP.md
├── README.md
└── manage.py
```

## Documentation API

Swagger :

```text
/api/docs/
```

Redoc :

```text
/api/redoc/
```

---

## État actuel du projet

Phase en cours :

**Mise en place de l'architecture backend et configuration des modules principaux.**

---

## Auteur

Projet réalisé dans le cadre du développement de la plateforme COFINANCE CI. Par Aloukou Ariel

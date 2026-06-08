# ROADMAP.md

# Roadmap - COFINANCE CI

## Progression globale

* [x] Création du dépôt GitHub
* [x] Initialisation du projet Django
* [x] Mise en place de l'environnement virtuel
* [x] Configuration Git
* [x] Configuration des variables d'environnement
* [ ] Stabilisation complète de l'architecture
* [ ] Première version fonctionnelle (MVP)

---

# Phase 1 — Architecture du projet

## Configuration générale

* [x] Création du projet Django
* [x] Création du dossier apps
* [ ] Configuration définitive des applications
* [ ] Configuration SQLite
* [ ] Préparation PostgreSQL
* [ ] Configuration DRF
* [ ] Configuration drf-spectacular
* [ ] Configuration Django Channels
* [ ] Configuration WebSocket
* [ ] Configuration CORS

## Documentation

* [ ] Swagger (/api/docs/)
* [ ] Redoc
* [ ] Documentation des endpoints

---

# Phase 2 — Authentification & Profils

## Gestion des utilisateurs

* [ ] Création du modèle CustomUser
* [ ] Gestion des rôles :

  * [ ] Client
  * [ ] Agent de terrain
  * [ ] Administrateur

## Authentification JWT

* [ ] Inscription
* [ ] Connexion
* [ ] Rafraîchissement des tokens
* [ ] Déconnexion

## Gestion des profils

* [ ] Consultation du profil
* [ ] Modification du profil
* [ ] Photo de profil
* [ ] Historique des connexions

---

# Phase 3 — Gestion des microcrédits

## Demandes de crédit

* [ ] Soumission d'une demande
* [ ] Téléversement des pièces justificatives
* [ ] Consultation d'une demande
* [ ] Liste des demandes

## Workflow métier

* [ ] Soumise
* [ ] En analyse
* [ ] Approuvée
* [ ] Décaissée

## Calculs automatiques

* [ ] Score d'éligibilité
* [ ] Calcul du montant accordable
* [ ] Génération d'échéancier

---

# Phase 4 — Suivi des remboursements

## Gestion des paiements

* [ ] Enregistrement des paiements
* [ ] Historique des remboursements
* [ ] Solde restant

## Automatisation

* [ ] Calcul des intérêts
* [ ] Calcul des pénalités
* [ ] Alertes J-3
* [ ] Alertes J+1

---

# Phase 5 — Assurance mobile

## Catalogue

* [ ] Liste des assurances
* [ ] Détail des garanties

## Souscriptions

* [ ] Souscription en ligne
* [ ] Renouvellement
* [ ] Résiliation

## Gestion des échéances

* [ ] Date de validité
* [ ] Expiration automatique
* [ ] Notification à J-15

---

# Phase 6 — Notifications internes

## Notifications système

* [ ] Crédit approuvé
* [ ] Crédit refusé
* [ ] Crédit décaissé
* [ ] Paiement enregistré
* [ ] Assurance souscrite

## Centre de notifications

* [ ] Lu / Non lu
* [ ] Historique
* [ ] API utilisateur

---

# Phase 7 — Chat temps réel

## Backend WebSocket

* [ ] Configuration Channels
* [ ] Routing WebSocket
* [ ] Consumers

## Fonctionnalités

* [ ] Ouverture d'une conversation
* [ ] Attribution à un agent
* [ ] Messages temps réel
* [ ] Historique complet
* [ ] Présence en ligne
* [ ] Plusieurs conversations simultanées

## Bonus

* [ ] Indicateur "en train d'écrire"

---

# Phase 8 — Tableau de bord administrateur

## Indicateurs crédits

* [ ] Nombre de demandes
* [ ] Répartition par statut
* [ ] Taux de recouvrement

## Indicateurs assurance

* [ ] Souscriptions actives
* [ ] Assurances expirées

## Support client

* [ ] Conversations ouvertes
* [ ] Temps moyen de réponse

## Filtres

* [ ] Par période
* [ ] Par région
* [ ] Par agent

---

# Phase 9 — Tests

* [ ] Tests unitaires
* [ ] Tests API
* [ ] Tests WebSocket
* [ ] Tests des permissions
* [ ] Validation métier

---

# Phase 10 — Livraison

* [ ] requirements.txt complet
* [ ] README final
* [ ] Jeu de données de démonstration
* [ ] Commande seed_db
* [ ] Documentation API
* [ ] Démonstration du chat
* [ ] Préparation soutenance

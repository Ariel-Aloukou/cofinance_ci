# COFINANCE CI — Plateforme API REST
 
> Plateforme digitale de microcrédits, assurance mobile et support client.
> Développée avec Python 3.11, Django 5.x et Django REST Framework. par Aloukou Ariel
 
## Technologies
- Backend       : Python 3.11+, Django 5.x, Django REST Framework
- Authentification : JWT via djangorestframework-simplejwt
- WebSocket     : Django Channels (chat en temps réel)
- Documentation : drf-spectacular (Swagger UI sur /api/docs/)
- Base de données : SQLite (dev) / PostgreSQL (prod)
 
## Prérequis
- Python 3.11 ou supérieur
- Git
 
## Installation
 
### 1. Cloner le dépôt
```bash
git clone https://github.com/TON_USERNAME/cofinance-ci-api.git
cd cofinance-ci-api
```
 
### 2. Créer et activer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate     # Windows
```
 
### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
 
### 4. Configurer les variables d'environnement
```
SECRET_KEY=django-insecure-votre-cle-secrete-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```
 
### 5. Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
 
### 6. Charger les données de démonstration
```bash
python manage.py seed_db
```
 
### 7. Lancer le serveur
```bash
python manage.py runserver
```

### . Lancer le serveur en asychrone
```bash
python -m daphne -p 8001 config.asgi:application```
 
## Comptes de démonstration
| Rôle            | Username          | Password      |
|-----------------|-------------------|---------------|
| Administrateur  | admin_cofinance   | Admin@2026    |
| Agent terrain   | agent_kouassi     | Agent@2026    |
| Client          | aya_kone          | Client@2026   |
 
## Accès aux interfaces
| Interface          | URL                               |
|--------------------|-----------------------------------|
| Swagger UI         | http://127.0.0.1:8001/api/docs/   |
| Redoc              | http://127.0.0.1:8001/api/redoc/  |
| Chat HTML          | http://127.0.0.1:8001/chat/       |
| Admin Django       | http://127.0.0.1:8001/admin/      |
 
## Démo du chat en temps réel
1. Ouvrir DEUX onglets sur http://127.0.0.1:8000/chat/
2. Onglet 1 : Se connecter avec aya_kone (Client)
3. Onglet 2 : Se connecter avec agent_kouassi (Agent)
4. Utiliser l'ID de conversation 1 dans les deux onglets
5. Les messages apparaissent instantanément des deux côtés
 
## Passer en production (PostgreSQL)
Dans .env, ajouter :
DB_NAME=cofinance_db
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
Dans settings.py, décommenter le bloc PostgreSQL.

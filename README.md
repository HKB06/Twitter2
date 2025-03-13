# Twitter Clone Application

## Objectif
Un clone de Twitter moderne développé avec Next.js 13 et FastAPI, mettant l'accent sur une expérience utilisateur fluide .

## Prérequis Techniques

### Frontend
- Node.js (version LTS recommandée)
- npm ou yarn
- Next.js 13
- TypeScript
- Tailwind CSS

### Backend
- Python 3.12
- pip
- FastAPI
- uvicorn

## Configuration du Frontend



1. Cloner le projet :
```bash
git clone [URL_DU_REPO]
cd client
```
2. Installer les dépendances :
```bash
npm install
```
3. Lancer le serveur de développement :
```bash
npm run dev
```
4. Lancement du Front sur :

* http://localhost:3000


## Configuration du Backend

1. Installer Python 3.12 :
```bash
# Vérifier la version
python --version
# Doit afficher Python 3.12.x
```
2. Créer et activer un environnement virtuel :

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Installer les dépendances depuis requirements.txt :

```bash
pip install -r requirements.txt
```

4. Lancer le serveur backend (deux options) : :

```bash
# Option 1
py -3.11 main.py

# Option 2
py -3.11 -m uvicorn app.main:app --reload
```
Note : Si vous rencontrez des erreurs lors de l'installation :

* Nettoyer le cache pip : pip cache purge 

* Mettre à jour pip : python -m pip install --upgrade pip

5. Lancement du Back sur :

* http://localhost:8000


## Fonctionnalités Implémentées
 ### Frontend
 * Authentification
 * Mode jour/nuit
 * Création de tweets
 * Notifications
 * Interface responsive
### Backend
 * API REST
 * Authentification JWT
 * Gestion des fichiers
 * Détection d'émotions
### Prochaines Étapes
 * Tests unitaires
 * Optimisation des performances
 * WebSocket pour les notifications en temps réel

### Déploiement
 * Docker
 
## Liens utiles

* Trello le lien https://trello.com/b/4IJ92z25/mia28-hackathon


# Twitter-Clone
- Twitter-Clone est une application type Twitter où 
- les utilisateurs publient des tweets, interagissent (likes, retweets, réponses) et 
- bénéficient d’une IA analysant leurs expressions faciales (joie, tristesse, colère, etc.).

### Installation
#### Prérequis
- Node.js
- Python 3.x
- MongoDB

## Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Utilisation
Ouvrez l'interface dans votre navigateur à l'adresse http://localhost:3000.

## API Endpoints
FastAPI Swagger UI http://localhost:8000/docs)

## Trello
Trello le lien https://trello.com/b/4IJ92z25/mia28-hackathon)


## Technologies Used
### Frontend: 
#### Next.js, React, Tailwind CSS
### Backend: 
#### FastAPI, MongoDB, Python 

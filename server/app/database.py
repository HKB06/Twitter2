from pymongo import MongoClient
import os
from dotenv import load_dotenv
import gridfs

# Charger les variables d'environnement
load_dotenv()

# Connexion MongoDB
# MONGO_URI = "mongodb+srv://user:1234@cluster0.hsa1yir.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_URI = "mongodb://mongodb:27017/mydatabase"
client = MongoClient(MONGO_URI)
db = client["twitter_clone"]

fs = gridfs.GridFS(db, collection="media")
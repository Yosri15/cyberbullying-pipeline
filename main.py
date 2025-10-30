from fastapi import FastAPI
from pymongo import MongoClient
from typing import List, Dict

# 1. CRÉATION DE L'APPLICATION FASTAPI
app = FastAPI(title="API Cyberbullying Detection")

# 2. CONNEXION MONGODB
client = MongoClient("mongodb://localhost:27017")
db = client["harassment_db"]
collection = db["tweets"]

# 3. ENDPOINTS DE L'API

# Page d'accueil
@app.get("/")
def accueil():
    return {"message": "Bienvenue dans l'API de détection de harcèlement !"}

# Récupérer les tweets avec pagination  
@app.get("/tweets")
def get_tweets(skip: int = 0, limit: int = 10):
    # Récupère les tweets depuis MongoDB
    tweets = list(collection.find().skip(skip).limit(limit))
    
    # Convertit les ObjectId en string pour JSON
    for tweet in tweets:
        tweet["_id"] = str(tweet["_id"])
    
    return {"tweets": tweets, "skip": skip, "limit": limit}

# Récupérer les statistiques
@app.get("/stats")
def get_stats():
    # Nombre total de tweets
    total_tweets = collection.count_documents({})
    
    # Répartition par type de harcèlement
    pipeline_repartition = [
        {"$group": {"_id": "$cyberbullying_type", "count": {"$sum": 1}}}
    ]
    repartition_list = list(collection.aggregate(pipeline_repartition))
    
    repartition_dict = {}
    for item in repartition_list:
        repartition_dict[item["_id"]] = item["count"]
    
    # Longueur moyenne des tweets
    pipeline_moyenne = [
        {"$group": {"_id": None, "moyenne": {"$avg": "$tweet_length"}}}
    ]
    moyenne_result = list(collection.aggregate(pipeline_moyenne))
    longueur_moyenne = round(moyenne_result[0]["moyenne"], 2) if moyenne_result else 0
    
    return {
        "total_tweets": total_tweets,
        "repartition_par_type": repartition_dict,  
        "longueur_moyenne_tweets": longueur_moyenne
    }

# 4. LANCEMENT DU SERVEUR
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
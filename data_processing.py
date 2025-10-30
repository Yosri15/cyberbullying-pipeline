#data_processing.py

import pandas as pd
from pymongo import MongoClient
import re
import uuid
from datetime import datetime
import os

# 1. CONNEXION À MONGODB
client = MongoClient("mongodb://localhost:27017")  # Connexion locale
db = client["harassment_db"]  # Crée la base de données
collection = db["tweets"]     # Crée la collection

# 2. LECTURE DU FICHIER CSV
df = pd.read_csv('DataBase\cyberbullying_tweets.csv')

# 3. NETTOYAGE DES TWEETS

def nettoyer_tweet(texte):
    # Supprimer les @utilisateur
    texte = re.sub(r'@\w+', '', texte)
    # Supprimer les liens http
    texte = re.sub(r'http\S+', '', texte)
    # Supprimer la ponctuation
    texte = re.sub(r'[^\w\s]', '', texte)
    # Mettre en minuscules
    texte = texte.lower().strip()
    return texte

# 3 .Appliquer le nettoyage
df['cleaned_tweet_text'] = df['tweet_text'].apply(nettoyer_tweet)

# 4. SUPPRIMER LES DOUBLONS
df = df.drop_duplicates(subset=['cleaned_tweet_text'])

# 5. AJOUTER LES NOUVELLES COLONNES
df['tweet_length'] = df['cleaned_tweet_text'].str.len()  # Longueur du tweet
df['tweet_id'] = [str(uuid.uuid4()) for _ in range(len(df))]  # ID unique
df['ingestion_date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")  # Date d'ajout

# 6. PRÉPARATION POUR MONGODB
documents = []
for index, row in df.iterrows():
    document = {
        "tweet_id": row['tweet_id'],
        "cleaned_tweet_text": row['cleaned_tweet_text'],
        "cyberbullying_type": row['cyberbullying_type'],
        "tweet_length": row['tweet_length'],
        "ingestion_date": row['ingestion_date']
    }
    documents.append(document)

# 7. INSERTION DANS MONGODB
collection.insert_many(documents)

print(f"✅ SUCCÈS : {len(documents)} tweets insérés dans MongoDB!")
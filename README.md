# Pipeline Cyberharcèlement

## 📌 Objectif
Créer un pipeline qui :
1. Lit un fichier CSV contenant des tweets
2. Nettoie et déduplique les textes
3. Ajoute des métadonnées (`tweet_id`, longueur, date d’ingestion)
4. Insère les données dans une base **MongoDB**
5. Expose les données via une **API FastAPI**

---

## ✅ Prérequis
- Python 3.10+ (Anaconda recommandé)
- MongoDB installé localement 
- Dataset `cyberbullying_tweets.csv` (placé dans `DataBase/`)

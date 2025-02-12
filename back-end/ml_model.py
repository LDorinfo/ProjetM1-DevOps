import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import pickle
import numpy as np

# Charger les données TMDb
df = pd.read_csv("movies.csv")

# Remplacer les valeurs manquantes
df.fillna(0, inplace=True)

# 🔹 Transformer les genres en liste
df["genres"] = df["genres"].apply(lambda x: x.split("-") if isinstance(x, str) else [])

print("🔹 Prétraitement des données...")

# 🔹 Utiliser MultiLabelBinarizer pour encoder plusieurs genres
mlb = MultiLabelBinarizer()
genre_encoded = mlb.fit_transform(df["genres"])
genre_columns = [f"genre_{g}" for g in mlb.classes_]
df_genres = pd.DataFrame(genre_encoded, columns=genre_columns)
df = pd.concat([df, df_genres], axis=1)
df.drop(columns=["genres"], inplace=True)

print("🔹 Encodage des genres terminé.")

# 🔹 Transformer la langue en valeurs numériques
label_encoder_lang = LabelEncoder()
df["original_language"] = label_encoder_lang.fit_transform(df["original_language"].astype(str))

# 🔹 Transformer la société de production en valeur numérique
df["production_companies"] = df["production_companies"].apply(lambda x: hash(x) % 1000 if isinstance(x, str) else 0)

# 🔹 Transformer la date de sortie en "année de sortie"
df["release_year"] = pd.to_datetime(df["release_date"], errors='coerce').dt.year.fillna(0).astype(int)

# 🔹 Définition de la variable cible "succès"
df["success"] = df.apply(lambda row: 1 if row["revenue"] > row["budget"] * 2 else 0, axis=1)

print("🔹 Création de la variable cible 'succès' terminée.")

# Sélection des variables d'entrée
features = ["budget", "original_language", "production_companies", "release_year", "runtime"] + genre_columns
X = df[features]
y_success = df["success"]
y_revenue = df["revenue"]

# Séparation des données en train/test
X_train, X_test, y_success_train, y_success_test = train_test_split(X, y_success, test_size=0.2, random_state=42)
X_train_rev, X_test_rev, y_revenue_train, y_revenue_test = train_test_split(X, y_revenue, test_size=0.2, random_state=42)

# 🎯 Modèle de classification pour prédire le succès
success_model = RandomForestClassifier(n_estimators=100, random_state=42)
success_model.fit(X_train, y_success_train)

# 💰 Modèle de régression pour prédire les revenus
revenue_model = RandomForestRegressor(n_estimators=100, random_state=42)
revenue_model.fit(X_train_rev, y_revenue_train)

print("🎯 Modèles entraînés avec succès.")

# Sauvegarde des modèles et encodeurs
pickle.dump(success_model, open("models/success_model.pkl", "wb"))
pickle.dump(revenue_model, open("models/revenue_model.pkl", "wb"))
pickle.dump(label_encoder_lang, open("models/label_encoder_lang.pkl", "wb"))
pickle.dump(mlb, open("models/mlb_genres.pkl", "wb"))

print("✅ Modèles entraînés et sauvegardés avec succès.")

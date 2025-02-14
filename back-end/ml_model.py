import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import classification_report, mean_absolute_error

# Charger les données
df = pd.read_csv("movies.csv")

# Remplacement des valeurs manquantes
df.fillna(0, inplace=True)

# Transformation des genres en listes
df["genres"] = df["genres"].apply(lambda x: x.split("-") if isinstance(x, str) else [])

print("Prétraitement des données...")

# Encodage des genres avec MultiLabelBinarizer
mlb = MultiLabelBinarizer()
genre_encoded = mlb.fit_transform(df["genres"])
genre_columns = [f"genre_{g}" for g in mlb.classes_]
df_genres = pd.DataFrame(genre_encoded, columns=genre_columns)
df = pd.concat([df, df_genres], axis=1)
df.drop(columns=["genres"], inplace=True)

# Ajouter une colonne "nombre de genres"
df["num_genres"] = df_genres.sum(axis=1)

print("Encodage des genres terminé.")

# Encodage des langues avec One-Hot Encoding
df_lang = pd.get_dummies(df["original_language"], prefix="lang")
df = pd.concat([df, df_lang], axis=1)
df.drop(columns=["original_language"], inplace=True)

# Encodage des sociétés de production en nombre de films produits
company_counts = df["production_companies"].value_counts().to_dict()
df["production_company_count"] = df["production_companies"].map(company_counts).fillna(1)
df.drop(columns=["production_companies"], inplace=True)

# Transformer la date en "année de sortie"
df["release_year"] = pd.to_datetime(df["release_date"], errors='coerce').dt.year.fillna(0).astype(int)
df.drop(columns=["release_date"], inplace=True)

# Détection des suites (franchises)
df["is_sequel"] = df["title"].str.contains(r'\b(II|III|IV|V|VI|VII|VIII|IX|X|2|3|4|5|6|7|8|9)\b', regex=True).astype(int)

# Appliquer une transformation logarithmique sur le budget
df["log_budget"] = np.log1p(df["budget"])
df.drop(columns=["budget"], inplace=True)

# Définition de la variable cible "succès" (mieux calibrée)
df["success"] = df.apply(lambda row: 1 if row["revenue"] > row["log_budget"] * 2.5 else 0, axis=1)

print("Création de la variable cible 'succès' terminée.")

#  Sélection des variables d'entrée
features = ["log_budget", "production_company_count", "release_year", "runtime", "num_genres", "is_sequel"] + genre_columns + list(df_lang.columns)
X = df[features]
y_success = df["success"]
y_revenue = df["revenue"]

# Séparation des données en train/test
X_train, X_test, y_success_train, y_success_test = train_test_split(X, y_success, test_size=0.2, random_state=42)
X_train_rev, X_test_rev, y_revenue_train, y_revenue_test = train_test_split(X, y_revenue, test_size=0.2, random_state=42)

# Modèle de classification pour prédire le succès
success_model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
success_model.fit(X_train, y_success_train)

# Modèle de régression pour prédire les revenus
revenue_model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
revenue_model.fit(X_train_rev, y_revenue_train)

print(" Modèles entraînés avec succès.")

# Évaluation des modèles
y_pred_success = success_model.predict(X_test)
print("Rapport de classification (succès) :")
print(classification_report(y_success_test, y_pred_success))

y_pred_revenue = revenue_model.predict(X_test_rev)
print("💰 Erreur moyenne absolue sur le revenu : ", mean_absolute_error(y_revenue_test, y_pred_revenue))

# Sauvegarde des modèles et encodeurs
pickle.dump(success_model, open("models/success_model.pkl", "wb"))
pickle.dump(revenue_model, open("models/revenue_model.pkl", "wb"))
pickle.dump(mlb, open("models/mlb_genres.pkl", "wb"))

# Évaluation du modèle
from sklearn.metrics import accuracy_score
y_pred_success = stacking_model.predict(X_test)
success_accuracy = accuracy_score(y_success_test, y_pred_success)

print(f"✅ Modèle entraîné avec une précision de {success_accuracy * 100:.2f}%")


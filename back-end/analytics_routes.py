from flask import Blueprint, jsonify
import pandas as pd

# Charger le fichier CSV au démarrage de l'application
df = pd.read_csv("movies.csv", nrows=50000)

# Créer le Blueprint
analytics_blueprint = Blueprint('analytics', __name__)

#1. Répartition des Genres
@analytics_blueprint.route('/api/genre-distribution', methods=['GET'])
def genre_distribution():
    genres_counts = df['genres'].value_counts().nlargest(10)
    return jsonify({
        "labels": genres_counts.index.tolist(),
        "data": genres_counts.values.tolist()
    })

#2. Évolution de la Popularité au Fil du Temps
@analytics_blueprint.route('/api/popularity-over-time', methods=['GET'])
def popularity_over_time():
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year
    popularity = df.groupby('year')['popularity'].mean().dropna()
    return jsonify({
        "labels": popularity.index.astype(int).tolist(),
        "data": popularity.values.tolist()
    })

#3. Répartition des Langues Originales
@analytics_blueprint.route('/api/language-distribution', methods=['GET'])
def language_distribution():
    # Filtrer les langues définies (exclure NaN, None, etc.)
    valid_languages = df['original_language'].dropna()  # Supprimer les valeurs nulles
    valid_languages = valid_languages[valid_languages != '']  # Supprimer les chaînes vides
    language_counts = valid_languages.value_counts().nlargest(10)  # Compter les occurrences des 10 premières langues

    return jsonify({
        "labels": language_counts.index.tolist(),
        "data": language_counts.values.tolist()
    })

#4. Budget Moyen par Genre
@analytics_blueprint.route('/api/average-budget-by-genre', methods=['GET'])
def average_budget_by_genre():
    genres_budgets = df[['genres', 'budget']].groupby('genres')['budget'].mean().nlargest(10)
    return jsonify({
        "labels": genres_budgets.index.tolist(),
        "data": genres_budgets.values.tolist()
    })

#5. Comparaison Budget vs Revenus
@analytics_blueprint.route('/api/budget-vs-revenue', methods=['GET'])
def budget_vs_revenue():
    filtered_data = df[['budget', 'revenue']].dropna()
    return jsonify({
        "budget": filtered_data['budget'].tolist(),
        "revenue": filtered_data['revenue'].tolist()
    })

#6. Films les Plus Populaires
@analytics_blueprint.route('/api/top-popular-movies', methods=['GET'])
def top_popular_movies():
    top_movies = df[['title', 'popularity']].nlargest(10, 'popularity')
    return jsonify({
        "titles": top_movies['title'].tolist(),
        "popularity": top_movies['popularity'].tolist()
    })

#7. Rentabilité des Films
@analytics_blueprint.route('/api/movie-profitability', methods=['GET'])
def movie_profitability():
    df['profitability'] = df['revenue'] / df['budget']
    df['profitability'] = df['profitability'].fillna(0)
    profitability_data = df[['title', 'profitability']].nlargest(10, 'profitability')
    return jsonify({
        "titles": profitability_data['title'].tolist(),
        "profitability": profitability_data['profitability'].tolist()
    })

#8. Le nombre de films sortis par mois.
@analytics_blueprint.route('/api/release-month-distribution', methods=['GET'])
def release_month_distribution():
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['month'] = df['release_date'].dt.month
    month_counts = df['month'].value_counts().sort_index()
    return jsonify({
        "labels": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        "data": month_counts.tolist()
    })

#9. Films par Compagnies de Production
@analytics_blueprint.route('/api/top-production-companies', methods=['GET'])
def top_production_companies():
    companies_counts = df['production_companies'].value_counts().nlargest(10)
    return jsonify({
        "labels": companies_counts.index.tolist(),
        "data": companies_counts.values.tolist()
    })

#10. Films les Plus Rentables
@analytics_blueprint.route('/api/most-profitable-movies', methods=['GET'])
def most_profitable_movies():
    df['profitability'] = df['revenue'] / df['budget']
    df['profitability'] = df['profitability'].fillna(0)
    top_profitable_movies = df[['title', 'profitability']].nlargest(10, 'profitability')
    return jsonify({
        "titles": top_profitable_movies['title'].tolist(),
        "profitability": top_profitable_movies['profitability'].tolist()
    })

#11. Films avec les Plus Gros Budgets
@analytics_blueprint.route('/api/highest-budget-movies', methods=['GET'])
def highest_budget_movies():
    top_budget_movies = df[['title', 'budget']].nlargest(10, 'budget')
    return jsonify({
        "titles": top_budget_movies['title'].tolist(),
        "budgets": top_budget_movies['budget'].tolist()
    })

#12. Analyse de la Relation Popularité vs Revenus
@analytics_blueprint.route('/api/popularity-vs-revenue', methods=['GET'])
def popularity_vs_revenue():
    filtered_data = df[['popularity', 'revenue']].dropna()
    return jsonify({
        "popularity": filtered_data['popularity'].tolist(),
        "revenue": filtered_data['revenue'].tolist()
    })

#13. Films les Plus Anciens
@analytics_blueprint.route('/api/oldest-movies', methods=['GET'])
def oldest_movies():
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    oldest_movies = df[['title', 'release_date']].sort_values(by='release_date').head(10)
    return jsonify({
        "titles": oldest_movies['title'].tolist(),
        "release_dates": oldest_movies['release_date'].astype(str).tolist()
    })

#14. Analyse des Notes Moyennes
@analytics_blueprint.route('/api/top-rated-movies', methods=['GET'])
def top_rated_movies():
    top_rated_movies = df[['title', 'vote_average']].nlargest(10, 'vote_average')
    return jsonify({
        "titles": top_rated_movies['title'].tolist(),
        "ratings": top_rated_movies['vote_average'].tolist()
    })

#15. Nombre Total de Films et Statistiques Clés
@analytics_blueprint.route('/api/summary-stats', methods=['GET'])
def summary_stats():
    total_movies = len(df)
    avg_budget = df['budget'].mean()
    avg_revenue = df['revenue'].mean()
    return jsonify({
        "total_movies": total_movies,
        "average_budget": avg_budget,
        "average_revenue": avg_revenue
    })


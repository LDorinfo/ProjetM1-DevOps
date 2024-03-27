# statistique
from flask import Blueprint, current_app, jsonify, request, session
from flask_bcrypt import Bcrypt
import requests
from models import User, Watchlist

statistic_blueprint = Blueprint('statistic', __name__)

@statistic_blueprint.route('/nb/user', methods=['GET'])
def get_nbuser():
    nb = User.query.count()
    if(nb is None): 
        return jsonify("error","erreur dans le calcul du nombre d'utilisateur")
    return jsonify({"nb": nb})

@statistic_blueprint.route("/genre-stats", methods=["GET"])
def genre_stats():
    """
    Calculer les statistiques sur les genres des films dans la watchlist de l'utilisateur.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    # Récupérer la watchlist de l'utilisateur
    watchlist = Watchlist.query.filter_by(user_id=user_id).all()

    genre_stats = {}
    for item in watchlist:
        genres = item.genres.split(",")
        # Parcourir chaque genre du film
        for genre in genres:
            # Mettre à jour le compteur de chaque genre
            genre_stats[genre] = genre_stats.get(genre, 0) + 1

    return jsonify(genre_stats)
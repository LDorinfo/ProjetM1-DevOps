from flask import Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt
import requests
from models import Watchlist, db

watchlist_blueprint = Blueprint('watchlist', __name__)
bcrypt = Bcrypt()

@watchlist_blueprint.route("/add", methods=["POST"])
def add_to_watchlist():
    """
    Ajoute un film à la Watchlist de l'utilisateur.

    ---
    tags:
      - Watchlist
    parameters:
      - name: film_id
        in: body
        type: integer
        required: true
        description: ID du film à ajouter à la Watchlist.
      - name: title
        in: body
        type: string
        required: true
        description: Titre du film à ajouter à la Watchlist.
      - name: poster_path
        in: body
        type: string
        required: true
        description: Chemin vers l'affiche du film.
    responses:
      200:
        description: Le film a été ajouté à la Watchlist avec succès.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Message de confirmation.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    data = request.json
    film_id = data.get("film_id")
    title = data.get("title")  # Ajoutez cette ligne
    poster_path = data.get("poster_path")

    # Vérifie si le film est déjà dans la Watchlist de l'utilisateur
    existing_watchlist_item = Watchlist.query.filter_by(user_id=user_id, film_id=film_id).first()
    if existing_watchlist_item:
        return jsonify({"message": "Film already in Watchlist"})

    # Ajoutez le film à la Watchlist dans la base de données
    watchlist_item = Watchlist(user_id=user_id, film_id=film_id, title=title, poster_path=poster_path)
    db.session.add(watchlist_item)
    db.session.commit()

    return jsonify({"message": "Film added to Watchlist"})

from models import Watchlist

@watchlist_blueprint.route("/remove", methods=["POST"])
def remove_from_watchlist():
    """
    Supprime un film de la Watchlist de l'utilisateur.

    ---
    tags:
      - Watchlist
    parameters:
      - in: body
        name: Film ID
        description: ID du film à supprimer de la Watchlist.
        required: true
        schema:
          type: object
          properties:
            film_id:
              type: integer
              description: ID du film à supprimer.
    responses:
      200:
        description: Message indiquant que le film a été supprimé de la Watchlist.
      401:
        description: Non autorisé, l'utilisateur n'est pas authentifié.
      404:
        description: Le film n'a pas été trouvé dans la Watchlist.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    film_id = request.json.get("film_id")

    # Recherche et suppression de l'entrée correspondante dans la Watchlist
    watchlist_item = Watchlist.query.filter_by(user_id=user_id, film_id=film_id).first()
    if not watchlist_item:
        return jsonify({"error": "Film not found in Watchlist"})

    db.session.delete(watchlist_item)
    db.session.commit()

    return jsonify({"message": "Film removed from Watchlist"})

@watchlist_blueprint.route("/get-watchlist", methods=["GET"])
def get_watchlist():
    """
    Récupère la Watchlist de l'utilisateur.

    ---
    tags:
      - Watchlist
    responses:
      200:
        description: Liste des films dans la Watchlist de l'utilisateur.
        schema:
          type: object
          properties:
            watchlist:
              type: array
              items:
                type: object
                properties:
                  film_id:
                    type: integer
                    description: ID du film.
                  title:
                    type: string
                    description: Titre du film.
                  poster_path:
                    type: string
                    description: Chemin vers l'affiche du film.
      401:
        description: Non autorisé, l'utilisateur n'est pas authentifié.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    watchlist = Watchlist.query.filter_by(user_id=user_id).all()

    watchlist_data = []
    for item in watchlist:
        watchlist_data.append({
            "id": item.film_id,
            "title": item.title,
            "poster_path": item.poster_path,
            # Ajoutez d'autres champs au besoin
        }) 

    return jsonify({"watchlist": watchlist_data})

    watchlist_data = []
    for item in watchlist:
        #url = f'https://api.themoviedb.org/3/movie/{item.film_id}'
        #params = {'api_key': tmdb_api_key}
        #response = requests.get(url, params=params).json()
        #import requests

        url = "https://api.themoviedb.org/3/find/external_id?external_source={item.film_id}"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        print(response)
        watchlist_data.append({
            "id": item.film_id,
            "title": item.title,
            "poster_path": item.poster_path
            #"name": response.original_title, 
            #"release_date" : response.release_date, 
            #"overview" : response.overview
            # Ajoutez d'autres champs au besoin
        })

    return jsonify({"watchlist": watchlist_data})

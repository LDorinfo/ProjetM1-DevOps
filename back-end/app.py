from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import Planning, db, User
from flask_mail import Message, Mail
from config import ApplicationConfig
import requests  # Importez le module requests
from flask_migrate import Migrate
from users_routes import users_blueprint
from comments_routes import comments_blueprint
#from search_routes import search_blueprint
from evenement_routes import event_blueprint
from watchlist_routes import watchlist_blueprint
from flasgger import Swagger



app = Flask(__name__)
app.config.from_object(ApplicationConfig)
migrate= Migrate(app,db,render_as_batch=True)

# Accédez à la clé d'API TMDb depuis la configuration
tmdb_api_key = app.config["TMDB_API_KEY"]

# URL de base de l'API TMDb
BASE_URL = 'https://api.themoviedb.org/3'

bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)
#=> prise en charge des cookies dans les requêtes 
server_session = Session(app)
db.init_app(app)
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(comments_blueprint, url_prefix='/comments')
app.register_blueprint(event_blueprint, url_prefix='/event')
app.register_blueprint(watchlist_blueprint, url_prefix='/watchlist')
#app.register_blueprint(search_blueprint, url_prefix='/search', tmdb_api_key=tmdb_api_key)
#pas possible car ces routes on besoin de tmdb_api_key

# documentation API Swagger
swagger = Swagger(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'cineverse.noreply@gmail.com'
#app.config['MAIL_PASSWORD'] =
app.config['MAIL_DEFAULT_SENDER'] = {'flask email','cineverse.noreply@gmail.com'}


mail = Mail(app)

with app.app_context():
    db.create_all()

@app.route("/@me")
def get_current_user():
    """
    Récupère les détails de l'utilisateur actuellement authentifié.

    ---
    tags:
      - Utilisateur
    responses:
      200:
        description: Données de l'utilisateur récupérées avec succès.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Identifiant de l'utilisateur.
            email:
              type: string
              description: Adresse e-mail de l'utilisateur.
      401:
        description: Non autorisé, l'utilisateur n'est pas authentifié.
    """
    user_id = session.get("user_id")
    #stocke la clé dans la session flask
    # session.get permet de récupère la clé user_id dans la session flask.
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 
#@search_blueprint.route('search/search-multi', methods=['GET'])
@app.route('/search/search-multi', methods=['GET'])
def search_multi():
    """
    Recherche multi-critères.
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: true
        description: Le terme de recherche.
    responses:
      200:
        description: Les résultats de la recherche.
      401: 
        error: Pas de résultats à la recherche
    """
    keyword = request.args.get('query')
    url = f'{BASE_URL}/search/multi'
    params = {'api_key': tmdb_api_key, 'query': keyword}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        return jsonify({"error": "Pas de résultats à la recherche"}), 401 
    
#@search_blueprint.route('search/api/trending-movie', methods=['GET'])
@app.route('/search/trending-movie', methods=['GET'])
def trending_movies():
    """
    Récupère les films populaires du jour.

    ---
    tags:
      - Recherche
    responses:
      200:
        description: Liste des films populaires du jour.
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                description: Titre du film.
              release_date:
                type: string
                description: Date de sortie du film.
              poster_path:
                type: string
                description: Chemin vers l'affiche du film.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    url = f'{BASE_URL}/trending/movie/day?language=fr-FR'
    params = {'api_key': tmdb_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        print("On retourne rien")
        return []
    
#@search_blueprint.route('search/api/trending-tv', methods=['GET'])
@app.route('/search/trending-tv', methods=['GET'])
def trending_tv():
    """
    Récupère les émissions de télévision populaires de la semaine.

    ---
    tags:
      - Recherche
    responses:
      200:
        description: Liste des émissions populaires de la semaine.
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                description: Nom de l'émission de télévision.
              first_air_date:
                type: string
                description: Date de première diffusion de l'émission.
              poster_path:
                type: string
                description: Chemin vers l'affiche de l'émission.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    url = f'{BASE_URL}/trending/tv/week?language=fr-FR'
    params = {'api_key': tmdb_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

#@search_blueprint.route('search/filtre', methods=['GET'])
@app.route('/search/filtre', methods=['GET'])
def filtre_movies():
    """
    Récupère les films en fonction d'un genre spécifié.

    ---
    tags:
      - Recherche
    parameters:
      - name: query
        in: query
        type: integer
        required: true
        description: ID du genre de film.
    responses:
      200:
        description: Liste des films du genre spécifié.
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                description: Titre du film.
              release_date:
                type: string
                description: Date de sortie du film.
              poster_path:
                type: string
                description: Chemin vers l'affiche du film.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    keyword = request.args.get('query')
    url = f'{BASE_URL}/discover/movie'
    # 28 pour les films d'action
    # 12 pour les films d'aventure
    # 16 pour les films d'animation
    # 35 pour les comédies 
    # 80 pour les films criminels
    # 99 pour les films documentaires
    #18 pour les films dramatiques
    # 10751 pour les films famille
    # 14 pour les films fantastiques
    # 36 pour les films historiques
    # 27 pour les films d'horreur 
    # 10402 pour les comédies musicales 
    # 9648 pour les films mystérieux 
    # 10749 pour les films romantiques 
    # 878 pour les films de science fiction.
    # 53 pour les films à suspense. 
    # 10752 pour les films de guerre
    params = {'api_key': tmdb_api_key, 'with_genres':keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        return []
    
#@search_blueprint.route('search/tv/filtre', methods=['GET'])
@app.route('/search/tv/filtre', methods=['GET'])
def search_tv():
    """
    Récupère les émissions de télévision en fonction d'un genre spécifié.

    ---
    tags:
      - Recherche
    parameters:
      - name: query
        in: query
        type: integer
        required: true
        description: ID du genre de l'émission de télévision.
    responses:
      200:
        description: Liste des émissions de télévision du genre spécifié.
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                description: Nom de l'émission de télévision.
              first_air_date:
                type: string
                description: Date de première diffusion de l'émission.
              poster_path:
                type: string
                description: Chemin vers l'affiche de l'émission.
      404:
        description: Aucun résultat trouvé pour la recherche spécifiée.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    keyword = request.args.get('query')
    url = f'{BASE_URL}/discover/tv'

    params = {'api_key': tmdb_api_key, 'with_genres':keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        if not search_results:
            return jsonify([]), 404  # Aucun résultat trouvé
        return jsonify(search_results)
    else:
        return jsonify([]), 500
#@search_blueprint.route('search/discover-western-movies', methods=['GET'])
@app.route('/search/discover-western-movies', methods=['GET'])
def western_movies():
    """
    Récupère les films du genre Western.

    ---
    tags:
      - Recherche
    responses:
      200:
        description: Liste des films du genre Western.
        schema:
          type: array
          items:
            type: object
            properties:
              title:
                type: string
                description: Titre du film.
              release_date:
                type: string
                description: Date de sortie du film.
              poster_path:
                type: string
                description: Chemin vers l'affiche du film.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':37, 'language':'fr-FR'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
@app.route("/get-trailer", methods=["POST"])
def get_trailer():
    """
    Récupère les bandes-annonces d'un film ou d'une émission de télévision.

    ---
    tags:
      - Bande-annonce
    parameters:
      - in: body
        name: Trailer Request
        description: Informations sur le média pour lequel récupérer les bandes-annonces.
        required: true
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID du film ou de l'émission de télévision.
            media_type:
              type: string
              enum: ['movie', 'tv']
              description: Type de média ('movie' pour film, 'tv' pour émission de télévision).
    responses:
      200:
        description: Liste des bandes-annonces du média spécifié.
      400:
        description: Paramètres manquants dans la requête.
    """
    data = request.json

    media_id = data.get("id")
    media_type = data.get("media_type")

    if not media_id or not media_type:
        return jsonify({"error": "Paramètres manquants"}), 400

    # Construisez l'URL de l'API TMDb en fonction du type de média
    tmdb_url = f"https://api.themoviedb.org/3/{media_type}/{media_id}/videos"

    # Ajoutez la clé API à la requête
    params = {"api_key": tmdb_api_key, 'language':'fr-FR'}

    # Effectuez la requête vers l'API TMDb
    response = requests.get(tmdb_url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Erreur lors de la requête vers l'API TMDb"}), response.status_code

    data = response.json()

    # Récupérez les résultats de la requête
    videos = data.get("results", [])

    return jsonify({"videos": videos})

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Envoie un e-mail pour réinitialiser le mot de passe.

    ---
    tags:
      - Authentification
    parameters:
      - in: body
        name: Forgot Password Request
        description: Adresse e-mail pour la réinitialisation du mot de passe.
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Adresse e-mail de l'utilisateur.
    responses:
      200:
        description: Message indiquant que l'e-mail de réinitialisation a été envoyé.
    """
    email = request.json.get('email')

    msg = Message('Réinitialisation du mot de passe', recipients=[email])
    msg.body = "Corps : Merci de cliquer sur le lien pour réinitialiser le mot de passe "
    mail.send(msg)
    return "Message envoyé"
@app.route('/movie/details', methods=['GET'])
def get_movie_details():
    """
    Récupère les détails d'un film en fonction de son ID en utilisant l'endpoint /find.

    ---
    tags:
      - Détails du film
    parameters:
      - name: movie_id
        in: query
        type: integer
        required: true
        description: ID du film.
    responses:
      200:
        description: Détails du film.
        schema:
          type: object
          properties:
            title:
              type: string
              description: Titre du film.
            release_date:
              type: string
              description: Date de sortie du film.
            overview:
              type: string
              description: Résumé du film.
            poster_path:
              type: string
              description: Chemin vers l'affiche du film.
      404:
        description: Aucun résultat trouvé pour l'ID du film.
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    #https://www.themoviedb.org/movie/787699-wonka?language=fr-FR
    movie_id = request.args.get('query')
    url = f'{BASE_URL}/movie/{movie_id}'

    params = {'api_key': tmdb_api_key}
    headers = {"accept": "application/json"}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        movie_details = response.json()

        return jsonify({"info": movie_details})
    else:
        return jsonify({'error': 'Aucun résultat trouvé pour l\'ID du film.'}), 404

@app.route('/planning/delete', methods=['DELETE'])
def delete_event():
    """
    Supprime un événement du planning en fonction de son ID.

    ---
    tags:
      - Planning
    parameters:
      - name: id_event
        in: body
        type: integer
        required: true
        description: ID de l'événement à supprimer.
    responses:
      200:
        description: Événement supprimé avec succès.
      404:
        description: Aucun événement trouvé avec l'ID spécifié.
    """
    data = request.json
    id_event = data.get('id_event')

    if id_event is None:
        return jsonify({"error": "ID de l'événement manquant"}), 400

    event_to_delete = Planning.query.get(id_event)

    if event_to_delete is None:
        return jsonify({"error": "Aucun événement trouvé avec l'ID spécifié"}), 404

    db.session.delete(event_to_delete)
    db.session.commit()

    return jsonify({"status": "Événement supprimé avec succès"})

@app.route('/planning/add', methods=['POST'])
def add_eventPlanning():
    """
    Ajoute un nouvel événement de planification pour un film.

    ---
    tags:
      - Planning
    parameters:
      - in: body
        name: Event Planning
        description: Informations sur l'événement de planification à ajouter.
        required: true
        schema:
          type: object
          properties:
            idFilm:
              type: integer
              description: ID du film associé à l'événement.
            user:
              type: integer
              description: ID de l'utilisateur associé à l'événement.
            start:
              type: string
              description: Date et heure de début de l'événement au format ISO 8601.
            end:
              type: string
              description: Date et heure de fin de l'événement au format ISO 8601.
            title:
              type: string
              description: Titre de l'événement.

    responses:
      200:
        description: Événement de planification ajouté avec succès.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Identifiant unique de l'événement de planification.
            start:
              type: string
              description: Date et heure de début de l'événement au format ISO 8601.
            end:
              type: string
              description: Date et heure de fin de l'événement au format ISO 8601.
            title:
              type: string
              description: Titre de l'événement.
            film_id:
              type: integer
              description: ID du film associé à l'événement.
      404:
        description: Les informations requises ne sont pas présentes.
    """
    idFilm = request.json.get('idFilm')
    user_id = request.json.get('user')
    start= request.json.get('start')
    end= request.json.get('end')
    title = request.json.get('title')
    if idFilm is None :
        return jsonify({"error": "IdFilm is not present"}), 404
    if start is None or "" : 
      return jsonify({"error": "Start is not present"}), 404
    if end is None or "" :
      return jsonify({"error": "End is not present"}), 404
    if title is None :
      return jsonify({"error": "title is not present"}), 404
    if user_id is None: 
        return jsonify({"error" : "User unauthenticate"}),403
    user = User.query.filter_by(id=user_id).first()
    if user is None: 
        return jsonify({"error" : "User not found"}), 404
    newprojet = Planning(title= title, end = end, start=start, user_id= user_id,film_id=idFilm)
    db.session.add(newprojet)
    db.session.commit()
  
    return jsonify({
        "id": newprojet.id,
        "start": newprojet.start,
        "end": newprojet.end,
        "title": newprojet.title,
        "film_id": newprojet.film_id
    })

from datetime import datetime
@app.route('/planning/get', methods=['GET'])
def get_eventPlanning():
  """
    Récupère la liste des événements de planification pour l'utilisateur authentifié.

    ---
    tags:
      - Planning
    responses:
      200:
        description: Liste des événements de planification trouvés.
        schema:
          type: object
          properties:
            status:
              type: string
              description: Statut de la requête.
            planning:
              type: array
              description: Liste des événements de planification.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Identifiant unique de l'événement de planification.
                  start:
                    type: string
                    description: Date et heure de début de l'événement au format ISO 8601.
                  end:
                    type: string
                    description: Date et heure de fin de l'événement au format ISO 8601.
                  title:
                    type: string
                    description: Titre de l'événement.
                  film_id:
                    type: integer
                    description: ID du film associé à l'événement.
      403:
        description: L'utilisateur n'est pas authentifié.
      404:
        description: Aucun événement de planification trouvé.
  """ 
  user_id = session.get("user_id")
  if user_id is None: 
    return jsonify({"error" : "User unauthenticate"}),403
  events_planning = Planning.query.filter_by(user_id=user_id).all()
  if events_planning is None : 
    return jsonify({"error":"No events"}), 404 
    
  events_list = []
  for event_planning in events_planning:
    # Convertir les chaînes de caractères en objets datetime
    start_date = datetime.strptime(event_planning.start, '%Y, %m, %d, %H, %M')
    end_date = datetime.strptime(event_planning.end, '%Y, %m, %d, %H, %M')
    events_list.append({
      "id": event_planning.id,
      "start": start_date.strftime('%Y-%m-%dT%H:%M:%S'),
      "end": end_date.strftime('%Y-%m-%dT%H:%M:%S'),
      "title": event_planning.title,
      "film_id": event_planning.film_id,
    })
  return jsonify({"status": "Found events", "planning": events_list})
    
@app.route("/home")
def home():
    return "Hello"

if __name__ == "__main__":
  app.run(debug=True)
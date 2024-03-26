from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import db, User
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
app.config['MAIL_PASSWORD'] = 'ROUjeElaR0se'
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
      401:
        description: Non autorisé, l'accès à la ressource est refusé.
    """
    keyword = request.args.get('query')
    url = f'{BASE_URL}/discover/tv'

    params = {'api_key': tmdb_api_key, 'with_genres':keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        return [] 
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

@app.route("/get-providers", methods=["POST"])
def get_providers():
    data = request.json

    movie_id = data.get("id")

    if not movie_id:
        return jsonify({"error": "Paramètres manquants"}), 400

    # Construisez l'URL de l'API TMDb en fonction du type de média
    tmdb_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"

    # Ajoutez la clé API à la requête
    params = {"api_key": tmdb_api_key, 'language': 'fr-FR'}

    # Effectuez la requête vers l'API TMDb
    response = requests.get(tmdb_url, params=params)

    data = response.json()

    # Récupérez uniquement les données pour la France (FR)
    france_providers = data.get("results", {}).get("FR", None)

    # Si les données pour la France sont disponibles, renvoyez-les, sinon renvoyez un objet JSON vide
    if france_providers:
        return jsonify({"providers": france_providers})
    else:
        return jsonify({"error": "Aucune donnée disponible pour la France"}), 404

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

@app.route("/home")
def home():
    return "Hello"

if __name__ == "__main__":
    

    app.run(debug=True)
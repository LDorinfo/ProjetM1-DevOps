from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from outil import generate_unique_token
from models import db, User
from flask_mail import Message, Mail
from config import ApplicationConfig
import requests  # Importez le module requests
from flask_migrate import Migrate
from flask_restx import Api, Swagger
from users_routes import users_blueprint
from comments_routes import comments_blueprint
#from search_routes import search_blueprint
from evenement_routes import event_blueprint
from watchlist_routes import watchlist_blueprint

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
migrate= Migrate(app,db,render_as_batch=True)
swagger = Swagger(app)
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
api = Api(app, version='0.3', title='ProjetM1-DevOps API', description='API Documentation')

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
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':37, 'language':'fr-FR'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route("/watchlist/add", methods=["POST"])
def add_to_watchlist():
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

@app.route("/watchlist/remove", methods=["POST"])
def remove_from_watchlist():
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

@app.route("/get-watchlist", methods=["GET"])
def get_watchlist():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    watchlist = Watchlist.query.filter_by(user_id=user_id).all()

    watchlist_data = []
    for item in watchlist:
        watchlist_data.append({
            "film_id": item.film_id,
            "title": item.title,
            "poster_path": item.poster_path,
            # Ajoutez d'autres champs au besoin
        })

    return jsonify({"watchlist": watchlist_data})

@app.route("/get-trailer", methods=["POST"])
def get_trailer():
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
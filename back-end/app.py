from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import db, User
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
migrate= Migrate(app,db)
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

@app.route("/home")
def home():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)

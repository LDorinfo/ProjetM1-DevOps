from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import db, User
from config import ApplicationConfig
import requests  # Importez le module requests
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
migrate= Migrate(app,db)
# Accédez à la clé d'API TMDb depuis la configuration
tmdb_api_key = app.config["TMDB_API_KEY"]

# URL de base de l'API TMDb
BASE_URL = 'https://api.themoviedb.org/3'

bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 

@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    phone_number = request.json["phone_number"]
    
    user_exists = User.query.filter_by(email=email).first() is not None
    print(user_exists)
    user_exists = User.query.filter_by(username=username).first() is not None
    print(user_exists)
    if user_exists:
        return jsonify({"error": "user already exists"}), 409
    
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, username=username, first_name=first_name, last_name=last_name, phone_number=phone_number, isconnected = True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "phone_number": new_user.phone_number,
        "isconnected": new_user.isconnected
    })

@app.route("/login", methods=["POST"])
def login_user():
    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username=username).first()

    if user is None :
        return jsonify({"error": "Incorrect Login"}), 401 
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect Password"}), 401
    
    session["user_id"] = user.id
    user.isconnected = True
    print(user.isconnected)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "isconnected": user.isconnected
    })

@app.route("/api/userinfo", methods=["GET"])
def info_user():
    id = request.args.get("user_id")
    user = User.query.filter_by(id=id).first()
    if user is None : 
        return jsonify({"error":"Unknown user"}), 401 
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "isconnected": user.isconnected
    })

@app.route("/modify", methods=["PATCH"])
def modify_user():
    if "user_id" not in session:
        return jsonify({"error": "User not authenticated"}), 401

    user_id = session["user_id"]
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if "email" in request.json:
        user.email = request.json["email"]

    if "password" in request.json:
        user.password = bcrypt.generate_password_hash(request.json["password"])

    if "username" in request.json:
        user.username = request.json["username"]

    if "first_name" in request.json:
        user.first_name = request.json["first_name"]

    if "last_name" in request.json:
        user.last_name = request.json["last_name"]

    if "phone_number" in request.json:
        user.phone_number = request.json["phone_number"]

    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "isconnected": True
    })


@app.route('/api/users/connected',methods=["GET"])
def isconnected(): 
    id = request.args.get("user_id")
    user = User.query.filter_by(id=id).first()
    if user is None : 
        return jsonify({"error":"Unknown user"}), 401 
    if not user.isconnected : 
        return jsonify({"error": "disconnected"}), 401 
    return jsonify({
        "isconnected": True
    })


@app.route('/api/search-multi', methods=['GET'])
def search_multi():
    keyword = request.args.get('query')
    url = f'{BASE_URL}/search/multi'
    params = {'api_key': tmdb_api_key, 'query': keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route('/api/trending-movies', methods=['GET'])
def trending_movies():
    url = f'{BASE_URL}/trending/movie/week'
    params = {'api_key': tmdb_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        print("On retourne rien")
        return []
    
@app.route('/api/trending-tv', methods=['GET'])
def trending_tv():
    url = f'{BASE_URL}/trending/tv/week'
    params = {'api_key': tmdb_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-action-movies', methods=['GET'])
def action_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':28}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-adventure-movies', methods=['GET'])
def adventure_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':12}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-animation-movies', methods=['GET'])
def animation_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':16}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route('/api/discover-comedy-movies', methods=['GET'])
def comedy_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':35}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route('/api/discover-crime-movies', methods=['GET'])
def crime_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':80}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-documentary-movies', methods=['GET'])
def documentary_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':99}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-drama-movies', methods=['GET'])
def drama_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':18}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route('/api/discover-family-movies', methods=['GET'])
def family_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':10751}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-fantasy-movies', methods=['GET'])
def fantasy_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':14}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-history-movies', methods=['GET'])
def history_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':36}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-horror-movies', methods=['GET'])
def horror_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':27}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-music-movies', methods=['GET'])
def music_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':10402}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-mystery-movies', methods=['GET'])
def mystery_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':9648}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-romance-movies', methods=['GET'])
def romance_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':10749}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route('/api/discover-sciencefiction-movies', methods=['GET'])
def sciencefiction_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':878}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-thriller-movies', methods=['GET'])
def thriller_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':53}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
@app.route('/api/discover-war-movies', methods=['GET'])
def war_movies():
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':10752}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@app.route('/api/discover-western-movies', methods=['GET'])
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

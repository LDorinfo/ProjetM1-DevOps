from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import Comments, db, User
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
#=> prise en charge des cookies dans les requêtes 
server_session = Session(app)
db.init_app(app)

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


@app.route("/logout", methods=["POST"])
def logout_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.isconnected = False
    session.pop("user_id", None)
    db.session.commit()

    return jsonify({"message": "Logout successful"})


@app.route('/api/comments', methods=['GET'])
def get_comments():
    idFilm = request.args.get('idFilm')
    if idFilm is None: 
        return jsonify({"status":"Not found Id in database Comment"}) 
    comments = Comments.query.filter_by(film_id=idFilm).all()
    if comments is None : 
        return jsonify({"error":"Aucun commentaire"}), 404 
    
    comments_list = []
    for comment in comments:
        user = User.query.filter_by(id=comment.user_id).first()

        if user is None: 
            return jsonify({"error" : "User not found"}), 404

        comments_list.append({
            "id": comment.id,
            "comment_text": comment.comment_text, 
            "note": comment.note, 
            "user_id": comment.user_id, 
            "username": user.username,
            "film_id": comment.film_id
        })

    return jsonify({"status": "Found comments", "comments": comments_list})
    
@app.route('/api/comments/create', methods=['PUT'])
def create_comments():
    data = request.json; 
    idFilm = data.get('idFilm')
    username = data.get('username')
    comments= data.get('comments')
    note = data.get('note')
    if idFilm is None : 
        return jsonify({"error":"Comments without idFilm"}), 404
    if username is None: 
        return jsonify({"error" : "User unauthenticate, it's guest and he can not publish"}),403
    newcomments = Comments(comment_text= comments, note = note, user_id= username,film_id=idFilm)
    db.session.add(newcomments)
    db.session.commit()
    user = User.query.filter_by(id=newcomments.user_id).first()

    if user is None: 
        return jsonify({"error" : "User not found"}), 404
    return jsonify({
        "id": newcomments.id,
        "username": user.username,
        "comment_text": newcomments.comment_text,
        "note": newcomments.note,
        "user_id": newcomments.user_id,
        "film_id": newcomments.film_id
    })
@app.route('/api/comments/editing', methods=['POST'])
def editing_comments():
    newtextcomment = request.json.get('comment_text')
    id_comment = request.json.get('id_comment')
    #print(id_comment)
    #print(newtextcomment)
    if newtextcomment is None : 
        return jsonify({"error":"Not found text"}), 404
    if id_comment is None: 
        return jsonify({"error":"Not found id"}), 404
    comment = Comments.query.filter_by(id=id_comment).first()
    if comment is None: 
        return jsonify({"error":"Not found comment"}), 404
    comment.comment_text = id_comment

    db.session.commit()
    return jsonify({
        "status": "update comment"
    })
    
@app.route('/api/comments/delete', methods=['DELETE'])
def delete_comments():
    id_comment = request.json.get('id_comment')
    if id_comment is None: 
        return jsonify({"error":"Not found id"}), 404
    comment = Comments.query.filter_by(id=id_comment).first()
    if comment is None: 
        return jsonify({"error":"Not found comment"}), 404

    db.session.delete(comment)  # Supprimer le commentaire de la session
    db.session.commit()  # Confirmer la suppression en effectuant un commit
    return jsonify({
        "status": "delete comment",
        "id": id_comment
    })
    
@app.route('/api/search-multi', methods=['GET'])
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
    
@app.route('/api/trending-movies', methods=['GET'])
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
    
@app.route('/api/trending-tv', methods=['GET'])
def trending_tv():
    url = f'{BASE_URL}/trending/tv/week?language=fr-FR'
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

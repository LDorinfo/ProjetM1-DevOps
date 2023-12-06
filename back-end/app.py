from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from models import Comments, Like, db, User, Watchlist
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
    id = session.get("user_id")
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
        like = Like.query.filter_by(comment_id=comment.id).count()
        print(like)
        user_like = Like.query.filter_by(user_id=comment.user_id).count()
        if user is None: 
            return jsonify({"error" : "User not found"}), 404

        comments_list.append({
            "id": comment.id,
            "comment_text": comment.comment_text, 
            "note": comment.note, 
            "like" : like,
            "user_id": comment.user_id, 
            "username": user.username,
            "film_id": comment.film_id, 
            "like_user": user_like
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
        "like": 0, 
        "note": newcomments.note,
        "user_id": newcomments.user_id,
        "film_id": newcomments.film_id, 
        "like_user": 0
    })
@app.route('/api/comments/editing', methods=['POST'])
def editing_comments():
    newtextcomment = request.json.get('comment_text')
    id_comment = request.json.get('id_comment')
    note = request.json.get('noteUser')
    #print(id_comment)
    #print(newtextcomment)
    if newtextcomment is None: 
        return jsonify({"error":"Not found text"}), 404
    if id_comment is None: 
        return jsonify({"error":"Not found id"}), 404
    if note is None: 
        return jsonify({"error":"Not found note"}), 404
    comment = Comments.query.filter_by(id=id_comment).first()
    if comment is None: 
        return jsonify({"error":"Not found comment"}), 404
    if newtextcomment != "":
        comment.comment_text = newtextcomment
    comment.note= note

    db.session.commit()
    return jsonify({
        "status": "update comment"
    })

@app.route('/api/comment/like', methods=['POST'])
def likes_comment():

    user_id = session.get("user_id")
    id_comment = request.json.get('id_comment')
    if user_id is None: 
        return jsonify({"status":"Not found Id in database User"}),404
    if id_comment is None: 
        return jsonify({"status":"Not found Id in database Comment"}),404 
    nblikes = Like.query.filter_by(id=id_comment).count()
    likes = Like.query.filter_by(user_id=user_id).first()
    print(likes)
    if likes is None : 
        newlike = Like(comment_id =id_comment , user_id= user_id)
        db.session.add(newlike)
        db.session.commit()
        print(nblikes)
        return jsonify({"like": nblikes+1})
    db.session.delete(likes)
    db.session.commit()
    return jsonify({"like":nblikes, "status": "suppression du like"})

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
    
@app.route('/api/trending-movie', methods=['GET'])
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

@app.route('/api/filtre', methods=['GET'])
def action_movies():
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
@app.route('/api/tv/filtre', methods=['GET'])
def action_tv():
    keyword = request.args.get('query')
    url = f'{BASE_URL}/discover/tv'

    params = {'api_key': tmdb_api_key, 'with_genres':keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
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


@app.route("/home")
def home():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)

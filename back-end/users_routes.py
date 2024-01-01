# users_routes.py
from flask import Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt
from models import User, db

users_blueprint = Blueprint('users', __name__)

bcrypt = Bcrypt()

@users_blueprint.route("/register", methods=["POST"])
def register_user():
    """
    Enregistre un nouvel utilisateur.

    ---
    tags:
      - Utilisateurs
    parameters:
      - in: body
        name: Informations utilisateur
        description: Informations pour créer un nouvel utilisateur.
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Adresse e-mail de l'utilisateur.
            password:
              type: string
              description: Mot de passe de l'utilisateur.
            username:
              type: string
              description: Nom d'utilisateur de l'utilisateur.
            first_name:
              type: string
              description: Prénom de l'utilisateur.
            last_name:
              type: string
              description: Nom de famille de l'utilisateur.
            phone_number:
              type: string
              description: Numéro de téléphone de l'utilisateur.
    responses:
      200:
        description: Informations sur le nouvel utilisateur créé.
      409:
        description: L'utilisateur existe déjà.
    """
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
    new_user = User(email=email, password=hashed_password, username=username, first_name=first_name, last_name=last_name, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "phone_number": new_user.phone_number,
    })

@users_blueprint.route("/login", methods=["PUT"])
def login_user():
    """
    Connecte un utilisateur.

    ---
    tags:
      - Utilisateurs
    parameters:
      - in: body
        name: Informations de connexion
        description: Informations pour connecter un utilisateur.
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nom d'utilisateur de l'utilisateur.
            password:
              type: string
              description: Mot de passe de l'utilisateur.
    responses:
      200:
        description: Utilisateur connecté avec succès.
      401:
        description: Nom d'utilisateur ou mot de passe incorrect.
    """
    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username=username).first()

    if user is None :
        return jsonify({"error": "Incorrect Login"}), 401 
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect Password"}), 401
    
    session["user_id"] = user.id
    return jsonify({
        "id": user.id,
        "username": user.username,
    })

@users_blueprint.route("/userinfo", methods=["GET"])
def info_user():
    """
    Récupère les informations de l'utilisateur connecté.

    ---
    tags:
      - Utilisateurs
    responses:
      200:
        description: Informations de l'utilisateur connecté.
      401:
        description: Utilisateur non authentifié.
    """
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
        "phone_number": user.phone_number
    })

@users_blueprint.route("/modify", methods=["PUT"])
def modify_user():
    """
    Modifie les informations de l'utilisateur connecté.

    ---
    tags:
      - Utilisateurs
    parameters:
      - in: body
        name: Nouvelles informations utilisateur
        description: Nouvelles informations pour l'utilisateur connecté.
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Nouvelle adresse e-mail de l'utilisateur.
            password:
              type: string
              description: Nouveau mot de passe de l'utilisateur.
            username:
              type: string
              description: Nouveau nom d'utilisateur de l'utilisateur.
            first_name:
              type: string
              description: Nouveau prénom de l'utilisateur.
            last_name:
              type: string
              description: Nouveau nom de famille de l'utilisateur.
            phone_number:
              type: string
              description: Nouveau numéro de téléphone de l'utilisateur.
    responses:
      200:
        description: Informations mises à jour pour l'utilisateur connecté.
      401:
        description: Utilisateur non authentifié.
      404:
        description: Utilisateur non trouvé.
    """
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
    })

@users_blueprint.route("/logout", methods=["PUT"])
def logout_user():
    """
    Déconnecte l'utilisateur connecté.

    ---
    tags:
      - Utilisateurs
    responses:
      401:
        description: Utilisateur non authentifié.
      404:
        description: Utilisateur non trouvé.
    """
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
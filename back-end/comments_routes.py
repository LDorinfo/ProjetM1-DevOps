# comments_routes.py
from flask import Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt
from models import Comments, Likes, User, db

comments_blueprint = Blueprint('comments', __name__)

bcrypt = Bcrypt()

@comments_blueprint.route('/comments', methods=['GET'])
def get_comments():
    """
    Récupère les commentaires d'un film.

    ---
    tags:
      - Commentaires
    parameters:
      - in: query
        name: idFilm
        description: ID du film pour lequel les commentaires doivent être récupérés.
        type: integer
        required: true
    responses:
      200:
        description: Commentaires récupérés avec succès.
      404:
        description: Commentaires non trouvés pour l'ID du film spécifié.
    """
    user_id = session.get("user_id")
    idFilm = request.args.get('idFilm')
    if idFilm is None: 
        return jsonify({"status":"Not found Id in database Comment"}), 404 
    comments = Comments.query.filter_by(film_id=idFilm).all()
    if comments is None : 
        return jsonify({"error":"Aucun commentaire"}), 404 
    
    comments_list = []
    for comment in comments:
        user = User.query.filter_by(id=comment.user_id).first()
        like = Likes.query.filter_by(comment_id=comment.id).count()
        print(like)
        user_like = Likes.query.filter_by(user_id=user_id).count()
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
    
@comments_blueprint.route('/create', methods=['POST'])
def create_comments():
    """
    Crée un nouveau commentaire.

    ---
    tags:
      - Commentaires
    parameters:
      - in: body
        name: Informations sur le commentaire
        description: Informations pour créer un nouveau commentaire.
        required: true
        schema:
          type: object
          properties:
            idFilm:
              type: integer
              description: ID du film pour lequel le commentaire est créé.
            username:
              type: string
              description: Nom d'utilisateur de l'auteur du commentaire.
            comments:
              type: string
              description: Texte du commentaire.
            note:
              type: integer
              description: Note attribuée au film dans le commentaire.
    responses:
      200:
        description: Commentaire créé avec succès.
      404:
        description: Erreur lors de la création du commentaire.
    """
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
        "film_id": newcomments.film_id, 
        "like_user": 0
    })
@comments_blueprint.route('/editing', methods=['PUT'])
def editing_comments():
    """
    Modifie un commentaire existant.

    ---
    tags:
      - Commentaires
    parameters:
      - in: body
        name: Nouvelles informations du commentaire
        description: Nouvelles informations pour mettre à jour un commentaire existant.
        required: true
        schema:
          type: object
          properties:
            id_comment:
              type: integer
              description: ID du commentaire à mettre à jour.
            comment_text:
              type: string
              description: Nouveau texte du commentaire.
            noteUser:
              type: integer
              description: Nouvelle note attribuée au film dans le commentaire.
    responses:
      200:
        description: Commentaire mis à jour avec succès.
      404:
        description: Erreur lors de la mise à jour du commentaire.
    """
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

@comments_blueprint.route('/like', methods=['POST'])
def likes_comment():
    """
    Gère les likes des commentaires.

    ---
    tags:
      - Commentaires
    parameters:
      - in: body
        name: Informations du like
        description: Informations pour gérer le like d'un commentaire.
        required: true
        schema:
          type: object
          properties:
            id_comment:
              type: integer
              description: ID du commentaire pour lequel le like doit être géré.
    responses:
      200:
        description: Like géré avec succès.
      404:
        description: Erreur lors de la gestion du like.
    """
    user_id = session.get("user_id")
    id_comment = request.json.get('id_comment')
    if user_id is None: 
        return jsonify({"status":"Not found Id in database User"}),404
    if id_comment is None: 
        return jsonify({"status":"Not found Id in database Comment"}),404 
    nblikes = Likes.query.filter_by(id=id_comment).count()
    likes = Likes.query.filter_by(user_id=user_id).first()
    print(likes)
    if likes is None : 
        newlike = Likes(comment_id =id_comment , user_id= user_id)
        db.session.add(newlike)
        db.session.commit()
        print(nblikes)
        return jsonify({"like": nblikes+1})
    db.session.delete(likes)
    db.session.commit()
    return jsonify({"like":nblikes, "status": "suppression du like"})

@comments_blueprint.route('/delete', methods=['DELETE'])
def delete_comments():
    """
    Supprime un commentaire existant.

    ---
    tags:
      - Commentaires
    parameters:
      - in: body
        name: Informations de suppression du commentaire
        description: Informations pour supprimer un commentaire existant.
        required: true
        schema:
          type: object
          properties:
            id_comment:
              type: integer
              description: ID du commentaire à supprimer.
    responses:
      200:
        description: Commentaire supprimé avec succès.
      404:
        description: Erreur lors de la suppression du commentaire.
    """
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
    
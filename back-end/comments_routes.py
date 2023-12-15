# comments_routes.py
from flask import Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt
from models import Comments, Likes, User, db

comments_blueprint = Blueprint('comments', __name__)

bcrypt = Bcrypt()

@comments_blueprint.route('/comments', methods=['GET'])
def get_comments():
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
    
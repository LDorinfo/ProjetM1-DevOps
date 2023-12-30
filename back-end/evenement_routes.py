# search_routes.py
from flask import Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt
from models import Evenement, db

event_blueprint = Blueprint('event', __name__)
bcrypt = Bcrypt()

@event_blueprint.route("/change", methods=["PUT"])
def event_change():
    user_id = session.get("user_id")
    title = request.json.get("title")
    description = request.json.get("description")
    prix = request.json.get("prix")
    image = request.json.get("image")
    idEvent = request.json.get("idEvent")

    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    
    event = Evenement.query.filter_by(id=idEvent).first()
    if title : 
        event.title = title 
    if description : 
        event.description = description 
    if prix : 
        event.prix= prix 
    if image: 
        event.image = image
    db.session.commit() 
    return jsonify({"evenement": event})

@event_blueprint.route("/create", methods=["POST"])
def event_create():
    user_id = session.get("user_id")
    title = request.json.get("title")
    description = request.json.get("description")
    prix = request.json.get("prix")
    image = request.json.get("image")

    if user_id is None or prix is None or description is None or image is None:
        return jsonify({"error": "Paramatre problem"}), 401

    event = Evenement(user_id= user_id, prix = prix, title= title, image = image, description = description)
    #if event is None : 
    #    return jsonify({"error": "Problem to create"})

    db.session.add(event)
    db.session.commit() 

    event_data = {
    'id': event.id,
    'user_id': event.user_id,
    'title': event.title,
    'description': event.description,
    'prix': event.prix,
    'image': event.image,
    # Include other attributes as needed
    }
    return jsonify({"evenement": event_data})

@event_blueprint.route("/events", methods=["GET"])
def events_get():
    events = Evenement.query.all()
    if events is None: 
        return jsonify({
            "error": "No events"
        }), 404
    
    events_data = [
        {
            'id': event.id,
            'user_id': event.user_id,
            'title': event.title,
            'description': event.description,
            'prix': event.prix,
            'image': event.image,
            # Include other attributes as needed
        }
        for event in events
    ]

    return jsonify({"events": events_data})

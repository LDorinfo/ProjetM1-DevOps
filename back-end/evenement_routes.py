# search_routes.py
from flask import Blueprint, jsonify, request, session
from flask_bcrypt import Bcrypt
from models import Evenement, User, db, Participant
from planning_routes import get_google_credentials, create_google_calendar_event, format_to_iso8601
from googleapiclient.discovery import build

event_blueprint = Blueprint('event', __name__)
bcrypt = Bcrypt()

@event_blueprint.route("/change", methods=["PUT"])
def event_change():
    """
    Met à jour les informations d'un événement existant.

    ---
    tags:
      - Événements
    parameters:
      - in: body
        name: Informations sur l'événement
        description: Informations mises à jour pour l'événement.
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Nouveau titre de l'événement.
            description:
              type: string
              description: Nouvelle description de l'événement.
            prix:
              type: float
              description: Nouveau prix de l'événement.
            image:
              type: string
              description: Nouveau chemin vers l'image de l'événement.
            idEvent:
              type: integer
              description: ID de l'événement à mettre à jour.
    responses:
      200:
        description: Informations mises à jour pour l'événement spécifié.
      401:
        description: Non autorisé, l'utilisateur n'est pas authentifié.
    """
    user_id = session.get("user_id")
    title = request.json.get("title")
    description = request.json.get("description")
    prix = request.json.get("prix")
    image = request.json.get("image")
    idEvent = request.json.get("idEvent")
    startdate = request.json.get("startdate")
    enddate = request.json.get("enddate")
    nbmax = request.json.get("nbmax")
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401
    
    event = Evenement.query.filter_by(id=idEvent).first()
    if title : 
        event.title = title 
    if nbmax : 
        event.nbparticipantmax = nbmax
    if description : 
        event.description = description 
    if prix : 
        event.prix= prix 
    if image: 
        event.image = image
    if startdate: 
        event.startdate = startdate
    if enddate: 
        event.enddate = enddate
    db.session.commit() 
    event_data = {
    'id': event.id,
    'user_id': event.user_id,
    'title': event.title,
    'description': event.description,
    'prix': event.prix,
    'image': event.image,
    'startdate': event.startdate,
    'enddate': event.enddate
    }
    return jsonify({"evenement": event_data})


@event_blueprint.route("/create", methods=["POST"])
def event_create():
    """
    Crée un nouvel événement.

    ---
    tags:
      - Événements
    parameters:
      - in: body
        name: Nouvel événement
        description: Informations pour créer un nouvel événement.
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Titre de l'événement.
            description:
              type: string
              description: Description de l'événement.
            prix:
              type: float
              description: Prix de l'événement.
            image:
              type: string
              description: Chemin vers l'image de l'événement.
    responses:
      200:
        description: Informations sur le nouvel événement créé.
      401:
        description: Paramètre manquant, l'utilisateur n'est pas authentifié.
    """
    user_id = session.get("user_id")
    title = request.json.get("title")
    description = request.json.get("description")
    prix = request.json.get("prix")
    image = request.json.get("image")
    startdate = request.json.get("startdate")
    enddate = request.json.get("enddate")
    nbmax = request.json.get("nbmax")
    if user_id is None or nbmax is None or prix is None or description is None or image is None or startdate is None or enddate is None:
        return jsonify({"error": "Paramatre problem"}), 401

    event = Evenement(user_id= user_id, prix = prix, nbparticipantmax= nbmax, title= title, image = image, description = description, startdate= startdate, enddate=enddate)
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
    'startdate': event.startdate,
    'enddate': event.enddate,
    'nbmax': event.nbparticipantmax,
    'nb': 0
    # Include other attributes as needed
    }
    return jsonify({"evenement": event_data})

@event_blueprint.route("/events", methods=["GET"])
def events_get():
    """
    Récupère la liste de tous les événements.

    ---
    tags:
      - Événements
    responses:
      200:
        description: Liste de tous les événements.
      404:
        description: Aucun événement trouvé.
    """
    events = Evenement.query.all()
    if events is None: 
        return jsonify({
            "error": "No events"
        }), 404
      
    events_data = []
    for event in events:
        # Calculer le nombre actuel de participants à l'événement
        nb_participants = Participant.query.filter_by(event_id=event.id).count()
        event_data = {
            'id': event.id,
            'user_id': event.user_id,
            'title': event.title,
            'description': event.description,
            'prix': event.prix,
            'image': event.image,
            'startdate': event.startdate,
            'enddate': event.enddate,
            'nbmax': event.nbparticipantmax,
            'nb': nb_participants
            # Inclure d'autres attributs si nécessaire
        }
        events_data.append(event_data)

    return jsonify({"events": events_data})
@event_blueprint.route("/adduser", methods=["PUT"])
def add_participant():
    """
    Add a user as a participant to an event.

    ---
    tags:
      - Événements
    parameters:
      - name: user_id
        in: body
        type: string
        required: true
        description: ID of the user
      - name: evenement_id
        in: body
        type: string
        required: true
        description: ID of the event

    responses:
      201:
        description: User added as a participant
      400:
        description: User ID or Event ID not provided
      404:
        description: User or Event not found
      200:
        description: User already a participant
    """
    user_id = request.json.get('user')
    evenement_id = request.json.get('evenement_id')
    if user_id is None : 
        return jsonify({"message": "L'utilisateur n'est pas connecté"}), 200
    if evenement_id is None:
        return jsonify({"error": "Event ID not provided"}), 400

    user = User.query.get(user_id)
    evenement = Evenement.query.get(evenement_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not evenement:
        return jsonify({"error": "Event not found"}), 404

    # Check if the user is already a participant in the event
    if Participant.query.filter_by(user_id=user_id, event_id=evenement_id).first():
        return jsonify({"message": "User already a participant"}), 200
    nb_participants = Participant.query.filter_by(event_id=evenement.id).count()
    if evenement.nbparticipantmax <= nb_participants : 
        return jsonify({"message": "There are not places"}), 200
    # Add the user as a participant to the event
    try:
      credentials, calendar_id = get_google_credentials(user_id)
      if credentials is None or calendar_id is None:
          return jsonify({"error": "Failed to retrieve Google credentials or calendar ID"}), 500
      print(credentials)
      # Prepare event data for Google Calendar
      iso_start = format_to_iso8601(evenement.startdate)
      iso_end = format_to_iso8601(evenement.enddate)
      event_data = {
        'summary': evenement.title,
        'description': evenement.description,
        'start': {
          'dateTime': iso_start,
          'timeZone': 'Europe/Paris',
        },
        'end': {
          'dateTime': iso_end,
          'timeZone': 'Europe/Paris',
        },
      }
      # Create event in Google Calendar
      print("Calendar ID:", calendar_id) 
      print(event_data)
      event = create_google_calendar_event(credentials, event_data, calendar_id)
      participant = Participant(user_id=user_id, event_id=evenement_id, google_id_event=event["id"])
      db.session.add(participant)
      db.session.commit()
      return jsonify({"message": "User added as a participant and event added to Google Calendar"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@event_blueprint.route("/isparticipant", methods=["GET"])
def is_participant():
    """
    Check if a user is a participant of an event.

    ---
    tags:
      - Événements
    parameters:
      - name: user_id
        in: query
        type: string
        required: true
        description: ID of the user
      - name: evenement_id
        in: query
        type: string
        required: true
        description: ID of the event

    responses:
      200:
        description: User participation status retrieved successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                participant:
                  type: boolean
                  description: Indicates whether the user is a participant or not
      404:
        description: User or Event not found
    """
    user_id = request.args.get('user_id')
    evenement_id = request.args.get('evenement_id')

    if user_id is None or evenement_id is None:
        return jsonify({"error": "User ID or Event ID not provided"}), 400

    user = User.query.get(user_id)
    evenement = Evenement.query.get(evenement_id)
    print(user)
    print(evenement)
    if not user or not evenement:
        return jsonify({"error": "User or Event not found"}), 404

    # Check if the user is a participant in the event
    is_participant = Participant.query.filter_by(user_id=user_id, event_id=evenement_id).first() is not None
    return jsonify({"participant": is_participant}), 200
@event_blueprint.route("/deleteuser", methods=["PUT"])
def delete_participant():
    """
    Remove a participant from an event.

    ---
    tags:
      - Événements
    parameters:
      - name: user_id
        in: body
        type: string
        required: true
        description: ID of the user
      - name: evenement_id
        in: body
        type: string
        required: true
        description: ID of the event

    responses:
      200:
        description: Participant removed successfully
      400:
        description: User ID or Event ID not provided
      404:
        description: User or Event not found
    """
    user_id = request.json.get('user')
    evenement_id = request.json.get('evenement_id')
    if user_id is None : 
        return jsonify({"message": "L'utilisateur n'est pas connecté"}), 200
    if evenement_id is None:
        return jsonify({"error": "Event ID not provided"}), 400

    user = User.query.get(user_id)
    evenement = Evenement.query.get(evenement_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not evenement:
        return jsonify({"error": "Event not found"}), 404

    # Check if the user is a participant in the event
    participant = Participant.query.filter_by(user_id=user_id, event_id=evenement_id).first()
    if not participant:
        return jsonify({"message": "User is not a participant"}), 200

    try:
        # Delete the event from the user's calendar
        credentials, calendar_id = get_google_credentials(user_id)
        if credentials is None or calendar_id is None:
            return jsonify({"error": "Failed to retrieve Google credentials or calendar ID"}), 500
        print("c'est bon")
        print(credentials)
        print(calendar_id)
        # Delete event from Google Calendar
        service = build('calendar', 'v3', credentials=credentials)
        
        # Supprimer l'événement
        deleted_event = service.events().delete(calendarId=calendar_id, eventId=participant.google_id_event).execute()
        print("c'est pas bon")
        # Remove the user as a participant from the event
        db.session.delete(participant)
        db.session.commit()
        return jsonify({"message": "Participant removed successfully and event deleted from user's calendar"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
from googleapiclient.discovery import build
from flask import Blueprint, request, jsonify, session
from models import Participant, User, db
from datetime import datetime
from google.auth.exceptions import RefreshError

def format_to_iso8601(date_string):
    # Convertit la chaîne de date en objet datetime
    print(date_string)
    date_object = datetime.strptime(date_string, '%Y, %m, %d, %H, %M')
    # Formate la date en format ISO 8601
    print(date_object)
    return date_object.isoformat()

def format_to_rfc3339(date_string):
    """# Convertit la chaîne de date en objet datetime
    print(date_string)
    date_object = datetime.fromisoformat(date_string)
    # Format the date in RFC3339 format
    print(date_object)
    return date_object.strftime('%Y-%m-%dT%H:%M:%S')"""
    try:
        # Convertit la chaîne de date en objet datetime en utilisant strptime
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        # Formatte la date en format RFC3339
        return date_object.strftime('%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        # Gérer l'erreur si la chaîne de date n'est pas au format attendu
        print("Erreur de format de date:", e)
        return None

planning_blueprint = Blueprint('planning', __name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_google_credentials(user_id):
  user_credentials_file = f'./usertoken/user_credentials_{user_id}.json'
  # Charger les informations d'identification depuis le fichier s'il existe
  credentials= None
  
  if os.path.exists(user_credentials_file):
    print("Merde")
    try :
      credentials = Credentials.from_authorized_user_file(user_credentials_file, SCOPES)
      if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
          credentials.refresh(Request())
    except RefreshError as e:
      print("Erreur lors du rafraîchissement du jeton:", e)
      raise e
    print("Les infos d'identification existe et credentials fonctionne")
    if credentials is None or not credentials.valid:
      redirect_uri = os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/callback")
      flow = InstalledAppFlow.from_client_secrets_file(
        './client_secret.json',
      SCOPES,
      redirect_uri=redirect_uri,
      )
      credentials = flow.run_local_server(port=8000)

      # Sauvegardez les informations d'identification pour la prochaine exécution
      with open(user_credentials_file, 'w') as token:
        token.write(credentials.to_json())
    #on cherche l'id du calendrier 
    calendar_service = get_calendar_service(credentials)
    calendar_list = calendar_service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])
    calendar_id = None
    for calendar in calendars:
      if calendar.get('summary') == 'Calendrier de Cineverse':
        calendar_id = calendar['id']
        break
    print("Utilisateur déjà connecté")
    print(calendar_id)
    if calendar_id is None: 
      application_calendar_data = {
      'summary': 'Calendrier de Cineverse',
      'description': 'Calendrier contenant les événements de planification pour l\'application Cineverse.'
      }
      service = build('calendar', 'v3', credentials=credentials)
      calendar = service.calendars().insert(body=application_calendar_data).execute()
      calendar_id = calendar['id']   
    return credentials,calendar_id
  print("pas d'info d'authentificationn")
  # Si les informations d'identification n'existent pas, demandez à l'utilisateur de s'authentifier
  redirect_uri = os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/callback")

  # If there are no (valid) credentials available, let the user log in.
  if credentials is None or not credentials.valid:
    print("Je suis pas valide")
    if credentials and credentials.expired and credentials.refresh_token:
      print("FUCK")
      credentials.refresh(Request())
      print("je suis ici")
    flow = InstalledAppFlow.from_client_secrets_file(
      './client_secret.json',
    SCOPES,
    redirect_uri=redirect_uri,
    )
    credentials = flow.run_local_server(port=8000)

    # Sauvegardez les informations d'identification pour la prochaine exécution
    with open(user_credentials_file, 'w') as token:
      token.write(credentials.to_json())
    print("les informations ont été écrites")
  # Vérifier si le calendrier de l'application existe déjà
  user_credentials = get_google_credentials(user_id)
  calendar_service = get_calendar_service(user_credentials)
  calendar_list = calendar_service.calendarList().list().execute()
  calendars = calendar_list.get('items', [])

  application_calendar_exists = False
  for calendar in calendars:
    if calendar.get('summary') == 'Calendrier de Cineverse':
      application_calendar_exists = True
      calendar_id = calendar['id']
      break
        
  # Si le calendrier n'existe pas, créez-le
  if not application_calendar_exists:
    application_calendar_data = {
      'summary': 'Calendrier de Cineverse',
      'description': 'Calendrier contenant les événements de planification pour l\'application Cineverse.'
    }
    service = build('calendar', 'v3', credentials=credentials)
    calendar = service.calendars().insert(body=application_calendar_data).execute()
    calendar_id = calendar['id']
  print("Utilisateur déjà connecté")
  print(calendar_id)
  return credentials, calendar_id

def get_calendar_service(credentials):
    """Obtenez le service de calendrier Google pour l'utilisateur."""
    service = build('calendar', 'v3', credentials=credentials)
    return service
def create_google_calendar_event(credentials, event_data, calendar_id):
    """
    Crée un nouvel événement dans le calendrier Google de l'utilisateur.

    Args:
        credentials (google.oauth2.credentials.Credentials): Les informations d'identification de l'utilisateur pour accéder à l'API Google Calendar.
        event_data (dict): Les données de l'événement à créer, comprenant les détails tels que le titre, la date de début et de fin.

    Returns:
        dict: Les détails de l'événement nouvellement créé, y compris son identifiant unique.
    """
    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId=calendar_id, body=event_data).execute()
    print("ca va")
    return event
@planning_blueprint.route('/add', methods=['POST'])
def add_eventPlanning():
    """
    Ajoute un nouvel événement de planification pour un film.

    ---
    tags:
      - Planning
    parameters:
      - in: body
        name: Event Planning
        description: Informations sur l'événement de planification à ajouter.
        required: true
        schema:
          type: object
          properties:
            idFilm:
              type: integer
              description: ID du film associé à l'événement.
            user:
              type: integer
              description: ID de l'utilisateur associé à l'événement.
            start:
              type: string
              description: Date et heure de début de l'événement au format ISO 8601.
            end:
              type: string
              description: Date et heure de fin de l'événement au format ISO 8601.
            title:
              type: string
              description: Titre de l'événement.

    responses:
      200:
        description: Événement de planification ajouté avec succès.
        schema:
          type: object
          properties:
            id:
              type: integer
              description: Identifiant unique de l'événement de planification.
            start:
              type: string
              description: Date et heure de début de l'événement au format ISO 8601.
            end:
              type: string
              description: Date et heure de fin de l'événement au format ISO 8601.
            title:
              type: string
              description: Titre de l'événement.
            film_id:
              type: integer
              description: ID du film associé à l'événement.
      404:
        description: Les informations requises ne sont pas présentes.
    """
    idFilm = request.json.get('idFilm')
    user_id = request.json.get('user')
    start= request.json.get('start')
    end= request.json.get('end')
    title = request.json.get('title')
    if idFilm is None :
        return jsonify({"error": "IdFilm is not present"}), 404
    if start is None or "" : 
      return jsonify({"error": "Start is not present"}), 404
    if end is None or "" :
      return jsonify({"error": "End is not present"}), 404
    if title is None :
      return jsonify({"error": "title is not present"}), 404
    if user_id is None: 
        return jsonify({"error" : "User unauthenticate"}),403
    user = User.query.filter_by(id=user_id).first()
    print(user)
    if user is None: 
        return jsonify({"error" : "User not found"}), 404
    #newprojet = Planning(title= title, end = end, start=start, user_id= user_id,film_id=idFilm)
    #db.session.add(newprojet)
    #db.session.commit()
    print(idFilm)
    print(start)
    print(title)
    print(user_id)
    print(end)

    # Récupération des informations d'identification Google pour l'utilisateur
    user_credentials, calendar_id = get_google_credentials(user_id)

    # Conversion des dates au format ISO 8601
    iso_start = format_to_iso8601(start)
    iso_end = format_to_iso8601(end)

    # Création des données de l'événement
    event_data = {
        'summary': title,
        'description': f'Film ID: {idFilm}',
        'start': {
            'dateTime': iso_start,
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': iso_end,
            'timeZone': 'Europe/Paris',
        },
    }

    # Création de l'événement dans le calendrier Google
    print("Calendar ID:", calendar_id) 
    event = create_google_calendar_event(user_credentials, event_data, calendar_id)
    return jsonify({
            "id": event['id'],
            "start": event['start']['dateTime'],
            "end": event['end']['dateTime'],
            "title": event['summary'],
            "film_id": idFilm
    }), 200
#séance, prix, note, moyenne. Où savoir voir le film, 
@planning_blueprint.route('/get', methods=['GET'])
def get_eventPlanning():
  """
    Récupère la liste des événements de planification pour l'utilisateur authentifié.

    ---
    tags:
      - Planning
    responses:
      200:
        description: Liste des événements de planification trouvés.
        schema:
          type: object
          properties:
            status:
              type: string
              description: Statut de la requête.
            planning:
              type: array
              description: Liste des événements de planification.
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Identifiant unique de l'événement de planification.
                  start:
                    type: string
                    description: Date et heure de début de l'événement au format ISO 8601.
                  end:
                    type: string
                    description: Date et heure de fin de l'événement au format ISO 8601.
                  title:
                    type: string
                    description: Titre de l'événement.
                  film_id:
                    type: integer
                    description: ID du film associé à l'événement.
      403:
        description: L'utilisateur n'est pas authentifié.
      404:
        description: Aucun événement de planification trouvé.
  """ 
  user_id = session.get("user_id")
  if user_id is None: 
    return jsonify({"error" : "User unauthenticate"}),403
  
  # Obtenez les informations d'identification de l'utilisateur
  user_credentials, calendar_id = get_google_credentials(user_id)
  if calendar_id is None:
    print(calendar_id is None)
    return jsonify({"error": "Calendar ID not found"}), 404
  # Obtenez le service du calendrier Google
  calendar_service = get_calendar_service(user_credentials)

  # Utilisez le service pour récupérer les événements du calendrier
  events_result = calendar_service.events().list(calendarId=calendar_id, timeMin=datetime.utcnow().isoformat() + 'Z', maxResults=10, singleEvents=True, orderBy='startTime').execute()
  print(events_result)
  events = events_result.get('items', [])

  if not events:
    return jsonify({"error": "No events found"}), 404

  events_list = []
  for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        print(start_time)
        end_time = event['end'].get('dateTime', event['end'].get('date'))

        # Conversion des dates au format ISO 8601
        iso_start = format_to_rfc3339(start_time)
        iso_end = format_to_rfc3339(end_time)
        if iso_start is None : 
           iso_start = start_time
           iso_end =end_time
        # Obtenez l'ID du film de la description de l'événement
        film_id = None
        description = event.get('description', '')
        if description:
            film_id_index = description.find('Film ID:')
            if film_id_index != -1:
                film_id = int(description[film_id_index + len('Film ID:'):].strip())
        if(film_id is None):
           events_list.append({
            "id": event['id'],
            "film_id": film_id, 
            "start": iso_start,
            "end": iso_end,
            "title": event['summary'],
            "evenement": True
        })
        events_list.append({
            "id": event['id'],
            "film_id": film_id, 
            "start": iso_start,
            "end": iso_end,
            "title": event['summary'], 
            "evenement": False
        })

  return jsonify({"status": "Found events", "events": events_list})

@planning_blueprint.route('/delete', methods=['DELETE'])
def delete_eventPlanning():
    """
    Supprime un événement de planification du calendrier de l'utilisateur.

    ---
    tags:
      - Planning
    parameters:
      - in: body
        name: Event ID
        description: L'identifiant unique de l'événement à supprimer.
        required: true
        schema:
          type: object
          properties:
            event_id:
              type: string
              description: L'identifiant unique de l'événement à supprimer.

    responses:
      200:
        description: Événement de planification supprimé avec succès.
        schema:
          type: object
          properties:
            status:
              type: string
              description: Statut de la requête.
            message:
              type: string
              description: Message indiquant que l'événement a été supprimé avec succès.
      404:
        description: L'événement à supprimer n'a pas été trouvé.
    """
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "User unauthenticated"}), 403

    event_id = request.json.get('id_event')
    if event_id is None:
        return jsonify({"error": "Event ID is not present"}), 404
    isevent = request.json.get('isevent')
    if isevent is None: 
       return jsonify({"error": "IsEvent is not present"}), 404
    # Obtenez les informations d'identification de l'utilisateur
    user_credentials, calendar_id = get_google_credentials(user_id)
    if calendar_id is None:
        return jsonify({"error": "Calendar ID not found"}), 404

    # Supprimer l'événement du calendrier

    service = build('calendar', 'v3', credentials=user_credentials)

    # Supprimer l'événement
    deleted_event = service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    if deleted_event is None:
      return jsonify({"error": "Failed to delete event"}), 500
    if isevent : 
      participant = Participant.query.filter_by(user_id=user_id, google_id_event= event_id).first()
      if not participant:
        return jsonify({"message": "User is not a participant"}), 200
      db.session.delete(participant)
      db.session.commit()
    return jsonify({"status": "Event deleted successfully", "message": "Event deleted successfully"}), 200

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Blueprint, request, jsonify, session
from models import Planning, User, db
from datetime import datetime

planning_blueprint = Blueprint('planning', __name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_google_credentials(user_id):
  user_credentials_file = f'./user_credentials_{user_id}.json'
  # Charger les informations d'identification depuis le fichier s'il existe
  credentials= None
  if os.path.exists(user_credentials_file):
    credentials = Credentials.from_authorized_user_file(user_credentials_file, SCOPES)
    return credentials
  # Si les informations d'identification n'existent pas, demandez à l'utilisateur de s'authentifier
  redirect_uri = os.environ.get("OAUTH_REDIRECT_URI", "http://localhost:5000/callback")

  # If there are no (valid) credentials available, let the user log in.
  if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      credentials.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
           './client_secret_221784644667-0c19vaqligbnd7gc52efc8cdqa32gm1l.apps.googleusercontent.com.json',
    SCOPES,
    redirect_uri=redirect_uri  
      )
      credentials = flow.run_local_server(port=0)

  # Sauvegardez les informations d'identification pour la prochaine exécution
  with open(user_credentials_file, 'w') as token:
    token.write(credentials.to_json())
  return credentials

def get_calendar_service(credentials):
    """Obtenez le service de calendrier Google pour l'utilisateur."""
    service = build('calendar', 'v3', credentials=credentials)
    return service

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
    if user is None: 
        return jsonify({"error" : "User not found"}), 404
    #newprojet = Planning(title= title, end = end, start=start, user_id= user_id,film_id=idFilm)
    #db.session.add(newprojet)
    #db.session.commit()

    user_credentials = get_google_credentials(user_id)
    newprojet ={
       'start': {
            'dateTime': start,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'UTC',
        },
        'idFilm': idFilm,
        'title': title
    }
    event = get_calendar_service(user_credentials).events().insert(calendarId='primary', body=event).execute()
    return jsonify({
        "id": newprojet.id,
        "start": newprojet.start,
        "end": newprojet.end,
        "title": newprojet.title,
        "film_id": newprojet.film_id
    })
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
  user_credentials = get_google_credentials(user_id)
  # Obtenez le service du calendrier Google
  calendar_service = get_calendar_service(user_credentials)

  # Utilisez le service pour récupérer les événements du calendrier
  events_result = calendar_service.events().list(calendarId='primary', timeMin=datetime.utcnow().isoformat() + 'Z', maxResults=10, singleEvents=True, orderBy='startTime').execute()
  events = events_result.get('items', [])

  if not events:
    return jsonify({"error": "No events found"}), 404

  events_list = []
  for event in events:
    start_time = event['start'].get('dateTime', event['start'].get('date'))
    end_time = event['end'].get('dateTime', event['end'].get('date'))

  events_list.append({
    "id": event['id'],
    "start": start_time,
    "end": end_time,
    "title": event['summary'],
  })

  return jsonify({"status": "Found events", "events": events_list})
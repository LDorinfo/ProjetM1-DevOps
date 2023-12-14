# search_routes.py
from flask import Blueprint, current_app, jsonify, request, session
from flask_bcrypt import Bcrypt
import requests

search_blueprint = Blueprint('search', __name__)
BASE_URL = 'https://api.themoviedb.org/3'

bcrypt = Bcrypt()


@search_blueprint.route('/search-multi', methods=['GET'])
def search_multi():
    keyword = request.args.get('query')
    #tmdb_api_key = current_app.config.get("TMDB_API_KEY")
    url = f'{BASE_URL}/search/multi'
    params = {'api_key': tmdb_api_key, 'query': keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        return jsonify({"error": "Pas de résultats à la recherche", "api_tmdb": tmdb_api_key}), 401 
    
@search_blueprint.route('/api/trending-movie', methods=['GET'])
def trending_movies():
    tmdb_api_key = current_app.config.get("TMDB_API_KEY")
    url = f'{BASE_URL}/trending/movie/day?language=fr-FR'
    params = {'api_key': tmdb_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        print("On retourne rien")
        return []
    
@search_blueprint.route('/api/trending-tv', methods=['GET'])
def trending_tv():
    tmdb_api_key = current_app.config.get("TMDB_API_KEY")
    url = f'{BASE_URL}/trending/tv/week?language=fr-FR'
    params = {'api_key': tmdb_api_key}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []

@search_blueprint.route('/filtre', methods=['GET'])
def filtre_movies():
    tmdb_api_key = current_app.config.get("TMDB_API_KEY")
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
    
@search_blueprint.route('/tv/filtre', methods=['GET'])
def search_tv():
    tmdb_api_key = current_app.config.get("TMDB_API_KEY")
    keyword = request.args.get('query')
    url = f'{BASE_URL}/discover/tv'

    params = {'api_key': tmdb_api_key, 'with_genres':keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return search_results
    else:
        return [] 
@search_blueprint.route('/discover-western-movies', methods=['GET'])
def western_movies():
    tmdb_api_key = current_app.config.get("TMDB_API_KEY")
    url = f'{BASE_URL}/discover/movie'
    params = {'api_key': tmdb_api_key, 'with_genres':37, 'language':'fr-FR'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()
        return jsonify(search_results.get('results', []))
    else:
        return []
    
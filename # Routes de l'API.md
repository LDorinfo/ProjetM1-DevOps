# Routes de l'API.md

1# Routes de l'API entre le serveurs et le Client
## Signin 
**Nom du service Web:** Signin
**URL:** 	POST 	/register
**Description :** 	Créer un utilisateur
**Paramètres d’entrée:** username, password, lastName, firstName, email, phone_number
**Exemples de sortie :** 
{"error": "user already exists"}), 409
{
        "id": new_user.id,
        "email": new_user.email,
        "username": new_user.username,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "phone_number": new_user.phone_number,
        "isconnected": new_user.isconnected
    }
**Erreurs possibles:** si l’utilisateur existe déjà, login déjà pris (409), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Signin.js

## Login
**Nom du service Web:** Login
**URL:** 	PUT 	/login
**Description :** 	Connexion de l'utilisateur. 
**Paramètres d’entrée:** username, password
**Exemples de sortie :** 
{"error": "Incorrect Login"}), 401 
{"error": "Incorrect Password"}), 401
{
        "id": user.id,
        "username": user.username,
        "isconnected": user.isconnected
    }
**Erreurs possibles:** si le username n'est pas le bon ou si le password n'est pas bon(401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Login.js

## Session/ @me
**Nom du service Web:** IsConnected
**URL:** 	POST 	/@me
**Description :** 	information sur la session de l'utilisateur. 
**Paramètres d’entrée:** user_id
**Exemples de sortie :** 
{"error": "Unauthorized"}), 401
{
        "id": user.id,
        "email": user.email
    }
**Erreurs possibles:** L'utilisateur n'existe pas dans la base de données(401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Pas encore utilisé dans le front

## UserInfo
**Nom du service Web:** UserInfo
**URL:** 	GET 	/api/userinfo
**Description :** 	obtenir les informations de l'utilisateur
**Paramètres d’entrée:** user_id
**Exemples de sortie :** 
{"error":"Unknown user"}), 401 
{
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "isconnected": user.isconnected
    }
**Erreurs possibles:** si l'id de l'utilisateur n'existe pas (401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé mais pas encore utilisé danns le front
**Composant JS:** Profil.js

## SetUser
**Nom du service Web:** SetUser
**URL:** 	PUT	/modify
**Description :** 	modification des information de l'utilisateur
**Paramètres d’entrée:** username, password, lastName, firstName, email, phone_number
**Exemples de sortie :** 
{"error": "User not authenticated"}), 401
{"error": "User not found"}), 404,
{
        "id": user.id,
        "username": user.username,
        "isconnected": True
    }
**Erreurs possibles:** L'utilisateur n'est pas authentifié (401), l'utilisateur n'existe pas (401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Pas encore utilisé dans le front

## Connected
**Nom du service Web:** Connected
**URL:** 	GET	/api/users/connected
**Description :** 	vérifie si l'utilisateur est connecté
**Paramètres d’entrée:** user_id
**Exemples de sortie :** 
{"error":"Unknown user"}), 401 ,
{"error": "disconnected"}), 401 ,
{
        "isconnected": True
}
**Erreurs possibles:** l'utilisateur n'est pas connu de la base de données (401), L'utilisateur n'est pas authentifié (401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** ConnectionPanel.js / n'existe plus remplacé par @me 

## Logout 
**Nom du service Web:** Logout
**URL:** 	PUT	/users/logout
**Description :** déconnecte l'utilisateur
**Paramètres d’entrée:** user_id
**Exemples de sortie :** 
jsonify({"error": "User not authenticated"}), 401
jsonify({"error": "User not found"}), 404
jsonify({"message": "Logout successful"})
**Erreurs possibles:** L'utilisateur n'est pas connecté (401), l'utilisateur n'existe pas (404), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** ConnectionPannel.js

## DeleteComment
**Nom du service Web:** DeleteComment
**URL:** 	DELETE	/comments/delete
**Description :** supprime un commentaire
**Paramètres d’entrée:**
**Exemples de sortie :** 
return jsonify({"error":"Not found id"}), 404
return jsonify({"error":"Not found comment"}), 404
 jsonify({
        "status": "delete comment",
        "id": id_comment
    })
**Erreurs possibles:** Ne trouve aucun commentaire (404), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Message.js 

## Like_comment
**Nom du service Web:** Like_comment
**URL:** 	POST	/comments/like
**Description :** ajoute un like au commentaire et si l'utilisateur a déjà mis un like le supprime. 
**Paramètres d’entrée:**user_id, id_comment
**Exemples de sortie :** 
jsonify({"status":"Not found Id in database User"}),404
jsonify({"status":"Not found Id in database Comment"}),404 
jsonify({"like": nblikes+1})
jsonify({"like":nblikes, "status": "suppression du like"})
**Erreurs possibles:** Ne trouve aucun commentaire ou pas l'utilisateur (404), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Message.js 

## EditComment
**Nom du service Web:** EditComment
**URL:** 	PUT	/comments/edit
**Description :** modification du commentaire 
**Paramètres d’entrée:**comment_text, id_comment, noteUser
**Exemples de sortie :** 
jsonify({"error":"Not found text"}), 404
jsonify({"error":"Not found id"}), 404
jsonify({"error":"Not found note"}), 404
jsonify({"error":"Not found comment"}), 404
jsonify({
        "status": "update comment"
    })
**Erreurs possibles:** Ne trouve pas l'un des paramètres ou le commentaire en question (404), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** Message.js 

## CreateComment
**Nom du service Web:** CreateComment
**URL:** 	POST	/comments/create
**Description :** création d'un commentaire
**Paramètres d’entrée:**comments, note, idFilm, username
**Exemples de sortie :** 
jsonify({"error":"Comments without idFilm"}), 404
return jsonify({"error" : "User unauthenticate, it's guest and he can not publish"}),403
jsonify({"error" : "User not found"}), 404
jsonify({
        "id": newcomments.id,
        "username": user.username,
        "comment_text": newcomments.comment_text,
        "note": newcomments.note,
        "user_id": newcomments.user_id,
        "film_id": newcomments.film_id, 
        "like_user": 0
    })
**Erreurs possibles:** Ne trouve pas l'un des paramètres ou le commentaire en question (404), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** MessageForm.js 

## GetComment
**Nom du service Web:** GetComments
**URL:** 	GET	/comments/comments
**Description :** avoir tous les commentaires pour un certain film 
**Paramètres d’entrée:** idFilm
**Exemples de sortie :** 
jsonify({"status":"Not found Id in database Comment"}), 404 
jsonify({"error":"Aucun commentaire"}), 404 
jsonify({"error" : "User not found"}), 404
jsonify({"status": "Found comments", "comments": comments_list})
**Erreurs possibles:** Ne trouve pas l'id du film ou de commentaire pour ce film ou ne trouve pas l'utilisateur pour tel commentaire (404), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** PageFilm.js

## searchMulti
**Nom du service Web:** searchMulti
**URL:** 	GET	/search/search-multi
**Description :** effectue une recherche dans l'API TMDB pour trouver le film par mot clé
**Paramètres d’entrée:**query
**Exemples de sortie :** 
jsonify({"error": "Pas de résultats à la recherche"}), 401 
search_results = response.json()
        return search_results
**Erreurs possibles:** Ne trouve aucun résultat (401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** BarreRecherche.js 


## TrendingMovies
**Nom du service Web:** TrendingMovies
**URL:** 	GET	/search/trending-movies
**Description :** effectue une recherche dans l'API TMDB pour les films qui sont tendances. 
**Paramètres d’entrée:** 
**Exemples de sortie :** 
jsonify(search_results.get('results', [])),  []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js

## TrendingTV
**Nom du service Web:** TrendingTV
**URL:** 	GET	/search/trending-tv
**Description :** effectue une recherche dans l'API TMDB pour les tendance à la télé. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## FiltreMovies
**Nom du service Web:** FiltreMovies
**URL:** 	GET	/search/filtre
**Description :** effectue une recherche dans l'API TMDB pour les films d'un certain genre. 
**Paramètres d’entrée:**query
**Exemples de sortie :** 
search_results = response.json()
        return search_results
[]
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** NavigationBar.js 

## SearchTV
**Nom du service Web:** SearchTV
**URL:** 	GET	/search/tv/filtre
**Description :** effectue une recherche dans l'API TMDB pour les serie d'un certain genre. 
**Paramètres d’entrée:**query
**Exemples de sortie :** 
search_results = response.json()
        return search_results
[]
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** In progress
**Composant JS:** NavigationBar.js 

## DiscoverWesternMovies
**Nom du service Web:** DiscoverWesternMovies
**URL:** 	GET	/search/discover-western-movies
**Description :** effectue une recherche dans l'API TMDB pour les films policiers. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## SetEvent
**Nom du service Web:** SetEvent
**URL:** 	PUT	/event/change
**Description :** modifier un événement
**Paramètres d’entrée:** user_id, title, description, prix, image, idEvent
**Exemples de sortie :** 
jsonify({"error": "User not authenticated"}), 401
jsonify({"evenement": event})
**Erreurs possibles:** l'utilisateur n'est pas connecté (401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** En cours
**Composant JS:** EvenementPage.js 

## CreateEvent
**Nom du service Web:** CreateEvent
**URL:** 	POST	/event/create
**Description :** créer un événement
**Paramètres d’entrée:** user_id, title, description, prix, image
**Exemples de sortie :** 
jsonify({"error": "Paramatre problem user"}), 401
jsonify({"error": "Paramatre problem"}), 401
jsonify({"evenement": event})
**Erreurs possibles:** l'utilisateur n'est pas connecté ou l'un des paramètres est invalide (401), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finish 
**Composant JS:** ProfilPage.js 

## GetEvents
**Nom du service Web:** GetEvents
**URL:** 	GET	/event/events
**Description :** retourne tous les événements
**Paramètres d’entrée:** 
**Exemples de sortie :** 
jsonify({
            "error": "No events"
        }), 404
jsonify({"events": events})
**Erreurs possibles:** Il n'y a pas d'évenement (404) le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** En cours
**Composant JS:** HomePage.js 
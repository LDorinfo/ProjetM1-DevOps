# Routes de l'API entre le serveurs et le Client

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
**URL:** 	POST 	/login
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
**URL:** 	PATCH 	/modify
**Description :** 	modification des information de l'utilisateur
**Paramètres d’entrée:** user_id
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
**Composant JS:** ConnectionPanel.js

## TrendingMovies
**Nom du service Web:** TrendingMovies
**URL:** 	GET	/api/trending-movies
**Description :** effectue une recherche dans l'API TMDB pour les films qui sont tendances. 
**Paramètres d’entrée:** 
**Exemples de sortie :** 
jsonify(search_results.get('results', [])),  []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js

## TrendingTV
**Nom du service Web:** TrendingTV
**URL:** 	GET	/api/trending-tv
**Description :** effectue une recherche dans l'API TMDB pour les tendance à la télé. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverActionMovies
**Nom du service Web:** DiscoverActionMovies
**URL:** 	GET	/api/discover-action-movies
**Description :** effectue une recherche dans l'API TMDB pour les films d'action. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverAdventureMovies
**Nom du service Web:** DiscoverAdventureMovies
**URL:** 	GET	/api/discover-adventure-movies
**Description :** effectue une recherche dans l'API TMDB pour les films d'aventure. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 


## DiscoverAnimationMovies
**Nom du service Web:** DiscoverAnimationMovies
**URL:** 	GET	/api/discover-animation-movies
**Description :** effectue une recherche dans l'API TMDB pour les films d'animation. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverComedyMovies
**Nom du service Web:** DiscoverComedyMovies
**URL:** 	GET	/api/discover-comedy-movies
**Description :** effectue une recherche dans l'API TMDB pour les films comiques. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverCrimeMovies
**Nom du service Web:** DiscoverCrimeMovies
**URL:** 	GET	/api/discover-crime-movies
**Description :** effectue une recherche dans l'API TMDB pour les films policiers. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverDocumentaryMovies
**Nom du service Web:** DiscoverDocumentaryMovies
**URL:** 	GET	/api/discover-documentary-movies
**Description :** effectue une recherche dans l'API TMDB pour les films documentaire. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverDramaMovies
**Nom du service Web:** DiscoverDramaMovies
**URL:** 	GET	/api/discover-drama-movies
**Description :** effectue une recherche dans l'API TMDB pour les films dramatiques. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverFamilyMovies
**Nom du service Web:** DiscoverFamilyMovies
**URL:** 	GET	/api/discover-family-movies
**Description :** effectue une recherche dans l'API TMDB pour les films policiers. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverFantasyMovies
**Nom du service Web:** DiscoverFantasyMovies
**URL:** 	GET	/api/discover-fantasy-movies
**Description :** effectue une recherche dans l'API TMDB pour les films fantastiques. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverHistoryMovies
**Nom du service Web:** DiscoverHistoryMovies
**URL:** 	GET	/api/discover-history-movies
**Description :** effectue une recherche dans l'API TMDB pour les films historiques. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverHorrorMovies
**Nom du service Web:** DiscoverHorrorMovies
**URL:** 	GET	/api/discover-horror-movies
**Description :** effectue une recherche dans l'API TMDB pour les films d'horreur. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverMusicMovies
**Nom du service Web:** DiscoverMusicMovies
**URL:** 	GET	/api/discover-music-movies
**Description :** effectue une recherche dans l'API TMDB pour les films musicaux. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverMysteryMovies
**Nom du service Web:** DiscoverMysteryMovies
**URL:** 	GET	/api/discover-mystery-movies
**Description :** effectue une recherche dans l'API TMDB pour les films mystères. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverRomanceMovies
**Nom du service Web:** DiscoverRomanceMovies
**URL:** 	GET	/api/discover-romance-movies
**Description :** effectue une recherche dans l'API TMDB pour les films romantiques. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverSciencefictionMovies
**Nom du service Web:** DiscoverScienceFictionMovies
**URL:** 	GET	/api/discover-sciencefiction-movies
**Description :** effectue une recherche dans l'API TMDB pour les films de science-fiction. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverthrillerMovies
**Nom du service Web:** DiscoverThrillerMovies
**URL:** 	GET	/api/discover-thriller-movies
**Description :** effectue une recherche dans l'API TMDB pour les films à suspense. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverWarMovies
**Nom du service Web:** DiscoverWarMovies
**URL:** 	GET	/api/discover-war-movies
**Description :** effectue une recherche dans l'API TMDB pour les films sur la guerre. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 

## DiscoverWesternMovies
**Nom du service Web:** DiscoverWesternMovies
**URL:** 	GET	/api/discover-western-movies
**Description :** effectue une recherche dans l'API TMDB pour les films policiers. 
**Paramètres d’entrée:**
**Exemples de sortie :** 
jsonify(search_results.get('results', [])), 200,   []
**Erreurs possibles:** Ne trouve aucun résultat (retourne un tableau vide), le serveur de bdd ne répond pas (le serveur va interroger la base de données, le serveur est incapable de mener à bien l’opération) ou erreur interne (500).
**Avancement du service :** finalisé
**Composant JS:** HomePage.js 
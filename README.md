"# ProjetM1-DevOps"

[![Version 0.2](https://img.shields.io/badge/Version-0.2-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.2)
[![Version 0.3](https://img.shields.io/badge/Version-0.3-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.3)
[![Version 0.4](https://img.shields.io/badge/Version-0.4-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.4)
[![Version 1.0](https://img.shields.io/badge/Version-1.0-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/valpha)
[![Tags](https://img.shields.io/badge/tag-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/tags)
[![Qualité de code](https://img.shields.io/badge/Codacy-brightgreen.svg)](https://app.codacy.com/organizations/gh/LDorinfo/repositories)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/blob/main/LICENCE)

Notre projet consiste en un site de critique de cinéma. Il permet de partager son avis. 

Pour utiliser React il faut installer le module react, je vous invite à regader sur ce site : `https://code.visualstudio.com/docs/nodejs/reactjs-tutorial`

Pour installer react-toastify : 
`npm install react-toastify`

Pour le côté client : 

[![Version 0.2](https://img.shields.io/badge/Version-0.2-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.2)
[![Version 0.3](https://img.shields.io/badge/Version-0.3-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.3)
[![Version 0.4](https://img.shields.io/badge/Version-0.4-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.4)
[![Version 1.0](https://img.shields.io/badge/Version-1.0-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/valpha)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/blob/main/client/LICENCE)

1- Installer les dépendances du client avec la commande `npm install` depuis le dossier client

2- (Si besoin installer react-icon/fa : 
`npm install react-icons`
Pour l'api Swagger installer : `npm install swagger-ui-react` 
Pour big calendar : `npm install react-big-calendar`
facultatif car les dépendances s'intallent toutes dès qu'on lance npm install)
3 - Lancer le client avec la commande `npm start` depuis le dossier client. Le client est lancé sur le port 3000.

4 - Ouvrir un navigateur et se rendre à l'adresse `http://localhost:3000/`

#Pour la partie Backend

[![Version 0.2](https://img.shields.io/badge/Version-0.2-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.2)
[![Version 0.3](https://img.shields.io/badge/Version-0.3-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.3)
[![Version 0.4](https://img.shields.io/badge/Version-0.4-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.4)
[![Version 1.0](https://img.shields.io/badge/Version-1.0-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/valpha)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/blob/main/back-end/LICENCE)

1- S'assurer d'avoir une version de python installer sur son ordinateur : `python3 --version`

2- Se mettre sur le dossier backend (cd back-end)

( il faut installer requests si vous ne l'avez pas : `pip install requests` )

3- Creer son envrironnement `virtuel avec python -m venv mon_env` et l'activer avec `source mon_env/bin/activate` ou sur Windows avec la commande `.\mon_env\Scripts\activate`

4- Installer les requirements ( `pip install -r requirements.txt` )


5- Installer Redis brew install redis (sur mac) puis le lancer brew services start redis

6- lancer le serveur `python3 app.py`. Le serveur est lancé sur le port 5000.

Pour désactiver l'environnement virtuel il faut : 
  Sous Windows taper : `.\mon_env\Scripts\deactivate`
  Sous Linux/macOS : `source mon_env/bin/deactivate`


## API Swagger 
Nous avons une api swagger dans le back avec le framework flasgger. Pour la lancer il faut langer le back, le serveur : `python3 app.py`

Ensuite il faut ouvrir la page http://localhost:5000/apidocs/ dans le navigateur web. 

## Analyse de code / qualité de code
[![Qualité de code](https://img.shields.io/badge/Codacy-brightgreen.svg)](https://app.codacy.com/organizations/gh/LDorinfo/repositories)

Pour l'analyse de code nous utilisons codacy. 

## Intégration continue 
Nous utilisons Github action pour l'intégration continue. https://github.com/LDorinfo/ProjetM1-DevOps/actions 

## Tests Front: Cypress
Nous utilisons pour tester le front avec des tests unitaires et end to end cypress. Pour lancer cypress vous devez vous placer dans le front, avoir lancer le front et le back et lancer la commande `./node_modules/.bin/cypress open` dans le répertoire client. 
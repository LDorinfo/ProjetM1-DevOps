"# ProjetM1-DevOps" 

[![Version 0.2](https://img.shields.io/badge/Version-0.2-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.2)
[![Version 0.3](https://img.shields.io/badge/Version-0.3-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.3)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/blob/main/LICENCE)

Notre projet consiste en un site de critique de cinéma. Il permet de partager son avis. 

Pour utiliser React il faut installer le module react, je vous invite à regader sur ce site : https://code.visualstudio.com/docs/nodejs/reactjs-tutorial

Pour installer react-toastify
npm install react-toastify

Pour le côté client : 

[![Version 0.2](https://img.shields.io/badge/Version-0.2-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.2)
[![Version 0.3](https://img.shields.io/badge/Version-0.3-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.3)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/blob/main/client/LICENCE)

1- Installer les dépendances du client avec la commande npm install depuis le dossier client

Si besoin installer react-icon/fa : 
\\\ npm react-icon/fa \\\
2- pour l'api Swagger installer :\\\ npm install swagger-ui-react \\\
3 - Lancer le client avec la commande npm start depuis le dossier client. Le client est lancé sur le port 3000.

4 - Ouvrir un navigateur et se rendre à l'adresse http://localhost:3000/

#Pour la partie Backend

[![Version 0.2](https://img.shields.io/badge/Version-0.2-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.2)
[![Version 0.3](https://img.shields.io/badge/Version-0.3-brightgreen.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/releases/tag/v0.3)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LDorinfo/ProjetM1-DevOps/blob/main/back-end/LICENCE)

1- S'assurer d'avoir une version de python installer sur son ordinateur : \\\ python3 --version \\\

2- Se mettre sur le dossier backend (cd back-end)

( il faut installer requests si vous ne l'avez pas : \\\ pip install requests \\\ )

3- Creer son envrironnement virtuel avec \\\ python -m venv mon_env \\\ et l'activer avec source mon_env/bin/activate ou sur Windows avec la commande \\\ .\mon_env\Scripts\activate \\\

4- Installer les requirements ( \\\ pip install -r requirements.txt \\\ )


5- Inataller Redis brew install redis (sur mac) puis le lancer brew services start redis

6- lancer le serveur python3 app.py. Le serveur est lancé sur le port 5000.

Pour désactiver l'environnement virtuel il faut : 
  Sous Windows taper : \\\ .\mon_env\Scripts\deactivate \\\
  Sous Linux/macOS : \\\ source mon_env/bin/deactivate \\\

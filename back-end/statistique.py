# statistique
from flask import Blueprint, current_app, jsonify, request, session
from flask_bcrypt import Bcrypt
import requests
from models import User

statistic_blueprint = Blueprint('statistic', __name__)

@statistic_blueprint.route('/nb/user', methods=['GET'])
def get_nbuser():
    nb = User.query.count()
    if(nb is None): 
        return jsonify("error","erreur dans le calcul du nombre d'utilisateur")
    return jsonify({"nb": nb})


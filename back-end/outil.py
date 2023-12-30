import secrets
import hashlib

def generate_unique_token(email):
    # Combinez l'e-mail de l'utilisateur avec une chaîne aléatoire
    data = f'{email}{secrets.token_urlsafe(32)}'
    
    # Utilisez SHA-256 pour générer un hash unique
    token = hashlib.sha256(data.encode()).hexdigest()

    return token
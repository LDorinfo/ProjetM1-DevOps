from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15))
    isconnected = db.Column(db.Boolean, default=False)

class Comments(db.Model): 
    __tablename__="comments"
    id = db.Column(db.String(32), primary_key=True, unique=True,default=get_uuid)
    comment_text = db.Column(db.String(345), nullable=False)
    note = db.Column(db.Integer)  # note 
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    film_id = db.Column(db.String(32), nullable=False)
    user = db.relationship('User', backref='comments')

class Watchlist(db.Model):
    __tablename__ = "watchlist"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    film_id = db.Column(db.String(32), nullable=False)

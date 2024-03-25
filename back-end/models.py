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
    likes = db.relationship('Likes', backref='user_likes' )
    comments = db.relationship('Comments', backref='user_comments' )
    watchlist = db.relationship('Watchlist', backref='user_watchlist' )
    participation = db.relationship('Participant', backref='participation_user' )

#    evenements = db.relationship('Evenement', backref='user_evenements')
class Comments(db.Model): 
    __tablename__="comments"
    id = db.Column(db.String(32), primary_key=True, unique=True,default=get_uuid)
    comment_text = db.Column(db.String(345), nullable=False)
    note = db.Column(db.Integer)  # note 
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    film_id = db.Column(db.String(32), nullable=False)
    user = db.relationship('User', backref='comments_user' )
    likes = db.relationship('Likes', backref='comments_likes' )

class Likes(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.String(32), db.ForeignKey('comments.id'), nullable=False)
    user = db.relationship('User', backref='likes_user', )
    comment = db.relationship('Comments', backref='likes_comments' )

class Watchlist(db.Model):
    __tablename__ = "watchlist"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    film_id = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(60))
    poster_path = db.Column(db.String(100))
    media_type = db.Column(db.String(32))
    user = db.relationship('User', backref='watchlist_user' )

class Evenement(db.Model):
    __tablename__ = "evenement"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(32))
    description = db.Column(db.String(64))
    prix = db.Column(db.Integer)
    image = db.Column(db.String(32))
    startdate = db.Column(db.String(32))
    enddate = db.Column(db.String(32))
    nbparticipantmax =db.Column(db.Integer)
    user = db.relationship('User', backref='evenement_user' )
class Participant(db.Model):
    __tablename__= "participant"
    id= db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.String(32), db.ForeignKey('evenement.id'), nullable=False)
    user = db.relationship('User', backref='participation_user' ) 
    google_id_event = db.Column(db.String(32))
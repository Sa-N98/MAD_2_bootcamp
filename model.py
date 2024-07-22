from flask_sqlalchemy import SQLAlchemy
from flask_security import  UserMixin, RoleMixin
from datetime import datetime

db= SQLAlchemy()






roles_users= db.Table('roles_users',
                      db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
                      )

class User(db.Model,UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String,unique=True, nullable=False)
    password=db.Column(db.String)
    active=db.Column(db.Boolean )
    fs_uniquifier = db.Column(db.String)
    user_type=db.Column(db.String)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users',lazy='dynamic'))
    last_login = db.Column(db.DateTime)
    API_token = db.Column(db.String ,  default=None )
    myPlaylist= db.relationship("playlist", secondary="user_playlist")

    def log_login(self):
        self.last_login = datetime.now()
        db.session.commit()

class Role(db.Model,RoleMixin):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description= db.Column(db.String,nullable=False)

class songs(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable = False)
    name = db.Column(db.String)
    artist = db.Column(db.String)
    album = db.Column(db.String)
    year = db.Column(db.Integer)
    url = db.Column(db.String) 

class playlist(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable = False)
    playlistName = db.Column(db.String)
    songList = db.Column(db.String)


class user_playlist(db.Model):
    __tablename__ = "user_playlist"
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id") , primary_key=True, nullable = False )
    user_id = db.Column(db.Integer,  db.ForeignKey("User.id"), primary_key=True, nullable = False)
    
    
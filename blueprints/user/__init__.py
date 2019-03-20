import random, logging
from blueprints import db
from flask_restful import fields


class Users(db.Model):

    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique =True)
    password = db.Column(db.String(50), nullable =False)
    email = db.Column(db.String(50), nullable =False, unique=True)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    
    response_field = {
        'user_id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'email': fields.String,
        'address': fields.String,
        'phone': fields.String,

    }

    user_profile_response = {
        'username': fields.String,
        'email': fields.String,
        'address': fields.String,
        'phone': fields.String,

    }
    def __init__(self, user_id, username, password, email, address, phone):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.address = address
        self.phone = phone
    
    def __repr__(self):
        return '<Users %r>' %self.user_id

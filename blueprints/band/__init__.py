import random, logging
from blueprints import db
from flask_restful import fields


class Bands(db.Model):

    __tablename__ = "band"
    band_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique =True)
    password = db.Column(db.String(50), nullable =False)
    bandName = db.Column(db.String(100), nullable =False)
    bandDesc = db.Column(db.String(1000))
    bandMail = db.Column(db.String(50), nullable =False, unique=True)
    bandAddress = db.Column(db.String(100))
    bandPhone = db.Column(db.String(100))
    bandPhoto = db.Column(db.String(100))
    
    response_field = {
        'band_id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'bandName': fields.String,
        'bandDesc': fields.String,
        'bandMail': fields.String,
        'bandAddress': fields.String,
        'bandPhone': fields.String,
        'bandPhoto': fields.String

    }

    band_profile_response = {
        'bandName': fields.String,
        'bandDesc': fields.String,
        'bandMail': fields.String,
        'bandAddress': fields.String,
        'bandPhone': fields.String,
        'bandPhoto': fields.String

    }
    def __init__(self, band_id, username, password, bandName, bandDesc, bandMail, bandAddress, bandPhone, bandPhoto):
        self.band_id = band_id
        self.username = username
        self.password = password
        self.bandName = bandName
        self.bandDesc = bandDesc
        self.bandMail = bandMail
        self.bandAddress = bandAddress
        self.bandPhone = bandPhone
        self.bandPhoto = bandPhoto
    
    def __repr__(self):
        return '<Bands %r>' %self.band_id

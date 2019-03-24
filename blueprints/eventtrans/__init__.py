import random, logging
from blueprints import db
from flask_restful import fields

class Transactionevent(db.Model):

    __tablename__ = "TransaksiEvent"
    tr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable =False)
    event_name = db.Column(db.String(100), nullable =False)
    user_name = db.Column(db.String(100), nullable =False)
    price = db.Column(db.Integer, nullable =False)
    quantity = db.Column(db.Integer, nullable =False)
    band_id = db.Column(db.Integer, nullable =False)
    bandName = db.Column(db.String(100), nullable =False)

    response_field = {
        'tr_id': fields.Integer,
        'event_id': fields.Integer,
        'user_id': fields.Integer,
        'event_name': fields.String,
        'user_name': fields.String,
        'price': fields.Integer,
        'quantity': fields.Integer,
        'band_id': fields.Integer,
        'bandName': fields.String
    }

    public_response_field = {
        'event_name': fields.String,
        'user_name': fields.String,
        'price': fields.Integer,
        'quantity': fields.Integer,
        'bandName': fields.String
    }

    def __init__(self, tr_id, event_id, user_id, event_name, user_name, price, quantity, band_id, bandName):
        self.tr_id = tr_id
        self.event_id = event_id
        self.user_id = user_id
        self.event_name = event_name
        self.user_name = user_name
        self.price = price
        self.quantity = quantity
        self.band_id = band_id
        self.bandName = bandName
    
    def __repr__(self):
        return '<Transactionevent %r>' %self.tr_id
    
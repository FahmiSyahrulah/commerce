import random, logging
from blueprints import db
from flask_restful import fields

class Event(db.Model):

    __tablename__ = "event"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    band_id = db.Column(db.Integer, nullable=False)
    bandName = db.Column(db.String(100), nullable =False)
    event_name = db.Column(db.String(100), nullable =False)
    price = db.Column(db.Integer, nullable =False)
    location = db.Column(db.String(100), nullable =False)
    quantity = db.Column(db.Integer, nullable =False)
    event_desc = db.Column(db.String(500), nullable =False)
    event_photo = db.Column(db.String(100), nullable =False)

    response_field = {
        'event_id': fields.Integer,
        'band_id': fields.Integer,
        'bandName': fields.String,
        'event_name': fields.String,
        'price': fields.Integer,
        'location': fields.String,
        'quantity': fields.Integer,
        'event_desc': fields.String,
        'event_photo': fields.String
    }

    public_response_field = {
        'bandName': fields.String,
        'event_name': fields.String,
        'price': fields.Integer,
        'location': fields.String,
        'quantity': fields.Integer,
        'event_desc': fields.String,
        'event_photo': fields.String
    }

    def __init__(self, event_id, band_id, bandName, event_name, price, location, quantity, event_desc, event_photo):
        self.event_id = event_id
        self.band_id = band_id
        self.bandName = bandName
        self.event_name = event_name
        self.price = price
        self.location = location
        self.quantity = quantity
        self.event_desc = event_desc
        self.event_photo = event_photo
    
    def __repr__(self):
        return '<Event %r>' %self.event_id
    
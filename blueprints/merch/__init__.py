import random, logging
from blueprints import db
from flask_restful import fields

class Merch(db.Model):

    __tablename__ = "merch"
    merch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    band_id = db.Column(db.Integer, nullable=False)
    bandName = db.Column(db.String(100), nullable =False)
    merch_name = db.Column(db.String(100), nullable =False)
    price = db.Column(db.Integer, nullable =False)
    kategori = db.Column(db.String(100), nullable =False)
    quantity = db.Column(db.Integer, nullable =False)
    merch_desc = db.Column(db.String(500), nullable =False)
    merch_photo = db.Column(db.String(100), nullable =False)

    response_field = {
        'merch_id': fields.Integer,
        'band_id': fields.Integer,
        'bandName': fields.String,
        'merch_name': fields.String,
        'price': fields.Integer,
        'kategori': fields.String,
        'quantity': fields.Integer,
        'merch_desc': fields.String,
        'merch_photo': fields.String
    }

    public_response_field = {
        'bandName': fields.String,
        'merch_name': fields.String,
        'price': fields.Integer,
        'kategori': fields.String,
        'quantity': fields.Integer,
        'merch_desc': fields.String,
        'merch_photo': fields.String
    }

    def __init__(self, merch_id, band_id, bandName, merch_name, price, kategori, quantity, merch_desc, merch_photo):
        self.merch_id = merch_id
        self.band_id = band_id
        self.bandName = bandName
        self.merch_name = merch_name
        self.price = price
        self.kategori = kategori
        self.quantity = quantity
        self.merch_desc = merch_desc
        self.merch_photo = merch_photo
    
    def __repr__(self):
        return '<Merch %r>' %self.merch_id
    
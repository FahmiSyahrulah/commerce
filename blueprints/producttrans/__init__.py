import random, logging
from blueprints import db
from flask_restful import fields

class Transactionproduct(db.Model):

    __tablename__ = "TransaksiProduk"
    tr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merch_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable =False)
    merch_name = db.Column(db.String(100), nullable =False)
    user_name = db.Column(db.String(100), nullable =False)
    price = db.Column(db.Integer, nullable =False)
    quantity = db.Column(db.Integer, nullable =False)

    response_field = {
        'tr_id': fields.Integer,
        'merch_id': fields.Integer,
        'user_id': fields.Integer,
        'merch_name': fields.String,
        'user_name': fields.String,
        'price': fields.Integer,
        'quantity': fields.Integer
    }

    public_response_field = {
        'merch_name': fields.String,
        'user_name': fields.String,
        'price': fields.Integer,
        'quantity': fields.Integer
    }

    def __init__(self, tr_id, merch_id, user_id, merch_name, user_name, price, quantity):
        self.tr_id = tr_id
        self.merch_id = merch_id
        self.user_id = user_id
        self.merch_name = merch_name
        self.user_name = user_name
        self.price = price
        self.quantity = quantity
    
    def __repr__(self):
        return '<Transactionproduct %r>' %self.tr_id
    
import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.user import Users
from blueprints.event import Event
from blueprints.eventtrans import Transactionevent
from . import *

bp_transEvent = Blueprint('transactionEvent', __name__)
api = Api(bp_transEvent)

class UserTransactionEvent(Resource):
    @jwt_required 
    def post(self):
        user = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('event_id', location='args', required=True)        
        parse.add_argument('quantity', type=int, location='args', required=True)

        args = parse.parse_args()

        qryEvent = Event.query.filter_by(event_id=args['event_id']).first()
        if qryEvent is not None:
            temp = marshal(qryEvent, Event.response_field)
            print(temp)
            total = temp['price']*args['quantity']
            qryEvent.quantity = qryEvent.quantity-args['quantity']
            if qryEvent.quantity >= 0:
                new_trans = Transactionevent(None, args['event_id'], user['user_id'], temp['event_name'], user['username'], total, args['quantity'], temp['band_id'], temp['bandName'])
                db.session.add(new_trans)
                db.session.commit()

                return {"status":"success" ,"message": "pembelian berhasil", "transaksi": marshal(new_trans, Transactionevent.public_response_field)}, 200, {'Content-Type': 'application/json'}
            else:
                return {"status":"failed" ,"message": "Produk tidak mencukupi"}, 200, {'Content-Type': 'application/json'}
        else :
            return {'status': 'failed', "message": "Produk tidak ditemukan"}, 404, {'Content-Type': 'application/json'}

    @jwt_required
    def get(self):
        user = get_jwt_claims()
        qry = Transactionevent.query.filter_by(user_id=user['user_id']).all()
        if qry is not None:
            rows = []
            for row in qry:
                temp = marshal(row, Transactionevent.public_response_field)
                rows.append(temp)
            return {'status':'sucess', 'EventTransaksi': rows}, 200, {'Content-Type': 'application/jason'}
        return {'status': 'Not_found', 'message': 'Transaksi event tidak ditemukan'}, 404, {'Content-Type': 'application/json'}
        
api.add_resource(UserTransactionEvent, '/user/transevent')

class BandEvents(Resource):
    @jwt_required
    def get(self):
        band = get_jwt_claims()
        qry = Transactionevent.query.filter_by(band_id=band['band_id']).all()
        if qry is not None:
            rows = []
            for row in qry:
                temp = marshal(row, Transactionevent.public_response_field)
                rows.append(temp)
            return {'status':'sucess', 'EventTransaksi': rows}, 200, {'Content-Type': 'application/jason'}
        return {'status': 'Not_found', 'message': 'Transaksi event tidak ditemukan'}, 404, {'Content-Type': 'application/json'}
api.add_resource(BandEvents, '/band/transevent')
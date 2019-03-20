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
        print(user)
        parse = reqparse.RequestParser()
        parse.add_argument('event_id', location='args', required=True)        
        parse.add_argument('quantity', type=int, location='args', required=True)

        args = parse.parse_args()

        qryEvent = Event.query.filter_by(event_id=args['event_id']).first()
        if qryEvent is not None:
            temp = marshal(qryEvent, Event.public_response_field)
            total = temp['price']*args['quantity']
            qryEvent.quantity = qryEvent.quantity-args['quantity']
            if qryEvent.quantity >= 0:
                new_trans = Transactionevent(None, args['event_id'], user['user_id'], temp['event_name'], user['username'], total, args['quantity'])
                db.session.add(new_trans)
                db.session.commit()

                return {"message": "SUCCESS"}, 200, {'Content-Type': 'application/json'}
            else:
                return {"message": "Produk tidak mencukupi"}, 200, {'Content-Type': 'application/json'}
        else :
            return {'status': 'Not_found'}, 404, {'Content-Type': 'application/json'}

api.add_resource(UserTransactionEvent, '/user/transevent')
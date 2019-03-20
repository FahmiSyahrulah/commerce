import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.user import Users
from blueprints.merch import Merch
from blueprints.producttrans import Transactionproduct
from . import *

bp_transProd = Blueprint('transaction', __name__)
api = Api(bp_transProd)

class UserTransaction(Resource):
    @jwt_required 
    def post(self):
        user = get_jwt_claims()
        print(user)
        parse = reqparse.RequestParser()
        parse.add_argument('merch_id', location='args', required=True)        
        parse.add_argument('quantity', type=int, location='args', required=True)

        args = parse.parse_args()

        qryMerch = Merch.query.filter_by(merch_id=args['merch_id']).first()
        if qryMerch is not None:
            temp = marshal(qryMerch, Merch.public_response_field)
            total = temp['price']*args['quantity']
            qryMerch.quantity = qryMerch.quantity-args['quantity']
            if qryMerch.quantity >= 0:
                new_trans = Transactionproduct(None, args['merch_id'], user['user_id'], temp['merch_name'], user['username'], total, args['quantity'])
                db.session.add(new_trans)
                db.session.commit()

                return {"message": "SUCCESS"}, 200, {'Content-Type': 'application/json'}
            else:
                return {"message": "Produk tidak mencukupi"}, 200, {'Content-Type': 'application/json'}
        else :
            return {'status': 'Not_found'}, 404, {'Content-Type': 'application/json'}

api.add_resource(UserTransaction, '/user/trans')
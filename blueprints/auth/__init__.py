import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.band import Bands
from blueprints.user import Users

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class BandLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()

        qry = Bands.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        if qry is not None:
            token = create_access_token(identity=marshal(qry, Bands.response_field))
        else:
            return{'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401
        return{'status':'success','token': token}, 200 

api.add_resource(BandLogin, '/login/band')

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        qry = Users.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        if qry is not None:
            token = create_access_token(identity=marshal(qry, Users.response_field))
        else:
            return{'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401
        return{'status':'success','token': token}, 200 


api.add_resource(UserLogin, '/login/user')
        
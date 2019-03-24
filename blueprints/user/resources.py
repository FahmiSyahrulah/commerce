import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.user import Users

from . import *
bp_user = Blueprint('user', __name__)
api = Api(bp_user)

# Untuk fitur-fitur yang bisa dilakukan user
class UserResource(Resource):
    
    # fungsi user melakukan register 
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('password', location='json',  required=True)       
        parse.add_argument('email', location='json', required=True)
        parse.add_argument('address', location='json')
        parse.add_argument('phone', location='json')

        args = parse.parse_args()

        qry = Users.query.filter_by(username = args['username']).first()
        if qry is not None:
            return {'message': 'USERNAME_ALREADY_EXISTS'}

        new_user = Users(None, args['username'], args['password'], args['email'], args['address'], args['phone'])
        db.session.add(new_user)
        db.session.commit()

        return {"status":"success", 'profile':marshal(new_user, Users.response_field) }, 200, {'Content-Type': 'application/json'}
    
    # Fungsi user melihat profilnya
    @jwt_required
    def get(self):
        user = get_jwt_claims()
        qry = Users.query.get(user['user_id'])
        result = marshal(qry, Users.response_field)
        return {'status': 'success', 'data': result}, 200, {'Content-Type': 'application/json'}
    
    # fungsi untuk user mengedit profiilnya
    @jwt_required
    def put(self):
        user = get_jwt_claims()
        qry = Users.query.get(user['user_id'])
        result = marshal(qry, Users.response_field)
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', default=result['username'])
        parse.add_argument('password', location='json',  default=result['password'])       
        parse.add_argument('email', location='json', default=result['email'])
        parse.add_argument('address', location='json', default=result['address'])
        parse.add_argument('phone', location='json', default=result['phone'])
        
        args = parse.parse_args()
        qry.username = args['username']
        qry.password = args['password']
        qry.email = args['email']
        qry.address = args['address']
        qry.phone = args['phone']
        db.session.commit()
        return {'status':'success', 'message': 'profile_updated', 'profile': marshal(qry, Users.response_field)}, 200, {'Content-Type': 'application/json'}

    #fungsi untuk user menghapus akunnya
    @jwt_required
    def delete(self):
        user = get_jwt_claims()
        qry = Users.query.get(user['user_id'])
        
        db.session.delete(qry)
        db.session.commit()
        return {'status':'success', 'message': 'akun terhapus'}, 200, {'Content-Type': 'application/json'}

api.add_resource(UserResource, '/user/profile')




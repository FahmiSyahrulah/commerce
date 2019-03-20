import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.band import Bands
from . import *

bp_band = Blueprint('band', __name__)
api = Api(bp_band)

# Untuk fitur-fitur yang bisa dilakukan band
class BandResource(Resource):
    
    # fungsi band melakukan register 
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', required=True)
        parse.add_argument('password', location='json',  required=True)
        parse.add_argument('bandName', location='json', required=True)
        parse.add_argument('bandDesc', location='json')        
        parse.add_argument('bandMail', location='json', required=True)
        parse.add_argument('bandAddress', location='json')
        parse.add_argument('bandPhone', location='json')
        parse.add_argument('bandPhoto', location='json')

        args = parse.parse_args()

        qry = Bands.query.filter_by(username = args['username']).first()
        if qry is not None:
            return {'message': 'USERNAME_ALREADY_EXISTS'}

        new_band = Bands(None, args['username'], args['password'], args['bandName'], args['bandDesc'], args['bandMail'], args['bandAddress'], args['bandPhone'], args['bandPhoto'])
        db.session.add(new_band)
        db.session.commit()

        return {"message": "SUCCESS"}, 200, {'Content-Type': 'application/json'}
    
    # Fungsi band melihat profilnya
    @jwt_required
    def get(self):
        band = get_jwt_claims()
        qry = Bands.query.get(band['band_id'])
        result = marshal(qry, Bands.response_field)
        return result, 200, {'Content-Type': 'application/json'}
    
    # fungsi untuk band mengedit profiilnya
    @jwt_required
    def put(self):
        band = get_jwt_claims()
        qry = Bands.query.get(band['band_id'])
        result = marshal(qry, Bands.response_field)
        parse = reqparse.RequestParser()
        parse.add_argument('username', location='json', default=result['username'])
        parse.add_argument('password', location='json',  default=result['password'])
        parse.add_argument('bandName', location='json', default=result['bandName'])
        parse.add_argument('bandDesc', location='json', default=result['bandDesc'])        
        parse.add_argument('bandMail', location='json', default=result['bandMail'])
        parse.add_argument('bandAddress', location='json', default=result['bandAddress'])
        parse.add_argument('bandPhone', location='json', default=result['bandPhone'])
        parse.add_argument('bandPhoto', location='json', default=result['bandPhoto'])
        
        args = parse.parse_args()
        qry.username = args['username']
        qry.password = args['password']
        qry.bandName = args['bandName']
        qry.bandDesc = args['bandDesc']
        qry.bandMail = args['bandMail']
        qry.bandAddress = args['bandAddress']
        qry.bandPhone = args['bandPhone']
        qry.bandPhoto = args['bandPhoto']
        db.session.commit()
        return {'message': 'Data_Updated', 'data': marshal(qry, Bands.response_field)}, 200, {'Content-Type': 'application/json'}

    #fungsi untuk band menghapus akunnya
    @jwt_required
    def delete(self):
        band = get_jwt_claims()
        qry = Bands.query.get(band['band_id'])
        
        db.session.delete(qry)
        db.session.commit()
        return {'message': 'Data_Deleted'}, 200, {'Content-Type': 'application/json'}

api.add_resource(BandResource, '/band/profile')

class ViewAllBand(Resource):
    #pencarian band dan band detail
    def get(self, bandID = None):
        parse = reqparse.RequestParser()
        parse.add_argument('p', type=int, location='args', default=1)
        parse.add_argument('rp', type=int, location='args', default=10)
        parse.add_argument('band', location='args')
        args = parse.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        if bandID is None:
            qry = Bands.query
            if args['band'] is not None:
                qry = qry.filter(Bands.bandName.like("%"+args['band']+"%"))
                if qry.first() is None:
                    return {'status': 'Band_not_found','message':'item not found'},404, { 'Content-Type': 'application/json' }

            rows = [{'halaman': args['p']}]
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Bands.band_profile_response))
            return {'status':'success','data':rows}, 200, {'Content-Type': 'application/json'}
        else: 
            qry = Bands.query.filter_by(band_id=bandID).first()
            if qry is not None:
                 return marshal(qry, Bands.band_profile_response), 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'NOT_FOUND'}, 404, {'Content-Type': 'application/json'}
        
api.add_resource(ViewAllBand, '/public/bands', '/public/bands/<int:bandID>')




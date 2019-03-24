import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.band import Bands
from blueprints.merch import Merch
from . import *

bp_merch = Blueprint('merch', __name__)
api = Api(bp_merch)

class BandMerch(Resource):
    
    # fungsi band menambahkan merchandise
    @jwt_required 
    def post(self):
        band = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('merch_name', location='json', required=True)        
        parse.add_argument('price', location='json', required=True)
        parse.add_argument('kategori', location='json', required=True)
        parse.add_argument('quantity', location='json', required=True)
        parse.add_argument('merch_desc', location='json', required=True)
        parse.add_argument('merch_photo', location='json', required=True)

        args = parse.parse_args()

        new_merch = Merch(None, band['band_id'], band['bandName'], args['merch_name'], args['price'], args['kategori'], args['quantity'], args['merch_desc'], args['merch_photo'])
        merch = marshal(new_merch, Merch.public_response_field)
        db.session.add(new_merch)
        db.session.commit()

        return {"status": "Sucess", 'message': "Merchandise ditambahkan", 'merchandise':merch}, 200, {'Content-Type': 'application/json'}
    
    # fungsi band menampilkan mercahndisenya dan detail merchandise
    @jwt_required
    def get(self, merchID = None):
        band = get_jwt_claims()

        if merchID is None:
            qry = Merch.query.filter_by(band_id=band['band_id']).all()
            rows = []
            for row in qry:
                temp = marshal(row, Merch.response_field)
                rows.append(temp)
        else:
            qry = Merch.query.filter_by(band_id=band['band_id']).filter_by(merch_id=merchID).first()
            if qry is not None:
                return {'status':'Sucess', 'merchandise':marshal(qry, Merch.response_field)}, 200, {'Content-Type': 'application/jason'}
            else:
                return {'status': 'Not_found', 'message': 'merchandise tidak ditemukan'}, 404, {'Content-Type': 'application/json'}
        
        return {'status':'Sucess', 'merchandises': rows}, 200, {'Content-Type': 'application/jason'}
    
    #fungsi band mengedit merchandisenya
    @jwt_required
    def put(self, merchID = None):
        band = get_jwt_claims()
        
        qryMerch = Merch.query.filter_by(band_id=band['band_id']).filter_by(merch_id=merchID).first()

        if qryMerch is None:
            return {'status': 'Not_found', 'message': 'merchandise tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

        else:
            merch = marshal(qryMerch, Merch.response_field)

            parse = reqparse.RequestParser()
            parse.add_argument('merch_name', location='json', default=merch['merch_name'])        
            parse.add_argument('price', location='json', default=merch['price'])
            parse.add_argument('kategori', location='json', default=merch['kategori'])
            parse.add_argument('quantity', location='json', default=merch['quantity'])
            parse.add_argument('merch_desc', location='json', default=merch['merch_desc'])
            parse.add_argument('merch_photo', location='json', default=merch['merch_photo'])

            args = parse.parse_args()

            qryMerch.merch_name = args['merch_name']
            qryMerch.price = args['price']
            qryMerch.kategori = args['kategori']
            qryMerch.quantity = args['quantity']
            qryMerch.merch_desc = args['merch_desc']
            qryMerch.merch_photo = args['merch_photo']

            db.session.commit()
            return {'status':'success', 'message':'updated', 'merch': marshal(qryMerch, Merch.response_field)}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, merchID):
        band = get_jwt_claims()

        qryMerch = Merch.query.filter_by(band_id = band['band_id']).filter_by(merch_id = merchID).first()

        if qryMerch is not None:
            db.session.delete(qryMerch)
            db.session.commit()
            return {'status': 'Data_Deleted', 'message': 'merchandise terhapus'}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'Not_found', 'message': 'merchandise tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

api.add_resource(BandMerch, '/band/merch', '/band/merch/<int:merchID>')

class PublicMerch(Resource):

    def get(self, merchID = None):
        if merchID is None:
            parse = reqparse.RequestParser()
            parse.add_argument('p', type=int, location='args', default=1)
            parse.add_argument('rp', type=int, location='args', default=10)
            parse.add_argument('search', location='args')
            args = parse.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry = Merch.query
            if args['search'] is not None:
                qry = qry.filter(Merch.bandName.like("%"+args['search']+"%"))
                if qry.first() is None:
                    qry = Merch.query.filter(Merch.merch_name.like("%"+args['search']+"%"))
                    if qry.first() is None:
                        qry = Merch.query.filter(Merch.kategori.like("%"+args['search']+"%"))
                        if qry.first() is None:
                            return {'status': 'Not_found','message':'merchandise not found'},404, { 'Content-Type': 'application/json' }
            
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Merch.public_response_field))
            return {'status': 'success', 'halaman': args['p'], 'merchandises':rows}, 200, {'Content-Type': 'application/json'}

        else:
            qry = Merch.query.get(merchID)
            if qry is not None:
                return {'status': 'success','merchandise':marshal(qry, Merch.public_response_field)}, 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'Not_found', 'message': 'merchandise tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

api.add_resource(PublicMerch, '/public/merch', '/public/merch/<int:merchID>')
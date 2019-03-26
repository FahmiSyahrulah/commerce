import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints import db
from blueprints.band import Bands
from blueprints.event import Event
from . import *

bp_event = Blueprint('event', __name__)
api = Api(bp_event)

class BandEvent(Resource):
    
    # fungsi band menambahkan event
    @jwt_required 
    def post(self):
        band = get_jwt_claims()
        parse = reqparse.RequestParser()
        parse.add_argument('event_name', location='json', required=True)        
        parse.add_argument('price', location='json', required=True)
        parse.add_argument('location', location='json', required=True)
        parse.add_argument('quantity', location='json', required=True)
        parse.add_argument('event_desc', location='json', required=True)
        parse.add_argument('event_photo', location='json', required=True)

        args = parse.parse_args()

        new_event = Event(None, band['band_id'], band['bandName'], args['event_name'], args['price'], args['location'], args['quantity'], args['event_desc'], args['event_photo'])
        db.session.add(new_event)
        db.session.commit()

        return {"status": "Sucess", 'message': "Event ditambahkan", 'event':marshal(new_event, Event.response_field)  }, 200, {'Content-Type': 'application/json'}
    
    # fungsi band menampilkan eventnya dan detail event
    @jwt_required
    def get(self, eventID = None):
        band = get_jwt_claims()

        if eventID is None:
            qry = Event.query.filter_by(band_id=band['band_id']).all()
            rows = []
            for row in qry:
                temp = marshal(row, Event.response_field)
                rows.append(temp)
        else:
            qry = Event.query.filter_by(band_id=band['band_id']).filter_by(event_id=eventID).first()
            if qry is not None:
                return marshal(qry, Event.response_field), 200, {'Content-Type': 'application/jason'}
            else:
                return {'status': 'Not_found', 'message': 'event tidak ditemukan'}, 404, {'Content-Type': 'application/json'}
        
        return {'status':'sucess', 'events': rows}, 200, {'Content-Type': 'application/jason'}
    
    #fungsi band mengedit eventnya
    @jwt_required
    def put(self, eventID = None):
        band = get_jwt_claims()
        
        qryEvent = Event.query.filter_by(band_id=band['band_id']).filter_by(event_id=eventID).first()

        if qryEvent is None:
            return {'status': 'Not_found', 'message': 'Event tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

        else:
            event = marshal(qryEvent, Event.response_field)

            parse = reqparse.RequestParser()
            parse.add_argument('event_name', location='json', default=event['event_name'])        
            parse.add_argument('price', location='json', default=event['price'])
            parse.add_argument('location', location='json', default=event['location'])
            parse.add_argument('quantity', location='json', default=event['quantity'])
            parse.add_argument('event_desc', location='json', default=event['event_desc'])
            parse.add_argument('event_photo', location='json', default=event['event_photo'])

            args = parse.parse_args()

            qryEvent.event_name = args['event_name']
            qryEvent.price = args['price']
            qryEvent.location = args['location']
            qryEvent.quantity = args['quantity']
            qryEvent.event_desc = args['event_desc']
            qryEvent.event_photo = args['event_photo']

            db.session.commit()
            return {'status':'Success', 'message':'Berhasil update', 'updated':marshal(qryEvent, Event.response_field)}, 200, {'Content-Type': 'application/json'}

    @jwt_required
    def delete(self, eventID):
        band = get_jwt_claims()

        qryEvent = Event.query.filter_by(band_id = band['band_id']).filter_by(merch_id = eventID).first()

        if qryEvent is not None:
            db.session.delete(qryEvent)
            db.session.commit()
            return {'status': 'Success', 'message': 'Event Terhapus'}, 200, {'Content-Type': 'application/json'}
        else:
            return {'status': 'Not_found', 'message': 'Event tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

api.add_resource(BandEvent, '/band/event', '/band/event/<int:eventID>')

class PublicEvent(Resource):

    def get(self, eventID = None):
        if eventID is None:
            parse = reqparse.RequestParser()
            parse.add_argument('p', type=int, location='args', default=1)
            parse.add_argument('rp', type=int, location='args', default=10)
            parse.add_argument('search', location='args')
            args = parse.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry = Event.query
            if args['search'] is not None:
                qry = qry.filter(Event.band_id.like(args['search']))
                if qry.first() is None:
                    qry = qry.filter(Event.bandName.like("%"+args['search']+"%"))
                    if qry.first() is None:
                        qry = Event.query.filter(Event.event_name.like("%"+args['search']+"%"))
                        if qry.first() is None:
                            qry = Event.query.filter(Event.location.like("%"+args['search']+"%"))
                            if qry.first() is None:
                                return {'status': 'Not_found','message':'event tidak ditemukan'},404, { 'Content-Type': 'application/json' }
            
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Event.public_response_field))
            return {'Status': 'Success', 'halaman': args['p'], 'events':rows}, 200, {'Content-Type': 'application/json'}

        else:
            qry = Event.query.get(eventID)
            if qry is not None:
                return {'Status': 'Success', 'event':marshal(qry, Event.public_response_field)}, 200, {'Content-Type': 'application/json'}
            else:
                return {'status': 'Not_found', 'message': 'event tidak ditemukan'}, 404, {'Content-Type': 'application/json'}

api.add_resource(PublicEvent, '/public/event', '/public/event/<int:eventID>')
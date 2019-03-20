from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse
from time import strftime
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fahmi:syahrulah@172.31.19.225:3306/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'DkbkNKNCOnONkPoooJBb'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


api = Api(app, catch_all_404s=True)


# middleware
@app.after_request
def after_request(response):
    if request.method=='GET':
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request': request.args.to_dict(),
            'response': json.loads (response.data.decode('utf-8')) }))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({'requests': request.get_json(), 
            'response': json.loads(response.data.decode('utf-8')) }))
    return response

from blueprints.band.resources import bp_band
from blueprints.user.resources import bp_user
from blueprints.auth import bp_auth
from blueprints.merch.resources import bp_merch
from blueprints.event.resources import bp_event
from blueprints.producttrans.resources import bp_transProd
from blueprints.eventtrans.resources import bp_transEvent
app.register_blueprint(bp_band)
app.register_blueprint(bp_auth)
app.register_blueprint(bp_user)
app.register_blueprint(bp_merch)
app.register_blueprint(bp_event)
app.register_blueprint(bp_transProd)
app.register_blueprint(bp_transEvent)
db.create_all()

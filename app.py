from flask import Flask, jsonify, make_response
from flask_restful import Api

from route.config import Config
from route.device import Device
from route.event import Event
from route.index import Index
from route.user import User

from lib.database import Database
from lib.message import Message

MESSAGE = Message()
APP = Flask(__name__)
API = Api(APP, catch_all_404s=True)

# it seems that this line of code is called twice
Database().create()

@APP.errorhandler(404)
def not_found(error):
    return make_response(jsonify(MESSAGE.errorhandler(404)), 404)

@APP.errorhandler(500)
def server_error(error):
    return make_response(jsonify(MESSAGE.errorhandler(500)), 500)

API.add_resource(Index, '/')
API.add_resource(Config, '/config')
API.add_resource(Device, 
    '/device/add',
    '/device/delete',
    "/device/<key>",
    "/devices",
    "/pulse"
    )
# api.add_resource(User, '/user')
API.add_resource(Event, 
    '/events',
    "/event/add",
    "/event/delete",
    "/event/update",
    "/event/clear"
    )

if __name__ == '__main__':
    APP.run()
  
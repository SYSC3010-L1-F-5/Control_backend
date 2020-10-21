from flask import Flask, jsonify, make_response
from flask_restful import Api

from route.config import Config
from route.device import Device
from route.event import Event
from route.index import Index
from route.user import User
from lib.message import errorhandler
from lib.database import Database
from lib.libuser import LibUser

# it seems that this line of code is called twice
Database().create()
LibUser().initialize()

APP = Flask(__name__)
API = Api(APP)

@APP.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(errorhandler(400)), 400)

@APP.errorhandler(404)
def not_found(error):
    return make_response(jsonify(errorhandler(404)), 404)

@APP.errorhandler(500)
def server_error(error):
    return make_response(jsonify(errorhandler(500)), 500)

API.add_resource(Index, '/')
API.add_resource(Config, '/config')
API.add_resource(Device, 
    '/device/add',
    '/device/delete',
    "/device/update",
    "/device/<key>",
    "/devices",
    "/pulse"
)
API.add_resource(User, 
    '/user',
    '/users',
    '/user/login',
    '/user/add',
    '/user/delete'
    '/user/update',
    '/user/logout',
    '/user/<uuid>'
)
API.add_resource(Event, 
    "/events",
    "/event/add",
    "/event/delete",
    "/event/update",
    "/event/clear",
    "/event/<uuid>"
)

if __name__ == '__main__':
    APP.run()
  
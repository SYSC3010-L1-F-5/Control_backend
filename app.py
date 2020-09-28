from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api
import os

from route.config import Config
from route.device import Device
from route.event import Event
from route.index import Index
from route.user import User

from lib.database import Database
from lib.message import Message

message = Message()
app = Flask(__name__)
api = Api(app)

# it seems that this line of code is called twice
Database().create()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(message.errorhandler(404)), 404)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify(message.errorhandler(500)), 500)

api.add_resource(Index, '/')
api.add_resource(Config, '/config')
api.add_resource(Device, 
    '/device/add',
    '/device/delete',
    "/devices",
    "/pulse"
    )
api.add_resource(User, '/user')
api.add_resource(Event, 
    '/events',
    "/event/add",
    "/event/delete",
    "/event/update"
    )

if __name__ == '__main__':
    app.run()
  
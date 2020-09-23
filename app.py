from flask import Flask, jsonify
from flask_restful import Resource, Api
import os

from route.config import Config
from route.device import Device
from route.event import Event
from route.index import Index
from route.user import User

from lib.database import Database

app = Flask(__name__)
api = Api(app)

# it seems that this line of code is called twice
Database().create()

api.add_resource(Index, '/')
api.add_resource(Config, '/config')
api.add_resource(Device, '/device/<string:operation>/<string:zone>/<string:type>/<string:name>')
api.add_resource(User, '/user')
api.add_resource(Event, '/event')

if __name__ == '__main__':
    app.run()
  
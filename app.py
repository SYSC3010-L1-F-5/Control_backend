from flask import Flask, jsonify
import os
from lib.Api import Api
from lib.Config import Config
from lib.Key import Key

app = Flask(__name__)
config = Config()
api = Api()

app.config.update(
    SECRET_KEY = os.urandom(16)
)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route('/', methods=['GET'])
@api.message
def index():
    return "hello world!"

@app.route('/config', methods=['GET'])
@api.message
def config_page():
    return config.get()

@app.route('/device/add/<string:zone>/<string:type>/<string:name>', methods=['GET'])
@api.message
def add_device(zone, type, name):
    device = {
        "zone": zone,
        "type": type,
        "name": name
    }
    key = Key()
    if key.add(device) is True:
        return str(key.get_key())

if __name__ == '__main__':
    app.run()
  
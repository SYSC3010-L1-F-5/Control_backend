from flask import Flask, json, render_template
import os
from lib.Api import Api
from lib.Config import Config
from lib.Key import Key

config = Config()
api = Api()

app = Flask(__name__)
app.config.update(
    SECRET_KEY = os.urandom(16)
)

@app.route('/', methods=['GET'])
@api.message
def index():
    return "hello world!"

@app.route('/config', methods=['GET'])
@api.message
def config_page():
    return config.get()

@app.route('/device/add/<string:zone>/<string:type>', methods=['GET'])
@api.message
def add_device(zone, type):
    device = {
        "zone": zone,
        "type": type
    }
    key = Key()
    if key.add(device) is True:
        return str(key.get_key())

if __name__ == '__main__':
    app.run()
  
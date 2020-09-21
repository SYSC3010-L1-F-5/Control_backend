from flask import Flask, json, render_template
import os
from lib.Config import Config
from lib.Test import Test

config = Config()

app = Flask(__name__)
app.config.update(
  SECRET_KEY = os.urandom(16)
)

@app.route('/', methods=['GET'])
def index():
  r = Test()
  
  return r.get_body()

@app.route('/config', methods=['GET'])
def config():
  return str(config.get())

if __name__ == '__main__':
  app.run()
  
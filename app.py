from flask import Flask, json, render_template
import os
from lib.Test import Test

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

app = Flask(__name__)
app.config.update(
  SECRET_KEY = os.urandom(16)
)

@app.route('/', methods=['GET'])
def index():
  r = Test()

  return r.get_body()


if __name__ == '__main__':
    app.run()
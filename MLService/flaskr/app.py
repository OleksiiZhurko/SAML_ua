from flask import Flask

from flaskr.config.di import _init
from flaskr.controller.controller import load_routes

app = Flask(__name__)
_init()
load_routes(app)

if __name__ == '__main__':
    app.run(debug=True)

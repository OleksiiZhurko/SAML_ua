from flask import Flask

from flaskr.config.di import init, get_cleaner, get_model_text_verifier
from flaskr.controller.controller import load_routes

app = Flask(__name__)
init()
load_routes(app, get_cleaner(), get_model_text_verifier())

if __name__ == '__main__':
    app.run(debug=True)

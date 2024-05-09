import logging as log

from flask import request, jsonify, Flask

from flaskr.config.di import get_ml_handler
from flaskr.consts.mls import ML_RNN, ML_SVM, ML_NB
from flaskr.service.ml_handlers import MLHandler


def load_routes(app: Flask) -> None:
    _ml_handler: MLHandler = get_ml_handler()

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.get_json()
        if not data or 'toPredict' not in data or 'mlModel' not in data:
            log.warning(f"Unexpected data received. Full request: {data}")
            return jsonify({"error": "Unexpected data received"}), 400

        predicted = _ml_handler.handle(
            data['mlModel'],
            [d['text'] for d in data['toPredict']],
            [d['lemmas'] for d in data['toPredict']]
        )

        return jsonify(
            {
                "predicted": predicted
            }
        )

    @app.route('/models', methods=['GET'])
    def models():
        return jsonify(
            {
                "models": [ML_RNN, ML_SVM, ML_NB]
            }
        )

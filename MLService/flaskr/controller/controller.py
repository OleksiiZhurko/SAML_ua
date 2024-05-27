import logging as log

from flask import request, jsonify, Flask

from flaskr.consts.mls import ML_RNN, ML_SVM, ML_NB
from flaskr.service.ml_handlers import MLHandler


def load_routes(app: Flask, ml_handler: MLHandler) -> None:
    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.get_json()
        if not data or 'toPredict' not in data or 'model' not in data:
            log.warning(f"Unexpected data received. Full request: {data}")
            return jsonify({"error": "Unexpected data received"}), 400

        if data['toPredict'] is None or len(data['toPredict']) == 0:
            log.warning(f"'toPredict' is empty or None. Full request: {data}")
            return jsonify({"error": "'toPredict' must not be empty"}), 400

        log.info(f"Request received: {data}")

        predicted = ml_handler.handle(
            data['model'],
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
                "models": [
                    {
                        "name": ML_RNN,
                        "description": "78%"
                    },
                    {
                        "name": ML_NB,
                        "description": "79%"
                    },
                    {
                        "name": ML_SVM,
                        "description": "80%"
                    },
                ]
            }
        )

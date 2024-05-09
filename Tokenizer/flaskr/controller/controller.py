import logging as log

from flask import request, jsonify, Flask

from flaskr.config.di import get_cleaner, get_model_text_verifier
from flaskr.service.cleaner import Cleaner
from flaskr.service.verifier import ModelTextVerifier


def load_routes(app: Flask) -> None:
    _cleaner: Cleaner = get_cleaner()
    _verifier: ModelTextVerifier = get_model_text_verifier()

    @app.route('/process_texts', methods=['POST'])
    def process_texts():
        data = request.get_json()
        if not data or 'texts' not in data:
            log.warning(f"Request does not contain values in 'texts'. Full request: {data}")
            return jsonify({"error": "Empty 'texts' array."}), 400

        processed = _cleaner.clean(data['texts'])

        verified = _verifier.verify(processed, 'isInModel' in data and data['isInModel'] is True)

        return jsonify(
            {
                "processed_texts": verified
            }
        )

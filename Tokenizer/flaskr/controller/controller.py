import logging as log

from flask import request, jsonify, Flask

from flaskr.service.cleaner import Cleaner
from flaskr.service.verifier import ModelTextVerifier


def load_routes(app: Flask, cleaner: Cleaner, verifier: ModelTextVerifier) -> None:

    @app.route('/processTexts', methods=['POST'])
    def process_texts():
        data = request.get_json()
        if not data or 'texts' not in data or not data['texts']:
            log.warning(f"Request does not contain values in 'texts'. Full request: {data}")
            return jsonify({"error": "Empty 'texts' array."}), 400
        log.info(f"Request received: '{data}'")
        processed = cleaner.clean(data['texts'])

        verified = verifier.verify(processed, 'inModel' in data and data['inModel'] is True)

        return jsonify(
            {
                "processed": verified
            }
        )

import unittest
from unittest.mock import MagicMock

from flask import Flask

from flaskr.consts.mls import ML_RNN
from flaskr.controller.controller import load_routes
from flaskr.service.ml_handlers import MLHandler


class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.ml_handler = MagicMock(spec=MLHandler)
        load_routes(self.app, self.ml_handler)
        self.client = self.app.test_client()

    def test_predict_successful(self):
        self.ml_handler.handle.return_value = ["positive"]

        payload = {
            "model": f"{ML_RNN}",
            "toPredict": [{"text": "Hello world", "lemmas": ["hello", "world"]}]
        }
        response = self.client.post('/predict', json=payload)
        self.assertEqual(200, response.status_code)
        self.assertEqual({"predicted": ["positive"]}, response.json)

    def test_predict_bad_request(self):
        payload = {"toPredict": [{"text": "Hello world", "lemmas": ["hello", "world"]}]}
        response = self.client.post('/predict', json=payload)
        self.assertEqual(400, response.status_code)
        self.assertIn("error", response.json)

    def test_models_endpoint(self):
        response = self.client.get('/models')
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, len(response.json['models']))
        self.assertEqual(ML_RNN, response.json['models'][0]['name'])


if __name__ == '__main__':
    unittest.main()

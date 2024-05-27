import unittest
from unittest import TestCase
from unittest.mock import patch

from flask import Flask

from flaskr.controller.controller import load_routes
from flaskr.service.cleaner import Cleaner
from flaskr.service.verifier import ModelTextVerifier


def create_app(cleaner: Cleaner, verifier: ModelTextVerifier):
    app = Flask(__name__)
    load_routes(app, cleaner, verifier)
    return app


class TestFlaskApi(TestCase):

    def setUp(self):
        self.cleaner_mock = patch('flaskr.config.di.get_cleaner').start()
        self.verifier_mock = patch('flaskr.config.di.get_model_text_verifier').start()
        self.cleaner_mock.clean.return_value = ['cleaned_text']
        self.verifier_mock.verify.return_value = ['verified_text']
        self.app = create_app(self.cleaner_mock, self.verifier_mock)
        self.client = self.app.test_client()

    def tearDown(self):
        patch.stopall()

    def test_process_success(self):
        response = self.client.post('/processTexts', json={
            "texts": ["some text"],
            "inModel": True
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual({"processed": ['verified_text']}, response.json)

    def test_process_empty_texts(self):
        response = self.client.post('/processTexts', json={"texts": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Empty 'texts' array.", response.json['error'])

    def test_process_no_texts(self):
        response = self.client.post('/processTexts', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Empty 'texts' array.", response.json['error'])

    def test_process_no_json(self):
        response = self.client.post('/processTexts')
        self.assertEqual(415, response.status_code)


if __name__ == '__main__':
    unittest.main()

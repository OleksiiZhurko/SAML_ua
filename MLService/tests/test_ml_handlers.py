import unittest
from unittest.mock import patch, MagicMock

import numpy as np

from flaskr.consts.mls import ML_RNN, ML_SVM, ML_NB
from flaskr.service.ml_handlers import BayesHandler, SVMHandler, RNNHandler, _labelize, _to_response


class TestMLHandlers(unittest.TestCase):
    def test_to_response(self):
        expected = {
            'model': ML_RNN,
            'text': 'test text',
            'predicted': 'Positive',
            'probabilities': {'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}
        }
        result = _to_response(ML_RNN, 'test text', 'Positive', 0.8, 0.1, 0.1)
        self.assertEqual(expected, result)

    def test_labelize(self):
        predictions = [[0.2, 0.8], [0.9, 0.1]]
        texts = ["text1", "text2"]
        result = _labelize(texts, predictions, ML_NB)
        expected = [
            {'model': ML_NB, 'text': 'text1', 'predicted': 'Positive',
             'probabilities': {'positive': 0.8, 'neutral': 0.0, 'negative': 0.2}},
            {'model': ML_NB, 'text': 'text2', 'predicted': 'Negative',
             'probabilities': {'positive': 0.1, 'neutral': 0.0, 'negative': 0.9}}
        ]
        self.assertEqual(expected, result)

    @patch('flaskr.service.ml_handlers.read_pickle')
    def test_bayes_handler(self, mock_read_pickle):
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.2, 0.8]]
        mock_tokenizer.transform.return_value = None
        mock_read_pickle.side_effect = [mock_tokenizer, mock_model]

        handler = BayesHandler()
        result = handler.handle(ML_NB, ['original text'], ['predict this'])
        self.assertEqual(1, len(result))
        self.assertIn('predicted', result[0])

    @patch('flaskr.service.ml_handlers.read_pickle')
    @patch('flaskr.service.ml_handlers.read_keras')
    def test_rnn_handler(self, mock_read_keras, mock_read_pickle):
        mock_tokenizer = MagicMock()
        mock_tokenizer.texts_to_sequences.return_value = [[1, 2, 3]]
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([[0.1, 0.9]])
        mock_read_pickle.return_value = mock_tokenizer
        mock_read_keras.return_value = mock_model

        handler = RNNHandler()
        result = handler.handle(ML_RNN, ['original text'], ['predict this'])
        self.assertEqual(1, len(result))
        self.assertIn('Positive', result[0]['predicted'])

    @patch('flaskr.service.ml_handlers.read_pickle')
    def test_svm_handler(self, mock_read_pickle):
        mock_tokenizer = MagicMock()
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = [[0.8, 0.2]]
        mock_read_pickle.side_effect = [mock_tokenizer, mock_model]

        handler = SVMHandler()
        result = handler.handle(ML_SVM, ['original text'], ['predict this'])
        self.assertEqual(1, len(result))
        self.assertIn('Negative', result[0]['predicted'])

    @patch('flaskr.service.ml_handlers.read_pickle')
    @patch('flaskr.service.ml_handlers.read_keras')
    def test_handler_chain_responsibility_when_no_handler_for_model_type(self, mock_read_keras,
                                                                         mock_read_pickle):
        mock_read_pickle.side_effect = MagicMock()
        mock_read_keras.side_effect = MagicMock()
        initial_handler = BayesHandler()
        svm_handler = SVMHandler()
        rnn_handler = RNNHandler()
        initial_handler.set_next(svm_handler).set_next(rnn_handler)

        result = initial_handler.handle('XYZ', ['text'], ['predict'])
        self.assertIn("Unknown 'XYZ'", result[0]['model'])


if __name__ == '__main__':
    unittest.main()

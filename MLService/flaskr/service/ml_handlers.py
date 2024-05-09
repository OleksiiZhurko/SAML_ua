from __future__ import annotations

import logging
from abc import abstractmethod, ABC

from keras.src.utils import pad_sequences

from flaskr.consts.mls import ML_NB, ML_SVM, ML_RNN, POSITIVE_PRED, NEGATIVE_PRED, NEUTRAL_PRED
from flaskr.utils.reader import read_pickle, read_keras


def _to_response(model: str, text: str, prediction: str, positive: float, neutral: float,
                 negative: float):
    return {
        'model': model,
        'text': text,
        'predicted': prediction,
        'probabilities': {
            POSITIVE_PRED: positive,
            NEUTRAL_PRED: neutral,
            NEGATIVE_PRED: negative
        }
    }


def _labelize(texts: list[str], predictions, model: str):
    predicted = []
    for i in range(len(predictions)):
        if predictions[i][0] < predictions[i][1]:
            predicted.append(
                _to_response(model, texts[i], POSITIVE_PRED, predictions[i][1], 0.0,
                             predictions[i][0]))
        else:
            predicted.append(
                _to_response(model, texts[i], NEGATIVE_PRED, predictions[i][1], 0.0,
                             predictions[i][0]))
    return predicted


class MLHandler(ABC):
    _next_handler: MLHandler = None

    def set_next(self, handler: MLHandler) -> MLHandler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, ml_type: str, originals: list[str], to_predict: list[str]):
        if self._next_handler:
            return self._next_handler.handle(ml_type, originals, to_predict)
        predicted = []
        logging.warning(f"'{ml_type}' does not exist as model")
        for i in range(len(to_predict)):
            predicted.append(
                _to_response(f"Unknown '{ml_type}'", originals[i], NEUTRAL_PRED, 0.0, 1.0, 0.0))
        return predicted


class BayesHandler(MLHandler):
    def __init__(self):
        super().__init__()
        self.tokenizer = read_pickle('tokenizer_nb.pickle')
        self.model = read_pickle('model_nb.pickle')

    def handle(self, ml_type: str, originals: list[str], to_predict: list[str]):
        if ml_type == ML_NB:
            sequences = self.tokenizer.transform(to_predict)
            predictions = self.model.predict_proba(sequences)
            return _labelize(originals, predictions, ML_NB)
        else:
            return super().handle(ml_type, originals, to_predict)


class SVMHandler(MLHandler):
    def __init__(self):
        super().__init__()
        self.tokenizer = read_pickle('tokenizer_svm.pickle')
        self.model = read_pickle('model_svm.pickle')

    def handle(self, ml_type: str, originals: list[str], to_predict: list[str]):
        if ml_type == ML_SVM:
            sequences = self.tokenizer.transform(to_predict)
            predictions = self.model.predict_proba(sequences)
            return _labelize(originals, predictions, ML_SVM)
        else:
            return super().handle(ml_type, originals, to_predict)


class RNNHandler(MLHandler):
    def __init__(self):
        super().__init__()
        self.tokenizer = read_pickle('tokenizer_rnn.pickle')
        self.model = read_keras('model_rnn.keras')

    def handle(self, ml_type: str, originals: list[str], to_predict: list[str]):
        if ml_type == ML_RNN:
            sequences = self.tokenizer.texts_to_sequences(to_predict)
            data_padded = pad_sequences(sequences, maxlen=30)
            predictions = self.model.predict(data_padded).tolist()
            return _labelize(originals, predictions, ML_RNN)
        else:
            return super().handle(ml_type, originals, to_predict)

import os

from flaskr.config.logger import setup_logger
from flaskr.service.ml_handlers import MLHandler, RNNHandler, SVMHandler, BayesHandler

_ml_handler: MLHandler


def _init() -> None:
    global _ml_handler

    setup_logger()

    if not os.path.exists('resources'):
        os.makedirs('resources')

    _ml_handler = RNNHandler()
    ml_svm = SVMHandler()
    ml_nb = BayesHandler()
    _ml_handler.set_next(ml_svm).set_next(ml_nb)


def get_ml_handler() -> MLHandler:
    return _ml_handler

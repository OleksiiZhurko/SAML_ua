import spacy
from spacy import Language

from flaskr.config.logger import setup_logger
from flaskr.service.cleaner import Cleaner
from flaskr.service.lemma import Lemmatizer
from flaskr.service.verifier import ModelTextVerifier

_nlp: Language
_cleaner: Cleaner
_lemmatizer: Lemmatizer
_modelTextVerifier: ModelTextVerifier


def _init() -> None:
    global _nlp, _cleaner, _lemmatizer, _modelTextVerifier

    _nlp = spacy.load("uk_core_news_md") # uk_core_news_trf
    setup_logger()

    _lemmatizer = Lemmatizer(nlp=_nlp)
    _cleaner = Cleaner(lemmatizer=_lemmatizer)
    _modelTextVerifier = ModelTextVerifier()


def get_cleaner() -> Cleaner:
    return _cleaner


def get_model_text_verifier() -> ModelTextVerifier:
    return _modelTextVerifier

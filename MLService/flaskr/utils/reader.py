import pickle
from typing import Any

from keras.src.saving import load_model


def read_pickle(tokenizer_file: str):
    tokenizer: Any
    with open(f"./resources/{tokenizer_file}", 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer


def read_keras(model_file: str):
    return load_model(f"./resources/{model_file}")

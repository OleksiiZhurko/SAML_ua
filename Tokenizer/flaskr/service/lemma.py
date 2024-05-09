import logging as log
import re
from typing import Any

from spacy import Language

from flaskr.consts.patterns import stop_words

_EXCLUDED_POSES: list[str] = ['PUNCT', 'PRON', 'NUM', 'CONJ', 'X', 'SCONJ']
_EXCLUDED_POS: str = 'PART'
_POLARITY_KEY: str = 'Polarity'


def _replace_word(text, to_replace, replacement) -> str:
    pattern = rf'\b{to_replace}\b'
    result = re.sub(pattern, replacement, text)
    return result


def _replace_words(text: str, to_replace: list[tuple[str, str]]) -> str:
    for old, new in to_replace:
        try:
            text = _replace_word(text, old, new)
        except Exception as e:
            log.error(f"Unable to replace old '{old}' to new '{new}' in '{text}'. Error: {e}")
    return text


class Lemmatizer:
    def __init__(self, nlp: Language):
        self.nlp = nlp

    def replace_named_entities(self, text: str) -> str:
        doc = self.nlp(text)
        ents: list[tuple[str, Any]] = [(ent.text, ent.label_) for ent in doc.ents]
        to_replace: list[tuple[str, str]] = []
        if len(ents) != 0:
            to_replace = self._find_replacements(ents)
        if len(to_replace) != 0:
            text = _replace_words(text, to_replace)
        return text

    def _find_replacements(self, ents) -> list[tuple[str, str]]:
        to_replace: list[tuple[str, str]] = []
        for line, _ in ents:
            newDoc = self.nlp(line)
            replacement = " ".join([d.lemma_ for d in newDoc])
            to_replace.append((newDoc.text, replacement))
        return to_replace

    def process_lemmas(self, text) -> str:
        doc = self.nlp(text)
        res = []
        for token in doc:
            if token.pos_ not in _EXCLUDED_POSES:
                if token.text not in stop_words:
                    if token.pos_ != _EXCLUDED_POS:
                        res.append(token.lemma_)
                    else:
                        polarity = token.morph.get(_POLARITY_KEY)
                        if len(polarity) != 0:
                            res.append(token.lemma_)
        return " ".join(res)

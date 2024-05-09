from flaskr.service.lemma import Lemmatizer
from flaskr.utils.pattern import align_symbols, clean_unused_symbols


class Cleaner:
    def __init__(self, lemmatizer: Lemmatizer):
        self.lemmatizer = lemmatizer

    def clean(self, rows) -> list[dict[str, str]]:
        result = []
        for text in rows:
            updated = align_symbols(text)
            updated = self.lemmatizer.replace_named_entities(updated)
            updated = self.lemmatizer.process_lemmas(updated)
            updated = clean_unused_symbols(updated)
            result.append(
                {
                    'text': text,
                    'processed': updated
                }
            )
        return result


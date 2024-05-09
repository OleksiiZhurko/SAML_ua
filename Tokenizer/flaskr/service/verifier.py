import logging as log
import os

_DIRECTORY_PATH: str = 'resources'


def _read_files_in_directory() -> list[str]:
    if not os.path.exists(_DIRECTORY_PATH):
        os.makedirs(_DIRECTORY_PATH)
    files = [f for f in os.listdir(_DIRECTORY_PATH) if
             os.path.isfile(os.path.join(_DIRECTORY_PATH, f))]
    file_contents = []
    log.info(f"Discovered {len(file_contents)} to read")
    for filename in files:
        file_path = os.path.join(_DIRECTORY_PATH, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                log.info("Model dictionaries loaded")
                file_contents.extend([line.strip() for line in file.readlines()])
        except Exception as e:
            log.warning(f"Failed to read {filename}. Error: {e}")
    return file_contents


class ModelTextVerifier:
    def __init__(self):
        self._words = _read_files_in_directory()
        if len(self._words) == 0:
            log.warning("There are no files with words on which the model was trained")

    def verify(self, response: list[dict[str, str]], check: bool) -> \
            list[dict[str, str | list[str] | bool]]:
        if check:
            self._verify(response)
        else:
            self._fill_with_empty(response)
        return response

    def _verify(self, response):
        for entity in response:
            missing: list[str] = []
            for lemma in entity['processed'].split(' '):
                if lemma not in self._words:
                    missing.append(lemma)
            if len(missing) > 0:
                log.warning(f"Missing lemmas {', '.join(missing)} for {entity['text']}")
            entity['missingLemmas'] = ', '.join(missing)
            entity['isInModel'] = entity['processed'] == ' '.join(missing)

    def _fill_with_empty(self, response):
        for entity in response:
            missing: list[str] = []
            for lemma in entity['processed'].split(' '):
                if lemma in self._words:
                    missing.append(lemma)
            entity['missingLemmas'] = None
            entity['isInModel'] = None

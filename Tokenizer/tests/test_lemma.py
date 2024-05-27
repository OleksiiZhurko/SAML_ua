import unittest
from unittest.mock import patch, MagicMock

import spacy

from flaskr.service.lemma import _replace_word, _replace_words, Lemmatizer


class TestTextReplacementFunctions(unittest.TestCase):
    def test_replace_word_basic(self):
        text = "Hello world, hello universe"
        replaced_text = _replace_word(text, "hello", "hi")
        self.assertEqual("Hello world, hi universe", replaced_text)

    def test_replace_word_case_sensitive(self):
        text = "Hello world, hello universe"
        replaced_text = _replace_word(text, "HELLO", "hi")
        self.assertEqual("Hello world, hello universe", replaced_text)

    def test_replace_word_no_match(self):
        text = "Hello world, hello universe"
        replaced_text = _replace_word(text, "bye", "hi")
        self.assertEqual(text, replaced_text)

    def test_replace_words_empty_list(self):
        text = "Hello world"
        replaced_text = _replace_words(text, [])
        self.assertEqual(text, replaced_text)


class TestLemmatizer(unittest.TestCase):
    def setUp(self):
        self.mock_nlp = MagicMock(spec=spacy.Language)
        self.lemmatizer = Lemmatizer(self.mock_nlp)

    @patch('flaskr.service.lemma._replace_words')
    def test_replace_named_entities_no_entities(self, mock_replace_words):
        mock_doc = MagicMock()
        mock_doc.ents = []
        self.mock_nlp.return_value = mock_doc

        result = self.lemmatizer.replace_named_entities("Hello world")
        mock_replace_words.assert_not_called()
        self.assertEqual("Hello world", result)

    def test_process_lemmas_excluded_pos(self):
        mock_doc = MagicMock()
        mock_token = MagicMock(text="and", lemma_="and", pos_="CONJ")
        mock_doc.__iter__.return_value = iter([mock_token])
        self.mock_nlp.return_value = mock_doc

        result = self.lemmatizer.process_lemmas("and then")
        self.assertEqual("", result)

    def test_process_lemmas_stop_words(self):
        mock_doc = MagicMock()
        mock_token = MagicMock(text="word", lemma_="word", pos_="NOUN")
        mock_doc.__iter__.return_value = iter([mock_token])
        self.mock_nlp.return_value = mock_doc

        result = self.lemmatizer.process_lemmas("word")
        self.assertEqual("word", result)


if __name__ == '__main__':
    unittest.main()

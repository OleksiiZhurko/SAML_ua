import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from flaskr.service.cleaner import Cleaner
from flaskr.service.lemma import Lemmatizer


class TestCleaner(TestCase):
    def setUp(self):
        self.lemmatizer = MagicMock(spec=Lemmatizer)
        self.cleaner = Cleaner(self.lemmatizer)

    @patch('flaskr.service.cleaner.align_symbols')
    @patch('flaskr.service.cleaner.clean_unused_symbols')
    def test_clean_multiple_rows(self, mock_clean_unused_symbols, mock_align_symbols):
        input_rows = ["First example", "Second example"]

        mock_align_symbols.side_effect = lambda x: x + " 1"
        self.lemmatizer.replace_named_entities.side_effect = lambda x: x + "2"
        self.lemmatizer.process_lemmas.side_effect = lambda x: x + "3"
        mock_clean_unused_symbols.side_effect = lambda x: x + "4"

        expected = [
            {'text': 'First example', 'processed': 'First example 1234'},
            {'text': 'Second example', 'processed': 'Second example 1234'}
        ]

        result = self.cleaner.clean(input_rows)
        self.assertEqual(expected, result)

        mock_align_symbols.assert_has_calls([call("First example"), call("Second example")])
        self.lemmatizer.replace_named_entities.assert_has_calls(
            [call("First example 1"), call("Second example 1")])
        self.lemmatizer.process_lemmas.assert_has_calls(
            [call("First example 12"), call("Second example 12")])
        mock_clean_unused_symbols.assert_has_calls(
            [call("First example 123"), call("Second example 123")])

    def test_empty_input(self):
        result = self.cleaner.clean([])
        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, mock_open

from flaskr.service.verifier import _read_files_in_directory, ModelTextVerifier


class TestFileReading(unittest.TestCase):
    @patch('flaskr.service.verifier.os.path.exists')
    @patch('flaskr.service.verifier.os.makedirs')
    @patch('flaskr.service.verifier.os.listdir')
    @patch('flaskr.service.verifier.os.path.isfile')
    @patch('builtins.open', new_callable=mock_open, read_data='word1\nword2\n')
    def test_read_files_in_directory(self, mock_file, mock_isfile, mock_listdir, mock_makedirs,
                                     mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        mock_isfile.side_effect = lambda x: True

        result = _read_files_in_directory()
        self.assertEqual(['word1', 'word2', 'word1', 'word2'], result)
        # mock_file.assert_called_with('resources/file1.txt', 'r', encoding='utf-8')

    @patch('flaskr.service.verifier.os.path.exists')
    @patch('flaskr.service.verifier.os.makedirs')
    @patch('flaskr.service.verifier.os.listdir')
    def test_create_directory_when_absent(self, mock_listdir, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        mock_listdir.return_value = ['file.txt']
        _read_files_in_directory()
        mock_makedirs.assert_called_once_with('resources')


class TestModelTextVerifier(unittest.TestCase):
    @patch('flaskr.service.verifier._read_files_in_directory')
    def test_initialization_reads_files(self, mock_read_files):
        mock_read_files.return_value = ['word1', 'word2']
        verifier = ModelTextVerifier()
        self.assertEqual(['word1', 'word2'], verifier._words)

    @patch('flaskr.service.verifier._read_files_in_directory', return_value=['word1', 'word2'])
    def test_verify_method_check_false(self, mock_read_files):
        verifier = ModelTextVerifier()
        response = [{'text': 'test text', 'processed': 'word1 word3'}]
        actual = verifier.verify(response, check=False)
        for entity in actual:
            self.assertIsNone(entity['missingLemmas'])
            self.assertIsNone(entity['isInModel'])

    @patch('flaskr.service.verifier._read_files_in_directory', return_value=['word1', 'word2'])
    def test_verify_method_check_true(self, mock_read_files):
        verifier = ModelTextVerifier()
        response = [{'text': 'test text', 'processed': 'word1 word3'}]
        actual = verifier.verify(response, check=True)
        self.assertIn('missingLemmas', actual[0])
        self.assertIn('isInModel', actual[0])
        self.assertEqual('word3', actual[0]['missingLemmas'])
        self.assertFalse(actual[0]['isInModel'])


if __name__ == '__main__':
    unittest.main()

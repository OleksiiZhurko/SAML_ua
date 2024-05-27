import unittest

from flaskr.utils.pattern import align_symbols, clean_unused_symbols


class TestTextProcessing(unittest.TestCase):

    def test_align_symbols(self):
        test_cases = [
            ("“Hello”", '"Hello"'),
            ("‘Good‘ Morning", "'Good' Morning"),
            ("Text with «quotes» and „quotes“", 'Text with "quotes" and "quotes"')
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(expected, align_symbols(input_text))

    def test_clean_unused_symbols(self):
        test_cases = [
            ("This is an email: example@example.com", "this is an email"),
            ("Visit http://example.com now!", "visit now"),
            ("Call me at +1234567890", "call me at"),
            ("My twitter @handle", "my twitter"),
            ("Use #hashtag", "use"),
            ("New\tline and spaces", "new line and spaces"),
            ("Unusual      spaces", "unusual spaces"),
            ("Contain's apostrophes", "contains apostrophes"),
            ("Non-English ЯБГД character", "nonenglish ябгд character")
        ]

        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(expected, clean_unused_symbols(input_text))


if __name__ == '__main__':
    unittest.main()

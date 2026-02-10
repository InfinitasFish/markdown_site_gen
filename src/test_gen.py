import unittest
from gen import extract_title


class TestHtmlGen(unittest.TestCase):
    def test_title_extraction(self):
        text = '##hiii\n\n# hello'
        real_title = extract_title(text)
        expected_title = 'hello'
        self.assertEqual(expected_title, real_title)
    
    def test_title_extraction_another(self):
        text = '##hiii\n\n#\n\nparagraph#\n\n#hello'
        real_title = extract_title(text)
        expected_title = 'hello'
        self.assertEqual(expected_title, real_title)

    def test_generate_page(self):
        pass


import unittest
from generate_page_functions import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        result = extract_title("# Hello!")
        expected = "Hello!"
        self.assertEqual(result, expected)
    


if __name__ == "__main__":
    unittest.main()

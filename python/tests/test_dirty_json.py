import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJson(unittest.TestCase):
    def test_multiline_string(self):
        # The parser used to strip the result, but now it preserves whitespace.
        json_str = '"""line1\nline2"""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "line1\nline2")

    def test_multiline_string_preserves_whitespace(self):
        json_str = '"""  line1\nline2  """'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "  line1\nline2  ")

    def test_multiline_string_with_quotes(self):
        json_str = '"""He said "hello"."""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, 'He said "hello".')

    def test_multiline_string_empty(self):
        json_str = '""""""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "")

    def test_multiline_string_single_quote(self):
        json_str = "'''line1\nline2'''"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "line1\nline2")

    def test_multiline_string_backticks(self):
        json_str = "```line1\nline2```"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "line1\nline2")

if __name__ == '__main__':
    unittest.main()

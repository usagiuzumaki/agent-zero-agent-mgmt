import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJson(unittest.TestCase):
    def test_multiline_string(self):
        # The parser strips the result, so "line1\nline2" might become "line1\nline2"
        json_str = '"""line1\nline2"""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "line1\nline2")

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

    def test_string_escapes(self):
        json_str = '"Line 1\\nLine 2\\tTabbed\\""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, 'Line 1\nLine 2\tTabbed"')

    def test_long_string_correctness(self):
        # A test that ensures the optimized parser handles long strings correctly
        segment = "abc" * 1000
        json_str = f'"{segment}"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, segment)

if __name__ == '__main__':
    unittest.main()

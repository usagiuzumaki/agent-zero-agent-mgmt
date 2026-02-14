import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJsonExtended(unittest.TestCase):
    def test_simple_string(self):
        json_str = '"hello world"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "hello world")

    def test_escapes(self):
        json_str = '"line1\\nline2\\tline3\\r\\b\\f\\\"\\\\"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        expected = 'line1\nline2\tline3\r\b\f"\\'
        self.assertEqual(result, expected)

    def test_unicode(self):
        json_str = '"\\u0041\\u0042\\u0043"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "ABC")

    def test_invalid_unicode(self):
        json_str = '"\\u004X"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "\\u004X")

    def test_mixed_content(self):
        # A mix of long text and escapes to trigger both paths
        long_part = "a" * 1000
        json_str = f'"{long_part}\\n{long_part}"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, f"{long_part}\n{long_part}")

    def test_unknown_escape(self):
        # Current behavior: ignores backslash before unknown char, consumes char.
        # \z -> "" (consumes z, returns nothing) based on my analysis of previous code.
        # Wait, previous code:
        # if not in list: do nothing (result.append skipped).
        # self._advance() (skip z).
        # result: empty string.
        json_str = '"\\z"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "")

    def test_incomplete_escape(self):
        # "foo\" at end of string
        # The parser sees \" as an escaped quote, so it appends " to the result.
        # Since EOF is reached, it terminates.
        json_str = '"foo\\"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, 'foo"')

if __name__ == '__main__':
    unittest.main()


import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJsonStrings(unittest.TestCase):
    def test_simple_string(self):
        json_str = '"hello world"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "hello world")

    def test_string_with_escapes(self):
        json_str = '"Line1\\nLine2\\tTabbed"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "Line1\nLine2\tTabbed")

    def test_string_with_quotes(self):
        json_str = '"He said \\"Hello\\""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, 'He said "Hello"')

    def test_unicode_escape(self):
        json_str = '"\\u00A9 Copyright"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "\u00A9 Copyright")

    def test_unicode_literal(self):
        json_str = '"Emoji 🚀"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "Emoji 🚀")

    def test_complex_nested_structure(self):
        json_str = '{"key": "value", "list": ["item1", "item2"]}'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, {"key": "value", "list": ["item1", "item2"]})

    def test_unquoted_string(self):
        # DirtyJson supports unquoted strings in some contexts, but let's test quoted mainly
        # This test ensures we don't break fallback or other logic
        json_str = '{key: value}'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, {"key": "value"})

    def test_long_string_performance_check(self):
        # Correctness check for long string
        long_str = "a" * 1000
        json_str = f'"{long_str}"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, long_str)

    def test_invalid_escape(self):
        # \z is invalid escape. Legacy behavior is to ignore/swallow the character.
        json_str = '"abc\\zdef"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "abcdef")

if __name__ == '__main__':
    unittest.main()

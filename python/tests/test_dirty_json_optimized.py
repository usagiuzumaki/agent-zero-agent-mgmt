import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJsonOptimized(unittest.TestCase):
    def test_simple_string(self):
        json_str = '"hello world"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "hello world")

    def test_escapes(self):
        # Test standard escapes
        json_str = r'"Line1\nLine2\tTab\rReturn\bBack\fForm\"Quote\\Slash"'
        expected = "Line1\nLine2\tTab\rReturn\bBack\fForm\"Quote\\Slash"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, expected)

    def test_unicode_escapes(self):
        # Test unicode escapes
        json_str = r'"\u0041\u0042\u0043"' # ABC
        expected = "ABC"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, expected)

    def test_unicode_escapes_mixed(self):
        json_str = r'"Hello \u0041 world"'
        expected = "Hello A world"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, expected)

    def test_invalid_unicode(self):
        # Test invalid unicode escapes - legacy behavior preserves them as literal text
        json_str = r'"\u004X"'
        expected = r"\u004X"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, expected)

    def test_partial_unicode(self):
         # Test truncated unicode escapes
        json_str = r'"\u004"'
        expected = r"\u004"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, expected)

    def test_unrecognized_escape(self):
        # Test unrecognized escape sequence - legacy behavior ignores the backslash?
        # Based on my code reading:
        # \z -> advance -> z not in list -> no append -> advance -> next char
        # So \z should become nothing if 'z' is skipped.
        # Wait, let's verify what my implementation does.
        # If I have r'"\z"', `\` is found. `_advance()` -> `z`.
        # `z` is not in list. `z` != `u`.
        # `_advance()` -> char after `z`.
        # So `z` IS skipped. result should be empty string for `\z`.

        # Let's verify what `test_dirty_json.py` behavior implies or just test what happens.
        json_str = r'"a\zb"'
        # expected: "ab" ?
        parser = DirtyJson()
        result = parser.parse(json_str)
        # I'll assert what it IS, to confirm behavior.
        self.assertEqual(result, "ab")

    def test_mixed_content(self):
        # Mix of fast path and slow path
        json_str = r'"Start of string \n escaped \u0041 end of string"'
        expected = "Start of string \n escaped A end of string"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, expected)

    def test_single_quotes(self):
        json_str = "'hello world'"
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "hello world")

    def test_empty_string(self):
        json_str = '""'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, "")

    def test_no_escapes_long(self):
        # Long string with no escapes (trigger fast path)
        s = "a" * 1000
        json_str = f'"{s}"'
        parser = DirtyJson()
        result = parser.parse(json_str)
        self.assertEqual(result, s)

if __name__ == '__main__':
    unittest.main()

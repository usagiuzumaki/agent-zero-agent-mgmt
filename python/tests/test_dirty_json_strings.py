import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJsonStrings(unittest.TestCase):
    def setUp(self):
        self.parser = DirtyJson()

    def test_simple_string(self):
        json_str = '"hello world"'
        result = self.parser.parse(json_str)
        self.assertEqual(result, "hello world")

    def test_escaped_quotes(self):
        json_str = '"He said \\"hello\\""'
        result = self.parser.parse(json_str)
        self.assertEqual(result, 'He said "hello"')

    def test_backslashes(self):
        json_str = '"C:\\\\path\\\\to\\\\file"'
        result = self.parser.parse(json_str)
        self.assertEqual(result, 'C:\\path\\to\\file')

    def test_unicode(self):
        json_str = '"\\u0041\\u0042\\u0043"'
        result = self.parser.parse(json_str)
        self.assertEqual(result, "ABC")

    def test_standard_escapes(self):
        json_str = '"Line1\\nLine2\\tTabbed"'
        result = self.parser.parse(json_str)
        self.assertEqual(result, "Line1\nLine2\tTabbed")

    def test_mixed_content(self):
        json_str = '"Start \\"quote\\" end"'
        result = self.parser.parse(json_str)
        self.assertEqual(result, 'Start "quote" end')

    def test_empty_string(self):
        json_str = '""'
        result = self.parser.parse(json_str)
        self.assertEqual(result, "")

    def test_single_quotes(self):
        json_str = "'hello world'"
        result = self.parser.parse(json_str)
        self.assertEqual(result, "hello world")

    def test_invalid_unicode(self):
        # Should handle gracefully, typically by keeping literal
        json_str = '"\\uXYZ"'
        result = self.parser.parse(json_str)
        # The parser implementation appends "\\u" + chars if valid hex not found
        # It consumes 4 chars if possible, or stops if not alphanumeric.
        # X is alphanumeric, Y is alphanumeric, Z is alphanumeric.
        # So it might try to parse XYZ + next char.
        # Let's adjust expectation based on implementation:
        # It tries to collect 4 hex digits. If loop finishes (4 chars collected), it tries int(..., 16).
        # If ValueError, it appends "\\u" + chars.
        # If loop breaks early (non-alnum), it appends "\\u" + chars.

        # Test 1: Short invalid
        # "\uXYZ" -> tries to read X, Y, Z, quote. quote is not alnum (wait, quote is not alnum).
        # So it breaks loop. Result: "\\uXYZ"

        # But wait, logic is:
        # for _ in range(4):
        #    if not alnum: break

        # If json_str is '"\uXYZ"' -> \u is consumed. current is X.
        # X is alnum. unicode_char="X". advance.
        # Y is alnum. unicode_char="XY". advance.
        # Z is alnum. unicode_char="XYZ". advance.
        # " is NOT alnum. Break.
        # result.append("\\u" + "XYZ")

        self.assertEqual(result, "\\uXYZ")

    def test_invalid_unicode_full_length(self):
        # "\uZZZZ" -> 4 chars, Z is alnum.
        # int("ZZZZ", 16) raises ValueError.
        # result.append("\\uZZZZ")
        json_str = '"\\uZZZZ"'
        result = self.parser.parse(json_str)
        self.assertEqual(result, "\\uZZZZ")

if __name__ == '__main__':
    unittest.main()

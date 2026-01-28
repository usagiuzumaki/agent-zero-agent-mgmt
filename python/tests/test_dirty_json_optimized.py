import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJsonOptimized(unittest.TestCase):
    def setUp(self):
        self.parser = DirtyJson()

    def parse_string_only(self, s):
        # Helper to parse a JSON string literal
        return self.parser.parse(s)

    def test_simple_string(self):
        self.assertEqual(self.parse_string_only('"hello"'), "hello")
        self.assertEqual(self.parse_string_only("'hello'"), "hello")

    def test_empty_string(self):
        self.assertEqual(self.parse_string_only('""'), "")
        self.assertEqual(self.parse_string_only("''"), "")

    def test_escaped_quotes(self):
        self.assertEqual(self.parse_string_only(r'"He said \"hello\""'), 'He said "hello"')
        self.assertEqual(self.parse_string_only(r"'It\'s me'"), "It's me")

    def test_common_escapes(self):
        self.assertEqual(self.parse_string_only(r'"\n\t\r\b\f\\\/ "'), "\n\t\r\b\f\\/ ")

    def test_unicode_escapes(self):
        self.assertEqual(self.parse_string_only(r'"\u0041"'), "A")
        self.assertEqual(self.parse_string_only(r'"\u00A9"'), "©")
        self.assertEqual(self.parse_string_only(r'"\u2603"'), "☃")

    def test_broken_unicode_escapes(self):
        # Fallback behavior as per original implementation
        self.assertEqual(self.parse_string_only(r'"\u12"'), r"\u12")
        self.assertEqual(self.parse_string_only(r'"\uXYZ"'), r"\uXYZ")

    def test_mixed_content(self):
        s = r'"Start \u0041 \n End"'
        self.assertEqual(self.parse_string_only(s), "Start A \n End")

    def test_unterminated_string(self):
        # Should probably return what it found or handle it gracefully
        # Original implementation behavior: returns what it collected so far if loop finishes
        # But wait, existing code: while current is not None... if None, loop ends.
        # Then check if current == quote. If not, it just returns result joined.
        self.assertEqual(self.parse_string_only('"unterminated'), "unterminated")

if __name__ == '__main__':
    unittest.main()

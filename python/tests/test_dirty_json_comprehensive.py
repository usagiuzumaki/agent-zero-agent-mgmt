import unittest
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.getcwd(), 'python'))
from helpers.dirty_json import DirtyJson

class TestDirtyJsonComprehensive(unittest.TestCase):
    def setUp(self):
        self.parser = DirtyJson()

    def parse(self, json_str):
        return self.parser.parse(json_str)

    def test_standard_types(self):
        self.assertEqual(self.parse('{"a": 1}'), {"a": 1})
        self.assertEqual(self.parse('["a", 1, true, null]'), ["a", 1, True, None])
        self.assertEqual(self.parse('123'), 123)
        self.assertEqual(self.parse('-12.34'), -12.34)
        self.assertEqual(self.parse('true'), True)
        self.assertEqual(self.parse('false'), False)
        self.assertEqual(self.parse('null'), None)

    def test_comments(self):
        self.assertEqual(self.parse('{"a": 1} // comment'), {"a": 1})
        self.assertEqual(self.parse('{"a": 1, // comment\n "b": 2}'), {"a": 1, "b": 2})
        self.assertEqual(self.parse('{"a": /* comment */ 1}'), {"a": 1})
        self.assertEqual(self.parse('/* start */ {"a": 1} /* end */'), {"a": 1})

    def test_trailing_commas(self):
        self.assertEqual(self.parse('[1, 2, ]'), [1, 2])
        self.assertEqual(self.parse('{"a": 1, "b": 2, }'), {"a": 1, "b": 2})

    def test_unquoted_keys(self):
        self.assertEqual(self.parse('{a: 1, b: 2}'), {"a": 1, "b": 2})
        self.assertEqual(self.parse('{$key: 1}'), {"$key": 1})
        self.assertEqual(self.parse('{key_name: 1}'), {"key_name": 1})

    def test_single_quotes(self):
        self.assertEqual(self.parse("{'a': 'value'}"), {"a": "value"})
        self.assertEqual(self.parse("['a', 'b']"), ["a", "b"])

    def test_nested_structures(self):
        json_str = """
        {
            key: {
                nested: [1, 2, {deep: 'value'}]
            }
        }
        """
        expected = {"key": {"nested": [1, 2, {"deep": "value"}]}}
        self.assertEqual(self.parse(json_str), expected)

    def test_dirty_wrappers(self):
        self.assertEqual(self.parse('Here is JSON: {"a": 1} ... end'), {"a": 1})
        self.assertEqual(self.parse('```json\n{"a": 1}\n```'), {"a": 1})

    def test_unicode_escapes(self):
        self.assertEqual(self.parse('{"a": "\\u0041"}'), {"a": "A"})
        # Graceful degradation
        self.assertEqual(self.parse('{"a": "\\u004z"}'), {"a": "\\u004z"})

    def test_urls_unquoted(self):
        # This currently fails or produces truncated result.
        # Goal: support unquoted URLs
        self.assertEqual(self.parse('{"url": http://example.com}'), {"url": "http://example.com"})
        self.assertEqual(self.parse('{"url": https://example.com/path?q=1}'), {"url": "https://example.com/path?q=1"})

    def test_delimiter_consumption_bug(self):
        # Current bug: unquoted string consumes delimiter
        # Input: {"a": unquoted} {"b": 2}
        # If 'unquoted' consumes '}', the parser might fail to stop or parse next object correctly if streamed?
        # DirtyJson.parse_string only parses first object.

        # However, checking if '}' is correctly handled:
        # If '}' is consumed, the parser effectively finishes the object.
        # But if we have {"a": unquoted, "b": 2}
        # It consumes ',' and thinks it's end of value.
        # Then next char is '"'.
        # It expects ',' or '}'. Neither match.
        # It loops. Parses '"b"' as key.
        # So it works by accident due to loose parsing.

        # But let's verify exact behavior for multiple unquoted values
        self.assertEqual(self.parse('{a: val1, b: val2}'), {"a": "val1", "b": "val2"})

        # Test case where consuming delimiter is bad:
        # Nested object with unquoted string at end
        self.assertEqual(self.parse('{a: {b: val}, c: 2}'), {"a": {"b": "val"}, "c": 2})

if __name__ == '__main__':
    unittest.main()

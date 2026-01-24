import unittest
from python.helpers.dirty_json import DirtyJson

class TestDirtyJson(unittest.TestCase):
    def test_standard_json(self):
        json_str = '{"key": "value", "num": 123, "bool": true, "null": null}'
        expected = {"key": "value", "num": 123, "bool": True, "null": None}
        self.assertEqual(DirtyJson.parse_string(json_str), expected)

    def test_multiline_string(self):
        json_str = '''{
            "key": """line1
line2"""
        }'''
        expected = {"key": "line1\nline2"}
        self.assertEqual(DirtyJson.parse_string(json_str), expected)

    def test_dirty_json_comments(self):
        json_str = '''{
            "key": "value", // comment
            /* multi
               line */
            "key2": "value2"
        }'''
        expected = {"key": "value", "key2": "value2"}
        self.assertEqual(DirtyJson.parse_string(json_str), expected)

    def test_nested_structures(self):
        json_str = '{"a": [1, {"b": 2}]}'
        expected = {"a": [1, {"b": 2}]}
        self.assertEqual(DirtyJson.parse_string(json_str), expected)

    def test_dirty_start(self):
        json_str = 'garbage text {"key": "value"} garbage'
        expected = {"key": "value"}
        self.assertEqual(DirtyJson.parse_string(json_str), expected)

if __name__ == '__main__':
    unittest.main()

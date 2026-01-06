import unittest
from python.helpers.memory import Memory

class TestMemoryComparator(unittest.TestCase):
    def test_comparator_basic(self):
        condition = "x > 10"
        comparator = Memory._get_comparator(condition)
        self.assertTrue(comparator({"x": 11}))
        self.assertFalse(comparator({"x": 10}))
        self.assertFalse(comparator({"x": 9}))

    def test_comparator_string(self):
        condition = "name == 'Alice'"
        comparator = Memory._get_comparator(condition)
        self.assertTrue(comparator({"name": "Alice"}))
        self.assertFalse(comparator({"name": "Bob"}))

    def test_comparator_compound(self):
        condition = "x > 10 and y < 5"
        comparator = Memory._get_comparator(condition)
        self.assertTrue(comparator({"x": 11, "y": 4}))
        self.assertFalse(comparator({"x": 11, "y": 5}))
        self.assertFalse(comparator({"x": 10, "y": 4}))

    def test_comparator_invalid_syntax(self):
        # Should handle invalid syntax gracefully
        condition = "x > " # Invalid
        comparator = Memory._get_comparator(condition)
        # Should return a function that returns False safely
        self.assertFalse(comparator({"x": 10}))

    def test_comparator_runtime_error(self):
        # Should handle runtime errors during evaluation
        condition = "x > 10"
        comparator = Memory._get_comparator(condition)
        # Missing key 'x'
        self.assertFalse(comparator({"y": 10}))

if __name__ == '__main__':
    unittest.main()

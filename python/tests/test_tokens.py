import unittest
from python.helpers.tokens import approximate_tokens, count_tokens

class TestTokens(unittest.TestCase):
    def test_approximate_tokens_short(self):
        # Very short string
        s = "Hello"
        tokens = approximate_tokens(s)
        self.assertGreater(tokens, 0)

        # Medium short string (< 100 chars)
        s2 = "The quick brown fox jumps over the lazy dog."
        tokens2 = approximate_tokens(s2)
        self.assertGreater(tokens2, 0)
        # We expect it to be roughly len // 3 or count_tokens * 1.1
        # Currently it is count_tokens * 1.1
        # count_tokens("The quick brown fox jumps over the lazy dog.") is 10.
        # So expected is 11.

    def test_approximate_tokens_long(self):
        # Long string (> 100 chars)
        s = "word " * 50  # 250 chars
        tokens = approximate_tokens(s)
        self.assertGreater(tokens, 0)

    def test_approximate_tokens_heuristic_comparison(self):
        # This test documents the behavior.
        # Once we switch to heuristic, the values might change slightly.
        text = "Hello world"
        # count is 2. approx (current) is int(2 * 1.1) = 2.
        # heuristic (new) will be max(1, 11 // 3) = 3.

        val = approximate_tokens(text)
        self.assertTrue(isinstance(val, int))

    def test_empty(self):
        self.assertEqual(approximate_tokens(""), 0)

if __name__ == '__main__':
    unittest.main()

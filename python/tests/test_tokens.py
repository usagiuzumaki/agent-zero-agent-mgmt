import unittest
from python.helpers import tokens

class TestTokens(unittest.TestCase):
    def test_approximate_tokens_empty(self):
        self.assertEqual(tokens.approximate_tokens(""), 0)

    def test_approximate_tokens_short(self):
        # Short strings use heuristic
        # Heuristic: max(1, len // 3)
        self.assertEqual(tokens.approximate_tokens("a"), 1)
        self.assertEqual(tokens.approximate_tokens("hello"), 1) # 5 chars / 3 = 1
        self.assertEqual(tokens.approximate_tokens("hello world"), 3) # 11 chars / 3 = 3
        self.assertEqual(tokens.approximate_tokens("Message"), 2) # 7 chars / 3 = 2

    def test_approximate_tokens_long(self):
        # Long strings (>100 chars) use tiktoken
        long_text = "a" * 200
        # tiktoken("a"*200) -> 200 tokens?
        # count_tokens("a"*200) -> 200 (if 'a' is a token)

        count = tokens.count_tokens(long_text)
        approx = tokens.approximate_tokens(long_text)

        # Should use BUFFER logic: count * APPROX_BUFFER
        expected = int(count * tokens.APPROX_BUFFER)
        self.assertEqual(approx, expected)

if __name__ == "__main__":
    unittest.main()

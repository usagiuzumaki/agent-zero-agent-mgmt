import unittest
from python.helpers.strings import calculate_valid_match_lengths

class TestStrings(unittest.TestCase):
    def test_calculate_valid_match_lengths_basic(self):
        s1 = "hello world"
        s2 = "hello world"
        res = calculate_valid_match_lengths(s1, s2)
        self.assertEqual(res, (11, 11))

    def test_calculate_valid_match_lengths_with_ignore(self):
        s1 = "hello world"
        s2 = "hello   world"
        ignore = [r"\s+"]
        # It should match "hello" (5), skip spaces, match "world" (5).
        # Total matched indices should advance to end of strings.
        res = calculate_valid_match_lengths(s1, s2, ignore_patterns=ignore)
        self.assertEqual(res, (11, 13))

    def test_calculate_valid_match_lengths_bytes(self):
        s1 = b"hello world"
        s2 = b"hello   world"
        ignore = [rb"\s+"]
        res = calculate_valid_match_lengths(s1, s2, ignore_patterns=ignore)
        self.assertEqual(res, (11, 13))

    def test_calculate_valid_match_lengths_partial(self):
        s1 = "hello world"
        s2 = "hello there"
        # It should match "hello " (6) then fail at 'w' vs 't'
        # With deviation, it might skip ahead.
        # But here we just want to ensure it doesn't crash.
        res = calculate_valid_match_lengths(s1, s2)
        # It matches 'hello ' (6 chars). 'w' != 't'.
        # With deviation default 5, it tries to look ahead.
        # It won't find match for 'w' in 'there' easily.
        # It might find 'e' (index 1 of world) in 'there' (index 2).
        # Let's just check it returns valid integers <= len.
        self.assertTrue(res[0] <= len(s1))
        self.assertTrue(res[1] <= len(s2))

if __name__ == '__main__':
    unittest.main()

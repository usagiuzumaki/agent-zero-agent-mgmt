import unittest
from python.helpers.strings import calculate_valid_match_lengths

class TestStrings(unittest.TestCase):
    def test_calculate_valid_match_lengths_basic(self):
        i, j = calculate_valid_match_lengths("abcdef", "abcdef")
        self.assertEqual(i, 6)
        self.assertEqual(j, 6)

        i, j = calculate_valid_match_lengths("abc", "def")
        self.assertEqual(i, 0)
        self.assertEqual(j, 0)

    def test_calculate_valid_match_lengths_ignore(self):
        # Case 1: Ignored pattern at start
        i, j = calculate_valid_match_lengths("ignoreme", "ignoreme", ignore_patterns=["ignore"])
        self.assertEqual(i, 8)
        self.assertEqual(j, 8)

        # Case 2: Ignored pattern in middle
        i, j = calculate_valid_match_lengths("abcignoredef", "abcignoredef", ignore_patterns=["ignore"])
        self.assertEqual(i, 12)
        self.assertEqual(j, 12)

        # Case 3: Ignored pattern at end
        # Note: logic loops while i < len(first). If skip pushes i past end, loop terminates.
        # But last_matched is only updated when char match occurs.
        # Wait, if we skip "ignore", we don't increment matched count explicitly?
        # In original code:
        # i matches j. matched_since_deviation increments.
        # If we skip, we just move i and j. We don't verify characters match (because they are ignored).
        # And we don't update last_matched_i/j until we find a real match AFTER skipping?
        # Let's check original behavior.

        # "abcignore" vs "abcignore"
        # i=0..3 matches "abc". last_matched = 3.
        # i=3 skip "ignore" -> i=9.
        # Loop ends. Returns 3.
        i, j = calculate_valid_match_lengths("abcignore", "abcignore", ignore_patterns=["ignore"])
        self.assertEqual(i, 3)
        self.assertEqual(j, 3)

    def test_calculate_valid_match_lengths_bytes(self):
        i, j = calculate_valid_match_lengths(b"abcignoredef", b"abcignoredef", ignore_patterns=[b"ignore"])
        self.assertEqual(i, 12)
        self.assertEqual(j, 12)

    def test_calculate_valid_match_lengths_mismatch(self):
        # Test with deviation
        i, j = calculate_valid_match_lengths("abcXdef", "abcYdef", deviation_threshold=2)
        # abc matches. i=3, j=3.
        # X!=Y. deviations=1. i=4, j=4.
        # d==d. match.
        # e==e. match.
        # f==f. match.
        # Returns 7, 7.
        self.assertEqual(i, 7)
        self.assertEqual(j, 7)

if __name__ == '__main__':
    unittest.main()

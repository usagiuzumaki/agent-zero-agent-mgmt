import time
import re
import unittest
from python.helpers.strings import calculate_valid_match_lengths
from python.helpers.shell_ssh import SSHInteractiveSession

class TestSSHOptimization(unittest.TestCase):
    def test_calculate_valid_match_lengths_mixed_inputs(self):
        """Verify calculate_valid_match_lengths works with both bytes and compiled patterns"""
        command = b"echo 'hello'"
        output = b"echo 'hello'\r\nhello\r\nCLI> "

        # Original style (bytes)
        ignore_patterns_bytes = [
            rb"\x1b\[\?\d{4}[a-zA-Z](?:> )?",
            rb"\r",
            rb">\s",
        ]

        # New style (compiled)
        ignore_patterns_compiled = SSHInteractiveSession.IGNORE_PATTERNS

        res_bytes = calculate_valid_match_lengths(
            command, output, ignore_patterns=ignore_patterns_bytes
        )

        res_compiled = calculate_valid_match_lengths(
            command, output, ignore_patterns=ignore_patterns_compiled
        )

        self.assertEqual(res_bytes, res_compiled, "Results should be identical regardless of pattern type")

    def test_performance_improvement(self):
        """Verify that passing compiled patterns + isinstance check is efficient"""
        command = b"echo 'hello'"
        output = b"echo 'hello'\r\nhello\r\nCLI> "
        ignore_patterns_compiled = SSHInteractiveSession.IGNORE_PATTERNS

        iterations = 10000

        start = time.time()
        for _ in range(iterations):
            calculate_valid_match_lengths(
                command, output, ignore_patterns=ignore_patterns_compiled
            )
        end = time.time()
        duration = end - start
        print(f"\nPerformance (10k iterations): {duration:.4f}s")

        # Just ensure it's reasonable (under 1s for 10k simple calls)
        # This is not a strict performance regression test, but a sanity check
        self.assertLess(duration, 1.0)

    def test_clean_string_patterns(self):
        """Verify clean_string regex works as expected"""
        # Mocking the session object just to access clean_string
        class MockSession(SSHInteractiveSession):
            def __init__(self):
                pass

        session = MockSession()

        input_str = "Hello \x1b[31mWorld\x1b[0m"
        cleaned = session.clean_string(input_str)
        self.assertEqual(cleaned, "Hello World")

if __name__ == "__main__":
    unittest.main()

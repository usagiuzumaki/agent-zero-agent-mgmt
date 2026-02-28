import unittest
import os
from python.helpers.safe_mode import is_safe_mode

class TestSafeMode(unittest.TestCase):
    def test_safe_mode_enabled(self):
        os.environ["OPERATIONAL_SAFE_MODE"] = "true"
        self.assertTrue(is_safe_mode())

    def test_safe_mode_disabled(self):
        os.environ["OPERATIONAL_SAFE_MODE"] = "false"
        self.assertFalse(is_safe_mode())

    def test_safe_mode_default(self):
        if "OPERATIONAL_SAFE_MODE" in os.environ:
            del os.environ["OPERATIONAL_SAFE_MODE"]
        self.assertFalse(is_safe_mode())

if __name__ == "__main__":
    unittest.main()

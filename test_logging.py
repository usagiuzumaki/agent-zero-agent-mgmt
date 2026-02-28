import unittest
import json
import io
import logging
from python.helpers.logger import setup_logger, JsonFormatter

class TestLogging(unittest.TestCase):
    def test_json_formatter(self):
        log_output = io.StringIO()
        handler = logging.StreamHandler(log_output)
        handler.setFormatter(JsonFormatter())

        logger = logging.getLogger("test_json")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        logger.info("Test message")

        output = log_output.getvalue().strip()
        log_json = json.loads(output)

        self.assertEqual(log_json["message"], "Test message")
        self.assertEqual(log_json["level"], "INFO")
        self.assertIn("timestamp", log_json)

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Mocking modules that might fail during import
sys.modules['flask_login'] = MagicMock()
sys.modules['flask_sqlalchemy'] = MagicMock()

from python.helpers.ready_check import perform_ready_check

class TestReadyCheck(unittest.TestCase):
    @patch('python.helpers.ready_check.check_db')
    @patch('python.helpers.ready_check.check_config')
    def test_perform_ready_check_success(self, mock_cfg, mock_db):
        mock_db.return_value = (True, "OK")
        mock_cfg.return_value = (True, "OK")

        ok, results = perform_ready_check()
        self.assertTrue(ok)
        self.assertEqual(results['database']['status'], 'ok')
        self.assertEqual(results['config']['status'], 'ok')

    @patch('python.helpers.ready_check.check_db')
    @patch('python.helpers.ready_check.check_config')
    def test_perform_ready_check_failure(self, mock_cfg, mock_db):
        mock_db.return_value = (False, "Error")
        mock_cfg.return_value = (True, "OK")

        ok, results = perform_ready_check()
        self.assertFalse(ok)
        self.assertEqual(results['database']['status'], 'error')

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add repo root to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from python.helpers import settings

class TestSettingsToken(unittest.TestCase):
    def setUp(self):
        # Reset settings global state
        settings._settings = None
        settings._final_settings = None

    @patch('python.helpers.settings.runtime')
    @patch('python.helpers.settings.dotenv')
    @patch('python.helpers.settings.get_providers')
    def test_create_auth_token_with_args(self, mock_get_providers, mock_dotenv, mock_runtime):
        """Test create_auth_token uses arguments when provided."""
        # Setup mocks
        mock_runtime.get_persistent_id.return_value = "test_runtime_id"
        mock_dotenv.get_dotenv_value.return_value = None
        mock_dotenv.KEY_AUTH_LOGIN = "AUTH_LOGIN"
        mock_dotenv.KEY_AUTH_PASSWORD = "AUTH_PASSWORD"

        token = settings.create_auth_token(username="user1", password="pass1")
        # Token should be deterministic based on runtime_id, user, pass
        self.assertTrue(len(token) > 0)

        token2 = settings.create_auth_token(username="user1", password="pass1")
        self.assertEqual(token, token2)

        token3 = settings.create_auth_token(username="user2", password="pass2")
        self.assertNotEqual(token, token3)

    @patch('python.helpers.settings.runtime')
    @patch('python.helpers.settings.dotenv')
    def test_create_auth_token_with_env(self, mock_dotenv, mock_runtime):
        """Test create_auth_token uses env vars when args are missing."""
        # Setup mocks
        mock_runtime.get_persistent_id.return_value = "test_runtime_id"
        mock_dotenv.KEY_AUTH_LOGIN = "AUTH_LOGIN"
        mock_dotenv.KEY_AUTH_PASSWORD = "AUTH_PASSWORD"

        # Configure side effect for dotenv lookup
        mock_dotenv.get_dotenv_value.side_effect = lambda key, default=None: {
            "AUTH_LOGIN": "env_user",
            "AUTH_PASSWORD": "env_pass"
        }.get(key, default)

        token = settings.create_auth_token()
        token_expected = settings.create_auth_token(username="env_user", password="env_pass")
        self.assertEqual(token, token_expected)

    def test_normalize_settings_updates_token(self):
        """Test that normalize_settings calculates the token correctly based on provided settings."""
        # This test doesn't need mocks because it passes username/password explicitly
        # causing create_auth_token to rely only on runtime.get_persistent_id()
        # BUT create_auth_token calls runtime.get_persistent_id() which is real here!
        # If runtime.get_persistent_id() is stable, it's fine.
        # But for consistency, we should mock runtime.

        with patch('python.helpers.settings.runtime') as mock_runtime:
            mock_runtime.get_persistent_id.return_value = "test_runtime_id"

            input_settings = {
                "auth_login": "new_user",
                "auth_password": "new_pass",
            }

            # use_env_auth=False mimics set_settings behavior
            normalized = settings.normalize_settings(input_settings, use_env_auth=False)

            expected_token = settings.create_auth_token(username="new_user", password="new_pass")
            self.assertEqual(normalized["mcp_server_token"], expected_token)

    @patch('python.helpers.settings.create_auth_token')
    def test_normalize_settings_uses_env_by_default(self, mock_create_token):
        """Test that normalize_settings uses env vars (via create_auth_token default) by default."""
        input_settings = {}
        settings.normalize_settings(input_settings, use_env_auth=True)

        # Should call create_auth_token() with no args
        mock_create_token.assert_called()
        args, kwargs = mock_create_token.call_args
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import importlib

# Mock modules that might not be available or side-effect heavy
sys.modules['litellm'] = MagicMock()
sys.modules['models'] = MagicMock()
sys.modules['webcolors'] = MagicMock()
sys.modules['python.helpers.runtime'] = MagicMock()
sys.modules['python.helpers.dotenv'] = MagicMock()
sys.modules['python.helpers.files'] = MagicMock()
sys.modules['python.helpers.git'] = MagicMock()
sys.modules['python.helpers.whisper'] = MagicMock()
sys.modules['python.helpers.defer'] = MagicMock()
sys.modules['python.helpers.providers'] = MagicMock()

# Add repo root to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from python.helpers import settings

class TestSettingsToken(unittest.TestCase):
    def setUp(self):
        # Setup mocks BEFORE reload
        self.dotenv_mock = sys.modules['python.helpers.dotenv']
        self.dotenv_mock.KEY_AUTH_LOGIN = "AUTH_LOGIN"
        self.dotenv_mock.KEY_AUTH_PASSWORD = "AUTH_PASSWORD"

        # Reload settings to ensure we have fresh module state and use mocks
        global settings
        settings = importlib.reload(settings)

        # FORCE override of dotenv in settings to ensure it matches our mock
        # This handles cases where relative imports might resolve differently during test reload
        settings.dotenv = self.dotenv_mock

        # Reset settings global state
        settings._settings = None
        settings._final_settings = None

        self.runtime_mock = sys.modules['python.helpers.runtime']

        # Default mock return values
        self.runtime_mock.get_persistent_id.return_value = "test_runtime_id"
        self.dotenv_mock.get_dotenv_value.return_value = None

        sys.modules['python.helpers.providers'].get_providers.return_value = []

    def test_create_auth_token_with_args(self):
        """Test create_auth_token uses arguments when provided."""
        token = settings.create_auth_token(username="user1", password="pass1")
        # Token should be deterministic based on runtime_id, user, pass
        self.assertTrue(len(token) > 0)

        token2 = settings.create_auth_token(username="user1", password="pass1")
        self.assertEqual(token, token2)

        token3 = settings.create_auth_token(username="user2", password="pass2")
        self.assertNotEqual(token, token3)

    def test_create_auth_token_with_env(self):
        """Test create_auth_token uses env vars when args are missing."""
        def side_effect(key, default=None):
            if str(key) == "AUTH_LOGIN":
                return "env_user"
            if str(key) == "AUTH_PASSWORD":
                return "env_pass"
            return default

        self.dotenv_mock.get_dotenv_value.side_effect = side_effect

        token = settings.create_auth_token()

        token_expected = settings.create_auth_token(username="env_user", password="env_pass")
        self.assertEqual(token, token_expected)

    def test_normalize_settings_updates_token(self):
        """Test that normalize_settings calculates the token correctly based on provided settings."""
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

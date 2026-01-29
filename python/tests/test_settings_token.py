import pytest
from unittest.mock import patch
import sys
import os

# Ensure we can import from python root
sys.path.append(os.getcwd())

from python.helpers.settings import create_auth_token

class TestSettingsToken:

    def test_create_auth_token_with_args(self):
        # Generate tokens with specific credentials
        token1 = create_auth_token(username="user1", password="pass1")
        token2 = create_auth_token(username="user2", password="pass2")

        # Ensure tokens are different for different credentials
        assert token1 != token2

        # Ensure deterministic generation
        token1_again = create_auth_token(username="user1", password="pass1")
        assert token1 == token1_again

    @patch('python.helpers.dotenv.get_dotenv_value')
    def test_create_auth_token_defaults(self, mock_get_dotenv):
        # Mock dotenv values
        mock_get_dotenv.side_effect = lambda key: "env_user" if "LOGIN" in key else "env_pass"

        token = create_auth_token()

        # Should generate token based on mocked env values
        token_manual = create_auth_token(username="env_user", password="env_pass")
        assert token == token_manual

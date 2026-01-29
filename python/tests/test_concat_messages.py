import pytest
from unittest.mock import MagicMock
import sys
import os

# Ensure we can import from python root
sys.path.append(os.getcwd())

from python.helpers.history import History
from agents.agent import Agent

class TestConcatMessages:
    @pytest.fixture
    def mock_agent(self):
        # Mocking Agent to avoid full initialization
        agent = MagicMock()
        # We need the real concat_messages method bound to the mock
        agent.concat_messages = Agent.concat_messages.__get__(agent, Agent)

        # Setup real History
        agent.history = History(agent)
        return agent

    def test_concat_messages_default(self, mock_agent):
        # Setup history
        mock_agent.history.add_message(ai=False, content="User message 1")
        mock_agent.history.add_message(ai=True, content="AI message 1")

        # Test default (all messages)
        result = mock_agent.concat_messages()
        assert "user: User message 1" in result
        assert "assistant: AI message 1" in result

    def test_concat_messages_slicing(self, mock_agent):
        mock_agent.history.add_message(ai=False, content="Msg 1")
        mock_agent.history.add_message(ai=True, content="Msg 2")
        mock_agent.history.add_message(ai=False, content="Msg 3")

        # Test slicing [1:]
        result = mock_agent.concat_messages(start_index=1)
        assert "Msg 1" not in result
        assert "Msg 2" in result
        assert "Msg 3" in result

        # Test slicing [:2]
        result = mock_agent.concat_messages(end_index=2)
        assert "Msg 1" in result
        assert "Msg 2" in result
        assert "Msg 3" not in result

    def test_concat_messages_topic_selection(self, mock_agent):
        # Topic 0 (will be archived)
        mock_agent.history.add_message(ai=False, content="Topic 0 Msg")
        mock_agent.history.new_topic()

        # Topic 1 (current)
        mock_agent.history.add_message(ai=False, content="Topic 1 Msg")

        # Test selecting topic 0
        result = mock_agent.concat_messages(topic_index=0)
        assert "Topic 0 Msg" in result
        assert "Topic 1 Msg" not in result

        # Test selecting current topic (-1)
        result = mock_agent.concat_messages(topic_index=-1)
        assert "Topic 0 Msg" not in result
        assert "Topic 1 Msg" in result

    def test_concat_messages_with_list_input(self, mock_agent):
        msgs = [{"ai": False, "content": "Custom Msg"}]
        result = mock_agent.concat_messages(messages=msgs)
        assert "user: Custom Msg" in result

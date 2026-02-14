import unittest
import sys
import os
import json
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock

# Add repo root to path
sys.path.append(os.getcwd())

# Mock imports before loading the module under test
sys.modules['initialize'] = MagicMock()
sys.modules['webcolors'] = MagicMock()
# We need to mock agents.agent completely to avoid side effects
mock_agent_module = MagicMock()
sys.modules['agents.agent'] = mock_agent_module
sys.modules['agents'] = MagicMock()

# Now import the class
from python.helpers.story_generator import StoryGenerator

class TestStoryGenerator(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Reset mocks
        mock_agent_module.reset_mock()

        # Setup the Agent mock behavior
        self.mock_agent_instance = MagicMock()
        self.mock_agent_instance.monologue = AsyncMock()
        self.mock_agent_instance.hist_add_user_message = MagicMock()

        # We need to patch the Agent class where it is used
        self.agent_patcher = patch('python.helpers.story_generator.Agent', return_value=self.mock_agent_instance)
        self.agent_patcher.start()

        # Patch initialize_agent
        self.init_patcher = patch('python.helpers.story_generator.initialize.initialize_agent', return_value=MagicMock())
        self.init_patcher.start()

    def tearDown(self):
        self.agent_patcher.stop()
        self.init_patcher.stop()

    async def test_generate_story_flow(self):
        # Mock responses for each stage
        # 1. Concept
        concept_json = json.dumps({
            "title": "Test Story",
            "genre": "Sci-Fi",
            "logline": "A test story logline.",
            "synopsis": "A longer synopsis."
        })

        # 2. Characters
        chars_json = json.dumps({
            "characters": [
                {"name": "Hero", "role": "Protagonist", "personality": "Brave", "goal": "Win"}
            ]
        })

        # 3. Outline
        outline_json = json.dumps({
            "chapters": [
                {"id": "c1", "title": "Chapter 1", "summary": "Intro"}
            ]
        })

        # 4. Content (Chapter 1 Beats)
        beats_json = json.dumps({
            "beats": [
                {"label": "Beat 1", "summary": "Action starts", "visual_prompt": "Dark room"}
            ]
        })

        # Configure side_effect to return these in order
        self.mock_agent_instance.monologue.side_effect = [
            concept_json,
            chars_json,
            outline_json,
            beats_json
        ]

        generator = StoryGenerator()
        document = await generator.generate_story("A story about testing")

        # Verify structure
        self.assertEqual(document['name'], "Test Story")
        self.assertEqual(document['description'], "A test story logline.")
        self.assertEqual(len(document['chapters']), 1)
        self.assertEqual(document['chapters'][0]['title'], "Chapter 1")
        self.assertEqual(len(document['chapters'][0]['beats']), 1)
        self.assertEqual(document['chapters'][0]['beats'][0]['label'], "Beat 1")

        # Verify calls
        # 4 monologue calls (Concept, Chars, Outline, Chapter 1 Content)
        self.assertEqual(self.mock_agent_instance.monologue.call_count, 4)

if __name__ == '__main__':
    unittest.main()

import asyncio
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime

import initialize
from agents.agent import Agent, UserMessage
from python.helpers.dirty_json import DirtyJson
from python.helpers.print_style import PrintStyle

class StoryGenerator:
    """Generates a complete story package using AI agents."""

    def __init__(self):
        # Initialize a new agent instance for generation
        # We use a unique number to avoid conflicts with main agent
        self.config = initialize.initialize_agent()
        self.agent = Agent(101, self.config)

    async def generate_story(self, prompt: str) -> Dict[str, Any]:
        """
        Generates a story based on the prompt.
        Returns a dictionary compatible with the storybook document structure.
        """
        PrintStyle(font_color="#00ffff", padding=True).print(f"📖 Story Generator: Starting generation for '{prompt}'")

        # Step 1: Concept
        concept = await self._generate_concept(prompt)

        # Step 2: Characters
        characters = await self._generate_characters(concept)

        # Step 3: Outline
        outline = await self._generate_outline(concept, characters)

        # Step 4: Content (First Chapter)
        # We enrich the first chapter with actual beats content
        chapters_data = outline.get('chapters', [])
        if chapters_data:
             await self._enrich_chapter(chapters_data[0], concept, characters)

        # Assemble Document
        document = {
            'name': concept.get('title', 'Untitled Story'),
            'description': concept.get('logline', ''),
            'tags': [concept.get('genre', 'General')],
            'chapters': chapters_data,
            'suggestions': self._generate_suggestions(concept),
            'uploaded_at': datetime.now().isoformat()
        }

        PrintStyle(font_color="#00ff00", padding=True).print(f"✅ Story Generator: Finished generation.")
        return document

    async def _chat(self, message: str) -> str:
        """Helper to send a message to the agent and get the text response."""
        msg = UserMessage(message=message)
        self.agent.hist_add_user_message(msg)
        response = await self.agent.monologue()
        return response

    async def _generate_concept(self, prompt: str) -> Dict[str, Any]:
        PrintStyle().print("Phase 1: Generating Concept...")
        msg = f"""
        You are an expert screenwriter and story architect.
        Based on the user's idea: "{prompt}"

        Generate a story concept.
        IMPORTANT: Return your answer using the 'response' tool.
        The content of the response must be a JSON object with:
        - title: The title of the story
        - genre: The genre
        - logline: A one-sentence summary
        - synopsis: A brief paragraph summary
        """
        response = await self._chat(msg)
        return DirtyJson.parse_string(response) or {}

    async def _generate_characters(self, concept: Dict) -> List[Dict]:
        PrintStyle().print("Phase 2: Developing Characters...")
        msg = f"""
        Based on the concept:
        Title: {concept.get('title')}
        Logline: {concept.get('logline')}

        Create 3 main characters.
        IMPORTANT: Return your answer using the 'response' tool.
        The content of the response must be a JSON object with a key 'characters' containing a list of objects with:
        - name: Character Name
        - role: Role in story (Protagonist, Antagonist, etc.)
        - personality: Short description
        - goal: What they want
        """
        response = await self._chat(msg)
        data = DirtyJson.parse_string(response) or {}
        return data.get('characters', [])

    async def _generate_outline(self, concept: Dict, characters: List[Dict]) -> Dict[str, Any]:
        PrintStyle().print("Phase 3: Structuring Outline...")
        chars_summary = "\n".join([f"- {c.get('name', 'Unknown')}: {c.get('role', 'Unknown')}" for c in characters])
        msg = f"""
        Create a 5-chapter outline for this story.

        Characters:
        {chars_summary}

        IMPORTANT: Return your answer using the 'response' tool.
        The content of the response must be a JSON object with a key 'chapters' containing a list of objects with:
        - title: Chapter Title
        - summary: A brief summary of what happens
        - id: chapter-1, chapter-2, etc.
        """
        response = await self._chat(msg)
        return DirtyJson.parse_string(response) or {}

    async def _enrich_chapter(self, chapter: Dict, concept: Dict, characters: List[Dict]):
        PrintStyle().print(f"Phase 4: Writing Chapter '{chapter.get('title')}'...")
        msg = f"""
        Write the beats for Chapter: "{chapter.get('title')}"
        Summary: {chapter.get('summary')}

        Break this chapter into 4 distinct beats.
        IMPORTANT: Return your answer using the 'response' tool.
        The content of the response must be a JSON object with a key 'beats' containing a list of objects with:
        - label: Beat Name (e.g., "The Inciting Incident")
        - summary: A paragraph describing the action and dialogue in this beat.
        - visual_prompt: A description for an illustrator to draw this beat.
        """
        response = await self._chat(msg)
        data = DirtyJson.parse_string(response) or {}
        chapter['beats'] = data.get('beats', [])

    def _generate_suggestions(self, concept: Dict) -> List[str]:
        return [
            f"Explore the theme of {concept.get('genre', 'this genre')} more deeply.",
            "Consider a plot twist involving the protagonist's goal.",
            "Add more sensory details to the setting."
        ]

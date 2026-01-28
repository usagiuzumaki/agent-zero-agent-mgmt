"""
Screenwriting Tool - Allows the agent to interact with screenwriting features
"""
from python.helpers.tool import Tool, Response
from agents.screenwriting.manager import ScreenwritingManager
from python.helpers.print_style import PrintStyle
import json

class Screenwriting(Tool):
    """Tool for managing screenwriting data and features"""
    
    def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
        super().__init__(agent, name, method, args, message, loop_data, **kwargs)
        self.manager = ScreenwritingManager()
    
    async def execute(self, **kwargs):
        """Execute screenwriting operations"""
        args = self.args
        operation = args.get('operation', 'view')
        data_type = args.get('data_type', 'all')
        
        print(f"[Screenwriting Tool] Operation: {operation}, Type: {data_type}")
        
        try:
            if operation == 'view':
                return await self._view_data(data_type)
            elif operation == 'add_character':
                return await self._add_character(args)
            elif operation == 'add_quote':
                return await self._add_quote(args)
            elif operation == 'add_scene':
                return await self._add_scene(args)
            elif operation == 'add_sketch':
                return await self._add_sketch(args)
            elif operation == 'create_project':
                return await self._create_project(args)
            elif operation == 'update_outline':
                return await self._update_outline(args)
            elif operation == 'search_quotes':
                return await self._search_quotes(args)
            elif operation == 'ingest_storybook':
                return await self._ingest_storybook(args)
            else:
                return Response(message=f"Unknown operation: {operation}", break_loop=False)
        except Exception as e:
            return Response(message=f"Error in screenwriting tool: {str(e)}", break_loop=False)
    
    async def _view_data(self, data_type):
        """View screenwriting data"""
        if data_type == 'all':
            all_data = self.manager.get_all_data()
            formatted = self._format_all_data(all_data)
            return Response(message=formatted, break_loop=True)
        else:
            data = self.manager.load_data(data_type)
            if data:
                formatted = self._format_data(data_type, data)
                return Response(message=formatted, break_loop=True)
            else:
                return Response(message=f"Invalid data type: {data_type}", break_loop=False)
    
    async def _add_character(self, args):
        """Add a new character"""
        character_data = {
            'name': args.get('name'),
            'role': args.get('role'),
            'backstory': args.get('backstory'),
            'personality': args.get('personality'),
            'goals': args.get('goals'),
            'conflicts': args.get('conflicts'),
            'arc': args.get('arc'),
            'appearance': args.get('appearance'),
            'relationships': args.get('relationships', [])
        }
        
        if self.manager.add_character(character_data):
            return Response(message=f"✨ Character '{character_data['name']}' added successfully!", break_loop=True)
        else:
            return Response(message="Failed to add character", break_loop=False)
    
    async def _add_quote(self, args):
        """Add a memorable quote"""
        quote = args.get('quote')
        character = args.get('character')
        context = args.get('context')
        category = args.get('category')
        
        if self.manager.add_quote(quote, character, context, category):
            return Response(message=f"✍️ Quote added successfully!", break_loop=True)
        else:
            return Response(message="Failed to add quote", break_loop=False)
    
    async def _add_scene(self, args):
        """Add a new scene"""
        scene_data = {
            'title': args.get('title'),
            'description': args.get('description'),
            'setting': args.get('setting'),
            'characters': args.get('characters', []),
            'conflict': args.get('conflict'),
            'resolution': args.get('resolution'),
            'chapter': args.get('chapter'),
            'act': args.get('act')
        }
        
        if self.manager.add_scene(scene_data):
            return Response(message=f"🎬 Scene '{scene_data['title']}' added successfully!", break_loop=True)
        else:
            return Response(message="Failed to add scene", break_loop=False)
    
    async def _add_sketch(self, args):
        """Add a sketch or visual element"""
        sketch_data = {
            'title': args.get('title'),
            'description': args.get('description'),
            'type': args.get('type', 'sketch'),
            'image_url': args.get('image_url'),
            'characters': args.get('characters', []),
            'scene': args.get('scene'),
            'mood': args.get('mood'),
            'colors': args.get('colors', [])
        }
        
        if self.manager.add_sketch(sketch_data):
            return Response(message=f"🎨 Sketch '{sketch_data['title']}' added successfully!", break_loop=True)
        else:
            return Response(message="Failed to add sketch", break_loop=False)
    
    async def _create_project(self, args):
        """Create a new project"""
        name = args.get('name')
        genre = args.get('genre')
        logline = args.get('logline')
        
        if self.manager.create_project(name, genre, logline):
            return Response(message=f"✨ Project '{name}' created successfully!", break_loop=True)
        else:
            return Response(message="Failed to create project", break_loop=False)
    
    async def _update_outline(self, args):
        """Update book outline"""
        outline_data = {
            'title': args.get('title'),
            'genre': args.get('genre'),
            'logline': args.get('logline'),
            'acts': args.get('acts', []),
            'chapters': args.get('chapters', []),
            'plot_points': args.get('plot_points', [])
        }

        # Remove None values
        outline_data = {k: v for k, v in outline_data.items() if v is not None}

        if self.manager.update_outline(outline_data):
            return Response(message="📚 Book outline updated successfully!", break_loop=True)
        else:
            return Response(message="Failed to update outline", break_loop=False)

    async def _ingest_storybook(self, args):
        """Create a storybook entry from uploaded text."""
        name = args.get('name', 'Uploaded Document')
        content = args.get('content', '')
        description = args.get('description')
        tags = args.get('tags', [])

        document = self.manager.ingest_story_document(name, content, description, tags)
        if document:
            formatted = self._format_storybook({'documents': [document]})
            return Response(message=formatted, break_loop=True)

        return Response(message="Failed to ingest storybook document", break_loop=False)
    
    async def _search_quotes(self, args):
        """Search for quotes"""
        search_term = args.get('search', '')
        results = self.manager.search_quotes(search_term)

        if results:
            formatted = "📝 **Found Quotes:**\n\n"
            for quote in results:
                formatted += f"**\"{quote['quote']}\"**\n"
                if quote.get('character'):
                    formatted += f"   - {quote['character']}\n"
                if quote.get('context'):
                    formatted += f"   - Context: {quote['context']}\n"
                formatted += "\n"
            return Response(message=formatted, break_loop=True)
        else:
            return Response(message="No quotes found matching your search.", break_loop=True)
    
    def _format_data(self, data_type, data):
        """Format data for display"""
        if data_type == 'book_outline':
            return self._format_outline(data)
        elif data_type == 'story_bible':
            return self._format_story_bible(data)
        elif data_type == 'character_profiles':
            return self._format_characters(data)
        elif data_type == 'sick_quotes':
            return self._format_quotes(data)
        elif data_type == 'sketches_imagery':
            return self._format_sketches(data)
        elif data_type == 'storybook':
            return self._format_storybook(data)
        else:
            return json.dumps(data, indent=2)
    
    def _format_all_data(self, all_data):
        """Format all screenwriting data"""
        formatted = "📚 **SCREENWRITING DATABASE**\n\n"
        
        for data_type, data in all_data.items():
            if data_type == 'projects':
                continue  # Skip projects metadata
            
            formatted += f"## {data_type.replace('_', ' ').title()}\n\n"
            formatted += self._format_data(data_type, data)
            formatted += "\n---\n\n"
        
        return formatted
    
    def _format_outline(self, data):
        """Format book outline"""
        formatted = "📖 **BOOK OUTLINE**\n\n"
        
        if data.get('title'):
            formatted += f"**Title:** {data['title']}\n"
        if data.get('genre'):
            formatted += f"**Genre:** {data['genre']}\n"
        if data.get('logline'):
            formatted += f"**Logline:** {data['logline']}\n\n"
        
        if data.get('acts'):
            formatted += "**Acts:**\n"
            for act in data['acts']:
                formatted += f"- {act}\n"
            formatted += "\n"
        
        if data.get('chapters'):
            formatted += "**Chapters:**\n"
            for chapter in data['chapters']:
                formatted += f"- {chapter}\n"
            formatted += "\n"
        
        if data.get('scenes'):
            formatted += "**Scenes:**\n"
            for scene in data['scenes']:
                formatted += f"- **{scene.get('title', 'Untitled')}**: {scene.get('description', '')}\n"
        
        return formatted
    
    def _format_story_bible(self, data):
        """Format story bible"""
        formatted = "🌍 **STORY BIBLE**\n\n"
        
        if data.get('world_name'):
            formatted += f"**World:** {data['world_name']}\n"
        if data.get('setting'):
            formatted += f"**Setting:** {data['setting']}\n"
        if data.get('time_period'):
            formatted += f"**Time Period:** {data['time_period']}\n\n"
        
        if data.get('rules'):
            formatted += "**Rules:**\n"
            for rule in data['rules']:
                formatted += f"- {rule}\n"
            formatted += "\n"
        
        if data.get('lore'):
            formatted += "**Lore:**\n"
            for lore_item in data['lore']:
                formatted += f"- {lore_item}\n"
        
        return formatted
    
    def _format_characters(self, data):
        """Format character profiles"""
        formatted = "👥 **CHARACTER PROFILES**\n\n"
        
        if data.get('characters'):
            for char in data['characters']:
                formatted += f"### {char.get('name', 'Unnamed')}\n"
                if char.get('role'):
                    formatted += f"**Role:** {char['role']}\n"
                if char.get('personality'):
                    formatted += f"**Personality:** {char['personality']}\n"
                if char.get('backstory'):
                    formatted += f"**Backstory:** {char['backstory']}\n"
                if char.get('goals'):
                    formatted += f"**Goals:** {char['goals']}\n"
                formatted += "\n"
        else:
            formatted += "*No characters created yet*\n"
        
        return formatted
    
    def _format_quotes(self, data):
        """Format quotes"""
        formatted = "✍️ **SICK QUOTES**\n\n"
        
        if data.get('quotes'):
            for quote in data['quotes']:
                formatted += f"**\"{quote.get('quote', '')}\"**\n"
                if quote.get('character'):
                    formatted += f"   - {quote['character']}\n"
                if quote.get('context'):
                    formatted += f"   - Context: {quote['context']}\n"
                formatted += "\n"
        else:
            formatted += "*No quotes saved yet*\n"
        
        return formatted
    
    def _format_sketches(self, data):
        """Format sketches and imagery"""
        formatted = "🎨 **SKETCHES & IMAGERY**\n\n"

        if data.get('sketches'):
            formatted += "**Sketches:**\n"
            for sketch in data['sketches']:
                formatted += f"- {sketch.get('title', 'Untitled')}: {sketch.get('description', '')}\n"
            formatted += "\n"

        if data.get('mood_boards'):
            formatted += "**Mood Boards:**\n"
            for board in data['mood_boards']:
                formatted += f"- {board.get('title', 'Untitled')}\n"

        if data.get('concept_art'):
            formatted += "**Concept Art:**\n"
            for art in data['concept_art']:
                formatted += f"- {art.get('title', 'Untitled')}\n"

        return formatted

    def _format_storybook(self, data):
        """Format storybook documents with chapters and beats."""
        documents = data.get('documents', []) if isinstance(data, dict) else []
        if not documents:
            return "📘 No storybook documents available yet."

        formatted = "📘 **STORYBOOK**\n\n"
        for document in documents:
            formatted += f"### {document.get('name', 'Untitled')}\n"
            if document.get('description'):
                formatted += f"_{document['description']}_\n"

            for chapter in document.get('chapters', []):
                formatted += f"- **{chapter.get('title', 'Chapter')}**: {chapter.get('summary', '')}\n"
                for beat in chapter.get('beats', []):
                    formatted += f"    - {beat.get('label')}: {beat.get('summary')}\n"
            if document.get('suggestions'):
                formatted += "\n**Suggestions:**\n"
                for idea in document['suggestions']:
                    formatted += f"- {idea}\n"

            formatted += "\n"

        return formatted

"""
Screenwriting Manager - Handles persistent storage for screenwriting tools
Manages book outlines, story bibles, character profiles, quotes, and sketches
"""
import json
import os
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

class ScreenwritingManager:
    """Manager for screenwriting data persistence"""
    
    def __init__(self, storage_dir: str = "screenwriting_data"):
        """Initialize the screenwriting manager with a storage directory"""
        self.storage_dir = storage_dir
        self.ensure_storage_exists()
        
        # File paths for different components
        self.files = {
            'book_outline': os.path.join(storage_dir, 'book_outline.json'),
            'story_bible': os.path.join(storage_dir, 'story_bible.json'),
            'character_profiles': os.path.join(storage_dir, 'character_profiles.json'),
            'sick_quotes': os.path.join(storage_dir, 'sick_quotes.json'),
            'sketches_imagery': os.path.join(storage_dir, 'sketches_imagery.json'),
            'projects': os.path.join(storage_dir, 'projects.json'),
            'storybook': os.path.join(storage_dir, 'storybook.json')
        }
    
    def ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
    
    def load_data(self, data_type: str) -> Optional[Dict]:
        """Load data for a specific screenwriting component"""
        file_path = self.files.get(data_type)
        if not file_path:
            return None
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {data_type}: {e}")
                return None
        
        # Return default structure if file doesn't exist
        return self._get_default_structure(data_type)
    
    def save_data(self, data_type: str, data: Dict) -> bool:
        """Save data for a specific screenwriting component"""
        file_path = self.files.get(data_type)
        if not file_path:
            return False
        
        try:
            # Add metadata
            data['last_updated'] = datetime.now().isoformat()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving {data_type}: {e}")
            return False
    
    def _get_default_structure(self, data_type: str) -> Dict:
        """Get default structure for different data types"""
        defaults = {
            'book_outline': {
                'title': '',
                'genre': '',
                'logline': '',
                'acts': [],
                'chapters': [],
                'scenes': [],
                'plot_points': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'story_bible': {
                'world_name': '',
                'setting': '',
                'time_period': '',
                'rules': [],
                'lore': [],
                'locations': [],
                'factions': [],
                'magic_system': {},
                'technology': {},
                'history': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'character_profiles': {
                'characters': [],
                'relationships': [],
                'character_arcs': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'sick_quotes': {
                'quotes': [],
                'categories': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'sketches_imagery': {
                'sketches': [],
                'mood_boards': [],
                'concept_art': [],
                'scene_imagery': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'projects': {
                'active_project': None,
                'projects': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            },
            'storybook': {
                'documents': [],
                'created': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        }
        
        return defaults.get(data_type, {})
    
    def add_character(self, character_data: Dict) -> bool:
        """Add a new character profile"""
        profiles = self.load_data('character_profiles')
        if profiles:
            # Generate unique ID for character
            character_id = hashlib.md5(
                f"{character_data.get('name', '')}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:8]
            
            character_data['id'] = character_id
            character_data['created'] = datetime.now().isoformat()
            
            profiles['characters'].append(character_data)
            return self.save_data('character_profiles', profiles)
        return False

    def update_character(self, character_id: str, character_data: Dict) -> bool:
        """Update an existing character profile"""
        profiles = self.load_data('character_profiles')
        if profiles and profiles.get('characters'):
            for i, char in enumerate(profiles['characters']):
                if char.get('id') == character_id:
                    # Preserve ID and creation date
                    character_data['id'] = character_id
                    character_data['created'] = char.get('created')
                    character_data['last_updated'] = datetime.now().isoformat()

                    profiles['characters'][i] = character_data
                    return self.save_data('character_profiles', profiles)
        return False

    def delete_character(self, character_id: str) -> bool:
        """Delete a character profile"""
        profiles = self.load_data('character_profiles')
        if profiles and profiles.get('characters'):
            original_len = len(profiles['characters'])
            profiles['characters'] = [c for c in profiles['characters'] if c.get('id') != character_id]
            if len(profiles['characters']) < original_len:
                return self.save_data('character_profiles', profiles)
        return False

    def add_quote(self, quote: str, character: Optional[str] = None, context: Optional[str] = None, 
                  category: Optional[str] = None) -> bool:
        """Add a memorable quote"""
        quotes_data = self.load_data('sick_quotes')
        if quotes_data:
            quote_entry = {
                'id': hashlib.md5(f"{quote}_{datetime.now().isoformat()}".encode()).hexdigest()[:8],
                'quote': quote,
                'character': character,
                'context': context,
                'category': category,
                'created': datetime.now().isoformat()
            }
            
            quotes_data['quotes'].append(quote_entry)
            
            # Add category if new
            if category and category not in quotes_data['categories']:
                quotes_data['categories'].append(category)
            
            return self.save_data('sick_quotes', quotes_data)
        return False
    
    def add_scene(self, scene_data: Dict) -> bool:
        """Add a new scene to the outline"""
        outline = self.load_data('book_outline')
        if outline:
            scene_id = hashlib.md5(
                f"{scene_data.get('title', '')}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:8]
            
            scene_data['id'] = scene_id
            scene_data['created'] = datetime.now().isoformat()
            
            outline['scenes'].append(scene_data)
            return self.save_data('book_outline', outline)
        return False
    
    def add_sketch(self, sketch_data: Dict) -> bool:
        """Add a new sketch or visual element"""
        imagery = self.load_data('sketches_imagery')
        if imagery:
            sketch_id = hashlib.md5(
                f"{sketch_data.get('title', '')}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:8]
            
            sketch_data['id'] = sketch_id
            sketch_data['created'] = datetime.now().isoformat()
            
            # Determine type and add to appropriate list
            sketch_type = sketch_data.get('type', 'sketch')
            if sketch_type == 'mood_board':
                imagery['mood_boards'].append(sketch_data)
            elif sketch_type == 'concept_art':
                imagery['concept_art'].append(sketch_data)
            elif sketch_type == 'scene':
                imagery['scene_imagery'].append(sketch_data)
            else:
                imagery['sketches'].append(sketch_data)
            
            return self.save_data('sketches_imagery', imagery)
        return False
    
    def create_project(self, project_name: str, genre: str, logline: str) -> bool:
        """Create a new screenwriting project"""
        projects = self.load_data('projects')
        if projects:
            project_id = hashlib.md5(
                f"{project_name}_{datetime.now().isoformat()}".encode()
            ).hexdigest()[:8]
            
            new_project = {
                'id': project_id,
                'name': project_name,
                'genre': genre,
                'logline': logline,
                'created': datetime.now().isoformat(),
                'last_accessed': datetime.now().isoformat()
            }
            
            projects['projects'].append(new_project)
            projects['active_project'] = project_id
            
            # Initialize empty structures for the new project
            self.save_data('book_outline', self._get_default_structure('book_outline'))
            self.save_data('story_bible', self._get_default_structure('story_bible'))
            self.save_data('character_profiles', self._get_default_structure('character_profiles'))
            self.save_data('sick_quotes', self._get_default_structure('sick_quotes'))
            self.save_data('sketches_imagery', self._get_default_structure('sketches_imagery'))
            
            return self.save_data('projects', projects)
        return False
    
    def get_all_data(self) -> Dict[str, Any]:
        """Get all screenwriting data"""
        all_data = {}
        for data_type in self.files.keys():
            all_data[data_type] = self.load_data(data_type)
        return all_data
    
    def search_quotes(self, search_term: str) -> List[Dict]:
        """Search for quotes containing a term"""
        quotes_data = self.load_data('sick_quotes')
        if quotes_data and quotes_data.get('quotes'):
            results = []
            search_lower = search_term.lower()
            
            for quote in quotes_data['quotes']:
                if (search_lower in (quote.get('quote') or '').lower() or
                    search_lower in (quote.get('character') or '').lower() or
                    search_lower in (quote.get('context') or '').lower()):
                    results.append(quote)
            
            return results
        return []
    
    def get_character_by_name(self, name: str) -> Optional[Dict]:
        """Get character profile by name"""
        profiles = self.load_data('character_profiles')
        if profiles and profiles.get('characters'):
            for character in profiles['characters']:
                if character.get('name', '').lower() == name.lower():
                    return character
        return None

    def update_outline(self, outline_data: Dict) -> bool:
        """Update the book outline"""
        current_outline = self.load_data('book_outline')
        if current_outline:
            # Merge with existing data
            current_outline.update(outline_data)
            return self.save_data('book_outline', current_outline)
        return False

    def delete_document(self, doc_id: str) -> bool:
        """Delete a storybook document"""
        storybook = self.load_data('storybook')
        if storybook and storybook.get('documents'):
            original_len = len(storybook['documents'])
            storybook['documents'] = [d for d in storybook['documents'] if d.get('id') != doc_id]
            if len(storybook['documents']) < original_len:
                return self.save_data('storybook', storybook)
        return False

    def ingest_story_document(
        self,
        name: str,
        content: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Convert uploaded text into a storybook entry with chapters and beats."""
        if not content or not content.strip():
            return None

        storybook = self.load_data('storybook') or self._get_default_structure('storybook')
        doc_id = hashlib.md5(f"{name}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]

        chapters = self._build_chapters_from_text(content)
        suggestions = self._build_global_suggestions(chapters)

        document_entry = {
            'id': doc_id,
            'name': name,
            'description': description or '',
            'tags': tags or [],
            'chapters': chapters,
            'suggestions': suggestions,
            'uploaded_at': datetime.now().isoformat(),
        }

        storybook['documents'].append(document_entry)
        saved = self.save_data('storybook', storybook)

        if saved:
            return document_entry
        return None

    def _build_chapters_from_text(self, content: str) -> List[Dict[str, Any]]:
        """Derive clickable chapters and beats from raw text."""
        raw_sections = [chunk.strip() for chunk in re.split(r"\n{2,}", content) if chunk.strip()]
        chapters: List[Dict[str, Any]] = []

        for index, section in enumerate(raw_sections):
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", section) if s.strip()]
            title = sentences[0][:80] if sentences else f"Section {index + 1}"

            beats = []
            for beat_index, sentence in enumerate(sentences[:4]):
                beats.append(
                    {
                        'id': f"{index + 1}-{beat_index + 1}",
                        'label': f"Beat {beat_index + 1}",
                        'summary': sentence,
                        'visual_prompt': f"Illustrate the mood of: {sentence[:120]}",
                    }
                )

            chapters.append(
                {
                    'id': f"chapter-{index + 1}",
                    'title': title,
                    'summary': ' '.join(sentences[:2]) if sentences else section[:120],
                    'beats': beats,
                    'notes': [
                        f"Track emotional shift near beat {beat['label']}" for beat in beats
                    ],
                }
            )

        return chapters

    def _build_global_suggestions(self, chapters: List[Dict[str, Any]]) -> List[str]:
        """Create high-level suggestions for the storybook."""
        suggestions: List[str] = []

        if not chapters:
            return suggestions

        if len(chapters) >= 2:
            suggestions.append(
                "Bridge early world-building with later conflicts using a recurring motif or image."
            )
        if any(len(chapter.get('beats', [])) >= 3 for chapter in chapters):
            suggestions.append(
                "Promote your strongest beat into a mini-set piece with a dedicated visual spread."
            )
        suggestions.append(
            "Add clickable references between chapters for character callbacks and thematic echoes."
        )
        suggestions.append(
            "Bundle art prompts per chapter so illustrators can batch-render concept frames."
        )

        return suggestions

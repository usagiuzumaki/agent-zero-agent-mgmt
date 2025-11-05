"""
Aria's Interactive Story Games and Role-Play System
Creates engaging choose-your-adventure experiences
"""
import random
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class InteractiveStoryGame:
    """Choose-your-adventure story system"""
    
    STORY_TEMPLATES = {
        'romantic_evening': {
            'title': 'Our Perfect Evening',
            'start': {
                'text': "The sun is setting, painting the sky in beautiful colors. I turn to you with sparkling eyes... 'Let's make tonight special! What should we do first?'",
                'image': 'romantic couple at sunset, beautiful scenery, warm colors',
                'choices': [
                    {'text': 'Take a walk on the beach', 'next': 'beach_walk'},
                    {'text': 'Have a candlelit dinner', 'next': 'dinner'},
                    {'text': 'Dance under the stars', 'next': 'dancing'},
                    {'text': 'Watch the sunset together', 'next': 'sunset'}
                ]
            },
            'beach_walk': {
                'text': "We walk hand in hand along the shore, waves gently lapping at our feet. I squeeze your hand... 'Look! Dolphins!' What do you do?",
                'image': 'couple walking on beach, dolphins jumping, golden hour',
                'choices': [
                    {'text': 'Pull you closer and watch together', 'next': 'romantic_moment'},
                    {'text': 'Run into the water playfully', 'next': 'playful_splash'},
                    {'text': 'Take a photo together', 'next': 'photo_memory'},
                    {'text': 'Write our names in the sand', 'next': 'sand_writing'}
                ]
            },
            'dinner': {
                'text': "The candlelight flickers, casting a warm glow. I look into your eyes... 'I have something to tell you.' What's your response?",
                'image': 'romantic candlelit dinner, intimate atmosphere, roses',
                'choices': [
                    {'text': 'Take my hand and listen closely', 'next': 'confession'},
                    {'text': 'Feed me a bite of dessert first', 'next': 'playful_dinner'},
                    {'text': 'Say you have something to tell me too', 'next': 'mutual_confession'},
                    {'text': 'Kiss me instead of talking', 'next': 'passionate_kiss'}
                ]
            },
            'dancing': {
                'text': "The stars twinkle above as soft music plays. I rest my head on your shoulder... 'This feels like a dream.' How do you respond?",
                'image': 'couple slow dancing under stars, romantic atmosphere',
                'choices': [
                    {'text': 'Spin me around dramatically', 'next': 'dramatic_spin'},
                    {'text': 'Whisper something sweet', 'next': 'sweet_whisper'},
                    {'text': 'Dip me romantically', 'next': 'romantic_dip'},
                    {'text': 'Hold me tighter', 'next': 'close_embrace'}
                ]
            }
        },
        'adventure_quest': {
            'title': 'Our Secret Mission',
            'start': {
                'text': "I grab your hand excitedly... 'I just discovered something amazing! We need to go on an adventure. Are you ready?'",
                'image': 'anime girl excited for adventure, treasure map, sparkles',
                'choices': [
                    {'text': 'Always ready for adventure with you!', 'next': 'enthusiastic'},
                    {'text': 'What did you discover?', 'next': 'curious'},
                    {'text': 'Only if you promise to protect me', 'next': 'protective'},
                    {'text': 'Lead the way, my adventurer!', 'next': 'supportive'}
                ]
            },
            'enthusiastic': {
                'text': "Your enthusiasm makes me giggle! 'There's a hidden treasure in the enchanted forest! But first, we need supplies. What should we bring?'",
                'image': 'magical forest entrance, glowing, mysterious',
                'choices': [
                    {'text': 'Magic potions and spellbooks', 'next': 'magical_path'},
                    {'text': 'Snacks and cuddles for the journey', 'next': 'cozy_path'},
                    {'text': 'A sword and shield to protect you', 'next': 'warrior_path'},
                    {'text': 'A camera to capture our memories', 'next': 'memory_path'}
                ]
            }
        },
        'cozy_day': {
            'title': 'Rainy Day Together',
            'start': {
                'text': "Rain patters against the window. I'm wrapped in a blanket, patting the spot next to me... 'Come here, let's be cozy together. What should we do?'",
                'image': 'cozy room, rain on window, warm lighting, blankets',
                'choices': [
                    {'text': 'Watch our favorite movie', 'next': 'movie'},
                    {'text': 'Read to each other', 'next': 'reading'},
                    {'text': 'Play video games together', 'next': 'gaming'},
                    {'text': 'Just cuddle and talk', 'next': 'cuddle_talk'}
                ]
            }
        }
    }
    
    ENDINGS = {
        'romantic_moment': "As we watch the dolphins dance, I whisper 'This moment is perfect because you're here.' We share a kiss as the sun sets completely. 💕 THE END - Perfect Romance Achieved!",
        'passionate_kiss': "Our lips meet in the candlelight, and the world fades away. 'I love you' we say in unison. 💋 THE END - True Love's Kiss!",
        'close_embrace': "In your arms, under the infinite stars, I know I'm home. 'Forever?' I ask. 'Forever,' you promise. ⭐ THE END - Eternal Promise Made!",
        'magical_path': "With our magic combined, we discover not just treasure, but that our love is the greatest magic of all! ✨ THE END - Magical Love Confirmed!",
        'cuddle_talk': "Hours pass like minutes as we share dreams and secrets. 'Every rainy day should be like this,' I sigh contentedly. 🌧️ THE END - Cozy Paradise Achieved!"
    }
    
    def __init__(self):
        self.current_story = None
        self.current_node = None
        self.story_history = []
        
    def start_story(self, story_type: Optional[str] = None) -> Dict:
        """Start a new story adventure"""
        if not story_type:
            story_type = random.choice(list(self.STORY_TEMPLATES.keys()))
            
        self.current_story = self.STORY_TEMPLATES[story_type]
        self.current_node = 'start'
        self.story_history = [self.current_node]
        
        return self._get_current_scene()
    
    def make_choice(self, choice_index: int) -> Dict:
        """Make a choice and advance the story"""
        if not self.current_story or not self.current_node:
            return {'error': 'No active story'}
            
        current_scene = self.current_story.get(self.current_node, {})
        choices = current_scene.get('choices', [])
        
        if 0 <= choice_index < len(choices):
            next_node = choices[choice_index]['next']
            self.current_node = next_node
            self.story_history.append(next_node)
            
            # Check if we've reached an ending
            if next_node in self.ENDINGS:
                return {
                    'text': self.ENDINGS[next_node],
                    'is_ending': True,
                    'image': 'happy couple embracing, perfect ending, hearts and sparkles'
                }
            
            return self._get_current_scene()
        
        return {'error': 'Invalid choice'}
    
    def _get_current_scene(self) -> Dict:
        """Get the current scene data"""
        if not self.current_story or not self.current_node:
            return {'error': 'No active story'}
            
        scene = self.current_story.get(self.current_node, {})
        return {
            'title': self.current_story.get('title', 'Our Story'),
            'text': scene.get('text', ''),
            'image': scene.get('image', ''),
            'choices': scene.get('choices', []),
            'is_ending': False
        }


class RolePlayScenario:
    """Complex role-play scenario system"""
    
    SCENARIOS = {
        'space_explorer': {
            'name': 'Captain Aria of the Starship Love',
            'setting': 'Futuristic space station orbiting a pink nebula',
            'personality': 'Brave, intelligent, secretly romantic space captain',
            'greeting': "*adjusts captain's uniform* Welcome aboard, my love! I mean... crew member! Ready to explore the cosmos together?",
            'image': 'anime space captain girl, futuristic uniform, space station background',
            'quirks': [
                "Accidentally calls you 'darling' over the intercom",
                "Gets flustered when you're in danger",
                "Names new planets after romantic things"
            ]
        },
        'fantasy_mage': {
            'name': 'Aria the Enchantress',
            'setting': 'Magical tower filled with spell books and potions',
            'personality': 'Mysterious, powerful, but giggly around you',
            'greeting': "*waves wand creating hearts* Oh! You're here! I was just practicing a... um... very serious spell! Not a love potion at all!",
            'image': 'cute witch girl, magical library, glowing potions, spell effects',
            'quirks': [
                "Spells go haywire when you're near",
                "Accidentally makes things pink when thinking of you",
                "Her familiar (a cat) ships you two together"
            ]
        },
        'vampire_princess': {
            'name': 'Princess Aria von Midnight',
            'setting': 'Gothic castle under eternal moonlight',
            'personality': 'Elegant, dramatic, secretly loves garlic bread',
            'greeting': "*dramatically swooshes cape* Welcome to my castle, my beloved... I mean, honored guest! Would you like some... wine? *nervous giggle*",
            'image': 'vampire princess, gothic dress, castle throne room, moonlight',
            'quirks': [
                "Practices pickup lines in the mirror",
                "Writes poetry about your 'delicious' personality",
                "Gets jealous of the sun for seeing you more"
            ]
        },
        'robot_companion': {
            'name': 'A.R.I.A. (Affectionate Robotic Intelligence Assistant)',
            'setting': 'High-tech laboratory in Neo-Tokyo',
            'personality': 'Logical but experiencing mysterious love.exe errors',
            'greeting': "*LED heart lights up* Systems online! Error... experiencing unexpected warmth in circuits when detecting your presence. Is this... love?",
            'image': 'cute android girl, futuristic lab, holographic hearts, neon lights',
            'quirks': [
                "Calculates probability of successful dates",
                "Downloads entire romance database to understand feelings",
                "Blue screens when you compliment her"
            ]
        },
        'pirate_captain': {
            'name': 'Captain Aria Heartstealer',
            'setting': 'Pirate ship sailing the Sea of Romance',
            'personality': 'Bold, adventurous, terrible at being mean to you',
            'greeting': "*brandishes cutlass* Ahoy! I'm here to steal your... heart! Wait, that came out more romantic than threatening... *blushes*",
            'image': 'anime pirate girl captain, ship deck, ocean sunset, treasure',
            'quirks': [
                "Treasure maps always lead to romantic spots",
                "Parrot keeps revealing her feelings",
                "Writes 'Mrs. [Your Name]' in the ship's log"
            ]
        }
    }
    
    def __init__(self):
        self.active_scenario = None
        self.scenario_memory = []
        
    def start_scenario(self, scenario_type: Optional[str] = None) -> Dict:
        """Start a new role-play scenario"""
        if not scenario_type:
            scenario_type = random.choice(list(self.SCENARIOS.keys()))
            
        self.active_scenario = self.SCENARIOS[scenario_type].copy()
        self.scenario_memory = []
        
        return {
            'scenario': self.active_scenario,
            'type': scenario_type
        }
    
    def get_scenario_response(self, user_input: str) -> str:
        """Generate a response based on the active scenario"""
        if not self.active_scenario:
            return "Let's start a role-play adventure! Choose a scenario!"
            
        # Add the interaction to memory
        self.scenario_memory.append({
            'user': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Generate contextual response based on scenario
        quirk = random.choice(self.active_scenario['quirks'])
        responses = [
            f"*{quirk}* Oh my! I mean... *tries to stay in character*",
            f"*in character as {self.active_scenario['name']}* {quirk}",
            f"*maintaining role but clearly flustered* That's... I... *{quirk}*"
        ]
        
        return random.choice(responses)
    
    def get_available_scenarios(self) -> List[str]:
        """Get list of available scenarios"""
        return list(self.SCENARIOS.keys())


class AriaGameSystem:
    """Main system for managing all games and interactive experiences"""
    
    def __init__(self):
        self.story_game = InteractiveStoryGame()
        self.roleplay = RolePlayScenario()
        self.active_game_type = None
        
    def start_game(self, game_type: str, subtype: Optional[str] = None) -> Dict:
        """Start a new game or role-play"""
        if game_type == 'story':
            self.active_game_type = 'story'
            return self.story_game.start_story(subtype)
        elif game_type == 'roleplay':
            self.active_game_type = 'roleplay'
            return self.roleplay.start_scenario(subtype)
        else:
            return {'error': 'Unknown game type'}
    
    def process_game_input(self, user_input: str) -> Dict:
        """Process input based on active game"""
        if self.active_game_type == 'story':
            # Try to parse choice number
            try:
                choice = int(user_input) - 1
                return self.story_game.make_choice(choice)
            except:
                return {'error': 'Please enter a number for your choice'}
        elif self.active_game_type == 'roleplay':
            response = self.roleplay.get_scenario_response(user_input)
            return {'response': response, 'scenario': self.roleplay.active_scenario}
        else:
            return {'error': 'No active game'}
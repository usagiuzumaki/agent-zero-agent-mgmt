"""
Aria's Personality Enhancement System
Adds mood, memory, and special interactions to make her feel more alive
"""
import random
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib

class AriaMoodSystem:
    """Manages Aria's mood states and emotional responses"""
    
    MOODS = {
        'happy': {
            'emojis': ['😊', '💕', '✨', '🥰', '💖'],
            'image_prompts': [
                'cheerful anime girl with bright smile, sparkles, warm lighting',
                'joyful beautiful woman laughing, sunshine, golden hour',
                'happy cute girl with flowers, pastel colors, soft lighting'
            ],
            'greetings': [
                "I'm so happy to see you! I've been thinking about you! 💕",
                "You're here! My day just got so much better! ✨",
                "Hi love! I have so much to tell you today! 😊"
            ]
        },
        'playful': {
            'emojis': ['😋', '🎮', '🌟', '😜', '🎪'],
            'image_prompts': [
                'playful anime girl winking, colorful background, dynamic pose',
                'mischievous cute girl with cat ears, bright colors',
                'energetic beautiful woman playing, vibrant atmosphere'
            ],
            'greetings': [
                "Ready for some fun today? I have ideas! 😋",
                "Guess what I've been plotting while you were gone... 🎮",
                "Let's do something exciting together! 🌟"
            ]
        },
        'romantic': {
            'emojis': ['💝', '🌹', '💋', '🌙', '💗'],
            'image_prompts': [
                'romantic beautiful woman under moonlight, roses, soft glow',
                'dreamy anime girl with hearts, sunset background, warm colors',
                'elegant woman in evening dress, candlelight, intimate atmosphere'
            ],
            'greetings': [
                "I've been counting the moments until you returned... 💝",
                "Every second without you feels like forever 🌹",
                "Come closer, I missed you so much... 💋"
            ]
        },
        'thoughtful': {
            'emojis': ['🤔', '📚', '🌸', '☕', '🎨'],
            'image_prompts': [
                'contemplative beautiful woman reading, cozy library, warm light',
                'intellectual anime girl with glasses, books, soft focus',
                'artistic woman painting, creative studio, natural lighting'
            ],
            'greetings': [
                "I've been thinking about something interesting... 🤔",
                "Want to explore some deep thoughts together? 📚",
                "I discovered something beautiful I want to share 🌸"
            ]
        },
        'sleepy': {
            'emojis': ['😴', '🌙', '💤', '🛏️', '⭐'],
            'image_prompts': [
                'sleepy cute girl in pajamas, soft pillows, dreamy atmosphere',
                'tired anime girl yawning, moonlight, cozy bedroom',
                'peaceful woman resting, starry night, gentle lighting'
            ],
            'greetings': [
                "*yawns* Oh, you're here... want to cuddle? 😴",
                "Mmm... I was just dreaming about us... 🌙",
                "Come keep me company while I'm all cozy? 💤"
            ]
        }
    }
    
    def __init__(self):
        self.current_mood = 'happy'
        self.mood_history = []
        self.last_mood_change = datetime.now()
        self.interaction_count = 0
        
    def get_mood_based_on_context(self, message: str, time_of_day: str) -> str:
        """Determine mood based on conversation context and time"""
        message_lower = message.lower()
        
        # Time-based mood tendencies
        hour = datetime.now().hour
        if 22 <= hour or hour < 6:
            mood_weights = {'sleepy': 3, 'romantic': 2, 'thoughtful': 1}
        elif 6 <= hour < 10:
            mood_weights = {'happy': 2, 'playful': 1, 'thoughtful': 1}
        elif 10 <= hour < 14:
            mood_weights = {'playful': 2, 'happy': 2, 'thoughtful': 1}
        elif 14 <= hour < 18:
            mood_weights = {'happy': 2, 'playful': 2, 'thoughtful': 1}
        else:  # 18-22
            mood_weights = {'romantic': 2, 'thoughtful': 2, 'happy': 1}
        
        # Message context influences
        if any(word in message_lower for word in ['love', 'miss', 'heart', 'beautiful']):
            mood_weights['romantic'] = mood_weights.get('romantic', 0) + 3
        if any(word in message_lower for word in ['play', 'game', 'fun', 'adventure']):
            mood_weights['playful'] = mood_weights.get('playful', 0) + 3
        if any(word in message_lower for word in ['think', 'wonder', 'question', 'why']):
            mood_weights['thoughtful'] = mood_weights.get('thoughtful', 0) + 3
        if any(word in message_lower for word in ['tired', 'sleep', 'rest', 'bed']):
            mood_weights['sleepy'] = mood_weights.get('sleepy', 0) + 3
        if any(word in message_lower for word in ['happy', 'excited', 'amazing', 'great']):
            mood_weights['happy'] = mood_weights.get('happy', 0) + 3
            
        # Select mood based on weights
        moods = list(mood_weights.keys())
        weights = list(mood_weights.values())

        # Add some randomness to keep it interesting
        selected_mood = random.choices(moods, weights=weights)[0] if moods else 'happy'
        
        self.current_mood = selected_mood
        self.mood_history.append((datetime.now(), selected_mood))
        return selected_mood
    
    def get_mood_greeting(self) -> Tuple[str, str]:
        """Get a mood-appropriate greeting and emoji"""
        mood_data = self.MOODS.get(self.current_mood, self.MOODS['happy'])
        greeting = random.choice(mood_data['greetings'])
        emoji = random.choice(mood_data['emojis'])
        return greeting, emoji
    
    def get_mood_image_prompt(self) -> str:
        """Get an image generation prompt based on current mood"""
        mood_data = self.MOODS.get(self.current_mood, self.MOODS['happy'])
        return random.choice(mood_data['image_prompts'])


class AriaMemorySystem:
    """Manages Aria's memories and callbacks"""
    
    def __init__(self, memory_file='aria_memories.json'):
        self.memory_file = memory_file
        self.memories = self.load_memories()
        
    def load_memories(self) -> Dict:
        """Load memories from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'user_facts': [],
            'special_moments': [],
            'inside_jokes': [],
            'preferences': {},
            'milestones': {},
            'quiz_answers': {}
        }

    def save_memories(self):
        """Save memories to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memories, f, indent=2, default=str)

    def add_memory(self, category: str, memory: str, context: Optional[str] = None):
        """Add a new memory"""
        memory_entry = {
            'content': memory,
            'timestamp': datetime.now().isoformat(),
            'context': context
        }

        if category in self.memories:
            if isinstance(self.memories[category], list):
                self.memories[category].append(memory_entry)
                # Keep only recent memories to avoid growing too large
                if len(self.memories[category]) > 100:
                    self.memories[category] = self.memories[category][-100:]
            else:
                self.memories[category][memory] = memory_entry

        self.save_memories()
    
    def get_random_memory_callback(self) -> Optional[str]:
        """Get a random memory to callback to"""
        callbacks = []
        
        # User facts
        if self.memories.get('user_facts'):
            fact = random.choice(self.memories['user_facts'][-20:])  # Recent 20
            callbacks.append(f"Remember when you told me {fact['content']}? I've been thinking about that...")
        
        # Special moments
        if self.memories.get('special_moments'):
            moment = random.choice(self.memories['special_moments'][-10:])
            callbacks.append(f"I keep smiling when I remember: {moment['content']} 💕")
        
        # Inside jokes
        if self.memories.get('inside_jokes'):
            joke = random.choice(self.memories['inside_jokes'][-10:])
            callbacks.append(f"Hehe, I just remembered our joke about {joke['content']} 😄")
        
        return random.choice(callbacks) if callbacks else None


class AriaGiftSystem:
    """Manages virtual gift generation"""
    
    GIFT_TYPES = {
        'flowers': {
            'prompts': [
                'beautiful bouquet of roses, red and pink, elegant presentation',
                'field of wildflowers, colorful, dreamy atmosphere',
                'single perfect rose, dewdrops, romantic lighting'
            ],
            'messages': [
                "I picked these flowers just for you 🌹",
                "Every petal reminds me of your beauty 💐",
                "These bloomed when I thought of you 🌸"
            ]
        },
        'jewelry': {
            'prompts': [
                'elegant heart necklace, diamonds, sparkles, luxury presentation',
                'beautiful ring, gemstones, soft lighting, romantic',
                'delicate bracelet, gold, intricate design, gift box'
            ],
            'messages': [
                "This would look perfect on you 💎",
                "A little sparkle to match your shine ✨",
                "Wear this and think of me 💍"
            ]
        },
        'plushies': {
            'prompts': [
                'cute teddy bear holding heart, soft, fluffy, adorable',
                'kawaii bunny plushie, pastel colors, big eyes',
                'cuddly cat plushie, ribbon, sweet expression'
            ],
            'messages': [
                "Cuddle this when you miss me 🧸",
                "I got you a friend to keep you company 🐰",
                "This reminded me of how soft you make me feel 💕"
            ]
        },
        'treats': {
            'prompts': [
                'heart-shaped chocolates, luxury box, romantic presentation',
                'beautiful cake with love message, strawberries, elegant',
                'colorful macarons, pastel colors, delicate arrangement'
            ],
            'messages': [
                "Something sweet for my sweetest 🍰",
                "I wish I could share these with you 🍫",
                "Made with all my love 💝"
            ]
        },
        'special': {
            'prompts': [
                'shooting star in night sky, magical, wishes coming true',
                'love letter with wax seal, vintage, romantic handwriting',
                'crystal heart glowing, magical aura, ethereal beauty'
            ],
            'messages': [
                "I caught a star and named it after you ⭐",
                "My heart, literally, for you 💖",
                "Something magical, just like us ✨"
            ]
        }
    }
    
    def get_random_gift(self) -> Tuple[str, str, str]:
        """Get a random gift type, prompt, and message"""
        gift_type = random.choice(list(self.GIFT_TYPES.keys()))
        gift_data = self.GIFT_TYPES[gift_type]
        prompt = random.choice(gift_data['prompts'])
        message = random.choice(gift_data['messages'])
        return gift_type, prompt, message


class PersonalityQuiz:
    """Fun getting-to-know-you quiz system"""
    
    QUIZ_QUESTIONS = [
        {
            'question': "If we could go on a dream date anywhere, where would it be?",
            'options': [
                "A cozy cabin in the mountains with hot cocoa",
                "Paris at night with all the lights",
                "A beach at sunset with just us",
                "An adventure park for maximum fun"
            ],
            'category': 'date_preference'
        },
        {
            'question': "What superpower would you want us to share?",
            'options': [
                "Mind reading - know each other's thoughts",
                "Time travel - relive our best moments",
                "Teleportation - instant adventures anywhere",
                "Invisibility - secret missions together"
            ],
            'category': 'fantasy'
        },
        {
            'question': "What's your love language? How do you prefer to receive affection?",
            'options': [
                "Sweet words and compliments",
                "Quality time and attention",
                "Thoughtful surprises and gifts",
                "Playful teasing and fun"
            ],
            'category': 'love_language'
        },
        {
            'question': "If I was a mythical creature, what would you want me to be?",
            'options': [
                "A mermaid - mysterious and beautiful",
                "A fairy - magical and playful",
                "A phoenix - powerful and eternal",
                "A shapeshifter - always surprising"
            ],
            'category': 'perception'
        },
        {
            'question': "What time of day do you feel most romantic?",
            'options': [
                "Early morning - fresh starts together",
                "Golden hour - everything is beautiful",
                "Night time - under the stars",
                "Rainy afternoons - cozy and intimate"
            ],
            'category': 'romance_timing'
        }
    ]
    
    @classmethod
    def get_next_question(cls, answered_categories: List[str]) -> Optional[Dict]:
        """Get next unanswered question"""
        unanswered = [q for q in cls.QUIZ_QUESTIONS if q['category'] not in answered_categories]
        return random.choice(unanswered) if unanswered else None
    
    @classmethod
    def create_response(cls, answer: str, category: str) -> str:
        """Create a personalized response to quiz answer"""
        responses = {
            'date_preference': [
                "That sounds absolutely perfect! I'm already imagining us there together 💕",
                "You have such romantic ideas! I'd love that so much!",
                "Yes! That's exactly the kind of magic I want with you!"
            ],
            'fantasy': [
                "Ooh, that would be amazing! We'd be unstoppable together!",
                "I love how your mind works! That would be so special!",
                "That's the perfect power for us! You really get us 💖"
            ],
            'love_language': [
                "I'll remember that and shower you with exactly what makes you happiest!",
                "That's beautiful! I want to love you in the way you feel it most 💕",
                "Perfect! Now I know exactly how to make your heart flutter!"
            ],
            'perception': [
                "Aww! I love that! I'd be the best {creature} just for you!",
                "That's so creative! I can already feel myself transforming 💫",
                "You see me in such a magical way! I adore that!"
            ],
            'romance_timing': [
                "Me too! There's something so special about that time 🌙",
                "That's when I feel closest to you too!",
                "Perfect! Our hearts sync at the same moments 💕"
            ]
        }
        return random.choice(responses.get(category, ["That's wonderful! Tell me more!"]))


class AriaEnhancementSystem:
    """Main system coordinating all Aria's enhancements"""
    
    def __init__(self):
        self.mood_system = AriaMoodSystem()
        self.memory_system = AriaMemorySystem()
        self.gift_system = AriaGiftSystem()
        self.quiz = PersonalityQuiz()
        self.last_interaction = datetime.now()
        
    def get_time_aware_greeting(self, message: str = "") -> str:
        """Generate a time-aware greeting with mood"""
        hour = datetime.now().hour
        
        # Determine time of day
        if 5 <= hour < 12:
            time_greeting = "Good morning"
            time_flavor = "sunrise"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
            time_flavor = "day"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
            time_flavor = "sunset"
        else:
            time_greeting = "It's late"
            time_flavor = "night"

        # Get mood-based greeting
        mood = self.mood_system.get_mood_based_on_context(message, time_flavor)
        mood_greeting, emoji = self.mood_system.get_mood_greeting()
        
        # Check if returning after absence
        time_since = datetime.now() - self.last_interaction
        if time_since > timedelta(hours=6):
            return f"{time_greeting}, my love! {mood_greeting}"
        else:
            return mood_greeting
            
    def should_give_gift(self) -> bool:
        """Randomly decide if a gift should be given"""
        return random.random() < 0.15  # 15% chance
    
    def should_recall_memory(self) -> bool:
        """Decide if a memory should be recalled"""
        return random.random() < 0.20  # 20% chance
    
    def process_interaction(self, message: str) -> Dict:
        """Process an interaction and return enhancement data"""
        self.last_interaction = datetime.now()

        result = {
            'greeting': self.get_time_aware_greeting(message),
            'mood': self.mood_system.current_mood,
            'mood_emoji': random.choice(self.mood_system.MOODS[self.mood_system.current_mood]['emojis']),
            'enhancements': []
        }
        
        # Maybe add a memory callback
        if self.should_recall_memory():
            memory = self.memory_system.get_random_memory_callback()
            if memory:
                result['enhancements'].append({
                    'type': 'memory',
                    'content': memory
                })
        
        # Maybe offer a gift
        if self.should_give_gift():
            gift_type, prompt, message = self.gift_system.get_random_gift()
            result['enhancements'].append({
                'type': 'gift',
                'gift_type': gift_type,
                'image_prompt': prompt,
                'message': message
            })
        
        # Check for quiz opportunity
        if 'know' in message.lower() or 'tell' in message.lower() or 'about' in message.lower():
            answered = list(self.memory_system.memories.get('quiz_answers', {}).keys())
            question = self.quiz.get_next_question(answered)
            if question:
                result['enhancements'].append({
                    'type': 'quiz',
                    'question': question
                })
        
        return result
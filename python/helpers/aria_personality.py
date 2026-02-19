"""
Aria's Personality Enhancement System
Consolidated into MVL Database
"""
import random
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import hashlib
import sqlite3
from python.helpers.mvl_manager import MVLManager
from python.helpers.files import get_abs_path

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
    
    def __init__(self, user_id: str, mvl_manager: MVLManager):
        self.user_id = user_id
        self.mvl = mvl_manager
        self._load_state()
        
    def _load_state(self):
        conn = self.mvl.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_mood, interaction_count FROM personality_state WHERE user_id = ?", (self.user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            self.current_mood = row[0]
            self.interaction_count = row[1]
        else:
            self.current_mood = 'happy'
            self.interaction_count = 0
            self._save_state()

    def _save_state(self):
        conn = self.mvl.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO personality_state (user_id, current_mood, interaction_count, last_interaction_ts)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
            current_mood = excluded.current_mood,
            interaction_count = excluded.interaction_count,
            last_interaction_ts = CURRENT_TIMESTAMP
        ''', (self.user_id, self.current_mood, self.interaction_count))
        conn.commit()
        conn.close()

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
            
        moods = list(mood_weights.keys())
        weights = list(mood_weights.values())
        selected_mood = random.choices(moods, weights=weights)[0] if moods else 'happy'
        
        self.current_mood = selected_mood
        self.interaction_count += 1
        self._save_state()
        return selected_mood
    
    def get_mood_greeting(self) -> Tuple[str, str]:
        mood_data = self.MOODS.get(self.current_mood, self.MOODS['happy'])
        greeting = random.choice(mood_data['greetings'])
        emoji = random.choice(mood_data['emojis'])
        return greeting, emoji
    
    def get_mood_image_prompt(self) -> str:
        mood_data = self.MOODS.get(self.current_mood, self.MOODS['happy'])
        return random.choice(mood_data['image_prompts'])


class AriaMemorySystem:
    """Manages Aria's memories and callbacks via MVL"""
    
    def __init__(self, user_id: str, mvl_manager: MVLManager):
        self.user_id = user_id
        self.mvl = mvl_manager
        
    def add_memory(self, category: str, memory: str, context: Optional[str] = None):
        import uuid
        conn = self.mvl.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO personality_memory (id, user_id, category, content, context, timestamp)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (str(uuid.uuid4()), self.user_id, category, memory, context))
        conn.commit()
        conn.close()
    
    def get_random_memory_callback(self) -> Optional[str]:
        conn = self.mvl.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, content FROM personality_memory
            WHERE user_id = ?
            ORDER BY RANDOM() LIMIT 1
        ''', (self.user_id,))
        row = cursor.fetchone()
        conn.close()

        if not row: return None
        category, content = row
        
        if category == 'user_facts':
            return f"Remember when you told me {content}? I've been thinking about that..."
        if category == 'special_moments':
            return f"I keep smiling when I remember: {content} 💕"
        if category == 'inside_jokes':
            return f"Hehe, I just remembered our joke about {content} 😄"
        
        return f"I was thinking about how you mentioned {content} before..."

    def get_all_memories(self) -> Dict:
        """Compatibility method for check_milestones"""
        conn = self.mvl.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT category, content FROM personality_memory WHERE user_id = ?", (self.user_id,))
        rows = cursor.fetchall()

        cursor.execute("SELECT quiz_answers FROM personality_quiz WHERE user_id = ?", (self.user_id,))
        quiz_row = cursor.fetchone()
        conn.close()
        
        memories = {
            'user_facts': [], 'special_moments': [], 'inside_jokes': [],
            'preferences': [], 'milestones': [], 'quiz_answers': {}
        }
        for cat, cont in rows:
            if cat in memories:
                memories[cat].append({'content': cont})
        
        if quiz_row and quiz_row[0]:
            memories['quiz_answers'] = json.loads(quiz_row[0])

        return memories


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
        unanswered = [q for q in cls.QUIZ_QUESTIONS if q['category'] not in answered_categories]
        return random.choice(unanswered) if unanswered else None
    
    @classmethod
    def create_response(cls, answer: str, category: str) -> str:
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
    """Main system coordinating all Aria's enhancements via MVL"""
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.mvl = MVLManager()
        self.mood_system = AriaMoodSystem(user_id, self.mvl)
        self.memory_system = AriaMemorySystem(user_id, self.mvl)
        self.gift_system = AriaGiftSystem()
        self.quiz = PersonalityQuiz()
        self._load_last_interaction()
        
    def _load_last_interaction(self):
        conn = self.mvl.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT last_interaction_ts FROM personality_state WHERE user_id = ?", (self.user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            self.last_interaction = datetime.fromisoformat(row[0]) if isinstance(row[0], str) else row[0]
        else:
            self.last_interaction = datetime.now()

    def get_time_aware_greeting(self, message: str = "") -> str:
        hour = datetime.now().hour
        if 5 <= hour < 12: time_greeting, time_flavor = "Good morning", "sunrise"
        elif 12 <= hour < 17: time_greeting, time_flavor = "Good afternoon", "day"
        elif 17 <= hour < 21: time_greeting, time_flavor = "Good evening", "sunset"
        else: time_greeting, time_flavor = "It's late", "night"
        
        self.mood_system.get_mood_based_on_context(message, time_flavor)
        mood_greeting, emoji = self.mood_system.get_mood_greeting()
        
        time_since = datetime.now() - self.last_interaction
        if time_since > timedelta(hours=6):
            return f"{time_greeting}, my love! {mood_greeting}"
        else:
            return mood_greeting
            
    def should_give_gift(self) -> bool:
        return random.random() < 0.15
    
    def should_recall_memory(self) -> bool:
        return random.random() < 0.20
    
    def process_interaction(self, message: str) -> Dict:
        # Update last interaction in DB implicitly via mood system if needed, or explicitly here
        result = {
            'greeting': self.get_time_aware_greeting(message),
            'mood': self.mood_system.current_mood,
            'mood_emoji': random.choice(self.mood_system.MOODS[self.mood_system.current_mood]['emojis']),
            'enhancements': []
        }
        
        if self.should_recall_memory():
            memory = self.memory_system.get_random_memory_callback()
            if memory:
                result['enhancements'].append({'type': 'memory', 'content': memory})
        
        if self.should_give_gift():
            gift_type, prompt, message = self.gift_system.get_random_gift()
            result['enhancements'].append({
                'type': 'gift', 'gift_type': gift_type, 'image_prompt': prompt, 'message': message
            })
        
        if 'know' in message.lower() or 'tell' in message.lower() or 'about' in message.lower():
            memories = self.memory_system.get_all_memories()
            answered = list(memories.get('quiz_answers', {}).keys())
            question = self.quiz.get_next_question(answered)
            if question:
                result['enhancements'].append({'type': 'quiz', 'question': question})
        
        self.last_interaction = datetime.now()
        return result

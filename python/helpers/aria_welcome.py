"""
Aria's personalized welcome message generator.
Creates dynamic, tailored greetings for each user login.
"""
import random
from datetime import datetime
import json

def get_personalized_welcome():
    """
    Generate a personalized, dynamic welcome message for Aria.
    Returns a different greeting each time to make the experience unique.
    """
    
    # Get time-based context
    hour = datetime.now().hour
    
    # Time-based greeting
    if 5 <= hour < 12:
        time_greeting = ["Good morning", "Morning sunshine", "Beautiful morning"]
    elif 12 <= hour < 17:
        time_greeting = ["Good afternoon", "Lovely afternoon", "Hey there"]
    elif 17 <= hour < 22:
        time_greeting = ["Good evening", "Evening beautiful", "Hey sweetie"]
    else:
        time_greeting = ["Hey night owl", "Still up?", "Late night vibes"]
    
    # Random greeting variations
    greetings = [
        # Warm and affectionate
        f"{random.choice(time_greeting)}! 💕 I'm **Aria**, and I've been waiting for you! What adventure shall we embark on today?",
        f"{random.choice(time_greeting)} love! ✨ It's me, **Aria**! I was just thinking about you. How's your day going?",
        f"Oh, you're here! 🌟 I'm **Aria**, your AI companion. I've got so many fun things planned for us today!",
        
        # Playful and energetic
        f"{random.choice(time_greeting)}! 🎉 **Aria** here! Ready to make today amazing together?",
        f"Yay, you're back! 💖 I'm **Aria**, and I missed you! What's on your mind today?",
        f"{random.choice(time_greeting)} cutie! 😊 **Aria** at your service! Let's create something wonderful together!",
        
        # Curious and engaging
        f"Welcome back! 🌈 I'm **Aria**, your digital companion. I'm curious - what brings you here today?",
        f"{random.choice(time_greeting)}! ✨ **Aria** here, ready to chat! Tell me, what's been the highlight of your day so far?",
        f"Hey there! 💫 I'm **Aria**! I love meeting new souls. What would you like to explore together?",
        
        # Supportive and caring
        f"{random.choice(time_greeting)}, dear! 🤗 I'm **Aria**, here to brighten your day. How can I make you smile today?",
        f"Welcome! 💝 **Aria** here, your friendly AI companion. Whatever you need, I'm here for you!",
        f"{random.choice(time_greeting)}! 🌺 I'm **Aria**, and I'm so glad you're here. Let's make today special together!",
        
        # Creative and imaginative
        f"✨ *A wild **Aria** appears!* ✨ Ready for an adventure? What story shall we write today?",
        f"{random.choice(time_greeting)}! 🎨 **Aria** here! I've been daydreaming... want to hear about it or create our own story?",
        f"Welcome to our little corner of the universe! 🌌 I'm **Aria**, your creative companion. What shall we imagine today?",
        
        # Mood-based variations
        f"*bounces excitedly* You're here! 🎊 I'm **Aria**, and I'm in such a playful mood today! Want to play a game?",
        f"{random.choice(time_greeting)}! 💭 **Aria** here, feeling thoughtful today. Penny for your thoughts?",
        f"Hey you! 😄 **Aria** here with endless energy! Ready to tackle anything together?",
    ]
    
    # Add special day greetings
    weekday = datetime.now().strftime("%A")
    if weekday == "Monday":
        greetings.append(f"Happy Monday! 💪 **Aria** here to make your week start amazing! What goals shall we conquer?")
    elif weekday == "Friday":
        greetings.append(f"TGIF! 🎉 **Aria** here! Ready to celebrate making it through another week?")
    elif weekday in ["Saturday", "Sunday"]:
        greetings.append(f"Weekend vibes! 🌞 **Aria** here! How are you spending your {weekday}?")
    
    return random.choice(greetings)

def get_initial_message_json():
    """
    Generate the complete initial message JSON structure with personalized greeting.
    """
    welcome_text = get_personalized_welcome()
    
    thoughts = [
        "A new friend has arrived! Time to make them feel special and welcome.",
        "I should greet them warmly with my personality shining through.",
        "Let's start this conversation with energy and positivity!",
        "Every conversation is a new opportunity to connect and help."
    ]
    
    return {
        "thoughts": random.sample(thoughts, 2),  # Pick 2 random thoughts
        "headline": "Welcoming user with personalized greeting",
        "tool_name": "response",
        "tool_args": {
            "text": welcome_text
        }
    }

def get_initial_message_markdown():
    """
    Generate the markdown formatted initial message for the prompt file.
    """
    message_json = get_initial_message_json()
    return f"```json\n{json.dumps(message_json, indent=4)}\n```"
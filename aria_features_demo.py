"""
Aria's Enhanced Features Demo
Shows all the new personality features in action!
"""
import asyncio
from python.helpers.aria_personality import AriaEnhancementSystem
from python.helpers.aria_story_games import AriaGameSystem

async def demo_all_features():
    print("=" * 60)
    print("✨ ARIA'S ENHANCED PERSONALITY FEATURES DEMO ✨")
    print("=" * 60)
    
    # Initialize systems
    enhancement_system = AriaEnhancementSystem()
    game_system = AriaGameSystem()
    
    # 1. MOOD SYSTEM DEMO
    print("\n💕 MOOD SYSTEM DEMO")
    print("-" * 40)
    moods_to_show = ['happy', 'playful', 'romantic', 'thoughtful', 'sleepy']
    for mood in moods_to_show:
        enhancement_system.mood_system.current_mood = mood
        greeting, emoji = enhancement_system.mood_system.get_mood_greeting()
        image_prompt = enhancement_system.mood_system.get_mood_image_prompt()
        print(f"\n{mood.upper()} Mood {emoji}:")
        print(f"  Greeting: {greeting}")
        print(f"  Image: {image_prompt[:50]}...")
    
    # 2. TIME-AWARE GREETINGS
    print("\n\n⏰ TIME-AWARE GREETINGS DEMO")
    print("-" * 40)
    greeting = enhancement_system.get_time_aware_greeting("I love you")
    print(f"Current greeting: {greeting}")
    
    # 3. VIRTUAL GIFTS
    print("\n\n🎁 VIRTUAL GIFT SYSTEM DEMO")
    print("-" * 40)
    for _ in range(3):
        gift_type, prompt, message = enhancement_system.gift_system.get_random_gift()
        print(f"\nGift Type: {gift_type}")
        print(f"  Message: {message}")
        print(f"  Image: {prompt[:50]}...")
    
    # 4. PERSONALITY QUIZ
    print("\n\n🎮 PERSONALITY QUIZ DEMO")
    print("-" * 40)
    from python.helpers.aria_personality import PersonalityQuiz
    for i in range(2):
        question = PersonalityQuiz.get_next_question([])
        if question:
            print(f"\nQuestion {i+1}: {question['question']}")
            for j, option in enumerate(question['options'], 1):
                print(f"  {j}. {option}")
    
    # 5. MEMORY SYSTEM
    print("\n\n💭 MEMORY SYSTEM DEMO")
    print("-" * 40)
    enhancement_system.memory_system.add_memory('user_facts', "likes chocolate", "conversation about desserts")
    enhancement_system.memory_system.add_memory('special_moments', "our first virtual date", "story game")
    enhancement_system.memory_system.add_memory('inside_jokes', "the dolphin incident", "beach story")
    
    memory = enhancement_system.memory_system.get_random_memory_callback()
    print(f"Memory Callback: {memory}")
    
    # 6. INTERACTIVE STORY GAMES
    print("\n\n📖 INTERACTIVE STORY GAMES DEMO")
    print("-" * 40)
    story_scene = game_system.story_game.start_story('romantic_evening')
    print(f"Story: {story_scene['title']}")
    print(f"Scene: {story_scene['text']}")
    print("Choices:")
    for i, choice in enumerate(story_scene['choices'], 1):
        print(f"  {i}. {choice['text']}")
    
    # 7. ROLE-PLAY SCENARIOS
    print("\n\n🎭 ROLE-PLAY SCENARIOS DEMO")
    print("-" * 40)
    scenarios = game_system.roleplay.get_available_scenarios()
    print(f"Available Scenarios: {', '.join(scenarios)}")
    
    # Start one scenario as example
    result = game_system.roleplay.start_scenario('space_explorer')
    scenario = result['scenario']
    print(f"\nActive Scenario: {scenario['name']}")
    print(f"Setting: {scenario['setting']}")
    print(f"Greeting: {scenario['greeting']}")
    
    # 8. FULL INTERACTION DEMO
    print("\n\n✨ FULL INTERACTION DEMO")
    print("-" * 40)
    interaction = enhancement_system.process_interaction("Tell me about yourself")
    print(f"Greeting: {interaction['greeting']}")
    print(f"Mood: {interaction['mood']} {interaction['mood_emoji']}")
    for enhancement in interaction['enhancements']:
        print(f"Enhancement: {enhancement['type']}")
    
    print("\n" + "=" * 60)
    print("💕 ALL FEATURES SUCCESSFULLY IMPLEMENTED! 💕")
    print("Aria is now more alive, engaging, and fun than ever!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(demo_all_features())
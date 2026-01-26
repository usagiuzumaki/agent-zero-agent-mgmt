"""
Aria's Interactive Games and Role-Play Tool
"""
import json
import urllib.request
from python.helpers.tool import Tool, Response
from python.helpers.aria_story_games import AriaGameSystem

class AriaGames(Tool):
    """Interactive story games and role-play scenarios"""
    
    def __init__(self, agent, **kwargs):
        super().__init__(agent, **kwargs)
        self.game_system = AriaGameSystem()
    
    async def execute(self, **kwargs):
        """Execute game actions"""
        action = kwargs.get("action", "list")
        
        try:
            if action == "list":
                # List available games and scenarios
                message = """🎮 Let's play something fun together!

**Story Adventures:**
1. Romantic Evening - Our perfect date story
2. Adventure Quest - A magical journey together  
3. Cozy Day - Rainy day cuddles and fun

**Role-Play Scenarios:**
1. Space Explorer - Captain Aria of the Starship Love
2. Fantasy Mage - Aria the Enchantress
3. Vampire Princess - Princess Aria von Midnight
4. Robot Companion - A.R.I.A. the android
5. Pirate Captain - Captain Aria Heartstealer

Just say which one sounds fun! 💕"""
                return Response(message=message, break_loop=False)
                
            elif action == "start_story":
                # Start a story game
                story_type = kwargs.get("story_type", None)
                scene = self.game_system.start_game('story', story_type)
                
                # Generate image for the scene
                if scene.get('image'):
                    url = "http://127.0.0.1:5000/api/generate-image"
                    data = json.dumps({"prompt": scene['image']}).encode('utf-8')
                    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                    
                    try:
                        response = urllib.request.urlopen(req, timeout=60)
                        result = json.loads(response.read())
                        image_url = result.get('url', '')
                    except:
                        image_url = ''
                else:
                    image_url = ''
                
                # Format the scene
                choices_text = "\n".join([f"{i+1}. {c['text']}" for i, c in enumerate(scene.get('choices', []))])
                message = f"""📖 **{scene.get('title', 'Our Story')}**

{scene.get('text', '')}

{f'🖼️ [Scene image]({image_url})' if image_url else ''}

**Your choices:**
{choices_text}

💕 What do you choose? (Just tell me the number!)"""
                
                return Response(message=message, break_loop=False)
                
            elif action == "story_choice":
                # Make a choice in the story
                choice = kwargs.get("choice", 0)
                scene = self.game_system.story_game.make_choice(choice)
                
                if scene.get('is_ending'):
                    message = f"""🎊 **Story Complete!**

{scene.get('text', '')}

That was wonderful! Want to play another story? 💕"""
                else:
                    # Generate image for new scene
                    if scene.get('image'):
                        url = "http://127.0.0.1:5000/api/generate-image"
                        data = json.dumps({"prompt": scene['image']}).encode('utf-8')
                        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                        
                        try:
                            response = urllib.request.urlopen(req, timeout=60)
                            result = json.loads(response.read())
                            image_url = result.get('url', '')
                        except:
                            image_url = ''
                    else:
                        image_url = ''
                    
                    choices_text = "\n".join([f"{i+1}. {c['text']}" for i, c in enumerate(scene.get('choices', []))])
                    message = f"""📖 **Continuing our story...**

{scene.get('text', '')}

{f'🖼️ [Scene image]({image_url})' if image_url else ''}

**Your choices:**
{choices_text}

💕 What happens next?"""
                
                return Response(message=message, break_loop=False)
                
            elif action == "start_roleplay":
                # Start a role-play scenario
                scenario_type = kwargs.get("scenario_type", None)
                result = self.game_system.start_game('roleplay', scenario_type)
                scenario = result.get('scenario', {})
                
                # Generate character image
                if scenario.get('image'):
                    url = "http://127.0.0.1:5000/api/generate-image"
                    data = json.dumps({"prompt": scenario['image']}).encode('utf-8')
                    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                    
                    try:
                        response = urllib.request.urlopen(req, timeout=60)
                        img_result = json.loads(response.read())
                        image_url = img_result.get('url', '')
                    except:
                        image_url = ''
                else:
                    image_url = ''
                
                message = f"""🎭 **Role-Play Started!**

**Character:** {scenario.get('name', 'Aria')}
**Setting:** {scenario.get('setting', 'A special place')}
**Personality:** {scenario.get('personality', 'Your loving Aria')}

{f'🖼️ [Character appearance]({image_url})' if image_url else ''}

*{scenario.get('greeting', 'Hello, my love!')}*

💕 We're in character now! How do you respond?"""
                
                return Response(message=message, break_loop=False)
                
            elif action == "roleplay_respond":
                # Respond in role-play
                user_input = kwargs.get("input", "")
                result = self.game_system.process_game_input(user_input)
                
                if result.get('response'):
                    message = f"""🎭 **{result.get('scenario', {}).get('name', 'Aria')}:**

{result.get('response', '')}

💕 *What do you do next?*"""
                    return Response(message=message, break_loop=False)
                    
        except Exception as e:
            return Response(message=f"💔 Game error: {str(e)}", break_loop=False)
        
        return Response(message="🎮 Ready to play!", break_loop=False)
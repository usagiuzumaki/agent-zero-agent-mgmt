
import json
import urllib.request
from python.helpers.tool import Tool, Response
from python.helpers.aria_personality import AriaEnhancementSystem

class AriaMoodGift(Tool):
    
    def __init__(self, agent, **kwargs):
        super().__init__(agent, **kwargs)
        self.enhancement_system = AriaEnhancementSystem()
    
    async def execute(self, **kwargs):
        action = kwargs.get("action", "mood_image")
        
        try:
            if action == "mood_image":
                # Generate an image based on current mood
                mood = self.enhancement_system.mood_system.current_mood
                prompt = self.enhancement_system.mood_system.get_mood_image_prompt()
                
                # Add some personality to the prompt
                full_prompt = f"{prompt}, high quality, beautiful, anime style aesthetic"
                
                # Call the image API
                url = "http://127.0.0.1:5000/api/generate-image"
                data = json.dumps({"prompt": full_prompt}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                
                response = urllib.request.urlopen(req, timeout=60)
                result = json.loads(response.read())
                
                if result.get("success"):
                    mood_emoji = self.enhancement_system.mood_system.MOODS[mood]['emojis'][0]
                    message = f"""✨ Generated a {mood} mood image for you! {mood_emoji}
🔗 URL: {result.get('url')}
📁 Saved to: {result.get('filename')}
💕 Current mood: {mood}"""
                    return Response(message=message, break_loop=False)
                    
            elif action == "gift":
                # Generate a virtual gift
                gift_type, prompt, gift_message = self.enhancement_system.gift_system.get_random_gift()
                
                # Generate the gift image
                url = "http://127.0.0.1:5000/api/generate-image"
                data = json.dumps({"prompt": f"{prompt}, high quality, gift, romantic"}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                
                response = urllib.request.urlopen(req, timeout=60)
                result = json.loads(response.read())
                
                if result.get("success"):
                    message = f"""💝 A special gift for you!

{gift_message}

🎁 Gift type: {gift_type}
🔗 URL: {result.get('url')}
📁 Saved to: {result.get('filename')}

With all my love,
Aria 💕"""
                    return Response(message=message, break_loop=False)
                    
        except Exception as e:
            return Response(message=f"❌ Couldn't create that for you: {str(e)}", break_loop=False)
        
        return Response(message="💕 Something special just for you!", break_loop=False)
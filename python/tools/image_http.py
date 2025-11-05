"""
Simplified image generation tool using direct HTTP API
"""
import urllib.request
import json
from python.helpers.tool import Tool, Response

class image_generation(Tool):
    """Generate images using direct HTTP API"""
    
    async def execute(self, **kwargs):
        """Generate an image by calling the local API endpoint"""
        import urllib.request
        import json
        
        prompt = kwargs.get("prompt", "")
        if not prompt:
            return Response(message="Please provide a prompt for the image", break_loop=False)
        
        # Call local API endpoint
        url = "http://127.0.0.1:5000/api/generate-image"
        data = json.dumps({"prompt": prompt}).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            response = urllib.request.urlopen(req, timeout=60)
            result = json.loads(response.read())
            
            if result.get("success"):
                message = f"""✅ Image generated successfully!
🔗 URL: {result.get('url')}
📁 Saved to: {result.get('filename')}"""
                return Response(message=message, break_loop=False)
            else:
                return Response(message=f"❌ Failed: {result.get('error')}", break_loop=False)
                
        except Exception as e:
            return Response(message=f"❌ Error generating image: {str(e)}", break_loop=False)
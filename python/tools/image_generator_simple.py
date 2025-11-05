#!/usr/bin/env python3
"""
Simplified image generation tool that bypasses import issues
"""
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

def generate_image_direct(prompt, output_dir="outputs"):
    """Generate image using direct HTTP requests to Replicate API"""
    
    # API configuration
    api_token = os.getenv("REPLICATE_API_TOKEN", "r8_IamCkTsQVQVc4C98QySJXkub1HXoIQn4YT5E9")
    model_version = "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
    
    # Create prediction
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps({
        "version": model_version,
        "input": {
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, bad anatomy",
            "width": 1024,
            "height": 1024,
            "num_outputs": 1,
            "scheduler": "K_EULER",
            "num_inference_steps": 25,
            "guidance_scale": 7.5
        }
    }).encode()
    
    try:
        # Create prediction
        req = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(req)
        prediction = json.loads(response.read())
        
        prediction_id = prediction["id"]
        
        # Poll for completion
        import time
        max_attempts = 60
        for attempt in range(max_attempts):
            status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
            req = urllib.request.Request(status_url, headers={"Authorization": f"Bearer {api_token}"})
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            
            if result["status"] == "succeeded":
                # Download image
                image_url = result["output"][0]
                os.makedirs(output_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{output_dir}/image_{timestamp}.png"
                
                # Download with urllib
                urllib.request.urlretrieve(image_url, filename)
                
                return {
                    "success": True,
                    "filename": filename,
                    "url": image_url,
                    "message": f"✅ Image generated successfully!\n📁 Saved to: {filename}\n🔗 URL: {image_url}"
                }
            elif result["status"] == "failed":
                return {
                    "success": False,
                    "message": f"❌ Generation failed: {result.get('error', 'Unknown error')}"
                }
            
            time.sleep(2)
        
        return {
            "success": False,
            "message": "❌ Timeout waiting for image generation"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {str(e)}"
        }

if __name__ == "__main__":
    # Test generation
    result = generate_image_direct("a beautiful magical forest with glowing mushrooms")
    print(json.dumps(result, indent=2))
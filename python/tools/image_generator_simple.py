#!/usr/bin/env python3
"""
Simplified image generation tool that bypasses import issues
"""
import os
import json
import time
from datetime import datetime
import requests

def generate_image_direct(prompt, output_dir="outputs"):
    """Generate image using direct HTTP requests to Replicate API"""
    
    # API configuration
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        return {
            "success": False,
            "message": "❌ REPLICATE_API_TOKEN not configured"
        }

    model_version = "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
    
    # Create prediction
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
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
    }
    
    try:
        # Create prediction
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        prediction = response.json()
        
        prediction_id = prediction["id"]
        
        # Poll for completion
        max_attempts = 60
        for attempt in range(max_attempts):
            status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"

            response = requests.get(status_url, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result["status"] == "succeeded":
                # Download image
                image_url = result["output"][0]
                os.makedirs(output_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{output_dir}/image_{timestamp}.png"
                
                # Download with requests
                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(img_response.content)
                
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

"""
Direct image generation API endpoint for Aria Bot
"""
from flask import jsonify, request
import os
import json
import urllib.request
import time
from datetime import datetime

def register_image_routes(app):
    """Register image generation routes with the Flask app"""
    
    @app.route("/api/generate-image", methods=["POST"])
    def generate_image():
        """Direct API endpoint for image generation"""
        try:
            data = request.get_json()
            prompt = data.get("prompt", "")
            
            if not prompt:
                return jsonify({"error": "No prompt provided"}), 400
            
            # API configuration
            api_token = os.getenv("REPLICATE_API_TOKEN")
            if not api_token:
                return jsonify({"error": "REPLICATE_API_TOKEN not set"}), 500

            model_version = "39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
            
            # Create prediction
            url = "https://api.replicate.com/v1/predictions"
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            
            payload = json.dumps({
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
            
            # Create prediction
            req = urllib.request.Request(url, data=payload, headers=headers)
            response = urllib.request.urlopen(req, timeout=30)
            prediction = json.loads(response.read())
            
            prediction_id = prediction["id"]
            
            # Poll for completion (max 30 seconds)
            for attempt in range(15):
                status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
                req = urllib.request.Request(status_url, headers={"Authorization": f"Bearer {api_token}"})
                response = urllib.request.urlopen(req, timeout=10)
                result = json.loads(response.read())
                
                if result["status"] == "succeeded":
                    image_url = result["output"][0]
                    
                    # Download and save image
                    os.makedirs("outputs", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"outputs/image_{timestamp}.png"
                    
                    urllib.request.urlretrieve(image_url, filename)
                    
                    return jsonify({
                        "success": True,
                        "url": image_url,
                        "filename": filename,
                        "message": f"✅ Image generated successfully!"
                    })
                    
                elif result["status"] == "failed":
                    return jsonify({
                        "success": False,
                        "error": result.get("error", "Generation failed")
                    }), 500
                
                time.sleep(2)
            
            return jsonify({
                "success": False,
                "error": "Timeout waiting for image generation"
            }), 504
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
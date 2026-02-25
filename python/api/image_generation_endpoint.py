"""
Direct image generation API endpoint for Aria - AI Creative Companion
"""
from flask import jsonify, request
import os
import json
import time
from datetime import datetime
import requests

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
                return jsonify({"error": "REPLICATE_API_TOKEN not configured"}), 500

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
            
            # Create prediction
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                prediction = response.json()
            except requests.exceptions.RequestException as e:
                return jsonify({"success": False, "error": f"Replicate API error: {str(e)}"}), 500

            prediction_id = prediction.get("id")
            if not prediction_id:
                return jsonify({"success": False, "error": "Invalid response from Replicate"}), 500
            
            # Poll for completion (max 30 seconds)
            start_time = time.time()
            while time.time() - start_time < 30:
                status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
                try:
                    response = requests.get(status_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    result = response.json()
                except requests.exceptions.RequestException as e:
                     return jsonify({"success": False, "error": f"Replicate polling error: {str(e)}"}), 500
                
                status = result.get("status")
                if status == "succeeded":
                    output = result.get("output")
                    if not output or not isinstance(output, list):
                         return jsonify({"success": False, "error": "No output in response"}), 500

                    image_url = output[0]
                    
                    # Download and save image
                    os.makedirs("outputs", exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"outputs/image_{timestamp}.png"
                    
                    try:
                        img_response = requests.get(image_url, timeout=30)
                        img_response.raise_for_status()
                        with open(filename, "wb") as f:
                            f.write(img_response.content)
                    except Exception as e:
                         return jsonify({"success": False, "error": f"Failed to download image: {str(e)}"}), 500
                    
                    return jsonify({
                        "success": True,
                        "url": image_url,
                        "filename": filename,
                        "message": f"✅ Image generated successfully!"
                    })
                    
                elif status == "failed":
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

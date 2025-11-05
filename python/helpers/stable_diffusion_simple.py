"""
Simplified Stable Diffusion wrapper that avoids import hangs
"""
import os
import json
import subprocess
import sys

def generate_image(prompt, output_dir="outputs", **kwargs):
    """Generate image using simple subprocess call to avoid import hangs"""
    
    # Build the command
    script = """
import os
import sys
import json
import urllib.request
import time
from datetime import datetime

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
        "prompt": %s,
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
            os.makedirs(%s, exist_ok=True)
            timestamp = datetime.now().strftime("%%Y%%m%%d_%%H%%M%%S")
            filename = f"%s/sd_image_{timestamp}.png"
            
            # Download image
            urllib.request.urlretrieve(image_url, filename)
            print(filename)
            sys.exit(0)
        elif result["status"] == "failed":
            print("ERROR: " + result.get("error", "Unknown error"))
            sys.exit(1)
        
        time.sleep(2)
    
    print("ERROR: Timeout waiting for image")
    sys.exit(1)
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    sys.exit(1)
""" % (json.dumps(prompt), json.dumps(output_dir), output_dir)
    
    # Execute the script
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "REPLICATE_API_TOKEN": os.getenv("REPLICATE_API_TOKEN", "r8_IamCkTsQVQVc4C98QySJXkub1HXoIQn4YT5E9")}
        )
        
        if result.returncode == 0:
            filename = result.stdout.strip()
            if filename and os.path.exists(filename):
                return filename
            else:
                raise RuntimeError(f"Image generation succeeded but file not found: {filename}")
        else:
            error_msg = result.stdout.strip() if result.stdout else result.stderr.strip()
            if error_msg.startswith("ERROR: "):
                raise RuntimeError(error_msg[7:])
            else:
                raise RuntimeError(f"Image generation failed: {error_msg}")
                
    except subprocess.TimeoutExpired:
        raise RuntimeError("Image generation timed out after 60 seconds")
    except Exception as e:
        raise RuntimeError(f"Image generation failed: {str(e)}")
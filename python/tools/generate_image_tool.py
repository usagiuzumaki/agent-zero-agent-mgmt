import os
import json
import requests
from typing import Dict, Any
from python.helpers.tool import Tool, Response

try:
    import replicate
except ImportError:
    replicate = None

class GenerateImage(Tool):
    """
    Generate images using Replicate API (Stable Diffusion XL)
    """
    
    def execute(self, prompt: str = "", **kwargs) -> Response:
        """
        Generate an image from a text prompt using Replicate API
        
        Args:
            prompt: Text description of the image to generate
            **kwargs: Additional parameters for image generation
        """
        if not prompt:
            return Response(
                message="❌ Please provide a prompt for image generation!",
                break_loop=False
            )
        
        if replicate is None:
             return Response(
                message="❌ 'replicate' library is not installed.",
                break_loop=False
            )

        # Set the API token directly from environment
        api_token = os.getenv("REPLICATE_API_TOKEN")
        if not api_token:
            return Response(
                message="❌ REPLICATE_API_TOKEN not configured. Please set your Replicate API token.",
                break_loop=False
            )
        
        os.environ["REPLICATE_API_TOKEN"] = api_token
        
        # SDXL model with proper version hash
        model = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
        
        # Default parameters for high quality generation
        params = {
            "prompt": prompt,
            "negative_prompt": kwargs.get("negative_prompt", "low quality, blurry, bad anatomy, ugly"),
            "width": kwargs.get("width", 1024),
            "height": kwargs.get("height", 1024),
            "num_outputs": 1,
            "scheduler": "K_EULER",
            "num_inference_steps": kwargs.get("steps", 25),
            "guidance_scale": kwargs.get("guidance", 7.5),
            "prompt_strength": 0.8,
            "refine": "expert_ensemble_refiner",
            "high_noise_frac": 0.8
        }
        
        try:
            # Run the model
            self.agent.context.log.log(type="info", content=f"🎨 Generating image with prompt: {prompt[:100]}...")
            
            output = replicate.run(model, input=params)
            
            if output and len(output) > 0:
                image_url = output[0]
                
                # Download and save the image
                response = requests.get(image_url, timeout=30)
                if response.status_code == 200:
                    # Create directory if it doesn't exist
                    os.makedirs("generated_images", exist_ok=True)
                    
                    # Save with timestamp
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"generated_images/image_{timestamp}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    
                    message = f"""✅ Image generated successfully!
🔗 URL: {image_url}
💾 Saved to: {filename}
📏 Size: {len(response.content) / 1024:.1f} KB
🎨 Prompt: {prompt[:100]}..."""
                    
                    return Response(
                        message=message,
                        break_loop=False
                    )
                else:
                    return Response(
                        message=f"❌ Failed to download image from URL: {image_url}",
                        break_loop=False
                    )
            else:
                return Response(
                    message="❌ No image generated - Replicate returned empty response",
                    break_loop=False
                )
                
        except Exception as e:
            error_msg = str(e)
            self.agent.context.log.log(type="error", content=f"Image generation error: {error_msg}")
            
            return Response(
                message=f"❌ Image generation failed: {error_msg}",
                break_loop=False
            )

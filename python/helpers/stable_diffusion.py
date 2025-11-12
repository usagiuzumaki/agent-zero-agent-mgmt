import os
import uuid
from pathlib import Path
from typing import Optional

try:  # pragma: no cover - optional dependency
    import torch
except Exception:  # pragma: no cover
    torch = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from diffusers import StableDiffusionPipeline
except Exception:  # pragma: no cover
    StableDiffusionPipeline = None  # type: ignore

try:  # pragma: no cover - optional dependency
    import replicate
except Exception:  # pragma: no cover
    replicate = None  # type: ignore

# Default to a hyper-realistic model capable of NSFW generation.
# The model can be overridden via the ``SD_MODEL_NAME`` environment variable.
_MODEL_ID = os.getenv("SD_MODEL_NAME", "SG161222/Realistic_Vision_V5.1_noVAE")
_MODEL_PATH = os.getenv("SD_MODEL_PATH")
_pipe: Optional["StableDiffusionPipeline"] = None

# Replicate configuration
_REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
_REPLICATE_MODEL = os.getenv("REPLICATE_SD_MODEL", "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b")


def _generate_image_via_replicate(
    prompt: str,
    *,
    output_dir: str = "outputs",
    seed: int | None = None,
    steps: int = 30,
    guidance_scale: float = 7.5,
    negative_prompt: str | None = None,
    width: int | None = None,
    height: int | None = None,
) -> str:
    """Generate image using Replicate API."""
    if replicate is None:
        raise RuntimeError("Replicate SDK not installed. Install with: pip install replicate")
    
    # Check for token again at runtime
    token = _REPLICATE_API_TOKEN or os.getenv("REPLICATE_API_TOKEN")
    if not token:
        raise RuntimeError(
            "REPLICATE_API_TOKEN environment variable not set. "
            "Get your API token from https://replicate.com/account/api-tokens"
        )
    
    # Configure Replicate client with the found token
    os.environ["REPLICATE_API_TOKEN"] = token
    
    # Prepare input parameters
    input_params = {
        "prompt": prompt,
        "num_inference_steps": steps,
        "guidance_scale": guidance_scale,
    }

    if negative_prompt:
        input_params["negative_prompt"] = negative_prompt
    if width:
        input_params["width"] = width
    if height:
        input_params["height"] = height

    if seed is not None:
        input_params["seed"] = seed
    
    # Run the model
    output = replicate.run(_REPLICATE_MODEL, input=input_params)
    
    # Download the generated image
    import httpx
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"sd_image_{uuid.uuid4().hex}.png")
    
    # Handle different output types from Replicate
    if isinstance(output, list):
        image_output = output[0]
    else:
        image_output = output
    
    # Check if it's a FileOutput object or a URL string
    if hasattr(image_output, 'url'):
        # It's a FileOutput object, get the URL
        image_url = str(image_output.url) if hasattr(image_output, 'url') else str(image_output)
    else:
        # It's already a URL string
        image_url = str(image_output)
    
    # Download the image
    response = httpx.get(image_url)
    response.raise_for_status()
    
    with open(filename, "wb") as f:
        f.write(response.content)
    
    return filename


def _load_pipeline() -> "StableDiffusionPipeline":
    global _pipe
    if _pipe is None:
        if StableDiffusionPipeline is None or torch is None:
            raise RuntimeError("Stable Diffusion dependencies missing.")
        device = "cuda" if torch.cuda and torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        if _MODEL_PATH:
            model_path = Path(_MODEL_PATH).expanduser()
            if model_path.is_file():
                _pipe = StableDiffusionPipeline.from_single_file(
                    str(model_path),
                    torch_dtype=dtype,
                    safety_checker=None,
                    feature_extractor=None,
                    requires_safety_checker=False,
                )
            else:
                _pipe = StableDiffusionPipeline.from_pretrained(
                    str(model_path),
                    torch_dtype=dtype,
                    safety_checker=None,
                    feature_extractor=None,
                    requires_safety_checker=False,
                )
        else:
            _pipe = StableDiffusionPipeline.from_pretrained(
                _MODEL_ID,
                torch_dtype=dtype,
                safety_checker=None,
                feature_extractor=None,
                requires_safety_checker=False,
            )
        _pipe.to(device)
        # Ensure safety checker is disabled for unrestricted generation
        if hasattr(_pipe, "safety_checker"):
            _pipe.safety_checker = None
    return _pipe


def generate_image(
    prompt: str,
    *,
    output_dir: str = "outputs",
    seed: int | None = None,
    steps: int = 30,
    guidance_scale: float = 7.5,
    negative_prompt: str | None = None,
    width: int | None = None,
    height: int | None = None,
) -> str:
    """Generate an image from ``prompt`` using Stable Diffusion.
    
    This function supports two modes:
    1. Replicate API (cloud-based): If REPLICATE_API_TOKEN is set
    2. Local model: If torch and diffusers are installed
    
    The Replicate API is preferred when available as it doesn't require
    heavy ML dependencies and works better in resource-constrained environments.

    Args:
        prompt: Text prompt describing the image.
        output_dir: Directory where the image will be saved.
        seed: Optional random seed for reproducible results.
        steps: Number of inference steps.
        guidance_scale: CFG guidance scale.

    Returns:
        Path to the generated image file.
        
    Raises:
        RuntimeError: If neither Replicate API token nor local dependencies are available.
    """
    # Check for Replicate API token at runtime (not at module load time)
    current_replicate_token = os.getenv("REPLICATE_API_TOKEN")
    
    # Try using simple subprocess method first (avoids import hangs)
    if current_replicate_token:
        try:
            # Use the simple subprocess method that avoids import hangs
            from python.helpers.stable_diffusion_simple import generate_image as generate_simple

            return generate_simple(
                prompt,
                output_dir=output_dir,
                steps=steps,
                guidance_scale=guidance_scale,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                seed=seed,
                model_version=_REPLICATE_MODEL,
            )
        except Exception as e:
            # Fall back to the original method if simple method fails
            pass

    # Prioritize Replicate API if available
    if current_replicate_token and replicate is not None:
        # Update the module-level variable
        global _REPLICATE_API_TOKEN
        _REPLICATE_API_TOKEN = current_replicate_token
        return _generate_image_via_replicate(
            prompt,
            output_dir=output_dir,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
        )

    # Fall back to local generation
    pipe = _load_pipeline()
    generator = None
    if seed is not None and torch is not None:
        generator = torch.Generator(device=pipe.device).manual_seed(seed)
    run_kwargs = {
        "num_inference_steps": steps,
        "guidance_scale": guidance_scale,
        "generator": generator,
    }
    if negative_prompt:
        run_kwargs["negative_prompt"] = negative_prompt
    if width:
        run_kwargs["width"] = width
    if height:
        run_kwargs["height"] = height
    result = pipe(prompt, **run_kwargs)
    image = result.images[0]
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"sd_image_{uuid.uuid4().hex}.png")
    image.save(filename)
    return filename

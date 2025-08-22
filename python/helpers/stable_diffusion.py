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

_MODEL_ID = os.getenv("SD_MODEL_NAME", "runwayml/stable-diffusion-v1-5")
_MODEL_PATH = os.getenv("SD_MODEL_PATH")
_pipe: Optional["StableDiffusionPipeline"] = None


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
                _pipe = StableDiffusionPipeline.from_single_file(str(model_path), torch_dtype=dtype)
            else:
                _pipe = StableDiffusionPipeline.from_pretrained(str(model_path), torch_dtype=dtype)
        else:
            _pipe = StableDiffusionPipeline.from_pretrained(_MODEL_ID, torch_dtype=dtype)
        _pipe.to(device)
    return _pipe


def generate_image(
    prompt: str,
    *,
    output_dir: str = "outputs",
    seed: int | None = None,
    steps: int = 30,
    guidance_scale: float = 7.5,
) -> str:
    """Generate an image from ``prompt`` using Stable Diffusion.

    Args:
        prompt: Text prompt describing the image.
        output_dir: Directory where the image will be saved.
        seed: Optional random seed for reproducible results.
        steps: Number of inference steps.
        guidance_scale: CFG guidance scale.

    Returns:
        Path to the generated image file.
    """
    pipe = _load_pipeline()
    generator = None
    if seed is not None and torch is not None:
        generator = torch.Generator(device=pipe.device).manual_seed(seed)
    result = pipe(prompt, num_inference_steps=steps, guidance_scale=guidance_scale, generator=generator)
    image = result.images[0]
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"sd_image_{uuid.uuid4().hex}.png")
    image.save(filename)
    return filename

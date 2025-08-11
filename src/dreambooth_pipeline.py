import os, logging, subprocess, sys, pathlib, requests, hashlib, shutil
try:
    import torch
except Exception as e:  # pragma: no cover - optional dependency
    logging.warning("Torch not available: %s", e)
    torch = None
from PIL import Image
try:
    from diffusers import StableDiffusionPipeline
except Exception as e:  # pragma: no cover - optional dependency
    logging.warning("Diffusers library not available: %s", e)
    StableDiffusionPipeline = None

MODEL_NAME = os.getenv("SD_MODEL_NAME", "runwayml/stable-diffusion-v1-5")
OUTPUT_DIR = os.getenv("DB_OUTPUT_DIR", "outputs/dreambooth_model")
INSTANCE_TOKEN = os.getenv("DB_INSTANCE_TOKEN", "<egirl>")
CLASS_TOKEN = os.getenv("DB_CLASS_TOKEN", "woman")

HF_DREAMBOOTH_SCRIPT_URL = "https://raw.githubusercontent.com/huggingface/diffusers/main/examples/dreambooth/train_dreambooth_lora.py"

def _download_file(url: str, dest: str):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(dest, "wb") as f:
        f.write(r.content)

def train_dreambooth(instance_data_dir: str, class_data_dir: str = None, max_steps: int = 400):
    """Launch official Diffusers DreamBooth LoRA training script via Accelerate."""
    os.makedirs("scripts", exist_ok=True)
    script_path = "scripts/train_dreambooth_lora.py"
    if not os.path.exists(script_path):
        logging.info("Downloading DreamBooth training script...")
        _download_file(HF_DREAMBOOTH_SCRIPT_URL, script_path)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Basic command; customize as needed
    cmd = [
        sys.executable, "-m", "accelerate", "launch", script_path,
        "--pretrained_model_name_or_path", MODEL_NAME,
        "--instance_data_dir", instance_data_dir,
        "--output_dir", OUTPUT_DIR,
        "--instance_prompt", f"{INSTANCE_TOKEN} {CLASS_TOKEN}",
        "--resolution", "512",
        "--train_batch_size", "1",
        "--gradient_accumulation_steps", "1",
        "--learning_rate", "1e-4",
        "--lr_scheduler", "constant",
        "--max_train_steps", str(max_steps),
        "--checkpointing_steps", "200",
        "--mixed_precision", "no"
    ]
    if class_data_dir:
        cmd += ["--class_data_dir", class_data_dir, "--with_prior_preservation", "--prior_loss_weight", "1.0"]

    logging.info("Starting DreamBooth training via accelerate...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("DreamBooth training failed.")
    logging.info("DreamBooth training completed.")

_persona_pipe = None
def load_persona_pipeline(model_dir: str = OUTPUT_DIR):
    global _persona_pipe
    if StableDiffusionPipeline is None or torch is None:
        raise RuntimeError("Stable Diffusion dependencies missing.")
    _persona_pipe = StableDiffusionPipeline.from_pretrained(model_dir, torch_dtype=torch.float32)
    device = "cuda" if torch.cuda and torch.cuda.is_available() else "cpu"
    _persona_pipe.to(device)
    return _persona_pipe

def generate_persona_image(prompt: str, output_path: str = "outputs/sample_image.png", seed: int = 42):
    global _persona_pipe
    if _persona_pipe is None:
        load_persona_pipeline()
    generator = torch.Generator(device=_persona_pipe.device).manual_seed(seed)
    image = _persona_pipe(prompt, num_inference_steps=40, generator=generator).images[0]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path)
    return output_path

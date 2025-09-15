"""Utilities for guiding the e-girl agent through the Stable Diffusion Colab."""

from __future__ import annotations

from textwrap import dedent
from typing import Iterable

COLAB_NOTEBOOK_ID = "1GsQ5_t3BRl4ibRgMK7ffgcoVKUSGC4Jl"
COLAB_NOTEBOOK_URL = (
    f"https://colab.research.google.com/drive/{COLAB_NOTEBOOK_ID}?usp=sharing"
)

# Paths that the shared Colab notebook mounts inside Google Drive.
DRIVE_BASE_PATH = "/content/drive/MyDrive/SD"
MODELS_DIR = f"{DRIVE_BASE_PATH}/models/Stable-diffusion"
VAE_DIR = f"{DRIVE_BASE_PATH}/models/VAE"
LORA_DIR = f"{DRIVE_BASE_PATH}/models/Lora"
EMBEDDINGS_DIR = f"{DRIVE_BASE_PATH}/embeddings"
OUTPUTS_DIR = f"{DRIVE_BASE_PATH}/outputs"
RAW_DATASET_DIR = f"{DRIVE_BASE_PATH}/datasets/egirl_blonde/raw"
PREP_DATASET_DIR = f"{DRIVE_BASE_PATH}/datasets/egirl_blonde/prepared"

DEFAULT_LAUNCH_FLAGS = (
    "--medvram --opt-sdp-no-mem-attention --no-half-vae --theme dark "
    "--gradio-queue --share"
)


def _numbered_steps(steps: Iterable[str]) -> str:
    return "\n".join(f"{idx}. {step}" for idx, step in enumerate(steps, start=1))


def get_overview() -> str:
    """Return a concise description of the Colab workspace."""

    summary = dedent(
        f"""
        Google Colab notebook: {COLAB_NOTEBOOK_URL}

        Workspace layout on Google Drive:
        • Base directory: {DRIVE_BASE_PATH}
        • Stable Diffusion checkpoints: {MODELS_DIR}
        • VAE files: {VAE_DIR}
        • LoRA weights: {LORA_DIR}
        • Textual inversion embeddings: {EMBEDDINGS_DIR}
        • Generated outputs (mirrored from the WebUI): {OUTPUTS_DIR}
        • Optional DreamBooth dataset staging:
          - Raw assets folder: {RAW_DATASET_DIR}
          - Prepared 512x768 set with BLIP captions: {PREP_DATASET_DIR}

        Notebook cell overview:
        1. Mounts Google Drive and ensures the folder structure exists.
        2. Installs Python 3.10 and modern packaging tools required by AUTOMATIC1111.
        3. Clones the AUTOMATIC1111/stable-diffusion-webui repository into /content.
        4. Symlinks the WebUI's models, embeddings, and outputs folders to Drive.
        5. Installs the CUDA 12.1 build of PyTorch plus supporting libraries.
        6. Launches the WebUI with the flags: {DEFAULT_LAUNCH_FLAGS}.
        7. (Optional) Prepares a DreamBooth-ready dataset with BLIP captions.
        """
    ).strip()

    return summary


def build_workflow(
    prompt: str | None = None,
    *,
    negative_prompt: str | None = None,
    steps: int | None = None,
    guidance: float | None = None,
    num_images: int | None = None,
    scheduler: str | None = None,
) -> str:
    """Render a full step-by-step workflow for running the Colab notebook."""

    prompt_section: list[str] = []
    if prompt:
        prompt_section.append(f"• Positive prompt: `{prompt}`")
    if negative_prompt:
        prompt_section.append(f"• Negative prompt: `{negative_prompt}`")
    if steps is not None:
        prompt_section.append(f"• Sampling steps: {steps}")
    if guidance is not None:
        prompt_section.append(f"• CFG guidance scale: {guidance}")
    if num_images is not None:
        prompt_section.append(f"• Batch count: {num_images}")
    if scheduler:
        prompt_section.append(f"• Sampler/scheduler: {scheduler}")

    if prompt_section:
        prompt_section_text = "\n".join(prompt_section)
        prompt_section_text = (
            "Suggested WebUI settings based on the request:\n" + prompt_section_text
        )
    else:
        prompt_section_text = (
            "Customize your prompts inside the AUTOMATIC1111 interface after it opens."
        )

    steps_text = _numbered_steps(
        [
            (
                "Open the shared notebook and ensure the runtime uses a GPU: go to"
                " Runtime → Change runtime type, pick `T4` under GPU, click Save,"
                " then press Connect."
            ),
            (
                "Run the first cell to mount Google Drive at `/content/drive` and"
                " create the Stable Diffusion workspace directories. Approve the"
                " OAuth dialog so the notebook can write to Drive."
            ),
            (
                "Execute the environment bootstrap cell that installs Python 3.10"
                " and pip. This takes a few minutes and only needs to run once per"
                " fresh runtime."
            ),
            (
                "Run the git clone cell to download"
                " `AUTOMATIC1111/stable-diffusion-webui` into `/content/sd-webui`."
            ),
            (
                "Execute the symlink cell so that models, VAEs, LoRAs, embeddings,"
                " and outputs inside the WebUI point at your Drive folders."
            ),
            (
                "Install the CUDA 12.1 build of PyTorch, torchmetrics,"
                " pytorch-lightning, and optional OpenCV support."
            ),
            (
                "Launch the WebUI with `launch.py` using the flags"
                f" `{DEFAULT_LAUNCH_FLAGS}`. Wait until the log prints"
                " `Running on public URL: https://...` (or `https://127.0.0.1`"
                " when using Colab's UI preview)."
            ),
            (
                "Open the provided public Gradio link in a new browser tab."
                " Inside the txt2img tab, paste your prompt(s) and adjust"
                " sampling parameters as needed."
            ),
            (
                "Generate images. Every render is written to"
                f" `{OUTPUTS_DIR}` on Google Drive (mirrored under"
                " `/content/sd-webui/outputs`). Keep the WebUI tab open"
                " until generation finishes."
            ),
            (
                "When you are done, use Runtime → Disconnect and delete runtime"
                " to clean up Colab resources."
            ),
        ]
    )

    download_section = dedent(
        f"""
        Downloading your results:
        • Option A – Google Drive: open *My Drive → SD → outputs* to browse and
          download the generated images directly from Drive.
        • Option B – Direct download from the runtime:
          ```python
          from google.colab import files
          files.download('{OUTPUTS_DIR}/<relative_path_to_image>.png')
          ```
        • Option C – Grab the entire outputs folder as a zip inside Colab:
          ```python
          !zip -r /content/sd_outputs.zip '{OUTPUTS_DIR}'
          from google.colab import files
          files.download('/content/sd_outputs.zip')
          ```
        """
    ).strip()

    optional_section = dedent(
        f"""
        Optional dataset preparation:
        • The final cell in the notebook can resize images from
          `{RAW_DATASET_DIR}` to 512×768 PNGs, and (when `use_blip = True`) create
          BLIP captions alongside them in `{PREP_DATASET_DIR}`. Run it only if you
          are preparing DreamBooth or LoRA training data."
        """
    ).strip()

    return (
        dedent(
            f"""
            Stable Diffusion WebUI workflow on Colab

            Notebook link: {COLAB_NOTEBOOK_URL}

            {steps_text}

            {prompt_section_text}

            {download_section}

            {optional_section}
            """
        )
        .strip()
    )


def build_download_instructions(
    filename: str | None = None,
    *,
    as_zip: bool = False,
) -> str:
    """Return specific instructions for downloading generated assets."""

    if filename:
        target_path = f"{OUTPUTS_DIR}/{filename.lstrip('/')}"
    else:
        target_path = OUTPUTS_DIR

    if as_zip:
        command = dedent(
            f"""
            !zip -r /content/sd_outputs.zip '{target_path}'
            from google.colab import files
            files.download('/content/sd_outputs.zip')
            """
        ).strip()
        description = (
            "Zip the requested folder or file inside the runtime, then trigger a"
            " browser download."
        )
    else:
        command = dedent(
            f"""
            from google.colab import files
            files.download('{target_path}')
            """
        ).strip()
        description = (
            "Download the specific file directly. If you provided a folder,"
            " enable `as_zip` to bundle it first."
        )

    return (
        dedent(
            f"""
            Direct download helper for the Stable Diffusion Colab

            Target on Drive: {target_path}

            {description}

            ```python
            {command}
            ```

            Remember that every render is also available via Google Drive at
            {OUTPUTS_DIR}.
            """
        )
        .strip()
    )


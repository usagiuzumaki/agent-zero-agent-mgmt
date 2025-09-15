# Stable Diffusion Colab Pipeline

Use the shared Google Colab notebook to launch AUTOMATIC1111's Stable Diffusion WebUI with persistent storage in Google Drive.

## Notebook & Workspace
- **Notebook:** https://colab.research.google.com/drive/1GsQ5_t3BRl4ibRgMK7ffgcoVKUSGC4Jl?usp=sharing
- **Drive base folder:** `/content/drive/MyDrive/SD`
  - Checkpoints → `/models/Stable-diffusion`
  - VAEs → `/models/VAE`
  - LoRAs → `/models/Lora`
  - Embeddings → `/embeddings`
  - Generated images → `/outputs`
  - Optional dataset prep folders → `/datasets/egirl_blonde/`

## Cell-by-Cell Instructions
1. **Mount Drive / build folders** – approve the OAuth prompt; creates the directory structure above.
2. **Install Python 3.10** – installs Python 3.10, pip and packaging tools required for AUTOMATIC1111.
3. **Clone the repository** – clones `AUTOMATIC1111/stable-diffusion-webui` into `/content/sd-webui`.
4. **Symlink to Drive assets** – ensures checkpoints, embeddings and outputs point at Drive so they persist between runs.
5. **Install PyTorch CUDA 12.1 build** – installs `torch==2.1.2+cu121`, `torchvision==0.16.2+cu121`, matplotlib, torchmetrics, PyTorch Lightning, and OpenCV.
6. **Launch the WebUI** – runs `launch.py` with `--medvram --opt-sdp-no-mem-attention --no-half-vae --theme dark --gradio-queue --share`. Wait for the `Running on public URL: ...` log entry.
7. *(Optional)* **Dataset preparation** – resizes files from `/datasets/egirl_blonde/raw` to 512×768 PNGs and (when enabled) writes BLIP captions to `/datasets/egirl_blonde/prepared`.

## Generating Images
- Open the public Gradio link shown after the WebUI launches.
- In **txt2img**, paste your prompt, set the negative prompt, sampler, CFG scale, steps, and batch count.
- Click **Generate**; results land in `My Drive/SD/outputs/<date>` and remain persisted on Drive.

## Download Options
- **From Drive UI:** `My Drive → SD → outputs`.
- **From the runtime:**
  ```python
  from google.colab import files
  files.download('/content/drive/MyDrive/SD/outputs/<date>/<filename>.png')
  ```
- **Download everything as a zip:**
  ```python
  !zip -r /content/sd_outputs.zip /content/drive/MyDrive/SD/outputs
  from google.colab import files
  files.download('/content/sd_outputs.zip')
  ```

## Cleanup
- Choose **Runtime → Disconnect and delete runtime** when finished to release the GPU.


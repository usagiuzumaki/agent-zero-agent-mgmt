import os, logging
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

from dreambooth_pipeline import train_dreambooth, generate_persona_image
from instagram_integration import post_image, comment_on_hashtags
from video_generator import generate_video_from_image
from persona_engine import PersonaEngine
from stripe_integration import create_checkout_session

def main():
    # Train DreamBooth if output dir doesn't exist and training images are present
    out_dir = os.getenv("DB_OUTPUT_DIR", "outputs/dreambooth_model")
    img_dir = os.getenv("PERSONA_IMAGES_DIR", "training_images")
    if not os.path.exists(out_dir) and os.path.isdir(img_dir) and os.listdir(img_dir):
        logging.info("Starting DreamBooth training...")
        train_dreambooth(img_dir, max_steps=200)
    else:
        logging.info("Skipping DreamBooth training (model exists or no images).")

    # Generate persona image
    inst_tok = os.getenv("DB_INSTANCE_TOKEN", "<egirl>")
    cls_tok = os.getenv("DB_CLASS_TOKEN", "woman")
    prompt = f"a portrait of {inst_tok} {cls_tok} in a kawaii pastel outfit, smiling, soft light"
    img_path = generate_persona_image(prompt, output_path="outputs/demo_persona.png")
    logging.info(f"Generated image at {img_path}")

    # Post to Instagram (expects a public URL; here we assume you host outputs or upload elsewhere)
    # Example only: comment out post if you don't have a public URL yet.
    # post_image("https://your-cdn.com/demo_persona.png", "Meet Aria, my AI persona! #AIgirl #virtualinfluencer")
    comment_on_hashtags(["AIgirl", "virtualinfluencer"], "This is awesome! 💕", max_posts=1)

    # Video from image
    generate_video_from_image(img_path, prompt="the girl blinks and waves hello", output_path="outputs/demo_video.mp4" )

    # Persona chat + voice
    persona = PersonaEngine(name="Aria")
    reply = persona.generate_response("Hi Aria, can you send me something special?")
    logging.info(f"Persona text: {reply['text']}")
    if reply.get("audio_path"): logging.info(f"Voice at: {reply['audio_path']}")

    # Stripe sample
    # url = create_checkout_session("price_12345")
    # if url: logging.info(f"Stripe checkout: {url}")

if __name__ == "__main__":
    main()


# === Aria persona wiring ===
try:
    import os
    EGIRL_NAME = os.getenv("EGIRL_NAME","Aria")
    EGIRL_PROMPT_PATH = os.getenv("EGIRL_PROMPT_PATH","agent/egirl/prompt.md")
    if os.path.exists(EGIRL_PROMPT_PATH):
        with open(EGIRL_PROMPT_PATH,"r",encoding="utf-8") as f:
            ARIA_PROMPT = f.read()
        print(f"[Aria] Loaded persona prompt for {EGIRL_NAME} from {EGIRL_PROMPT_PATH}")
except Exception as e:
    print("[Aria] Persona wiring note:", e)

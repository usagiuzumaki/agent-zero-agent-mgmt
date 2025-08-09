import os, logging, base64, time, requests

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
RUNWAY_ENDPOINT = "https://api.runwayml.com/v1/image_to_video"

def generate_video_from_image(image_path: str, prompt: str, output_path: str = "outputs/video.mp4") -> str | None:
    if not RUNWAY_API_KEY:
        logging.error("RUNWAY_API_KEY missing.")
        return None
    with open(image_path, "rb") as f:
        img_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
        "Runway-Version": "2024-11-06"
    }
    payload = {"prompt_image": img_b64, "prompt_text": prompt, "seed": 42}
    task = requests.post(RUNWAY_ENDPOINT, json=payload, headers=headers).json()
    if "id" not in task:
        logging.error(f"Runway error: {task}")
        return None
    tid = task["id"]
    status_url = f"https://api.runwayml.com/v1/tasks/{tid}"
    for _ in range(120):
        st = requests.get(status_url, headers=headers).json()
        if st.get("status") == "succeeded":
            vurl = st["result"]["video"]
            data = requests.get(vurl).content
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as vf:
                vf.write(data)
            logging.info(f"Saved video to {output_path}")
            return output_path
        if st.get("status") == "failed":
            logging.error(f"Runway failed: {st}")
            return None
        time.sleep(2)
    logging.error("Runway timed out.")
    return None

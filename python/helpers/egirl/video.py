import os
import logging
import base64
import time
try:
    import requests
except ImportError:
    requests = None

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
RUNWAY_ENDPOINT = "https://api.runwayml.com/v1/image_to_video"

def generate_video_from_image(image_path: str, prompt: str, output_path: str = "outputs/video.mp4") -> str | None:
    if requests is None:
        logging.error("Requests library not installed.")
        return None

    if not RUNWAY_API_KEY:
        logging.error("RUNWAY_API_KEY missing.")
        return None

    if not os.path.exists(image_path):
        logging.error(f"Image file not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as f:
            img_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        logging.error(f"Error reading image file: {e}")
        return None

    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
        "Runway-Version": "2024-11-06"
    }
    payload = {"prompt_image": img_b64, "prompt_text": prompt, "seed": 42}

    try:
        response = requests.post(RUNWAY_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        task = response.json()
    except Exception as e:
        logging.error(f"Runway API error: {e}")
        return None

    if "id" not in task:
        logging.error(f"Runway error: {task}")
        return None

    tid = task["id"]
    status_url = f"https://api.runwayml.com/v1/tasks/{tid}"

    # Poll for 4 minutes (120 * 2s)
    for _ in range(120):
        try:
            st_response = requests.get(status_url, headers=headers, timeout=10)
            st_response.raise_for_status()
            st = st_response.json()

            status = st.get("status")
            if status == "succeeded":
                vurl = st["result"]["video"]
                video_response = requests.get(vurl, timeout=60)
                video_response.raise_for_status()
                data = video_response.content

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as vf:
                    vf.write(data)
                logging.info(f"Saved video to {output_path}")
                return output_path

            if status == "failed":
                logging.error(f"Runway failed: {st}")
                return None

        except Exception as e:
            logging.error(f"Error polling Runway task: {e}")
            # Continue polling even if one request fails, unless it's critical
            pass

        time.sleep(2)

    logging.error("Runway timed out.")
    return None

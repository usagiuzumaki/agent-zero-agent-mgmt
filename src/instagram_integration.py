import os, logging, requests

IG_USER_ID = os.getenv("IG_USER_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
GRAPH_API_BASE = "https://graph.facebook.com/v17.0"

def post_image(image_url: str, caption: str):
    """Upload an image by URL and publish with caption on Instagram Business account."""
    if not IG_USER_ID or not IG_ACCESS_TOKEN:
        logging.error("Instagram credentials missing.")
        return None
    # Step 1: create media container
    url = f"{GRAPH_API_BASE}/{IG_USER_ID}/media"
    params = { "image_url": image_url, "caption": caption, "access_token": IG_ACCESS_TOKEN }
    r = requests.post(url, params=params)
    data = r.json()
    if "id" not in data:
        logging.error(f"Create media container failed: {data}")
        return None
    creation_id = data["id"]
    # Step 2: publish
    pub_url = f"{GRAPH_API_BASE}/{IG_USER_ID}/media_publish"
    pub_params = { "creation_id": creation_id, "access_token": IG_ACCESS_TOKEN }
    r2 = requests.post(pub_url, params=pub_params)
    res = r2.json()
    if "id" in res:
        logging.info(f"Published IG media id={res['id']}")
    else:
        logging.error(f"Publish failed: {res}")
    return res

def comment_on_hashtags(hashtags, comment_text: str, max_posts: int = 3):
    if not IG_USER_ID or not IG_ACCESS_TOKEN:
        logging.error("Instagram credentials missing.")
        return
    for tag in hashtags:
        # Hashtag search
        search = requests.get(
            f"{GRAPH_API_BASE}/ig_hashtag_search",
            params={"user_id": IG_USER_ID, "q": tag, "access_token": IG_ACCESS_TOKEN}
        ).json()
        if not search.get("data"):
            logging.warning(f"No hashtag found for {tag}")
            continue
        hashtag_id = search["data"][0]["id"]
        # Recent media
        media = requests.get(
            f"{GRAPH_API_BASE}/{hashtag_id}/recent_media",
            params={"user_id": IG_USER_ID, "fields": "id,caption", "access_token": IG_ACCESS_TOKEN}
        ).json().get("data", [])
        count = 0
        for m in media:
            if count >= max_posts: break
            mid = m["id"]
            res = requests.post(
                f"{GRAPH_API_BASE}/{mid}/comments",
                params={"message": comment_text, "access_token": IG_ACCESS_TOKEN}
            ).json()
            if "id" in res:
                logging.info(f"Commented on {mid}")
            else:
                logging.error(f"Comment failed on {mid}: {res}")
            count += 1

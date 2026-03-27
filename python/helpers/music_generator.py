from typing import Dict, Any, List

def analyze_sentiment(text: str) -> Dict[str, float]:
    """A highly simplified keyword-based sentiment analyzer."""
    text = text.lower()

    # Very basic lexicons
    positive = ["love", "happy", "pumped", "pumped", "great", "perfect", "good", "beautiful", "excited", "let's go", "gym", "enthusiast"]
    negative = ["sad", "angry", "miss", "misses", "cried", "loss", "empty", "lonely", "hate", "bad"]
    energetic = ["pumped", "fast", "run", "marathon", "gym", "action", "power", "let's go!!", "pumped for today!"]
    intimate = ["close", "stars", "beach", "sunset", "date", "romantic", "softie", "chocolate"]
    nostalgic = ["old times", "postcards", "vintage", "miss", "misses", "remember"]
    intense = ["angry", "heavy metal", "rage", "conflict", "conflict"]

    scores = {
        "positive": 0.0,
        "negative": 0.0,
        "energetic": 0.0,
        "intimate": 0.0,
        "nostalgic": 0.0,
        "intense": 0.0
    }

    # Tokenize and score roughly
    for word in positive:
        if word in text: scores["positive"] += 1.0
    for word in negative:
        if word in text: scores["negative"] += 1.0
    for word in energetic:
        if word in text: scores["energetic"] += 1.0
    for word in intimate:
        if word in text: scores["intimate"] += 1.0
    for word in nostalgic:
        if word in text: scores["nostalgic"] += 1.0
    for word in intense:
        if word in text: scores["intense"] += 1.0

    return scores

def deduce_song_profile(user_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deduces a musical profile based on user context memories and messages.
    """
    # 1. Aggregate all text
    all_text = ""
    for fact in user_context.get("user_facts", []):
        all_text += fact.get("content", "") + " "
    for moment in user_context.get("special_moments", []):
        all_text += moment.get("content", "") + " "
    for msg in user_context.get("recent_messages", []):
        all_text += msg + " "

    all_text = all_text.strip()

    # Handle empty state
    if not all_text:
        return {
            "tempo": "medium",
            "key_signature": "neutral",
            "instruments": ["lo-fi beats", "electric piano"],
            "mood": ["chill", "neutral"],
            "lyric_themes": ["exploration", "daydreaming", "abstract"]
        }

    # 2. Analyze sentiment
    sentiment = analyze_sentiment(all_text)

    # 3. Determine dominant traits
    max_trait = max(sentiment, key=sentiment.get)
    max_score = sentiment[max_trait]

    # Defaults
    tempo = "medium"
    key_signature = "major"
    instruments = []
    mood = []
    lyric_themes = []

    # Complex case: mixed emotions (e.g. angry and sad)
    if sentiment["intense"] > 0 and sentiment["negative"] > 0:
        tempo = "variable"
        key_signature = "minor"
        instruments = ["electric guitar", "drums", "bass"]
        mood = ["angst", "passionate"]
        lyric_themes = ["conflict", "duality", "inner turmoil"]

    # Energetic case
    elif sentiment["energetic"] > 0 and sentiment["positive"] >= 0:
        tempo = "fast"
        key_signature = "major"
        instruments = ["synth", "drums", "electric guitar"]
        mood = ["energetic", "hype", "uplifting"]
        lyric_themes = ["energy", "power", "action"]

    # Nostalgic/Melancholy case
    elif sentiment["nostalgic"] > 0 or (sentiment["negative"] > sentiment["positive"]):
        tempo = "slow"
        key_signature = "minor"
        instruments = ["cello", "piano", "strings"]
        mood = ["nostalgic", "melancholy", "sad"]
        lyric_themes = ["loss", "memory", "longing"]

    # Intimate/Romantic case
    elif sentiment["intimate"] > 0 or sentiment["positive"] > 0:
        tempo = "slow"
        key_signature = "major"
        instruments = ["acoustic guitar", "piano"]
        mood = ["intimate", "romantic", "peaceful"]
        lyric_themes = ["love", "connection", "beauty"]

    # Fallback
    else:
        tempo = "medium"
        key_signature = "major"
        instruments = ["acoustic guitar", "bass", "drums"]
        mood = ["chill"]
        lyric_themes = ["life", "reflection"]


    return {
        "tempo": tempo,
        "key_signature": key_signature,
        "instruments": instruments,
        "mood": mood,
        "lyric_themes": lyric_themes
    }

import pytest
from python.helpers.music_generator import deduce_song_profile

def test_deduce_song_profile_romantic_slow():
    user_context = {
        "user_facts": [{"content": "loves sunsets on the beach"}, {"content": "likes chocolate"}],
        "special_moments": [{"content": "our first virtual date under the stars"}],
        "recent_messages": ["I feel so close to you right now.", "This is perfect."]
    }

    result = deduce_song_profile(user_context)

    assert result["tempo"] in ["slow", "andante", "adagio"]
    assert "acoustic guitar" in result["instruments"] or "piano" in result["instruments"]
    assert result["key_signature"] in ["major", "lydian"]
    assert "intimate" in result["mood"]
    assert "love" in result["lyric_themes"] or "connection" in result["lyric_themes"]

def test_deduce_song_profile_energetic_upbeat():
    user_context = {
        "user_facts": [{"content": "gym enthusiast"}, {"content": "drinks 5 coffees a day"}],
        "special_moments": [{"content": "ran a marathon"}],
        "recent_messages": ["Let's go!!", "I'm so pumped for today!"]
    }

    result = deduce_song_profile(user_context)

    assert result["tempo"] in ["fast", "allegro", "presto"]
    assert "synth" in result["instruments"] or "drums" in result["instruments"] or "electric guitar" in result["instruments"]
    assert "energetic" in result["mood"] or "hype" in result["mood"]
    assert "energy" in result["lyric_themes"] or "power" in result["lyric_themes"] or "action" in result["lyric_themes"]

def test_deduce_song_profile_melancholy_sad():
    user_context = {
        "user_facts": [{"content": "misses their old dog"}, {"content": "collects vintage postcards"}],
        "special_moments": [{"content": "saying goodbye at the airport"}],
        "recent_messages": ["It's been raining all day.", "I feel kind of empty today.", "I miss the old times."]
    }

    result = deduce_song_profile(user_context)

    assert result["tempo"] in ["slow", "largo", "adagio"]
    assert result["key_signature"] in ["minor", "dorian", "aeolian"]
    assert "cello" in result["instruments"] or "piano" in result["instruments"] or "strings" in result["instruments"]
    assert "nostalgic" in result["mood"] or "melancholy" in result["mood"]
    assert "loss" in result["lyric_themes"] or "memory" in result["lyric_themes"] or "longing" in result["lyric_themes"]

def test_deduce_song_profile_empty_state():
    user_context = {
        "user_facts": [],
        "special_moments": [],
        "recent_messages": []
    }

    result = deduce_song_profile(user_context)

    # Should fallback to a neutral, chill lo-fi vibe
    assert result["tempo"] in ["medium", "moderato"]
    assert "lo-fi beats" in result["instruments"] or "electric piano" in result["instruments"]
    assert result["key_signature"] in ["major", "minor", "neutral"]
    assert "chill" in result["mood"] or "neutral" in result["mood"]
    assert "exploration" in result["lyric_themes"] or "abstract" in result["lyric_themes"] or "daydreaming" in result["lyric_themes"]

def test_deduce_song_profile_complex_mixed_emotions():
    user_context = {
        "user_facts": [{"content": "loves heavy metal"}, {"content": "is a softie at heart"}],
        "special_moments": [{"content": "cried at a concert"}],
        "recent_messages": ["I'm so angry but also just really sad about it all."]
    }

    result = deduce_song_profile(user_context)

    # Should blend intensity with emotional depth
    assert result["tempo"] in ["medium", "fast", "variable"]
    assert "electric guitar" in result["instruments"]
    assert result["key_signature"] == "minor"
    assert "angst" in result["mood"] or "passionate" in result["mood"]
    assert "conflict" in result["lyric_themes"] or "duality" in result["lyric_themes"]

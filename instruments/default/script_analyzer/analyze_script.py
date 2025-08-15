import sys
import json
import re
from collections import Counter


def extract_scenes(lines):
    scene_regex = re.compile(r"^(INT|EXT|EST|INT./EXT.|INT/EXT|EXT./INT.)", re.IGNORECASE)
    return [line.strip() for line in lines if scene_regex.match(line.strip())]


def extract_characters(lines):
    characters = []
    for line in lines:
        stripped = line.strip()
        if stripped.isupper() and 0 < len(stripped.split()) <= 4 and not stripped.startswith(("INT", "EXT", "EST")):
            characters.append(stripped)
    return characters


def analyze_script(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    scenes = extract_scenes(lines)
    characters = extract_characters(lines)

    char_counts = Counter()
    current_char = None
    for line in lines:
        stripped = line.strip()
        if stripped in characters:
            current_char = stripped
        elif current_char and stripped:
            char_counts[current_char] += 1
        elif not stripped:
            current_char = None

    report = {
        "scenes": len(scenes),
        "characters": sorted(set(characters)),
        "dialogue_lines": char_counts,
    }
    return report


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_script.py <path_to_script>")
        sys.exit(1)

    result = analyze_script(sys.argv[1])
    result["dialogue_lines"] = dict(result["dialogue_lines"])
    print(json.dumps(result, indent=2))

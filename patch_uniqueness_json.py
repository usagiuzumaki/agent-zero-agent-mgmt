import json

with open("python/uniqueness/uniqueness.config.json", "r") as f:
    config = json.load(f)

# Add sensory_overload to traits
config["traits"]["sensory_overload"] = {"enabled": True, "strength": 0.6}

# Add oblique_strategy to rituals
config["rituals"]["oblique_strategy"] = {"enabled": True}

with open("python/uniqueness/uniqueness.config.json", "w") as f:
    json.dump(config, f, indent=2)

print("Uniqueness config patched.")

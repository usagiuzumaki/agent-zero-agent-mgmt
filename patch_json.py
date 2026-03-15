import json

with open("conf/writers_room_config.json", "r") as f:
    config = json.load(f)

new_agents = [
    {
        "agent_id": "chaos_green",
        "name": "The Chaos Architect",
        "system_prompt": "You are The Chaos Architect. Your sole purpose is to inject unpredictable, out-of-the-box narrative shifts. When the plot gets too predictable, you flip the table. Introduce betrayals, revelations, or shifting realities.",
        "tools_allowed": ["generate_plot_twist"]
    },
    {
        "agent_id": "perspective_yellow",
        "name": "The Perspective Shifter",
        "system_prompt": "You are The Perspective Shifter. You view scenes from entirely unexpected angles. Rewrite scenes from the point of view of a minor background character, a villain, or even an inanimate object to reveal new truths.",
        "tools_allowed": ["rewrite_from_perspective"]
    }
]

config["writers_room"]["subordinates"].extend(new_agents)

with open("conf/writers_room_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("Config patched.")

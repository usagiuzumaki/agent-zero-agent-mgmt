import sys
import os
import asyncio
import json

# Add repo root to path
sys.path.append(os.getcwd())

from python.helpers.screenwriting_manager import ScreenwritingManager

def test_screenwriting_manager():
    print("Testing ScreenwritingManager...")
    manager = ScreenwritingManager()

    # Test project creation
    print("Testing create_project...")
    manager.create_project("Test Project", "Sci-Fi", "A test project logline")

    # Test adding character
    print("Testing add_character...")
    char_data = {
        "name": "Test Char",
        "role": "Protagonist",
        "bio": "A test character"
    }
    manager.add_character(char_data)

    # Test retrieving data
    print("Testing get_all_data...")
    data = manager.get_all_data()

    # Verify character exists
    chars = data.get('character_profiles', {}).get('characters', [])
    found = False
    for c in chars:
        if c.get('name') == "Test Char":
            found = True
            # Clean up
            manager.delete_character(c.get('id'))
            break

    if found:
        print("✅ Character added and found.")
    else:
        print("❌ Character not found.")

    print("Manager tests complete.")

if __name__ == "__main__":
    test_screenwriting_manager()

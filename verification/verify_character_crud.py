import requests
import json
import sys

# Base URL for the API
BASE_URL = "http://localhost:5000/api/screenwriting"

def test_crud():
    print("Testing Character CRUD...")

    # 1. Create a character
    new_char = {
        "name": "Test Character",
        "role": "Protagonist",
        "archetype": "The Tester",
        "motivation": "To pass all tests",
        "flaw": "Buggy",
        "bio": "Created for automated testing"
    }

    print(f"Adding character: {new_char['name']}")
    response = requests.post(f"{BASE_URL}/character/add", json=new_char)
    if response.status_code != 200:
        print(f"Failed to add character: {response.text}")
        return False

    # 2. Retrieve all characters to find the ID
    print("Retrieving characters...")
    response = requests.get(f"{BASE_URL}/all")
    if response.status_code != 200:
        print(f"Failed to get data: {response.text}")
        return False

    data = response.json()
    characters = data.get('character_profiles', {}).get('characters', [])

    target_char = None
    for char in characters:
        if char['name'] == "Test Character" and char['role'] == "Protagonist":
            target_char = char
            break

    if not target_char:
        print("Created character not found in list")
        return False

    char_id = target_char['id']
    print(f"Found character ID: {char_id}")

    # 3. Update the character
    update_data = target_char.copy()
    update_data['bio'] = "Updated bio for testing"
    update_data['flaw'] = "None"

    print(f"Updating character {char_id}...")
    response = requests.post(f"{BASE_URL}/character/update", json=update_data)
    if response.status_code != 200:
        print(f"Failed to update character: {response.text}")
        return False

    # Verify update
    response = requests.get(f"{BASE_URL}/all")
    data = response.json()
    updated_char = next((c for c in data['character_profiles']['characters'] if c['id'] == char_id), None)

    if not updated_char or updated_char['bio'] != "Updated bio for testing":
        print("Update verification failed")
        return False
    print("Update verified.")

    # 4. Delete the character
    print(f"Deleting character {char_id}...")
    response = requests.delete(f"{BASE_URL}/character/delete", json={"id": char_id})
    if response.status_code != 200:
        print(f"Failed to delete character: {response.text}")
        return False

    # Verify deletion
    response = requests.get(f"{BASE_URL}/all")
    data = response.json()
    deleted_char = next((c for c in data['character_profiles']['characters'] if c['id'] == char_id), None)

    if deleted_char:
        print("Deletion verification failed (character still exists)")
        return False

    print("Deletion verified.")
    print("CRUD Test Passed!")
    return True

if __name__ == "__main__":
    try:
        if test_crud():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"Test failed with exception: {e}")
        sys.exit(1)

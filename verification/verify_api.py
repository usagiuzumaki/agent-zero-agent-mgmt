import time
import requests

def verify_characters_api():
    base_url = "http://localhost:5000/api/screenwriting"

    # 1. Create a character
    new_char = {
        "name": "Test Character",
        "role": "Protagonist",
        "archetype": "The Hero",
        "motivation": "To verify the API",
        "flaw": "Impatient",
        "bio": "Created by verification script"
    }

    print(f"Adding character: {new_char['name']}")
    resp = requests.post(f"{base_url}/character/add", json=new_char)
    assert resp.status_code == 200

    # 2. Fetch characters and find the one we just created
    print("Fetching characters...")
    resp = requests.get(f"{base_url}/all")
    assert resp.status_code == 200
    data = resp.json()
    characters = data['character_profiles']['characters']

    found_char = None
    for char in characters:
        if char['name'] == new_char['name']:
            found_char = char
            break

    assert found_char is not None
    print(f"Found character: {found_char['name']} (ID: {found_char['id']})")

    # 3. Update the character
    updated_data = found_char.copy()
    updated_data['bio'] = "Updated bio"

    print(f"Updating character bio...")
    resp = requests.post(f"{base_url}/character/update", json={
        "id": found_char['id'],
        "data": updated_data
    })
    assert resp.status_code == 200

    # Verify update
    resp = requests.post(f"{base_url}/character/find", json={"name": new_char['name']})
    assert resp.status_code == 200
    assert resp.json()['bio'] == "Updated bio"
    print("Character updated successfully")

    # 4. Delete the character
    print(f"Deleting character...")
    resp = requests.post(f"{base_url}/character/delete", json={"id": found_char['id']})
    assert resp.status_code == 200

    # Verify deletion
    resp = requests.get(f"{base_url}/all")
    characters = resp.json()['character_profiles']['characters']
    assert not any(c['id'] == found_char['id'] for c in characters)
    print("Character deleted successfully")

    print("\nAPI Verification passed!")

if __name__ == "__main__":
    verify_characters_api()

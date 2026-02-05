import time
import requests
from playwright.sync_api import sync_playwright, expect

def test_draft_scene():
    print("Starting verification...")

    # 1. Setup: Upload a document via API
    try:
        res = requests.post("http://localhost:5000/api/screenwriting/storybook/upload", json={
            "name": "Verification Doc",
            "content": "EXT. FOREST - DAY\nA quiet forest.\n\nINT. CABIN - DAY\nUse this beat.",
            "description": "For verification"
        })
        if res.status_code == 200:
            print("Document uploaded via API.")
        else:
            print(f"Failed to upload doc: {res.text}")
    except Exception as e:
        print(f"API Error: {e}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 2. Navigate to app
        print("Navigating to app...")
        page.goto("http://localhost:5173")
        page.wait_for_load_state("networkidle")

        # 3. Open AgentLauncher
        print("Opening AgentLauncher...")
        # Wait for launcher to appear
        page.locator(".agent-launcher").wait_for()
        page.locator(".agent-launcher").click()

        # 4. Select Screenwriting UI
        print("Selecting Screenwriting UI...")
        # The select has title "Select Interface Mode"
        page.get_by_title("Select Interface Mode").wait_for()
        page.get_by_title("Select Interface Mode").select_option("screenwriting")

        # 5. Select Storybook Tab
        print("Selecting Storybook Tab...")
        # Wait for the UI to switch
        page.get_by_role("tab", name="Storybook").wait_for()
        page.get_by_role("tab", name="Storybook").click()

        # 6. Open the document
        print("Opening document...")
        # It should be in the list.
        page.get_by_text("Verification Doc").first.wait_for()
        page.get_by_text("Verification Doc").first.click()

        # 7. Click Draft Scene
        print("Clicking Draft Scene...")
        # Find the first "Draft Scene" button
        draft_btn = page.get_by_role("button", name="Draft Scene").first
        draft_btn.wait_for()
        draft_btn.click()

        # 8. Wait for result
        print("Waiting for draft...")
        # The modal has header "Scene Draft"
        page.get_by_text("Scene Draft").wait_for(timeout=60000) # Give it time

        # 9. Verify content
        modal_content = page.locator(".agent-modal .modal-content")
        expect(modal_content).not_to_be_empty()

        # 10. Screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/draft_scene_modal.png")
        print("Screenshot saved to verification/draft_scene_modal.png")

        browser.close()

if __name__ == "__main__":
    test_draft_scene()

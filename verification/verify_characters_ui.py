from playwright.sync_api import Page, expect, sync_playwright
import time

def verify_characters_ui(page: Page):
    # Navigate to the Characters UI
    # In the actual app, this might be under a tab.
    # We need to find the correct route.
    # Based on `ui-kit-react/src/components/ScreenwritingUI.jsx`:
    # It has tabs. We need to click "Characters".

    # Assuming we are viewing the ScreenwritingUI.
    # We might need to launch it first.
    # Let's check how the app starts. It seems `App.jsx` handles routing/mode.
    # Since we can't easily switch modes programmatically without more info,
    # let's try to assume we can get to the screenwriting mode.
    # Or we can just go to the root and click buttons.

    page.goto("http://localhost:4173")

    # Wait for the app to load
    page.wait_for_timeout(2000)

    # Click "Open Agent" if present (Launcher)
    if page.get_by_text("Open Agent").is_visible():
        page.get_by_text("Open Agent").click()
        # Select "Screenwriting" from dropdown. It's a select element.
        page.locator("select.ui-select").select_option("screenwriting")

    # Now we should be in ScreenwritingUI.
    # Click "Characters" tab.
    page.get_by_role("tab", name="Characters").click()

    # Wait for Characters UI to load
    expect(page.get_by_text("Cast of Characters")).to_be_visible()

    # Wait for spinner to disappear if present
    expect(page.locator(".spinner")).not_to_be_visible()

    # Click "+ Add Character"
    page.get_by_role("button", name="+ Add Character").click()

    # Check title is "New Character Profile"
    expect(page.get_by_role("heading", name="New Character Profile")).to_be_visible()

    # Fill out form
    page.get_by_label("Name *").fill("Test Hero")
    page.get_by_label("Role").select_option("Protagonist")
    page.get_by_role("button", name="Save Character").click()

    # Wait for character to appear in list
    expect(page.get_by_text("Test Hero").first).to_be_visible()

    # Click "Edit" on the character
    page.get_by_role("button", name="Edit Test Hero").first.click()

    # Check title is "Edit Character Profile" (This is the change we made!)
    expect(page.get_by_role("heading", name="Edit Character Profile")).to_be_visible()

    # Take screenshot
    page.screenshot(path="verification/characters_edit_title.png")

    # Clean up (Delete)
    # Handle multiple if previous run failed
    count = page.get_by_role("button", name="Delete Test Hero").count()
    for _ in range(count):
        # We need to setup dialog handler BEFORE clicking
        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Delete Test Hero").first.click()
        # Wait for the item to disappear instead of using timeout
        expect(page.get_by_text("Test Hero").first).not_to_be_visible()


    # Wait for deletion
    expect(page.get_by_text("Test Hero")).not_to_be_visible()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_characters_ui(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/failure.png")
        finally:
            browser.close()

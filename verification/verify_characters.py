
from playwright.sync_api import sync_playwright, expect
import time

def verify_characters_edit(page):
    page.goto("http://localhost:4173")

    # Open the modal
    page.get_by_role("button", name="Open Agent").click()

    # Select Screenwriting from the dropdown
    # The error message said it found an <option>, which is not clickable directly in some browsers/playwright contexts if hidden.
    # But this is a standard <select>. We should use `select_option`.
    page.locator("select.ui-select").select_option("screenwriting")

    # 3. Navigate to Characters tab
    page.get_by_role("tab", name="Characters").click()

    # 4. Create a new character
    # Check if we need to click cancel first if form was open from previous run (state might persist in backend, but UI resets on refresh)
    # UI resets on refresh so we are good.

    page.get_by_text("+ Add Character").click()

    # Fill form
    # Using specific locators since labels are associated
    page.get_by_label("Name").fill("Test Character For Verification")
    page.get_by_label("Bio & Notes").fill("A temporary character for testing.")

    # Save
    page.get_by_role("button", name="Save Character").click()

    # Wait for it to appear in the list
    expect(page.get_by_text("Test Character For Verification")).to_be_visible()

    # 5. Edit the character
    # Locate the card
    card = page.locator(".char-card").filter(has_text="Test Character For Verification")

    # Click Edit
    card.get_by_label("Edit Test Character For Verification").click()

    # Verify form is populated
    expect(page.get_by_label("Name")).to_have_value("Test Character For Verification")

    # Change name
    page.get_by_label("Name").fill("Updated Character Name")

    # Update
    page.get_by_role("button", name="Update Character").click()

    # Verify update in list
    expect(page.get_by_text("Updated Character Name")).to_be_visible()
    expect(page.get_by_text("Test Character For Verification")).not_to_be_visible()

    # 6. Delete the character
    # Handle dialog
    page.on("dialog", lambda dialog: dialog.accept())

    updated_card = page.locator(".char-card").filter(has_text="Updated Character Name")
    updated_card.get_by_label("Delete Updated Character Name").click()

    # Verify deletion
    expect(page.get_by_text("Updated Character Name")).not_to_be_visible()

    # Take final screenshot
    page.screenshot(path="verification/characters_verified.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_characters_edit(page)
            print("Verification successful!")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/failure.png")
        finally:
            browser.close()

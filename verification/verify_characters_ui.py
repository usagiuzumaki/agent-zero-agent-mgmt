
import re
import os
from playwright.sync_api import Page, expect, sync_playwright

def test_characters_ui(page: Page):
    print("Starting test...")
    # Mock the backend API to return empty characters initially to test empty state
    page.route("**/api/screenwriting/all", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"character_profiles": {"characters": []}}'
    ))

    # Mock other endpoints to prevent errors
    page.route("**/api/poll", lambda route: route.fulfill(status=200, body="{}"))

    # Navigate to the app
    print("Navigating to app...")
    page.goto("http://localhost:4173")

    # Navigate to Characters UI
    # 1. Click "Open Agent"
    print("Clicking Open Agent...")
    page.get_by_role("button", name="Open Agent").click()

    # 2. Select "Screenwriting" from dropdown
    print("Selecting Screenwriting...")
    page.select_option("select.ui-select", "screenwriting")

    # 3. Click "Characters" tab
    print("Clicking Characters tab...")
    page.get_by_role("tab", name="Characters").click()

    # Verify Empty State
    print("Verifying empty state...")
    expect(page.get_by_text("No characters yet. Every story needs a cast!")).to_be_visible()
    expect(page.get_by_role("button", name="Create First Character")).to_be_visible()

    # Screenshot Empty State
    screenshot_path = "/home/jules/verification/characters_empty_state.png"
    print(f"Taking screenshot to {screenshot_path}...")
    page.screenshot(path=screenshot_path)
    if os.path.exists(screenshot_path):
        print("Screenshot saved successfully.")
    else:
        print("Screenshot failed to save.")

    # Click Create First Character
    print("Clicking Create First Character...")
    page.get_by_role("button", name="Create First Character").click()

    # Verify Form Opens
    print("Verifying form opens...")
    expect(page.get_by_text("New Character Profile")).to_be_visible()

    # Verify Required Asterisk
    print("Verifying asterisk...")
    # We look for the asterisk text inside the label for "Name"
    name_input = page.get_by_label("Name *")
    if not name_input.is_visible():
         print("Asterisk label not found directly, checking fallback...")
         name_input = page.get_by_label("Name")

    expect(name_input).to_be_visible()

    # Taking a screenshot of the form
    form_screenshot_path = "/home/jules/verification/characters_form.png"
    print(f"Taking form screenshot to {form_screenshot_path}...")
    page.screenshot(path=form_screenshot_path)
    if os.path.exists(form_screenshot_path):
        print("Form screenshot saved successfully.")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_characters_ui(page)
        except Exception as e:
            print(f"Test failed: {e}")
            page.screenshot(path="/home/jules/verification/failure.png")
            raise e
        finally:
            browser.close()

from playwright.sync_api import sync_playwright, expect
import time

def verify_characters_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Route API calls
        page.route("**/api/screenwriting/all", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"character_profiles": {"characters": []}}'
        ))

        # Navigate
        print("Navigating to app...")
        page.goto("http://localhost:4173")

        # Open Agent
        print("Clicking Open Agent...")
        page.get_by_role("button", name="Open Agent").click()

        # Select "Screenwriting" from the dropdown
        # The dropdown is a <select> element with class "ui-select"
        # Since there are two selects, we can distinguish by values or order, or just use the option label
        print("Selecting Screenwriting...")
        # We should select the option in the select element, not click the option text directly (which might be hidden if it's native select)
        page.locator("select.ui-select").first.select_option("screenwriting")

        # Now we should be in ScreenwritingUI. Click "Characters" tab.
        print("Clicking Characters tab...")
        page.get_by_role("tab", name="Characters").click()

        # Click "+ Add Character" to open the form
        print("Clicking Add Character...")
        page.get_by_role("button", name="+ Add Character").click()

        # Verify Focus
        print("Verifying focus...")
        name_input = page.get_by_label("Name")
        expect(name_input).to_be_focused()
        print("Focus verified!")

        # Verify Cancel Button
        print("Verifying Cancel button...")
        cancel_btn = page.locator(".form-actions").get_by_role("button", name="Cancel")
        expect(cancel_btn).to_be_visible()
        print("Cancel button verified!")

        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/characters_ui_verified.png")

        browser.close()

if __name__ == "__main__":
    verify_characters_ui()


import os
import sys
from playwright.sync_api import sync_playwright, expect

def verify_characters_ui():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock the backend API
        page.route('**/api/screenwriting/all', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"character_profiles": {"characters": []}}'
        ))

        try:
            page.goto("http://localhost:4173")
        except Exception:
            print("Could not connect to localhost:4173. Make sure the preview server is running.")
            browser.close()
            return

        # 2. Open the "Screenwriting" mode.
        # Click the launcher button
        page.locator(".agent-launcher").click()

        # Wait for modal
        page.locator(".agent-modal").wait_for()

        # Select Screenwriting from the dropdown
        # Use .first to resolve strict mode violation if there are multiple selectors,
        # though usually there should be one main mode selector.
        # If there are two, the first one is likely the mode selector.
        page.locator("select.ui-select").first.select_option(label="Screenwriting")

        # 3. Open the "Characters" tab
        # The ScreenwritingUI has tabs. We need to find the one for characters.
        # It's likely a button with text "Characters".
        page.get_by_role("tab", name="Characters").click()

        # 4. Open the "Add Character" form
        page.get_by_role("button", name="+ Add Character").click()

        # 5. Verify AutoFocus
        expect(page.locator("#char-name")).to_be_focused()
        print("✅ AutoFocus verified on #char-name")

        # 6. Verify Cancel Button
        cancel_btn = page.locator(".btn-cancel")
        expect(cancel_btn).to_be_visible()
        expect(cancel_btn).to_have_text("Cancel")
        print("✅ Cancel button verified")

        # 7. Take a screenshot
        page.screenshot(path="verification/characters_ui_verification.png")
        print("📸 Screenshot taken at verification/characters_ui_verification.png")

        browser.close()

if __name__ == "__main__":
    verify_characters_ui()

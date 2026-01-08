from playwright.sync_api import Page, expect, sync_playwright
import os

def verify_focus_and_cancel(page: Page):
    # 1. Arrange: Go to the verification page
    page.goto("http://localhost:4173")

    # Wait for the data to load
    page.wait_for_selector(".char-card", timeout=5000)

    # 2. Act: Click "Edit" on the first character
    # Using the aria-label we know exists: "Edit Alice"
    edit_button = page.get_by_label("Edit Alice")
    edit_button.click()

    # 3. Assert: Focus should be on the Name input
    # We wait a brief moment for the effect to run
    page.wait_for_timeout(100)

    name_input = page.get_by_label("Name *")
    expect(name_input).to_be_focused()

    # 4. Assert: Cancel button should be visible
    cancel_button = page.get_by_role("button", name="Cancel").first
    expect(cancel_button).to_be_visible()

    # 5. Screenshot
    page.screenshot(path="/home/jules/verification/focus_and_cancel.png")

    # 6. Act: Click Cancel
    cancel_button.click()

    # 7. Assert: Form should be gone
    expect(page.locator("#char-form")).not_to_be_visible()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_focus_and_cancel(page)
        finally:
            browser.close()

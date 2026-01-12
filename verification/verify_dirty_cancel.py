
import os
import sys
from playwright.sync_api import sync_playwright, expect

def verify_dirty_cancel():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock the backend API
        page.route('**/api/screenwriting/all', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"character_profiles": {"characters": [{"id": "1", "name": "Test Char", "role": "Protagonist"}]}}'
        ))

        try:
            page.goto("http://localhost:4173")
        except Exception:
            print("Could not connect to localhost:4173. Make sure the preview server is running.")
            browser.close()
            return

        page.locator(".agent-launcher").click()
        page.locator(".agent-modal").wait_for()
        page.locator("select.ui-select").first.select_option(label="Screenwriting")
        page.get_by_role("tab", name="Characters").click()

        # 1. Click Edit on the character
        page.get_by_label("Edit Test Char").click()

        # Verify we are in edit mode
        expect(page.get_by_text("Edit Character Profile")).to_be_visible()
        expect(page.locator("#char-name")).to_have_value("Test Char")

        # 2. Click the Top Cancel button (The one that says "Cancel" when form is open)
        # It has class btn-primary and text Cancel.
        page.get_by_role("button", name="Cancel").first.click()

        # Form should close
        expect(page.get_by_text("Edit Character Profile")).not_to_be_visible()

        # 3. Click "+ Add Character"
        page.get_by_role("button", name="+ Add Character").click()

        # 4. Verify state. If bug exists, we might still see "Edit Character Profile" or the old name.
        # If handleCancel was NOT called, editingId is still "1" and name is "Test Char".
        # If handleCancel WAS called, editingId is null and name is "".

        # We expect it to be "New Character Profile" and empty name.
        try:
            expect(page.get_by_text("New Character Profile")).to_be_visible()
            expect(page.locator("#char-name")).to_have_value("")
            print("✅ Top Cancel button correctly reset the form (No bug found?)")
        except AssertionError:
            print("❌ FAILURE: Top Cancel button DID NOT reset the form!")
            # Take screenshot of failure
            page.screenshot(path="verification/dirty_cancel_fail.png")

        browser.close()

if __name__ == "__main__":
    verify_dirty_cancel()

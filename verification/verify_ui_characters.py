from playwright.sync_api import sync_playwright, expect
import time

def verify_characters_ui():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to the app (served by Vite preview on port 4173)
            # The backend is proxying requests, so we need the full integration
            page.goto("http://localhost:4173")

            # Wait for the app to load
            page.wait_for_selector(".agent-launcher", timeout=10000)

            # Navigate to Screenwriting UI
            # 1. Click "Open Agent"
            page.get_by_role("button", name="Open Agent").click()

            # 2. Select "Screenwriting" from dropdown
            # Based on the screenshot and code, it's a select element with class "ui-select"
            # We should select the option by value or label
            page.locator("select.ui-select").select_option(label="Screenwriting")

            # Wait for Screenwriting UI to load
            page.wait_for_selector(".screenwriting-ui")

            # Click "Characters" tab
            page.get_by_role("tab", name="Characters").click()

            # Wait for Characters UI
            page.wait_for_selector(".characters-ui")

            # Take initial screenshot
            page.screenshot(path="verification/1_characters_list.png")
            print("Captured initial list")

            # Click "+ Add Character"
            page.get_by_role("button", name="+ Add Character").click()

            # Fill form
            page.get_by_label("Name").fill("Playwright Test Char")
            page.get_by_label("Role").select_option("Protagonist")
            page.get_by_label("Archetype").fill("The Verifier")
            page.get_by_label("Motivation (Want)").fill("To pass the test")
            page.get_by_label("Fatal Flaw (Need)").fill("Timeouts")
            page.get_by_label("Bio & Notes").fill("Created by automation")

            # Screenshot form
            page.screenshot(path="verification/2_add_form.png")
            print("Captured add form")

            # Save
            page.get_by_role("button", name="Save Character").click()

            # Wait for card to appear
            expect(page.get_by_text("Playwright Test Char")).to_be_visible()

            # Screenshot after add
            page.screenshot(path="verification/3_after_add.png")
            print("Captured after add")

            # Click Edit button (pencil icon)
            # We need to find the specific card
            card = page.locator(".char-card").filter(has_text="Playwright Test Char")
            # We can select by aria-label since we added it
            card.get_by_label("Edit Playwright Test Char").click()

            # Verify form is populated and button says "Update Character"
            expect(page.get_by_label("Name")).to_have_value("Playwright Test Char")
            expect(page.get_by_role("button", name="Update Character")).to_be_visible()

            # Modify data
            page.get_by_label("Bio & Notes").fill("Updated by automation")

            # Screenshot edit form
            page.screenshot(path="verification/4_edit_form.png")
            print("Captured edit form")

            # Update
            page.get_by_role("button", name="Update Character").click()

            # Wait for update (bio text change)
            expect(page.get_by_text("Updated by automation")).to_be_visible()

            # Screenshot after update
            page.screenshot(path="verification/5_after_update.png")
            print("Captured after update")

            # Click Delete button (trash icon)
            # Need to handle confirmation dialog
            page.on("dialog", lambda dialog: dialog.accept())

            card = page.locator(".char-card").filter(has_text="Playwright Test Char")
            card.get_by_label("Delete Playwright Test Char").click()

            # Wait for card to disappear - use verify removal from list logic
            # Be careful with timing here. The card might not vanish instantly if animation/delay
            expect(page.get_by_text("Playwright Test Char")).not_to_be_visible()

            # Screenshot after delete
            page.screenshot(path="verification/6_after_delete.png")
            print("Captured after delete")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_characters_ui()

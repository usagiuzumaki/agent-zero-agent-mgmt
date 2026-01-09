from playwright.sync_api import sync_playwright
import time

def verify_characters():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to UI...")
        page.goto("http://localhost:4173")

        # Wait for potential initial load
        time.sleep(2)

        # Open Agent -> Screenwriting
        print("Opening Screenwriting mode...")
        page.click("text=Open Agent")

        # Need to select the option
        # Use first() or stricter locator
        page.locator("select.ui-select").first.select_option(value="screenwriting")

        time.sleep(1)

        # Go to Characters tab
        print("Clicking Characters tab...")
        page.click("#tab-characters")

        # Check for Add Character button
        print("Checking for Add Character button...")
        page.wait_for_selector("text=+ Add Character")

        # Add a character
        page.click("text=+ Add Character")

        # Fill form
        print("Filling form...")
        page.fill("#char-name", "Test Hero")
        page.fill("#char-archetype", "The Tester")
        page.fill("#char-motivation", "To pass the test")
        page.fill("#char-flaw", "Timeouts")
        page.fill("#char-bio", "A generated hero.")

        # Save
        print("Saving...")
        page.click("button.btn-save")

        # Verify spinner or button disabled state if possible, but mainly check if it appears in list
        print("Waiting for character in list...")
        page.wait_for_selector("text=Test Hero")

        print("Character 'Test Hero' found!")

        # Cleanup (Delete)
        print("Deleting character...")

        # We need to handle the dialog BEFORE clicking delete
        def handle_dialog(dialog):
            print(f"Dialog message: {dialog.message}")
            dialog.accept()

        page.on("dialog", handle_dialog)

        page.click("text=Delete")

        # Verify deletion
        time.sleep(2)

        content = page.content()
        if "Test Hero" not in content:
            print("Character successfully deleted.")
        else:
            print("Character still visible (might need refresh or wait).")

        browser.close()

if __name__ == "__main__":
    verify_characters()

from playwright.sync_api import sync_playwright
import time

def verify_characters_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to UI...")
        page.goto("http://localhost:4173")
        time.sleep(2)

        # Open Agent -> Screenwriting
        print("Opening Screenwriting mode...")
        page.click("text=Open Agent")
        page.locator("select.ui-select").first.select_option(value="screenwriting")
        time.sleep(1)

        # Go to Characters tab
        print("Clicking Characters tab...")
        page.click("#tab-characters")

        # Add a character to ensure the card is visible for screenshot
        print("Adding a temporary character for screenshot...")
        page.click("text=+ Add Character")
        page.fill("#char-name", "Screenshot Hero")
        page.select_option("#char-role", "Protagonist")
        page.fill("#char-bio", "A hero created for the screenshot.")
        page.click("button.btn-save")
        page.wait_for_selector("text=Screenshot Hero")

        time.sleep(1)

        print("Taking screenshot of Characters UI...")
        page.screenshot(path="verification/characters_ui.png")

        # Cleanup
        print("Deleting temporary character...")
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("text=Delete")
        time.sleep(1)

        browser.close()

if __name__ == "__main__":
    verify_characters_screenshot()

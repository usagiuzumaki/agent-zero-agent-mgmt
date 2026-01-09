from playwright.sync_api import sync_playwright, expect
import time

def verify_storybook_screenshot():
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

        # Go to Storybook tab
        print("Clicking Storybook tab...")
        page.click("#tab-storybook")

        # Wait for the document list to load
        page.wait_for_selector(".storybook-ui")
        time.sleep(1)

        # Take screenshot of the Storybook main view
        print("Taking screenshot of Storybook main view...")
        page.screenshot(path="verification/storybook_main.png")

        # Click on the document we created earlier (if it persists) or verify empty state
        # Since the backend resets or we might not have persistent storage, we'll check what we see.
        # But wait, the backend process is running, so it might persist if it uses file storage.
        # Let's check for "Test Script" from previous run.

        if page.is_visible("text=Test Script"):
            print("Opening Test Script...")
            page.click("text=Test Script")
            page.wait_for_selector(".document-view")
            time.sleep(1)
            print("Taking screenshot of Document View...")
            page.screenshot(path="verification/storybook_doc_view.png")
        else:
            print("Test Script not found, taking screenshot of empty/list state.")

        browser.close()

if __name__ == "__main__":
    verify_storybook_screenshot()

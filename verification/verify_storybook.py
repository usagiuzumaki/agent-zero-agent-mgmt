from playwright.sync_api import sync_playwright
import time

def verify_storybook():
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

        # Check for New Document button
        print("Checking for New Document button...")
        page.wait_for_selector("text=New Document")

        # Click New Document
        page.click("text=New Document")

        # Fill form
        print("Filling upload form...")
        page.fill("#doc-title", "Test Script")
        page.fill("#doc-content", "INT. ROOM - DAY\nA test script content.")

        # Ingest
        print("Ingesting...")
        page.click("text=Ingest Document")

        # Wait for document in list
        print("Waiting for document in list...")
        page.wait_for_selector("text=Test Script")

        print("Document 'Test Script' found!")

        # Click on the document to view it
        page.click("text=Test Script")

        # Verify view details
        page.wait_for_selector("text=INT. ROOM - DAY")
        print("Document content verified.")

        # Back to list
        page.click("text=← Back to List")
        page.wait_for_selector("text=Test Script")

        browser.close()

if __name__ == "__main__":
    verify_storybook()

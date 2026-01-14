from playwright.sync_api import sync_playwright, expect
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Mock the API responses
        def handle_storybook(route):
            print(f"Mocking storybook request: {route.request.url}")
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"documents": [{"id": "doc1", "name": "Test Doc", "description": "Desc", "uploaded_at": "2023-01-01", "tags": [], "chapters": []}]}'
            )

        # Use a more generic pattern and ensure it catches
        page.route("**/*api/screenwriting/storybook", handle_storybook)

        # Mock delete endpoint with a delay to capture loading state
        def handle_delete(route):
            print(f"Mocking delete request: {route.request.url}")
            # Do not sleep here as it blocks the playwright driver loop if not careful with threading,
            # though lambda sleep is usually ok in sync mode.
            # Better to not sleep but rely on the test waiting.
            # Actually, to verify the loading state, we need the response to be pending.
            # So we can defer fulfillment.
            pass
            # We will fulfill it manually later if needed, or just delay.
            time.sleep(1)
            route.fulfill(status=200, content_type="application/json", body='{"success": true}')

        page.route("**/*api/screenwriting/storybook/delete", handle_delete)

        # Start loading
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))
        page.goto("http://localhost:4173")

        # Navigate to Storybook
        page.get_by_role("button", name="Open Agent").click()
        page.locator("select.ui-select").first.select_option("screenwriting")
        page.get_by_role("tab", name="Storybook").click()

        # Wait for Storybook to load
        print("Waiting for storybook UI...")
        try:
            page.wait_for_selector(".storybook-ui", timeout=5000)
        except Exception:
            print("Failed to find .storybook-ui. Dumping content:")
            print(page.content())
            raise

        # Test 1: Ingest Button Validation
        print("Testing Ingest Button Validation...")
        page.get_by_role("button", name="New Document").click()

        # Verify disabled state initially
        ingest_btn = page.locator(".storybook-upload button.btn-primary")
        expect(ingest_btn).to_be_disabled()
        page.screenshot(path="verification/storybook_ingest_disabled.png")
        print("Screenshot saved: verification/storybook_ingest_disabled.png")

        # Type something
        page.locator("#doc-content").fill("Some content")
        expect(ingest_btn).to_be_enabled()
        page.screenshot(path="verification/storybook_ingest_enabled.png")
        print("Screenshot saved: verification/storybook_ingest_enabled.png")

        # Test 2: Delete Loading State
        print("Testing Delete Loading State...")
        # Close upload panel to see list clearly
        page.get_by_role("button", name="Cancel").click()

        doc_card = page.locator(".document-card").first
        delete_btn = doc_card.locator("button[aria-label*='Delete']")

        # Handle dialog
        page.on("dialog", lambda dialog: dialog.accept())

        # Click delete
        delete_btn.click()

        # Check for spinner (assuming spinner class or svg changes)
        # The spinner component usually has a specific class or structure.
        # In the code: <Spinner size="small" />
        # Depending on Spinner implementation, checking for 'span.spinner' or similar.
        # Let's check if the SVG is gone (replaced by spinner)
        expect(delete_btn.locator("svg")).not_to_be_visible()

        page.screenshot(path="verification/storybook_delete_loading.png")
        print("Screenshot saved: verification/storybook_delete_loading.png")

        # Wait for action to complete (optional, just to close cleanly)
        # time.sleep(2.5)

        browser.close()

if __name__ == "__main__":
    run()

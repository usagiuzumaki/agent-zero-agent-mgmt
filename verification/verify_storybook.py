from playwright.sync_api import sync_playwright, expect
import time

def verify_storybook_accessibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a context with viewport large enough to see everything
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        try:
            # Navigate to the preview server
            print("Navigating to page...")
            page.goto("http://localhost:4173")

            # Wait for content to load
            time.sleep(2)

            # Navigate to Storybook tab (assuming there is navigation or it's the default)
            # Based on memory, there are tabs. We might need to click "Storybook"
            # However, since I don't know the exact tab selector, I'll take a screenshot of the initial state
            # and try to find the "Storybook" text.

            # Take initial screenshot
            page.screenshot(path="verification/initial_load.png")
            print("Initial screenshot taken.")

            # Look for Storybook link/button
            storybook_tab = page.get_by_text("Storybook")
            if storybook_tab.count() > 0:
                print("Clicking Storybook tab...")
                storybook_tab.first.click()
                time.sleep(1)

            # Verify the "New Document" button exists
            # This confirms we are on the right UI
            new_doc_btn = page.get_by_role("button", name="New Document")
            expect(new_doc_btn).to_be_visible()

            # Open the upload form
            print("Opening upload form...")
            new_doc_btn.click()

            # Verify the form accessibility
            # Check for hidden labels
            title_label = page.locator("label[for='doc-title']")
            content_label = page.locator("label[for='doc-content']")

            # Assert labels exist
            if title_label.count() > 0 and content_label.count() > 0:
                print("✅ Accessibility Check Passed: Form labels found.")
            else:
                print("❌ Accessibility Check Failed: Form labels missing.")

            # Check inputs have ids matching labels
            expect(page.locator("#doc-title")).to_be_visible()
            expect(page.locator("#doc-content")).to_be_visible()

            # Take screenshot of the form
            page.screenshot(path="verification/storybook_form.png")
            print("Form screenshot taken.")

            # Test "Ingest" button loading state
            # We'll type something and submit
            page.fill("#doc-title", "Test Doc")
            page.fill("#doc-content", "Test Content")

            # Intercept the network request to delay it so we can capture loading state
            # or just hope we catch it. A better way is to mock the route to hang.

            # Mock the upload endpoint to delay response
            def handle_route(route):
                time.sleep(1) # Delay 1 second
                route.fulfill(status=200, body='{"success":true}')

            page.route("**/api/screenwriting/storybook/upload", handle_route)

            # Click ingest
            ingest_btn = page.get_by_role("button", name="Ingest")
            ingest_btn.click()

            # Immediately check for loading state text "Ingesting..."
            # We might need to be fast.
            # Actually, since we sleep in the route handler, the UI should update.
            # But `page.route` with `time.sleep` blocks the python thread, not the browser network request necessarily in a way that allows us to assert in parallel easily without async playwright.
            # In sync playwright, `route.fulfill` happens when the route matches.
            # If we sleep in the handler, the browser waits.
            # So after `ingest_btn.click()`, the browser is waiting.
            # But the click returns immediately? No, click waits for actionability.

            # Let's try capturing the state.
            # Expect button to be disabled and have text "Ingesting..."
            # We need to run this assertion while the request is pending.
            # This is hard in sync mode if the click blocks.
            # Click shouldn't block on the network request unless we await navigation.

            # Let's just take a screenshot immediately after click?
            # Or use `expect` with a timeout.

            # Actually, `time.sleep` in the route handler effectively pauses the response.
            # So the button should stay in loading state for 1 second.

            expect(ingest_btn).to_have_text("Ingesting...")
            expect(ingest_btn).to_be_disabled()
            print("✅ Loading state verified.")

            page.screenshot(path="verification/loading_state.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_state.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_storybook_accessibility()

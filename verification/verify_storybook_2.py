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

            # Open the Agent Modal
            print("Clicking Open Agent...")
            page.get_by_role("button", name="Open Agent").click()
            time.sleep(1)

            # Select Screenwriting UI
            print("Selecting Screenwriting UI...")
            page.locator("select.ui-select").select_option("screenwriting")
            time.sleep(1)

            # Now we are in ScreenwritingUI, which likely contains Storybook tab
            # Let's check ScreenwritingUI source or screenshot if we fail.
            # But "Storybook" was in the previous plan and seemed correct based on file reading.
            # ScreenwritingUI has tabs.

            # Click Storybook tab
            print("Clicking Storybook tab...")
            page.get_by_text("Storybook").click()
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

            # Mock the upload endpoint to delay response
            def handle_route(route):
                # We do NOT sleep here because it blocks the playwright driver loop for python
                # Instead we fulfill later? No, we can't easily.
                # But since we are using sync playwright, we can just not fulfill immediately?
                # No, we must return from the handler.

                # If we sleep here, the browser hangs waiting for response?
                # Yes, but does `expect` run?
                # In sync playwright, `page.route` handler runs in the same thread?
                # Actually, callbacks might be in a separate thread or blocking.

                # Let's try simple sleep.
                time.sleep(2)
                route.fulfill(status=200, body='{"success":true}')

            page.route("**/api/screenwriting/storybook/upload", handle_route)

            # Click ingest
            ingest_btn = page.get_by_role("button", name="Ingest")

            # We can't verify DURING the click if the click blocks.
            # But the click shouldn't block.
            ingest_btn.click()

            # Now check state immediately
            # We used `time.sleep(2)` in route, so we have 2 seconds window.

            # Note: The button might be disabled now.
            # Using `expect(locator).to_have_text` will retry until it matches.
            # But if the response comes back too fast, it will fail.
            # 2 seconds should be enough.

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

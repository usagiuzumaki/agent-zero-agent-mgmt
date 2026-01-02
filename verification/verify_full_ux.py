from playwright.sync_api import sync_playwright, expect
import time
import json

def verify_storybook_accessibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Mock GET Documents
        def handle_get_docs(route):
            data = {
                "documents": [
                    {
                        "id": "1",
                        "name": "Test Script",
                        "description": "A test script",
                        "uploaded_at": "2023-01-01T00:00:00Z",
                        "tags": ["sci-fi"],
                        "chapters": [
                            {
                                "id": "c1",
                                "title": "Chapter 1",
                                "summary": "Start",
                                "beats": [
                                    {
                                        "id": "b1",
                                        "label": "Opening",
                                        "summary": "Hello",
                                        "visual_prompt": "Scene"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
            route.fulfill(status=200, body=json.dumps(data), headers={"Content-Type": "application/json"})

        # Mock Upload
        def handle_upload(route):
            # Delay to verify loading state
            time.sleep(2)
            route.fulfill(status=200, body='{"success":true}')

        # Apply mocks
        # Order: More specific first if needed, but here paths differ clearly.
        page.route("**/api/screenwriting/storybook/upload", handle_upload)
        page.route("**/api/screenwriting/storybook", handle_get_docs)

        try:
            print("Navigating...")
            page.goto("http://localhost:4173")
            time.sleep(2)

            # Open Agent -> Screenwriting -> Storybook
            print("Opening Screenwriting UI...")
            page.get_by_role("button", name="Open Agent").click()
            time.sleep(0.5)
            page.locator("select.ui-select").select_option("screenwriting")
            time.sleep(0.5)
            page.get_by_text("Storybook").click()
            time.sleep(0.5)

            # 1. Verify Document Card is a Button
            print("Verifying document card structure...")
            # We expect at least one document card from our mock
            doc_card = page.locator(".document-card").first
            expect(doc_card).to_be_visible()

            # Check tag name using evaluate
            tag_name = doc_card.evaluate("el => el.tagName")
            print(f"Document card tag: {tag_name}")
            if tag_name.lower() == "button":
                print("✅ Document card is a <button>.")
            else:
                print(f"❌ Document card is a <{tag_name}>.")

            page.screenshot(path="verification/1_document_list.png")

            # 2. Click Document to see Details and Check Icon Button
            print("Opening document details...")
            doc_card.click()

            # Find the "Draft Dialogue" button
            draft_btn = page.locator("button.btn-icon").first
            expect(draft_btn).to_be_visible()

            # Check aria-label
            aria_label = draft_btn.get_attribute("aria-label")
            print(f"Draft button aria-label: {aria_label}")
            if aria_label == "Draft Dialogue":
                print("✅ Icon button has correct aria-label.")
            else:
                print(f"❌ Icon button missing or wrong aria-label: {aria_label}")

            # Go back
            page.get_by_role("button", name="Back to List").click()

            # 3. Open Upload Form and Verify Labels
            print("Opening upload form...")
            page.get_by_role("button", name="New Document").click()

            # Verify hidden labels
            expect(page.locator("label[for='doc-title']")).to_have_count(1)
            expect(page.locator("label[for='doc-content']")).to_have_count(1)
            print("✅ Form labels verified.")

            page.screenshot(path="verification/2_upload_form.png")

            # 4. Verify Loading State
            print("Verifying loading state...")
            page.fill("#doc-title", "New Story")
            page.fill("#doc-content", "Once upon a time...")

            ingest_btn = page.get_by_role("button", name="Ingest")

            # Click and immediately check state
            # Note: Since the mock sleeps for 2s, the browser will wait for the response.
            # But the click() call in Playwright waits for the event to be dispatched.
            # The JS code sets state immediately.
            ingest_btn.click()

            # We must look for the NEW state immediately.
            loading_btn = page.get_by_role("button", name="Ingesting...")
            expect(loading_btn).to_be_visible()
            expect(loading_btn).to_be_disabled()
            print("✅ Loading state verified.")

            page.screenshot(path="verification/3_loading_state.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_final.png")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    verify_storybook_accessibility()

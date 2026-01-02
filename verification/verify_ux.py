from playwright.sync_api import sync_playwright, expect
import time
import json

def verify_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Mocks
        def handle_get_docs(route):
            data = {
                "documents": [
                    {
                        "id": "1",
                        "name": "Accessible Script",
                        "description": "Testing accessibility",
                        "uploaded_at": "2024-05-23T10:00:00Z",
                        "tags": ["ux", "a11y"],
                        "chapters": [
                            {"id": "c1", "title": "Ch1", "summary": "Sum", "beats": [
                                {"id": "b1", "label": "Beat1", "summary": "B1", "visual_prompt": "VP1"}
                            ]}
                        ]
                    }
                ]
            }
            route.fulfill(status=200, body=json.dumps(data), headers={"Content-Type": "application/json"})

        upload_routes = []
        def handle_upload(route):
            print("Intercepted upload request - holding pending...")
            upload_routes.append(route)
            # Stalled

        # Register Routes - Last registered wins in Playwright matching
        page.route("**/api/screenwriting/storybook/upload", handle_upload)
        page.route("**/api/screenwriting/storybook", handle_get_docs)

        try:
            print("Navigating...")
            page.goto("http://localhost:4173")

            # Navigate to Storybook
            print("Opening Agent...")
            page.get_by_role("button", name="Open Agent").click()
            time.sleep(0.5)
            page.locator("select.ui-select").select_option("screenwriting")
            time.sleep(0.5)
            page.get_by_text("Storybook").click()
            time.sleep(0.5)

            # 1. Verify Document Card <button>
            print("Verifying Document Card Semantics...")
            card = page.locator(".document-card").first
            expect(card).to_be_visible()
            tag = card.evaluate("el => el.tagName")
            print(f"Card Tag: {tag}")
            assert tag.lower() == "button", f"Expected 'button', got '{tag}'"
            print("✅ Document Card is a <button>")

            # 2. Verify Icon Button Aria Label
            print("Verifying Icon Button Accessibility...")
            card.click()
            icon_btn = page.locator("button.btn-icon").first
            expect(icon_btn).to_be_visible()
            label = icon_btn.get_attribute("aria-label")
            print(f"Icon Button Label: {label}")
            assert label == "Draft Dialogue", f"Expected 'Draft Dialogue', got '{label}'"
            print("✅ Icon Button has correct aria-label")

            # Go back
            page.get_by_role("button", name="Back to List").click()

            # 3. Verify Form Accessibility
            print("Verifying Upload Form Accessibility...")
            page.get_by_role("button", name="New Document").click()

            # Check labels
            assert page.locator("label[for='doc-title']").count() == 1, "Missing Title Label"
            assert page.locator("label[for='doc-content']").count() == 1, "Missing Content Label"
            print("✅ Form labels present")

            # 4. Verify Loading State
            print("Verifying Ingest Loading State...")
            page.fill("#doc-title", "New Doc")
            page.fill("#doc-content", "Content")

            ingest_btn = page.get_by_role("button", name="Ingest")
            ingest_btn.click()

            # Check pending state
            # Button should change to "Ingesting..." and be disabled
            loading_btn = page.get_by_role("button", name="Ingesting...")
            expect(loading_btn).to_be_visible()
            expect(loading_btn).to_be_disabled()
            print("✅ Loading state verified (text and disabled)")

            # Take verification screenshot of this state
            page.screenshot(path="verification/ux_verified.png")
            print("📸 Screenshot taken: verification/ux_verified.png")

            # Complete the request
            if upload_routes:
                print("Fulfilling upload request...")
                upload_routes[0].fulfill(status=200, body='{"success":true}')
                # Verify we return to list or form closes?
                # Code: setShowUpload(false)
                # So form should disappear.
                time.sleep(0.5)
                expect(page.locator(".storybook-upload")).not_to_be_visible()
                print("✅ Form closed after success")
            else:
                print("❌ Warning: Upload route was never hit!")

        except Exception as e:
            print(f"❌ Error: {e}")
            page.screenshot(path="verification/ux_error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_ux()

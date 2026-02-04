import json
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Mock the API response
    mock_data = {
        "documents": [
            {
                "id": "doc1",
                "name": "Test Screenplay",
                "description": "A test script",
                "uploaded_at": "2023-01-01T00:00:00Z",
                "tags": ["test"],
                "chapters": [
                    {
                        "id": "chap1",
                        "title": "The Beginning",
                        "beats": [
                            {
                                "id": "beat1",
                                "label": "Opening Image",
                                "visual_prompt": "A dark room",
                                "summary": "Fade in to..."
                            },
                            {
                                "id": "beat2",
                                "label": "Theme Stated",
                                "visual_prompt": "A conversation",
                                "summary": "They talk about..."
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Intercept the API call
    # Use generic glob to match any host
    page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps(mock_data)
    ))

    try:
        print("Navigating to app...")
        page.goto("http://localhost:5173")

        # Open Agent Launcher
        print("Opening Agent Modal...")
        page.locator(".agent-launcher").click()

        # Wait for modal content
        page.wait_for_selector(".ui-select")

        # Select Screenwriting Mode
        print("Switching to Screenwriting UI...")
        page.locator(".ui-select").first.select_option("screenwriting")

        # Click Storybook Tab
        print("Clicking Storybook Tab...")
        page.locator("#tab-storybook").click()

        # Wait for document list to load (uses our mock)
        print("Waiting for document list...")
        # Check if error message appeared
        if page.locator(".error-message").is_visible():
            print("ERROR MESSAGE VISIBLE:", page.locator(".error-message").text_content())

        page.wait_for_selector(".document-card", timeout=5000)

        # VERIFY 1: Delete Button ARIA Label
        print("Verifying Delete Button ARIA Label...")
        delete_btn = page.locator(".delete-doc-btn").first
        expect(delete_btn).to_have_attribute("aria-label", "Delete Test Screenplay")
        print("✅ Delete Button ARIA label confirmed.")

        # VERIFY 2: Form Labels (Click "+ New Document")
        print("Verifying Form Labels...")
        page.get_by_role("button", name="+ New Document").click()

        # Check if clicking the label focuses the input
        page.get_by_text("Document Title").click()
        expect(page.locator("#doc-title")).to_be_focused()
        print("✅ Label 'Document Title' focuses input #doc-title.")

        # Close upload form
        page.get_by_role("button", name="Cancel").click()

        # VERIFY 3: Document View & Dead Button
        print("Entering Document View...")
        page.get_by_text("Test Screenplay").first.click()

        # Wait for beats
        page.wait_for_selector(".beat-card")

        # Check Back Button ARIA hidden arrow
        print("Verifying Back Button Arrow hidden...")
        back_arrow = page.locator(".btn-back span").first
        expect(back_arrow).to_have_attribute("aria-hidden", "true")
        print("✅ Back button arrow is aria-hidden.")

        # Check Emoji Icons
        print("Verifying Emoji Icons...")
        # First beat is even index (0) -> Cinema (🎬)
        beat1_icon = page.locator(".visual-hint span").first
        expect(beat1_icon).to_have_attribute("role", "img")
        expect(beat1_icon).to_have_attribute("aria-label", "Cinema")
        print("✅ Cinema emoji has role='img' and aria-label='Cinema'.")

        # Second beat is odd index (1) -> Visual (👁️)
        beat2_icon = page.locator(".visual-hint span").nth(1)
        expect(beat2_icon).to_have_attribute("role", "img")
        expect(beat2_icon).to_have_attribute("aria-label", "Visual")
        print("✅ Visual emoji has role='img' and aria-label='Visual'.")

        # Check Dead Button
        print("Verifying Dead Button...")
        draft_btn = page.locator(".btn-draft").first
        expect(draft_btn).to_be_disabled()
        expect(draft_btn).to_have_attribute("title", "Feature coming soon")
        print("✅ Draft Scene button is disabled and has tooltip.")

        # Screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/storybook_verified.png")

    except Exception as e:
        print(f"FAILED: {e}")
        page.screenshot(path="verification/failed_debug.png")
        raise

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)

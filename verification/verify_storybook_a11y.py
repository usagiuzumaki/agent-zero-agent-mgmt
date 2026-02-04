from playwright.sync_api import sync_playwright, expect

def test_storybook_a11y():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock the API response
        page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='''{
                "documents": [
                    {
                        "id": "1",
                        "name": "The Hidden Fortress",
                        "description": "A tale of samurai and princesses.",
                        "uploaded_at": "2023-10-27T10:00:00Z",
                        "tags": ["Action", "Draft"],
                        "chapters": [
                             {
                                "id": "c1",
                                "title": "The Escape",
                                "beats": [
                                    {"id": "b1", "label": "Opening", "visual_prompt": "Wide shot of desert", "summary": "Two peasants argue."}
                                ]
                             }
                        ]
                    }
                ]
            }'''
        ))

        # Navigate to app
        page.goto("http://localhost:5173/")

        # 1. Open Agent Modal
        # The launcher is a button at the bottom right.
        # Looking at theme.css: .agent-launcher
        page.locator(".agent-launcher").click()

        # 2. Switch to Screenwriting Mode
        # The select has aria-label="Select Interface Mode"
        page.get_by_label("Select Interface Mode").select_option("screenwriting")

        # 3. Click Storybook Tab
        # role="tab", name="Storybook" (it has an emoji and text, so partial text or regex)
        page.get_by_role("tab", name="Storybook").click()

        # 4. Wait for documents to load
        # We expect to see "The Hidden Fortress"
        expect(page.get_by_text("The Hidden Fortress")).to_be_visible()

        # 5. Verify the Delete Button Accessibility
        # Find the delete button for this document.
        # It should have the aria-label "Delete document: The Hidden Fortress"
        delete_btn = page.get_by_role("button", name="Delete document: The Hidden Fortress")
        expect(delete_btn).to_be_visible()

        # Also check the icon inside has role="img"
        # We can't easily check internal roles of children with user-facing locators,
        # but if we found the button by name, the aria-label is working!

        # 6. Verify Visual Hint Accessibility (requires opening the document)
        # Click the document to open it
        page.get_by_text("The Hidden Fortress").click()

        # Wait for beats
        expect(page.get_by_text("The Escape")).to_be_visible()

        # Find the visual hint emoji
        # It should have role="img" and label "Cinematic shot" (since index 0 is even)
        visual_hint = page.get_by_role("img", name="Cinematic shot")
        expect(visual_hint).to_be_visible()

        # Take screenshot
        page.screenshot(path="verification/storybook_a11y.png")
        print("Verification successful!")

        browser.close()

if __name__ == "__main__":
    test_storybook_a11y()

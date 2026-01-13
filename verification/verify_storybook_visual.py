from playwright.sync_api import sync_playwright, expect

def test_storybook_visual(page):
    # Mock the API responses
    page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='''{"documents": [
            {
                "id": "doc1",
                "name": "Screenplay Draft v1",
                "description": "First draft of the opening scene.",
                "uploaded_at": "2023-10-27",
                "tags": ["Draft", "Sci-Fi"],
                "chapters": []
            },
            {
                "id": "doc2",
                "name": "Character Bible",
                "description": "Backgrounds for all main characters.",
                "uploaded_at": "2023-10-28",
                "tags": ["Reference"],
                "chapters": []
            }
        ]}'''
    ))

    page.route("**/api/screenwriting/storybook/delete", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"success": true}'
    ))

    # Navigate to app
    page.goto("http://localhost:4173")

    # Open Agent Modal
    page.get_by_role("button", name="Open Agent").click()

    # Switch to Screenwriting Mode
    page.locator("select.ui-select").first.select_option("screenwriting")

    # Switch to Storybook Tab
    page.get_by_role("tab", name="Storybook").click()

    # Wait for content
    page.locator(".document-card").first.wait_for()

    # Hover over the first delete button to show the hover state if any (and verify it's there)
    delete_btn = page.locator("button[aria-label*='Delete']").first
    delete_btn.hover()

    # Take screenshot of the document list with the new delete buttons
    page.screenshot(path="verification/storybook_delete_visual.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_storybook_visual(page)
        finally:
            browser.close()

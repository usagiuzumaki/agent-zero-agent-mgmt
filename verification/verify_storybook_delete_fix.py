import pytest
from playwright.sync_api import sync_playwright, expect
import time

@pytest.fixture(scope="module")
def page_fixture():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_storybook_delete_button_present(page_fixture):
    page = page_fixture

    # Mock the API responses
    page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"documents": [{"id": "doc1", "name": "Test Doc", "description": "Desc", "uploaded_at": "2023-01-01", "tags": [], "chapters": []}]}'
    ))

    # Mock delete endpoint to avoid 404
    page.route("**/api/screenwriting/storybook/delete", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"success": true}'
    ))

    page.goto("http://localhost:4173")

    # 1. Open Agent Modal
    page.get_by_role("button", name="Open Agent").click()

    # 2. Switch to Screenwriting Mode
    # Use select_option on the native select
    page.locator("select.ui-select").first.select_option("screenwriting")

    # 3. Switch to Storybook Tab
    page.get_by_role("tab", name="Storybook").click()

    # 4. Check for document card
    doc_card = page.locator(".document-card").first
    expect(doc_card).to_be_visible()

    # 5. Assert delete button exists
    delete_btn = doc_card.locator("button[aria-label*='Delete']")
    expect(delete_btn).to_be_visible()

    # 6. Verify clicking delete triggers confirmation
    # We need to handle the dialog
    page.on("dialog", lambda dialog: dialog.accept())

    # Click delete
    delete_btn.click()

    # If the button works, we expect a request to delete (which we mocked)
    # and then a refresh of the list.
    # Since we mocked the list again with the same content, it will still show the doc.
    # But the test here is just to verify the button exists and is clickable.

if __name__ == "__main__":
    pass

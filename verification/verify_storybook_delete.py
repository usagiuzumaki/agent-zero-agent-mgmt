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

def test_storybook_delete_button_missing(page_fixture):
    page = page_fixture

    # Mock the API responses
    page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"documents": [{"id": "doc1", "name": "Test Doc", "description": "Desc", "uploaded_at": "2023-01-01", "tags": [], "chapters": []}]}'
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

    # 5. Assert NO delete button exists currently
    # We look for a button with text "Delete" or aria-label containing Delete
    delete_btn = doc_card.locator("button[aria-label*='Delete']")
    expect(delete_btn).not_to_be_visible()

    # Also check for text "Delete"
    delete_text = doc_card.get_by_text("Delete")
    expect(delete_text).not_to_be_visible()

if __name__ == "__main__":
    pass

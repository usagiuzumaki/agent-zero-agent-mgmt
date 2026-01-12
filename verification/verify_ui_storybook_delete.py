import json
from playwright.sync_api import sync_playwright, expect
import os

def mock_storybook_api(route):
    if route.request.method == "GET" and "storybook" in route.request.url:
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "documents": [
                    {
                        "id": "doc1",
                        "name": "The Great Adventure",
                        "description": "A story about a hero.",
                        "uploaded_at": "2023-10-27T10:00:00.000000",
                        "tags": ["Action", "Adventure"],
                        "chapters": []
                    }
                ]
            })
        )
    elif route.request.method == "POST" and "delete" in route.request.url:
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"message": "Document deleted successfully"})
        )
    else:
        route.continue_()

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Route backend calls
    page.route("**/api/screenwriting/storybook*", mock_storybook_api)

    # We need to serve the static frontend. Since we don't have the full dev server running easily,
    # we can try to point to the built assets if they exist, or use the dev server if we start it.
    # However, memory says: "Verification of ui-kit-react features requires building the project
    # (pnpm --dir ui-kit-react build) and running the Vite preview server (pnpm --dir ui-kit-react preview -- --port 4173)"

    page.goto("http://localhost:4173")

    # Navigate to Screenwriting -> Storybook
    # First, open the agent launcher if needed, but the default might be the chat.
    # We need to select "Screenwriting" mode.

    # Wait for the mode selector to appear (it's in AgentModal)
    # Actually, looking at App.jsx: AgentLauncher opens AgentModal.
    # The modal contains the select box.

    page.locator('.agent-launcher').click()

    # Select screenwriting mode
    page.locator('select.ui-select').first.select_option('screenwriting')

    # Click "Storybook" tab
    page.get_by_role("tab", name="Storybook").click()

    # Check if document card is visible
    expect(page.get_by_text("The Great Adventure")).to_be_visible()

    # Hover over the card to reveal delete button
    page.locator(".document-card").hover()

    # Take screenshot of the hover state with delete button
    page.screenshot(path="verification/storybook_delete_hover.png")

    # Click delete button and handle confirm
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("button[title='Delete Document']").click()

    # Verify that we would see a success (in a real app, the doc would disappear,
    # but here our mock GET still returns it unless we make the mock smarter.
    # For now, we just want to verify the button exists and is clickable).

    browser.close()

with sync_playwright() as playwright:
    run(playwright)

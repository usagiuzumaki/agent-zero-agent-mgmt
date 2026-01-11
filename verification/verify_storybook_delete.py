import json
from playwright.sync_api import sync_playwright, expect

def verify_storybook_delete():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Mock data
        documents = [
            {
                "id": "doc1",
                "name": "My Great Script",
                "description": "A masterpiece",
                "uploaded_at": "2023-10-27T10:00:00",
                "tags": ["sci-fi"],
                "chapters": [],
                "suggestions": []
            }
        ]

        # Route API
        page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({"documents": documents})
        ))

        def handle_delete(route):
            print("Delete requested for doc1")
            documents.clear()
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({"message": "Document deleted successfully"})
            )

        page.route("**/api/screenwriting/storybook/delete", handle_delete)

        print("Navigating...")
        page.goto("http://localhost:4173")

        # Open Agent Modal
        page.get_by_role("button", name="Open Agent").click()

        # Select Screenwriting agent
        try:
             page.locator("select").first.select_option(value="screenwriting")
        except:
             try:
                 page.locator("select").first.select_option(label="Screenwriting")
             except:
                 print("Could not select 'Screenwriting'. Attempting to proceed anyway (might be default).")

        # Close modal
        page.mouse.click(10, 10)

        # Click Storybook tab
        print("Clicking Storybook tab...")
        try:
            page.get_by_role("tab", name="Storybook").click(timeout=3000)
        except:
            try:
                page.get_by_role("button", name="Storybook").click(timeout=3000)
            except:
                print("Could not find Storybook tab. Taking debug screenshot.")
                page.screenshot(path="verification/debug_tabs.png")
                raise

        # Now we should see the document
        expect(page.get_by_text("My Great Script")).to_be_visible()

        page.screenshot(path="verification/before_delete.png")

        # Delete
        page.on("dialog", lambda dialog: dialog.accept())
        page.get_by_label("Delete My Great Script").click()

        expect(page.get_by_text("My Great Script")).not_to_be_visible()

        page.screenshot(path="verification/after_delete.png")
        print("Verified!")
        browser.close()

if __name__ == "__main__":
    verify_storybook_delete()

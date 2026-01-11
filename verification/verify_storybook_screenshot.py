
import asyncio
from playwright.async_api import async_playwright
import time
import os
import subprocess

async def verify_storybook_delete_screenshot():
    print("Starting Storybook screenshot verification...")

    # Start vite preview server
    server = subprocess.Popen(['pnpm', '--dir', 'ui-kit-react', 'preview', '--', '--port', '4173'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait a bit for server
    await asyncio.sleep(5)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async def handle_storybook(route):
            await route.fulfill(json={
                "documents": [
                    {
                        "id": "doc1",
                        "name": "Screenplay Draft 1",
                        "description": "A draft screenplay for testing",
                        "uploaded_at": "2023-10-27T10:00:00Z",
                        "tags": ["draft", "sci-fi"],
                        "chapters": []
                    }
                ]
            })

        async def handle_delete(route):
             if route.request.method == 'POST':
                 await route.fulfill(json={"ok": True})
             else:
                 await route.continue_()

        try:
            # Mock API
            await page.route('**/api/screenwriting/storybook', handle_storybook)
            await page.route('**/api/screenwriting/storybook/delete', handle_delete)

            await page.goto("http://localhost:4173")

            # Navigate to Storybook
            await page.click('button.agent-launcher')
            await page.locator('select.ui-select').first.select_option(label='Screenwriting')
            await page.click('button:has-text("Storybook")')

            # Wait for doc
            await page.wait_for_selector('h4:has-text("Screenplay Draft 1")')

            # Take screenshot of the document list with delete button visible
            # We need to hover to see the delete button in list view?
            # CSS: .document-card:hover ...
            # Playwright hover
            await page.hover('.document-card')

            # Or we can click to view and see the big delete button
            await page.screenshot(path="verification/storybook_list_view.png")

            # Click to view
            await page.click('.document-card')
            await page.wait_for_selector('.document-view')

            # Take screenshot of document view with Delete Document button
            await page.screenshot(path="verification/storybook_doc_view.png")

            print("Screenshots captured.")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()
            server.terminate()

if __name__ == "__main__":
    asyncio.run(verify_storybook_delete_screenshot())

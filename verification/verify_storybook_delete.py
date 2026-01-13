import asyncio
import os
import subprocess
import time
import requests
from playwright.async_api import async_playwright

async def run_verification():
    # Start the preview server
    print("Starting preview server...")
    # Ensure build exists
    subprocess.run(["pnpm", "--dir", "ui-kit-react", "build"], check=True)

    server_process = subprocess.Popen(
        ["pnpm", "--dir", "ui-kit-react", "preview", "--", "--port", "4173"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for server
    for i in range(20):
        try:
            requests.get("http://localhost:4173")
            print("Server is up!")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            print("Waiting for server...")
    else:
        print("Server failed to start")
        server_process.kill()
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Mock APIs
        await page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"documents": [{"id": "doc1", "name": "Test Script", "description": "A test script", "uploaded_at": "2024-01-01T00:00:00Z", "tags": ["Draft"]}]}'
        ))

        await page.route("**/api/screenwriting/storybook/delete", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"success": true}'
        ))

        # Navigate
        print("Navigating to app...")
        await page.goto("http://localhost:4173")

        # 1. Open Agent Modal
        print("Opening agent modal...")
        await page.click("button.agent-launcher")

        # 2. Switch to Screenwriting Mode
        print("Switching to Screenwriting mode...")
        await page.locator("select.ui-select").first.select_option("screenwriting")

        # 3. Switch to Storybook Tab
        print("Switching to Storybook tab...")
        await page.click("button:has-text('Storybook')")

        # Wait for content
        print("Waiting for document list...")
        await page.wait_for_selector("text=Test Script", timeout=5000)

        # Check for Delete button
        delete_btn = page.locator("button[aria-label='Delete Test Script']")

        if await delete_btn.count() > 0 and await delete_btn.is_visible():
            print("SUCCESS: Delete button exists!")
        else:
            print("FAILURE: Delete button is missing!")

        # Take screenshot
        await page.screenshot(path="verification/storybook_after.png")

        await browser.close()

    server_process.kill()

if __name__ == "__main__":
    asyncio.run(run_verification())

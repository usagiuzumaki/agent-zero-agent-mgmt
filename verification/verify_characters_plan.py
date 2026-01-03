
import asyncio
from playwright.async_api import async_playwright, expect

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Mock the backend API calls
        await page.route("/api/screenwriting/all", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"character_profiles": {"characters": []}}'
        ))

        await page.route("/api/screenwriting/character/add", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"success": true}'
        ))

        # We need to serve the static files or run the vite server.
        # Since running vite might be tricky in the background without blocking,
        # I'll rely on the preview server if I can start it,
        # OR I can just verify the code structure via unit tests or similar if UI visual verification is too hard.
        # But wait, I can run `vite preview` in the background.

        # Actually, let's try to run the preview server in a separate bash session step first.
        # This script assumes the server is running on port 4173.
        try:
            await page.goto("http://localhost:4173")

            # Navigate to Screenwriting -> Characters (this might need navigation steps)
            # Assuming the app starts at home and we need to click "Open Agent" then "Screenwriting"

            # Wait for the app to load
            await expect(page.get_by_text("Select an Agent Mode")).to_be_visible()

            # Click Screenwriting
            await page.get_by_role("button", name="Screenwriting").click()

            # Click Characters tab
            await page.get_by_role("tab", name="Characters").click()

            # Open Add Character form
            await page.get_by_role("button", name="+ Add Character").click()

            # Fill out form
            await page.get_by_label("Name").fill("Test Character")

            # Verify the labels work by clicking them and checking focus?
            # Or just verify the label-for relationship via attribute check?
            # Playwright's get_by_label relies on this relationship, so if the above fill works, the accessibility fix is verified!

            # Click Save to see the spinner
            # We can't easily capture the spinner in a static screenshot unless we delay the response.
            # Let's update the mock to delay.
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

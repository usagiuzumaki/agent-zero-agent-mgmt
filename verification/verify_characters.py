
import asyncio
from playwright.async_api import async_playwright, expect

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Mock the backend API calls using wildcards to ensure we catch them
        await page.route("**/api/screenwriting/all", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"character_profiles": {"characters": []}}'
        ))

        # Mock add with a delay to capture the spinner
        async def handle_add(route):
            await asyncio.sleep(2) # Delay for 2 seconds to be safe
            await route.fulfill(
                status=200,
                content_type="application/json",
                body='{"success": true}'
            )

        await page.route("**/api/screenwriting/character/add", handle_add)

        try:
            # Go to the app
            await page.goto("http://localhost:4173")

            # Click "Open Agent"
            await page.get_by_role("button", name="Open Agent").click()

            # Select Screenwriting from the dropdown
            await page.locator(".ui-select").select_option("screenwriting")

            # Wait for "Screenwriting Studio"
            await expect(page.get_by_role("heading", name="Screenwriting Studio")).to_be_visible()

            # Click Characters tab
            await page.get_by_role("tab", name="Characters").click()

            # Open Add Character form
            await page.get_by_role("button", name="+ Add Character").click()

            # Fill out form using labels (verifies accessibility)
            await page.get_by_label("Name").fill("Test Character")

            # Click Save
            save_btn = page.get_by_role("button", name="Save Character")
            await save_btn.click()

            # Take screenshot immediately to capture "Saving..." state
            # Wait for "Saving..." text to appear to ensure state change
            await expect(page.get_by_text("Saving...")).to_be_visible()

            await page.screenshot(path="verification/characters_loading.png")
            print("Screenshot taken: verification/characters_loading.png")

        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(path="verification/error.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

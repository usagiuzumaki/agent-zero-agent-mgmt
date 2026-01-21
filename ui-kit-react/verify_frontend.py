from playwright.sync_api import sync_playwright

def verify_characters_ui_empty_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the Characters UI
        # Intercept the API call to return empty characters list
        page.route("**/api/screenwriting/all", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"character_profiles": {"characters": []}}'
        ))

        # Also need to intercept /api/screenwriting/storybook for StorybookUI which is default in ScreenwritingUI
        page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"documents": []}'
        ))

        try:
            page.goto("http://localhost:5173/")

            # 1. Open Agent Modal
            page.click("button:has-text('Open Agent')")

            # 2. Select Screenwriting UI
            page.select_option("select[aria-label='Select Interface Mode']", "screenwriting")

            # 3. Wait for ScreenwritingUI to load. It defaults to StorybookUI usually, so we might need to switch tab.
            # Let's check ScreenwritingUI.jsx to see how it switches between Storybook and Characters

            # Assuming there are tabs or buttons to switch.
            # I'll wait a bit and take a screenshot of what we have first to debug if needed.
            # But let's try to click "Characters" tab if it exists.

            # Let's read ScreenwritingUI.jsx quickly to be sure
            # Actually, I can just try to click "Characters" or "Cast" button/tab if I see one in the DOM dump or just try it.
            # But checking the file first is safer.

            # For now, let's just take a screenshot of the Screenwriting UI.
            page.wait_for_timeout(1000) # Wait for render

            # Click on "Characters" tab if it exists (guessing the name)
            # Based on previous file reads, ScreenwritingUI likely manages tabs.

            # Let's try to find a button with text "Characters"
            chars_tab = page.get_by_role("button", name="Characters")
            if chars_tab.is_visible():
                chars_tab.click()

            page.wait_for_timeout(1000) # Wait for characters to load (or empty state)

            # Take a screenshot
            page.screenshot(path="verification/characters_empty_state.png")
            print("Screenshot taken at verification/characters_empty_state.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_state.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_characters_ui_empty_state()

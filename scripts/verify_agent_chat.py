from playwright.sync_api import sync_playwright

def verify_agent_chat():
    """
    Verifies that the AgentChat component loads correctly.
    Requires the frontend dev server to be running on http://localhost:5173.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to http://localhost:5173...")
            page.goto("http://localhost:5173")

            # Click 'Open Agent' button
            print("Clicking 'Open Agent'...")
            page.get_by_text("Open Agent", exact=True).click()

            # Wait for 'Aria' heading in EmptyState
            print("Waiting for 'Aria' heading...")
            page.get_by_role("heading", name="Aria", exact=True).wait_for()

            # Take screenshot (optional, but good for debugging)
            # print("Taking screenshot...")
            # page.screenshot(path="agent_chat_verified.png")

            print("Verification successful: AgentChat loaded correctly.")

        except Exception as e:
            print(f"Error: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_agent_chat()

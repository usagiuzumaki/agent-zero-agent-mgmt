from playwright.sync_api import sync_playwright, expect

def test_agent_chat_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to app
        page.goto("http://localhost:5173/")

        # Open Agent Modal
        page.locator(".agent-launcher").click()

        # Expect to see "Aria" (from EmptyState title)
        # or the input box
        expect(page.get_by_label("Message input")).to_be_visible()

        # Check if EmptyState renders (it should if no messages)
        # The EmptyState has title "Aria"
        expect(page.get_by_text("Aria", exact=True)).to_be_visible()

        print("AgentChat loads successfully!")
        browser.close()

if __name__ == "__main__":
    test_agent_chat_loads()

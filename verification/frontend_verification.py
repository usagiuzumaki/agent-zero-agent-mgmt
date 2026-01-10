from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the UI
        page.goto("http://localhost:4177")

        # Open the agent
        page.click("button.agent-launcher")

        # Wait for modal
        page.wait_for_selector(".agent-modal")

        # Add many messages to force scroll
        print("Adding messages...")
        input_box = page.locator(".agent-chat textarea")
        send_btn = page.locator(".agent-chat button[aria-label='Send message']")

        for i in range(15):
            input_box.fill(f"Message {i} - " + "A" * 50)
            send_btn.click()
            page.wait_for_timeout(50)

        page.wait_for_timeout(1000)

        # Take screenshot
        page.screenshot(path="verification/frontend_scroll.png")
        print("Screenshot taken.")

        browser.close()

if __name__ == "__main__":
    verify_frontend()

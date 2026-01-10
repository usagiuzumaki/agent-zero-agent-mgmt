import time
from playwright.sync_api import sync_playwright

def verify_scroll():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the UI
        page.goto("http://localhost:4177")

        # Open the agent
        page.click("button.agent-launcher")

        # Wait for modal
        page.wait_for_selector(".agent-modal")

        # Helper to get scroll info
        def get_scroll_info(selector):
            return page.evaluate(f"""() => {{
                const el = document.querySelector('{selector}');
                if (!el) return {{ scrollTop: 0, scrollHeight: 0, clientHeight: 0 }};
                return {{
                    scrollTop: el.scrollTop,
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight
                }};
            }}""")

        # Add many messages to force scroll
        print("Adding messages...")
        input_box = page.locator(".agent-chat textarea")
        send_btn = page.locator(".agent-chat button[aria-label='Send message']")

        for i in range(20):
            input_box.fill(f"Message {i} - " + "A" * 50) # Long message
            send_btn.click()
            # Wait a bit for React to render
            page.wait_for_timeout(50)

        # Check if the modal or messages container is scrolling
        # Current implementation: AgentModal scrolls
        modal_scroll = get_scroll_info(".agent-modal")
        messages_scroll = get_scroll_info(".agent-chat .messages")

        print(f"Modal Scroll: {modal_scroll}")
        print(f"Messages Scroll: {messages_scroll}")

        # Check if we are at the bottom of the scroll container
        # Note: in new impl, .messages is the scroll container
        scroll_container = messages_scroll

        # Give smooth scroll time to finish
        if scroll_container['scrollHeight'] - scroll_container['scrollTop'] - scroll_container['clientHeight'] > 20:
             print("Waiting for smooth scroll...")
             page.wait_for_timeout(1000)
             messages_scroll = get_scroll_info(".agent-chat .messages")
             scroll_container = messages_scroll

        is_at_bottom = abs(scroll_container['scrollHeight'] - scroll_container['clientHeight'] - scroll_container['scrollTop']) < 20
        print(f"Is at bottom: {is_at_bottom}")

        if not is_at_bottom:
            print("FAILURE: Did not auto-scroll to bottom.")
        else:
            print("SUCCESS: Auto-scrolled to bottom (or content fits).")

        # Now scroll up
        print("Scrolling up...")
        page.evaluate("document.querySelector('.agent-chat .messages').scrollTop = 0")
        page.wait_for_timeout(500)

        # Add another message
        input_box.fill("Message while scrolled up")
        send_btn.click()
        page.wait_for_timeout(100)

        # Check if we stayed at top (Smart Scroll) or jumped to bottom
        new_scroll = get_scroll_info(".agent-chat .messages")
        print(f"New Scroll: {new_scroll}")

        if new_scroll['scrollTop'] > 100:
             print("FAILURE: Auto-scrolled even though user was at top.")
        else:
             print("SUCCESS: Smart scroll respected user position.")

        browser.close()

if __name__ == "__main__":
    verify_scroll()

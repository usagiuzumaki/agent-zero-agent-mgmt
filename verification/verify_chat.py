from playwright.sync_api import sync_playwright

def verify_chat_textarea():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use wildcard matching for the network request interception if needed
        # context = browser.new_context(record_video_dir="verification/videos")
        page = browser.new_page()

        try:
            # We need to navigate to the app.
            # Note: The app might redirect to / or start at /
            page.goto("http://localhost:4173")

            # The agent chat is likely inside one of the UIs.
            # We need to click "Open Agent" -> "E-Girl Mode" or similar to see the chat.
            # Based on memory, there is an AgentLauncher.

            # Click the launcher button if it exists
            page.get_by_role("button", name="Open Agent").click()

            # Click "E-Girl Mode" (or just wait if it defaults)
            # Let's see what happens.
            page.wait_for_timeout(1000)

            # Select "E-Girl Mode" from the dropdown/menu if needed.
            # Inspecting existing tests or code would help, but I'll try generic text.
            if page.get_by_text("E-Girl Mode").is_visible():
                page.get_by_text("E-Girl Mode").click()

            # Now look for the textarea
            textarea = page.get_by_label("Message input")

            # Check if it is a textarea
            tag_name = textarea.evaluate("el => el.tagName.toLowerCase()")
            print(f"Tag name: {tag_name}")

            if tag_name != 'textarea':
                raise Exception(f"Expected textarea, got {tag_name}")

            # Check placeholder
            placeholder = textarea.get_attribute("placeholder")
            print(f"Placeholder: {placeholder}")

            if "Shift+Enter" not in placeholder:
                raise Exception("Placeholder text update verification failed")

            # Type some text with Shift+Enter
            textarea.fill("Line 1")
            textarea.press("Shift+Enter")
            textarea.type("Line 2")

            # Take screenshot
            page.screenshot(path="verification/chat_textarea.png")
            print("Screenshot saved to verification/chat_textarea.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_chat_textarea()

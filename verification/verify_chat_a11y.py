from playwright.sync_api import sync_playwright, expect
import sys

def run():
    print("Starting Chat Accessibility Verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to the app
            print("Navigating to http://localhost:4173")
            page.goto("http://localhost:4173")

            # Open Agent
            print("Opening Agent Modal...")
            page.get_by_role("button", name="Open Agent").click()

            # Wait for chat container
            messages_container = page.locator(".agent-chat .messages")
            expect(messages_container).to_be_visible()

            # Check for accessibility attributes
            print("Checking for accessibility attributes...")

            # 1. Check role="log"
            role = messages_container.get_attribute("role")
            if role != "log":
                print(f"FAIL: Expected role='log', but got '{role}'")
            else:
                print("PASS: role='log' found.")

            # 2. Check aria-live="polite"
            aria_live = messages_container.get_attribute("aria-live")
            if aria_live != "polite":
                print(f"FAIL: Expected aria-live='polite', but got '{aria_live}'")
            else:
                print("PASS: aria-live='polite' found.")

            # 3. Check tabindex="0"
            tabindex = messages_container.get_attribute("tabindex")
            if tabindex != "0":
                print(f"FAIL: Expected tabindex='0', but got '{tabindex}'")
            else:
                print("PASS: tabindex='0' found.")

            # 4. Check aria-label
            aria_label = messages_container.get_attribute("aria-label")
            if not aria_label:
                print(f"FAIL: Expected aria-label to be present, but got '{aria_label}'")
            else:
                print(f"PASS: aria-label='{aria_label}' found.")

            # Check for empty state text
            print("Checking for empty state text...")
            expect(page.get_by_text("Start a conversation...")).to_be_visible()
            print("PASS: Empty state text found.")

            # Take screenshot
            screenshot_path = "verification/chat_a11y.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

            # Final Assertion for script exit code
            if role != "log" or aria_live != "polite" or tabindex != "0" or not aria_label:
                print("VERIFICATION FAILED")
                sys.exit(1)

            print("VERIFICATION PASSED")

        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()

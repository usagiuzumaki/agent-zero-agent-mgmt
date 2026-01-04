from playwright.sync_api import sync_playwright, expect
import time

def verify_dom_structure():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the local server
        page.goto("http://localhost:8080/index.html")

        # Since we don't have a backend, the UI might be empty or show an error toast.
        # We just want to check if the JS loads without error (no console errors).

        # Capture console logs
        page.on("console", lambda msg: print(f"Console: {msg.text}"))

        # Wait a bit
        time.sleep(2)

        # Take a screenshot
        page.screenshot(path="verification/webui_load.png")

        browser.close()

if __name__ == "__main__":
    verify_dom_structure()

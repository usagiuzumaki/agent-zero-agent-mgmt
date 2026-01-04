import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:4173")
        page.wait_for_load_state("networkidle")

        # Click "Open Agent"
        if page.get_by_role("button", name="Open Agent").is_visible():
            page.get_by_role("button", name="Open Agent").click()

        # Select "Screenwriting"
        page.select_option("select.ui-select", "screenwriting")

        # Wait for "Characters" tab button and click it
        page.get_by_role("tab", name="Characters").click()

        # Wait for "Cast of Characters" header to confirm we are in Characters UI
        page.wait_for_selector("text=Cast of Characters")

        # Click "+ Add Character"
        page.get_by_role("button", name="+ Add Character").click()

        # Fill form using LABELS (verifies htmlFor)
        page.get_by_label("Name").fill("Test Character")
        page.get_by_label("Role").select_option("Protagonist")

        # Intercept add request to delay it
        def handle_route(route):
            time.sleep(2)
            route.fulfill(status=200, body='{"status":"ok"}')

        page.route("**/api/screenwriting/character/add", handle_route)

        # Click Save
        save_btn = page.get_by_role("button", name="Save Character")
        save_btn.click()

        # Wait a tiny bit for React state update
        time.sleep(0.5)

        # Screenshot
        page.screenshot(path="verification/saving_state.png")

        browser.close()

if __name__ == "__main__":
    run()

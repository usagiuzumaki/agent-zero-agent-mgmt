import time
from playwright.sync_api import sync_playwright

def verify_spinner():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Mock the backend responses
        page.route("**/api/screenwriting/all", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"character_profiles": {"characters": []}}'
        ))

        # Important: Delay the add response so we can see the spinner
        def handle_add(route):
            time.sleep(2)
            route.fulfill(status=200, body='{}')

        page.route("**/api/screenwriting/character/add", handle_add)

        # Navigate to the app (Preview server)
        page.goto("http://localhost:4173")

        # Open Agent Launcher
        page.get_by_role("button", name="Open Agent").click()

        # Select Screenwriting mode
        page.locator('select.ui-select').select_option('screenwriting')

        # In Screenwriting UI, find "Characters" tab/button
        # The tab has text "Characters". But in CharactersUI.jsx we see "Cast of Characters" header.
        # Wait, ScreenwritingUI likely has tabs. CharactersUI is just the component.
        # I don't see ScreenwritingUI source, but likely it has tabs.
        # Let's try to just wait for "+ Add Character" button which is in CharactersUI.
        # If it's the default tab or we can find the tab button.

        # Let's try to click the tab "Characters" again, but maybe use a less strict locator or wait longer.
        try:
             page.get_by_text("Characters", exact=True).click(timeout=5000)
        except:
             print("Could not find 'Characters' text to click. Maybe it is already active?")

        # Click "+ Add Character"
        page.get_by_text("+ Add Character").click()

        # Fill form - The label is "Name"
        # The input has no id, but is inside a form-group with label "Name".
        # <label>Name</label><input ...>
        # Playwright get_by_label matches <label> text to associated input.
        # Since the input is NOT nested inside the label and has no id/for, explicit association is missing.
        # This is an accessibility issue! I should fix it as Palette, but for now I need to verify.
        # I'll use locator based on layout or placeholders if any. No placeholder.
        # I'll use CSS selector.
        page.locator('input').first.fill("Test Spinner") # Risky

        # Better locator: input after label "Name"
        # page.locator('label:has-text("Name") + input').fill("Test Spinner") # If adjacent
        # In the code: <label>Name</label><input ...> yes, they are siblings in flex col.

        # Let's try finding the input by traversing.
        name_input = page.locator('.form-group').filter(has_text="Name").locator('input')
        name_input.fill("Test Spinner")

        # Click Save
        save_btn = page.get_by_role("button", name="Save Character")
        save_btn.click(no_wait_after=True)

        # Verify spinner exists
        spinner = page.locator('div[role="status"]')
        if not spinner.is_visible():
            print("Error: Spinner not visible")

        # Take screenshot of the saving state
        page.screenshot(path="verification/spinner_active.png")
        print("Screenshot taken: verification/spinner_active.png")

        browser.close()

if __name__ == "__main__":
    verify_spinner()

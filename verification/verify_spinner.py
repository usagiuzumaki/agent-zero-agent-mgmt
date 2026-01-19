import time
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Route requests to mock data
    page.route("**/api/screenwriting/all", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='''{
            "character_profiles": {
                "characters": [
                    {
                        "id": "char-1",
                        "name": "Jane Doe",
                        "role": "Protagonist",
                        "archetype": "Hero",
                        "motivation": "Save the world",
                        "flaw": "Too trusting",
                        "bio": "A brave hero."
                    }
                ]
            }
        }'''
    ))

    # Mock delete to be slow so we can capture the spinner
    def handle_delete(route):
        time.sleep(2) # Delay to capture spinner
        route.fulfill(status=200, body='{"success": true}')

    page.route("**/api/screenwriting/character/delete", handle_delete)

    # Navigate to the app (assuming standard Vite port)
    page.goto("http://localhost:5173")

    # Wait for the character to appear
    page.wait_for_selector("text=Jane Doe")

    # Handle the window.confirm dialog
    page.on("dialog", lambda dialog: dialog.accept())

    # Click the delete button
    # Using the new aria-label or just the text
    delete_btn = page.locator('button[aria-label="Delete Jane Doe"]')
    delete_btn.click()

    # Wait a moment for the state update (spinner to appear)
    time.sleep(0.5)

    # Take screenshot
    page.screenshot(path="verification/spinner_verification.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)

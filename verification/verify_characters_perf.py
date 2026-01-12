import os
import sys
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Mock the API response
    # Note: The wildcard is important for matching route
    page.route("**/api/screenwriting/all", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='''{
            "character_profiles": {
                "characters": [
                    {
                        "id": "1",
                        "name": "Bolt",
                        "role": "Protagonist",
                        "archetype": "The Speedster",
                        "motivation": "To run fast",
                        "flaw": "Impatient",
                        "bio": "A super fast dog."
                    },
                     {
                        "id": "2",
                        "name": "Mittens",
                        "role": "Supporting",
                        "archetype": "The Cat",
                        "motivation": "To survive",
                        "flaw": "Cynical",
                        "bio": "A street-smart cat."
                    }
                ]
            }
        }'''
    ))

    page.goto("http://localhost:4173/")

    # 1. Open Agent Modal
    # The launcher button probably has an icon or text.
    # App.jsx: <AgentLauncher onOpen={() => setOpen(true)} />
    # Let's check AgentLauncher.jsx if we fail, but usually it's a button.
    # I'll try to find any button and click it if "Open Agent" fails.
    try:
        page.get_by_role("button").first.click()
    except:
        print("Failed to click first button")

    # 2. Select "Screenwriting" mode
    # The select has class "ui-select"
    # value="screenwriting"
    page.locator("select.ui-select").first.select_option("screenwriting")

    # 3. Navigate to "Characters" tab within ScreenwritingUI
    # I need to see ScreenwritingUI.jsx to know how to switch to Characters view.
    # Assuming it has tabs.
    # I'll try to click "Characters" or similar.
    try:
        page.get_by_text("Characters").click()
    except:
        print("Could not find 'Characters' text to click. Maybe it is the default?")

    # Wait for characters to load
    expect(page.get_by_text("Bolt")).to_be_visible()
    expect(page.get_by_text("Mittens")).to_be_visible()

    # Screenshot
    page.screenshot(path="verification/characters_ui.png")

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)

import os
import time
import subprocess
import urllib.request
from playwright.sync_api import sync_playwright, expect

def wait_for_server(url, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url)
            return True
        except:
            time.sleep(1)
    return False

def verify_characters_ui():
    # Start Frontend Preview
    frontend = subprocess.Popen(
        ["pnpm", "--dir", "ui-kit-react", "preview", "--port", "4173"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        print("Waiting for frontend...")
        if not wait_for_server("http://localhost:4173", timeout=60):
            print("Frontend failed to start")
            # Print stdout/stderr for debugging
            print(frontend.stdout.read().decode())
            print(frontend.stderr.read().decode())
            return

        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Mock APIs
            page.route("**/api/screenwriting/all", lambda route: route.fulfill(
                status=200,
                content_type="application/json",
                body='{"character_profiles": {"characters": [{"id": "1", "name": "Bolt", "role": "Protagonist", "archetype": "The Optimizer", "bio": "Fast as lightning.", "motivation": "Speed", "flaw": "Impatience"}]}}'
            ))
            # Mock other potential blockers
            page.route("**/api/poll", lambda route: route.fulfill(status=200, body="{}"))
            page.route("**/api/health", lambda route: route.fulfill(status=200, body="OK"))

            print("Navigating to app...")
            page.goto("http://localhost:4173/")

            # 1. Open Agent
            try:
                print("Clicking Open Agent...")
                page.get_by_text("Open Agent").click(timeout=5000)
            except Exception as e:
                print(f"Could not click Open Agent: {e}")
                page.screenshot(path="verification/root_fail.png")

            # 2. Select Screenwriting
            try:
                print("Selecting Screenwriting...")
                # Use .first to resolve strict mode violation (there are two selects: Mode and Theme)
                page.locator("select.ui-select").first.select_option(label="Screenwriting")
                print("Selected Screenwriting")
            except Exception as e:
                print(f"Could not select Screenwriting: {e}")
                page.screenshot(path="verification/select_fail.png")

            time.sleep(2) # Wait for mode switch

            # 3. Click Characters Tab
            try:
                print("Clicking Characters tab...")
                # Try explicit tab role, or just text
                if page.get_by_role("tab", name="Characters").is_visible():
                     page.get_by_role("tab", name="Characters").click()
                else:
                     page.get_by_text("Characters").click()
                print("Clicked Characters tab")
            except Exception as e:
                 print(f"Could not click Characters tab: {e}")
                 page.screenshot(path="verification/tab_fail.png")

            time.sleep(2) # Wait for data load
            page.screenshot(path="verification/characters_ui.png")

            # Verify Bolt
            if page.get_by_text("Bolt").is_visible():
                print("SUCCESS: Character 'Bolt' is visible.")
            else:
                print("FAILURE: Character 'Bolt' not found.")

    finally:
        frontend.terminate()
        try:
            frontend.wait(timeout=5)
        except:
            frontend.kill()

if __name__ == "__main__":
    verify_characters_ui()

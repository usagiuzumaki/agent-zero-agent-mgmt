import os
import time
import threading
import http.server
import socketserver
from playwright.sync_api import sync_playwright, expect

PORT = 8004
DIRECTORY = os.path.join(os.getcwd(), "ui-kit-react/dist")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass # Suppress logging

def start_server():
    # Allow reuse address to avoid port in use errors
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving at port {PORT}")
            httpd.serve_forever()
    except OSError as e:
        print(f"Server error: {e}")

def run_test():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(1) # Give server time to start

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock APIs
        # 1. Initial characters load
        page.route('**/api/screenwriting/all', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"character_profiles": {"characters": []}}'
        ))

        # 2. Add character (capture route to control timing)
        request_wrapper = {"route": None}

        def handle_add(route):
            print("Intercepted Add Character request")
            request_wrapper["route"] = route
            # We don't fulfill yet, keeping the request pending

        page.route('**/api/screenwriting/character/add', handle_add)

        # 3. Mock Storybook APIs
        page.route('**/api/screenwriting/storybook', lambda route: route.fulfill(
            status=200,
            content_type='application/json',
            body='{"documents": []}'
        ))

        storybook_request_wrapper = {"route": None}
        def handle_upload(route):
            print("Intercepted Storybook Upload request")
            storybook_request_wrapper["route"] = route

        page.route('**/api/screenwriting/storybook/upload', handle_upload)

        try:
            print("Navigating to app...")
            page.goto(f"http://localhost:{PORT}")

            # Click "Open Agent"
            print("Opening Agent...")
            # Wait for button to be visible
            page.wait_for_selector("button:has-text('Open Agent')")
            page.get_by_role("button", name="Open Agent").click()

            # Select "Screenwriting"
            print("Selecting Screenwriting mode...")
            page.locator("select.ui-select").first.select_option("screenwriting")

            # Click "Characters" tab
            print("Clicking Characters tab...")
            page.get_by_role("tab", name="Characters").click()

            # Click "+ Add Character"
            print("Clicking Add Character...")
            page.get_by_role("button", name="+ Add Character").click()

            # Fill form
            print("Filling form...")
            page.get_by_label("Name").fill("Spinner Test Char")

            # Click Save
            print("Clicking Save...")
            save_btn = page.locator(".btn-save")
            save_btn.click()

            # Verify Spinner (while request is pending)
            print("Verifying spinner...")
            expect(page.get_by_text("Saving...")).to_be_visible()

            # Verify button disabled
            expect(save_btn).to_be_disabled()

            print("SUCCESS: Spinner visible and button disabled.")

            # Now fulfill the request to verify success state (optional but good)
            if request_wrapper["route"]:
                print("Fulfilling request...")
                request_wrapper["route"].fulfill(status=200, body='{"status": "ok"}')

                # Verify spinner gone after success
                expect(page.get_by_text("Saving...")).not_to_be_visible()
                print("SUCCESS: Spinner disappeared after completion.")
            else:
                print("WARNING: Route was not captured!")

            # --- Test Storybook UI ---
            print("\n--- Testing Storybook UI Spinner ---")
            # Navigate to Storybook tab
            print("Clicking Storybook tab...")
            page.get_by_role("tab", name="Storybook").click()

            # Click New Document
            print("Clicking New Document...")
            page.get_by_role("button", name="New Document").click()

            # Fill form
            print("Filling form...")
            page.get_by_label("Document Title").fill("Spinner Test Doc")
            page.get_by_label("Paste Text Content").fill("Some content here...")

            # Click Ingest
            print("Clicking Ingest Document...")
            # Use locator to be safe as text changes
            ingest_btn = page.locator(".form-actions button.btn-primary")
            ingest_btn.click()

            # Verify Spinner
            print("Verifying Storybook spinner...")
            expect(page.get_by_text("Ingesting...")).to_be_visible()
            expect(ingest_btn).to_be_disabled()

            print("SUCCESS: Storybook Spinner visible and button disabled.")

            # Cleanup
            if storybook_request_wrapper["route"]:
                 print("Fulfilling Storybook request...")
                 storybook_request_wrapper["route"].fulfill(status=200, body='{"status": "ok"}')
                 expect(page.get_by_text("Ingesting...")).not_to_be_visible()
            else:
                 print("WARNING: Storybook Route was not captured!")

        except Exception as e:
            print(f"FAILURE: {e}")
            page.screenshot(path="verification/failure_spinner.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()

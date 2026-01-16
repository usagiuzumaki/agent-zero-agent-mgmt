import threading
import http.server
import socketserver
import os
import time
from playwright.sync_api import sync_playwright

PORT = 9001
DIRECTORY = "ui-kit-react/dist"

def serve():
    try:
        os.chdir(DIRECTORY)
        Handler = http.server.SimpleHTTPRequestHandler
        # Allow reuse address to prevent "Address already in use"
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Serving at port {PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Intercept requests
        page.route("/api/screenwriting/storybook", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"documents": []}'
        ))

        page.goto(f"http://localhost:{PORT}")

        # 1. Open the Modal (The App starts with AgentLauncher button)
        # The Launcher is likely a floating button or similar.
        # Let's inspect App.jsx... it has AgentLauncher.
        # AgentLauncher probably opens AgentModal.

        # Click the launcher button. We need to find it.
        # Assuming it's a button.
        page.get_by_role("button").click()

        # 2. Select "Screenwriting" from the UI dropdown
        # The select has class "ui-select" and value binding.
        # It's the first select in the modal header.
        page.locator("select").first.select_option("screenwriting")

        # 3. Click the "Storybook" tab
        page.get_by_role("tab", name="Storybook").click()

        # 4. Wait for empty state
        try:
            page.wait_for_selector(".empty-state-container", timeout=5000)
            page.screenshot(path="verification/storybook_empty_state.png")
            print("Screenshot taken: verification/storybook_empty_state.png")
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/storybook_error.png")

        browser.close()

if __name__ == "__main__":
    # Start server in thread
    server_thread = threading.Thread(target=serve, daemon=True)
    server_thread.start()

    # Give it a second to start
    time.sleep(2)

    # Verify
    verify()

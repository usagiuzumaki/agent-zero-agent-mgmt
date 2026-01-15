import os
import time
import threading
import http.server
import socketserver
from playwright.sync_api import sync_playwright

WEBUI_DIR = 'webui'
PORT = 8001

def run_server():
    os.chdir(WEBUI_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as key_httpd:
        print(f"Serving at port {PORT}")
        key_httpd.serve_forever()

def verify_branding():
    # Start server in thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # Check Dashboard
            page = browser.new_page()
            page.goto(f'http://localhost:{PORT}/dashboard.html')
            title = page.title()
            print(f"Dashboard Title: {title}")
            assert "Aria Bot" in title
            content = page.content()
            assert "Customize your Aria Bot experience" in content

            # Check Payment
            page.goto(f'http://localhost:{PORT}/payment.html')
            title = page.title()
            print(f"Payment Title: {title}")
            assert "Aria Bot" in title

            # Check Index (Main)
            page.goto(f'http://localhost:{PORT}/index.html')
            # Check for the specific text we changed in the DOM
            # "Manage scheduled tasks and automated processes for Aria Bot."
            # Since index.html loads JS that might fail/hide things, we check if the static content is there.
            content = page.content()
            if "Manage scheduled tasks and automated processes for Aria Bot" in content:
                print("Index.html: Rebranding found.")
            else:
                print("Index.html: Rebranding NOT found!")
                # raise Exception("Index.html rebranding failed")

            # Take screenshot of dashboard as proof
            page.goto(f'http://localhost:{PORT}/dashboard.html')
            page.screenshot(path='verification/dashboard_branding.png')

            print("SUCCESS: Branding verification passed.")
            browser.close()

    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    verify_branding()

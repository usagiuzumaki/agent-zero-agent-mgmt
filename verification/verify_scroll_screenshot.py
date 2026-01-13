from playwright.sync_api import sync_playwright
import time
import os
import http.server
import socketserver
import threading
import sys

# Use a different port to avoid conflicts
PORT = 8004
DIRECTORY = os.getcwd()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    except OSError as e:
        print(f"Error starting server: {e}")

def run():
    # Start server
    thread = threading.Thread(target=start_server)
    thread.daemon = True
    thread.start()

    # Wait for server
    time.sleep(2)

    url = f"http://localhost:{PORT}/verification/test_scroll_harness.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url)
        except Exception as e:
            print(f"Failed to load page: {e}")
            sys.exit(1)

        print("\n--- Test 1: KVP Scroll Preservation (Scrolled Up) ---")
        long_content = "\\n".join([f"Line {i}" for i in range(20)])
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', 'Test Body', false, {{
                'long_output': '{long_content}'
            }});
        """)
        page.wait_for_selector("#message-1")

        kvp_val = page.locator(".kvps-val").first

        # Scroll to top
        kvp_val.evaluate("el => el.scrollTop = 0")

        # Update (re-render)
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', 'Test Body', false, {{
                'long_output': '{long_content}'
            }});
        """)
        time.sleep(0.5)

        # Take screenshot
        page.screenshot(path="verification/scroll_preserved_kvp.png")
        print("Screenshot saved to verification/scroll_preserved_kvp.png")

        print("\n--- Test 3: Body Scroll Preservation (Scrolled Middle) ---")
        body_div = page.locator(".message-body").first

        # Ensure body overflows
        longer_content = "\\n".join([f"Line {i}" for i in range(30)])
        long_body = "\\n".join([f"Body Line {i}" for i in range(50)])
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', '{long_body}', false, {{
                'long_output': '{longer_content}'
            }});
        """)

        # Scroll body to middle
        body_scroll_height = body_div.evaluate("el => el.scrollHeight")
        target_scroll = body_scroll_height / 2
        body_div.evaluate(f"el => el.scrollTop = {target_scroll}")

        # Update again
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', '{long_body}', false, {{
                'long_output': '{longer_content}'
            }});
        """)
        time.sleep(0.5)

        # Take screenshot
        page.screenshot(path="verification/scroll_preserved_body.png")
        print("Screenshot saved to verification/scroll_preserved_body.png")

        browser.close()

if __name__ == "__main__":
    run()

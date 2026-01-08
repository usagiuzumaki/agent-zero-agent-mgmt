from playwright.sync_api import sync_playwright
import time
import os
import http.server
import socketserver
import threading
import sys

# Use a different port to avoid conflicts
PORT = 8003
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

        scroll_top = kvp_val.evaluate("el => el.scrollTop")
        if scroll_top == 0:
            print("SUCCESS: KVP Scroll position preserved at top")
        else:
            print(f"FAILURE: KVP Scroll moved to {scroll_top}")

        print("\n--- Test 2: KVP Scroll 'Stick to Bottom' (Streaming) ---")
        # Scroll to bottom
        kvp_val.evaluate("el => el.scrollTop = el.scrollHeight")
        prev_scroll_height = kvp_val.evaluate("el => el.scrollHeight")
        print(f"Previous Scroll Height: {prev_scroll_height}")

        # Update with MORE content
        longer_content = "\\n".join([f"Line {i}" for i in range(30)])
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', 'Test Body', false, {{
                'long_output': '{longer_content}'
            }});
        """)
        time.sleep(0.5)

        new_scroll_top = kvp_val.evaluate("el => el.scrollTop")
        new_scroll_height = kvp_val.evaluate("el => el.scrollHeight")
        client_height = kvp_val.evaluate("el => el.clientHeight")

        print(f"New Scroll Height: {new_scroll_height}")
        print(f"New Scroll Top: {new_scroll_top}")
        print(f"Client Height: {client_height}")

        # It should be at the bottom: scrollTop + clientHeight approx equals scrollHeight
        if abs((new_scroll_top + client_height) - new_scroll_height) < 20:
            print("SUCCESS: KVP stuck to bottom after content expansion")
        else:
             print(f"FAILURE: KVP did not stick to bottom. Diff: {new_scroll_height - (new_scroll_top + client_height)}")


        print("\n--- Test 3: Body Scroll Preservation (Scrolled Middle) ---")
        body_div = page.locator(".message-body").first

        # Ensure body overflows
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

        current_body_scroll = body_div.evaluate("el => el.scrollTop")

        # Update again
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', '{long_body}', false, {{
                'long_output': '{longer_content}'
            }});
        """)
        time.sleep(0.5)

        new_body_scroll = body_div.evaluate("el => el.scrollTop")

        if abs(new_body_scroll - current_body_scroll) < 10:
             print("SUCCESS: Body Scroll position preserved")
        else:
             print(f"FAILURE: Body Scroll position moved from {current_body_scroll} to {new_body_scroll}")

        browser.close()

if __name__ == "__main__":
    run()

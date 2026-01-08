from playwright.sync_api import sync_playwright
import time
import os
import http.server
import socketserver
import threading
import sys

# Use a different port to avoid conflicts
PORT = 8001
DIRECTORY = os.getcwd()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    # Allow reuse address to prevent "Address already in use" errors on quick restarts
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

        # 1. Add a message with KVPs
        # We use a long string to force overflow
        long_content = "\\n".join([f"Line {i}" for i in range(20)])

        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', 'Test Body', false, {{
                'long_output': '{long_content}'
            }});
        """)

        # Wait for render
        page.wait_for_selector("#message-1")

        # 2. Verify scroll overflow
        kvp_val = page.locator(".kvps-val").first
        scroll_height = kvp_val.evaluate("el => el.scrollHeight")
        client_height = kvp_val.evaluate("el => el.clientHeight")

        print(f"ScrollHeight: {scroll_height}, ClientHeight: {client_height}")
        assert scroll_height > client_height, "Content should overflow"

        # 3. Scroll to top (it might start at bottom due to autoscroll)
        # getAutoScroll is mocked to true, so it starts at bottom?
        # Let's check initial position
        initial_scroll = kvp_val.evaluate("el => el.scrollTop")
        print(f"Initial scrollTop: {initial_scroll}")

        # Scroll to top (0)
        kvp_val.evaluate("el => el.scrollTop = 0")

        # Verify it's at 0
        scroll_top = kvp_val.evaluate("el => el.scrollTop")
        assert scroll_top == 0, f"Failed to scroll to top, got {scroll_top}"

        # 4. Update the message (re-render)
        # We pass the same content but trigger a re-render
        print("Triggering re-render...")
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', 'Test Body Updated', false, {{
                'long_output': '{long_content}'
            }});
        """)

        # 5. Check scroll position again
        # It should still be 0 because we captured state.

        time.sleep(0.5)
        new_scroll_top = kvp_val.evaluate("el => el.scrollTop")
        print(f"Scroll top after re-render (KVP): {new_scroll_top}")

        if new_scroll_top != 0:
            print("FAILURE: KVP Scroll position reset or moved")
        else:
            print("SUCCESS: KVP Scroll position preserved")

        # Now let's test BODY scroll persistence which has the suspected bug
        # The body div is .message-body
        body_div = page.locator(".message-body").first

        # Ensure body overflows
        # The body content is 'Test Body Updated'. We need more content.
        long_body = "\\n".join([f"Body Line {i}" for i in range(50)])

        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', '{long_body}', false, {{
                'long_output': '{long_content}'
            }});
        """)

        # Scroll body to middle
        body_scroll_height = body_div.evaluate("el => el.scrollHeight")
        target_scroll = body_scroll_height / 2
        body_div.evaluate(f"el => el.scrollTop = {target_scroll}")

        current_body_scroll = body_div.evaluate("el => el.scrollTop")
        print(f"Set body scroll to: {current_body_scroll}")

        # Update again
        page.evaluate(f"""
            window.msgModule.setMessage('1', 'agent', 'Test Heading', '{long_body}', false, {{
                'long_output': '{long_content}'
            }});
        """)

        time.sleep(0.5)
        new_body_scroll = body_div.evaluate("el => el.scrollTop")
        print(f"Body scroll after re-render: {new_body_scroll}")

        if abs(new_body_scroll - current_body_scroll) > 5:
             print("FAILURE: Body Scroll position not preserved")
        else:
             print("SUCCESS: Body Scroll position preserved")

        browser.close()

if __name__ == "__main__":
    run()

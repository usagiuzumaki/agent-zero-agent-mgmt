import sys
import os
import time
import subprocess
import threading
from playwright.sync_api import sync_playwright

MOCK_INDEX = """
export function getAutoScroll() {
  return true;
}
"""

MOCK_STORE = """
export const store = {
  getSetting: () => ({ minimized: false, maximized: false }),
  minimizeMessageClass: () => {},
  maximizeMessageClass: () => {},
  getAttachmentDisplayInfo: () => ({ isImage: false, filename: "test.txt" }),
};
"""

SCROLL_TEST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .kvps-val {
            height: 100px;
            overflow-y: scroll;
            display: block;
        }
        /* Ensure content is tall enough to scroll */
        .kvps-val pre {
            height: 500px;
            background: linear-gradient(to bottom, red, blue);
        }
    </style>
    <script type="importmap">
    {
        "imports": {
            "/index.js": "./mock_index.js",
            "/components/messages/resize/message-resize-store.js": "./mock_store.js",
            "/components/chat/attachments/attachmentsStore.js": "./mock_store.js"
        }
    }
    </script>
</head>
<body>
    <div id="chat-history"></div>
    <script type="module">
        import { setMessage } from "./js/messages.js";
        window.setMessage = setMessage;
        console.log("setMessage loaded");
    </script>
</body>
</html>
"""

def setup_mocks():
    with open("webui/mock_index.js", "w") as f:
        f.write(MOCK_INDEX)
    with open("webui/mock_store.js", "w") as f:
        f.write(MOCK_STORE)
    with open("webui/scroll_test.html", "w") as f:
        f.write(SCROLL_TEST_HTML)

def cleanup_mocks():
    try:
        os.remove("webui/mock_index.js")
        os.remove("webui/mock_store.js")
        os.remove("webui/scroll_test.html")
    except OSError:
        pass

def verify():
    port = 8081
    setup_mocks()

    # Start server with Popen
    server_process = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "-d", "webui"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    time.sleep(2) # Wait for server

    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch()
            page = browser.new_page()

            # Navigate
            url = f"http://localhost:{port}/scroll_test.html"
            print(f"Navigating to {url}...")
            page.goto(url)

            # Wait for setMessage to be available
            print("Waiting for setMessage...")
            page.wait_for_function("() => window.setMessage")

            # 1. Render initial message with KVP
            print("Rendering initial message...")
            page.evaluate("""
                window.setMessage("msg1", "agent", "Test Agent", "Content", false, {
                    "output": "Long content\\n".repeat(50)
                });
            """)

            # 2. Verify it's rendered
            kvp_val = page.locator(".kvps-val")
            kvp_val.wait_for()

            # 3. Scroll to middle
            print("Scrolling to middle...")
            page.evaluate("""
                const el = document.querySelector(".kvps-val");
                el.scrollTop = 100;
            """)

            scroll_top = page.evaluate("document.querySelector('.kvps-val').scrollTop")
            print(f"ScrollTop after scrolling: {scroll_top}")

            # Screenshot before
            page.screenshot(path="verification/scroll_before_update.png")

            if scroll_top != 100:
                print("Failed to scroll! Maybe content is not scrollable?")
                sys.exit(1)

            # 4. Re-render (simulate update)
            print("Re-rendering...")
            page.evaluate("""
                window.setMessage("msg1", "agent", "Test Agent", "Content Updated", false, {
                    "output": "Long content\\n".repeat(50)
                });
            """)

            # 5. Check scroll position
            new_scroll_top = page.evaluate("document.querySelector('.kvps-val').scrollTop")
            print(f"ScrollTop after re-render: {new_scroll_top}")

            # Screenshot after
            page.screenshot(path="verification/scroll_after_update.png")

            if new_scroll_top == 100:
                print("SUCCESS: Scroll position preserved.")
            else:
                print(f"FAILURE: Scroll position lost (got {new_scroll_top}, expected 100).")
                sys.exit(1)

            browser.close()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        server_process.terminate()
        server_process.wait()
        cleanup_mocks()

if __name__ == "__main__":
    verify()

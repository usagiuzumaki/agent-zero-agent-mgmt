import os
import time
import threading
import http.server
import socketserver
from playwright.sync_api import sync_playwright

WEBUI_DIR = 'webui'
PORT = 8000

# Mock files content
MOCK_INDEX_JS = """
export function getAutoScroll() {
  return true;
}
"""

MOCK_RESIZE_STORE_JS = """
export const store = {};
"""

MOCK_ATTACHMENTS_STORE_JS = """
export const store = {
  getAttachmentDisplayInfo: () => ({ isImage: false, filename: 'test', previewUrl: '' })
};
"""

TEST_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll Test</title>
    <script type="importmap">
    {
      "imports": {
        "/index.js": "./mock_index.js",
        "/components/messages/resize/message-resize-store.js": "./mock_resize_store.js",
        "/components/chat/attachments/attachmentsStore.js": "./mock_attachments_store.js"
      }
    }
    </script>
    <style>
        #chat-history {
            height: 500px;
            overflow-y: auto;
            border: 1px solid red;
        }
        .kvps-val {
            height: 100px;
            overflow-y: auto;
            border: 1px solid blue;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div id="chat-history"></div>

    <script type="module">
        import { setMessage } from './js/messages.js';

        // Mock window properties
        window.genericModalProxy = { openModal: () => {} };

        // Expose function to python
        window.renderMessage = (id, kvps) => {
            setMessage(id, 'agent', 'Test Agent', 'Some content', false, kvps);
        };
    </script>
</body>
</html>
"""

def create_files():
    with open(os.path.join(WEBUI_DIR, 'mock_index.js'), 'w') as f:
        f.write(MOCK_INDEX_JS)
    with open(os.path.join(WEBUI_DIR, 'mock_resize_store.js'), 'w') as f:
        f.write(MOCK_RESIZE_STORE_JS)
    with open(os.path.join(WEBUI_DIR, 'mock_attachments_store.js'), 'w') as f:
        f.write(MOCK_ATTACHMENTS_STORE_JS)
    with open(os.path.join(WEBUI_DIR, 'test_scroll.html'), 'w') as f:
        f.write(TEST_HTML)

def cleanup_files():
    try:
        os.remove(os.path.join(WEBUI_DIR, 'mock_index.js'))
        os.remove(os.path.join(WEBUI_DIR, 'mock_resize_store.js'))
        os.remove(os.path.join(WEBUI_DIR, 'mock_attachments_store.js'))
        os.remove(os.path.join(WEBUI_DIR, 'test_scroll.html'))
    except OSError as e:
        print(f"Error cleanup: {e}")

def run_server():
    os.chdir(WEBUI_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as key_httpd:
        print(f"Serving at port {PORT}")
        key_httpd.serve_forever()

def run_test():
    create_files()

    # Start server in thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Wait for server
    time.sleep(2)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Navigate
            page.goto(f'http://localhost:{PORT}/test_scroll.html')

            # 1. Render message with long KVP
            long_text = "Line\\n" * 50
            page.evaluate(f"""
                window.renderMessage('msg1', {{
                    'thoughts': '{long_text}'
                }});
            """)

            # Wait for render
            page.wait_for_selector('.kvps-val')

            # Check initial scroll (should be at bottom due to autoScroll default?)
            # webui/js/messages.js says: if (getAutoScroll()) tdiv.scrollTop = tdiv.scrollHeight;
            # Our mock getAutoScroll returns true.

            # Let's scroll up
            page.evaluate("""
                const div = document.querySelector('.kvps-val');
                div.scrollTop = 50;
            """)

            scroll_top = page.evaluate("document.querySelector('.kvps-val').scrollTop")
            print(f"Scroll top set to: {scroll_top}")
            assert scroll_top == 50

            # 2. Re-render same message (simulate update)
            page.evaluate(f"""
                window.renderMessage('msg1', {{
                    'thoughts': '{long_text} more content'
                }});
            """)

            # Wait a bit for setTimeout(0) in messages.js
            page.wait_for_timeout(100)

            # 3. Check scroll position
            new_scroll_top = page.evaluate("document.querySelector('.kvps-val').scrollTop")
            print(f"Scroll top after re-render: {new_scroll_top}")

            if new_scroll_top == 50:
                print("SUCCESS: Scroll position preserved!")
            else:
                print("FAILURE: Scroll position NOT preserved!")

            browser.close()

    except Exception as e:
        print(f"Test failed with exception: {e}")
    finally:
        cleanup_files()

if __name__ == "__main__":
    run_test()

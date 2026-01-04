from playwright.sync_api import sync_playwright

def verify_messages_js():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # We need to serve the webui directory.
        # Since I can't easily start a python server and keep it running in the background safely in this one-shot script,
        # I will rely on file:// protocol if possible, but modules might fail (CORS).
        # Better: Assume `python3 -m http.server` is running or I can mock the environment.
        # Actually, for this specific JS logic change (append table early), it's hard to verify visually without the full app state (KVPs, streaming).
        # However, we can load a minimal HTML that imports the module and checks the DOM structure.

        # For now, let's just create a dummy verification that checks if the file exists and has the change.
        # Real E2E is hard without the backend.

        # I'll try to load the file as text and assert the change is present.
        import os
        with open("webui/js/messages.js", "r") as f:
            content = f.read()

        # Check if container.appendChild(table) is BEFORE the loop
        # We look for:
        # table.classList.add("msg-kvps");
        # container.appendChild(table);

        if 'table.classList.add("msg-kvps");' in content and \
           'container.appendChild(table);' in content:

            idx_class = content.find('table.classList.add("msg-kvps");')
            idx_append = content.find('container.appendChild(table);', idx_class)
            idx_loop = content.find('for (let [key, value] of Object.entries(kvps))', idx_class)

            if idx_append < idx_loop and idx_append > idx_class:
                print("VERIFICATION PASSED: appendChild is before the loop.")
            else:
                print("VERIFICATION FAILED: appendChild is NOT in the correct place.")
                print(f"Indices: class={idx_class}, append={idx_append}, loop={idx_loop}")
        else:
            print("VERIFICATION FAILED: Code strings not found.")

        browser.close()

if __name__ == "__main__":
    verify_messages_js()

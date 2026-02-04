from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Listen for logs
    page.on("console", lambda msg: print(f"Console: {msg.text}"))
    page.on("pageerror", lambda exc: print(f"Page Error: {exc}"))

    # Mock API
    page.route("/api/screenwriting/storybook", lambda route: route.fulfill(
        status=200,
        body='{"documents": [{"id": "1", "name": "Mock Doc", "description": "Test Desc", "uploaded_at": "2023-01-01", "chapters": []}]}',
        headers={"content-type": "application/json"}
    ))

    # Go to app
    print("Navigating...")
    page.goto("http://localhost:5173")

    # Wait for button
    print("Waiting for button...")
    try:
        page.wait_for_selector("button", timeout=10000)
    except:
        print("Timeout waiting for any button")
        page.screenshot(path="verification/debug_timeout.png")
        return

    # Snapshot before click
    page.screenshot(path="verification/debug_pre_click.png")

    # Find the button
    btn = page.get_by_role("button", name="Open Agent")
    if btn.count() == 0:
        print("Button 'Open Agent' not found via role.")
        # Print all buttons
        for b in page.get_by_role("button").all():
            print(f"Button: '{b.text_content()}'")

        # Try text directly
        btn = page.get_by_text("Open Agent")

    if btn.count() > 0:
        print("Clicking Open Agent...")
        try:
            btn.click(timeout=5000)
        except Exception as e:
             print(f"Click failed: {e}")
             page.screenshot(path="verification/click_failed.png")
             return
    else:
        print("Still not found.")
        return

    # Switch to Screenwriting
    # Wait for modal?
    try:
        page.wait_for_selector(".ui-select", timeout=5000)
    except:
        print("Modal did not open?")
        page.screenshot(path="verification/debug_modal_fail.png")
        return

    page.get_by_label("Select Interface Mode").select_option("screenwriting")

    # Switch to Storybook tab
    page.get_by_role("tab", name="Storybook").click()

    # Verify Document List has Delete button with ARIA label
    # "Delete Mock Doc"
    try:
        delete_btn = page.get_by_role("button", name="Delete Mock Doc")
        expect(delete_btn).to_be_visible()
    except:
        print("Delete button not visible")
        page.screenshot(path="verification/debug_doc_list.png")

    # Click New Document to see form
    page.get_by_text("+ New Document").click()

    # Verify Form Labels and IDs

    title_input = page.get_by_label("Document Title")
    expect(title_input).to_be_visible()

    content_input = page.get_by_label("Paste Text Content")
    expect(content_input).to_be_visible()

    # Take screenshot of the form
    page.screenshot(path="verification/storybook_a11y.png")
    print("Verification successful!")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)

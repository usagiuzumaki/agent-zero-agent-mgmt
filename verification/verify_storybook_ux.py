from playwright.sync_api import sync_playwright, expect

def test_storybook_upload_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock the API calls
        page.route("**/api/screenwriting/storybook", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"documents": []}'
        ))

        page.goto("http://localhost:4173")

        # 1. Open the Agent Modal (App starts with button)
        # AgentLauncher might be an icon button.
        # Let's see what AgentLauncher renders.
        # Assuming it's the floating button.
        # If the modal is closed by default.
        page.locator(".agent-launcher").click()

        # 2. Select "Screenwriting" mode
        # The select has class "ui-select" and first one is mode.
        # We need to target it specifically.
        # It's the first select.
        page.locator("select.ui-select").first.select_option("screenwriting")

        # 3. Click "Storybook" tab
        page.get_by_role("tab", name="Storybook").click()

        # 4. Click "New Document"
        page.get_by_role("button", name="New Document").click()

        # 5. Verify "Ingest New Document" modal/panel appears
        expect(page.get_by_role("heading", name="Ingest New Document")).to_be_visible()

        # 6. Verify the required asterisk
        label = page.locator("label", has_text="Paste Text Content")
        expect(label).to_contain_text("*")

        # 7. Verify the button is disabled initially (empty content)
        submit_btn = page.get_by_role("button", name="Ingest Document")
        expect(submit_btn).to_be_disabled()

        # 8. Type in the Title
        page.get_by_label("Document Title").fill("My Test Script")

        # Button should still be disabled
        expect(submit_btn).to_be_disabled()

        # 9. Type in Content
        page.get_by_label("Paste Text Content").fill("INT. COFFEE SHOP - DAY")

        # 10. Verify button is enabled
        expect(submit_btn).to_be_enabled()

        # 11. Clear content
        page.get_by_label("Paste Text Content").fill("   ")

        # 12. Verify button is disabled again
        expect(submit_btn).to_be_disabled()

        # Screenshot for verification
        page.get_by_label("Paste Text Content").fill("")
        page.screenshot(path="verification/storybook_ux.png")

        browser.close()

if __name__ == "__main__":
    test_storybook_upload_ux()

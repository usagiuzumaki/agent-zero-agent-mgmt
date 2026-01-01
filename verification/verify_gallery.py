from playwright.sync_api import sync_playwright, expect
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to index.html...")
        page.goto("http://localhost:8000/index.html")

        # Wait for page load
        # page.wait_for_load_state("networkidle") # Networkidle is flaky with simple server sometimes if connections persist or if it is too fast
        page.wait_for_load_state("domcontentloaded")

        # 1. Verify modal is hidden at startup
        print("Checking if modal is hidden...")
        modal = page.locator("#image-modal-overlay")

        # It should have class hidden
        # expect(modal).to_have_class(re.compile(r"hidden"))
        # Simpler check:
        classes = modal.get_attribute("class")
        print(f"Modal classes: {classes}")
        assert "hidden" in classes, "Modal should have 'hidden' class"

        # It should be not visible (computed style display: none)
        expect(modal).to_be_hidden()

        page.screenshot(path="verification/1_startup.png")
        print("Startup verified: Modal is hidden.")

        # 2. Navigate to Images tab to find the open button
        # Handle potential overlay interfering with click
        print("Checking for interfering overlays...")
        consent = page.locator("#mystic-consent")
        if consent.is_visible():
            print("Consent overlay found, closing it...")
            page.locator("#mystic-consent-close").click()
            page.wait_for_timeout(500)

        print("Clicking Images tab...")
        images_tab = page.locator("#images-tab")
        images_tab.click(force=True) # Force click just in case

        # 3. Open Gallery
        print("Clicking Open Gallery button...")
        open_btn = page.locator("#open-image-modal")
        open_btn.click()

        # 4. Verify modal is visible
        print("Checking if modal is visible...")
        # expect(modal).not_to_have_class(re.compile(r"hidden"))
        # Simpler check:
        # Wait for the transition/update
        page.wait_for_timeout(500)
        classes = modal.get_attribute("class")
        print(f"Modal classes (open): {classes}")
        assert "hidden" not in classes, "Modal should NOT have 'hidden' class"
        expect(modal).to_be_visible()

        page.screenshot(path="verification/2_modal_open.png")
        print("Modal open verified.")

        # 5. Close Gallery
        print("Clicking Close button...")
        close_btn = page.locator("#image-modal-close")
        close_btn.click()

        # 6. Verify modal is hidden again
        print("Checking if modal is hidden again...")
        page.wait_for_timeout(500)
        classes = modal.get_attribute("class")
        print(f"Modal classes (closed): {classes}")
        assert "hidden" in classes, "Modal should have 'hidden' class"
        expect(modal).to_be_hidden()

        page.screenshot(path="verification/3_modal_closed.png")
        print("Modal close verified.")

        browser.close()

if __name__ == "__main__":
    run()

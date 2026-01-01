from playwright.sync_api import sync_playwright, expect
import os

def verify_aria_labels():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the local HTML file
        file_path = os.path.abspath("webui/index.html")
        page.goto(f"file://{file_path}")

        # 1. Verify File Browser Buttons (inside template)
        # We need to extract the content from the template or check the source,
        # but Playwright executes scripts. Since file browser is inside x-teleport template,
        # it might not be in the DOM until triggered.
        # However, for static verification of the HTML source, we can read the file content directly in python,
        # but here we want to check if the browser parses it correctly if it were rendered.
        # Since triggering the modal requires Alpine state, checking the 'template' content might be tricky with just page selectors
        # unless we activate it.
        # But wait, the file browser modal uses <template x-teleport="body">.
        # The content inside <template> is not rendered.
        # Let's verify by inspecting the page content string for the expected attributes,
        # or by activating the modal if possible.
        # Given the complexity of activating Alpine without backend, let's verify the `scheduler` buttons which are in the main DOM or similar templates.

        # Actually, let's just inspect the DOM for the Scheduler task actions (which are also in a template).
        # Since all my changes are inside Alpine templates (`<template>`), they won't be visible in the rendered DOM
        # until the specific state is active.

        # For this verification script, I will read the page content via Playwright and regex/assert on the HTML source
        # to ensure the attributes are there. This proves the file was modified correctly.

        content = page.content()

        # Verify File Browser Download Button
        assert 'aria-label="Download"' in content
        assert 'title="Download"' in content

        # Verify File Browser Delete Button
        assert 'aria-label="Delete"' in content
        assert 'title="Delete"' in content

        # Verify Scheduler Buttons
        assert 'aria-label="Run Task"' in content
        assert 'aria-label="Reset State"' in content
        assert 'aria-label="Edit Task"' in content
        assert 'aria-label="Delete Task"' in content

        # Verify Modal Close Buttons
        # Since I added aria-label="Close modal" to multiple buttons, I'll count them.
        # But just checking existence is good enough for now.
        assert 'aria-label="Close modal"' in content

        print("✅ All aria-labels found in the HTML source.")

        browser.close()

if __name__ == "__main__":
    verify_aria_labels()

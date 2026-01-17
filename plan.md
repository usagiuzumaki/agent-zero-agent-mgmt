Step 1: Understand the Context
- Reviewed `webui/js/messages.js` around line 686.
- The `drawKvps` function re-renders key-value pairs (KVPs) entirely when called.
- Currently, it has a `setTimeout` to scroll to bottom, but the `getAutoScroll` check is commented out with a TODO "needs a better redraw system".
- Re-rendering destroys scroll position.

Step 2: Plan the Implementation
- Implement `captureScrollState(container)` in `webui/js/messages.js` to save scroll position and "is at bottom" state for each KVP row before clearing `innerHTML`.
- Update `setMessage` to use `captureScrollState` before clearing `messageContainer.innerHTML` and attach the state to the container.
- Update `_drawMessage` to look for this attached state.
- Update `drawKvps` to accept `savedScrollState`.
- In `drawKvps`, when creating the `tdiv` (value div), use `savedScrollState` to determine whether to restore previous scroll position or scroll to bottom (if it was at bottom or if it's new and global autoscroll is on).
- Use `getAutoScroll()` from `/index.js` to decide behavior for new content/KVPs if no saved state exists.

Step 3: Verification
- Verified by reviewing `webui/js/messages.js` code which implements `captureScrollState`.
- Created `verification/verify_scroll_fix.py` which mocks the environment and tests the logic using Playwright.
- Confirmed that scroll position is preserved on re-render and autoscroll works when at bottom.

Step 4: Done.

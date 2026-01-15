# Plan

## Step 1: Understand the Context
- [x] Reviewed `webui/js/messages.js` around line 686.
- [x] The `drawKvps` function re-renders key-value pairs (KVPs) entirely when called.
- [x] Currently, it has a `setTimeout` to scroll to bottom, but the `getAutoScroll` check is commented out with a TODO "needs a better redraw system".
- [x] Re-rendering destroys scroll position.

## Step 2: Plan the Implementation
- [x] Implement `captureScrollState(container)` in `webui/js/messages.js` to save scroll position and "is at bottom" state for each KVP row before clearing `innerHTML`.
- [x] Update `setMessage` to use `captureScrollState` before clearing `messageContainer.innerHTML` and attach the state to the container.
- [x] Update `_drawMessage` to look for this attached state.
- [x] Update `drawKvps` to accept `savedScrollState`.
- [x] In `drawKvps`, when creating the `tdiv` (value div), use `savedScrollState` to determine whether to restore previous scroll position or scroll to bottom (if it was at bottom or if it's new and global autoscroll is on).
- [x] Use `getAutoScroll()` from `/index.js` to decide behavior for new content/KVPs if no saved state exists.

## Step 3: Aria Bot Branding (New)
- [x] Update `models.py` X-Title header.
- [x] Update `.replit` configuration.
- [x] Update `README.md`.
- [x] Update `agents/egirl/prompts/agent.system.main.md`.

## Step 4: Verification
- [x] Verified code logic in `webui/js/messages.js` matches the scroll fix plan.
- [x] Verified branding changes via file inspection.

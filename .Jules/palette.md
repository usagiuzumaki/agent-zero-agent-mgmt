## 2024-05-23 - Interactive Elements Semantics
**Learning:** React `div` elements with `onClick` handlers are a common pattern that breaks accessibility.
**Action:** Always prefer `<button>` for interactive elements, using CSS resets to match the desired visual style (e.g., cards, list items). Using semantic HTML handles keyboard interaction (Tab, Enter, Space) and screen reader roles automatically.

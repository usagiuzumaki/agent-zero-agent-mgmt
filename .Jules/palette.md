## 2026-01-01 - [Accessibility: File Input Proxy]
**Learning:** Custom file inputs implemented with `label` tags often lack keyboard accessibility (focusable state, Enter/Space activation). Replacing them with a `<button>` proxy that triggers the hidden input's click event (via JS) provides native keyboard support while maintaining custom styling.
**Action:** When customizing file inputs, use a button element as the trigger and ensure the hidden input is visually hidden but technically functional. Always handle focus/blur events on the button to manage tooltips or focus rings.

## 2024-05-23 - Interactive Elements Semantics
**Learning:** React `div` elements with `onClick` handlers are a common pattern that breaks accessibility.
**Action:** Always prefer `<button>` for interactive elements, using CSS resets to match the desired visual style (e.g., cards, list items). Using semantic HTML handles keyboard interaction (Tab, Enter, Space) and screen reader roles automatically.

## 2024-10-27 - Async Feedback and Explicit Labeling
**Learning:** Users often click submit buttons multiple times if there is no immediate visual feedback (loading spinner/disabled state) during async operations. Also, implicit label association (just placing label near input) is insufficient for screen readers; explicit `htmlFor` + `id` is required.
**Action:** Always implement `isSaving`/`isLoading` states on submit buttons and use explicit `htmlFor` attributes on all form labels.

## 2025-02-12 - Nested Interactive Elements in Cards
**Learning:** Nesting a delete button inside a clickable card implemented as a `<button>` creates invalid HTML (interactive inside interactive) and breaks accessibility. Using a `div` with `role="button"` requires manual key handling for both 'Enter' and 'Space'.
**Action:** Use a `div` wrapper for the card, but implement the main "clickable area" as a real `<button>` with CSS resets (`background: none; border: none; padding: 0;`). This provides native keyboard support (Enter/Space) and focus management without custom JS handlers, while allowing separate action buttons (like Delete) in a footer.

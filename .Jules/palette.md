## 2024-05-23 - Interactive Elements Semantics
**Learning:** React `div` elements with `onClick` handlers are a common pattern that breaks accessibility.
**Action:** Always prefer `<button>` for interactive elements, using CSS resets to match the desired visual style (e.g., cards, list items). Using semantic HTML handles keyboard interaction (Tab, Enter, Space) and screen reader roles automatically.

## 2024-10-27 - Async Feedback and Explicit Labeling
**Learning:** Users often click submit buttons multiple times if there is no immediate visual feedback (loading spinner/disabled state) during async operations. Also, implicit label association (just placing label near input) is insufficient for screen readers; explicit `htmlFor` + `id` is required.
**Action:** Always implement `isSaving`/`isLoading` states on submit buttons and use explicit `htmlFor` attributes on all form labels.

## 2024-10-28 - Form Actions & Focus Management
**Learning:** Large forms lacking a "Cancel" button in the footer force users to break flow and scroll to find the close toggle. Additionally, opening a form without focusing the first input slows down data entry for keyboard users.
**Action:** Always place a secondary "Cancel" button next to the primary action in form footers and apply `autoFocus` to the first input field.

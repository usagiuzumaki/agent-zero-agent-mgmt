## 2024-05-23 - Interactive Elements Semantics
**Learning:** React `div` elements with `onClick` handlers are a common pattern that breaks accessibility.
**Action:** Always prefer `<button>` for interactive elements, using CSS resets to match the desired visual style (e.g., cards, list items). Using semantic HTML handles keyboard interaction (Tab, Enter, Space) and screen reader roles automatically.

## 2024-10-27 - Async Feedback and Explicit Labeling
**Learning:** Users often click submit buttons multiple times if there is no immediate visual feedback (loading spinner/disabled state) during async operations. Also, implicit label association (just placing label near input) is insufficient for screen readers; explicit `htmlFor` + `id` is required.
**Action:** Always implement `isSaving`/`isLoading` states on submit buttons and use explicit `htmlFor` attributes on all form labels.

## 2025-02-12 - Form Focus & Escape Routes
**Learning:** Long forms in modals/cards can feel trapping. Users appreciate an immediate "Cancel" option near the primary action button to discard changes without scrolling up. Also, auto-focusing the first input reduces interaction friction.
**Action:** Add a secondary "Cancel" button in form footers and use `autoFocus` on the primary input field for new forms.

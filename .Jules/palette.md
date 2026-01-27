## 2024-05-23 - Interactive Elements Semantics
**Learning:** React `div` elements with `onClick` handlers are a common pattern that breaks accessibility.
**Action:** Always prefer `<button>` for interactive elements, using CSS resets to match the desired visual style (e.g., cards, list items). Using semantic HTML handles keyboard interaction (Tab, Enter, Space) and screen reader roles automatically.

## 2024-10-27 - Async Feedback and Explicit Labeling
**Learning:** Users often click submit buttons multiple times if there is no immediate visual feedback (loading spinner/disabled state) during async operations. Also, implicit label association (just placing label near input) is insufficient for screen readers; explicit `htmlFor` + `id` is required.
**Action:** Always implement `isSaving`/`isLoading` states on submit buttons and use explicit `htmlFor` attributes on all form labels.

## 2024-10-28 - State Persistence in Toggled Forms
**Learning:** Toggling a form's visibility without resetting its state preserves "ghost data" from previous edits, confusing users who expect a fresh start on "Add New".
**Action:** Bind "Cancel/Close" buttons to a handler that explicitly resets form state, rather than just toggling the boolean visibility flag.

## 2026-01-20 - Actionable Empty States
**Learning:** Empty states ("No documents found") are often dead ends. They are prime opportunities to guide the user towards the primary action (e.g., "Create Document").
**Action:** Replace text-only empty states with "Hero" empty states: Icon + Title + Description + Primary Action Button.

## 2024-05-28 - Global Focus Visibility
**Learning:** Custom CSS themes often reset browser defaults (like `outline: none`) but fail to provide a `:focus-visible` replacement, leaving keyboard users lost.
**Action:** Always include a global `:focus-visible` rule in the theme root to ensure all interactive elements have a visible focus indicator, using `outline` with `var(--color-primary)`.

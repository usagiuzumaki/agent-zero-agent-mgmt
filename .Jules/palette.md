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

## 2026-02-04 - Emojis as Icons
**Learning:** Emojis used as icons (like 🗑️ or ←) are often announced by their literal name (e.g., "Wastebasket", "Left Arrow") which can be confusing or redundant when accompanying text or when the action is specific (e.g., "Delete Document").
**Action:** Wrap decorative emojis in `<span aria-hidden="true">` and provide explicit `aria-label`s for the interactive element. For semantic icons (like status indicators), use `role="img"` and an `aria-label` describing the meaning, not the symbol.

# Manual Test: Empty States and AgentChat Fix

## Pre-requisites
1. Application is running (`npm run dev` or Docker container).
2. Browser is open to the application URL (e.g., http://localhost:50001).

## Test Case 1: AgentChat Load Verification
**Goal:** Verify that the AgentChat component loads without crashing due to missing `EmptyState` import.

1. Navigate to the "Assistant" tab (default view).
2. Ensure there are no existing messages (or clear local storage/start fresh session if needed).
3. **Verify:**
   - The chat interface is visible.
   - An empty state is displayed with the Aria logo/icon.
   - The title "Aria" is visible.
   - The description "I'm here to help with your screenwriting tasks..." is visible.
   - No "ReferenceError: EmptyState is not defined" appears in the browser console.

## Test Case 2: StorybookUI Hero Empty State
**Goal:** Verify the new "Hero" empty state in StorybookUI.

1. Navigate to the "Storybook" tab.
2. Ensure there are no documents (delete all if any exist).
3. **Verify:**
   - The empty state container is centered.
   - **Icon:** A book icon (📖) is visible.
   - **Title:** "No Documents Found" is displayed in bold/larger text.
   - **Description:** "Start your story by creating or uploading a new document." is displayed.
   - **Action:** A "Create First Document" button is visible and clickable.

## Test Case 3: CharactersUI Hero Empty State
**Goal:** Verify the new "Hero" empty state in CharactersUI.

1. Navigate to the "Characters" tab.
2. Ensure there are no characters (delete all if any exist).
3. **Verify:**
   - The empty state container is centered.
   - **Icon:** A users icon (👥) is visible.
   - **Title:** "No Characters Found" is displayed in bold/larger text.
   - **Description:** "Every story needs a cast! Start by creating your first character." is displayed.
   - **Action:** A "Create First Character" button is visible and clickable.

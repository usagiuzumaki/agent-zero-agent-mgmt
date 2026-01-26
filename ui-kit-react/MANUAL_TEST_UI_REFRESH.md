# Manual Test Plan: Screenwriting Studio UI Refresh

## 1. Prerequisites
- Environment variable `USE_REACT_UI` is set to `true`.
- Run `python run_ui.py`.
- Navigate to `http://localhost:5000` (or configured port).
- Log in if authentication is enabled.

## 2. Test Cases

### 2.1 Launch Screenwriting Studio
1. Click the "Agent" launcher button (bottom right).
2. In the modal, select "Screenwriting" from the UI dropdown.
3. **Verify:** The modal expands to full screen (or near full screen).
4. **Verify:** The layout changes to a dark "Studio" theme with a sidebar on the left.

### 2.2 Sidebar Navigation
1. Click "Assistant" tab in the sidebar.
   - **Verify:** The Chat interface appears in the main area.
2. Click "Storybook" tab.
   - **Verify:** The Storybook library view appears.
3. Click "Characters" tab.
   - **Verify:** The Cast of Characters grid appears.

### 2.3 Characters UI
1. Navigate to "Characters".
2. **Verify:** Characters are displayed as cards in a grid layout.
3. **Verify:** Each card shows an avatar placeholder (circle with initials) and role badge.
4. Click "+ Add Character" (top right or empty state).
   - **Verify:** A side drawer slides in from the right.
   - **Verify:** The drawer has a "Generate Traits" button (if name/archetype is empty).
5. Fill in dummy data and click "Save".
   - **Verify:** The drawer closes and the new character appears in the grid.
6. Click "Edit" on a character card.
   - **Verify:** The drawer opens with pre-filled data.

### 2.4 Storybook UI
1. Navigate to "Storybook".
2. **Verify:** Documents are listed in a grid.
3. Click on a Document to view details.
   - **Verify:** The view switches to the "Storyboard" view.
   - **Verify:** Beats are displayed in a horizontally scrolling list.
   - **Verify:** Beat cards look like index cards (white/off-white background, shadow).
4. Scroll the beat list horizontally.
   - **Verify:** Scrolling is smooth.

### 2.5 Responsiveness
1. Resize the browser window.
2. **Verify:** The sidebar remains fixed width.
3. **Verify:** The grid layouts (Characters, Documents) adjust columns automatically.

# Manual Verification Steps

1. **Build the Frontend**:
   - Run `cd ui-kit-react && pnpm install && pnpm build` to compile the React app.

2. **Start the Backend and Preview**:
   - In one terminal, run `python run_ui.py`.
   - In another terminal, run `cd ui-kit-react && pnpm preview`.

3. **Verify CharactersUI Spinner**:
   - Open the browser to the preview URL (usually `http://localhost:4173`).
   - Click on "Open Agent" if needed, and select "Screenwriting" mode.
   - Navigate to the "Characters" tab.
   - Click "+ Add Character".
   - Fill in dummy data (Name, Role, etc.).
   - Click "Save Character".
   - **Observe**: The button should change to "Saving..." and show a spinning icon. The button should be disabled.
   - Once saved, the form should close and the new character should appear in the list.

4. **Verify StorybookUI Spinner**:
   - Navigate to the "Storybook" tab.
   - Click "New Document".
   - Fill in a title and content.
   - Click "Ingest".
   - **Observe**: The button should change to "Ingesting..." and show a spinning icon. The button should be disabled.
   - Once ingested, the document should appear in the list.

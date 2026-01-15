# Build & Run Instructions (PowerShell)

## Prerequisites
1. Ensure **Node.js** is installed.
2. Install **pnpm** if you haven't:
   ```powershell
   npm install -g pnpm
   ```
3. Ensure **Python** dependencies are installed for the backend.

## Step-by-Step

Run these commands from the root of the repository.

### 1. Start the Python Backend
The React app needs the backend API to function. Run this to start it in a separate window:

```powershell
Start-Process python -ArgumentList "run_ui.py" -WorkingDirectory .
```

*Note: Keep this window open.*

### 2. Build and Run the React App
Run these commands to install dependencies, build the optimized production version, and serve it.

```powershell
# Navigate to the react project
cd ui-kit-react

# Install dependencies
pnpm install

# Build the project for production
pnpm build

# Serve the production build locally
pnpm preview
```

The terminal will show a local URL (e.g., `http://localhost:4173`). Open that in your browser.

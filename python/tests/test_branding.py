import os
import re
import pytest

def find_repo_root():
    # Start from current file location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up until we find README.md or .git
    while current_dir != "/":
        if os.path.exists(os.path.join(current_dir, "README.md")) or os.path.exists(os.path.join(current_dir, ".git")):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return os.getcwd() # Fallback

REPO_ROOT = find_repo_root()

# whitelist of allowed occurrences
ALLOWED_PATTERNS = [
    "formerly Agent Zero",
    "spin off of Agent Zero",
    "spin-off of Agent Zero",
    "credit to the original project by",
    "github.com/fredrl/agent-zero", # URL
    "agent0ai/agent-zero", # Docker image or repo
    "agent-zero:hacking", # Docker image tag
    "agent-zero/releases", # URL
    "agent-zero/discussions", # URL
    "agent-zero/agent-zero", # URL part
    "agent-zero folder", # Might be needed for migration instructions? No, we should rename it.
    "Original project by",
]

# Files to explicitly check
CHECK_DIRS = [
    "knowledge",
    "python",
    "webui",
    "docs",
    "agents",
    "prompts",
]

IGNORE_DIRS = [
    "__pycache__",
    ".git",
    ".vscode",
    "node_modules",
    "tests", # Skip tests directory to avoid self-flagging this file if we rename it, but we should check other tests
    "tmp",
    "logs",
    "_example",
]

IGNORE_FILES = [
    "test_branding.py", # This file
    "README_ARIA_NOTES.md", # Contains notes about the rebrand
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
]

def is_allowed(line):
    for pattern in ALLOWED_PATTERNS:
        if pattern in line:
            return True
    return False

def test_branding_recursive():
    print(f"Scanning from {REPO_ROOT}")

    errors = []

    for check_dir in CHECK_DIRS:
        start_path = os.path.join(REPO_ROOT, check_dir)
        if not os.path.exists(start_path):
            continue

        if os.path.isfile(start_path):
             # If it's a file (like webui/index.html might be passed if we change structure), check it
             files_to_check = [("", [], [os.path.basename(start_path)])]
             start_path = os.path.dirname(start_path)
        else:
            files_to_check = os.walk(start_path)

        for root, dirs, files in files_to_check:
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if file in IGNORE_FILES:
                    continue

                # specific check for python tests: we want to check them but maybe not this one
                if "test_branding.py" in file:
                    continue

                filepath = os.path.join(root, file)

                # Skip binary files or non-text
                if not file.endswith(('.py', '.md', '.txt', '.html', '.js', '.jsx', '.json')):
                    continue

                # Skip json files that are large data or generated
                if file.endswith('.json') and 'aria_memories.json' in file:
                    continue

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if "Agent Zero" in line:
                            if not is_allowed(line):
                                errors.append(f"{os.path.relpath(filepath, REPO_ROOT)}:{i+1}: {line.strip()}")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    if errors:
        pytest.fail(f"Found 'Agent Zero' in {len(errors)} locations:\n" + "\n".join(errors[:20]) + ("\n...and more" if len(errors) > 20 else ""))

def test_branding_in_run_ui_boot_message():
    path = os.path.join(REPO_ROOT, "run_ui.py")
    if not os.path.exists(path):
        return # Skip if not found (e.g. running in isolated environment)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for Aria Bot in boot message
    assert '[BOOT] Aria Bot' in content, "run_ui.py should contain '[BOOT] Aria Bot'"

def test_branding_in_agents():
    # Helper to check if a file contains "Aria Bot"
    def check_file(path):
        if not os.path.exists(path):
            pytest.fail(f"File {path} not found")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Aria Bot" in content, f"{path} should contain 'Aria Bot'"

    # Check key agent files
    check_file(os.path.join(REPO_ROOT, "agents/developer/prompts/agent.system.main.role.md"))
    check_file(os.path.join(REPO_ROOT, "agents/researcher/prompts/agent.system.main.role.md"))

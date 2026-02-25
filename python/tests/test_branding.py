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

# whitelist of allowed occurrences of the word "Aria"
ALLOWED_PATTERNS = [
    "Aria - AI Creative Companion",
    "Aria AI Creative Companion",
    "Aria System Manual",
    "formerly Aria",
    "spin off of Aria",
    "spin-off of Aria",
    "credit to the original project by",
    "github.com/fredrl/agent-zero", # URL
    "agent0ai/agent-zero", # Docker image or repo
    "agent-zero:hacking", # Docker image tag
    "agent-zero/releases", # URL
    "agent-zero/discussions", # URL
    "agent-zero/agent-zero", # URL part
    "agent-zero folder",
    "Original project by",
]

# Forbidden patterns that should have been replaced
FORBIDDEN_PATTERNS = [
    "Aria Bot",
    "Agent Zero",
    "AgentZero",
]

# Files to explicitly check
CHECK_DIRS = [
    "knowledge",
    "python",
    "webui",
    "docs"
]

IGNORE_DIRS = [
    "__pycache__",
    ".git",
    ".vscode",
    "node_modules",
    "tests",
    "tmp",
    "logs",
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

def test_no_forbidden_branding():
    errors = []
    for check_dir in CHECK_DIRS:
        start_path = os.path.join(REPO_ROOT, check_dir)
        if not os.path.exists(start_path):
            continue

        for root, dirs, files in os.walk(start_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                if file in IGNORE_FILES: continue
                filepath = os.path.join(root, file)
                if not file.endswith(('.py', '.md', '.txt', '.html', '.js', '.jsx', '.json')):
                    continue

                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    for pattern in FORBIDDEN_PATTERNS:
                        # Skip if the forbidden pattern is part of an allowed pattern
                        occurences = [m.start() for m in re.finditer(re.escape(pattern), content)]
                        for start_pos in occurences:
                            line_start = content.rfind('\n', 0, start_pos) + 1
                            line_end = content.find('\n', start_pos)
                            if line_end == -1: line_end = len(content)
                            line = content[line_start:line_end]

                            if not is_allowed(line):
                                errors.append(f"Forbidden pattern '{pattern}' found in {os.path.relpath(filepath, REPO_ROOT)} on line: {line.strip()}")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    if errors:
        pytest.fail("Found forbidden branding:\n" + "\n".join(errors))

def test_branding_in_run_ui_boot_message():
    path = os.path.join(REPO_ROOT, "run_ui.py")
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for Aria - AI Creative Companion in boot message
    assert '[BOOT] Aria - AI Creative Companion' in content, "run_ui.py should contain '[BOOT] Aria - AI Creative Companion'"

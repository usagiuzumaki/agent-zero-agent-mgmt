import os
import re

def test_branding_in_run_ui():
    if not os.path.exists("run_ui.py"):
        # Might be running from python/tests, so check parent
        if os.path.exists("../../run_ui.py"):
             path = "../../run_ui.py"
        else:
             path = "run_ui.py"
    else:
        path = "run_ui.py"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for Aria Bot in boot message
    assert '[BOOT] Aria Bot' in content, "run_ui.py should contain '[BOOT] Aria Bot'"

    # Check for no "Agent Zero" in boot message line
    boot_line_pattern = re.compile(r'PrintStyle\(\)\.print\(f"\[BOOT\].*Agent Zero.*"\)')
    assert not boot_line_pattern.search(content), "run_ui.py should not contain 'Agent Zero' in boot message"

def test_branding_in_docs():
    docs_dir = "docs"
    if not os.path.exists(docs_dir):
        if os.path.exists("../../docs"):
            docs_dir = "../../docs"
        else:
            return

    for root, dirs, files in os.walk(docs_dir):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "Agent Zero" in line:
                    # Allow "formerly Agent Zero"
                    if "(formerly Agent Zero)" in line:
                        continue

                    # Allow attribution/credit lines
                    if "Credit to the original project by" in line:
                        continue

                    # Allow links to the original repo or similar
                    if "github.com/fredrl/agent-zero" in line or "github.com/agent0ai/agent-zero" in line:
                        continue

                    # Fail
                    assert False, f"Found 'Agent Zero' in {filepath}:{i+1}: {line.strip()}"

def test_branding_in_python():
    python_dir = "python"
    if not os.path.exists(python_dir):
        if os.path.exists("../../python"):
            python_dir = "../../python"
        else:
            return

    for root, dirs, files in os.walk(python_dir):
        # Skip tests directory and __pycache__
        if "tests" in dirs:
            dirs.remove("tests")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        # Also skip tests folder itself if we are inside it?
        # The os.walk starts at python/, so python/tests is a child.
        if "tests" in root.split(os.sep):
             continue

        for filename in files:
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "Agent Zero" in line:
                    # Allow "formerly Agent Zero"
                    if "(formerly Agent Zero)" in line:
                        continue

                    # Allow variable names (snake_case)
                    # This is a naive check, but should cover most cases like self.agent_zero_root
                    if "agent_zero" in line or "AGENT_ZERO" in line:
                        # Ensure it's not part of a string literal that is user facing?
                        # It's hard to distinguish perfectly without AST, but let's see.
                        # If "Agent Zero" (with space) is in the line, it's likely a string or comment.
                        # If it is a variable like agent_zero_root, it won't have the space.
                        pass

                    # If the exact string "Agent Zero" is present
                    if "Agent Zero" in line:
                         # Allow comments if they are historical or explanatory about the variable
                         # But we want to catch user facing strings.
                         # Let's flag it if it contains "Agent Zero" with space,
                         # unless it is explicitly exempted.

                         # Exemptions:
                         if "Resolved Agent Zero root" in line: # Allow this specific comment if we must, but better to update it.
                             # Wait, the plan is to update comments too if possible.
                             # So I won't exempt it yet.
                             pass

                         if "formerly Agent Zero" in line:
                             continue

                         assert False, f"Found 'Agent Zero' in {filepath}:{i+1}: {line.strip()}"

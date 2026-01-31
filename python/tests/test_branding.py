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

    for filename in os.listdir(docs_dir):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(docs_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "Agent Zero" in line:
                # Allow "formerly Agent Zero"
                if "(formerly Agent Zero)" in line:
                    continue
                # Allow links to original repo
                if "github.com/fredrl/agent-zero" in line or "github.com/agent0ai/agent-zero" in line:
                    continue

                # Fail
                assert False, f"Found 'Agent Zero' in {filename}:{i+1}: {line.strip()}"

def test_branding_in_python_code():
    start_dir = "python"
    if not os.path.exists(start_dir):
        if os.path.exists("../../python"):
            start_dir = "../../python"
        else:
            assert False, "Could not find 'python' directory to test branding."

    # Walk through python directory
    for root, dirs, files in os.walk(start_dir):
        # Exclude tests directory and __pycache__
        if "tests" in dirs:
            dirs.remove("tests")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        # Skip if we are somehow inside a tests directory (e.g. nested)
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
                    # Exceptions
                    if "(formerly Agent Zero)" in line:
                        continue
                    # Allow credit/links
                    if "github.com/fredrl/agent-zero" in line or "github.com/agent0ai/agent-zero" in line:
                        continue

                    assert False, f"Found 'Agent Zero' in {filepath}:{i+1}: {line.strip()}"

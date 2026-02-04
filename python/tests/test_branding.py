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

                    # Fail
                    assert False, f"Found 'Agent Zero' in {filepath}:{i+1}: {line.strip()}"

def test_branding_in_backup_create():
    # Determine path to backup_create.py
    # From root: python/api/backup_create.py
    # From python/tests: ../api/backup_create.py

    path = "python/api/backup_create.py"
    if not os.path.exists(path):
        if os.path.exists("../api/backup_create.py"):
             path = "../api/backup_create.py"
        elif os.path.exists("../../python/api/backup_create.py"):
             path = "../../python/api/backup_create.py"

    assert os.path.exists(path), f"Could not find backup_create.py"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check default backup name
    assert 'backup_name = input.get("backup_name", "aria-bot-backup")' in content, \
        "backup_create.py should use 'aria-bot-backup' as default"

    # Check for Agent Zero string (specifically the old backup name)
    assert "agent-zero-backup" not in content, "backup_create.py should not contain 'agent-zero-backup'"

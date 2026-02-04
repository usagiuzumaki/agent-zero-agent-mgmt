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

def test_branding_recursive():
    # Define directories to check
    dirs_to_check = ["docs", "knowledge"]
    # Also check specific files
    files_to_check = ["webui/index.html"]

    # Adjust paths if running from python/tests
    if not os.path.exists("docs") and os.path.exists("../../docs"):
        root_dir = "../.."
    else:
        root_dir = "."

    errors = []

    # Helper to check a single file
    def check_file(filepath):
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "Agent Zero" in line:
                # Exceptions
                if "(formerly Agent Zero)" in line:
                    continue
                if "spin off of Agent Zero" in line:
                    continue
                if "Credit to the original project by" in line:
                    continue
                # URLs/Images - often contain agent-zero in path but might display text
                # We want to catch "Agent Zero" in text.

                # If "Agent Zero" is part of a code block or URL it usually shouldn't have spaces?
                # Actually "Agent Zero" has a space. URLs usually use %20 or dashes.
                # So if we see "Agent Zero" with a space, it is likely text.

                # Exception: "Agent Zero" in a link text might be valid if referring to the original project?
                # e.g. [Agent Zero](...)
                # But we want to rebrand to "Aria Bot".

                # Special case: "agent0ai/agent-zero" (no space) is fine (URL/repo name)
                # But "Agent Zero" has space.

                # Let's allow it if it's clearly discussing the legacy/original project.
                # But for now, let's flag it and filter manually if needed.

                # Check for "Agent Zero" explicitly
                errors.append(f"{filepath}:{i+1}: {line.strip()}")

    # Traverse directories
    for d in dirs_to_check:
        full_d = os.path.join(root_dir, d)
        if not os.path.exists(full_d):
            continue

        for root, _, files in os.walk(full_d):
            for filename in files:
                if filename.endswith((".md", ".txt", ".html")):
                    check_file(os.path.join(root, filename))

    # Check specific files
    for f in files_to_check:
        full_f = os.path.join(root_dir, f)
        if os.path.exists(full_f):
            check_file(full_f)

    if errors:
        assert False, "Found 'Agent Zero' in the following locations:\n" + "\n".join(errors[:50]) + ("\n...and more" if len(errors) > 50 else "")

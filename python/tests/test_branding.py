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
    assert '[BOOT] Aria - Creative Companion' in content, "run_ui.py should contain '[BOOT] Aria - Creative Companion'"

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

                # Allow in image alt text if we missed it? No, I replaced it.
                # Allow in link targets? URLs usually are lowercase or specific.
                # If there is a legitimate use, we can add exception.

                # Fail
                assert False, f"Found 'Agent Zero' in {filename}:{i+1}: {line.strip()}"

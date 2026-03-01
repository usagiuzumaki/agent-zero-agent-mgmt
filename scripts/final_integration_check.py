import sys
import os

# Check for presence of all key components
files_to_check = [
    "python/helpers/aria_models.py",
    "python/api/aria_fastapi.py",
    "scripts/init_aria_db.py",
    "aria-frontend/app/layout.tsx",
    "aria-frontend/components/editor/BookEditor.tsx",
    "aria-frontend/components/journal/PhotoJournal.tsx",
    "aria-frontend/components/moodboard/Moodboard.tsx"
]

all_found = True
for f in files_to_check:
    if os.path.exists(f):
        print(f"✅ Found {f}")
    else:
        print(f"❌ Missing {f}")
        all_found = False

if all_found:
    print("Integration check passed: All core artifacts are in place.")
else:
    print("Integration check failed: Some artifacts are missing.")
    sys.exit(1)

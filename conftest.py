import os
import sys

# Ensure repository root is on sys.path for tests
repo_root = os.path.dirname(__file__)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

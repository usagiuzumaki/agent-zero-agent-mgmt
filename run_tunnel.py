import runpy
import os
import sys

# Aria - AI Creative Companion Tunnel Stub
# This file is a stub that points to the actual implementation in scripts/run_tunnel.py

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, "scripts", "run_tunnel.py")

    # Ensure the root directory is in sys.path
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)

    runpy.run_path(script_path, run_name="__main__")

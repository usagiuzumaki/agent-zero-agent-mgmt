import os
import sys
try:
    from PIL import Image
except ImportError:
    print("Pillow not installed, skipping icon conversion.")
    sys.exit(0)

def convert_icon():
    # Assume script is run from root or we find paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    source = os.path.join(root_dir, "generated-icon.png")
    dest = os.path.join(root_dir, "aria.ico")

    if os.path.exists(dest):
        print(f"Icon already exists at {dest}")
        return

    if os.path.exists(source):
        try:
            img = Image.open(source)
            # Create a high-quality icon including multiple sizes
            img.save(dest, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
            print(f"Created {dest}")
        except Exception as e:
            print(f"Failed to create icon: {e}")
    else:
        print(f"Source icon {source} not found.")

if __name__ == "__main__":
    convert_icon()

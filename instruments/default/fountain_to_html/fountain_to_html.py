import sys
import html as html_lib


def main(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        script = f.read()

    escaped = html_lib.escape(script)
    output = f"<pre>{escaped}</pre>"
    print(output)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fountain_to_html.py <path_to_fountain>")
        sys.exit(1)
    main(sys.argv[1])

from pathlib import Path
import subprocess
from subprocess import CalledProcessError
from typing import Optional
from python.helpers import files
import os
import sys


# this helper ensures that playwright is installed in /lib/playwright
# should work for both docker and local installation

def get_playwright_binary():
    pw_cache = Path(get_playwright_cache_dir())
    headless_shell = next(pw_cache.glob("chromium_headless_shell-*/chrome-*/headless_shell"), None)
    return headless_shell

def get_playwright_cache_dir():
    return files.get_abs_path("tmp/playwright")

def ensure_playwright_binary():
    bin_path = get_playwright_binary()
    if not bin_path:
        cache = Path(get_playwright_cache_dir())
        cache.mkdir(parents=True, exist_ok=True)

        env = os.environ.copy()
        env["PLAYWRIGHT_BROWSERS_PATH"] = str(cache)

        install_attempts = [
            ("Playwright CLI", ["playwright", "install", "chromium", "--only-shell"]),
            (
                "python -m playwright",
                [sys.executable, "-m", "playwright", "install", "chromium", "--only-shell"],
            ),
        ]

        cli_missing_error: Optional[RuntimeError] = None

        for label, cmd in install_attempts:
            try:
                subprocess.check_call(cmd, env=env)
                break
            except FileNotFoundError as exc:  # pragma: no cover - host dependent
                if label == "Playwright CLI":
                    cli_missing_error = RuntimeError(
                        "Playwright CLI is not on PATH. Attempting python -m playwright "
                        "fallback. Install the project requirements with `pip install -r "
                        "requirements.txt` if the fallback also fails."
                    )
                    continue
                raise RuntimeError(
                    "Python executable missing while invoking Playwright."
                ) from exc
            except CalledProcessError as exc:  # pragma: no cover - subprocess failure
                if label == "python -m playwright":
                    raise RuntimeError(
                        "Playwright Python package is not installed or the browser "
                        "download failed. Run `pip install -r requirements.txt` and "
                        "retry."
                    ) from exc
                raise RuntimeError(
                    "Failed to download the headless Chromium shell. Rerun "
                    "`playwright install chromium --only-shell` and ensure the "
                    "command can access the internet."
                ) from exc
        else:  # pragma: no cover - loop exhausted without break
            if cli_missing_error:
                raise cli_missing_error

        bin_path = get_playwright_binary()
    if not bin_path:
        raise RuntimeError("Playwright binary not found after installation")
    return bin_path

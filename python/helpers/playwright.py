
from pathlib import Path
import subprocess
from subprocess import CalledProcessError
from python.helpers import files


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
        cache = get_playwright_cache_dir()
        import os

        env = os.environ.copy()
        env["PLAYWRIGHT_BROWSERS_PATH"] = cache
        try:
            subprocess.check_call(
                ["playwright", "install", "chromium", "--only-shell"], env=env
            )
        except FileNotFoundError as exc:  # pragma: no cover - depends on host setup
            raise RuntimeError(
                "Playwright CLI is not installed. Install the project requirements "
                "(`pip install -r requirements.txt`) before using the browser agent."
            ) from exc
        except CalledProcessError as exc:  # pragma: no cover - subprocess failure
            raise RuntimeError(
                "Failed to download the headless Chromium shell. Rerun `playwright "
                "install chromium --only-shell` and ensure the command can access "
                "the internet."
            ) from exc
        bin_path = get_playwright_binary()
    if not bin_path:
        raise RuntimeError("Playwright binary not found after installation")
    return bin_path

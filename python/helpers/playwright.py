from pathlib import Path
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError
from typing import Optional
from python.helpers import files
import os
import sys


_LOGGER = logging.getLogger(__name__)


# this helper ensures that playwright is installed in /lib/playwright
# should work for both docker and local installation

def get_playwright_binary():
    pw_cache = Path(get_playwright_cache_dir())
    headless_shell = next(pw_cache.glob("chromium_headless_shell-*/chrome-*/headless_shell"), None)
    return headless_shell

def get_playwright_cache_dir():
    return files.get_abs_path("tmp/playwright")

def ensure_playwright_binary():
    """Ensure the chromium headless shell is available for the browser tool.

    The helper will automatically install the ``playwright`` python package if it
    is missing and download the chromium shell into the local cache directory.
    """

    bin_path = get_playwright_binary()
    if bin_path:
        return bin_path

    cache = get_playwright_cache_dir()
    env = os.environ.copy()
    env["PLAYWRIGHT_BROWSERS_PATH"] = cache

    _ensure_playwright_package()

    try:
        subprocess.check_call(
            [sys.executable, "-m", "playwright", "install", "chromium", "--only-shell"],
            env=env,
        )
    except CalledProcessError as exc:  # pragma: no cover - subprocess failure
        raise RuntimeError(
            "Failed to download the headless Chromium shell. Rerun `playwright "
            "install chromium --only-shell` and ensure the command can access "
            "the internet."
        ) from exc

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


def _ensure_playwright_package() -> None:
    """Install the :mod:`playwright` package if it is not present."""

    try:
        importlib.import_module("playwright")
        return
    except ModuleNotFoundError:
        _LOGGER.warning(
            "Playwright python package not found. Attempting automatic installation..."
        )

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    except CalledProcessError as exc:  # pragma: no cover - subprocess failure
        raise RuntimeError(
            "Playwright CLI is not installed and automatic installation failed. "
            "Install it manually with `pip install playwright` before using the "
            "browser agent."
        ) from exc

    try:
        importlib.import_module("playwright")
    except ModuleNotFoundError as exc:  # pragma: no cover - unexpected failure
        raise RuntimeError(
            "Playwright package installation succeeded but the module is still "
            "unavailable. Verify your python environment before retrying."
        ) from exc

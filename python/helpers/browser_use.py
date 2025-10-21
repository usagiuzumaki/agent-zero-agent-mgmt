"""Thin wrapper around the optional ``browser_use`` dependency.

The Browser Agent tool relies on the external ``browser-use`` package.  In
some environments this dependency is not installed by default (and the newest
versions bring in conflicting transitive requirements).  Importing the tool
module should therefore not fail outright – instead we expose a lightweight
proxy that raises a helpful error message when the tool is actually used.
"""

from __future__ import annotations

from typing import Any

from python.helpers import dotenv


dotenv.save_dotenv_value("ANONYMIZED_TELEMETRY", "false")


class _MissingBrowserUseAttr:
    """Callable placeholder that raises a helpful import error when used."""

    def __init__(self, exc: ModuleNotFoundError):
        self._exc = exc

    _HELP_TEXT = (
        "Optional dependency 'browser-use' is required for the browser agent tool. "
        "Install the UI extras with `pip install -r requirements.txt` and run "
        "`playwright install chromium --only-shell` to finish the setup."
    )

    def __call__(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover
        raise ModuleNotFoundError(self._HELP_TEXT) from self._exc

    def __getattr__(self, item: str) -> Any:  # pragma: no cover
        raise ModuleNotFoundError(self._HELP_TEXT) from self._exc


class _MissingBrowserUseProxy:
    """Fallback module-like object used when ``browser-use`` is missing."""

    def __init__(self, exc: ModuleNotFoundError):
        self._exc = exc

    def __getattr__(self, item: str) -> Any:  # pragma: no cover - simple proxy
        return _MissingBrowserUseAttr(self._exc)


try:  # pragma: no cover - import guarded to support optional dependency
    import browser_use  # type: ignore
    import browser_use.utils  # type: ignore
except ModuleNotFoundError as exc:  # pragma: no cover - executed when missing
    browser_use = _MissingBrowserUseProxy(exc)  # type: ignore[assignment]

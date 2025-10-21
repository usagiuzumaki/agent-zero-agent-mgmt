import argparse
import inspect
import logging
import secrets
from typing import TypeVar, Callable, Awaitable, Union, overload, cast
from urllib.parse import urlparse, urlunparse
from python.helpers import dotenv, rfc, files
import asyncio
import threading
import queue
import sys
import aiohttp

T = TypeVar('T')
R = TypeVar('R')

parser = argparse.ArgumentParser()
args = {}
dockerman = None
runtime_id = None
_rfc_connection_notified: set[str] = set()


def initialize():
    global args
    if args:
        return
    parser.add_argument("--port", type=int, default=None, help="Web UI port")
    parser.add_argument("--host", type=str, default=None, help="Web UI host")
    parser.add_argument(
        "--cloudflare_tunnel",
        type=bool,
        default=False,
        help="Use cloudflare tunnel for public URL",
    )
    parser.add_argument(
        "--development", type=bool, default=False, help="Development mode"
    )

    known, unknown = parser.parse_known_args()
    args = vars(known)
    for arg in unknown:
        if "=" in arg:
            key, value = arg.split("=", 1)
            key = key.lstrip("-")
            args[key] = value

def get_arg(name: str):
    global args
    return args.get(name, None)

def has_arg(name: str):
    global args
    return name in args

def is_dockerized() -> bool:
    return bool(get_arg("dockerized"))

def is_development() -> bool:
    return not is_dockerized()

def get_local_url():
    if is_dockerized():
        return "host.docker.internal"
    return "127.0.0.1"

def get_runtime_id() -> str:
    global runtime_id
    if not runtime_id:
        runtime_id = secrets.token_hex(8)   
    return runtime_id

def get_persistent_id() -> str:
    id = dotenv.get_dotenv_value("A0_PERSISTENT_RUNTIME_ID")
    if not id:
        id = secrets.token_hex(16)
        dotenv.save_dotenv_value("A0_PERSISTENT_RUNTIME_ID", id)
    return id

@overload
async def call_development_function(func: Callable[..., Awaitable[T]], *args, **kwargs) -> T: ...

@overload
async def call_development_function(func: Callable[..., T], *args, **kwargs) -> T: ...

async def call_development_function(func: Union[Callable[..., T], Callable[..., Awaitable[T]]], *args, **kwargs) -> T:
    if not is_development():
        return await _execute_locally(func, *args, **kwargs)

    url = _get_rfc_url()
    password = _get_rfc_password()
    rel_path = files.deabsolute_path(func.__code__.co_filename)
    module = rel_path.replace("\\", "/").replace("/", ".").removesuffix(".py")  # __module__ is not reliable

    try:
        result = await rfc.call_rfc(
            url=url,
            password=password,
            module=module,
            function_name=func.__name__,
            args=list(args),
            kwargs=kwargs,
        )
    except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
        _log_rfc_connection_issue(url, exc)
        return await _execute_locally(func, *args, **kwargs)
    except Exception as exc:  # pragma: no cover - propagated runtime errors
        raise RuntimeError(
            "RFC call to {module}.{function} via {url} failed: {error}".format(
                module=module,
                function=func.__name__,
                url=url,
                error=exc,
            )
        ) from exc

    return cast(T, result)


async def handle_rfc(rfc_call: rfc.RFCCall):
    return await rfc.handle_rfc(rfc_call=rfc_call, password=_get_rfc_password())


async def _execute_locally(
    func: Union[Callable[..., T], Callable[..., Awaitable[T]]], *args, **kwargs
) -> T:
    if inspect.iscoroutinefunction(func):
        return cast(T, await func(*args, **kwargs))
    return cast(T, func(*args, **kwargs))


def _log_rfc_connection_issue(url: str, exc: Exception) -> None:
    fingerprint = f"{url}|{type(exc).__name__}"
    if fingerprint in _rfc_connection_notified:
        return

    _rfc_connection_notified.add(fingerprint)

    message = (
        "[runtime] Unable to reach RFC endpoint at {url} ({error_name}: {error}). "
        "Falling back to local execution. Start the Agent Zero UI (run_ui.py) "
        "and confirm RFC_URL/RFC_PASSWORD match across instances for remote calls."
    ).format(url=url, error_name=type(exc).__name__, error=exc)

    try:
        print(message, file=sys.stderr)
    except Exception:
        pass


def ensure_secret(
    key: str,
    *,
    label: str,
    length: int = 32,
    show_value: bool = False,
) -> str:
    """Ensure a persistent secret exists in ``.env`` and return it.

    Args:
        key: Environment variable key to read/write.
        label: Human readable label used for console notices.
        length: Amount of entropy to request from :func:`secrets.token_urlsafe`.
        show_value: When ``True`` include the generated secret in the notice
            message.  Defaults to ``False`` to avoid leaking credentials in
            shared logs.
    """

    value = (dotenv.get_dotenv_value(key) or "").strip()
    if value:
        return value

    token = secrets.token_urlsafe(length)
    dotenv.save_dotenv_value(key, token)

    notice = (
        f"[runtime] Auto-generated {label}. It has been stored under {key} in "
        f"{dotenv.get_dotenv_file_path()}. Ensure peer runtimes use the same "
        "value if they need to communicate."
    )

    try:
        print(notice, file=sys.stderr)
        if show_value:
            print(f"[runtime] {label}: {token}", file=sys.stderr)
    except Exception:
        pass

    return token


def _get_rfc_password() -> str:
    return ensure_secret(
        dotenv.KEY_RFC_PASSWORD,
        label="RFC password",
        length=48,
        show_value=False,
    )


def _get_rfc_url() -> str:
    from python.helpers import settings

    set = settings.get_settings()

    raw_url = set["rfc_url"].strip()
    if not raw_url:
        raw_url = "localhost"

    if "://" not in raw_url:
        raw_url = f"http://{raw_url}"

    parsed = urlparse(raw_url)

    scheme = parsed.scheme or "http"
    host = parsed.hostname or parsed.path or "localhost"

    # Always expose the RFC HTTP endpoint on port 5000 for consistency across environments.
    port = 5000

    # normalize IPv6 formatting
    formatted_host = host
    if ":" in host and not host.startswith("["):
        formatted_host = f"[{host}]"

    if parsed.username:
        userinfo = parsed.username
        if parsed.password:
            userinfo = f"{userinfo}:{parsed.password}"
        formatted_host = f"{userinfo}@{formatted_host}"

    netloc = formatted_host
    if port:
        netloc = f"{formatted_host}:{port}"

    base_path = parsed.path if parsed.netloc else ""
    base_path = base_path.rstrip("/")
    final_path = f"{base_path}/rfc" if base_path else "/rfc"

    return urlunparse((scheme, netloc, final_path, "", "", ""))


def call_development_function_sync(func: Union[Callable[..., T], Callable[..., Awaitable[T]]], *args, **kwargs) -> T:
    # run async function in sync manner
    result_queue = queue.Queue()
    
    def run_in_thread():
        result = asyncio.run(call_development_function(func, *args, **kwargs))
        result_queue.put(result)
    
    thread = threading.Thread(target=run_in_thread)
    thread.start()
    thread.join(timeout=30)  # wait for thread with timeout
    
    if thread.is_alive():
        raise TimeoutError("Function call timed out after 30 seconds")
    
    result = result_queue.get_nowait()
    return cast(T, result)


def get_web_ui_port():
    web_ui_port = (
        get_arg("port")
        or int(dotenv.get_dotenv_value("WEB_UI_PORT", 0))
        or 5000
    )
    return web_ui_port

def get_tunnel_api_port():
    tunnel_api_port = (
        get_arg("tunnel_api_port")
        or int(dotenv.get_dotenv_value("TUNNEL_API_PORT", 0))
        or 55520
    )
    return tunnel_api_port

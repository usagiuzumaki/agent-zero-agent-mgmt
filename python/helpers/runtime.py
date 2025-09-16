import argparse
import inspect
import secrets
from typing import TypeVar, Callable, Awaitable, Union, overload, cast
from urllib.parse import urlparse, urlunparse
from python.helpers import dotenv, rfc, files
import asyncio
import threading
import queue

T = TypeVar('T')
R = TypeVar('R')

parser = argparse.ArgumentParser()
args = {}
dockerman = None
runtime_id = None


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
    if is_development():
        url = _get_rfc_url()
        password = _get_rfc_password()
        rel_path = files.deabsolute_path(func.__code__.co_filename)
        module = rel_path.replace("\\", "/").replace("/", ".").removesuffix(".py")  # __module__ is not reliable
        result = await rfc.call_rfc(
            url=url,
            password=password,
            module=module,
            function_name=func.__name__,
            args=list(args),
            kwargs=kwargs,
        )
        return cast(T, result)
    else:
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs) # type: ignore


async def handle_rfc(rfc_call: rfc.RFCCall):
    return await rfc.handle_rfc(rfc_call=rfc_call, password=_get_rfc_password())


def _get_rfc_password() -> str:
    password = dotenv.get_dotenv_value(dotenv.KEY_RFC_PASSWORD)
    if not password:
        raise Exception("No RFC password, cannot handle RFC calls.")
    return password


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

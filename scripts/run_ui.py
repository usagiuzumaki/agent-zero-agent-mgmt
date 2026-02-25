from datetime import timedelta
import os
import secrets
import sys
import time
import socket
import struct
import asyncio
import inspect
from functools import wraps
import threading
import signal
from flask import Flask, request, Response, session, render_template_string, send_from_directory
from flask_basicauth import BasicAuth
from python.helpers import initialize
from python.helpers import files, git, mcp_server
from python.helpers.files import get_abs_path
from python.helpers import runtime, dotenv, process
from python.helpers.extract_tools import load_classes_from_folder
from python.helpers.api import ApiHandler
from python.helpers.print_style import PrintStyle

try:
    from python.api.auth.auth_models import init_db
    from python.api.auth.supabase_auth import init_supabase_auth, require_login
    from python.api.auth.stripe_payments import init_stripe_routes
    from python.api.image_generation_endpoint import register_image_routes
    from flask_login import current_user
    _auth_available = True
except Exception as e:
    PrintStyle().print(f"Warning: Auth/Payment modules not available: {e}")
    _auth_available = False

    def require_login(f):
        return f


# Set the new timezone to 'UTC'
os.environ["TZ"] = "UTC"
# Apply the timezone change
if hasattr(time, 'tzset'):
    time.tzset()

# initialize the internal Flask server
static_folder_path = "./webui"
if os.environ.get("USE_REACT_UI") == "true":
    static_folder_path = "./ui-kit-react/dist"

webapp = Flask("app", static_folder=get_abs_path(static_folder_path), static_url_path="/")
webapp.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)
webapp.config.update(
    JSON_SORT_KEYS=False,
    SESSION_COOKIE_NAME="session_" + runtime.get_runtime_id(),  # bind the session cookie name to runtime id to prevent session collision on same host
    SESSION_COOKIE_SAMESITE="Strict",
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(days=1)
)


lock = threading.Lock()

# Set up basic authentication for UI and API but not MCP
basic_auth = BasicAuth(webapp)


def is_loopback_address(address):
    loopback_checker = {
        socket.AF_INET: lambda x: struct.unpack("!I", socket.inet_aton(x))[0]
        >> (32 - 8)
        == 127,
        socket.AF_INET6: lambda x: x == "::1",
    }
    address_type = "hostname"
    try:
        socket.inet_pton(socket.AF_INET6, address)
        address_type = "ipv6"
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET, address)
            address_type = "ipv4"
        except socket.error:
            address_type = "hostname"

    if address_type == "ipv4":
        return loopback_checker[socket.AF_INET](address)
    elif address_type == "ipv6":
        return loopback_checker[socket.AF_INET6](address)
    else:
        for family in (socket.AF_INET, socket.AF_INET6):
            try:
                r = socket.getaddrinfo(address, None, family, socket.SOCK_STREAM)
            except socket.gaierror:
                return False
            for family, _, _, _, sockaddr in r:
                if not loopback_checker[family](sockaddr[0]):
                    return False
        return True


def _run_maybe_async(result):
    """Run the given result if it's awaitable, otherwise return it as-is."""

    if inspect.isawaitable(result):
        # ``asyncio.run`` creates and manages an event loop which avoids the
        # ``get_event_loop`` failures observed when Werkzeug handles requests in
        # worker threads without a default loop.
        try:
            return asyncio.run(result)
        except RuntimeError as exc:
            # ``asyncio.run`` raises when called from within a running loop.
            if "asyncio.run() cannot be called" not in str(exc):
                raise

            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(result)
            finally:
                asyncio.set_event_loop(None)
                loop.close()
    return result


def requires_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        valid_api_key = dotenv.get_dotenv_value("API_KEY")
        if api_key := request.headers.get("X-API-KEY"):
            if api_key != valid_api_key:
                return Response("API key required", 401)
        elif request.json and request.json.get("api_key"):
            api_key = request.json.get("api_key")
            if api_key != valid_api_key:
                return Response("API key required", 401)
        else:
            return Response("API key required", 401)
        return _run_maybe_async(f(*args, **kwargs))

    return decorated


# allow only loopback addresses
def requires_loopback(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_loopback_address(request.remote_addr):
            return Response(
                "Access denied.",
                403,
                {},
            )
        return _run_maybe_async(f(*args, **kwargs))

    return decorated


# require authentication for handlers
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = dotenv.get_dotenv_value("AUTH_LOGIN")
        password = dotenv.get_dotenv_value("AUTH_PASSWORD")
        if user and password:
            auth = request.authorization
            if not auth or not (auth.username == user and auth.password == password):
                return Response(
                    "Could not verify your access level for that URL.\n"
                    "You have to login with proper credentials",
                    401,
                    {"WWW-Authenticate": 'Basic realm="Login Required"'},
                )
        return _run_maybe_async(f(*args, **kwargs))

    return decorated


def csrf_protect(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("csrf_token")
        header = request.headers.get("X-CSRF-Token")
        cookie = request.cookies.get("csrf_token_" + runtime.get_runtime_id())
        sent = header or cookie
        if not token or not sent or token != sent:
            return Response("CSRF token missing or invalid", 403)
        return _run_maybe_async(f(*args, **kwargs))

    return decorated


# handle default address, load index
@webapp.route("/", methods=["GET"])
@requires_auth
async def serve_index():
    # Check if user is authenticated and hasn't paid
    if _auth_available:
        try:
            from flask_login import current_user
            if current_user.is_authenticated and not current_user.has_paid:
                return redirect('/payment/required')
        except:
            pass

    if os.environ.get("USE_REACT_UI") == "true":
        return send_from_directory(get_abs_path("./ui-kit-react/dist"), "index.html")

    gitinfo = None
    try:
        gitinfo = git.get_git_info()
    except Exception:
        gitinfo = {
            "version": "unknown",
            "commit_time": "unknown",
        }
    return files.read_file(
        "./webui/index.html",
        version_no=gitinfo["version"],
        version_time=gitinfo["commit_time"],
    )


@webapp.route("/healthz")
@webapp.route("/api/health")
def health_check():
    """Fast health check endpoint for deployment monitoring - responds under 1 second"""
    # Minimal response for quick health checks
    return {"status": "healthy", "service": "Aria"}, 200


@webapp.route("/login")
def login_page():
    if _auth_available:
        try:
            return files.read_file("./webui/login.html")
        except Exception:
            pass
    return "Login page not available", 404


@webapp.route("/dashboard")
@require_login
def dashboard_page():
    if _auth_available:
        try:
            return files.read_file("./webui/dashboard.html")
        except Exception:
            pass
    return "Dashboard not available", 404


@webapp.route("/payment")
@require_login
def payment_page():
    if _auth_available:
        try:
            return files.read_file("./webui/payment.html")
        except Exception:
            pass
    return "Payment page not available", 404


@webapp.route("/payment-success")
@require_login
def payment_success():
    session_id = request.args.get('session_id', 'unknown')
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Payment Success</title></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; text-align: center;">
        <h1 style="color: #4CAF50;">Payment Successful!</h1>
        <p>Thank you for your payment. Session ID: {session_id}</p>
        <a href="/dashboard" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Return to Dashboard</a>
    </body>
    </html>
    """


@webapp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return {"error": "Resource not found", "status": 404}, 404


@webapp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    PrintStyle().error(f"Internal server error: {error}")
    return {"error": "Internal server error", "status": 500}, 500


@webapp.errorhandler(Exception)
def handle_exception(error):
    """Handle all uncaught exceptions"""
    PrintStyle().error(f"Unhandled exception: {error}")
    return {"error": "An unexpected error occurred", "status": 500}, 500


def run():
    # Attempt to free port 5000 if it's already in use
    try:
        port = int(os.getenv("PORT") or runtime.get_web_ui_port())
        PrintStyle().print(f"Checking if port {port} is free...")
        import subprocess
        # Check if port is in use and kill process if so
        cmd = f"lsof -ti:{port} | xargs kill -9 2>/dev/null || true"
        subprocess.run(cmd, shell=True)
    except Exception as e:
        PrintStyle().warning(f"Failed to free port: {e}")

    # Log startup information
    commit_hash = os.getenv("GITHUB_SHA", "unknown")[:7]
    port = int(os.getenv("PORT") or runtime.get_web_ui_port())
    PrintStyle().print(f"[BOOT] Aria - AI Creative Companion | commit: {commit_hash} | port: {port}")
    PrintStyle().print("Initializing framework...")

    # Suppress only request logs but keep the startup messages
    from werkzeug.serving import WSGIRequestHandler
    from werkzeug.serving import make_server
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from a2wsgi import ASGIMiddleware

    PrintStyle().print("Starting server...")

    if _auth_available:
        try:
            PrintStyle().print("Initializing database and authentication...")
            db_initialized = init_db(webapp)
            if db_initialized:
                init_supabase_auth(webapp)
                init_stripe_routes(webapp)
                register_image_routes(webapp)

                # Register payment gate blueprint
                from python.api.auth.payment_gate import payment_gate
                webapp.register_blueprint(payment_gate)

                # Register user data API
                from python.api.user_data import init_user_data_api
                init_user_data_api(webapp)

                PrintStyle().print("✅ Supabase-backed auth with $19 payment gate is ready!")
            else:
                PrintStyle().print("⚠️ Database (SUPABASE_DB_URL) not found or sleeping. Auth features temporarily disabled.")
                PrintStyle().print("👉 Please check your .env file and ensure SUPABASE_DB_URL is set correctly.")
            PrintStyle().print("Authentication and payment routes configured successfully")
        except Exception as e:
            PrintStyle().print(f"Warning: Failed to initialize auth/payment: {e}")

    class NoRequestLoggingWSGIRequestHandler(WSGIRequestHandler):
        def log_request(self, code="-", size="-"):
            pass  # Override to suppress request logging

    # Get configuration from environment
    port = int(os.getenv("PORT") or runtime.get_web_ui_port())
    host = (
        runtime.get_arg("host") or dotenv.get_dotenv_value("WEB_UI_HOST") or "localhost"
    )
    server = None

    def register_api_handler(app, handler: type[ApiHandler]):
        name = handler.__module__.split(".")[-1]
        instance = handler(app, lock)

        def handler_wrap():
            return _run_maybe_async(instance.handle_request(request=request))

        if handler.requires_loopback():
            handler_wrap = requires_loopback(handler_wrap)
        if handler.requires_auth():
            handler_wrap = requires_auth(handler_wrap)
        if handler.requires_api_key():
            handler_wrap = requires_api_key(handler_wrap)
        if handler.requires_csrf():
            handler_wrap = csrf_protect(handler_wrap)

        app.add_url_rule(
            f"/{name}",
            f"/{name}",
            handler_wrap,
            methods=handler.get_methods(),
        )

    # initialize and register API handlers
    handlers = load_classes_from_folder("python/api", "*.py", ApiHandler)
    for handler in handlers:
        register_api_handler(webapp, handler)

    # Register Screenwriting Blueprint
    try:
        from python.api.screenwriting import screenwriting_bp
        webapp.register_blueprint(screenwriting_bp)
    except Exception as e:
        PrintStyle().print(f"Warning: Failed to register screenwriting blueprint: {e}")

    # add the webapp and mcp to the app
    app = DispatcherMiddleware(
        webapp,
        {
            "/mcp": ASGIMiddleware(app=mcp_server.DynamicMcpProxy.get_instance()),  # type: ignore
        },
    )

    server = make_server(
        host=host,
        port=port,
        app=app,
        request_handler=NoRequestLoggingWSGIRequestHandler,
        threaded=True,
    )
    process.set_server(server)
    port = server.server_port
    runtime.args["port"] = port
    PrintStyle().debug(f"Starting server at http://{host}:{port} ...")
    server.log_startup()

    # Start init_a0 in a background thread when server starts
    # threading.Thread(target=init_a0, daemon=True).start()
    init_a0()

    # run the server
    server.serve_forever()


def init_a0():
    # initialize contexts and MCP
    init_chats = initialize.initialize_chats()
    # only wait for init chats, otherwise they would seem to disappear for a while on restart
    init_chats.result_sync()

    initialize.initialize_mcp()
    # start job loop
    initialize.initialize_job_loop()
    # preload
    initialize.initialize_preload()



# run the internal server
if __name__ == "__main__":
    runtime.initialize()
    dotenv.load_dotenv()
    run()

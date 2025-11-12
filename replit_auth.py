import os
import secrets
import uuid
from functools import wraps
from urllib.parse import urlencode

import requests
from flask import Blueprint, request, redirect, session, url_for, jsonify, current_app
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.middleware.proxy_fix import ProxyFix

from auth_models import db, User, OAuth


replit_auth = Blueprint('replit_auth', __name__, url_prefix='/auth')
login_manager = LoginManager()


class UserSessionStorage:
    @staticmethod
    def get_session_key():
        if 'browser_session_key' not in session:
            session['browser_session_key'] = secrets.token_urlsafe(32)
        return session['browser_session_key']

    @staticmethod
    def get_user_from_session():
        session_key = UserSessionStorage.get_session_key()
        oauth = OAuth.query.filter_by(browser_session_key=session_key).first()
        if oauth:
            return User.query.get(oauth.user_id)
        return None

    @staticmethod
    def save_user_session(user_id, token=None, provider='email'):
        session_key = UserSessionStorage.get_session_key()

        oauth = OAuth.query.filter_by(browser_session_key=session_key).first()
        if oauth:
            oauth.user_id = user_id
            oauth.provider = provider
            if token is not None:
                oauth.token = token
        else:
            oauth = OAuth(
                user_id=user_id,
                browser_session_key=session_key,
                provider=provider,
                token=token,
            )
            db.session.add(oauth)

        db.session.commit()

    @staticmethod
    def clear_user_session():
        session_key = session.get('browser_session_key')
        if session_key:
            OAuth.query.filter_by(browser_session_key=session_key).delete()
            db.session.commit()
        session.clear()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    if current_user.is_authenticated and not current_user.has_paid:
        return redirect('/payment/required')
    return redirect(url_for('login_page'))


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login_page'))
        if not current_user.has_paid:
            return redirect('/payment/required')
        return f(*args, **kwargs)

    return decorated_function


def require_payment(f):
    """Decorator that requires user to be authenticated AND have paid"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login_page'))
        if not current_user.has_paid:
            return redirect('/payment/required')
        return f(*args, **kwargs)

    return decorated_function


def _get_base_url():
    explicit = os.getenv('AUTH_BASE_URL')
    if explicit:
        return explicit.rstrip('/')

    dev_domain = os.getenv('REPLIT_DEV_DOMAIN', '')
    domains = os.getenv('REPLIT_DOMAINS', '')
    base_domain = dev_domain or (domains.split(',')[0] if domains else '')
    if base_domain:
        return f"https://{base_domain}"

    app_url = os.getenv('PUBLIC_URL') or os.getenv('APP_URL')
    if app_url:
        return app_url.rstrip('/')

    raise ValueError(
        "AUTH_BASE_URL, PUBLIC_URL, or Replit domain environment variables are required"
    )


def get_google_oauth_config():
    client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError(
            'GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET environment variables are required'
        )

    redirect_uri = os.getenv('GOOGLE_OAUTH_REDIRECT_URI')
    if not redirect_uri:
        redirect_uri = f"{_get_base_url()}/auth/callback"

    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'authorization_endpoint': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_endpoint': 'https://oauth2.googleapis.com/token',
        'userinfo_endpoint': 'https://openidconnect.googleapis.com/v1/userinfo',
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile',
    }


def _normalize_email(value: str) -> str:
    return (value or '').strip().lower()


@replit_auth.route('/login')
def login():
    return redirect(url_for('login_page'))


@replit_auth.route('/login/google')
def login_with_google():
    try:
        config = get_google_oauth_config()
    except Exception as exc:
        current_app.logger.error(f"Google OAuth configuration error: {exc}")
        return (
            "Google sign-in is not configured. Please contact support.",
            500,
        )

    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    params = {
        'client_id': config['client_id'],
        'redirect_uri': config['redirect_uri'],
        'response_type': 'code',
        'scope': config['scope'],
        'state': state,
        'access_type': 'offline',
        'prompt': 'select_account',
        'include_granted_scopes': 'true',
    }

    auth_url = f"{config['authorization_endpoint']}?{urlencode(params)}"
    return redirect(auth_url)


@replit_auth.route('/callback')
def callback():
    try:
        code = request.args.get('code')
        state = request.args.get('state')

        if not code or not state:
            return "Missing authorization code or state", 400

        if state != session.get('oauth_state'):
            return "Invalid state parameter", 400

        config = get_google_oauth_config()

        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': config['redirect_uri'],
            'client_id': config['client_id'],
            'client_secret': config['client_secret'],
        }

        token_response = requests.post(config['token_endpoint'], data=token_data)
        token_response.raise_for_status()
        tokens = token_response.json()

        access_token = tokens.get('access_token')
        if not access_token:
            return "Failed to obtain access token", 500

        userinfo_response = requests.get(
            config['userinfo_endpoint'],
            headers={'Authorization': f'Bearer {access_token}'},
        )
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()

        email = _normalize_email(userinfo.get('email'))
        if not email:
            return "Failed to obtain email address from Google", 500

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                id=userinfo.get('sub') or str(uuid.uuid4()),
                email=email,
                first_name=userinfo.get('given_name', ''),
                last_name=userinfo.get('family_name', ''),
                profile_image_url=userinfo.get('picture', ''),
            )
            db.session.add(user)
        else:
            user.first_name = userinfo.get('given_name', user.first_name)
            user.last_name = userinfo.get('family_name', user.last_name)
            user.profile_image_url = userinfo.get('picture', user.profile_image_url)

        db.session.commit()

        UserSessionStorage.save_user_session(user.id, access_token, provider='google')
        login_user(user, remember=True)

        session.pop('oauth_state', None)

        if not user.has_paid:
            return redirect('/payment/required')

        return redirect('/')

    except Exception as exc:
        current_app.logger.error(f"Google authentication error: {exc}")
        return f"Authentication error: {exc}", 500


@replit_auth.route('/login/email', methods=['POST'])
def login_with_email():
    try:
        data = request.get_json() or {}
        email = _normalize_email(data.get('email'))
        password = (data.get('password') or '').strip()
        first_name = (data.get('first_name') or '').strip()
        last_name = (data.get('last_name') or '').strip()
        mode = (data.get('mode') or 'login').strip().lower()

        if not email or '@' not in email:
            return jsonify({'error': 'Please enter a valid email address.'}), 400

        if not password or len(password) < 6:
            return (
                jsonify({'error': 'Password must be at least 6 characters long.'}),
                400,
            )

        user = User.query.filter_by(email=email).first()

        if mode == 'register':
            if user and user.password_hash:
                return (
                    jsonify({'error': 'An account with this email already exists. Sign in instead.'}),
                    400,
                )

            if not user:
                user = User(
                    id=str(uuid.uuid4()),
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                db.session.add(user)
            else:
                user.first_name = first_name or user.first_name
                user.last_name = last_name or user.last_name

            user.set_password(password)
        else:  # login flow
            if not user:
                return (
                    jsonify({'error': 'No account found. Create an account to get started.'}),
                    404,
                )

            if not user.password_hash:
                return (
                    jsonify({'error': 'This email is linked to a social login. Use Google sign-in instead.'}),
                    400,
                )

            if not user.check_password(password):
                return jsonify({'error': 'Incorrect email or password.'}), 401

        db.session.commit()

        login_user(user, remember=True)
        UserSessionStorage.save_user_session(user.id, provider='email')

        redirect_url = '/' if user.has_paid else '/payment/required'
        return jsonify({'redirect': redirect_url})

    except Exception as exc:
        current_app.logger.error(f"Email authentication error: {exc}")
        db.session.rollback()
        return jsonify({'error': 'Unable to sign in right now. Please try again later.'}), 500


@replit_auth.route('/logout')
@login_required
def logout():
    UserSessionStorage.clear_user_session()
    logout_user()
    return redirect(url_for('login_page'))


@replit_auth.route('/user')
@login_required
def user_info():
    return jsonify(
        {
            'id': current_user.id,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'profile_image_url': current_user.profile_image_url,
            'has_paid': current_user.has_paid,
            'subscription_status': current_user.subscription_status,
        }
    )


def init_replit_auth(app):
    session_secret = os.getenv('SESSION_SECRET')
    if not session_secret:
        raise ValueError('SESSION_SECRET environment variable is required')

    if not app.secret_key:
        app.secret_key = session_secret

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    login_manager.init_app(app)
    login_manager.login_view = 'replit_auth.login'

    app.register_blueprint(replit_auth)

    print('Authentication routes initialized successfully')

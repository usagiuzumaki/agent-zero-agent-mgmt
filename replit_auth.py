import os
import secrets
import requests
from functools import wraps
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
    def save_user_session(user_id, token=None):
        session_key = UserSessionStorage.get_session_key()
        
        oauth = OAuth.query.filter_by(browser_session_key=session_key).first()
        if oauth:
            oauth.user_id = user_id
            if token:
                oauth.token = token
        else:
            oauth = OAuth(
                user_id=user_id,
                browser_session_key=session_key,
                token=token
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
    return redirect(url_for('replit_auth.login'))


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('replit_auth.login'))
        # Check if user has paid
        if not current_user.has_paid:
            return redirect('/payment/required')
        return f(*args, **kwargs)
    return decorated_function


def require_payment(f):
    """Decorator that requires user to be authenticated AND have paid"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('replit_auth.login'))
        if not current_user.has_paid:
            return redirect('/payment/required')
        return f(*args, **kwargs)
    return decorated_function


def get_replit_oidc_config():
    repl_id = os.getenv('REPL_ID')
    if not repl_id:
        raise ValueError("REPL_ID environment variable is required for Replit Auth")
    
    dev_domain = os.getenv('REPLIT_DEV_DOMAIN', '')
    domains = os.getenv('REPLIT_DOMAINS', '')
    base_domain = dev_domain or domains.split(',')[0] if domains else ''
    
    if not base_domain:
        raise ValueError("REPLIT_DEV_DOMAIN or REPLIT_DOMAINS environment variable is required")
    
    redirect_uri = f"https://{base_domain}/auth/callback"
    
    return {
        'client_id': repl_id,
        'authorization_endpoint': 'https://replit.com/auth/oauth2/authorize',
        'token_endpoint': 'https://replit.com/auth/oauth2/token',
        'userinfo_endpoint': 'https://replit.com/auth/oauth2/userinfo',
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile'
    }


@replit_auth.route('/login')
def login():
    try:
        config = get_replit_oidc_config()
        
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state
        
        auth_url = (
            f"{config['authorization_endpoint']}?"
            f"client_id={config['client_id']}&"
            f"redirect_uri={config['redirect_uri']}&"
            f"response_type=code&"
            f"scope={config['scope']}&"
            f"state={state}"
        )
        
        return redirect(auth_url)
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return f"Login error: {str(e)}", 500


@replit_auth.route('/callback')
def callback():
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        
        if not code or not state:
            return "Missing authorization code or state", 400
        
        if state != session.get('oauth_state'):
            return "Invalid state parameter", 400
        
        config = get_replit_oidc_config()
        
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': config['redirect_uri'],
            'client_id': config['client_id']
        }
        
        token_response = requests.post(config['token_endpoint'], data=token_data)
        token_response.raise_for_status()
        tokens = token_response.json()
        
        access_token = tokens.get('access_token')
        if not access_token:
            return "Failed to obtain access token", 500
        
        userinfo_response = requests.get(
            config['userinfo_endpoint'],
            headers={'Authorization': f'Bearer {access_token}'}
        )
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
        
        user_id = userinfo.get('sub')
        email = userinfo.get('email')
        
        if not user_id or not email:
            return "Failed to obtain user information", 500
        
        user = User.query.get(user_id)
        if not user:
            user = User(
                id=user_id,
                email=email,
                first_name=userinfo.get('given_name', ''),
                last_name=userinfo.get('family_name', ''),
                profile_image_url=userinfo.get('picture', '')
            )
            db.session.add(user)
        else:
            user.email = email
            user.first_name = userinfo.get('given_name', user.first_name)
            user.last_name = userinfo.get('family_name', user.last_name)
            user.profile_image_url = userinfo.get('picture', user.profile_image_url)
        
        db.session.commit()
        
        UserSessionStorage.save_user_session(user_id, access_token)
        login_user(user)
        
        session.pop('oauth_state', None)
        
        # Check if user has paid
        if not user.has_paid:
            return redirect('/payment/required')
        
        return redirect('/')
    
    except Exception as e:
        current_app.logger.error(f"Callback error: {str(e)}")
        return f"Authentication error: {str(e)}", 500


@replit_auth.route('/logout')
@login_required
def logout():
    UserSessionStorage.clear_user_session()
    logout_user()
    return redirect(url_for('login_page'))


@replit_auth.route('/user')
@login_required
def user_info():
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'profile_image_url': current_user.profile_image_url
    })


def init_replit_auth(app):
    session_secret = os.getenv('SESSION_SECRET')
    if not session_secret:
        raise ValueError("SESSION_SECRET environment variable is required")
    
    if not app.secret_key:
        app.secret_key = session_secret
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    login_manager.init_app(app)
    login_manager.login_view = 'replit_auth.login'
    
    app.register_blueprint(replit_auth)
    
    print("Replit Auth initialized successfully")

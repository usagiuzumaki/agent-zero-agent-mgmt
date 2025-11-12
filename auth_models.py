import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    profile_image_url = db.Column(db.String(512))
    password_hash = db.Column(db.String(255), nullable=True)
    
    # Payment and subscription status
    has_paid = db.Column(db.Boolean, default=False, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=True)
    stripe_customer_id = db.Column(db.String(255), unique=True, nullable=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=True)
    stripe_subscription_id = db.Column(db.String(255), nullable=True)
    subscription_status = db.Column(db.String(50), default='trial', nullable=False)  # trial, active, expired
    
    # Trial tracking
    trial_start_time = db.Column(db.DateTime, nullable=True)  # When user first sends a message
    trial_expired = db.Column(db.Boolean, default=False, nullable=False)  # Whether 3-minute trial has expired
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    oauth_tokens = db.relationship('OAuth', backref='user', lazy=True, cascade='all, delete-orphan')
    chats = db.relationship('UserChat', backref='user', lazy=True, cascade='all, delete-orphan')
    screenwriting_data = db.relationship('UserScreenwriting', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password: str):
        if not password:
            raise ValueError("Password must not be empty")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)


class OAuth(db.Model):
    __tablename__ = 'oauth'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, index=True)
    browser_session_key = db.Column(db.String(255), unique=True, nullable=False, index=True)
    provider = db.Column(db.String(50), nullable=False, default='replit')
    token = db.Column(db.Text)
    token_secret = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<OAuth {self.user_id} - {self.provider}>'


class UserChat(db.Model):
    __tablename__ = 'user_chats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, index=True)
    chat_id = db.Column(db.String(255), nullable=False, index=True)
    chat_name = db.Column(db.String(255))
    chat_data = db.Column(db.Text)  # JSON data for chat history
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'chat_id', name='_user_chat_uc'),)
    
    def __repr__(self):
        return f'<UserChat {self.user_id} - {self.chat_id}>'


class UserScreenwriting(db.Model):
    __tablename__ = 'user_screenwriting'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, index=True)
    data_type = db.Column(db.String(50), nullable=False)  # book_outline, story_bible, characters, etc.
    data_name = db.Column(db.String(255))
    data_content = db.Column(db.Text)  # JSON data for screenwriting content
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserScreenwriting {self.user_id} - {self.data_type}>'


def init_db(app):
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("Warning: DATABASE_URL not found, authentication features will be disabled")
        print("Please provision a database using the Replit database pane")
        return False
    
    # Handle both postgres:// and postgresql:// formats for pg8000
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
    elif database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
    
    # Remove sslmode parameter if present as pg8000 handles SSL differently
    if '?sslmode=' in database_url:
        database_url = database_url.split('?')[0]
    elif '&sslmode=' in database_url:
        # Remove sslmode parameter from middle of query string
        import re
        database_url = re.sub(r'[&?]sslmode=[^&]*', '', database_url)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,  # Reduced pool size for Neon
        'max_overflow': 10,  # Reduced overflow
        'pool_timeout': 30,  # Add timeout
        'connect_args': {
            'ssl_context': True
            # pg8000 doesn't accept connect_timeout as a parameter
        }
    }
    
    try:
        db.init_app(app)
        
        # Try to initialize database with retries
        max_retries = 3
        for retry in range(max_retries):
            try:
                with app.app_context():
                    # Try a simple query first to wake up the database
                    from sqlalchemy import text
                    db.session.execute(text("SELECT 1"))
                    db.session.commit()
                    
                    # Create tables if they don't exist
                    db.create_all()

                    # Ensure existing deployments receive new columns
                    _apply_user_schema_updates()
                    print("Database tables created successfully")
                    return True
            except Exception as e:
                if "endpoint has been disabled" in str(e).lower():
                    print(f"Database endpoint is disabled. Retry {retry + 1}/{max_retries}...")
                    if retry < max_retries - 1:
                        import time
                        time.sleep(2)  # Wait before retry
                        continue
                    else:
                        print("IMPORTANT: The Neon database endpoint is disabled.")
                        print("Please enable it through the Replit database pane:")
                        print("1. Go to the Database pane in Replit")
                        print("2. Click on your PostgreSQL database")
                        print("3. The database will automatically wake up")
                        print("4. Restart this application")
                        print("Authentication features will work once the database is enabled.")
                        return False
                else:
                    raise e
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Authentication features will be temporarily disabled")
        return False


def _apply_user_schema_updates():
    """Perform lightweight migrations required for the auth system."""
    from sqlalchemy import inspect, text

    try:
        inspector = inspect(db.engine)
        columns = {column["name"] for column in inspector.get_columns('users')}

        statements = []
        if 'password_hash' not in columns:
            statements.append(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
        if 'stripe_subscription_id' not in columns:
            statements.append(text("ALTER TABLE users ADD COLUMN stripe_subscription_id VARCHAR(255)"))

        for statement in statements:
            db.session.execute(statement)

        if statements:
            db.session.commit()
    except Exception as exc:
        db.session.rollback()
        print(f"Warning: Failed to apply user schema updates: {exc}")

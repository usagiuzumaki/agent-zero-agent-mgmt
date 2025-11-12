import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    profile_image_url = db.Column(db.String(512))
    
    # Payment and subscription status
    has_paid = db.Column(db.Boolean, default=False, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=True)
    stripe_customer_id = db.Column(db.String(255), unique=True, nullable=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=True)
    subscription_status = db.Column(db.String(50), default='trial', nullable=False)  # trial, active, expired
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    oauth_tokens = db.relationship('OAuth', backref='user', lazy=True, cascade='all, delete-orphan')
    chats = db.relationship('UserChat', backref='user', lazy=True, cascade='all, delete-orphan')
    screenwriting_data = db.relationship('UserScreenwriting', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'


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
        return False
    
    # Handle both postgres:// and postgresql:// formats for pg8000
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+pg8000://', 1)
    elif database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+pg8000://', 1)
    
    # Remove sslmode parameter if present as pg8000 handles SSL differently
    if 'sslmode=' in database_url:
        database_url = database_url.split('?')[0]
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'ssl_context': True
        }
    }
    
    try:
        db.init_app(app)
        
        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            print("Database tables created successfully")
            # Test connection
            db.engine.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")
        print("Authentication features will be temporarily disabled")
        print("The database may be sleeping - it will auto-wake on the next request")
        return False

from datetime import datetime
from auth_models import db

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chapters = db.relationship('Chapter', backref='project', lazy=True, cascade='all, delete-orphan')
    moodboard_items = db.relationship('MoodboardItem', backref='project', lazy=True)
    growth_events = db.relationship('GrowthEvent', backref='project', lazy=True)

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text)
    poetic_epilogue = db.Column(db.Text)
    chapter_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    pages = db.relationship('Page', backref='chapter', lazy=True, cascade='all, delete-orphan')
    images = db.relationship('Image', backref='chapter', lazy=True)

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False, index=True)
    title = db.Column(db.String(255))
    page_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    blocks = db.relationship('Block', backref='page', lazy=True, cascade='all, delete-orphan')

class Block(db.Model):
    __tablename__ = 'blocks'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False, index=True)
    block_type = db.Column(db.String(50), nullable=False) # page, margin-note, aria-annotation, highlighted-passage, illustrated-spread, emotional-bookmark
    content = db.Column(db.Text) # JSON string for rich text or other data
    block_order = db.Column(db.Integer, default=0)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    annotations = db.relationship('AriaAnnotation', backref='block', lazy=True, cascade='all, delete-orphan')

class AriaAnnotation(db.Model):
    __tablename__ = 'aria_annotations'
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('blocks.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    annotation_type = db.Column(db.String(50)) # margin-note, inline
    anchor_data = db.Column(db.Text) # JSON string for positioning
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, index=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), index=True)
    url = db.Column(db.String(512), nullable=False)
    filename = db.Column(db.String(255))
    tone_tags = db.Column(db.String(255))
    theme_labels = db.Column(db.String(255))
    detected_meaning = db.Column(db.Text)
    reflective_caption = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MoodboardItem(db.Model):
    __tablename__ = 'moodboard_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), index=True)
    item_type = db.Column(db.String(50), nullable=False) # sticker, symbol, image, swatch, text
    content = db.Column(db.Text) # URL, text, or color code
    x = db.Column(db.Float, default=0)
    y = db.Column(db.Float, default=0)
    z_index = db.Column(db.Integer, default=0)
    scale = db.Column(db.Float, default=1)
    rotation = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class GrowthEvent(db.Model):
    __tablename__ = 'growth_events'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    event_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    milestone_marker = db.Column(db.String(255))
    event_metadata = db.Column(db.Text) # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

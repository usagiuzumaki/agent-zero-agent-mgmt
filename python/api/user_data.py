"""
User-specific data management API
Handles personalized chat histories and screenwriting data for each user
"""

import json
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from python.api.auth.auth_models import db, UserChat, UserScreenwriting

user_data_api = Blueprint('user_data_api', __name__)


@user_data_api.route('/api/user/chats', methods=['GET'])
@login_required
def get_user_chats():
    """Get all chats for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    chats = UserChat.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': chat.chat_id,
        'name': chat.chat_name,
        'created_at': chat.created_at.isoformat(),
        'updated_at': chat.updated_at.isoformat()
    } for chat in chats])


@user_data_api.route('/api/user/chat/<chat_id>', methods=['GET'])
@login_required
def get_user_chat(chat_id):
    """Get a specific chat for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    chat = UserChat.query.filter_by(
        user_id=current_user.id,
        chat_id=chat_id
    ).first()
    
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    return jsonify({
        'id': chat.chat_id,
        'name': chat.chat_name,
        'data': json.loads(chat.chat_data) if chat.chat_data else [],
        'created_at': chat.created_at.isoformat(),
        'updated_at': chat.updated_at.isoformat()
    })


@user_data_api.route('/api/user/chat', methods=['POST'])
@login_required
def create_user_chat():
    """Create a new chat for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    data = request.get_json()
    chat_id = data.get('chat_id', str(uuid.uuid4()))
    chat_name = data.get('name', f'Chat {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    chat_data = data.get('data', [])
    
    # Check if chat already exists
    existing_chat = UserChat.query.filter_by(
        user_id=current_user.id,
        chat_id=chat_id
    ).first()
    
    if existing_chat:
        # Update existing chat
        existing_chat.chat_name = chat_name
        existing_chat.chat_data = json.dumps(chat_data)
        existing_chat.updated_at = datetime.utcnow()
    else:
        # Create new chat
        new_chat = UserChat(
            user_id=current_user.id,
            chat_id=chat_id,
            chat_name=chat_name,
            chat_data=json.dumps(chat_data)
        )
        db.session.add(new_chat)
    
    db.session.commit()
    
    return jsonify({
        'id': chat_id,
        'name': chat_name,
        'success': True
    })


@user_data_api.route('/api/user/chat/<chat_id>', methods=['PUT'])
@login_required
def update_user_chat(chat_id):
    """Update a chat for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    chat = UserChat.query.filter_by(
        user_id=current_user.id,
        chat_id=chat_id
    ).first()
    
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        chat.chat_name = data['name']
    if 'data' in data:
        chat.chat_data = json.dumps(data['data'])
    
    chat.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True})


@user_data_api.route('/api/user/chat/<chat_id>', methods=['DELETE'])
@login_required
def delete_user_chat(chat_id):
    """Delete a chat for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    chat = UserChat.query.filter_by(
        user_id=current_user.id,
        chat_id=chat_id
    ).first()
    
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404
    
    db.session.delete(chat)
    db.session.commit()
    
    return jsonify({'success': True})


# Screenwriting data endpoints
@user_data_api.route('/api/user/screenwriting/<data_type>', methods=['GET'])
@login_required
def get_screenwriting_data(data_type):
    """Get screenwriting data of a specific type for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    data = UserScreenwriting.query.filter_by(
        user_id=current_user.id,
        data_type=data_type
    ).all()
    
    return jsonify([{
        'id': item.id,
        'name': item.data_name,
        'content': json.loads(item.data_content) if item.data_content else {},
        'created_at': item.created_at.isoformat(),
        'updated_at': item.updated_at.isoformat()
    } for item in data])


@user_data_api.route('/api/user/screenwriting', methods=['POST'])
@login_required
def save_screenwriting_data():
    """Save screenwriting data for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    data = request.get_json()
    data_type = data.get('type')
    data_name = data.get('name', '')
    content = data.get('content', {})
    
    if not data_type:
        return jsonify({'error': 'Data type is required'}), 400
    
    # Check if data already exists
    existing = UserScreenwriting.query.filter_by(
        user_id=current_user.id,
        data_type=data_type,
        data_name=data_name
    ).first()
    
    if existing:
        # Update existing data
        existing.data_content = json.dumps(content)
        existing.updated_at = datetime.utcnow()
    else:
        # Create new data
        new_data = UserScreenwriting(
            user_id=current_user.id,
            data_type=data_type,
            data_name=data_name,
            data_content=json.dumps(content)
        )
        db.session.add(new_data)
    
    db.session.commit()
    
    return jsonify({'success': True})


@user_data_api.route('/api/user/screenwriting/<int:data_id>', methods=['DELETE'])
@login_required
def delete_screenwriting_data(data_id):
    """Delete screenwriting data for the current user"""
    if not current_user.has_paid:
        return jsonify({'error': 'Payment required'}), 402
    
    data = UserScreenwriting.query.filter_by(
        user_id=current_user.id,
        id=data_id
    ).first()
    
    if not data:
        return jsonify({'error': 'Data not found'}), 404
    
    db.session.delete(data)
    db.session.commit()
    
    return jsonify({'success': True})


def init_user_data_api(app):
    """Initialize user data API with Flask app"""
    app.register_blueprint(user_data_api)
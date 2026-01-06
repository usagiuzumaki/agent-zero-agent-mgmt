"""
API endpoints for screenwriting tools
Handles persistence and retrieval of screenwriting data
"""
from flask import Blueprint, request, jsonify
from python.helpers.screenwriting_manager import ScreenwritingManager
import json

# Create Flask blueprint for screenwriting API
screenwriting_bp = Blueprint('screenwriting', __name__)

# Initialize the screenwriting manager
manager = ScreenwritingManager()


@screenwriting_bp.route('/api/screenwriting/<data_type>', methods=['GET'])
def get_screenwriting_data(data_type):
    """Get screenwriting data by type"""
    try:
        data = manager.load_data(data_type)
        if data:
            return jsonify(data), 200
        return jsonify({'error': 'Invalid data type'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/<data_type>', methods=['POST'])
def save_screenwriting_data(data_type):
    """Save screenwriting data by type"""
    try:
        data = request.get_json()
        if manager.save_data(data_type, data):
            return jsonify({'message': f'{data_type} saved successfully'}), 200
        return jsonify({'error': 'Failed to save data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/character/add', methods=['POST'])
def add_character():
    """Add a new character profile"""
    try:
        character_data = request.get_json()
        if manager.add_character(character_data):
            return jsonify({'message': 'Character added successfully'}), 200
        return jsonify({'error': 'Failed to add character'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/character/update', methods=['POST'])
def update_character():
    """Update a character profile"""
    try:
        character_data = request.get_json()
        char_id = character_data.get('id')
        if not char_id:
            return jsonify({'error': 'Character ID required'}), 400

        if manager.update_character(char_id, character_data):
            return jsonify({'message': 'Character updated successfully'}), 200
        return jsonify({'error': 'Failed to update character'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/character/delete', methods=['DELETE'])
def delete_character():
    """Delete a character profile"""
    try:
        data = request.get_json()
        char_id = data.get('id')
        if not char_id:
            return jsonify({'error': 'Character ID required'}), 400

        if manager.delete_character(char_id):
            return jsonify({'message': 'Character deleted successfully'}), 200
        return jsonify({'error': 'Failed to delete character'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/quote/add', methods=['POST'])
def add_quote():
    """Add a memorable quote"""
    try:
        data = request.get_json()
        quote = data.get('quote')
        character = data.get('character')
        context = data.get('context')
        category = data.get('category')

        if manager.add_quote(quote, character, context, category):
            return jsonify({'message': 'Quote added successfully'}), 200
        return jsonify({'error': 'Failed to add quote'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/scene/add', methods=['POST'])
def add_scene():
    """Add a new scene"""
    try:
        scene_data = request.get_json()
        if manager.add_scene(scene_data):
            return jsonify({'message': 'Scene added successfully'}), 200
        return jsonify({'error': 'Failed to add scene'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/sketch/add', methods=['POST'])
def add_sketch():
    """Add a sketch or visual element"""
    try:
        sketch_data = request.get_json()
        if manager.add_sketch(sketch_data):
            return jsonify({'message': 'Sketch added successfully'}), 200
        return jsonify({'error': 'Failed to add sketch'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/project/create', methods=['POST'])
def create_project():
    """Create a new screenwriting project"""
    try:
        data = request.get_json()
        project_name = data.get('name')
        genre = data.get('genre')
        logline = data.get('logline')

        if manager.create_project(project_name, genre, logline):
            return jsonify({'message': 'Project created successfully'}), 200
        return jsonify({'error': 'Failed to create project'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/all', methods=['GET'])
def get_all_data():
    """Get all screenwriting data"""
    try:
        all_data = manager.get_all_data()
        return jsonify(all_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/quotes/search', methods=['POST'])
def search_quotes():
    """Search for quotes"""
    try:
        data = request.get_json()
        search_term = data.get('search', '')
        results = manager.search_quotes(search_term)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/character/find', methods=['POST'])
def find_character():
    """Find a character by name"""
    try:
        data = request.get_json()
        name = data.get('name')
        character = manager.get_character_by_name(name)
        if character:
            return jsonify(character), 200
        return jsonify({'error': 'Character not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/outline/update', methods=['POST'])
def update_outline():
    """Update book outline"""
    try:
        outline_data = request.get_json()
        if manager.update_outline(outline_data):
            return jsonify({'message': 'Outline updated successfully'}), 200
        return jsonify({'error': 'Failed to update outline'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@screenwriting_bp.route('/api/screenwriting/storybook/upload', methods=['POST'])
def upload_storybook():
    """Convert an uploaded document into a clickable storybook."""
    try:
        payload = request.get_json(force=True)
        name = payload.get('name', 'Untitled Document')
        content = payload.get('content', '')
        description = payload.get('description')
        tags = payload.get('tags', [])

        document = manager.ingest_story_document(name, content, description, tags)

        if document:
            return jsonify(document), 200

        return jsonify({'error': 'Failed to ingest document'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

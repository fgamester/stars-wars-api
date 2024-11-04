from flask import Blueprint, request, jsonify
from models import Character, favorite_characters, db, User

bp_character = Blueprint('character', __name__)

@bp_character.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    serialized_characters = [character.serialize() for character in characters]
    
    return jsonify({'status': 'success', 'characters': serialized_characters}), 200


@bp_character.route('/character/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    
    if not character:
        return jsonify({'status': 'error', 'message': 'Character not found'}), 404
    
    return jsonify({'status': 'success', 'character': character.serialize()}), 200


@bp_character.route('/character', methods=['POST'])
def add_character():
    name = request.json.get('name')
    description = request.json.get('description')

    if not name:
        return jsonify({'status': 'error', 'message': 'Name is required'}), 400
    
    if not description:
        return jsonify({'status': 'error', 'message': 'Description is required'}), 400
    
    character = Character(name=name, description=description)

    character.save()

    return jsonify({'status': 'success', 'message': 'Character added successfully', 'character': character.serialize()}), 201


@bp_character.route('/character/<int:id>', methods=['DELETE'])
def remove_character(id):
    character = Character.query.get(id)
    favorites = db.session.query(favorite_characters).filter_by(character_id=id).all()

    print(favorites)

    for favorite in favorites:
        user = User.query.get(favorite.user_id)
        character = Character.query.get(favorite.character_id)
        user.favorites_characters.remove(character)
        user.update()

    if not character:
        return jsonify({'status': 'error', 'message': 'Character not found'}), 404

    character.delete()

    return jsonify({'status': 'success', 'message': 'Character removed successfully'}), 200

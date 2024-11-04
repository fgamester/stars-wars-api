from flask import Blueprint, request, jsonify
from models import User, favorite_characters, favorite_planets, db, Character, Planet

bp_favorite = Blueprint('favorite', __name__)


@bp_favorite.route('/character/favorite', methods=['POST'])
def add_favorite():
    user_id = request.json.get('user_id')
    character_id = request.json.get('character_id')

    if not user_id:
        return jsonify({'status': 'error', 'message': 'User id is required'}), 400

    if not character_id:
        return jsonify({'status': 'error', 'message': 'Character id is required'}), 400
    
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    if not character:
        return jsonify({'status': 'error', 'message': 'Character not found'}), 404
    
    favorite = db.session.query(favorite_characters).filter_by(user_id=user_id, character_id=character_id).first()

    if favorite:
        return jsonify({'status': 'error', 'message': 'Favorite already exists'}), 400

    character = Character.query.get(character_id)
    user.favorites_characters.append(character)
    user.update()
    
    return jsonify({'status': 'success', 'message': 'Favorite added successfully'}), 201


@bp_favorite.route('/character/favorite', methods=['DELETE'])
def remove_favorite():
    user_id = request.json.get('user_id')
    character_id = request.json.get('character_id')

    if not user_id:
        return jsonify({'status': 'error', 'message': 'User id is required'}), 400
    
    if not character_id:
        return jsonify({'status': 'error', 'message': 'Character id is required'}), 400
    
    user = User.query.get(user_id)
    favorite = db.session.query(favorite_characters).filter_by(user_id=user_id, character_id=character_id).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    if not favorite:
        return jsonify({'status': 'error', 'message': 'Favorite not found'}), 404

    character = Character.query.get(character_id)
    user.favorites_characters.remove(character)
    user.update()

    return jsonify({'status': 'success', 'message': 'Favorite removed successfully'}), 200


@bp_favorite.route('/planet/favorite', methods=['POST'])
def add_favorite_planet():
    user_id = request.json.get('user_id')
    planet_id = request.json.get('planet_id')

    if not user_id:
        return jsonify({'status': 'error', 'message': 'User id is required'}), 400

    if not planet_id:
        return jsonify({'status': 'error', 'message': 'Planet id is required'}), 400

    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    if not planet:
        return jsonify({'status': 'error', 'message': 'Planet not found'}), 404
    
    favorite = db.session.query(favorite_planets).filter_by(user_id=user_id, planet_id=planet_id).first()

    if favorite:
        return jsonify({'status': 'error', 'message': 'Favorite already exists'}), 400
    
    planet = Planet.query.get(planet_id)
    user.favorites_planets.append(planet)
    user.update()
    
    return jsonify({'status': 'success', 'message': 'Favorite added successfully'}), 201


@bp_favorite.route('/planet/favorite', methods=['DELETE'])
def remove_favorite_planet():
    user_id = request.json.get('user_id')
    planet_id = request.json.get('planet_id')

    if not user_id:
        return jsonify({'status': 'error', 'message': 'User id is required'}), 400
    
    if not planet_id:
        return jsonify({'status': 'error', 'message': 'Planet id is required'}), 400
    
    user = User.query.get(user_id)
    favorite = db.session.query(favorite_planets).filter_by(user_id=user_id, planet_id=planet_id).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    if not favorite:
        return jsonify({'status': 'error', 'message': 'Favorite not found'}), 404
    
    planet = Planet.query.get(planet_id)
    user.favorites_planets.remove(planet)
    user.update()
    
    return jsonify({'status': 'success', 'message': 'Favorite removed successfully'}), 200


@bp_favorite.route('/user/favorite/<int:id>', methods=['GET'])
def get_user_favorites(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    characters = db.session.query(favorite_characters).filter_by(user_id=id)
    planets = db.session.query(favorite_planets).filter_by(user_id=id)

    serialized_characters = []
    serialized_planets = []

    for favorite in characters:
        character = Character.query.get(favorite.character_id)
        serialized_characters.append(character.serialize())

    for favorite in planets:
        planet = Planet.query.get(favorite.planet_id)
        serialized_planets.append(planet.serialize())
    
    return jsonify({'status': 'success', 'favorites': {'characters': serialized_characters, 'planets': serialized_planets}}), 200
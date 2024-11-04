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
    
    result = db.session.execute(favorite_characters.select().where(
        favorite_characters.c.user_id == user_id,
        favorite_characters.c.character_id == character_id
    )).first()

    if result:
        return jsonify({'status': 'error', 'message': 'Favorite already exists'}), 400

    new_favorite = favorite_characters.insert().values(user_id=user_id, character_id=character_id)
    db.session.execute(new_favorite)
    db.session.commit()
    
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
    get_data = favorite_characters.select().where(
        favorite_characters.c.user_id == user_id,
        favorite_characters.c.character_id == character_id
    )
    result = db.session.execute(get_data).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    if not result:
        return jsonify({'status': 'error', 'message': 'Favorite not found'}), 404
    
    del_fav = favorite_characters.delete().where(
        favorite_characters.c.user_id == user_id,
        favorite_characters.c.character_id == character_id
    )
    db.session.execute(del_fav)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Favorite removed successfully'}), 200


@bp_favorite.route('/planet/favorite', methods=['GET'])
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
    
    get_data = favorite_planets.select().where(
        favorite_planets.c.user_id == user_id,
        favorite_planets.c.planet_id == planet_id
    )
    result = db.session.execute(get_data).first()

    if result:
        return jsonify({'status': 'error', 'message': 'Favorite already exists'}), 400
    
    new_favorite = favorite_planets.insert().values(user_id=user_id, planet_id=planet_id)
    db.session.execute(new_favorite)
    db.session.commit()
    
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
    get_data = favorite_planets.select().where(
        favorite_planets.c.user_id == user_id,
        favorite_planets.c.planet_id == planet_id
    )
    result = db.session.execute(get_data).first()
    print(result)

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    if not result:
        return jsonify({'status': 'error', 'message': 'Favorite not found'}), 404
    
    del_fav = favorite_planets.delete().where(
        favorite_planets.c.user_id == user_id,
        favorite_planets.c.planet_id == planet_id
    )
    db.session.execute(del_fav)
    db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Favorite removed successfully'}), 200

@bp_favorite.route('/user/favorite/<int:id>', methods=['GET'])
def get_user_favorites(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    favorites_characters = db.session.execute(favorite_characters.select().where(favorite_characters.c.user_id == id))
    favorites_planets = db.session.execute(favorite_planets.select().where(favorite_planets.c.user_id == id))

    serialized_characters = []
    serialized_planets = []

    for favorite in favorites_characters:
        character = Character.query.get(favorite.character_id)
        serialized_characters.append(character.serialize())

    for favorite in favorites_planets:
        planet = Planet.query.get(favorite.planet_id)
        serialized_planets.append(planet.serialize())
    
    return jsonify({'status': 'success', 'favorites': {'characters': serialized_characters, 'planets': serialized_planets}}), 200
from flask import Blueprint, request, jsonify
from models import User, favorite_characters, favorite_planets, db

bp_user = Blueprint('user', __name__)

@bp_user.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    
    return jsonify({'status': 'success', 'users': serialized_users}), 200


@bp_user.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    return jsonify({'status': 'success', 'user': user.serialize()}), 200


@bp_user.route('/user', methods=['POST'])
def add_user():
    print('request received')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not username:
        return jsonify({'status': 'error', 'message': 'Username is required'}), 400
    
    if not email:
        return jsonify({'status': 'error', 'message': 'Email is required'}), 400
    
    if not password:
        return jsonify({'status': 'error', 'message': 'Password is required'}), 400
    
    user = User(username=username, email=email, password=password)
    user.save()

    return jsonify({'status': 'success', 'message': 'User added successfully', 'user': user.serialize()}), 201


@bp_user.route('/user/favorite', methods=['POST'])
def add_favorite():
    user_id = request.json.get('user_id')
    planet_id = request.json.get('planet_id')
    character_id = request.json.get('character_id')

    user = User.query.get(user_id)

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    if planet_id:
        new_favorite = favorite_planets.insert().values(user_id=user_id, planet_id=planet_id)
        db.session.execute(new_favorite)
        db.session.commit()

    if character_id:
        new_favorite = favorite_characters.insert().values(user_id=user_id, character_id=character_id)
        db.session.execute(new_favorite)
        db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Favorite added successfully'}), 201

@bp_user.route('/user/favorite', methods=['DELETE'])
def remove_favorite():
    user_id = request.json.get('user_id')
    planet_id = request.json.get('planet_id')
    character_id = request.json.get('character_id')

    user = User.query.get(user_id)


    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404
    
    if not planet_id and not character_id:
        return jsonify({'status': 'error', 'message': 'Planet or character id is required'}), 400
    
    """ planet = favorite_planets.select().where(
        favorite_planets.c.user_id == user_id,
        favorite_planets.c.planet_id == planet_id
        if not planet:
            return jsonify({'status': 'error', 'message': 'Favorite not found'}), 404
    )
     """
    if planet_id:
        del_fav = favorite_planets.delete().where(
            favorite_planets.c.user_id == user_id,
            favorite_planets.c.planet_id == planet_id
        )
        db.session.execute(del_fav)
        db.session.commit()

    if character_id:
        del_fav = favorite_characters.delete().where(
            favorite_characters.c.user_id == user_id,
            favorite_characters.c.character_id == character_id
        )
        db.session.execute(del_fav)
        db.session.commit()
    
    return jsonify({'status': 'success', 'message': 'Favorite removed successfully'}), 200
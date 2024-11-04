from flask import Blueprint, request, jsonify
from models import Planet, favorite_planets, db, User

bp_planet = Blueprint('planet', __name__)

@bp_planet.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    
    return jsonify({'status': 'success', 'planets': serialized_planets}), 200


@bp_planet.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    
    if not planet:
        return jsonify({'status': 'error', 'message': 'Planet not found'}), 404
    
    return jsonify({'status': 'success', 'planet': planet.serialize()}), 200


@bp_planet.route('/planet', methods=['POST'])
def add_planet():
    name = request.json.get('name')
    description = request.json.get('description')

    if not name:
        return jsonify({'status': 'error', 'message': 'Name is required'}), 400
    
    if not description:
        return jsonify({'status': 'error', 'message': 'Description is required'}), 400
    
    planet = Planet(name=name, description=description)

    planet.save()

    return jsonify({'status': 'success', 'message': 'Planet added successfully', 'planet': planet.serialize()}), 201

@bp_planet.route('/planet/<int:id>', methods=['DELETE'])
def remove_planet(id):
    planet = Planet.query.get(id)

    if not planet:
        return jsonify({'status': 'error', 'message': 'Planet not found'}), 404

    favorites = db.session.query(favorite_planets).filter_by(planet_id=id).all()

    for favorite in favorites:
        user = User.query.get(favorite.user_id)
        planet = Planet.query.get(favorite.planet_id)
        user.favorites_planets.remove(planet)
        user.update()

    planet.delete()

    return jsonify({'status': 'success', 'message': 'Planet removed successfully'}), 200
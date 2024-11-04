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

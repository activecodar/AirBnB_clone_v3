#!/usr/bin/python3
"""users creates a view for user objects
"""
from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import users_views


@users_views.route('/users',
                   methods=['GET'],
                   strict_slashes=False)
def all_users():
    """retrieves a list of all user objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@users_views.route('/users/<user_id>',
                   methods=['GET'],
                   strict_slashes=False)
def get_user(user_id):
    """retrieves user with id user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@users_views.route('/users/<user_id>',
                   methods=['GET'],
                   strict_slashes=False)
def delete(user_id):
    """deletes a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@users_views.route('/users',
                   methods=['POST'],
                   strict_slashes=False)
def create():
    """creates a new user"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    if "email" not in data.keys():
        return {"error": "Missing email"}, 400
    if "password" not in data.keys():
        return {"error": "Missing password"}
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@users_views.route('/users/<user_id>',
                   methods=['PUT'],
                   strict_slashes=True)
def update(user_id):
    """updates a user object"""
    user = storage.get(User, user_id)
    data = request.get_json(force=True, silent=True)
    new_dict = {}
    if user is None:
        abort(404)
    if not data:
        return {"error": "Not a JSON"}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            new_dict[key] = value
    user.__dict__.update(new_dict)
    storage.save()
    return jsonify(user.to_dict()), 200

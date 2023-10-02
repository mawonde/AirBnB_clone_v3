#!/usr/bin/python3
"""
    This is the users page handler for Flask.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """
    Flask route at /users for GET and POST requests.
    """
    if request.method == 'POST':
        request_data = request.get_json()
        if not request_data:
            return {"error": "Not a JSON"}, 400
        if "email" not in request_data:
            return {"error": "Missing email"}, 400
        if "password" not in request_data:
            return {"error": "Missing password"}, 400

        new_user = User(**request_data)
        new_user.save()
        return new_user.to_dict(), 201

    elif request.method == 'GET':
        users_list = [user.to_dict() for user in storage.all("User").values()]
        return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users_id(user_id):
    """
    Flask route at /users/<user_id> for GET, DELETE, and PUT requests.
    """
    user = storage.get(User, user_id)
    if user:
        if request.method == 'DELETE':
            user.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            request_data = request.get_json()
            if not request_data:
                return {"error": "Not a JSON"}, 400
            for key, value in request_data.items():
                if key not in ["id", "email", "created_at", "updated_at"]:
                    setattr(user, key, value)
            user.save()
        return user.to_dict()
    abort(404)


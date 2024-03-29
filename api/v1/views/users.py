#!/usr/bin/python3
"""
Task 10
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users/", methods=["GET"],
                 strict_slashes=False)
def users_get():
    """
    Retrieves list of all User objects.
    """
    all_users = storage.all(User)
    user_list = []
    for user in all_users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def user_id_get(user_id):
    """
    Retrieves an user with a given id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def user_id_delete(user_id):
    """
    Deletes an User object with a given id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users/", methods=["POST"],
                 strict_slashes=False)
def user_post():
    """
    Creates an User via POST
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"],
                 strict_slashes=False)
def user_put(user_id):
    """
    Updates an User object via PUT
    """
    user = storage.get(User, user_id)
    user_data = request.get_json()
    if user is None:
        abort(404)
    if user_data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

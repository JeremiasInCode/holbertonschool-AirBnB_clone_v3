#!/usr/bin/python3
""" states.py """
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify, abort, request



@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@app_views.route('/states')
def specific_state(state_id):
    """ Retrieve a specific state """
    if storage.get(State, state_id) is None:
        abort(404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Delete a specific state_id """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def add_state():
    """ Add a state """
    data = request.get_json()

    if data is None:
        abort(400, description='Not data')

    if 'name' not in data:
        abort(400, description='Missing name')

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update an state by given id"""
    data = request.get_json()

    if data is None:
        abort(400, description='Not data')

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            # updated attributes
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200

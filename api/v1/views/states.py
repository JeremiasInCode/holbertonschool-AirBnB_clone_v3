#!/usr/bin/python3
""" states.py - Module for handling state-related API endpoints """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states', defaults={'state_id': None}, methods=['GET'])
def get_states(state_id):
    """Retrieve details of a specific state or a list of all states.

    Args:
        state_id (str): The ID of the state to retrieve details for.
            If set to None, returns a list of all states.

    Returns:
        JSON: A JSON representation of the state details or a list of states.

    Raises:
        404: If the specified state is not found.
    """
    if state_id is not None:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    else:
        states = storage.all(State).values()
        return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a specific state by ID.

    Args:
        state_id (str): The ID of the state to delete.

    Returns:
        JSON: An empty JSON response.

    Raises:
        404: If the specified state is not found.
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Create a new state.

    Returns:
        JSON: A JSON representation of the newly created state.

    Raises:
        400: If the request does not contain valid JSON data
        or if 'name' is missing.
    """
    data = request.get_json()
    if data is None:
        abort(400, description='No JSON data provided')
    if 'name' not in data:
        abort(400, description='Missing required field: name')

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a state by ID.

    Args:
        state_id (str): The ID of the state to update.

    Returns:
        JSON: A JSON representation of the updated state.

    Raises:
        400: If the request does not contain valid JSON data.
        404: If the specified state is not found.
    """
    data = request.get_json()
    if data is None:
        abort(400, description='No JSON data provided')

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200

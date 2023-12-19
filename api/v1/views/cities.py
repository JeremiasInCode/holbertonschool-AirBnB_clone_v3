#!/usr/bin/python3
""" cities.py - Module for handling city-related API endpoints """
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_city_state(state_id):
    """Retrieve all cities of a specific state.

    Args:
        state_id (str): The ID of the state to retrieve cities for.

    Returns:
        JSON: A JSON representation of all cities in the specified state.

    Raises:
        404: If the specified state is not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve details of a specific city.

    Args:
        city_id (str): The ID of the city to retrieve details for.

    Returns:
        JSON: A JSON representation of the city details.

    Raises:
        404: If the specified city is not found.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a specific city by ID.

    Args:
        city_id (str): The ID of the city to delete.

    Returns:
        JSON: An empty JSON response.

    Raises:
        404: If the specified city is not found.
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """Create a new city in the specified state.

    Args:
        state_id (str): The ID of the state to add the city to.

    Returns:
        JSON: A JSON representation of the newly created city.

    Raises:
        404: If the specified state is not found.
        400: If the request does not contain valid JSON data or if 'name' is missing.
    """
    if storage.get(State, state_id) is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description='No JSON data provided')

    if "name" not in data:
        abort(400, description='Missing required field: name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """Update a city by ID.

    Args:
        city_id (str): The ID of the city to update.

    Returns:
        JSON: A JSON representation of the updated city.

    Raises:
        404: If the specified city is not found.
        400: If the request does not contain valid JSON data.
    """
    data = request.get_json()

    if data is None:
        abort(400, description='No JSON data provided')

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200

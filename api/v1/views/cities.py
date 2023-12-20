#!/usr/bin/python3
""" cities.py - Module for handling city-related API endpoints """
from flask import Flask, request, jsonify, abort, make_response
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City

app = Flask(__name__)


@app_views.route("states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
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
        return abort(404)
    list_cities = []
    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


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
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_cities_id(city_id):
    """Delete a specific city by ID.
        Args:
            city_id (str): The ID of the city to delete.

        Returns:
            JSON: An empty JSON response.

        Raises:
            404: If the specified city is not found.
    """
    to_delete = storage.get(City, city_id)
    if to_delete is None:
        return abort(404)
    storage.delete(to_delete)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """POST API route, creates a new city.
        Args:
            state_id (str): The ID of the state to add the city to.

        Returns:
            JSON: A JSON representation of the newly created city.

        Raises:
            404: If the specified state is not found.
            400: If the request does not contain valid JSON data or if
            'name' is missing.
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    data['state_id'] = state.id
    new_city = City(**data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
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
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)

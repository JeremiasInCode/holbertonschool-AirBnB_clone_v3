#!/usr/bin/python3
"""
Task 9
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", methods=["GET"],
                 strict_slashes=False)
def amenities_get():
    """
    Retrieves the list of all Amenity objects.
    """
    all_amenities = storage.all(Amenity)
    amenity_list = []
    for amenity in all_amenities.values():
        amenity_list.append(amenity.to_dict())
    return make_response(jsonify(amenity_list), 200)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity_id_get(amenity_id):
    """
    Retrieves an amenity with a given id
    Raise 404 error if id not linked to any Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_id_delete(amenity_id):
    """
    Deletes an Amenity object with a given id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities/", methods=["POST"],
                 strict_slashes=False)
def amenity_post():
    """
    Creates an Amenity via POST
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_put(id):
    """
    Updates an Amenity object via PUT
    """
    print("i am here")
    req_dict = request.get_json(silent=True)
    if req_dict is not None:
        amenity = storage.get(Amenity, id)
        if amenity is None:
            abort(404)
        ignore_keys = ["id", "created_at", "updated_at"]
        for key, value in req_dict.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)

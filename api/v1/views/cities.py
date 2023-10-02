#!/usr/bin/python3
""" CRUD City objects that handles default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.City import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def cities(state_id):
    """Retrieves  list of all City objects"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_id(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities", methods=["POST"], strict_slashes=False)
def create_city():
    """Creates a City"""
    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")
    city = City(**new_city)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

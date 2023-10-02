#!/usr/bin/python3
""" CRUD State objects that handles default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """Retrieves  list of all State objects"""
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_id(state_id):
    """Retrieves a State object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

route = "/states/<state_id>"
@app_views.route(route, methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State"""
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(state, k, v)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)

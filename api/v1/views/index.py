#!/usr/bin/python3
"""Index File"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """Retrieves  the number of each instance by type"""
    return jsonify(
        amenities=storage.count("Amenity"),
        cities=storage.count("City"),
        places=storage.count("Place"),
        reviews=storage.count("Review"),
        states=storage.count("State"),
        users=storage.count("User"),
    )

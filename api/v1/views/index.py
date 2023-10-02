#!/usr/bin/python3
"""Index File"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/api/v1/stats", methods=["GET"])
def get_stats():

    amenity_count = storage.count("Amenity")
    city_count = storage.count("City")
    place_count = storage.count("Place")
    review_count = storage.count("Review")
    state_count = storage.count("State")
    user_count = storage.count("User")

    counts = {
        "amenities": amenity_count,
        "cities": city_count,
        "places": place_count,
        "reviews": review_count,
        "states": state_count,
        "users": user_count,
    }

    return jsonify(counts), 200

#!/usr/bin/python3
"""
    This is the places reviews page handler for Flask.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id):
    """
    Retrieve a list of all Review objects of a Place or create a new Review.
    """
    # Retrieve the Place object based on place_id
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)  # Raise a 404 error if the place doesn't exist

    if request.method == 'POST':
        # Create a new Review object associated with the place
        data = request.get_json()
        if not data:
            return {"error": "Not a JSON"}, 400
        user_id = data.get("user_id")
        user = storage.get(User, user_id)
        if not user:
            return {"error": "Missing user_id"}, 400
        if "text" not in data:
            return {"error": "Missing text"}, 400

        new_review = Review(place_id=place_id, **data)
        new_review.save()
        return new_review.to_dict(), 201  # Return the new Review with status code 201

    elif request.method == 'GET':
        # Retrieve and return a list of Review objects associated with the place
        reviews_list = [review.to_dict() for review in place.reviews]
        return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    """
    Retrieve, delete, or update a Review object by ID.
    """
    # Retrieve the Review object based on review_id
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)  # Raise a 404 error if the review doesn't exist

    if request.method == 'DELETE':
        # Delete the Review object
        review.delete()
        storage.save()
        return {}, 200  # Return an empty dictionary with status code 200

    elif request.method == 'PUT':
        # Update the Review object with data from the request
        data = request.get_json()
        if not data:
            return {"error": "Not a JSON"}, 400
        # Update the Review object with valid key-value pairs from the data
        for key, value in data.items():
            if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
                setattr(review, key, value)
        review.save()
        return review.to_dict(), 200  # Return the updated Review with status code 200

    elif request.method == 'GET':
        return review.to_dict()  # Return the Review object as JSON

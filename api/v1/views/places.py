#!/usr/bin/python3
"""
    This is the places page handler for Flask.
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def cities_id_places(city_id):
    """
    Flask route at /cities/<city_id>/places.
    """
    # Retrieve the City object based on city_id
    city = storage.get(City, city_id)
    if not city:
        abort(404)  # Raise a 404 error if the city doesn't exist

    if request.method == 'POST':
        # Create a new Place object associated with the city
        data = request.get_json()
        if not data:
            return {"error": "Not a JSON"}, 400
        user_id = data.get("user_id")
        user = storage.get(User, user_id)
        if not user:
            return {"error": "Missing user_id"}, 400
        if "name" not in data:
            return {"error": "Missing name"}, 400

        new_place = Place(city_id=city_id, **data)
        new_place.save()
        return new_place.to_dict(), 201  # Return the new Place with status code 201

    elif request.method == 'GET':
        # Retrieve and return a list of Place objects associated with the city
        places_list = [place.to_dict() for place in city.places]
        return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def places_id(place_id):
    """
    Flask route at /places/<place_id>.
    """
    # Retrieve the Place object based on place_id
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Raise a 404 error if the place doesn't exist

    if request.method == 'DELETE':
        # Delete the Place object
        place.delete()
        storage.save()
        return {}, 200  # Return an empty dictionary with status code 200

    elif request.method == 'PUT':
        # Update the Place object with data from the request
        data = request.get_json()
        if not data:
            return {"error": "Not a JSON"}, 400
        # Update the Place object with valid key-value pairs from the data
        for key, value in data.items():
            if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
                setattr(place, key, value)
        place.save()
        return place.to_dict(), 200  # Return the updated Place with status code 200

    elif request.method == 'GET':
        return place.to_dict()  # Return the Place object as JSON


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
    Flask route at /places_search.
    """
    data = request.get_json()
    if not data:
        return {"error": "Not a JSON"}, 400

    # Retrieve criteria for searching places (states, cities, amenities)
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Initialize a list to store search results
    search_result = []

    if not states and not cities:
        # If no specific states or cities are provided, search all places
        places = storage.all("Place").values()
    else:
        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if not state:
                continue  # Skip invalid states
            for city in state.cities:
                if city.id not in cities:
                    cities.append(city.id)
        for city_id in cities:
            city = storage.get(City, city_id)
            if not city:
                continue  # Skip invalid cities
            for place in city.places:
                places.append(place)

    # Convert amenity IDs to Amenity objects and filter places based on amenities
    amenity_objs = [storage.get(Amenity, amenity_id) for amenity_id in amenities]
    for place in places:
        if all(amenity in place.amenities for amenity in amenity_objs):
            search_result.append(place.to_dict())

    return jsonify(search_result)  # Return the search results as JSON

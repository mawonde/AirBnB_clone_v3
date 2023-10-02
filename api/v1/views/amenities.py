#!/usr/bin/python3
"""
    An amenity page 
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """
        route at /amenities.
    """
    if request.method == 'POST':
        kwargs = request.get_json()
        if not kwargs:
            return {"error": "Not a JSON"}, 400
        if "name" not in kwargs:
            return {"error": "Missing name"}, 400
        n_amnt = Amenity(**kwargs)
        n_amnt.save()
        return n_amnt.to_dict(), 201

    elif request.method == 'GET':
        return jsonify([a.to_dict() for a in storage.all("Amenity").values()])


@app_views.route('/amenities/<id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_id(id):
    """
        Flask route at /amenities/<id>.
    """
    amnt = storage.get(Amenity, id)
    if (amnt):
        if request.method == 'DELETE':
            amnt.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            kwargs = request.get_json()
            if not kwargs:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(amnt, k, v)
            amnt.save()
        return amnt.to_dict()
    abort(404)

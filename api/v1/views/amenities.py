#!/usr/bin/python3
"""amenities creates a new view for amenity objects
by registering the view with a blueprint
"""
from flask import jsonify, abort, escape, request
from api.v1.views import amenities_views
from models import storage
from models.amenity import Amenity


@amenities_views.route('/amenities',
                       methods=['GET'],
                       strict_slashes=False)
def get_all_amenities():
    """retrieves all amenity objectsin storage"""
    amenities = storage.all(Amenity)
    return jsonify([item.to_dict() for item in amenities.values()])


@amenities_views.route('/amenities/<amenity_id>',
                       methods=['GET'],
                       strict_slashes=False)
def get_amenity(amenity_id):
    """retrieves amenity related to amenity_id"""
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        if amenity.id == escape(amenity_id):
            return jsonify(amenity.to_dict())
    abort(404)


@amenities_views.route('/amenities/<amenity_id>',
                       methods=['DELETE'],
                       strict_slashes=False)
def delete(amenity_id):
    """deletes the amenity with id amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return {}, 200


@amenities_views.route('/amenities',
                       methods=['POST'],
                       strict_slashes=False)
def create():
    """creates a new amenity"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    else:
        if "name" not in data.keys():
            return {"error": "Missing name"}, 400
        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()
        return amenity.to_dict(), 201


@amenities_views.route('/amenities/<amenity_id>',
                       methods=['PUT'],
                       strict_slashes=False)
def update(amenity_id):
    """updates an amenity object wit id amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    new_dict = {}
    if amenity is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    if 'name' not in data.keys():
        return {"error": "Missing name"}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            new_dict[key] = value
    amenity.__dict__.update(new_dict)
    storage.save()
    return amenity.to_dict(), 200

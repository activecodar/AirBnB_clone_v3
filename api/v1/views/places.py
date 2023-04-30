#!/usr/bin/python3
"""places defines a places view for the api registered
with a blueprint"""
from flask import jsonify, abort, escape, request
from api.v1.views import places_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@places_views.route('/cities/<city_id>/places',
                    methods=["GET"],
                    strict_slashes=False)
def get_all_places(city_id):
    """retrieves all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([item.to_dict() for item in city.places])


@places_views.route('/places/<place_id>',
                    methods=["GET"],
                    strict_slashes=False)
def get_place(place_id):
    """retrieves a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return place.to_dict(), 200


@places_views.route('/places/<place_id>',
                    methods=["DELETE"],
                    strict_slashes=False)
def delete(place_id):
    """deletes a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return {}, 200


@places_views.route('/cities/<city_id>/places',
                    methods=["POST"],
                    strict_slashes=True)
def create(city_id):
    """creates a place object"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if 'user_id' not in data.keys():
        return {"error": "Missing user_id"}, 400
    user_id = data.get('user_id')
    if storage.get(User, user_id) is None:
        abort(404)
    if 'name' not in data.keys():
        return {"error": "Missing name"}, 400
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return place.to_dict(), 201


@places_views.route('/places/<place_id>',
                    methods=["PUT"],
                    strict_slashes=True)
def update_place(place_id):
    """updates a place object"""
    place = storage.get(Place, place_id)
    new_dict = {}
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            new_dict[key] = value
    for key, value in new_dict.items():
        setattr(place, key, value)
    storage.save()
    return place.to_dict(), 200

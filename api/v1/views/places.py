#!/usr/bin/python3
"""places defines a places view for the api registered
with a blueprint"""
from flask import jsonify, abort, escape, request
from api.v1.views import places_views
from models import storage
from models.place import Place
from models.city import City


@places_views.route('/cities/<city_id>/places',
                    methods=["GET"],
                    strict_slashes=False)
def get_all_places(city_id):
    """retrieves all place objects of a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([item.to_dict() for item in city.places])

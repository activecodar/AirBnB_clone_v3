#!/usr/bin/python3
"""
This module provides views for managing cities.
Handles all CRUD functions
"""
from flask import request, jsonify

from api.v1.views import cities_views
from models import storage
from models.city import City
from models.state import State


@cities_views.route("/states/<state_id>/cities",
                    strict_slashes=False,
                    methods=["GET"])
def get_state_cities(state_id):
    """
    Gets a list of all cities linked to a state in the DB.

    Returns:
        A list of state cities in JSON format.
    """
    state = storage.get(State, state_id)
    if not state:
        return {"error": "Not found"}, 404
    return jsonify([s.to_dict() for s in state.cities])


@cities_views.route("/cities/<city_id>",
                    strict_slashes=False,
                    methods=["GET"])
def get_city(city_id):
    """
    Get a city by its ID.

    Args:
        city_id: The ID of the city to get.

    Returns:
        A city dictionary with all its details.

    Raises:
        404: If the city ID is not found.
    """
    city = storage.get(City, city_id)
    if not city:
        return {"error": "Not found"}, 404
    return city.to_dict(), 200


@cities_views.route("/cities/<city_id>",
                    strict_slashes=False,
                    methods=["DELETE"])
def delete_city(city_id):
    """
    Delete a city by its ID.

    Args:
        city_id: The ID of the city to be deleted.

    Returns:
        An empty dictionary.

    Raises:
        404: If the city ID is not found.
    """
    city = storage.get(City, city_id)
    if not city:
        return {"error": "Not found"}, 404
    storage.delete(city)
    storage.save()
    return {}, 200


@cities_views.route("/states/<state_id>/cities",
                    strict_slashes=False,
                    methods=["POST"])
def create_city(state_id):
    """
    Creates a new city with data provided in JSON format
    from request.get_json().

    Returns:
        A newly city dictionary.

    Raises:
        400: If the request is not JSON or does
        not contain name field.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    state = storage.get(State, state_id)
    if not state:
        return {"error": "Not found"}, 404
    if "name" not in data.keys():
        return {"error": "Missing name"}, 400
    data["state_id"] = state_id
    city = City(**data)
    storage.new(city)
    storage.save()
    return city.to_dict(), 201


@cities_views.route("/cities/<city_id>",
                    strict_slashes=False,
                    methods=["PUT"])
def update_city(city_id):
    """
    Update a city by its ID. Updates the name attribute
    with data provided in JSON format from request.get_json().

    Args:
        city_id: The ID of the city to update.

    Returns:
        An updated city dictionary.

    Raises:
        400: If the request is not JSON.
        404: If the state is not found.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    else:
        city = storage.get(City, city_id)
        if not city_id:
            return {"error": "Not found"}, 404
        ignored_keys = ["id", "created_at", "updated_at", "state_id"]
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(city, key, value)
        storage.save()
        return city.to_dict(), 200

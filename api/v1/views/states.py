#!/usr/bin/python3
"""
This module provides views for managing states.
Handles all CRUD functions
"""
from flask import request, jsonify

from api.v1.views import states_views
from models import storage
from models.state import State


@states_views.route("/states", strict_slashes=False, methods=["GET"])
def get_states():
    """
    Gets a list of all states in the DB.

    Returns:
        A list of state dictionaries.
    """
    states = storage.all('State')
    return jsonify([i[1].to_dict() for i in states.items()])


@states_views.route("/states/<state_id>",
                    strict_slashes=False,
                    methods=["GET"])
def get_state(state_id):
    """
    Get a state by its ID.

    Args:
        state_id: The ID of the state to get.

    Returns:
        A state dictionary with all ist details.

    Raises:
        404: If the state ID is not found.
    """
    state = storage.get(State, state_id)
    if not state:
        return {"error": "Not found"}, 404
    return state.to_dict(), 200


@states_views.route("/states/<state_id>",
                    strict_slashes=False,
                    methods=["DELETE"])
def delete_state(state_id):
    """
    Delete a state by its ID.

    Args:
        state_id: The ID of the state to delete.

    Returns:
        An empty dictionary.

    Raises:
        404: If the state ID is not found.
    """
    state = storage.get(State, state_id)
    if not state:
        return {"error": "Not found"}, 404
    storage.delete(state)
    storage.save()
    return {}, 200


@states_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """
    Creates a new state with data provided in JSON format
    from request.get_json().

    Returns:
        A newly state dictionary.

    Raises:
        400: If the request is not JSON or does
        not contain name field.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    else:
        if "name" not in data.keys():
            return {"error": "Missing name"}, 400
        state = State(**data)
        storage.new(state)
        storage.save()
        return state.to_dict(), 201


@states_views.route("/states/<state_id>",
                    strict_slashes=False,
                    methods=["PUT"])
def update_state(state_id):
    """
    Update a state by its ID. Updates the name attribute
    with data provided in JSON format from request.get_json().

    Args:
        state_id: The ID of the state to update.

    Returns:
        An updated state dictionary.

    Raises:
        400: If the request is not JSON.
        404: If the state is not found.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return {"error": "Not a JSON"}, 400
    else:
        state = storage.get(State, state_id)
        if not state:
            return {"error": "Not found"}, 404
        name = data.get("name", state.name) or state.name
        state.name = name if name.strip() != "" else state.name
        storage.save()
        return state.to_dict(), 200

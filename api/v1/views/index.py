#!/usr/bin/python3
"""
Module containing API endpoints.
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Endpoint to check the status of the application.

    Returns:
        A JSON object containing the status of the
        application.
    """
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Endpoint to retrieve the number of each objects by type.

    Returns:
        A JSON object containing the number of each objects by type.
    """
    amenity_count = storage.count(Amenity)
    city_count = storage.count(City)
    place_count = storage.count(Place)
    review_count = storage.count(Review)
    state_count = storage.count(State)
    user_count = storage.count(User)
    return {
        "amenities": amenity_count,
        "cities": city_count,
        "places": place_count,
        "reviews": review_count,
        "states": state_count,
        "users": user_count
    }

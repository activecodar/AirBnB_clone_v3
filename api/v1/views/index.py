#!/usr/bin/python3
"""
Module containing API endpoints.
"""
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Endpoint to check the status of the application.

    Returns:
        A JSON object containing the status of the
        application.
    """
    return {"status": "OK"}

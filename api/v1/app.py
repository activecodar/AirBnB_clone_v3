#!/usr/bin/python3
"""
This module contains the main
application/entrypoint for the API v1.
"""
import os

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views, states_views, cities_views, reviews_views
from api.v1.views import amenities_views, users_views, places_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
app.register_blueprint(states_views)
app.register_blueprint(cities_views)
app.register_blueprint(amenities_views)
app.register_blueprint(users_views)
app.register_blueprint(places_views)
app.register_blueprint(reviews_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Initiates teardown of the app context

    Args:
        exception (Exception): The exception thrown in process
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handles all page not found 404 errors

    Args:
        error (Exception): The exception thrown in process
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000),
            debug=True,
            threaded=True)

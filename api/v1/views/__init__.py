#!/usr/bin/python3
"""
This module contains the
views for the API v1.
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
states_views = Blueprint('state_views', __name__, url_prefix='/api/v1')
cities_views = Blueprint('cities_views', __name__, url_prefix='/api/v1')
amenities_views = Blueprint('amenities_views', __name__, url_prefix='/api/v1')
places_views = Blueprint('places_views', __name__, url_prefix='/api/v1')
users_views = Blueprint('users_views', __name__, url_prefix='/api/v1')
reviews_views = Blueprint('reviews_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *  # noqa
from api.v1.views.states import *  # noqa
from api.v1.views.cities import *  # noqa
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.places_reviews import *

#!/usr/bin/python3
"""places_reviews defines a view for place
reviews for the rest api
"""
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import request, jsonify, abort, escape
from api.v1.views import reviews_views


@reviews_views.route('/places/<place_id>/reviews',
                     methods=['GET'],
                     strict_slashes=True)
def get_place_reviews(place_id):
    """retrieves reviews of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([item.to_dict() for item in place.reviews])


@reviews_views.route('/reviews/<review_id>',
                     methods=['GET'],
                     strict_slashes=False)
def get_review(review_id):
    """retrieves a review based on review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@reviews_views.route('/reviews/<review_id>',
                     methods=['DELETE'],
                     strict_slashes=False)
def delete_review(review_id):
    """deletes a review based on review_id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@reviews_views.route('/places/<place_id>/reviews',
                     methods=['POST'],
                     strict_slashes=False)
def create_review(place_id):
    """creates a place review"""
    data = request.get_json()
    if not data:
        return {"error": "Not a JSON"}, 400
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if 'user_id' not in data.keys():
        return {"error": "Missing user_id"}, 400
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'text' not in data.keys():
        return {"error": "Missing text"}, 400
    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@reviews_views.route('/reviews/<review_id>',
                     methods=['PUT'],
                     strict_slashes=False)
def update_review(review_id):
    """updates a review object"""
    review = storege.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        return {"error": "Not a JSON"}, 400
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

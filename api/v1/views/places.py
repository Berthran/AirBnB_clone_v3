#!/usr/bin/python3
'''
Create a new view for Place objects that
handles all default RESTFul API actions
'''

from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_city_places(city_id):
    ''' Retrieves the list of all Place objects of a State '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    ''' Retrieves a City object '''
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    ''' Deletes a Place object '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    ''' Creates a Place Object '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.content_type == 'application/json':
        return jsonify('Not a JSON'), 400
    data = request.get_json()
    if 'user_id' not in data:
        return jsonify('Missing user_id'), 400
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'name' not in data:
        return jsonify('Missing name'), 400
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    ''' Updates a Place Object '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.content_type == 'application/json':
        return jsonify('Not a JSON'), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())

#!/usr/bin/python3
'''
Create a new view for Amenity objects that
handles all default RESTFul API actions
'''


from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.get('/amenities', strict_slashes=False)
def get_amenities():
    ''' Retrieves the list of all Amenity objects '''
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.get('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    ''' Retrieves a amenity object '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.delete('/amenities/<amenity_id>', strict_slashes=False)
def delete_amenity(amenity_id):
    ''' Deletes a amenity object '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.post('/amenities', strict_slashes=False)
def create_amenity():
    ''' Creates a amenity Object '''
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.put('/amenities/<amenity_id>', strict_slashes=False)
def update_amenity(amenity_id):
    ''' Updates a amenity Object '''
    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'amenity_id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())

#!/usr/bin/python3
'''
Create a new view for User objects that
handles all default RESTFul API actions
'''


from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.get('/users', strict_slashes=False)
def get_users():
    ''' Retrieves the list of all User objects '''
    users = storage.all(User).values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.get('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    ''' Retrieves a user object '''
    user = storage.get(User, user_id)
    if user is not None:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.delete('/users/<user_id>', strict_slashes=False)
def delete_user(user_id):
    ''' Deletes a User object '''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.post('/users', strict_slashes=False)
def create_user():
    ''' Creates a user Object '''
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    if 'email' not in data:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in data:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.put('/users/<user_id>', strict_slashes=False)
def update_user(user_id):
    ''' Updates a user Object '''
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())

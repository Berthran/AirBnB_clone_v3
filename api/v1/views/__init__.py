#!/usr/bin/python3
""" Blueprint for API """


from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
# from views.states import *
# from views.cities import *
# from views.amenities import *
# from views.users import *
# from views.places import *

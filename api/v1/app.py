#!/usr/bin/python3
"""
The Flask app settings
"""

from api.v1.views import app_views
from flask import Blueprint
from flask import Flasks
from models import storage
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """ Returns a 404 """
    return {"error": "Not found"}, 404


@app.teardown_appcontext
def close_session(exception):
    """ Closes the Session """
    storage.close()


if __name__ == "__main__":
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host='0.0.0.0',
            port=port,
            threaded=True)

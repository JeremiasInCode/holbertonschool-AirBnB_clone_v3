#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.error_api_404
def error_api_404():
    """ Return a custom error message """
    return jsonify({
        "error": "Not found"
    }), 404


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)

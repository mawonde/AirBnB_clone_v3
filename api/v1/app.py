#!/usr/bin/python3
""" Script that registers a Blueprint and runs Flask """
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
from flasgger import swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.register_blueprint(app_views)
cor = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """Closes the current SQLAlchemy session."""
    return storage.close()


@app.errorhandler(404)
def error(e):
    """Returns a JSON-formatted 404 status code"""
    return jsonify({"error": "Not found"}), 404


app.config['SWAGGER'] = {
        'title': 'AirBnB clone Restful API',
        'uiversion': 3
}


Swagger(app)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# Launch and configure app
def create_app():
    # Launch core
    app = Flask(__name__)
    CORS(app)

    with app.app_context():
        from . import routes
        return app

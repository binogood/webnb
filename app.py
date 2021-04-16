import json

from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from flask.json import JSONEncoder
from decimal import Decimal
from datetime import datetime, date
from response import *

from view import UserView, ItemView

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return JSONEncoder.default(self, obj)

def create_app(test_config=None):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_pyfile('config.py')
    app.register_blueprint(UserView.user_app)
    app.register_blueprint(ItemView.item_app)
    CORS(app, resources={'*': {'origins': '*'}}, expose_header='Authorization')
    return app



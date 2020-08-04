# -*- coding: utf-8 -*-

from flask import Flask
from flask_cors import CORS
from config import Config


app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers=[])
app.config.from_object(Config)
app.url_map.strict_slashes = False


from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/')

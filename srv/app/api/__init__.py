# -*- coding: utf-8 -*-

from flask import Blueprint, request, send_from_directory

from app import app
from app.lib.errors import err_method_not_allowed, err_not_implemented
from mordl import FeatsTagger, NeTagger, UposTagger
import os
from toxine import TextPreprocessor


(GET,   POST,   PUT,   PATCH,   DELETE,   HEAD,   OPTIONS) = (
'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS')

YES = ['t', 'tr', 'tru', 'true', 'y', 'ye', 'yes', 'yep', '1']

bp = Blueprint('api', __name__)

DATA_DIR = 'models'
text_preprocessor = TextPreprocessor()
upos_tagger = UposTagger()
upos_tagger.load(os.path.join(DATA_DIR, 'upos_model'))
feats_tagger = FeatsTagger()
feats_tagger.load(os.path.join(DATA_DIR, 'feats_model'))
ne_tagger = NeTagger()
ne_tagger.load(os.path.join(DATA_DIR, 'ne_model'))

#@app.route('/api/<path:path>', methods=[GET, POST, PUT, PATCH', DELETE])
@app.route('/<path:path>', methods=[GET, POST, PUT, PATCH, DELETE])
def catch_all (path):
    #path = '/api/' + path
    path = '/' + path
    res = err_not_implemented()
    for rule in app.url_map.iter_rules():
        if str(rule) == path:
            res = err_method_not_allowed()
            break
    return res

@bp.route('/static/<path:path>', methods=[GET])
def static (path):
    return send_from_directory('static', path)

from app.api import phonetize, tag, text_distance, tokenize

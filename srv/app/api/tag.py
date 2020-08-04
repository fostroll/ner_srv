# -*- coding: utf-8 -*-
from flask import jsonify, make_response
import json

from app.api import GET, bp, ne_tagger, text_preprocessor, upos_tagger


@bp.route('/api/tag/<string:text>', methods=[GET])
def tag(text=None):
    try:
        text = json.load(text)
        if isinstance(text[0], dict):
            text = [text]
    except AttributeError:
        text = [x[0] for x in text_preprocessor.process_text(text,
                                                             silent=True)]
    text = upos_tagger.predict(text, log_file=None)
    text = ne_tagger.predict(text, log_file=None)
    res = make_response(jsonify(list(text)), 200)
    return res

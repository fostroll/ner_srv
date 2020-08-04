# -*- coding: utf-8 -*-
from flask import jsonify, make_response

from app.api import GET, bp, text_preprocessor


@bp.route('/api/tokenize/<string:text>', methods=[GET], strict_slashes=False)
def tokenize(text):
    res = text_preprocessor.process_text(text, silent=True)
    res = make_response(jsonify([x[0] for x in res]), 200)
    return res

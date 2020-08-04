# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request
import json

from app.api import bp, GET, YES
from app.lib.phonetize import phonetize2


@bp.route('/api/phonetize/<string:text>',
          methods=[GET], strict_slashes=False)
def phonetize(text):
    level = request.args.get('level')
    syllables = request.args.get('syllables')

    kwargs = {}
    if level:
        kwargs['level'] = int(level)
    if syllables:
        kwargs['syllables'] = syllables.lower() in YES
    res = phonetize2(text, **kwargs)

    return make_response(jsonify(res), 200)

# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request
import json

from app.api import GET, YES, bp, feats_tagger, ne_tagger, \
                    text_preprocessor, upos_tagger
from app.lib.phonetize import phonetize2
from app.lib.text_distance import compute_distance


@bp.route('/api/text-distance/<string:text1>/<string:text2>',
          methods=[GET], strict_slashes=False)
def text_distance(text1, text2):
    ner1 = request.args.get('ner1')
    ner2 = request.args.get('ner2')
    level = request.args.get('level')
    algorithm = request.args.get('algorithm')
    normalize = request.args.get('normalize')
    qval = request.args.get('qval')

    def ner(text, ner_type):
        with text_preprocessor.lock:
            text = [x[0] for x in text_preprocessor.process_text(text,
                                                                 silent=True)]
        with upos_tagger.lock:
            text = upos_tagger.predict(text, log_file=None)
        with feats_tagger.lock:
            text = feats_tagger.predict(text, log_file=None)
        with ne_tagger.lock:
            text = ne_tagger.predict(text, log_file=None)

        addr = []
        for token in next(text):
            if token['MISC'].get('NE') == ner_type:
                addr.append(token['FORM'])

        return ' '.join(x for x in addr if x not in [
            'проспект', 'улица', 'шоссе'
        ])

    if ner1:
        text1 = ner(text1, ner1)
    if ner2:
        text2 = ner(text2, ner2)
    print(text1, ':', text2)

    if text1 and text2:
        kwargs = {}
        if level:
            kwargs['level'] = int(level)
        text1 = phonetize2(text1, **kwargs)
        text2 = phonetize2(text2, **kwargs)
        print(text1, ':', text2)
    
        kwargs = {}
        if algorithm:
            kwargs['algorithm'] = algorithm
        if normalize:
            kwargs['normalize'] = normalize.lower() in YES
        if qval:
            kwargs['qval'] = int(qval)
        res = compute_distance(text1, text2, **kwargs)
    else:
        res = -1

    return make_response(jsonify(res), 200)

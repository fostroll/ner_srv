# -*- coding: utf-8 -*-
from flask import jsonify, make_response, request
import json

from app.api import GET, POST, TimeoutException, bp, apply_thesaurus, \
                    feats_tagger, ne_tagger, text_preprocessor, upos_tagger


@bp.route('/api/tag/<path:text>', methods=[GET])
@bp.route('/api/tag', methods=[GET, POST])
def tag(text=None):
    format = request.args.get('format')
    if not text:
        text=request.args.get('text') or request.form.get('text')
    try:
        try:
            text = json.load(text)
            if isinstance(text[0], dict):
                text = [text]
        except AttributeError:
            text = apply_thesaurus(text)
            if not isinstance(text, str):
                raise TimeoutException()
            with text_preprocessor.lock:
                text = [x[0] for x in \
                            text_preprocessor.process_text(text, silent=True)]
        with upos_tagger.lock:
            text = upos_tagger.predict(text, log_file=None)
        with feats_tagger.lock:
            text = feats_tagger.predict(text, log_file=None)
        with text_preprocessor.lock:
            text = text_preprocessor.unmask_tokens(text, keep_empty=False,
                                                   keep_tags=True)
        with ne_tagger.lock:
            text = list(ne_tagger.predict(text, log_file=None))
        if format == 'simple':
            text = {'predict': [(x['FORM'], x['MISC'].get('NE'))
                                    for x in text for x in x
                                    if x['FORM'] and '-' not in x['ID']]}
        res = make_response(jsonify(text), 200)
    except TimeoutException:
        res = text
    return res

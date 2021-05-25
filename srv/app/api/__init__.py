# -*- coding: utf-8 -*-
from contextlib import contextmanager
from flask import Blueprint, request, send_from_directory
from junky import add_class_lock
from mordl import FeatsTagger, NeTagger, UposTagger
import os
import re
import signal
from toxine import TextPreprocessor

from app import app
from app.lib.errors import err_gateway_timeout, err_method_not_allowed, \
                           err_not_implemented


(GET,   POST,   PUT,   PATCH,   DELETE,   HEAD,   OPTIONS) = (
'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS')

YES = ['t', 'tr', 'tru', 'true', 'y', 'ye', 'yes', 'yep', '1']

bp = Blueprint('api', __name__)

DATA_DIR = 'models'
THESAURUS_FN = os.path.join(DATA_DIR, 'thesaurus.csv')
THESAURUS_TIMEOUT = None  # seconds
text_preprocessor = add_class_lock(TextPreprocessor())
upos_tagger = add_class_lock(UposTagger())
feats_tagger = add_class_lock(FeatsTagger())
ne_tagger = add_class_lock(NeTagger())

@app.before_first_request
def initialize():
    global text_preprocessor, upos_tagger, feats_tagger, ne_tagger

    upos_tagger.load(os.path.join(DATA_DIR, 'upos_model'))
    feats_tagger.load(os.path.join(DATA_DIR, 'feats_model'))
    ne_tagger.load(os.path.join(DATA_DIR, 'ne_model'))

thesaurus = {}
if not os.path.isfile(THESAURUS_FN):
    print('WARNING: thesaurus is not found')
else:
    with open(THESAURUS_FN) as f:
        err_no = None
        for line_no, line in enumerate(f, start=1):
            assert not err_no, \
                'ERROR: error in thesaurus (line #{})'.format(err_no)
            if not line:
                err_no = line_no
                continue
            line = line.split('\t')
            if len(line) == 3 and line[0] == '#':
                continue
            assert len(line) == 2, \
                'ERROR: error in thesaurus (line #{})'.format(line_no)
            assert line[0] not in thesaurus, \
                'ERROR: duplicate key in thesaurus (line #{})'.format(line_no)
            thesaurus[line[0]] = line[1]
re_thesaurus = [(re.compile(x), y) for x, y in thesaurus.items()]

class TimeoutException(Exception):
    pass

@contextmanager
def time_limit(seconds):
    yield
    return
    ### isgnal only works in the main thread:
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds or 0)
    try:
        yield
    finally:
        signal.alarm(0)

def apply_thesaurus(text):
    line_no = 1
    try:
        with time_limit(THESAURUS_TIMEOUT):
            for key, value in re_thesaurus:
                text = key.sub(value, text)
                line_no += 1
    except TimeoutException as e:
        text = 'WARNING: timeout while applying thesaurus regexps ' \
               '(line #{})'.format(line_no)
        print(text)
        text = err_gateway_timeout(text)
    return text

#@app.route('/api/<path:path>', methods=[GET, POST, PUT, PATCH', DELETE])
@app.route('/<path:path>', methods=[GET, POST, PUT, PATCH, DELETE])
def catch_all(path):
    #path = '/api/' + path
    path = '/' + path
    res = err_not_implemented()
    for rule in app.url_map.iter_rules():
        if str(rule) == path:
            res = err_method_not_allowed()
            break
    return res

@bp.route('/static/<path:path>', methods=[GET])
def static(path):
    return send_from_directory('static', path)

from app.api import phonetize, tag, text_distance, tokenize

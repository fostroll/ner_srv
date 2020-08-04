#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from app import app

PORT = 2020

if __name__ == "__main__":
    if 'prod' in sys.argv:
        from wsgiref.simple_server import make_server
        make_server('0.0.0.0', PORT, app).serve_forever()
    else:
        app.run(host='0.0.0.0', port=PORT, debug=True)

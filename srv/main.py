#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from app import app


ADDRESS = '0.0.0.0'
PORT = 2020

if __name__ == "__main__":
    if 'prod' in sys.argv:
        from wsgiref.simple_server import make_server
        make_server(ADDRESS, PORT, app).serve_forever()
    else:
        app.run(host=ADDRESS, port=PORT, debug=True)

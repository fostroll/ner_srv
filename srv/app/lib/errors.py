# -*- coding: utf-8 -*-

from flask import jsonify, make_response
from werkzeug.http import HTTP_STATUS_CODES

# message == None: empty response
# message == '': response without a message
def error_response (status_code, message=''):
    if message is None:
        response = ''
    else:
        payload = {'error': HTTP_STATUS_CODES.get(status_code,
                                                  'Unknown error')}
        if message != '':
            payload['message'] = message
        response = jsonify(payload)
        #response.status_code = status_code
    return make_response(response, status_code)

def err_bad_request (message=''):
    return error_response(400, message)

def err_unauthorized (message=''):
    return error_response(401, message)

def err_forbidden (message=''):
    return error_response(403, message)

def err_not_found (message=''):
    return error_response(404, message)

def err_method_not_allowed (message=''):
    return error_response(405, message)

def err_not_acceptable (message=''):
    return error_response(406, message)

def err_conflict (message=''):
    return error_response(409, message)

def err_gone (message=''):
    return error_response(410, message)

def err_unprocessable_entity (message=''):
    return error_response(422, message)

def err_not_implemented (message=''):
    return error_response(501, message)

def err_insufficient_storage (message=''):
    return error_response(507, message)

def err_network_connect_timeout (message=''):
    return error_response(599, message)

import traceback
from flask import current_app, jsonify
from common.DataClasses import ServerConfig

class ExceptionBase(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def handle_exception_base(error: ExceptionBase):
    response = jsonify(error.to_dict())
    return response, error.status_code


def handle_unexpected_error(error: Exception):
    response = {"message": "An unexpected error occurred"}

    sc = ServerConfig()
    if sc["FLASK_SHOW_TRACEBACK"]:
        response["traceback"] = traceback.format_exc()

    return jsonify(response), 500

__author__ = 'archeg'


class WebException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidFormatException(WebException):
    pass


class PermissionDeniedException(WebException):
    def __init__(self):
        WebException.__init__(self, "Permission denied", status_code=403)
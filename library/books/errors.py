from rest_framework import exceptions


class APIException(exceptions.APIException):
    """
    Exception class that caught by renderer and produce pretty output.

    It also has ``error_code`` attribute that may be set by other app otherwise it'll be ``-1``
    """

    def __init__(self, detail=None, error_code=-1, kw=None):
        if isinstance(kw, dict):
            detail = detail % kw
        super(APIException, self).__init__(detail=detail)
        self.error_code = error_code
        self.message = detail

class ValidationError(APIException):
    """
    Exception class for all kind of validation errors
    """
    status_code = 400


class NotFound(APIException):
    """
    Exception class for missing resource
    """
    status_code = 404


class UserError(APIException):
    status_code = 400
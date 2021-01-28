from .json_response import JsonResponse
from .error_code import ERROR_CODE

class KeyLost(JsonResponse):
    def __init__(self, key, kind, *args, **kwargs):
        error_code = 1000
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code].format(key, kind), status=400, *args, **kwargs)

class TypeError(JsonResponse):
    def __init__(self, key, kind, need_type, *args, **kwargs):
        error_code = 1001
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code].format(key, kind, need_type), status=400, *args, **kwargs)

class LengthError(JsonResponse):
    def __init__(self, key, kind, max_length, *args, **kwargs):
        error_code = 1002
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code].format(key, kind, max_length), status=400, *args, **kwargs)

class IllegalKey(JsonResponse):
    def __init__(self, key, kind, *args, **kwargs):
        error_code = 1003
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code].format(key, kind), status=400, *args, **kwargs)

class RequestExpired(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1004
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=400, *args, **kwargs)

class InvalidRequest(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1005
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=400, *args, **kwargs)

class RepeatRequest(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1006
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=400, *args, **kwargs)

class BadRequest(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1007
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=400, *args, **kwargs)

class AuthorizationFailed(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1008
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=401, *args, **kwargs)

class TokenExpired(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1009
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=401, *args, **kwargs)

class InvalidCaptcha(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1010
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=401, *args, **kwargs)

class NotFound(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1011
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=404, *args, **kwargs)

class MethodNotAllowed(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1012
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=405, *args, **kwargs)

class Conflict(JsonResponse):
    def __init__(self, key, *args, **kwargs):
        error_code = 1013
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code].format(key), status=409, *args, **kwargs)

class TooManyRequest(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1014
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=429, *args, **kwargs)

class JsonOk(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(error_code=0, message="ok", data=data, status=200, *args, **kwargs)

class Created(JsonResponse):
    def __init__(self, data, *args, **kwargs):
        super().__init__(error_code=0, message="created", data=data, status=201, *args, **kwargs)

class Forbidden(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1015
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=403, *args, **kwargs)

class Unregistered(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1016
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=401, *args, **kwargs)

class PasswordError(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1017
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=401, *args, **kwargs)

class SendCaptchaFailed(JsonResponse):
    def __init__(self, *args, **kwargs):
        error_code = 1018
        super().__init__(error_code=error_code, message=ERROR_CODE[error_code], status=400, *args, **kwargs)

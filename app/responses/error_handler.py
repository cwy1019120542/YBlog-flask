from .responses import NotFound, MethodNotAllowed, TooManyRequest

def error_404(e):
    return NotFound()

def error_405(e):
    return MethodNotAllowed()

def error_429(e):
    return TooManyRequest()

error_handler_group_list = ((404, error_404), (405, error_405), (429, error_429))
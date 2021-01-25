from json import dumps
from flask import Response

class JsonResponse(Response):

    def __init__(self, error_code, message, data=None, *args, **kwargs):
        data_group = {
            "error_code": error_code,
            "message": message,
            "data": data
        }
        json_data = dumps(data_group, indent=2, separators=(", ", ": ")) + "\n",
        super().__init__(json_data, mimetype="application/json", *args, **kwargs)
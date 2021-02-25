from copy import deepcopy
from flask import views, request, current_app
from ..models.models import MODELS
from ..func_tools.request_func import clean_request, catch_error, check_resource, check_request, authentication

class Base(views.MethodView):

    is_decorate = False

    decorator_list = [clean_request, check_resource, catch_error]

    def __new__(cls, *args, **kwargs):
        if not cls.is_decorate:
            for decorator in cls.decorator_list:
                for method in ("get", "post", "put", "delete"):
                    setattr(cls, method, decorator(getattr(cls, method)))
            cls.is_decorate = True
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, model_name=None, scope_name=None,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.params = request.args
        self.body = request.json if request.json else {}
        self.files = request.files
        self.headers = request.headers
        self.method = request.method.lower()
        self.url = request.url
        self.ip = request.remote_addr
        self.model = MODELS[model_name]() if model_name else None
        self.scope_name = scope_name
        model_fields = deepcopy(self.model.fields) if self.model else {}
        self.params_rule = deepcopy(self.model.params_fields) if self.model else {}
        self.body_rule = model_fields
        self.logger = current_app.logger

    def get(self, *args, **kwargs):
        raise NotImplementedError("get is not implemented")

    def post(self, *args, **kwargs):
        raise NotImplementedError("post is not implemented")

    def put(self, *args, **kwargs):
        raise NotImplementedError("put is not implemented")

    def delete(self, *args, **kwargs):
        raise NotImplementedError("delete is not implemented")

class EncryptedAPI(Base):

    decorator_list = [check_request, clean_request , check_resource, catch_error]

class Authentication(EncryptedAPI):

    decorator_list = [authentication, check_request, clean_request, check_resource, catch_error]


















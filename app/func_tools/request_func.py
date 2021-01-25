import json
import base64
from functools import wraps
from traceback import print_exc
from .tool_func import *
from ..responses.responses import *
from ..config.secret_config import AUTHORIZATION_SECRET
from ..models.models import MODELS
from ..extentions import redis_client

def clean_request(request_func):
    @wraps(request_func)
    def wrapper(self, *args, **kwargs):
        params_rule = {**self.params_rule.get(self.method, {}), **self.params_rule["base"]}
        body_rule = self.body_rule.get(self.method, {})
        for kind, data, api_rule in (
                ("params", self.params, params_rule), ("body", self.body, body_rule)):
            clean_data = {}
            for key, key_attr in api_rule.items():
                key_type, max_length, default, func = key_attr[:4]
                if key not in data and default == None and kind == "body":
                    return KeyLost(key, kind)
                value = data.get(key, default)
                if value == None and kind == "params":
                    continue
                value = func(value) if func else value
                if isinstance(value, FormatError):
                    return IllegalKey(key, kind)
                if not isinstance(value, key_type):
                    try:
                        value = key_type(value)
                    except:
                        return TypeError(key, kind, key_type)
                if max_length:
                    length = len(str(value))
                    if length > max_length:
                        return LengthError(key, kind, max_length)
                clean_data[key] = value
            setattr(self, kind, clean_data)
        return request_func(self, *args, **kwargs)
    return wrapper

def authentication(func):
    @wraps(func)
    def wrapper(self, user_id, *args, **kwargs):
        authorization = self.headers.get("Authorization")
        if not authorization:
            return AuthorizationFailed()
        token_list = re.findall(r"^Bearer (.*)", authorization)
        if not token_list:
            return AuthorizationFailed()
        token = token_list[0]
        token_split_list = token.split('.')
        if len(token_split_list) != 3:
            return AuthorizationFailed()
        token_headers, token_payload, token_signature = token_split_list
        check_str = ".".join((token_headers, token_payload, AUTHORIZATION_SECRET))
        check_signature = hashlib.sha256(check_str.encode()).hexdigest()
        if check_signature != token_signature:
            return AuthorizationFailed()
        token_payload_decode = json.loads(base64.b64decode(token_payload).decode())
        sub = token_payload_decode["sub"]
        if sub != user_id:
            return AuthorizationFailed()
        exp = token_payload_decode["exp"]
        timestamp = get_timestamp()
        if exp <= timestamp:
            return TokenExpired()
        scope = token_payload_decode["scope"][self.method]
        if self.model_name and self.model_name not in scope:
            return Forbidden()
        return func(self, user_id, *args, **kwargs)
    return wrapper

def check_request(request_func):
    @wraps(request_func)
    def wrapper(self, user_id, *args, **kwargs):
        timestamp = get_timestamp()
        clean_group = {**self.params, **self.body}
        clean_group["url"] = self.url
        secret = redis_client.get(f"user_{user_id}_secret")
        if not secret:
            return InvalidRequest()
        clean_group["secret"] = secret
        group_key_list = list(clean_group)
        group_key_list.sort()
        item_str_list = []
        for group_key in group_key_list:
            item_str_list.append(f"{group_key}={clean_group[group_key]}")
        item_str = "&".join(item_str_list)
        md5_item_str = hashlib.md5(item_str.encode()).hexdigest()
        signature = self.params["signature"]
        if md5_item_str != signature:
            return InvalidRequest()
        request_timestamp = self.params["timestamp"]
        if timestamp - request_timestamp >= 60:
            return RequestExpired()
        request_uid = self.params["uid"]
        request_uid_key = f"request_uid_{request_uid}"
        uid = redis_client.get(request_uid_key)
        if uid:
            return RepeatRequest()
        redis_client.set(request_uid_key, timestamp, ex=60)
        return request_func(self, user_id, *args, **kwargs)
    return wrapper

def catch_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.logger.error(f"{self.request.__dict__} {print_exc()}")
            return BadRequest()
    return wrapper

def check_resource(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        model_data_list = []
        for resource_group in kwargs.items():
            resource_key, resource_id = resource_group
            model_class = MODELS[resource_key.rstrip("_id")]
            model_data_list.append((model_class, resource_key,  resource_id))
        for model_index, (model_class, resource_key, resource_id) in enumerate(model_data_list):
            resource = model_class().find_one({resource_key: resource_id})
            if not resource:
                return NotFound()
            if model_index == 0:
                continue
            parent_model, parent_resource_key, parent_resource_id = model_data_list[model_index-1]
            if resource[parent_resource_key] != parent_resource_id:
                return NotFound()
        return func(self, *args, **kwargs)
    return wrapper
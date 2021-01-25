from bson.objectid import ObjectId
from functools import wraps
from copy import deepcopy
from pymongo.collection import ReturnDocument
from ..extentions import mongo_client
from ..func_tools.tool_func import get_timestamp

def clean_fields(limit_fields_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, data, *args, **kwargs):
            limit_fields = getattr(self, limit_fields_name)
            for field in deepcopy(data):
                if field not in limit_fields:
                    data.pop(field)
            return func(self, data, *args, **kwargs)
        return wrapper
    return decorator

def clean_one_return(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        data = func(self, *args, **kwargs)
        for field, value in data.items():
            handle_func = self.fields.get(field)
            data[field] = handle_func[4](value) if handle_func and handle_func[4] else value
        return data
    return wrapper

def clean_return(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        data_list = func(self, *args, **kwargs)
        for data in data_list:
            for field, value in data.items():
                handle_func = self.fields[field][4]
                data[field] = handle_func(value) if handle_func else value
        return data_list
    return wrapper


class Base:

    fields = {}
    params_fields = ()
    find_except_fields = ()
    find_one_except_fields = ()

    def __init__(self, model_name):
        self.model_name = model_name
        self.collection = mongo_client.db[self.model_name]
        self.params_fields = ()

    @clean_fields("params_fields")
    def find_exists(self, params):
        data = self.collection.find_one(params, {"_id": True})
        return True if data else False

    @clean_return
    @clean_fields("params_fields")
    def find(self, params, skip=0, limit=0, sort=(("id", 1), )):
        return self.collection.find(params, dict.fromkeys(self.find_except_fields, False), skip=skip, limit=limit, sort=sort)

    @clean_one_return
    @clean_fields("params_fields")
    def find_one(self, params):
        return self.collection.find_one(params, dict.fromkeys(self.find_one_except_fields, False))

    @clean_one_return
    @clean_fields("params_fields")
    def find_all_fields(self, params):
        return self.collection.find_one(params)

    @clean_one_return
    @clean_fields("fields")
    def insert(self, body):
        timestamp = get_timestamp()
        body["insert_timestamp"] = timestamp
        next_id = mongo_client.db.model_id.find_one_and_update({"model_name": self.model_name}, {"$inc": {"id": 1}}, return_document=ReturnDocument.AFTER)["id"]
        body["id"] = int(next_id)
        str_object_id = self.collection.insert(body)
        data = self.find_one({"_id": ObjectId(str_object_id)})
        return data







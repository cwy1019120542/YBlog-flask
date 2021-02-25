import time
from .base import Base
from ..func_tools.tool_func import check_email, md5_password
from ..config.secret_config import SCOPE

class User(Base):
    fields = {
        "name": [str, 30, "洋帅帅的小弟", None, None],
        "sex": [int, 1, 3, lambda i: i if i in (1, 2, 3) else 3, None],
        "birthday": [int, 10, 0, lambda i: i if i<time.time() else time.time(), None],
        "email": [str, 100, None, check_email, None],
        "password": [str, 32, None, md5_password, None],
        "scope": [dict, None, SCOPE, lambda i: SCOPE, None]
    }
    params_fields = {
        "id": [int, 5, None, None, None],
        "email": [str, 100, None, check_email, None]
    }
    find_except_fields = ("_id", "password", "scope")
    find_one_except_fields = ("_id", "password", "scope")

    def __init__(self):
        super().__init__("user")
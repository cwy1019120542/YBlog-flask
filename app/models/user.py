from .base import Base
from ..func_tools.tool_func import check_email, md5_password
from ..config.secret_config import SCOPE

class User(Base):
    fields = {
        "name": [str, 30, "洋帅帅的小弟", None, None],
        "sex": [int, 1, 3, None, None],
        "birthday": [int, 10, 0, None, None],
        "email": [str, 100, None, check_email, None],
        "password": [str, 32, None, md5_password, None],
        "scope": [dict, None, SCOPE, lambda i: SCOPE, None]
    }
    params_fields = ("id", "email")
    find_except_fields = ("_id", "password", "scope")
    find_one_except_fields = ("_id", "password", "scope")

    def __init__(self):
        super().__init__("user")
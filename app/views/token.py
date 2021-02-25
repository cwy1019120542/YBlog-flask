from hashlib import sha256
from json import dumps
from base64 import b64encode
from .base import EncryptedAPI
from ..responses.responses import Unregistered, PasswordError, Created
from ..func_tools.tool_func import get_timestamp
from ..config.secret_config import AUTHORIZATION_SECRET

class Token(EncryptedAPI):

    methods = ["POST"]

    def __init__(self, *args, **kwargs):
        super().__init__("user", 'token', *args, **kwargs)
        self.body_rule = {
            "email": self.model.fields["email"],
            "password": self.model.fields["password"],
        }

    def post(self, user_id):
        email = self.body["email"]
        user = self.model.find_all_fields({"email": email})
        if not user:
            return Unregistered()
        if user["password"] != self.body["password"]:
            return PasswordError()
        b64_encode = lambda i: b64encode(dumps(i).encode())
        token_headers = b64_encode({"alg": "HS256", "type": "JWT"})
        token_payload = b64_encode({"sub": user["id"], "exp": get_timestamp()+604800, "scope": user["scope"]})
        signature = sha256(".".join((token_headers, token_payload, AUTHORIZATION_SECRET)).encode()).hexdigest()
        token = ".".join((token_headers, token_payload, signature))
        return Created({"token": token})


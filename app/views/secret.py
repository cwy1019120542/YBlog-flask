import uuid
from .base import Base
from ..responses.responses import Unregistered, PasswordError, Created
from ..extentions import redis_client

class Secret(Base):

    methods = ["POST"]

    def __init__(self, *args, **kwargs):
        super().__init__("user", *args, **kwargs)
        self.body_rule = {
            "email": self.model.fields["email"],
            "password": self.model.fields["password"]
        }

    def post(self):
        email = self.body["email"]
        user = self.model.find_all_fields({"email": email})
        if not user:
            return Unregistered()
        if user["password"] != self.body["password"]:
            return PasswordError()
        user_id = user['id']
        secret_key = f"user_{user_id}_secret"
        user_secret = redis_client.get(secret_key)
        if not user_secret:
            user_secret = str(uuid.uuid1())
            redis_client.set(secret_key, user_secret, ex=604800)
        return Created({"secret": str(user_secret), "user_id": user_id})

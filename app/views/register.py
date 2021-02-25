from .base import Base
from ..responses.responses import Created, EmailConflict, InvalidCaptcha
from ..extentions import redis_client

class Register(Base):

    methods = ["POST"]

    def __init__(self, *args, **kwargs):
        super().__init__(model_name="user", *args, **kwargs)
        self.body_rule["captcha"] = [int, 6, None, None]

    def post(self):
        email = self.body["email"]
        repeat_email = self.model.find_exists({"email": email})
        if repeat_email:
            return EmailConflict()
        db_captcha = redis_client.get(f"{email}_captcha")
        if not db_captcha:
            return InvalidCaptcha()
        if self.body["captcha"] != int(db_captcha):
            return InvalidCaptcha()
        user = self.model.insert(self.body)
        redis_client.delete(f"{email}_captcha")
        return Created(user)





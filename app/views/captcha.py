import random
from flask import current_app
from .base import Base
from ..func_tools.tool_func import check_email, send_mail
from ..extentions import redis_client
from ..responses.responses import Created, SendCaptchaFailed

class SendCaptchaError(Exception):
    pass

class Captcha(Base):

    methods = ["POST"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.body_rule["POST"] = {
            "email": [str, 100, None, check_email]
        }

    def post(self):
        email = self.body["email"]
        random_num = random.randrange(100000, 999999)
        mail_username = current_app.config["MAIL_USERNAME"]
        try:
            send_mail(mail_username, [email], "YBlog验证码", f"{random_num}")
        except:
            return SendCaptchaFailed()
        redis_client.set(f"{email}_captcha", random_num, ex=60)
        return Created(None)
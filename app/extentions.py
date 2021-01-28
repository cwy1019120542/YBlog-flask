import logging
from logging import handlers
from flask_pymongo import PyMongo
from flask_redis import FlaskRedis
from flask_mail import Mail
from flask_limiter import Limiter
from flask_cors import CORS

mongo_client = PyMongo()
redis_client = FlaskRedis()
mail = Mail()
limiter = Limiter()

def init_extentions(app):
    mongo_client.init_app(app)
    redis_client.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    CORS(app)

def get_logging_handler(mailhost, fromaddr, password, log_path):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = handlers.TimedRotatingFileHandler(filename=log_path, when="W0", interval=1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    mail_handler = handlers.SMTPHandler(mailhost=(mailhost, 25), fromaddr=fromaddr,
                                        toaddrs=fromaddr,
                                        credentials=(fromaddr, password), subject="yblog_critical_log")
    mail_handler.setLevel(logging.CRITICAL)
    mail_handler.setFormatter(formatter)
    return (file_handler, mail_handler)
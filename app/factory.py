import logging
from flask import Flask, request
from flask.logging import default_handler
from .config.env_config import env_config
from .config.limit_config import limit_config
from .extentions import init_extentions, get_logging_handler, limiter
from .views.register import Register
from .views.captcha import Captcha
from .views.secret import Secret
from .views.token import Token
from .responses.error_handler import error_handler_group_list

def add_with_prefix(app, prefix, url_list):
    for url, view_class in url_list:
        view_name = view_class.__name__
        view_limit = limit_config[view_name]
        app.add_url_rule(f"/yblog/api{prefix}{url}", view_func=limiter.limit(view_limit)(view_class.as_view(view_name)))

def write_request_log(app):
    def wrapper(response):
        app.logger.info(f"{request.__dict__} {response.__dict__}")
        return response
    return wrapper

def create_app(config_type):
    app = Flask(__name__)
    app.config.from_object(env_config[config_type])
    init_extentions(app)
    add_with_prefix(app, "", (("/register", Register), ("/captcha", Captcha), ("/secret", Secret)))
    add_with_prefix(app, "/users/<int:user_id>", (("/token", Token), ))
    app.logger.removeHandler(default_handler)
    app.logger.setLevel(logging.DEBUG)
    for logging_handler in get_logging_handler(app.config["MAIL_SERVER"], app.config["MAIL_USERNAME"],
                                               app.config["MAIL_PASSWORD"], app.config["FLASK_LOG_PATH"]):
        app.logger.addHandler(logging_handler)
    for error_handler_group in error_handler_group_list:
        app.register_error_handler(*error_handler_group)
    app.after_request(write_request_log(app))
    return app


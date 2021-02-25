import hashlib
import time
import re
import os
import mimetypes
from flask_mail import Message
from ..extentions import mail

class FormatError(Exception):
    pass

def check_email(email):
    match_email = re.search(r'^\w+@(\w+\.)+(com|cn|net)$', email)
    if match_email:
        return email
    else:
        return FormatError()

def md5_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def get_timestamp():
    return int(time.time())

def transform_bool(value):
    try:
        int_value = int(value)
    except:
        return
    else:
        return bool(int_value)

def send_mail(sender, recipients, subject, body, attachment_path_list=[]):
    msg = Message(subject=subject, recipients=recipients, body=body, sender=sender)
    for attachment_path in attachment_path_list:
        attachment_dir, attachment_name = os.path.split(attachment_path)
        attachment_mimetype = mimetypes.guess_type(attachment_name)[0]
        msg.attach(attachment_name, attachment_mimetype, open(attachment_path).read())
    mail.send(msg)

def timestamp_to_datetime(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

def sort_and_connect(data):
    key_list = list(data)
    key_list.sort()
    str_item_list = []
    for key in key_list:
        value = data[key]
        if isinstance(value, bool):
            value = str(value).lower()
        elif value == None:
            value = "null"
        str_item_list.append(f"{key}={value}")
    return "&".join(str_item_list)


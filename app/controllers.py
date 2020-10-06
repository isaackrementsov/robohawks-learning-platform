from flask import session, redirect

from app import app
from app.mod_user.models import User


def is_admin():
    user = User.lookup_id(id())

    return user.admin


def get_field(e):
    return str(e).split('.')[2].split('[')[0]


def assign(source, target):
    for key in source:
        target.__dict__[key] = source[key]

    return target

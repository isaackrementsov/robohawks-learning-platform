from flask import session, redirect

from app import app
from app.mod_user.models import User


def id():
    return session.get('user_id', '')


def go_home():
    return redirect('/user/login')


def go_dashboard():
    return redirect('/user/dashboard')


def missing_session():
    return not User.matches_id(id())

def is_admin():
    user = User.lookup_id(id())

    return user.admin

def get_field(e):
    return str(e).split('.')[2].split('[')[0]

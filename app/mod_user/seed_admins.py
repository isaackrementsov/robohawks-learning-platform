from app import db
from sqlalchemy.orm import relationship
from app.mod_user.models import User

import json


user_source = app.LOCAL_CONFIG['seed_user']

user = User(
    email=user_source['email'],
    username=user_source['username'],
    first_name=user_source['first_name'],
    last_name=user_source['last_name'],
    password=user_source['password'],
    admin=True
)

try:
    user.save()
except Exception as e:
    print('Error saving seed user:', str(e))

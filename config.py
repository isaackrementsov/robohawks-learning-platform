import os
import json


LOCAL_CONFIG = json.load(open('local_config.json', 'r'))

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESS_KEY = LOCAL_CONFIG['csrf_sess_key']
SECRET_KEY = LOCAL_CONFIG['secret_key']

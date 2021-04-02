import os
import json

LOCAL_CONFIG = json.load(open('local_config.json', 'r'))

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_settings = LOCAL_CONFIG['database']

SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{server}/{db}'.format(
    username=db_settings['username'],
    password=db_settings['password'],
    server=db_settings['server'],
    db=db_settings['db']
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True
CSRF_SESS_KEY = LOCAL_CONFIG['csrf_sess_key']

SECRET_KEY = LOCAL_CONFIG['secret_key']
SESSION_TYPE = 'memcached'

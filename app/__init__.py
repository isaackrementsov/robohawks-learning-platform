from flask import Flask, jsonify, request
from flask_session import Session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

Session(app)

CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    res = {'error': '404 not found'}
    return jsonify(res), 404

@app.errorhandler(500)
def server_error():
    res = {'error': '500 server error'}
    return jsonify(res), 500

@app.after_request
def allow_credentials(res):
    res.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    res.headers['Vary'] = 'Origin'
    res.headers['Access-Control-Allow-Credentials'] = 'true'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type,Content-Length,Authorization,Accept,X-Requested-With,Cookie,Set-Cookie'
    res.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,PATCH,OPTIONS'

    return res


from app.mod_user.controllers import mod_user
from app.mod_page.controllers import mod_page
from app.mod_credential.controllers import mod_credential
from app.mod_course.controllers import mod_course
from app.mod_assessment.controllers import mod_assessment

app.register_blueprint(mod_user)
app.register_blueprint(mod_page)
app.register_blueprint(mod_credential)
app.register_blueprint(mod_course)
app.register_blueprint(mod_assessment)

db.create_all()

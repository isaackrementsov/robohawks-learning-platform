from flask import Flask, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    res = {'error': '404 not found'}
    return jsonify(res), 404


@app.errorhandler(500)
def server_error():
    res = {'error': '500 server error'}
    return jsonify(res), 500


from app.mod_user.controllers import mod_user
from app.mod_page.controllers import mod_page
from app.mod_credential import mod_credential
from app.mod_course import mod_course
from app.mod_assessment import mod_assessment

app.register_blueprint(mod_user)
app.register_blueprint(mod_page)
app.register_blueprint(mod_credential)
app.register_blueprint(mod_course)
app.register_blueprint(mod_assessment)



db.create_all()

from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug import secure_filename


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', session=session), 404


@app.errorhandler(500)
def server_error():
    return render_template('500.html', session=session), 500


@app.route('/')
def index():
    return render_template('index.html', session=session)



from app.mod_user.controllers import mod_user

app.register_blueprint(mod_user)



db.create_all()

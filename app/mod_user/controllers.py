from flask import Flask, Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash

from app import db
from app.controllers import missing_session, go_home, go_dashboard

from app.mod_user.forms import LoginForm, CreateForm
from app.mod_user.models import User


mod_user = Blueprint('user', __name__, url_prefix='/user')


def create_session(user):
    session['user_id'] = user.id
    session['username'] = user.username
    session['avatar'] = user.avatar
    session['admin'] = user.admin


@mod_user.route('/login/', methods['GET', 'POST'])
def login():
    if not missing_session(): return go_dashboard()

    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.lookup(form.emailOrUsername.data)

        if user and user.password == form.password.data:
            create_session(user)

            return redirect(url_for('user.dashboard', user_id=user.id))

        flash('Wrong username or password', 'error')

    return render_template('user/login.html', form=form, session=session)


@mod_user.route('/newstudent/', methods=['GET', 'POST'])
def create_student():
    if missing_session(): return go_home()

    form = CreateForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
            admin=form.admin.data
        )

        try:
            user.save()
        except Exception as e:
            field = str(e).split('.')[2].split('[')[0]

            flash('Please choose a unique' + field, 'error')

    return render_template('user/create_student.html', form=form, session=session)


@mod_user.route('/dashboard', methods=['GET'])
def dashboard():
    if missing_session(): return go_home()

    user = User.query.get(session['user_id'])


@mod_user.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()

    return redirect(url_for('user.login'))

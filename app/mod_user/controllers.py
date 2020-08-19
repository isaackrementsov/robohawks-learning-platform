from flask import Flask, Blueprint, request, render_template, flash, session, redirect, url_for

from app.controllers import missing_session, go_home, go_dashboard, get_field

from app.mod_user.forms import LoginForm, CreateForm
from app.mod_user.models import User


mod_user = Blueprint('user', __name__, url_prefix='/user')


def create_session(user):
    session['user_id'] = user.id
    session['username'] = user.username
    session['avatar'] = user.avatar
    session['admin'] = user.admin


@mod_user.route('/login', methods['GET', 'POST'])
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



@mod_user.route('/manage', methods=['GET', 'POST', 'DELETE'])
def manage():
    if missing_session() or not is_admin(): go_home()

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
            flash('Please choose a unique' + get_field(e), 'error')
    elif request.args.get('id') and request.method == 'DELETE':
        user = User.lookup_id(request.args.get('id'))

        if user:
            try:
                user.delete()
            except Exception:
                flash('Error deleting user', 'error')

    return render_template('users/manage.html', form=form, session=session)


@mod_user.route('/dashboard', methods=['GET'])
def dashboard():
    if missing_session(): return go_home()

    user = User.lookup_id(session['user_id'])

    if user:
        return render_template('users/dashboard.html', user=user, session=session)
    else:
        raise Exception()


@mod_user.route('/account', methods=['GET', 'PATCH'])
def account():
    if missing_session(): return go_home()

    user = User.lookup_id(session['user_id'])

    if user:
        form = UpdateForm()

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
            except Exception:
                flash('There was an error validating your account')

        return render_template('user/account.html', form=form, user=user)

    else:
        raise Exception()


@mod_user.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()

    return redirect(url_for('user.login'))

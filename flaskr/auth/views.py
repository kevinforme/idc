from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user

from flaskr.auth.forms import LoginForm
from flaskr.models import User
from . import auth


@auth.before_app_request
def before_request():
    if current_user.is_anonymous and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(url_for('main.index'))
        flash('帐号或密码错误')
    return render_template('login.html', form=form)

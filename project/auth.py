from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, login_required, logout_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        u = User.query.filter_by(username=username).first()
        if u is not None and check_password_hash(u.password, password):
            # remember_me = True if request.form.get('remember') else False
            login_user(u)
            return redirect(url_for('main.index'))
        else:
            error = 'Неправильный логин или пароль'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form, error=error)


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST': # and form.validate()
        username = request.form['username']
        useremail = request.form['email']
        user_name = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=useremail).first()
        if user_name is not None:
            flash(f'Пользователь с именем: {username} уже существует')
            return render_template('registration.html', form=form)
        elif user_email is not None:
            flash(f'Пользователь с {useremail} уже существует')
            return render_template('registration.html', form=form)
        else:
            gener_password_hash = generate_password_hash(form.password.data)
            create_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                password=gener_password_hash
            )
            db.session.add(create_user)
            db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('registration.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

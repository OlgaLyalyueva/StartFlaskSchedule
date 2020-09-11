from flask import Flask, session, redirect, url_for, request, render_template, flash, abort
from flask_login import login_manager, LoginManager, login_user
from markupsafe import escape
from forms import RegistrationForm, LoginForm
from models import User
from database import db_session, init_db
from sqlalchemy.orm import query


app = Flask(__name__)
app.secret_key = b'\xcb6\x836\xf6\xdd\xadl\x0fB\xb8\x14\xaa\xd3\r>'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


@app.route('/notes')
def notes():
    return render_template('notes.html')


@app.route('/calendar')
def calendar():
    return render_template('calendar.html')


@app.route('/add_event')
def add_event(start_date, end_date, event):
    pass


@app.route('/user/<username>')
def profile(username):
    return 'Добро пожаловать в профиль, {}'.format(escape(username))


#################################################
# FLASK LOGIN MODULE !!!!!!
#################################################
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if request.method == 'POST' and form.validate():
#         if load_user(form.username.data) is None:
#             flash('Invalid username')
#             return render_template('login.html', title='Login', form=form)
#         else:
#             # first_name = load_user(form.username.data)
#             return render_template('schedule.html')
#     else:
#         # if check_password_hash(cred.password, form.password.data):
#         #     return redirect(url_for('browse'))
#         # else:
#             flash('Invalid password')
#             return render_template('login.html', title='Login', form=form)
#     return render_template('login.html', title='Login', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        u = User.query.filter_by(username=username, password=password).first()
        print(username, password, u)
        if u is not None:
            return schedule()
        else:
            error = 'Неправильный логин или пароль'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST': # and form.validate()
        init_db()
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
        db_session.add(user)
        db_session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#             return render_template('login.html', error=error)
#     else:
#         return show_the_registration_form()
#
#
# def valid_login(username, password):
#     if username == User.login:
#         login_user_id = User.get.id(login == username)
#         if password == User.password:
#             password_user_id = User.get.id(password == password)
#             if login_user_id == password_user_id:
#                 return 'True'
#
#
# @app.route('/logged/username')
# def log_the_user_in(username):
#     return render_template('logged.html', username)
#
#
# def show_the_registration_form():
#     return render_template('registration.html')




with app.test_request_context():
    print(url_for('profile', username='Маша Лялюева'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# @app.route('/user/<username>')
# def show_user_profile(username):
#     return 'Пользователь %s' % escape(username)


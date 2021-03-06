from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, validators, TimeField, DateField
from wtforms.fields.html5 import EmailField


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Фамилия', [validators.Length(min=1, max=150), validators.DataRequired()])
    username = StringField('Логин', [validators.Length(min=4, max=30), validators.DataRequired()])
    email = EmailField('Email', [validators.Length(min=6, max=35), validators.DataRequired()]) #add email validator , Email()
    password = PasswordField('Пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Подтвердите пароль')


class LoginForm(FlaskForm):
    username = StringField('Логин', [validators.DataRequired()])
    password = PasswordField('Пароль', [validators.DataRequired()])


class EventForm(FlaskForm):
    name = StringField('Название события', [validators.DataRequired(), validators.Length(100)])
    start_time = TimeField('Начало события', [validators.DataRequired()])
    end_time = TimeField('Окончание события', [validators.DataRequired()])
    day = DateField('День недели события', [validators.DataRequired()])
    description = StringField('Описание события')
    section = StringField('Раздел', [validators.DataRequired()])


class NoteForm(FlaskForm):
    description = StringField('Заметка', [validators.DataRequired(), validators.length(1000)])

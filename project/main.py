from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from .models import Event, User, Note
from .forms import EventForm, NoteForm
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/schedule')
def schedule():
    return render_template('schedule.html')


@main.route('/notes')
def notes():
    try:
        notes = Note.query.filter_by(user_id=current_user.user_id)
    except AttributeError:
        notes = None
    return render_template('notes.html', notes=notes)


@main.route('/calendar')
def calendar():
    return render_template('calendar.html')


@main.route('/add_event', methods=['GET', 'POST', 'DELETE'])
@login_required
def add_event():
    form = EventForm()
    event_name = request.form.get('event_name')
    day = request.form.get('day')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    event_description = request.form.get('event_description')
    section = request.form.get('section')
    event = Event.query.filter_by(name=event_name).first()
    if request.method == 'POST':
        if event is not None:
            update_event = Event(
                name=form.event_name.data,
                day=form.day,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                event_description=form.event_description.data,
                section=form.section.data
            )
            db.session.update(update_event)
            db.session.commit()
            return redirect(url_for('main.schedule'))
        else:
            user_id = User.query.get(10)
            create_event = Event(
                name=form.event_name.data,
                day=form.day.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                event_description=form.event_description.data,
                section=form.section.data,
                user_id=user_id
            )
            db.session.add(create_event)
            db.session.commit()
            return redirect(url_for('main.schedule'))
    if request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('main.schedule'))

    return render_template('add_event.html')


@main.route('/add_note', methods=['GET', 'POST', 'DELETE'])
@login_required
def add_note():
    form = NoteForm()
    description = request.form.get('description')
    note = Note.query.filter_by(description=description).first()

    if request.method == 'POST':
        if note is not None:
            print(form.description.data)
            note.description = form.description.data
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('main.notes'))
        else:
            create_note = Note(
                description = form.description.data,
                date_time = datetime.now(),
                user_id = current_user.user_id
            )
            db.session.add(create_note)
            db.session.commit()
            return redirect(url_for('main.notes'))
    elif request.method == 'DELETE':
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('main.notes'))

    url = True
    return render_template('notes.html', url=url, form=form)

import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Zone
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')

    return render_template("home.html", user=current_user)


# @views.route('/table', methods=['GET', 'POST'])
# @login_required
# def table():
#     # if request.method == 'POST':
#     #     note = request.form.get('note')
#     #     if len(note) < 1:
#     #         flash('Note is too short', category='error')
#     #     else:
#     #         new_note = Note(data=note, user_id=current_user.id)
#     #         db.session.add(new_note)
#     #         db.session.commit()
#     #         flash('Note Added!', category='success')
#
#     return render_template("table.html", notes=current_user.notes)

# Sample data for demonstration
zones = [
    {"client_name": "John Doe", "payload": "Data 1"},
    {"client_name": "Jane Smith", "payload": "Data 2"},
    # Add more data as needed
]


@views.route('/zones', methods=['GET', 'POST'])
@login_required
def zones_page():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        payload = request.form.get('payload')

        # zone = Zone.query.filter_by(client_name=client_name).first()
        # if zone:
        #     flash('Email Already Exist', category='error')
        if len(client_name) < 1:
            flash('client_name too short', category='error')
        elif len(payload) < 1:
            flash('payload too short', category='error')
        else:
            # add user to database
            new_zone = Zone(client_name=client_name,
                            payload=payload,
                            user_id=current_user.id
                            )
            print(client_name)
            print(payload)
            print(new_zone)
            db.session.add(new_zone)
            db.session.commit()
            print('Zone created')

            flash('Zone created!', category='success')
    print(current_user.zones)
    return render_template('zones.html', zones=current_user.zones)



@views.route('/update_zone/<int:index>', methods=['POST'])
def update_zone(index):
    new_client_name = request.json.get('new_client_name')

    # Update the database here using your ORM or SQL commands
    zones[index]['client_name'] = new_client_name

    # You might want to wrap the database update logic in try-except and handle errors

    return jsonify({'success': True})


@views.route('/delete-zone', methods=['POST'])
def delete_zone():
    zone = json.loads(request.data)
    zone_id = zone['zoneId']
    zone = Zone.query.get(zone_id)
    if zone:
        if zone.user_id == current_user.id:
            db.session.delete(zone)
            db.session.commit()
    return jsonify({})


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

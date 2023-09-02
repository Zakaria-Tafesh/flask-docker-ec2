import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Zone
from . import db

views = Blueprint('views', __name__)


# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == 'POST':
#         note = request.form.get('note')
#         if len(note) < 1:
#             flash('Note is too short', category='error')
#         else:
#             new_note = Note(data=note, user_id=current_user.id)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note Added!', category='success')
#
#     return render_template("home.html", user=current_user)



@views.route('/', methods=['GET', 'POST'])
@login_required
def zones_page():
    if request.method == 'POST':
        client_name = request.form.get('client_name')
        url = request.form.get('url')
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
                            url=url,
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
    return render_template('zones.html', user=current_user, zones=current_user.zones)



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


@views.route('/update-zone1', methods=['POST'])
def update_zone1():
    zone = json.loads(request.data)
    zone_id = zone['zoneId']
    zone = Zone.query.get(zone_id)

    if zone:
        if zone.user_id == current_user.id:
            return jsonify({'client_name': zone.client_name,
                            'url': zone.url,
                            'payload': zone.payload})

    # return 'Zakaria'
    # return jsonify({'1': 'Zakaria'})

@views.route('/update-zone2', methods=['POST'])
def update_zone2():
    zone = json.loads(request.data)
    zone_id = zone['zone_id']
    client_name = zone['client_name']
    url = zone['url']
    payload = zone['payload']

    zone = Zone.query.get(zone_id)

    if zone:
        if zone.user_id == current_user.id:
            zone.client_name = client_name
            zone.url = url
            zone.payload = payload
            db.session.commit()
            return jsonify({'client_name': zone.client_name,
                            'url': zone.url,
                            'payload': zone.payload})

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10_000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(20))
    url = db.Column(db.String(4000))
    payload = db.Column(db.String(20_000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', back_populates='zones')  # Add this line

    def __repr__(self):
        return str({'id': self.id,
                'client_name': self.client_name,
                'url': self.url,
                'payload': self.payload,
                'date': self.date,
                'user_id': self.user_id,

                })


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    zones = db.relationship('Zone')

    def __repr__(self):
        return str({'id': self.id,
                'email': self.email,
                'password': self.password,
                'first_name': self.first_name,
                'notes': self.notes,
                'zones': self.zones,

                })


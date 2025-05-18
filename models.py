from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)
    is_banned = db.Column(db.Boolean, default=False)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_starttime = db.Column(db.Time, nullable=False)
    event_endtime = db.Column(db.Time, nullable=False)
    registration_start_date = db.Column(db.Date, nullable=False)
    registration_end_date = db.Column(db.Date, nullable=False)
    registration_starttime = db.Column(db.Time, nullable=False)
    registration_endtime = db.Column(db.Time, nullable=False)

    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    update_info = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
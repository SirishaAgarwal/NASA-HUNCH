from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # admin or user

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    expiration_date = db.Column(db.Date, nullable=True)
    checked_out = db.Column(db.Integer, default=0)
    last_checked_out = db.Column(db.DateTime, nullable=True)

class CrewMedicalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crew_name = db.Column(db.String(100), nullable=False)
    crew_id = db.Column(db.String(50), nullable=False)
    allergies = db.Column(db.Text, nullable=True)
    conditions = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.String(150), nullable=True)
    dosage = db.Column(db.String(100), nullable=True)
    prescribing_doctor = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start = db.Column(db.String(30), nullable=False)
    end = db.Column(db.String(30), nullable=True)
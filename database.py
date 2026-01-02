import json # Add this at the top
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    scans = db.relationship('History', backref='owner', lazy=True, cascade="all, delete-orphan")

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    score = db.Column(db.Float)
    # NEW: Store the full ML result dictionary as a JSON string
    full_report_json = db.Column(db.Text) 
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def get_report(self):
        return json.loads(self.full_report_json) if self.full_report_json else {}
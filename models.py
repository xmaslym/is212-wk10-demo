from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(20), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

from flask import Flask, jsonify, request

from booking_service import BookingError, create_booking, extend_booking
from models import Booking, db
from utils import parse_slot


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config.update(config or {})
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if not app.config.get("TESTING"):
            seed_demo_bookings()

    @app.errorhandler(BookingError)
    def handle_booking_error(err):
        return jsonify({"error": str(err)}), err.status

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    @app.get("/bookings")
    def list_bookings():
        bookings = Booking.query.order_by(Booking.start).all()
        return jsonify([booking_to_json(b) for b in bookings])

    @app.post("/bookings")
    def post_booking():
        body = request.get_json()
        b = create_booking(body["room"], body["student"], body["start"], body["end"])
        return jsonify({"id": b.id}), 201

    @app.patch("/bookings/<int:booking_id>")
    def patch_booking(booking_id):
        b = extend_booking(booking_id, request.get_json()["end"])
        return jsonify({"id": b.id, "end": b.end.isoformat()}), 200

    return app


def booking_to_json(b):
    return {"id": b.id, "room": b.room_id, "student": b.student_id,
            "start": b.start.isoformat(timespec="minutes"), "end": b.end.isoformat(timespec="minutes")}


def seed_demo_bookings():
    """Demo data for the UI (not used by the tests). Booking 1 matches the PR #57 example."""
    for room, student, start, end in [
        ("GSR-2-01", "s1", "2026-10-20T10:00", "2026-10-20T11:00"),
        ("GSR-2-01", "s2", "2026-10-20T12:00", "2026-10-20T13:00"),
        ("GSR-2-02", "s3", "2026-10-20T14:00", "2026-10-20T16:00"),
    ]:
        db.session.add(Booking(room_id=room, student_id=student, start=parse_slot(start), end=parse_slot(end)))
    db.session.commit()

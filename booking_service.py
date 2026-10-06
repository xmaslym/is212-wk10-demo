from datetime import datetime, timedelta

from models import Booking, db
from utils import parse_slot

MAX_DURATION = timedelta(hours=2)


class BookingError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def create_booking(room_id, student_id, start, end):
    start, end = parse_slot(start), parse_slot(end)
    if end - start > MAX_DURATION:
        raise BookingError("Bookings are limited to 2 hours")
    clash = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.start < end,
        Booking.end > start,
    ).first()
    if clash:
        raise BookingError("Room is not available", status=409)
    booking = Booking(room_id=room_id, student_id=student_id, start=start, end=end)
    db.session.add(booking)
    db.session.commit()
    return booking


def extend_booking(booking_id, new_end):
    booking = db.get_or_404(Booking, booking_id)
    end = _to_datetime(new_end)
    if end - booking.start > MAX_DURATION:
        raise BookingError("Bookings are limited to 2 hours")
    clash = Booking.query.filter(
        Booking.room_id == booking.room_id,
        Booking.id != booking.id,
        Booking.start <= end,
        Booking.end > booking.start,
    ).first()
    if clash:
        raise BookingError("Room is not available", status=409)
    booking.end = end
    db.session.commit()
    return booking


def _to_datetime(value):
    return datetime.strptime(value, "%Y-%m-%dT%H:%M")

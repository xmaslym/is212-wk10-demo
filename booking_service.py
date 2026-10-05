from datetime import timedelta

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

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


@pytest.fixture
def booked_room(client):
    client.post("/bookings", json={"room": "GSR-2-01", "student": "s1",
                                   "start": "2026-10-20T10:00", "end": "2026-10-20T11:00"})
    return "GSR-2-01"

def test_booking_within_two_hours_is_created(client):
    resp = client.post("/bookings", json={"room": "GSR-2-01", "student": "s1",
                                          "start": "2026-10-20T10:00", "end": "2026-10-20T12:00"})
    assert resp.status_code == 201


def test_overlapping_booking_is_rejected(client, booked_room):
    resp = client.post("/bookings", json={"room": booked_room, "student": "s2",
                                          "start": "2026-10-20T10:30", "end": "2026-10-20T11:30"})
    assert resp.status_code == 409
    assert resp.get_json() == {"error": "Room is not available"}


def test_back_to_back_booking_is_allowed(client, booked_room):
    resp = client.post("/bookings", json={"room": booked_room, "student": "s2",
                                          "start": "2026-10-20T11:00", "end": "2026-10-20T12:00"})
    assert resp.status_code == 201


def test_extend_booking_within_limit(client, booked_room):
    resp = client.patch("/bookings/1", json={"end": "2026-10-20T11:30"})
    assert resp.status_code == 200


def test_extend_into_next_booking_is_rejected(client, booked_room):
    client.post("/bookings", json={"room": booked_room, "student": "s2",
                                   "start": "2026-10-20T12:00", "end": "2026-10-20T13:00"})
    resp = client.patch("/bookings/1", json={"end": "2026-10-20T12:00"})
    assert resp.status_code == 409

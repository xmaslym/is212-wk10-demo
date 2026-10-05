# Study-Room Booking – IS212 Week 10 running example

A small Flask + SQLAlchemy app used in the Week 10 lecture, *Agentic AI and the Software Team*.
It lets students book campus group study rooms (GSRs), through a small web page or the JSON API.

## The booking rules (from the slides)

1. A booking lasts at most 2 hours.
2. Rooms can be booked up to 7 days ahead.
3. Back-to-back bookings are fine; overlapping ones are not.
4. Cancelling less than 2 hours before the start records a late-cancellation strike.

The code on `main` implements rules 1 and 3 for creating a booking. Rules 2 and 4 are not implemented –
rule 4 belongs to the "cancel a booking" story used in the lecture demo.

## What's in the repository

This folder is a git repository with two branches:

| Branch | What it contains |
|---|---|
| `main` | The app before PR #57: list and create bookings, a simple web UI, and 3 tests |
| `agent/extend-booking` | PR #57 from the lecture, written by a coding agent: extend an existing booking (2 commits, 3 files changed, 5 tests) |

The same change is also provided as a plain diff in `pr-57.diff` (next to this folder in the zip), if you'd rather read it without git.

`extras/` contains the two examples from the "guidance vs enforcement" slide: an `AGENTS.md` with testing rules, and a CI step that rejects pull requests that change existing tests. They are **not** active in this repository.

## Running it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

flask --app app run              # then open http://127.0.0.1:5000
pytest -q                        # main: 3 passed

git checkout agent/extend-booking
flask --app app run              # the "Extend" button now works
pytest -q                        # PR #57: 5 passed
git diff main...agent/extend-booking
```

Python 3.11 or later is fine (the CI workflow uses 3.13).

### The web UI

Open http://127.0.0.1:5000 after `flask --app app run`. It shows a day view of the rooms on 20 Oct 2026, a form to book a room, a form to extend a booking, and the last request and response the page sent to the API – so you can see exactly what the server returned (e.g. `409 {"error": "Room is not available"}`).

- Data is kept in memory: restarting the server resets it.
- The server starts with three demo bookings. Booking #1 (GSR-2-01, 10:00–11:00) is the one from the PR #57 example; booking #2 starts at 12:00 in the same room.
- Extending only works on the `agent/extend-booking` branch. On `main` the page tells you the endpoint doesn't exist.
- The UI and the demo data are only there for exploring – the tests don't use them.

## PR #57 – the story

> As a student, I want to extend my booking so that I can keep the room if I need more time.

- **AC1** Still at most 2 hours in total
- **AC2** Must not overlap another booking of the same room

All checks pass on the branch. Review it as if you were approving it for your team.

## Things to try

- In the UI, on the PR branch, try extending booking #1 to end at 12:00 – exactly when booking #2 starts. Is the response what the booking rules say it should be?
- Write a test showing that extending a booking to end exactly when the next booking starts should be **allowed** (rule 3). Does it pass on the PR branch? What is the smallest fix?
- Compare `_to_datetime()` in `booking_service.py` with `parse_slot()` in `utils.py`. Find an input that one accepts and the other rejects.
- Look at what changed in `tests/test_booking_api.py`. What does the modified test no longer check?
- Push the repository to your own GitHub account, add the step from `extras/test-protection-step.yml` to the CI workflow on `main`, and open a pull request from `agent/extend-booking`. Which of the three problems does the check catch – and which does it miss?
- Use the delegation dial from the lecture: at which autonomy level should a change like PR #57 have been allowed to merge, and with what checkpoint?
